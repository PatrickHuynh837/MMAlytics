# Frontend Architecture

## Overview

The MMAlytics frontend is a React-based web application that provides
the user interface for analyzing UFC/MMA fight data, comparing fighters,
exploring historical statistics, and requesting machine-learning-based
fight predictions.

The frontend is responsible for presentation, user interaction, data
visualization, and communication with the backend API.

The frontend does not communicate directly with PostgreSQL or the machine
learning system.

---

## Architecture

```text id="x2p8cy"
┌──────────────────────────┐
│          User            │
└────────────┬─────────────┘
             │
             ↓
┌──────────────────────────┐
│      React Frontend      │
│                          │
│ • Pages / Routes         │
│ • UI Components         │
│ • State Management      │
│ • Data Visualization    │
│ • User Interactions     │
└────────────┬─────────────┘
             │ HTTP
             ↓
┌──────────────────────────┐
│     FastAPI Backend      │
└────────────┬─────────────┘
             │
       ┌─────┴─────┐
       ↓           ↓
 PostgreSQL     ML System
```

The frontend communicates exclusively with the FastAPI backend through
HTTP requests.

---

## Technology Stack

### Core

* React
* Vite
* React Router

The frontend uses React for component-based UI development and Vite as
the frontend build tool.

React Router manages client-side navigation between application views.

### Data Fetching and State Management

* TanStack Query
* Zustand or React Context
* Fetch API or Axios

TanStack Query manages asynchronous server state, caching, loading
states, and API request lifecycle management.

Lightweight client-side state can be managed using Zustand or React
Context for values such as:

* User preferences
* Selected fighters
* UI state

### UI and Styling

* CSS / CSS Modules
* Recharts or Chart.js
* Lucide React or React Icons

The frontend uses data visualization libraries to represent historical
fighter statistics, matchup differentials, and prediction results.

---

## Application Structure

The frontend is organized around the major capabilities of MMAlytics.

```text id="u2v6y7"
React Application
│
├── Pages
│   ├── Dashboard
│   ├── Fighter Profile
│   ├── Fight / Matchup Analysis
│   └── Prediction
│
├── Components
│   ├── Fighter Components
│   ├── Fight Components
│   ├── Prediction Components
│   ├── Charts
│   └── Shared UI
│
├── API Layer
│   ├── Fighter Requests
│   ├── Fight Requests
│   └── Prediction Requests
│
├── State Management
│   ├── Server State
│   └── Client State
│
└── Styling
```

This structure separates page-level application views from reusable UI
components and API communication logic.

---

## Key Pages

### Dashboard

**Route:** `/`

The dashboard provides an overview of the MMAlytics system.

Potential functionality includes:

* Upcoming UFC events
* Upcoming fights
* Featured predictions
* Recent prediction results
* Model performance metrics
* Recent historical activity

---

### Fighter Profile

**Route:** `/fighter/:id`

The fighter profile provides detailed information about an individual
fighter.

Potential functionality includes:

* Fighter information
* Historical fight record
* Fighter statistics
* Rolling averages
* Performance trends
* Striking statistics
* Grappling statistics
* Recent fights

Charts are used where appropriate to make historical trends easier to
interpret.

---

### Fight / Matchup Analysis

**Route:** `/fight/:id`

The matchup analysis page compares two fighters competing in a specific
fight.

Potential functionality includes:

* Side-by-side fighter statistics
* Striking comparison
* Grappling comparison
* Historical performance
* Matchup-specific statistics
* Radar / spider charts
* Prediction information

---

### Prediction View

**Route:** `/predict`

The prediction view allows users to select two fighters and request a
machine-learning-based prediction.

The interface displays:

* Selected fighters
* Predicted winner
* Win probability
* Model version
* Relevant matchup statistics
* Key factors contributing to the prediction

The frontend sends the prediction request to the FastAPI backend rather
than running the ML model directly.

---

## Routing

The frontend uses client-side routing to provide separate application
views.

Initial routes include:

| Route          | Purpose                          |
| -------------- | -------------------------------- |
| `/`            | Application dashboard            |
| `/fighter/:id` | Fighter profile                  |
| `/fight/:id`   | Fight and matchup analysis       |
| `/predict`     | Interactive prediction interface |

Additional routes can be introduced as application functionality
expands.

---

## Data Fetching Strategy

The frontend communicates exclusively with the FastAPI backend.

```text id="3jkwcg"
React Component
      ↓
API Request
      ↓
FastAPI Backend
      ↓
PostgreSQL / ML System
      ↓
JSON Response
      ↓
React Query
      ↓
UI Update
```

The frontend does not access PostgreSQL directly and does not load or
execute ML models.

This keeps database access and ML implementation details isolated within
the backend.

---

## Server State

TanStack Query is used to manage data retrieved from the backend.

It provides:

* Request caching
* Cache invalidation
* Loading states
* Error states
* Request deduplication
* Background refetching

Fighter and historical statistics can be cached because they generally
remain stable between fight events.

This reduces unnecessary API requests and improves the responsiveness of
the application.

---

## Client State

Client-side state is used for information that does not need to be
persisted on the server.

Examples include:

* Selected fighters
* UI preferences
* Modal state
* Filters
* Visualization settings

Zustand or React Context can be used depending on the complexity of the
state.

Server data should remain managed by the server-state layer rather than
being duplicated unnecessarily in global client state.

---

## Prediction Request Flow

The prediction interface follows this lifecycle:

```text id="1d0o3p"
User Selects Fighters
        ↓
Frontend Validates Selection
        ↓
POST /predict
        ↓
FastAPI Backend
        ↓
ML Inference
        ↓
Prediction Response
        ↓
React Query
        ↓
Prediction UI
```

### Prediction Steps

1. The user selects Fighter A and Fighter B.
2. The frontend validates the selection.
3. The frontend sends a `POST /predict` request.
4. The UI displays a loading state while the request is processed.
5. The FastAPI backend performs the required data retrieval and ML
   inference.
6. The backend returns the prediction.
7. The frontend displays the predicted winner and win probability.
8. Additional prediction metadata can be displayed alongside the
   result.

---

## Loading and Error States

The frontend should provide clear feedback throughout asynchronous
operations.

### Loading States

Loading states can include:

* Skeleton components
* Loading indicators
* Disabled actions
* Prediction processing indicators

### Error States

The frontend should handle errors including:

* Invalid requests
* Fighter not found
* Fight not found
* Prediction failures
* Backend unavailable
* ML inference failures
* Network failures

Errors should be translated into user-friendly messages rather than
exposing internal backend or ML implementation details.

---

## Data Visualization

MMAlytics is designed around visual analysis of MMA data.

Visualizations may include:

* Historical performance trends
* Rolling averages
* Fighter statistical comparisons
* Striking differentials
* Grappling differentials
* Win probability
* Matchup comparisons
* Prediction factors

Charts should prioritize readability and provide enough context for
users to understand what the underlying statistics represent.

---

## Design and UI/UX Principles

### Data-First Design

The interface should make complex MMA statistics understandable without
requiring users to interpret raw datasets.

### Visual Hierarchy

Important information such as fighter identity, matchup statistics, and
prediction results should be visually prominent.

### Data Legibility

Charts, tables, and statistical indicators should be easy to read and
interpret.

Color and visual indicators can be used to communicate statistical
advantages and disadvantages, but should not be the only method of
communicating important information.

### Responsive Interaction

The application should provide immediate visual feedback for:

* Navigation
* Fighter selection
* Data loading
* Prediction requests
* Chart interactions

Subtle animations and transitions can be used to improve perceived
responsiveness without distracting from the data.

### Consistent Design

Reusable components should be used for common interface patterns such
as:

* Fighter cards
* Statistic cards
* Tables
* Charts
* Prediction displays
* Loading states
* Error states

---

## API Integration

The frontend communicates with the backend through defined HTTP
endpoints.

Initial API interactions include:

| Frontend Feature | Backend Endpoint    |
| ---------------- | ------------------- |
| Fighter Profile  | `GET /fighters/:id` |
| Fight Analysis   | `GET /fights/:id`   |
| Prediction       | `POST /predict`     |

The frontend expects structured JSON responses from the backend.

Detailed request and response contracts are documented in the backend
`api-reference.md`.

---

## Relationship to Backend

The frontend is decoupled from the database and machine learning
implementation.

```text
Frontend
   │
   │ HTTP / JSON
   ↓
FastAPI Backend
   │
   ├──────────────→ PostgreSQL
   │
   └──────────────→ ML Inference
```

The frontend is responsible for:

* User interaction
* Presentation
* Visualization
* Client-side state
* Server-state management
* API communication

The backend is responsible for:

* API handling
* Application logic
* Database access
* Historical data retrieval
* ML inference coordination
* Prediction responses

The frontend therefore does not need to know how PostgreSQL queries,
feature engineering, or model inference are implemented internally.

---

## Relationship to ML Systems

The frontend does not directly interact with the ML training or
inference pipeline.

Instead, it receives structured prediction responses from the backend.

The ML system is responsible for:

* Data processing
* Feature engineering
* Model training
* Model evaluation
* Model versioning
* Model artifacts

The backend is responsible for integrating those ML components into the
application.

The frontend is responsible for presenting the resulting predictions in
a way that is understandable to users.

