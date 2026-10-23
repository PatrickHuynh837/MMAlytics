
from fastapi import APIRouter
from sqlalchemy import text
from server.database import engine


router = APIRouter(
    prefix="/fight-details",
    tags=["fight-details"]
)


@router.get("/")
def get_fight_details(fight_url: str):
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT
                    -- Fight data
                    fight_url,
                    event_name,
                    referee,
                    fighter_1,
                    fighter_2,
                    fighter_1_url,
                    fighter_2_url,
                    winner,
                    num_rounds,
                    title_fight,
                    gender,
                    result,
                    result_details,
                    finish_round,
                    finish_time,
                    weight_class,

                    -- Fighter 1 fight statistics
                    fighter_1_knockdowns,
                    fighter_1_total_strikes_att,
                    fighter_1_total_strikes_succ,
                    fighter_1_sig_strikes_att,
                    fighter_1_sig_strikes_succ,
                    fighter_1_takedown_att,
                    fighter_1_takedown_succ,
                    fighter_1_submission_att,
                    fighter_1_reversals,
                    fighter_1_ctrl_time,

                    -- Fighter 2 fight statistics
                    fighter_2_knockdowns,
                    fighter_2_total_strikes_att,
                    fighter_2_total_strikes_succ,
                    fighter_2_sig_strikes_att,
                    fighter_2_sig_strikes_succ,
                    fighter_2_takedown_att,
                    fighter_2_takedown_succ,
                    fighter_2_submission_att,
                    fighter_2_reversals,
                    fighter_2_ctrl_time

                FROM ml.fight_dataset
                WHERE fight_url = :fight_url
            """),
            {"fight_url": fight_url}
        )

        row = result.fetchone()

    if row is None:
        return {"detail": "Fight not found"}

    return dict(row._mapping)

