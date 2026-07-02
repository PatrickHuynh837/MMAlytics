import pandas as pd






# pipeline = Pipeline([
#     ("imputer", SimpleImputer(strategy="median")),
#     ("scaler", StandardScaler()),
#     ("model", LogisticRegression(class_weight='balanced', max_iter=1000))
# ])

# param_dist = {
#     "model__C": [0.001, 0.01, 0.1, 1, 10, 100],
#     "model__penalty": ["l2"],
# }

# tscv = TimeSeriesSplit(n_splits=5)

# search = RandomizedSearchCV(
#     estimator=pipeline,
#     param_distributions=param_dist,
#     n_iter=6,
#     scoring="roc_auc",
#     cv=tscv,
#     random_state=42,
#     n_jobs=-1
# )

# # ---- time-based split ----
# split_idx = int(len(df) * 0.8)

# train_df = df.iloc[:split_idx]
# test_df = df.iloc[split_idx:]

# X_train = train_df[feature_cols]
# y_train = train_df["fighter_1_win"]

# X_test = test_df[feature_cols]
# y_test = test_df["fighter_1_win"]

# # ---- hyperparameter search ----
# search.fit(X_train, y_train)

# # ---- IMPORTANT: use best model, not pipeline ----
# best_model = search.best_estimator_

# # ---- evaluation ----
# preds = best_model.predict(X_test)
# probs = best_model.predict_proba(X_test)[:, 1]

# accuracy = accuracy_score(y_test, preds)
# precision = precision_score(y_test, preds)
# recall = recall_score(y_test, preds)
# f1 = f1_score(y_test, preds)
# roc_auc = roc_auc_score(y_test, probs)

# print("Best params:", search.best_params_)
# print("Accuracy:", accuracy)
# print("Precision:", precision)
# print("Recall:", recall)
# print("F1:", f1)
# print("ROC AUC:", roc_auc)

# print("\nConfusion Matrix:")
# print(confusion_matrix(y_test, preds))

# print("\nClassification Report:")
# print(classification_report(y_test, preds))

def preprocess_ranks():
    df["fighter_1_is_ranked"] = (
    df["fighter_1_rank"].between(0, 15)
).astype(int)

df["fighter_2_is_ranked"] = (
    df["fighter_2_rank"].between(0, 15)
).astype(int)

#Fill in ranks
df["fighter_1_rank"] = df["fighter_1_rank"].fillna(16)
df["fighter_2_rank"] = df["fighter_2_rank"].fillna(16)
