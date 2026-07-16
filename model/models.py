from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier



def run_model(df, features, target, model, use_scaler=True):

    split_idx = int(len(df) * 0.8)

    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]

    X_train = train_df[features]
    y_train = train_df[target]

    X_test = test_df[features]
    y_test = test_df[target]

    steps = [
        ("imputer", SimpleImputer(strategy="median"))
    ]

    if use_scaler:
        steps.append(("scaler", StandardScaler()))

    steps.append(("model", model))

    pipeline = Pipeline(steps)

    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    probs = pipeline.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, preds)

    return pipeline, acc, preds, probs, y_test


def run_logistic_regression(df, features, target):

    return run_model(
        df,
        features,
        target,
        LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=42
        ),
        use_scaler=True
    )


def run_xgboost(df, features, target, scale_pos_weight=None):

    return run_model(
        df,
        features,
        target,
        XGBClassifier(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=4,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1.0,
            min_child_weight=5,
            gamma=0.1,
            random_state=42,
            eval_metric="logloss",
            scale_pos_weight=scale_pos_weight
        ),
        use_scaler=False
    )


def run_random_forest(df, features, target):

    return run_model(
        df,
        features,
        target,
        RandomForestClassifier(
            n_estimators=500,
            max_depth=6,
            min_samples_split=10,
            min_samples_leaf=5,
            max_features="sqrt",
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        ),
        use_scaler=False
    )


def run_catboost(df, features, target):

    return run_model(
        df,
        features,
        target,
        CatBoostClassifier(
            iterations=500,
            learning_rate=0.05,
            depth=6,
            random_state=42,
            verbose=False
        ),
        use_scaler=False
    )












