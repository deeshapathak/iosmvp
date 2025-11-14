import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Rhinovate API"
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    # put your model paths here if you add beauty models
    AESTHETIC_MODEL_PATH: str = os.getenv("AESTHETIC_MODEL_PATH", "")

    class Config:
        case_sensitive = False


settings = Settings()

