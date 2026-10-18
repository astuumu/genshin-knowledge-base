import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from database import Base


class UserRoleEnum(str, enum.Enum):
    USER = "user"
    MODERATOR = "moderator"


class ElementEnum(str, enum.Enum):
    PYRO = "Pyro"
    HYDRO = "Hydro"
    CRYO = "Cryo"
    ELECTRO = "Electro"
    DENDRO = "Dendro"
    ANEMO = "Anemo"
    GEO = "Geo"


class WeaponTypeEnum(str, enum.Enum):
    SWORD = "Sword"
    CLAYMORE = "Claymore"
    POLEARM = "Polearm"
    BOW = "Bow"
    CATALYST = "Catalyst"


class WeaponPriorityEnum(str, enum.Enum):
    SIGNATURE = "Signature"
    BEST_ALTERNATIVE = "Best Alternative"
    F2P_OPTION = "F2P Option"
    BUDGET = "Budget"


class ArtifactSetTypeEnum(str, enum.Enum):
    FOUR_PIECE = "4-Piece"
    TWO_PIECE = "2-Piece Combo"


class TeamRoleEnum(str, enum.Enum):
    MAIN_DPS = "Main DPS"
    SUB_DPS = "Sub DPS"
    SUPPORT = "Support"
    HEALER = "Healer"
    SHIELDER = "Shielder"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), nullable=False)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    replies = relationship("ReviewReply", back_populates="user", cascade="all, delete-orphan")


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    element = Column(Enum(ElementEnum), nullable=False)
    weapon_type = Column(Enum(WeaponTypeEnum), nullable=False)
    rarity = Column(Integer, nullable=False)
    region = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    builds = relationship("Build", back_populates="character", cascade="all, delete-orphan")
    team_members = relationship("TeamMember", back_populates="character", cascade="all, delete-orphan")


class Weapon(Base):
    __tablename__ = "weapons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    weapon_type = Column(Enum(WeaponTypeEnum), nullable=False)
    rarity = Column(Integer, nullable=False)
    base_attack = Column(Integer, nullable=False)
    substat = Column(String(100), nullable=True)
    passive_desc = Column(Text, nullable=True)

    build_weapons = relationship("BuildWeapon", back_populates="weapon", cascade="all, delete-orphan")


class ArtifactSet(Base):
    __tablename__ = "artifact_sets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    two_piece_bonus = Column(Text, nullable=True)
    four_piece_bonus = Column(Text, nullable=True)

    build_artifacts = relationship("BuildArtifactSet", back_populates="artifact_set", cascade="all, delete-orphan")


class Build(Base):
    __tablename__ = "builds"

    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
    role_title = Column(String(100), nullable=False)
    stats_priority = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)

    character = relationship("Character", back_populates="builds")
    weapons = relationship("BuildWeapon", back_populates="build", cascade="all, delete-orphan")
    artifact_sets = relationship("BuildArtifactSet", back_populates="build", cascade="all, delete-orphan")


class BuildWeapon(Base):
    __tablename__ = "build_weapons"

    id = Column(Integer, primary_key=True, index=True)
    build_id = Column(Integer, ForeignKey("builds.id", ondelete="CASCADE"), nullable=False)
    weapon_id = Column(Integer, ForeignKey("weapons.id", ondelete="CASCADE"), nullable=False)
    priority = Column(Enum(WeaponPriorityEnum), default=WeaponPriorityEnum.BEST_ALTERNATIVE, nullable=False)
    notes = Column(String(255), nullable=True)

    build = relationship("Build", back_populates="weapons")
    weapon = relationship("Weapon", back_populates="build_weapons")


class BuildArtifactSet(Base):
    __tablename__ = "build_artifact_sets"

    id = Column(Integer, primary_key=True, index=True)
    build_id = Column(Integer, ForeignKey("builds.id", ondelete="CASCADE"), nullable=False)
    artifact_set_id = Column(Integer, ForeignKey("artifact_sets.id", ondelete="CASCADE"), nullable=False)
    set_type = Column(Enum(ArtifactSetTypeEnum), default=ArtifactSetTypeEnum.FOUR_PIECE, nullable=False)
    notes = Column(String(255), nullable=True)

    build = relationship("Build", back_populates="artifact_sets")
    artifact_set = relationship("ArtifactSet", back_populates="build_artifacts")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    team_type = Column(String(50), default="Meta", nullable=False)
    description = Column(Text, nullable=True)

    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False)
    role = Column(Enum(TeamRoleEnum), default=TeamRoleEnum.SUPPORT, nullable=False)
    notes = Column(String(255), nullable=True)

    team = relationship("Team", back_populates="members")
    character = relationship("Character", back_populates="team_members")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    target_type = Column(String(50), default="none", nullable=False)
    target_id = Column(Integer, nullable=True)
    target_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="reviews")
    replies = relationship("ReviewReply", back_populates="review", cascade="all, delete-orphan")


class ReviewReply(Base):
    __tablename__ = "review_replies"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    reply_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="replies")
    review = relationship("Review", back_populates="replies")