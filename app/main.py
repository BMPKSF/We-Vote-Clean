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

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()