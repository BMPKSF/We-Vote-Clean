from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models import Issue
from app.schemas.pydantic_schemas import IssueCreate, IssueOut

router = APIRouter()

@router.post("/", response_model=IssueOut)
async def create_issue(payload: IssueCreate, db: AsyncSession = Depends(get_db)):
    issue = Issue(title=payload.title, summary=payload.summary, jurisdiction=payload.jurisdiction)
    db.add(issue)
    await db.commit()
    await db.refresh(issue)
    return issue

@router.get("/", response_model=list[IssueOut])
async def list_issues(db: AsyncSession = Depends(get_db)):
    result = await db.execute(Issue.__table__.select().order_by(Issue.id.desc()))
    rows = result.fetchall()
    return [IssueOut.from_orm(row._mapping) for row in rows]