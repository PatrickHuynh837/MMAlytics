from fastapi import APIRouter
from sqlalchemy import text
from server.database import engine

router = APIRouter(
    prefix="/fights",
    tags=["fights"]
)


@router.get("/")
def get_fights(event_url: str):
    print(f"Received event_url: {event_url}")

    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    fight_url,
                    fighter_1,
                    fighter_2,
                    weight_class
                FROM ml.fight_dataset
                WHERE event_url = :event_url
            """),
            {"event_url": event_url}
        )

        fights = [dict(row._mapping) for row in result]

    print(f"Number of fights found: {len(fights)}")
    print(f"Fights returned: {fights}")

    return fights



