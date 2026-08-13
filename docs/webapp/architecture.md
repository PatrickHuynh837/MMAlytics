# Web Application Architecture

## Frontend

The frontend provides interfaces for:

- Fight Dashboard
- Fighter Profiles
- Prediction View

## Backend

The backend provides:

- Prediction Endpoint
- Fighter Endpoint
- Fight Endpoint
- Historical Analysis

## Storage

- PostgreSQL (Neon)

The database stores:

- Fighters
- Fights
- Fighter Statistics
- Historical Data
- Predictions

## Prediction Flow

The Prediction Endpoint uses:

- Fighter Data
- Historical Performance
- Prediction Model

The prediction service returns:

- Predicted Winner
- Win Probability
- Model Version
- Prediction Metadata

## Deployment

- Railway
- Docker (upcoming)