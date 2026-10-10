
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine


# Load environment variables from the project root
load_dotenv(
    Path(__file__).resolve().parents[1] / ".env"
)


# Get database URL
DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError(
        "DB_URL is missing from environment variables"
    )


# Create SQLAlchemy engine
engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

