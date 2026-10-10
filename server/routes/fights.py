from fastapi import APIRouter
from sqlalchemy import text
from server.database import engine


router = APIRouter(
    prefix="/fights",
    tags=["fights"]
)



@router.get("/")
def get_fights(event_url: str | None = None):
    query = """
        SELECT
            fight_url,
            event_url,
            event_name,
            event_date,
            fighter_1,
            fighter_1_url,
            fighter_2,
            fighter_2_url,
            weight_class,
            gender,
            title_fight,
            num_rounds,
            winner,
            result,
            finish_round,
            finish_time
        FROM ml.fight_dataset
    """

    params = {}

    if event_url:
        query += " WHERE event_url = :event_url"
        params["event_url"] = event_url

    query += " ORDER BY event_date DESC, fight_url"

    with engine.connect() as connection:
        result = connection.execute(text(query), params)
        fights = [dict(row._mapping) for row in result]

    return fights
