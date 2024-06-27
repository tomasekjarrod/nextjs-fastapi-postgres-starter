from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# User

class UserRead(BaseModel):
    id: int
    name: str
    
# ThreadMessage

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

# Thread

class ThreadBase(BaseModel):
    created_by: int

class ThreadCreate(ThreadBase):
    pass

class ThreadRead(ThreadBase):
    id: int
    created_at: datetime
    messages: Optional[List[ThreadMessageRead]] = None
    
    class Config:
        from_attributes = True