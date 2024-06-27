from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from schemas import *
from models import *
from db_engine import engine
from seed import seed_user_if_needed

seed_user_if_needed()

app = FastAPI()

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
            return ThreadRead(id=thread.id, created_by=thread.created_by, created_at=thread.created_at, messages=thread.messages)
        
        
@app.post("/threads", response_model=ThreadRead)
async def create_thread(thread: ThreadCreate):
    async with AsyncSession(engine) as session:
        async with session.begin():            
            try:
                db_thread = Thread(**thread.model_dump())
                session.add(db_thread)
                await session.flush()
                await session.refresh(db_thread)
                return ThreadRead(id=db_thread.id, created_by=db_thread.created_by, created_at=db_thread.created_at)
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=400, detail=str(e))

            
@app.post("/thread_messages_with_ai")
async def create_thread_message(threadMessage: ThreadMessageCreate):
    async with AsyncSession(engine) as session:
        async with session.begin():
            try:
                db_thread_message = ThreadMessage(**threadMessage.model_dump())
                session.add(db_thread_message)
                await session.flush()

                ai_thread_message = ThreadMessage(content="AI Generated", sender_id=None, thread_id=threadMessage.thread_id)
                session.add(ai_thread_message)
                await session.flush()           
                await session.refresh(ai_thread_message)
                
                return ThreadMessageRead(
                    id=ai_thread_message.id, 
                    content=ai_thread_message.content, 
                    sender_id=ai_thread_message.sender_id, 
                    thread_id=ai_thread_message.thread_id, 
                    created_at=ai_thread_message.created_at
                )
            except SQLAlchemyError as e:
                await session.rollback()
                raise HTTPException(status_code=400, detail=str(e))
