
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
                    referee,

                    winner,
                    result,
                    result_details,
                    finish_round,
                    finish_time,

                    fighter_1_height_cm,
                    fighter_1_weight_lbs,
                    fighter_1_reach_cm,
                    fighter_1_stance,
                    fighter_1_dob,
                    fighter_1_wins,
                    fighter_1_losses,
                    fighter_1_draws,

                    fighter_1_slpm,
                    fighter_1_str_acc,
                    fighter_1_sapm,
                    fighter_1_str_def,
                    fighter_1_td_avg,
                    fighter_1_td_acc,
                    fighter_1_td_def,
                    fighter_1_sub_avg,

                    fighter_2_height_cm,
                    fighter_2_weight_lbs,
                    fighter_2_reach_cm,
                    fighter_2_stance,
                    fighter_2_dob,
                    fighter_2_wins,
                    fighter_2_losses,
                    fighter_2_draws,

                    fighter_2_slpm,
                    fighter_2_str_acc,
                    fighter_2_sapm,
                    fighter_2_str_def,
                    fighter_2_td_avg,
                    fighter_2_td_acc,
                    fighter_2_td_def,
                    fighter_2_sub_avg,

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

                    fighter_2_knockdowns,
                    fighter_2_total_strikes_att,
                    fighter_2_total_strikes_succ,
                    fighter_2_sig_strikes_att,
                    fighter_2_sig_strikes_succ,
                    fighter_2_takedown_att,
                    fighter_2_takedown_succ,
                    fighter_2_submission_att,
                    fighter_2_reversals,
                    fighter_2_ctrl_time,

                    fighter_1_rank,
                    fighter_2_rank,
                    fighter_1_odds,
                    fighter_2_odds

                FROM ml.fight_dataset
                WHERE fight_url = :fight_url
            """),
            {"fight_url": fight_url}
        )

        row = result.fetchone()

    if row is None:
        return {"detail": "Fight not found"}

    return dict(row._mapping)

