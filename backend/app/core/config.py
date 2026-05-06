import os
from functools import lru_cache

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Ebook2LateX"
    database_url: str = os.getenv(
        "DATABASE_URL",
        os.getenv(
            "DB_URL",
            "postgresql+psycopg2://postgres:123asd@localhost:5432/ebook2latex_db",
        ),
    )
    api_key: str = os.getenv("API_KEY", "")
    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
