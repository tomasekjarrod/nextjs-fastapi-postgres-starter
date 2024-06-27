from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from seed import seed_user_if_needed
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from db_engine import engine
from models import User, Thread, ThreadMessage
from datetime import datetime
from typing import List, Optional
seed_user_if_needed()

app = FastAPI()


class UserRead(BaseModel):
    id: int
    name: str

class ThreadMessageBase(BaseModel):
    content: str
    sender_id: Optional[int] = None
    thread_id: int

class ThreadMessageCreate(ThreadMessageBase):
    pass

class ThreadMessageRead(ThreadMessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ThreadBase(BaseModel):
    created_by: int

class ThreadCreate(ThreadBase):
    pass

class ThreadRead(ThreadBase):
    id: int
    created_at: datetime
    
    messages: List[ThreadMessageRead]
    class Config:
        from_attributes = True


@app.get("/users/me")
async def get_my_user():
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Sample logic to simplify getting the current user. There's only one user.
            result = await session.execute(select(User))
            user = result.scalars().first()

            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return UserRead(id=user.id, name=user.name)


@app.get("/threads/{thread_id}", response_model=ThreadRead)
async def get_thread(thread_id: int):
    async with AsyncSession(engine) as session:
        async with session.begin():
            # TODO: Change to eager loading from over eager loading            
            result = await session.execute(select(Thread).options(joinedload(Thread.messages)).filter(Thread.id == thread_id))
            thread = result.scalars().first()

            if thread is None:
                raise HTTPException(status_code=404, detail="Thread not found")
            return thread
        
        
@app.post("/threads")
async def create_thread(thread: ThreadCreate):
    async with AsyncSession(engine) as session:
        async with session.begin():
            await session.execute()
            
@app.post("/thread_messages")
async def create_thread_message(threadMessage: ThreadMessageCreate):
    async with AsyncSession(engine) as session:
        async with session.begin():
            await session.execute()