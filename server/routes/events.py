from fastapi import APIRouter
from sqlalchemy import text
from server.database import engine

router = APIRouter(
    prefix="/events",
    tags=["events"]
)

@router.get("/")
def get_events():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    event_url,
                    event_name,
                    event_date,
                    location_city,
                    location_state,
                    location_country
                FROM raw.event_data
                ORDER BY event_date DESC
            """)
        )

        events = [dict(row._mapping) for row in result]

    return events

