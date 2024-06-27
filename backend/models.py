from sqlalchemy import String, DateTime, Integer, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    # Relationship to threads created by the user
    threads = relationship('Thread', back_populates='user')

    # Relationship to messages sent by the user
    messages = relationship('ThreadMessage', back_populates='sender')

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"


class Thread(Base):
    __tablename__ = "thread"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Relationship to user
    user = relationship('User', back_populates='threads')
    
    # Relationship to children thread messages, ordered by created_at desc
    messages = relationship('ThreadMessage', back_populates='thread')

    def __repr__(self) -> str:
        return f"Thread(id={self.id!r}, created_at={self.created_at!r}, created_by={self.created_by!r})"


class ThreadMessage(Base):
    __tablename__ = "thread_message"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String())
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=True) # Nullable to indicate AI message vs user message
    thread_id: Mapped[int] = mapped_column(Integer, ForeignKey('thread.id'))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    # Relationship to parent thread
    thread = relationship('Thread', back_populates='messages')

    # Relationship to sender
    sender = relationship('User', back_populates='messages')

    def __repr__(self) -> str:
        return f"ThreadMessage(id={self.id!r}, content={self.content!r}, created_at={self.created_at!r}, sender_id={self.sender_id!r}, thread_id={self.thread_id!r})"