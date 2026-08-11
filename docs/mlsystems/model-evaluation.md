# Model Evaluation

## Classification Metrics

Current evaluation includes:

- Confusion Matrix
- ROC-AUC

## Unsupervised Evaluation

Clustering experiments are evaluated using:

- Silhouette Score

## Validation Strategy

Model validation uses a time-based train/test split.

The temporal split is intended to prevent future information from
being used to evaluate predictions on earlier fights.