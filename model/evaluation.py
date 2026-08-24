from preprocessing import *
from features import (
    create_features,
    LINEAR_FEATURES,
    TREE_FEATURES
)

from models import (
    run_logistic_regression,
    run_xgboost,
    run_random_forest,
    run_catboost
)

import pandas as pd
from sqlalchemy import create_engine

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    roc_auc_score,
)

import os
from dotenv import load_dotenv
from pathlib import Path


# =========================
# EVALUATION PERIOD
# =========================

EVAL_START = pd.Timestamp("2023-01-01")
EVAL_END = pd.Timestamp("2026-08-22")

# Use an exclusive upper bound so the entire
# 2026-08-15 date is included.
EVAL_END_EXCLUSIVE = (
    EVAL_END + pd.Timedelta(days=1)
)


# =========================
# DB CONNECTION
# =========================

load_dotenv(
    Path(__file__).resolve().parents[1] / ".env"
)

DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError(
        "DB_URL is missing from environment variables"
    )


engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)


# =========================
# LOAD FULL HISTORICAL DATA
# =========================

df = pd.read_sql(
    """
    SELECT *
    FROM ml.fight_dataset
    ORDER BY event_date ASC
    """,
    engine
)


# =========================
# DATE PROCESSING
# =========================

df["event_date"] = pd.to_datetime(
    df["event_date"]
)


# Keep all historical fights up to the
# end of the evaluation period.
#
# This preserves pre-2023 history while
# preventing future fights from entering
# the evaluation dataset.

df = df[
    df["event_date"] < EVAL_END_EXCLUSIVE
].copy()


# =========================
# TARGET
# =========================

df["fighter_1_win"] = (
    df["winner"] == df["fighter_1"]
).astype(int)


# =========================
# PREPROCESSING
# =========================

df = preprocess_ranks(df)

df = preprocess_weight(df)

df = df.reset_index(drop=True)

df["fight_id"] = df.index


# =========================
# BUILD FIGHTER HISTORY
# =========================
#
# IMPORTANT:
# History is built using the FULL
# historical dataset.
#
# This allows a 2023 fight to use
# fighter history from 2018-2022,
# for example.
# =========================

history = build_fighter_history(df)


df = add_fighter_cumulative_features(
    df,
    history
)


df = add_striking_rolling_features(
    df,
    history
)


df = add_grappling_rolling_features(
    df,
    history
)


# =========================
# FEATURE ENGINEERING
# =========================

df = create_features(df)


# =========================
# TRAIN / TEST SPLIT
# =========================
#
# TRAIN:
# Everything before 2023-08-15
#
# TEST:
# 2023-08-15 through 2026-08-15
#
# Chronological split.
# No random sampling.
# =========================

train_df = df[
    df["event_date"] < EVAL_START
].copy()


test_df = df[
    (df["event_date"] >= EVAL_START) &
    (df["event_date"] < EVAL_END_EXCLUSIVE)
].copy()


# =========================
# SPLIT INFORMATION
# =========================

print(
    "\n================ DATA SPLIT ================\n"
)

print(
    f"Training period: "
    f"{train_df['event_date'].min().date()} "
    f"-> "
    f"{train_df['event_date'].max().date()}"
)

print(
    f"Evaluation period: "
    f"{test_df['event_date'].min().date()} "
    f"-> "
    f"{test_df['event_date'].max().date()}"
)

print(
    f"Training fights: {len(train_df)}"
)

print(
    f"Evaluation fights: {len(test_df)}"
)


# =========================
# EVALUATION FUNCTION
# =========================

def evaluate_model(
    name,
    y_true,
    y_pred,
    y_prob
):

    print(
        f"\n================ "
        f"{name.upper()} "
        f"================\n"
    )

    print(
        f"Accuracy: "
        f"{accuracy_score(y_true, y_pred):.4f}"
    )

    print(
        f"ROC AUC: "
        f"{roc_auc_score(y_true, y_prob):.4f}"
    )

    print(
        f"F1 Score (Macro): "
        f"{f1_score(y_true, y_pred, average='macro'):.4f}"
    )

    print("\nClassification Report:")

    print(
        classification_report(
            y_true,
            y_pred
        )
    )

    print("Confusion Matrix:")

    print(
        confusion_matrix(
            y_true,
            y_pred
        )
    )


# =========================
# MODELS
# =========================

models = [

    {
        "name": "Logistic Regression",
        "function": run_logistic_regression,
        "features": LINEAR_FEATURES
    },

    {
        "name": "XGBoost",
        "function": run_xgboost,
        "features": TREE_FEATURES
    },

    {
        "name": "CatBoost",
        "function": run_catboost,
        "features": TREE_FEATURES
    },

    {
        "name": "Random Forest",
        "function": run_random_forest,
        "features": TREE_FEATURES
    }

]


# =========================
# RUN MODELS
# =========================

results = []


for model_info in models:

    name = model_info["name"]

    model_function = model_info["function"]

    features = model_info["features"]


    model, acc, preds, probs, y_test = model_function(
        train_df,
        test_df,
        features,
        "fighter_1_win"
    )


    evaluate_model(
        name,
        y_test,
        preds,
        probs
    )


    results.append(
        {
            "model": name,

            "accuracy": accuracy_score(
                y_test,
                preds
            ),

            "roc_auc": roc_auc_score(
                y_test,
                probs
            ),

            "f1(macro)": f1_score(
                y_test,
                preds,
                average="macro"
            )
        }
    )


# =========================
# MODEL COMPARISON
# =========================

results = pd.DataFrame(results)


print(
    "\n================ "
    "MODEL COMPARISON "
    "================\n"
)


print(
    results.sort_values(
        by="roc_auc",
        ascending=False
    )
)