# MMAlytics ML System Architecture

## Goal

MMAlytics is a web application that analyzes future MMA fights using historical data.

The system currently focuses on UFC data, with the long-term goal of supporting data from multiple MMA organizations.

## Major Components

- Data Pipeline
  - Data ingestion
  - Data cleaning
  - Database storage
  - Data transformation

- Feature Engineering
  - Differentials
  - Rolling statistics
  - Engineered matchup features

- Model Construction
  - Logistic Regression
  - Random Forest
  - XGBoost
  - CatBoost

- Model Evaluation
  - Classification metrics
  - Unsupervised metrics
  - Time-based validation

- Web Application
  - Fighter analytics
  - Matchup research
  - Predictive modeling
  - Style discovery and trajectory analysis
  - Historical similarity