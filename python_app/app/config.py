from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    mistral_api_key: str = os.getenv("MISTRAL_API_KEY", "").strip()
    mistral_model: str = os.getenv("MISTRAL_MODEL", "mistral-small-latest").strip()


settings = Settings()