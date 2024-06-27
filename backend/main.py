from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import *
from models import *
from seed import seed_user_if_needed, seed_threads_if_needed
from routes import threads, users, thread_messages

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

app.include_router(threads.router, prefix="/threads")
app.include_router(users.router, prefix="/users")
app.include_router(thread_messages.router, prefix="/thread_messages")
