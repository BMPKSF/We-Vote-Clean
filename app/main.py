from fastapi import FastAPI
from app.api import auth, issues, votes
from app.db import database

app = FastAPI(title="Citizen Vote - Prototype")

# include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(issues.router, prefix="/issues", tags=["issues"])
app.include_router(votes.router, prefix="/votes", tags=["votes"])

@app.on_event("startup")
async def startup():
    await database.connect()

@app.get("/")
async def home():
    return {
        "message": "We Vote is LIVE!",
        "tagline": "Real democracy. Real voices. Verified citizens.",
        "status": "API running",
        "docs": "/docs"
    }

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()