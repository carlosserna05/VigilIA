from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os

class Settings(BaseSettings):
    app_name: str = Field(default="VigilIA", env="APP_NAME")
    app_version: str = Field(default="0.1.0", env="APP_VERSION")
    debug: bool = Field(default=True, env="DEBUG")

    database_url: str = Field(default="sqlite:///./data/database.db", env="DATABASE_URL")

    secret_key: str = Field(default="vigilia2105", env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=43200,env="ACCESS_TOKEN_EXPIRES_MINUTES")

    detection_interval: int=Field(default=10,env="DETECTION_INTERVAL")
    max_cameras_per_user:int=Field(default=3, env="MAX_CAMERAS_PER_USER")
    face_recognition_threshold: float = Field(default=0.6,env = "FACE_RECOGNITION_THRESHOLD")

    known_faces_dir: str = Field(default="./data/known_faces", env="KNOWN_FACES_DIR")
    alerts_dir: str= Field(default = "./data/alerts", env="ALERTS_DIR")

    telegram_bot_token: Optional[str] = Field(default=None, env="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: Optional[str] = Field(default=None, env="TELEGRAM_CHAT_ID")

    firebase_credentials_path: Optional[str] = Field(default=None, env="FIREBASE_CREDENTIALS_PATH")

    host: str = Field(default="0.0.0.0", env="HOST")
    port: int= Field(default=8000, env="PORT")

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, *kwargs):
        super().__init__(*kwargs)
        # Ensure directories exist
        os.makedirs(self.known_faces_dir, exist_ok=True)
        os.makedirs(self.alerts_dir, exist_ok=True)
        os.makedirs("./data", exist_ok=True)

settings = Settings()