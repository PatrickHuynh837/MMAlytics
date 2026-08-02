# MMAlytics

MMAlytics is an end-to-end MMA analytics platform that uses historical fight data, statistical analysis, and machine learning to predict fight outcomes and analyze fighter performance.

The platform transforms raw fight statistics into meaningful performance indicators and predictive features, allowing users to explore matchup analysis, fighter trends, and estimated win probabilities.

---

# Overview

Mixed Martial Arts outcomes are influenced by complex interactions between:

- Striking efficiency
- Grappling ability
- Defensive performance
- Physical attributes
- Experience
- Opponent quality
- Recent performance trends

MMAlytics attempts to quantify these factors through data engineering and machine learning.

The goal of this project is to build an analytics platform capable of:

- Predicting fight outcomes
- Comparing fighter strengths and weaknesses
- Analyzing historical performance trends
- Providing data-driven matchup insights

---

# Architecture

MMAlytics is composed of four major components:

## 1. Data Collection Pipeline

The data pipeline collects historical MMA fight information through web scraping.

Current data source:

- UFCStats

Responsibilities:

- Scrape fight records
- Collect fighter statistics
- Store historical fight information
- Prepare raw data for processing


## 2. Data Processing & Feature Engineering

Raw fight statistics are transformed into machine learning features.

Responsibilities:

- Clean historical fight data
- Generate fighter performance metrics
- Create matchup-based features
- Prepare training datasets

Examples of engineered features:

- Striking advantages
- Grappling advantages
- Experience differences
- Historical performance trends


## 3. Machine Learning Pipeline

The ML pipeline trains and evaluates classification models that estimate fight outcomes.

Current models:

- Logistic Regression
- Random Forest
- XGBoost
- CatBoost

Responsibilities:

- Train prediction models
- Compare model performance
- Evaluate prediction quality
- Generate fighter win probabilities


## 4. Analytics Application

The analytics layer will expose model predictions and fighter insights through a user-facing application.

Planned capabilities:

- Fight prediction dashboard
- Fighter comparison tools
- Historical analytics
- Matchup visualization

---

# Features

## Data Pipeline

- Historical MMA data collection
- Fighter statistics extraction
- Data cleaning and preprocessing

## Machine Learning

- Feature engineering pipeline
- Multiple classification models
- Model evaluation framework
- Probability-based fight predictions

## Analytics

- Fighter performance analysis
- Matchup analysis
- Historical trend exploration

---

# Current Model Performance

Models are evaluated using accuracy, ROC AUC, and F1 score.

| Model | Accuracy | ROC AUC | F1 Score |
|------|----------|---------|----------|
| Random Forest | 71.2% | 0.772 | 0.740 |
| CatBoost | 71.2% | 0.759 | 0.748 |
| Logistic Regression | 70.1% | 0.758 | 0.725 |
| XGBoost | 68.6% | 0.749 | 0.721 |

The current results demonstrate that historical fight statistics contain meaningful predictive signals, while future improvements will focus on additional features, automation, and model refinement.

---

# Tech Stack

## Data Engineering

- Python
- Pandas
- Web Scraping Tools

## Machine Learning

- Scikit-learn
- CatBoost
- XGBoost
- Random Forest

## Database

- PostgreSQL

---

# Installation

## Prerequisites

Ensure the following are installed:

- Python 3.x
- PostgreSQL

## Clone Repository

```bash
git clone <repository-url>

cd MMAlytics
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Usage

## Run Data Collection

```bash
python -m scripts.scrape_ufc_data
```

## Evaluate Models

```bash
python -m model.evaluation
```

---

# Project Structure

```
MMAlytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── scraper/
│   └── data collection pipeline
│
├── model/
│   ├── training
│   ├── evaluation
│   └── saved models
│
├── features/
│   └── feature engineering pipeline
│
└── docs/
    └── additional documentation
```

---

# Future Improvements

## Data Pipeline

- Automate scheduled data ingestion
- Improve scraping reliability
- Add additional MMA data sources

## Machine Learning

- Expand feature engineering
- Improve probability calibration
- Add opponent-adjusted metrics
- Perform time-based validation

## Application

- Build prediction API
- Develop analytics dashboard
- Add interactive fighter comparisons

---

# License

License information will be added in the future.