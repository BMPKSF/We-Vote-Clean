from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.pydantic_schemas import VoteCreate
from app.db.models import Vote, Issue, User
from sqlalchemy import select

router = APIRouter()

@router.post("/")
async def cast_vote(payload: VoteCreate, user_id: int = 1, db: AsyncSession = Depends(get_db)):
    # NOTE: user_id param simplified; integrate auth later.
    # Validate user and issue
    q = await db.execute(select(User).where(User.id == user_id))
    user = q.scalar_one_or_none()
    if not user or not user.verified:
        raise HTTPException(403, "User not verified to vote")
    q2 = await db.execute(select(Issue).where(Issue.id == payload.issue_id))
    issue = q2.scalar_one_or_none()
    if not issue:
        raise HTTPException(404, "Issue not found")
    # prevent duplicate vote
    existing = await db.execute(select(Vote).where(Vote.user_id==user_id, Vote.issue_id==payload.issue_id))
    if existing.scalar_one_or_none():
        raise HTTPException(400, "User already voted on this issue")
    v = Vote(user_id=user_id, issue_id=payload.issue_id, choice=payload.choice)
    db.add(v)
    await db.commit()
    await db.refresh(v)
    return {"status": "ok", "vote_id": v.id}