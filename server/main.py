# server/main.py

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine, text
from fastapi.middleware.cors import CORSMiddleware


# Load environment variables from .env
load_dotenv(
    Path(__file__).resolve().parents[1] / ".env"
)


# Get database URL
DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError("DB_URL is missing from environment variables")


# Create SQLAlchemy engine
engine = create_engine(DB_URL)


# Creates the application
app = FastAPI(title="MMAlytics API")

# Add CORS middleware to allow requests from     the React client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Defines a GET endpoint at /events
@app.get("/events")
def get_events():

    # Get a database connection
    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    event_url,
                    event_name,
                    event_date,
                    location_city,
                    location_state,
                    location_country
                FROM raw.event_data
                ORDER BY event_date DESC
            """)
        )


        # Convert database rows into dictionaries
        events = [dict(row._mapping) for row in result]

    # Return events to the client
    return events


# Defines a GET endpoint at /fighters
@app.get("/fighters")
def get_fighters():

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    fighter_url,
                    fighter_f_name || ' ' || fighter_l_name AS fighter_name,
                    fighter_nickname,
                    NULLIF(fighter_height_cm, 'NaN'::double precision) AS fighter_height_cm,
                    NULLIF(fighter_weight_lbs, 'NaN'::double precision) AS fighter_weight_lbs,
                    NULLIF(fighter_reach_cm, 'NaN'::double precision) AS fighter_reach_cm,
                    fighter_stance,
                    fighter_w,
                    fighter_l,
                    fighter_d
                FROM raw.fighter_data
                ORDER BY fighter_l_name, fighter_f_name
            """)
        )

        fighters = [dict(row._mapping) for row in result]

    return fighters
