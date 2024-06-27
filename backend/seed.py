from sqlalchemy import select, func
from sqlalchemy.orm import Session
from db_engine import sync_engine
from models import User, Thread


def seed_user_if_needed():
    with Session(sync_engine) as session:
        with session.begin():
            if session.execute(select(User)).scalar_one_or_none() is not None:
                print("User already exists, skipping seeding")
                return
            print("Seeding user")
            session.add(User(name="Alice"))
            session.commit()

def seed_threads_if_needed():
    with Session(sync_engine) as session:
        with session.begin():
            thread_count = session.execute(select(func.count(Thread.id))).scalar_one()
            if thread_count == 2:
                print("Exactly two users already exist, skipping seeding")
                return
            
            result = session.execute(select(User))
            user = result.scalars().first()
            
            if user is None:
                print("No existing user to create threads with")
                return
            
            print("Seeding threads")
            session.add_all([Thread(created_by=user.id), Thread(created_by=user.id)])
            session.commit()