import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
JWT_SECRET = os.getenv("JWT_SECRET", "default_insecure_secret_key")

_raw_moderators = os.getenv("MODERATOR_EMAILS", "")
MODERATOR_EMAILS = [email.strip() for email in _raw_moderators.split(",") if email.strip()]