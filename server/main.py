# server/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes.events import router as events_router
# from server.routes.fighters import router as fighters_router

app = FastAPI(title="MMAlytics API")

# Allow Vite dev server to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes under /api
app.include_router(events_router, prefix="/api")
