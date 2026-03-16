"""
Configuration settings for the Agentic AI system.
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

# Find the .env file in the package directory
PACKAGE_DIR = Path(__file__).parent
ENV_FILE = PACKAGE_DIR / ".env"


class Settings(BaseSettings):
    # LLM Configuration
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None

    # Default LLM provider and model
    LLM_PROVIDER: str = "anthropic"  # "anthropic" or "openai"
    LLM_MODEL: str = "claude-sonnet-4-20250514"

    # Agent Configuration
    MAX_AGENT_ITERATIONS: int = 10
    AGENT_TIMEOUT_SECONDS: int = 600  # 10 minutes for LLM calls

    # Scoring thresholds (thang điểm 10)
    WEAK_TOPIC_THRESHOLD: float = 8.0  # Dưới 8.0/10 được xem là yếu
    MINIMUM_SUBJECT_SCORE: float = 8.0  # Môn không thi cần tối thiểu 8.0/10

    # Path duration settings
    REMEDIAL_PATH_MIN_WEEKS: int = 4
    REMEDIAL_PATH_MAX_WEEKS: int = 8
    STRATEGIC_PATH_MIN_MONTHS: int = 12
    STRATEGIC_PATH_MAX_MONTHS: int = 24

    # Psychology interpretation thresholds (1-7 scale)
    LOW_THRESHOLD: float = 3.0
    HIGH_THRESHOLD: float = 5.0

    class Config:
        env_file = str(ENV_FILE)
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
