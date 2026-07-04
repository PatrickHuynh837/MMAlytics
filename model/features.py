import pandas as pd


def create_physical_features(df):
    """Create physical differential features."""

    df = df.copy()

    df["height_diff"] = (
        df["fighter_1_height_cm"] - df["fighter_2_height_cm"]
    )

    df["reach_diff"] = (
        df["fighter_1_reach_cm"] - df["fighter_2_reach_cm"]
    )

    df["weight_diff"] = (
        df["fighter_1_weight_lbs"] - df["fighter_2_weight_lbs"]
    )

    df["age_diff"] = (
        (
            pd.to_datetime(df["event_date"])
            - pd.to_datetime(df["fighter_1_dob"])
        ).dt.days
        - (
            pd.to_datetime(df["event_date"])
            - pd.to_datetime(df["fighter_2_dob"])
        ).dt.days
    ) / 365.25

    return df


def create_record_features(df):
    """Create prior record differential features."""

    df = df.copy()

    df["win_diff"] = (
        df["fighter_1_prior_wins"]
        - df["fighter_2_prior_wins"]
    )

    df["loss_diff"] = (
        df["fighter_1_prior_losses"]
        - df["fighter_2_prior_losses"]
    )

    df["draw_diff"] = (
        df["fighter_1_prior_draws"]
        - df["fighter_2_prior_draws"]
    )

    return df


def create_striking_features(df):
    """Create striking differential features."""

    df = df.copy()

    stats = [
        "slpm",
        "sapm",
        "str_acc",
        "str_def",
    ]

    for stat in stats:
        df[f"{stat}_roll_3_diff"] = (
            df[f"fighter_1_{stat}_roll_3"]
            - df[f"fighter_2_{stat}_roll_3"]
        )

    return df


def create_grappling_features(df):
    """Create grappling differential features."""

    df = df.copy()

    stats = [
        "td_avg",
        "td_acc",
        "td_def",
        "sub_avg",
        "ctrl_time",
        "td_success_rate",
    ]

    for stat in stats:
        df[f"{stat}_roll_3_diff"] = (
            df[f"fighter_1_{stat}_roll_3"]
            - df[f"fighter_2_{stat}_roll_3"]
        )

    return df


def create_perception_features(df):
    """Create perception-based features."""

    df = df.copy()

    df["rank_diff"] = (
        df["fighter_2_rank"] - df["fighter_1_rank"]
    )

    df["odds_diff"] = (
        df["fighter_1_odds"] - df["fighter_2_odds"]
    )

    return df


def create_features(df):
    """Run all feature engineering."""

    df = create_physical_features(df)
    df = create_record_features(df)
    df = create_striking_features(df)
    df = create_grappling_features(df)
    df = create_perception_features(df)

    return df

LINEAR_FEATURES = [
    "height_diff",
    "reach_diff",
    "weight_diff",
    "age_diff",
    "win_diff",
    "loss_diff",
    "draw_diff",
    "slpm_roll_3_diff",
    "sapm_roll_3_diff",
    "str_acc_roll_3_diff",
    "str_def_roll_3_diff",
    "td_avg_roll_3_diff",
    "td_acc_roll_3_diff",
    "td_def_roll_3_diff",
    "sub_avg_roll_3_diff",
    "ctrl_time_roll_3_diff",
    "td_success_rate_roll_3_diff",
    "rank_diff",
    "odds_diff"
]