from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    email: str
    password: Optional[str]

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    verified: bool

    class Config:
        orm_mode = True

class IssueCreate(BaseModel):
    title: str
    summary: Optional[str]
    jurisdiction: Optional[str]

class IssueOut(BaseModel):
    id: int
    title: str
    summary: Optional[str]
    jurisdiction: Optional[str]

    class Config:
        orm_mode = True

class VoteCreate(BaseModel):
    issue_id: int
    choice: str