from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User
from app.schemas.pydantic_schemas import UserCreate, UserOut
from app.db.database import get_db
from sqlalchemy import select

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    # simple email uniqueness check
    q = await db.execute(select(User).where(User.email == payload.email))
    if q.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(full_name=payload.full_name, email=payload.email, hashed_password=payload.password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/mock-verify/{user_id}")
async def mock_verify(user_id: int, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User).where(User.id == user_id))
    user = q.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "user not found")
    user.verified = True
    user.kyc_provider = "mock"
    user.kyc_reference = "mock-ref"
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"status": "verified"}