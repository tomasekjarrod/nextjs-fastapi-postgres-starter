from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schemas import UserRead
from db_engine import engine
from sqlalchemy import select

router = APIRouter()

@router.get("/me")
async def get_my_user():
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Sample logic to simplify getting the current user. There's only one user.
            result = await session.execute(select(User))
            user = result.scalars().first()

            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return UserRead(id=user.id, name=user.name)