import os
from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import BaseModel


def required_env(name):
    value = os.getenv(name)
    if value is None:
        raise Exception(f"Environment variable {name} is required")
    return value


BASE_DIR = Path(__file__).parent.parent
DB_HOST = required_env("DB_HOST")
DB_USER = required_env("DB_USER")
DB_PASSWORD = required_env("DB_PASSWORD")
DB_NAME = required_env("DB_NAME")
EMAIL_PASSWORD = required_env("EMAIL_PASSWORD")
EMAIL_SENDER = required_env("EMAIL_SENDER")


class DbSettings(BaseModel):
    url: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    echo: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    # access_token_expire_minutes: int = 3


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    email_password: str = EMAIL_PASSWORD
    image_directory: Path = BASE_DIR / "images"
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()
    nearest_distance: int = 3000
    email_sender: str = EMAIL_SENDER


settings = Settings()