from pathlib import Path
from typing import List

from pydantic import BaseSettings, Field

BASE_DIR: Path = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    PROJECT_NAME: str = "Vendor"

    ALLOWED_HOSTS: List = Field(default=['*'])

    DB_URL: str
    DB_SCHEMA: str

    class Config:
        env_file = str(BASE_DIR / '.env')
        env_prefix = 'VENDOR_'
        case_sensitive = True


settings = Settings()
