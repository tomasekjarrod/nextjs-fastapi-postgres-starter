from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from schemas import *
from models import *
from db_engine import engine
from seed import seed_user_if_needed, seed_threads_if_needed

seed_user_if_needed()
seed_threads_if_needed()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/threads", response_model=List[ThreadRead])
async def get_threads():
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(Thread))
            threads = result.scalars().all()

            return list(map(lambda thread: ThreadRead(id=thread.id, created_at=thread.created_at, created_by=thread.created_by), threads))
            
            
@app.get("/thread_messages", response_model=List[ThreadMessageRead])
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
