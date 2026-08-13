# Backend

## Overview

The backend provides the API and application logic for the MMAlytics web
application.

It acts as the coordination layer between the React frontend,
PostgreSQL database, and machine learning system.

The backend is responsible for:

* Serving fighter and fight data
* Retrieving historical statistics
* Coordinating prediction requests
* Preparing inference inputs
* Running ML inference
* Returning prediction results
* Storing prediction results
* Handling application and infrastructure errors

---

## Technology Stack

* Python
* FastAPI
* PostgreSQL
* Neon

The backend is implemented in Python so that it can integrate directly
with the Python-based machine learning system.

FastAPI provides the HTTP API consumed by the React frontend and
automatically generates OpenAPI documentation.

---

## API

The backend exposes HTTP endpoints consumed by the React frontend.

### Initial Endpoints

| Method | Endpoint        | Purpose                      |
| ------ | --------------- | ---------------------------- |
| `GET`  | `/fighters/:id` | Retrieve fighter information |
| `GET`  | `/fights/:id`   | Retrieve fight information   |
| `POST` | `/predict`      | Generate a fight prediction  |

See `api-reference.md` for detailed endpoint contracts, request
schemas, response schemas, and error responses.

### API Responsibilities

The API layer is responsible for:

* Validating incoming requests
* Retrieving application data
* Coordinating prediction requests
* Returning structured responses
* Handling application errors
* Exposing OpenAPI documentation

The API does not contain the model training pipeline. Training and model
development are handled by the ML system.

---

## Database

The backend communicates with PostgreSQL to retrieve and persist
application data.

The database stores:

* Fighters
* Fights
* Fighter Statistics
* Historical Data
* Predictions

The backend uses the database as the persistent source of application
and historical data.

Database access is kept separate from the ML training pipeline so that
the API can retrieve the data required for online inference without
rebuilding the entire historical dataset.

---

## Machine Learning Integration

The backend coordinates prediction requests between the frontend and
machine learning system.

The general flow is:

```text
React Frontend
      ↓
FastAPI Backend
      ↓
ML Inference Module
      ↓
Prediction Model
      ↓
FastAPI Backend
      ↓
React Frontend
```

Because the backend and ML system are both implemented in Python, the
backend can integrate with the ML system natively.

The backend can:

* Load pre-trained models into memory
* Import shared feature engineering logic
* Prepare inference data
* Generate matchup-specific features
* Execute model inference
* Return prediction results

The backend does not duplicate the model training pipeline.

---

## Prediction Architecture

The prediction endpoint uses the most recent available fighter
information rather than recomputing the complete historical dataset for
each request.

The prediction process is:

```text
Upcoming Fight
      ↓
Retrieve Fighter A Data
      ↓
Retrieve Fighter B Data
      ↓
Retrieve Most Recent Features
      ↓
Generate Matchup Features
      ↓
ML Inference
      ↓
Prediction Result
      ↓
Store Prediction
      ↓
API Response
```

### Prediction Steps

For an upcoming fight, the backend:

1. Receives the prediction request.
2. Validates the fighter and matchup information.
3. Retrieves the required fighter data.
4. Retrieves the most recent available historical features.
5. Generates matchup-specific features.
6. Passes the resulting feature vector to the prediction model.
7. Runs model inference.
8. Stores the prediction result when appropriate.
9. Returns the prediction to the frontend.

---

## Model Loading

Pre-trained machine learning models are loaded by the backend for
inference.

The models may include:

* Scikit-learn models
* CatBoost models

Model artifacts are produced by the ML training pipeline.

The backend is responsible for loading the appropriate model and using it
for inference. Model training, evaluation, and experimentation remain
part of the `mlsystems/` workflow.

---

## Prediction Response

The prediction service returns information required by the frontend to
display and interpret a prediction.

A prediction response includes:

* Predicted Winner
* Win Probability
* Model Version
* Prediction Metadata

The model version is included so that predictions can be associated
with the specific model used during inference.

---

## Error Handling

The backend should provide consistent error handling for failures
throughout the request lifecycle.

The backend should handle:

* Invalid requests
* Invalid fighter IDs
* Invalid fight IDs
* Missing fighters
* Missing fights
* Missing historical data
* Database errors
* Prediction failures
* ML inference errors
* Invalid or incompatible model inputs

Errors should return structured HTTP responses that allow the frontend
to distinguish between client-side request errors and server-side
failures.

---

## Data Flow

### Standard Data Request

```text
User
  ↓
React Frontend
  ↓
HTTP Request
  ↓
FastAPI Endpoint
  ↓
Database Query
  ↓
PostgreSQL
  ↓
Database Response
  ↓
FastAPI
  ↓
HTTP Response
  ↓
React Frontend
```

### Prediction Request

```text
User
  ↓
React Frontend
  ↓
POST /predict
  ↓
FastAPI Backend
  ↓
Validate Request
  ↓
Retrieve Fighter / Historical Data
  ↓
Feature Preparation
  ↓
ML Inference
  ↓
Prediction Result
  ↓
Persist Prediction
  ↓
API Response
  ↓
React Frontend
```

---

## Separation of Responsibilities

The backend and ML system have distinct responsibilities.

| System    | Responsibility                                                  |
| --------- | --------------------------------------------------------------- |
| Backend   | API, application logic, data access, inference coordination     |
| ML System | Data pipelines, feature engineering, model training, evaluation |
| Database  | Persistent application and historical data                      |
| Frontend  | User interface, visualization, and API interaction              |

The backend consumes trained ML artifacts and shared inference logic
rather than implementing the training workflow itself.

---

## Relationship to ML Systems

The `mlsystems/` documentation describes the machine learning lifecycle,
including:

* Data pipelines
* Data preprocessing
* Feature engineering
* Model training
* Model evaluation
* Model versioning
* Model artifacts

The backend consumes the resulting models and inference components.

This separation allows the ML system to evolve independently from the
web application's API while maintaining a defined interface between
model inference and the application.

---

## Deployment

The backend is currently deployed using:

* Railway

Planned infrastructure includes:

* Docker

The backend deployment environment is responsible for running the
FastAPI application and providing access to the required database and
ML model artifacts.

---

## Backend Design Principles

### Separation of Concerns

The backend separates API handling, application logic, database access,
and ML inference coordination.

### Native Python ML Integration

Using Python for both the backend and ML system allows models and shared
feature engineering code to be integrated without requiring a separate
inference service.

### Efficient Inference

Prediction requests use the most recent available historical features
instead of recomputing the complete historical dataset for every
request.

### Model Versioning

Prediction responses identify the model version used for inference,
allowing predictions to be traced back to a specific model artifact.

### API-First Architecture

The React frontend communicates with the backend through defined HTTP
endpoints, keeping the frontend decoupled from the database and ML
implementation.

### Reproducible ML Integration

The backend consumes the same feature engineering logic and model
artifacts produced by the ML workflow, reducing the risk of training and
inference inconsistencies.
