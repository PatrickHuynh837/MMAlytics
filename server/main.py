# server/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes import events, fighters, fights


# Creates the application
app = FastAPI(title="MMAlytics API")

# Add CORS middleware to allow requests from the React client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Get Endpoints
app.include_router(events.router)
app.include_router(fighters.router)
# app.include_router(fights.router)
