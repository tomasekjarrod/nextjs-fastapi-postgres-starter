from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import ThreadMessage
from schemas import ThreadMessageRead, ThreadMessageCreate
from db_engine import engine
from sqlalchemy import select
from typing import List
from sqlalchemy.exc import SQLAlchemyError
import random

router = APIRouter()

@router.get("/", response_model=List[ThreadMessageRead])
async def get_thread_messages(thread_id: int):
    async with AsyncSession(engine) as session:
        async with session.begin():
            # In the future, thread_id would be an optional parameter to apply to the query
            result = await session.execute(select(ThreadMessage).filter(ThreadMessage.thread_id == thread_id))
            threadMessages = result.scalars().all()

            fn = lambda thread_message: ThreadMessageRead(
                id=thread_message.id, 
                content=thread_message.content, 
                sender_id=thread_message.sender_id, 
                thread_id=thread_message.thread_id, 
                created_at=thread_message.created_at
            )
            return list(map(fn, threadMessages))


@router.post("/ai")
async def create_thread_message(threadMessage: ThreadMessageCreate):
    async with AsyncSession(engine) as session:
        async with session.begin():
            try:
                db_thread_message = ThreadMessage(**threadMessage.model_dump())
                session.add(db_thread_message)
                await session.flush()

                ai_content = "AI generated %s" % random.randint(0, 10)
                ai_thread_message = ThreadMessage(content=ai_content, sender_id=None, thread_id=threadMessage.thread_id)
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
            