"""
app/main.py

PURPOSE OF THIS FILE:
This is the entry point for the entire application.
It spins up the FastAPI server, connects to the database, and mounts our routers.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.init_db import init_db
from app.api import user_routes, auth_routes
from app.api import vehicle_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="RenTrik API", lifespan=lifespan)

app.include_router(auth_routes.router, tags=["authentication"])
app.include_router(user_routes.router, tags=["users"])
app.include_router(vehicle_routes.router, tags=["vehicles"])

@app.get("/")
def root():
    return {"message": "RenTrik : Your Journey. Our Wheels.🚀"}