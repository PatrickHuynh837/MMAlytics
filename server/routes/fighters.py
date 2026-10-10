from fastapi import APIRouter
from sqlalchemy import text
from server.database import engine


router = APIRouter(
    prefix="/fighters",
    tags=["fighters"]
)


# Defines a GET endpoint at /fighters
@router.get("/")
def get_fighters():
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    fighter_url,
                    fighter_f_name || ' ' || fighter_l_name AS fighter_name,
                    fighter_nickname,
                    NULLIF(fighter_height_cm, 'NaN'::double precision) AS fighter_height_cm,
                    NULLIF(fighter_weight_lbs, 'NaN'::double precision) AS fighter_weight_lbs,
                    NULLIF(fighter_reach_cm, 'NaN'::double precision) AS fighter_reach_cm,
                    fighter_stance,
                    fighter_w,
                    fighter_l,
                    fighter_d
                FROM raw.fighter_data
                ORDER BY fighter_l_name, fighter_f_name
            """)
        )

        fighters = [dict(row._mapping) for row in result]

    return fighters