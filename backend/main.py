from datetime import datetime, timedelta, timezone
from typing import List, Optional

import jwt
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from google.auth.transport import requests
from google.oauth2 import id_token
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, joinedload

from config import GOOGLE_CLIENT_ID, JWT_SECRET, MODERATOR_EMAILS
from database import Base, engine, get_db
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Genshin Hub API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GoogleAuthRequest(BaseModel):
    token: str


class CharacterCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    element: models.ElementEnum
    weapon_type: models.WeaponTypeEnum
    rarity: int = Field(..., ge=4, le=5)
    region: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class CharacterUpdateDTO(BaseModel):
    description: str
    region: str


class BuildCreateUpdateDTO(BaseModel):
    role_title: str = Field(..., min_length=1, max_length=100)
    stats_priority: str
    notes: Optional[str] = None


class TeamMemberDTO(BaseModel):
    character_id: int
    role: models.TeamRoleEnum
    notes: Optional[str] = None


class TeamCreateUpdateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    team_type: str = Field(default="Meta", max_length=50)
    description: Optional[str] = None
    members: List[TeamMemberDTO]


class ReviewCreateDTO(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=1)
    target_type: Optional[str] = "none"
    target_id: Optional[int] = None
    target_name: Optional[str] = None


class ReplyCreateDTO(BaseModel):
    reply_text: str = Field(..., min_length=1)


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> models.User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session token is missing"
        )

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        email = payload.get("email")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token payload missing email"
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session token"
        )

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not registered"
        )
    return user


def require_moderator(current_user: models.User = Depends(get_current_user)) -> models.User:
    if current_user.role != models.UserRoleEnum.MODERATOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Moderator privileges required"
        )
    return current_user


@app.post("/api/v1/auth/google")
def google_authentication(auth_data: GoogleAuthRequest, db: Session = Depends(get_db)):
    try:
        id_info = id_token.verify_oauth2_token(
            auth_data.token,
            requests.Request(),
            GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10
        )
        email = id_info.get("email")
        name = id_info.get("name", email.split("@")[0] if email else "User")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google token verification failed: {str(exc)}"
        )

    assigned_role = (
        models.UserRoleEnum.MODERATOR
        if email in MODERATOR_EMAILS
        else models.UserRoleEnum.USER
    )

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        user = models.User(email=email, username=name, role=assigned_role)
        db.add(user)
        db.commit()
        db.refresh(user)
    elif user.role != assigned_role:
        user.role = assigned_role
        db.commit()

    expiration = datetime.now(timezone.utc) + timedelta(hours=24)
    session_token = jwt.encode(
        {"email": user.email, "role": user.role.value, "exp": expiration},
        JWT_SECRET,
        algorithm="HS256"
    )

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role.value
        },
        "token": session_token
    }


@app.get("/api/v1/characters")
def list_characters(db: Session = Depends(get_db)):
    characters = db.query(models.Character).all()
    return {"data": characters}


@app.get("/api/v1/characters/{character_id}")
def get_character_profile(character_id: int, db: Session = Depends(get_db)):
    character = (
        db.query(models.Character)
        .options(
            joinedload(models.Character.builds)
            .joinedload(models.Build.weapons)
            .joinedload(models.BuildWeapon.weapon),
            joinedload(models.Character.builds)
            .joinedload(models.Build.artifact_sets)
            .joinedload(models.BuildArtifactSet.artifact_set),
        )
        .filter(models.Character.id == character_id)
        .first()
    )
    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")
    return {"data": character}


@app.post("/api/v1/characters", status_code=status.HTTP_201_CREATED)
def create_character(
    payload: CharacterCreateDTO,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_moderator)
):
    existing = db.query(models.Character).filter(models.Character.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Character already exists")

    new_character = models.Character(**payload.model_dump())
    db.add(new_character)
    db.commit()
    db.refresh(new_character)
    return {"data": new_character}


@app.put("/api/v1/characters/{character_id}")
def update_character(
    character_id: int,
    payload: CharacterUpdateDTO,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_moderator)
):
    character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")

    character.description = payload.description
    character.region = payload.region
    db.commit()
    db.refresh(character)
    return {"data": character}


@app.delete("/api/v1/characters/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(
    character_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_moderator)
):
    character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")

    db.delete(character)
    db.commit()
    return None


@app.post("/api/v1/characters/{character_id}/builds", status_code=status.HTTP_201_CREATED)
def create_build(
    character_id: int,
    payload: BuildCreateUpdateDTO,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_moderator)
):
    character = db.query(models.Character).filter(models.Character.id == character_id).first()
    if not character:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Character not found")

    new_build = models.Build(
        character_id=character_id,
        role_title=payload.role_title,
        stats_priority=payload.stats_priority,
        notes=payload.notes
    )
    db.add(new_build)
    db.commit()
    db.refresh(new_build)
    return {"data": new_build}


@app.put("/api/v1/builds/{build_id}")
def update_build(
    build_id: int,
    payload: BuildCreateUpdateDTO,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_moderator)
):
    build = db.query(models.Build).filter(models.Build.id == build_id).first()
    if not build:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Build not found")

    build.role_title = payload.role_title
    build.stats_priority = payload.stats_priority
    build.notes = payload.notes
    db.commit()
    db.refresh(build)
    return {"data": build}


@app.delete("/api/v1/builds/{build_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_build(
    build_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_moderator)
):
    build = db.query(models.Build).filter(models.Build.id == build_id).first()
    if not build:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Build not found")

    db.delete(build)
    db.commit()
    return None


@app.get("/api/v1/teams")
def list_teams(db: Session = Depends(get_db)):
    teams = (
        db.query(models.Team)
        .options(joinedload(models.Team.members).joinedload(models.TeamMember.character))
        .all()
    )
    return {"data": teams}


@app.post("/api/v1/teams", status_code=status.HTTP_201_CREATED)
def create_team(
    payload: TeamCreateUpdateDTO,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_moderator)
):
    if len(payload.members) != 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A team composition must contain exactly 4 character slots"
        )

    team = models.Team(
        name=payload.name,
        team_type=payload.team_type,
        description=payload.description
    )
    db.add(team)
    db.commit()
    db.refresh(team)

    for member_data in payload.members:
        member = models.TeamMember(
            team_id=team.id,
            character_id=member_data.character_id,
            role=member_data.role,
            notes=member_data.notes
        )
        db.add(member)

    db.commit()
    return {"data": team}


@app.put("/api/v1/teams/{team_id}")
def update_team(
    team_id: int,
    payload: TeamCreateUpdateDTO,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_moderator)
):
    if len(payload.members) != 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A team composition must contain exactly 4 character slots"
        )

    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    team.name = payload.name
    team.team_type = payload.team_type
    team.description = payload.description

    db.query(models.TeamMember).filter(models.TeamMember.team_id == team_id).delete()

    for member_data in payload.members:
        member = models.TeamMember(
            team_id=team.id,
            character_id=member_data.character_id,
            role=member_data.role,
            notes=member_data.notes
        )
        db.add(member)

    db.commit()
    return {"data": team}


@app.delete("/api/v1/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(
    team_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_moderator)
):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    db.delete(team)
    db.commit()
    return None


@app.get("/api/v1/reviews")
def list_reviews(db: Session = Depends(get_db)):
    reviews = (
        db.query(models.Review)
        .options(
            joinedload(models.Review.user),
            joinedload(models.Review.replies).joinedload(models.ReviewReply.user)
        )
        .order_by(models.Review.created_at.desc())
        .all()
    )
    return {"data": reviews}


@app.post("/api/v1/reviews", status_code=status.HTTP_201_CREATED)
def create_review(
    payload: ReviewCreateDTO,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    review = models.Review(
        user_id=current_user.id,
        rating=payload.rating,
        comment=payload.comment,
        target_type=payload.target_type or "none",
        target_id=payload.target_id,
        target_name=payload.target_name
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return {"data": review}


@app.post("/api/v1/reviews/{review_id}/replies", status_code=status.HTTP_201_CREATED)
def create_reply(
    review_id: int,
    payload: ReplyCreateDTO,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    reply = models.ReviewReply(
        review_id=review_id,
        user_id=current_user.id,
        reply_text=payload.reply_text
    )
    db.add(reply)
    db.commit()
    db.refresh(reply)
    return {"data": reply}


@app.delete("/api/v1/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(require_moderator)
):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    db.delete(review)
    db.commit()
    return None