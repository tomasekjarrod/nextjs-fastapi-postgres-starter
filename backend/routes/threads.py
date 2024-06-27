from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from models import Thread
from schemas import ThreadRead
from db_engine import engine
from sqlalchemy import select
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ThreadRead])
async def get_threads():
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(Thread))
            threads = result.scalars().all()

            return list(map(lambda thread: ThreadRead(id=thread.id, created_at=thread.created_at, created_by=thread.created_by), threads))