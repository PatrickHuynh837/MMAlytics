from preprocessing import *
from features import create_features, LINEAR_FEATURES, TREE_FEATURES

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


# =========================
# DB CONNECTION
# =========================

DB_URL = (
    "postgresql+psycopg://neondb_owner:npg_Bo2SUY6ngypR@"
    "ep-orange-frost-afcl94sd-pooler.c-2.us-west-2.aws.neon.tech/"
    "neondb?sslmode=require"
)

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)


# =========================
# LOAD DATA
# =========================

df = pd.read_sql(
    """
    SELECT *
    FROM ml.fight_dataset
    """,
    engine
)


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
# EVALUATION
# =========================

def evaluate_model(name, y_true, y_pred, y_prob):

    print(
        f"\n================ {name.upper()} ================\n"
    )

    print(
        f"Accuracy: {accuracy_score(y_true, y_pred):.4f}"
    )

    print(
        f"ROC AUC: {roc_auc_score(y_true, y_prob):.4f}"
    )

    print(
        f"F1 Score: {f1_score(y_true, y_pred):.4f}"
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
        df,
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
            "f1": f1_score(
                y_test,
                preds
            )
        }
    )



# =========================
# MODEL COMPARISON
# =========================

results = pd.DataFrame(results)


print(
    "\n================ MODEL COMPARISON ================\n"
)


print(
    results.sort_values(
        by="roc_auc",
        ascending=False
    )
)