import pandas as pd


def preprocess_ranks(df):
    df["fighter_1_is_ranked"] = df["fighter_1_rank"].between(0, 15).astype(int)
    df["fighter_2_is_ranked"] = df["fighter_2_rank"].between(0, 15).astype(int)

    df["fighter_1_rank"] = df["fighter_1_rank"].fillna(16)
    df["fighter_2_rank"] = df["fighter_2_rank"].fillna(16)

    return df

def preprocess_weight(df):
    weight_map = {
        "Flyweight": 125,
        "Bantamweight": 135,
        "Featherweight": 145,
        "Lightweight": 155,
        "Welterweight": 170,
        "Middleweight": 185,
        "Light Heavyweight": 205,
    }

    

    df["fighter_1_weight_lbs"] = df["fighter_1_weight_lbs"].fillna(
        df["weight_class"].map(weight_map)
    )

    df["fighter_2_weight_lbs"] = df["fighter_2_weight_lbs"].fillna(
        df["weight_class"].map(weight_map)
    )

    return df

def preprocess_fight_stats(df):
    
    return df



def build_fighter_history(df):
    

    # -------------------------
    # Fighter 1 history
    # -------------------------
    fighter_1_history = (
        df[
            [
                "fight_id",
                "event_date",
                "fighter_1",
                "fighter_2",
                "winner",
                "result",

                "fighter_1_height_cm",
                "fighter_1_weight_lbs",
                "fighter_1_reach_cm",
                "fighter_1_stance",
                "fighter_1_dob",

                "fighter_1_wins",
                "fighter_1_losses",
                "fighter_1_draws",
                "fighter_1_rank",
                "fighter_1_odds",
                "fighter_1_is_ranked",

                "fighter_1_slpm",
                "fighter_1_str_acc",
                "fighter_1_sapm",
                "fighter_1_str_def",
                "fighter_1_td_avg",
                "fighter_1_td_acc",
                "fighter_1_td_def",
                "fighter_1_sub_avg",

                "fighter_1_knockdowns",
                "fighter_1_sig_strikes_att",
                "fighter_1_sig_strikes_succ",
                "fighter_1_total_strikes_att",
                "fighter_1_total_strikes_succ",
                "fighter_1_takedown_att",
                "fighter_1_takedown_succ",
                "fighter_1_submission_att",
                "fighter_1_reversals",
                "fighter_1_ctrl_time",
            ]
        ]
        .rename(columns={
            "fighter_1": "fighter",
            "fighter_2": "opponent",

            "fighter_1_height_cm": "height_cm",
            "fighter_1_weight_lbs": "weight_lbs",
            "fighter_1_reach_cm": "reach_cm",
            "fighter_1_stance": "stance",
            "fighter_1_dob": "dob",

            "fighter_1_wins": "career_wins",
            "fighter_1_losses": "career_losses",
            "fighter_1_draws": "career_draws",
            "fighter_1_rank": "rank",
            "fighter_1_odds": "odds",
            "fighter_1_is_ranked": "is_ranked",

            "fighter_1_slpm": "slpm",
            "fighter_1_str_acc": "str_acc",
            "fighter_1_sapm": "sapm",
            "fighter_1_str_def": "str_def",
            "fighter_1_td_avg": "td_avg",
            "fighter_1_td_acc": "td_acc",
            "fighter_1_td_def": "td_def",
            "fighter_1_sub_avg": "sub_avg",

            "fighter_1_knockdowns": "knockdowns",
            "fighter_1_sig_strikes_att": "sig_str_att",
            "fighter_1_sig_strikes_succ": "sig_str_succ",
            "fighter_1_total_strikes_att": "total_str_att",
            "fighter_1_total_strikes_succ": "total_str_succ",
            "fighter_1_takedown_att": "td_att",
            "fighter_1_takedown_succ": "td_succ",
            "fighter_1_submission_att": "sub_att",
            "fighter_1_reversals": "reversals",
            "fighter_1_ctrl_time": "ctrl_time",
        })
    )

    # -------------------------
    # Fighter 2 history
    # -------------------------
    fighter_2_history = (
        df[
            [
                "fight_id",
                "event_date",
                "fighter_1",
                "fighter_2",
                "winner",
                "result",

                "fighter_2_height_cm",
                "fighter_2_weight_lbs",
                "fighter_2_reach_cm",
                "fighter_2_stance",
                "fighter_2_dob",

                "fighter_2_wins",
                "fighter_2_losses",
                "fighter_2_draws",
                "fighter_2_rank",
                "fighter_2_odds",
                "fighter_2_is_ranked",

                "fighter_2_slpm",
                "fighter_2_str_acc",
                "fighter_2_sapm",
                "fighter_2_str_def",
                "fighter_2_td_avg",
                "fighter_2_td_acc",
                "fighter_2_td_def",
                "fighter_2_sub_avg",

                "fighter_2_knockdowns",
                "fighter_2_sig_strikes_att",
                "fighter_2_sig_strikes_succ",
                "fighter_2_total_strikes_att",
                "fighter_2_total_strikes_succ",
                "fighter_2_takedown_att",
                "fighter_2_takedown_succ",
                "fighter_2_submission_att",
                "fighter_2_reversals",
                "fighter_2_ctrl_time",
            ]
        ]
        .rename(columns={
            "fighter_2": "fighter",
            "fighter_1": "opponent",

            "fighter_2_height_cm": "height_cm",
            "fighter_2_weight_lbs": "weight_lbs",
            "fighter_2_reach_cm": "reach_cm",
            "fighter_2_stance": "stance",
            "fighter_2_dob": "dob",

            "fighter_2_wins": "career_wins",
            "fighter_2_losses": "career_losses",
            "fighter_2_draws": "career_draws",
            "fighter_2_rank": "rank",
            "fighter_2_odds": "odds",
            "fighter_2_is_ranked": "is_ranked",

            "fighter_2_slpm": "slpm",
            "fighter_2_str_acc": "str_acc",
            "fighter_2_sapm": "sapm",
            "fighter_2_str_def": "str_def",
            "fighter_2_td_avg": "td_avg",
            "fighter_2_td_acc": "td_acc",
            "fighter_2_td_def": "td_def",
            "fighter_2_sub_avg": "sub_avg",

            "fighter_2_knockdowns": "knockdowns",
            "fighter_2_sig_strikes_att": "sig_str_att",
            "fighter_2_sig_strikes_succ": "sig_str_succ",
            "fighter_2_total_strikes_att": "total_str_att",
            "fighter_2_total_strikes_succ": "total_str_succ",
            "fighter_2_takedown_att": "td_att",
            "fighter_2_takedown_succ": "td_succ",
            "fighter_2_submission_att": "sub_att",
            "fighter_2_reversals": "reversals",
            "fighter_2_ctrl_time": "ctrl_time",
        })
    )

    # -------------------------
    # Combine
    # -------------------------
    history = pd.concat(
        [fighter_1_history, fighter_2_history],
        ignore_index=True
    )

    # -------------------------
    # ctrl_time conversion
    # -------------------------
    def time_to_seconds(x):
        if pd.isna(x):
            return 0
        parts = x.split(":")

        if len(parts) == 2:
            m, s = parts
            return int(m) * 60 + int(s)
        elif len(parts) == 3:
            h, m, s = parts
            return int(h) * 3600 + int(m) * 60 + int(s)
        else:
            return 0

    history["ctrl_time"] = history["ctrl_time"].apply(time_to_seconds)

    # -------------------------
    # sort
    # -------------------------
    history = history.sort_values(["fighter", "event_date", "fight_id"])

    return history


def add_fighter_cumulative_features(df, history):
    # -------------------------
    # Win / Loss / Draw flags
    # -------------------------
    history = history.copy()

    history["win"] = (history["fighter"] == history["winner"]).astype(int)
    history["loss"] = 1 - history["win"]

    history["draw"] = (
        (history["winner"] == "Draw").astype(int)
        if "Draw" in history["winner"].values
        else 0
    )

    # -------------------------
    # Prior cumulative stats
    # -------------------------
    history["prior_wins"] = (
        history.groupby("fighter")["win"]
        .transform(lambda s: s.cumsum().shift(fill_value=0))
    )

    history["prior_losses"] = (
        history.groupby("fighter")["loss"]
        .transform(lambda s: s.cumsum().shift(fill_value=0))
    )

    history["prior_draws"] = (
        history.groupby("fighter")["draw"]
        .transform(lambda s: s.cumsum().shift(fill_value=0))
    )

    # -------------------------
    # Fighter 1 features
    # -------------------------
    fighter_1_features = (
        history[["fight_id", "fighter", "prior_wins", "prior_losses", "prior_draws"]]
        .rename(columns={
            "fighter": "fighter_1",
            "prior_wins": "fighter_1_prior_wins",
            "prior_losses": "fighter_1_prior_losses",
            "prior_draws": "fighter_1_prior_draws",
        })
    )

    # -------------------------
    # Fighter 2 features
    # -------------------------
    fighter_2_features = (
        history[["fight_id", "fighter", "prior_wins", "prior_losses", "prior_draws"]]
        .rename(columns={
            "fighter": "fighter_2",
            "prior_wins": "fighter_2_prior_wins",
            "prior_losses": "fighter_2_prior_losses",
            "prior_draws": "fighter_2_prior_draws",
        })
    )

    # -------------------------
    # Merge into df
    # -------------------------
    df = df.merge(fighter_1_features, on=["fight_id", "fighter_1"], how="left")
    df = df.merge(fighter_2_features, on=["fight_id", "fighter_2"], how="left")

    return df

def add_striking_rolling_features(df, history, window=3):
    history = history.sort_values(["fighter", "event_date"]).copy()

    history["slpm_roll_3"] = (
        history.groupby("fighter")["slpm"]
        .transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
    )

    history["sapm_roll_3"] = (
        history.groupby("fighter")["sapm"]
        .transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
    )

    history["str_acc_roll_3"] = (
        history.groupby("fighter")["str_acc"]
        .transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
    )

    history["str_def_roll_3"] = (
        history.groupby("fighter")["str_def"]
        .transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
    )

    fighter_1 = history[
        ["fight_id", "fighter", "slpm_roll_3", "sapm_roll_3", "str_acc_roll_3", "str_def_roll_3"]
    ].rename(columns={
        "fighter": "fighter_1",
        "slpm_roll_3": "fighter_1_slpm_roll_3",
        "sapm_roll_3": "fighter_1_sapm_roll_3",
        "str_acc_roll_3": "fighter_1_str_acc_roll_3",
        "str_def_roll_3": "fighter_1_str_def_roll_3",
    })

    fighter_2 = history[
        ["fight_id", "fighter", "slpm_roll_3", "sapm_roll_3", "str_acc_roll_3", "str_def_roll_3"]
    ].rename(columns={
        "fighter": "fighter_2",
        "slpm_roll_3": "fighter_2_slpm_roll_3",
        "sapm_roll_3": "fighter_2_sapm_roll_3",
        "str_acc_roll_3": "fighter_2_str_acc_roll_3",
        "str_def_roll_3": "fighter_2_str_def_roll_3",
    })

    df = df.merge(fighter_1, on=["fight_id", "fighter_1"], how="left")
    df = df.merge(fighter_2, on=["fight_id", "fighter_2"], how="left")

    return df

def add_grappling_rolling_features(df, history, window=3):
    history = history.sort_values(["fighter", "event_date"]).copy()

    history["td_avg_roll_3"] = (
        history.groupby("fighter")["td_avg"]
        .transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
    )

    history["td_acc_roll_3"] = (
        history.groupby("fighter")["td_acc"]
        .transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
    )

    history["td_def_roll_3"] = (
        history.groupby("fighter")["td_def"]
        .transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
    )

    history["sub_avg_roll_3"] = (
        history.groupby("fighter")["sub_avg"]
        .transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
    )

    history["ctrl_time_roll_3"] = (
        history.groupby("fighter")["ctrl_time"]
        .transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
    )

    history["td_success_rate_roll_3"] = (
        history.groupby("fighter")["td_succ"]
        .transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
        / (
            history.groupby("fighter")["td_att"]
            .transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
            + 1e-6
        )
    )

    fighter_1 = history[
        [
            "fight_id",
            "fighter",
            "td_avg_roll_3",
            "td_acc_roll_3",
            "td_def_roll_3",
            "sub_avg_roll_3",
            "ctrl_time_roll_3",
            "td_success_rate_roll_3",
        ]
    ].rename(columns={
        "fighter": "fighter_1",
        "td_avg_roll_3": "fighter_1_td_avg_roll_3",
        "td_acc_roll_3": "fighter_1_td_acc_roll_3",
        "td_def_roll_3": "fighter_1_td_def_roll_3",
        "sub_avg_roll_3": "fighter_1_sub_avg_roll_3",
        "ctrl_time_roll_3": "fighter_1_ctrl_time_roll_3",
        "td_success_rate_roll_3": "fighter_1_td_success_rate_roll_3",
    })

    fighter_2 = history[
        [
            "fight_id",
            "fighter",
            "td_avg_roll_3",
            "td_acc_roll_3",
            "td_def_roll_3",
            "sub_avg_roll_3",
            "ctrl_time_roll_3",
            "td_success_rate_roll_3",
        ]
    ].rename(columns={
        "fighter": "fighter_2",
        "td_avg_roll_3": "fighter_2_td_avg_roll_3",
        "td_acc_roll_3": "fighter_2_td_acc_roll_3",
        "td_def_roll_3": "fighter_2_td_def_roll_3",
        "sub_avg_roll_3": "fighter_2_sub_avg_roll_3",
        "ctrl_time_roll_3": "fighter_2_ctrl_time_roll_3",
        "td_success_rate_roll_3": "fighter_2_td_success_rate_roll_3",
    })

    df = df.merge(fighter_1, on=["fight_id", "fighter_1"], how="left")
    df = df.merge(fighter_2, on=["fight_id", "fighter_2"], how="left")

    return df

    
