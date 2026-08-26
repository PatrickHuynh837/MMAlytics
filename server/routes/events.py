import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter
from sqlalchemy import create_engine, text

load_dotenv(
    Path(__file__).resolve().parents[2] / ".env"
)

DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError("DB_URL is missing from environment variables")

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

router = APIRouter(
    prefix="/events",
    tags=["events"]
)


@router.get("/")
def get_events():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT *
                FROM events
                ORDER BY event_date DESC
            """)
        )

        events = [dict(row._mapping) for row in result]

    return events