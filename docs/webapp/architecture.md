# Web Application Architecture

## Overview

MMAlytics is a web application for UFC/MMA fight analysis, fighter
statistics, historical analytics, and machine-learning-based fight
predictions.

The application is composed of four primary systems:

- Frontend
- Backend API
- Machine Learning
- PostgreSQL Database

The frontend communicates with the backend API through HTTP requests.
The backend coordinates access to application data and the machine
learning prediction system.

---

## Architecture

```text
┌──────────────────────┐
│        User          │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│   React Frontend     │
│                      │
│ • Fight Dashboard    │
│ • Fighter Profiles   │
│ • Predictions        │
│ • Comparisons        │
│ • Analytics          │
└──────────┬───────────┘
           │ HTTP
           ↓
┌──────────────────────┐
│   Python / FastAPI   │
│      Backend API     │
│                      │
│ • Fighter Data       │
│ • Fight Data         │
│ • Historical Data    │
│ • Prediction API     │
└───────┬────────┬─────┘
        │        │
        ↓        ↓
┌────────────┐  ┌──────────────────┐
│ PostgreSQL │  │ Machine Learning │
│            │  │                  │
│ • Fighters │  │ • Features       │
│ • Fights   │  │ • Models         │
│ • Stats    │  │ • Inference      │
│ • History  │  │ • Predictions    │
└────────────┘  └──────────────────┘
```

---

## System Components

### Frontend

The frontend provides the user-facing interface for MMAlytics.

Primary interfaces include:

- Fight Dashboard
- Fighter Profiles
- Prediction View
- Fighter Comparison
- Historical Analytics
- Matchup Visualization

The frontend communicates with the backend through HTTP API requests.

The frontend is responsible for:

- Presenting fighter and fight information
- Displaying historical statistics
- Submitting prediction requests
- Displaying prediction results
- Providing visualizations for matchup analysis

---

### Backend API

The backend provides the application's HTTP API and acts as the
coordination layer between the frontend, database, and machine learning
system.

The backend is responsible for:

- Fighter data retrieval
- Fight data retrieval
- Historical analysis
- Prediction requests
- Prediction responses
- Database access
- ML model inference

The backend is implemented in Python using FastAPI.

Because the ML system is also implemented in Python, inference can be
performed directly within the backend. This allows the application to
share feature engineering and model-loading logic without requiring a
separate inference service.

---

### Machine Learning System

The machine learning system is responsible for generating fight
predictions from historical fight data.

The ML pipeline includes:

- Data preparation
- Feature engineering
- Model training
- Model evaluation
- Model versioning
- Model inference

The ML system is implemented in Python and uses the datasets and
feature-engineering processes defined in the `mlsystems/` documentation.

The prediction system separates:

- Offline data processing and model training
- Online model inference

This allows prediction requests to use preprocessed historical
information rather than rebuilding the entire historical dataset for
each request.

---

### Database

PostgreSQL provides persistent application storage.

The database stores application and historical data including:

- Fighters
- Fights
- Fighter statistics
- Historical data
- Predictions

The database acts as the persistent source of application data.

Model-specific transformations and derived features can be separated
from the core historical data where appropriate.

---

## Technology Stack

### Frontend

- React

### Backend

- Python
- FastAPI

### Database

- PostgreSQL
- Neon

### Machine Learning

- Python
- Pandas
- Scikit-learn

---

## Data Flow

The general request flow is:

```text
User
  ↓
React Frontend
  ↓ HTTP Request
Python / FastAPI Backend
  ↓
  ├──────────────→ PostgreSQL
  │                    ↓
  │              Historical Data
  │                    ↓
  │              Fighter Statistics
  │
  └──────────────→ ML Inference
                       ↓
                 Prediction Model
                       ↓
                 Prediction Result
                       ↓
                  API Response
                       ↓
                React Frontend
                       ↓
                     User
```

The backend determines which data is required for a request and
coordinates access to the database and ML prediction system.

---

## Prediction Pipeline

The prediction pipeline uses historical fight data to generate the
features required by the prediction model.

```text
Historical Fight Data
        ↓
Data Processing
        ↓
Feature Engineering
        ↓
Fighter / Matchup Features
        ↓
Trained Prediction Model
        ↓
Prediction
        ↓
API Response
        ↓
Frontend
```

### Feature Generation

Historical fight data is transformed into fighter and matchup features.

These features may include information derived from:

- Fighter statistics
- Previous fight results
- Historical performance
- Recent performance
- Matchup characteristics

The resulting features are provided to the trained prediction model
during inference.

### Model Inference

When a user requests a prediction, the backend:

1. Identifies the fighters and matchup.
2. Retrieves the relevant historical information.
3. Generates or retrieves the required features.
4. Loads the appropriate model version.
5. Performs inference.
6. Returns the prediction through the API.

---

## Data and Prediction Lifecycle

Historical data and online prediction requests follow separate
processing paths.

### Historical Data

```text
Completed Fight
      ↓
Historical Dataset
      ↓
Data Processing
      ↓
Feature Engineering
      ↓
Updated Fighter / Matchup Features
```

When new fights are completed, they are added to the historical dataset.
Relevant fighter statistics and derived features are then updated.

### Prediction Request

```text
Upcoming Fight
      ↓
Most Recent Historical Data
      ↓
Fighter / Matchup Features
      ↓
Prediction Model
      ↓
Prediction
```

Upcoming fights use the most recent available historical information
when generating predictions.

This separation allows historical data processing to occur independently
from online prediction requests.

---

## Architectural Responsibilities

| Component | Primary Responsibility |
|---|---|
| React Frontend | User interface and visualization |
| FastAPI Backend | API, application logic, and system coordination |
| PostgreSQL | Persistent application and historical data |
| ML System | Feature engineering, model training, evaluation, and inference |

---

## Design Principles

The architecture is designed around several principles:

### Separation of Concerns

The frontend, backend, database, and ML system have distinct
responsibilities.

### Reusable ML Pipeline

Feature engineering and model inference are implemented in Python so
that the same logic can be reused during training and prediction.

### Historical Data as the Foundation

Predictions are generated from historical fight and fighter data rather
than treating each matchup as an isolated observation.

### Offline Training and Online Inference

Computationally expensive data processing and model training can occur
offline, while prediction requests use the resulting model and prepared
features during online inference.

### API-Based Communication

The frontend communicates with the backend through a defined HTTP API,
allowing the presentation layer to remain independent from the
underlying database and ML implementation.