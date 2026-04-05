"""
Configuration settings for the Agentic AI system.
"""
from pydantic_settings import BaseSettings
from pathlib import Path

# Find the .env file in the package directory
PACKAGE_DIR = Path(__file__).parent
ENV_FILE = PACKAGE_DIR / ".env"


class Settings(BaseSettings):
    # Scoring thresholds (thang điểm 10, deterministic analyzer)
    WEAK_TOPIC_THRESHOLD: float = 8.0  # Dưới 8.0/10 được xem là yếu
    MINIMUM_SUBJECT_SCORE: float = 8.0  # Môn không thi cần tối thiểu 8.0/10

    # Psychology interpretation thresholds (1-7 scale)
    LOW_THRESHOLD: float = 3.0
    HIGH_THRESHOLD: float = 5.0

    class Config:
        env_file = str(ENV_FILE)
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
