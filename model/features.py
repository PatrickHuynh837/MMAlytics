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


def create_ratio_features(df):
    """Create ratio-based features for tree models (XGBoost)."""

    df = df.copy()

    eps = 1e-6

    # ==========================
    # Experience Ratios
    # ==========================

    df["win_ratio"] = (
        (df["fighter_1_wins"] + 1) /
        (df["fighter_2_wins"] + 1)
    )

    df["loss_ratio"] = (
        (df["fighter_1_losses"] + 1) /
        (df["fighter_2_losses"] + 1)
    )

    df["draw_ratio"] = (
        (df["fighter_1_draws"] + 1) /
        (df["fighter_2_draws"] + 1)
    )

    fighter_1_total_fights = (
        df["fighter_1_wins"] +
        df["fighter_1_losses"] +
        df["fighter_1_draws"]
    )

    fighter_2_total_fights = (
        df["fighter_2_wins"] +
        df["fighter_2_losses"] +
        df["fighter_2_draws"]
    )

    df["experience_ratio"] = (
        (fighter_1_total_fights + 1) /
        (fighter_2_total_fights + 1)
    )


    # Win percentage advantage

    fighter_1_win_pct = (
        df["fighter_1_wins"] /
        (fighter_1_total_fights + 1)
    )

    fighter_2_win_pct = (
        df["fighter_2_wins"] /
        (fighter_2_total_fights + 1)
    )

    df["win_pct_ratio"] = (
        (fighter_1_win_pct + eps) /
        (fighter_2_win_pct + eps)
    )


    # ==========================
    # Physical Ratios
    # ==========================

    df["height_ratio"] = (
        df["fighter_1_height_cm"] /
        (df["fighter_2_height_cm"] + eps)
    )

    df["reach_ratio"] = (
        df["fighter_1_reach_cm"] /
        (df["fighter_2_reach_cm"] + eps)
    )

    df["weight_ratio"] = (
        df["fighter_1_weight_lbs"] /
        (df["fighter_2_weight_lbs"] + eps)
    )


    # ==========================
    # Striking Ratios
    # ==========================

    df["slpm_ratio"] = (
        df["fighter_1_slpm"] /
        (df["fighter_2_slpm"] + eps)
    )

    df["sapm_ratio"] = (
        df["fighter_1_sapm"] /
        (df["fighter_2_sapm"] + eps)
    )

    df["str_acc_ratio"] = (
        df["fighter_1_str_acc"] /
        (df["fighter_2_str_acc"] + eps)
    )

    df["str_def_ratio"] = (
        df["fighter_1_str_def"] /
        (df["fighter_2_str_def"] + eps)
    )


    # Combined striking dominance

    df["strike_efficiency_ratio"] = (
        (
            df["fighter_1_slpm"] *
            df["fighter_1_str_acc"]
        )
        /
        (
            df["fighter_2_slpm"] *
            df["fighter_2_str_acc"]
            + eps
        )
    )

    df["damage_resistance_ratio"] = (
        df["fighter_2_sapm"] /
        (df["fighter_1_sapm"] + eps)
    )


    # ==========================
    # Grappling Ratios
    # ==========================

    df["td_avg_ratio"] = (
        df["fighter_1_td_avg"] /
        (df["fighter_2_td_avg"] + eps)
    )

    df["td_acc_ratio"] = (
        df["fighter_1_td_acc"] /
        (df["fighter_2_td_acc"] + eps)
    )

    df["td_def_ratio"] = (
        df["fighter_1_td_def"] /
        (df["fighter_2_td_def"] + eps)
    )

    df["sub_avg_ratio"] = (
        df["fighter_1_sub_avg"] /
        (df["fighter_2_sub_avg"] + eps)
    )


    df["grappling_control_ratio"] = (
        (
            df["fighter_1_td_avg"] +
            df["fighter_1_sub_avg"]
        )
        /
        (
            df["fighter_2_td_avg"] +
            df["fighter_2_sub_avg"] +
            eps
        )
    )


    # ==========================
    # Recent Form Ratios
    # ==========================

    df["recent_slpm_ratio"] = (
        df["fighter_1_slpm_roll_3"] /
        (df["fighter_2_slpm_roll_3"] + eps)
    )

    df["recent_sapm_ratio"] = (
        df["fighter_1_sapm_roll_3"] /
        (df["fighter_2_sapm_roll_3"] + eps)
    )

    df["recent_str_acc_ratio"] = (
        df["fighter_1_str_acc_roll_3"] /
        (df["fighter_2_str_acc_roll_3"] + eps)
    )

    df["recent_str_def_ratio"] = (
        df["fighter_1_str_def_roll_3"] /
        (df["fighter_2_str_def_roll_3"] + eps)
    )

    df["recent_td_success_ratio"] = (
        df["fighter_1_td_success_rate_roll_3"] /
        (df["fighter_2_td_success_rate_roll_3"] + eps)
    )


    df["recent_performance_ratio"] = (
        (
            df["fighter_1_slpm_roll_3"] *
            df["fighter_1_str_acc_roll_3"]
        )
        /
        (
            df["fighter_2_slpm_roll_3"] *
            df["fighter_2_str_acc_roll_3"]
            + eps
        )
    )


    # ==========================
    # Ranking + Market Ratios
    # ==========================

    df["rank_ratio"] = (
        (df["fighter_2_rank"] + 1) /
        (df["fighter_1_rank"] + 1)
    )

    df["odds_ratio"] = (
        (df["fighter_1_odds"] + 1) /
        (df["fighter_2_odds"] + 1)
    )


    return df

def create_interaction_features(df):
    """Create MMA-specific interaction features for tree models."""
    
    df = df.copy()
    eps = 1e-6

    # ==========================
    # Striking Interactions
    # ==========================

    # Offensive output adjusted by accuracy
    df["fighter_1_strike_quality"] = (
        df["fighter_1_slpm"] *
        df["fighter_1_str_acc"]
    )

    df["fighter_2_strike_quality"] = (
        df["fighter_2_slpm"] *
        df["fighter_2_str_acc"]
    )

    df["strike_quality_diff"] = (
        df["fighter_1_strike_quality"] -
        df["fighter_2_strike_quality"]
    )


    # Damage output vs damage absorbed
    df["fighter_1_damage_balance"] = (
        df["fighter_1_slpm"] -
        df["fighter_1_sapm"]
    )

    df["fighter_2_damage_balance"] = (
        df["fighter_2_slpm"] -
        df["fighter_2_sapm"]
    )

    df["damage_balance_diff"] = (
        df["fighter_1_damage_balance"] -
        df["fighter_2_damage_balance"]
    )


    # ==========================
    # Grappling Interactions
    # ==========================

    # Takedown ability + takedown defense
    df["fighter_1_grappling_control"] = (
        df["fighter_1_td_avg"] *
        df["fighter_1_td_acc"] *
        df["fighter_1_td_def"]
    )

    df["fighter_2_grappling_control"] = (
        df["fighter_2_td_avg"] *
        df["fighter_2_td_acc"] *
        df["fighter_2_td_def"]
    )

    df["grappling_control_diff"] = (
        df["fighter_1_grappling_control"] -
        df["fighter_2_grappling_control"]
    )


    # Submission threat
    df["submission_advantage"] = (
        df["fighter_1_sub_avg"] -
        df["fighter_2_sub_avg"]
    )


    # ==========================
    # Physical Interactions
    # ==========================

    # Reach matters more for high volume strikers
    df["reach_striking_advantage"] = (
        df["fighter_1_reach_cm"] *
        df["fighter_1_slpm"]
    ) - (
        df["fighter_2_reach_cm"] *
        df["fighter_2_slpm"]
    )


    # Size + weight interaction
    df["size_advantage"] = (
        df["fighter_1_height_cm"] *
        df["fighter_1_weight_lbs"]
    ) - (
        df["fighter_2_height_cm"] *
        df["fighter_2_weight_lbs"]
    )


    # ==========================
    # Experience Interactions
    # ==========================

    fighter_1_total_fights = (
        df["fighter_1_wins"] +
        df["fighter_1_losses"] +
        df["fighter_1_draws"]
    )

    fighter_2_total_fights = (
        df["fighter_2_wins"] +
        df["fighter_2_losses"] +
        df["fighter_2_draws"]
    )


    df["experience_win_quality"] = (
        fighter_1_total_fights *
        (df["fighter_1_wins"] / (fighter_1_total_fights + eps))
    ) - (
        fighter_2_total_fights *
        (df["fighter_2_wins"] / (fighter_2_total_fights + eps))
    )


    # ==========================
    # Recent Form Interactions
    # ==========================

    df["recent_striking_momentum"] = (
        (
            df["fighter_1_slpm_roll_3"] -
            df["fighter_1_sapm_roll_3"]
        )
        -
        (
            df["fighter_2_slpm_roll_3"] -
            df["fighter_2_sapm_roll_3"]
        )
    )


    df["recent_accuracy_advantage"] = (
        df["fighter_1_str_acc_roll_3"] -
        df["fighter_2_str_acc_roll_3"]
    )


    # ==========================
    # Market + Performance
    # ==========================

    df["market_stat_mismatch"] = (
        df["win_pct_ratio"] /
        (df["odds_ratio"] + eps)
    )


    return df


def create_features(df):
    """Run all feature engineering."""

    df = create_physical_features(df)
    df = create_record_features(df)
    df = create_striking_features(df)
    df = create_grappling_features(df)
    df = create_perception_features(df)
    df = create_ratio_features(df)
    df = create_interaction_features(df)

    return df

# ==========================================
# Linear Model Features
# Logistic Regression
#
# Goal:
# - Linear model cannot discover interactions
# - Give it engineered MMA concepts
# ==========================================

LINEAR_FEATURES = [

    # --------------------------
    # Physical Differences
    # --------------------------

    "height_diff",
    "reach_diff",
    "weight_diff",
    "age_diff",


    # --------------------------
    # Experience Differences
    # --------------------------

    "win_diff",
    "loss_diff",
    "draw_diff",


    # --------------------------
    # Striking Differences
    # --------------------------

    "slpm_roll_3_diff",
    "sapm_roll_3_diff",
    "str_acc_roll_3_diff",
    "str_def_roll_3_diff",


    # --------------------------
    # Grappling Differences
    # --------------------------

    "td_avg_roll_3_diff",
    "td_acc_roll_3_diff",
    "td_def_roll_3_diff",
    "sub_avg_roll_3_diff",
    "ctrl_time_roll_3_diff",
    "td_success_rate_roll_3_diff",


    # --------------------------
    # Market Differences
    # --------------------------

    "rank_diff",
    "odds_diff",


    # --------------------------
    # Ratios
    # --------------------------

    "height_ratio",
    "reach_ratio",
    "weight_ratio",

    "win_ratio",
    "win_pct_ratio",
    "experience_ratio",

    "slpm_ratio",
    "sapm_ratio",
    "str_acc_ratio",
    "str_def_ratio",

    "td_avg_ratio",
    "td_acc_ratio",
    "td_def_ratio",
    "sub_avg_ratio",

    "recent_slpm_ratio",
    "recent_sapm_ratio",
    "recent_str_acc_ratio",
    "recent_str_def_ratio",
    "recent_td_success_ratio",

    "rank_ratio",
    "odds_ratio",


    # --------------------------
    # Handcrafted Interactions
    # --------------------------

    "strike_quality_diff",
    "damage_balance_diff",

    "grappling_control_diff",
    "submission_advantage",

    "reach_striking_advantage",
    "size_advantage",

    "experience_win_quality",

    "recent_striking_momentum",
    "recent_accuracy_advantage",

    "market_stat_mismatch",
]


TREE_FEATURES = [

    # --------------------------
    # Market / Perception
    # --------------------------

    "odds_ratio",
    "rank_ratio",

    "odds_diff",
    "rank_diff",


    # --------------------------
    # Experience
    # --------------------------

    "win_ratio",
    "win_pct_ratio",
    "experience_ratio",

    "win_diff",
    "loss_diff",
    "draw_diff",


    # --------------------------
    # Physical Matchup
    # --------------------------

    "height_ratio",
    "reach_ratio",
    "weight_ratio",

    "height_diff",
    "reach_diff",
    "weight_diff",
    "age_diff",


    # --------------------------
    # Striking
    # --------------------------

    "slpm_ratio",
    "sapm_ratio",
    "str_acc_ratio",
    "str_def_ratio",

    "strike_efficiency_ratio",
    "damage_resistance_ratio",

    # raw matchup differentials
    "slpm_roll_3_diff",
    "sapm_roll_3_diff",
    "str_acc_roll_3_diff",
    "str_def_roll_3_diff",


    # handcrafted striking interactions
    "strike_quality_diff",
    "damage_balance_diff",
    "reach_striking_advantage",


    # --------------------------
    # Grappling
    # --------------------------

    "td_avg_ratio",
    "td_acc_ratio",
    "td_def_ratio",
    "sub_avg_ratio",

    "grappling_control_ratio",

    # raw matchup differentials
    "td_avg_roll_3_diff",
    "td_acc_roll_3_diff",
    "td_def_roll_3_diff",
    "sub_avg_roll_3_diff",
    "ctrl_time_roll_3_diff",
    "td_success_rate_roll_3_diff",


    # handcrafted grappling interactions
    "grappling_control_diff",
    "submission_advantage",


    # --------------------------
    # Recent Form
    # --------------------------

    "recent_slpm_ratio",
    "recent_sapm_ratio",
    "recent_str_acc_ratio",
    "recent_str_def_ratio",

    "recent_td_success_ratio",
    "recent_performance_ratio",

    "recent_striking_momentum",
    "recent_accuracy_advantage",


    # --------------------------
    # Experience Interactions
    # --------------------------

    "experience_win_quality",


    # --------------------------
    # Physical Interactions
    # --------------------------

    "size_advantage",


    # --------------------------
    # Market + Performance
    # --------------------------

    "market_stat_mismatch",
]