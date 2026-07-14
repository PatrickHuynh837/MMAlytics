from preprocessing import *
from features import create_features, LINEAR_FEATURES, TREE_FEATURES
from models import run_logistic_regression, run_xgboost

import numpy as np
import pandas as pd
from sqlalchemy import create_engine

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
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

df["fighter_1_win"] = (df["winner"] == df["fighter_1"]).astype(int)

# =========================
# PREPROCESSING
# =========================

df = preprocess_ranks(df)
df = preprocess_weight(df)

df = df.reset_index(drop=True)
df["fight_id"] = df.index

history = build_fighter_history(df)

df = add_fighter_cumulative_features(df, history)
df = add_striking_rolling_features(df, history)
df = add_grappling_rolling_features(df, history)

# =========================
# FEATURE ENGINEERING
# =========================

df = create_features(df)

# =========================
# EVALUATION FUNCTION
# =========================

def evaluate_model(name, y_true, y_pred, y_prob):
    print(f"\n================ {name.upper()} ================\n")
    print(f"Accuracy: {accuracy_score(y_true, y_pred):.4f}")
    print(f"ROC AUC: {roc_auc_score(y_true, y_prob):.4f}")
    print(f"F1 Score: {f1_score(y_true, y_pred):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_true, y_pred))


# =========================
# LOGISTIC REGRESSION
# =========================

lr_model, lr_acc, lr_preds, lr_probs, y_test_lr = run_logistic_regression(
    df,
    LINEAR_FEATURES,
    "fighter_1_win"
)

evaluate_model("Logistic Regression", y_test_lr, lr_preds, lr_probs)


# =========================
# XGBOOST
# =========================

xgb_model, xgb_acc, xgb_preds, xgb_probs, y_test_xgb = run_xgboost(
    df,
    TREE_FEATURES,
    "fighter_1_win"
)

evaluate_model("XGBoost", y_test_xgb, xgb_preds, xgb_probs)


# =========================
# QUICK COMPARISON TABLE
# =========================

results = pd.DataFrame([
    {
        "model": "logistic_regression",
        "accuracy": accuracy_score(y_test_lr, lr_preds),
        "roc_auc": roc_auc_score(y_test_lr, lr_probs),
        "f1": f1_score(y_test_lr, lr_preds),
    },
    {
        "model": "xgboost",
        "accuracy": accuracy_score(y_test_xgb, xgb_preds),
        "roc_auc": roc_auc_score(y_test_xgb, xgb_probs),
        "f1": f1_score(y_test_xgb, xgb_preds),
    }
])

print("\n================ MODEL COMPARISON ================\n")
print(results)