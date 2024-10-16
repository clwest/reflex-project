from typing import Optional, List, Any
from datetime import datetime
# Reflex
import reflex as rx
from reflex_local_auth.user import LocalUser
# DB
import sqlalchemy
from sqlmodel import Field, Relationship
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
# utils
from . import utils


class UserInfo(rx.Model, table=True):
    email: str
    user_id: int = Field(foreign_key='localuser.id')
    user: LocalUser | None = Relationship() # LocalUser instance based off of user_id in FK

    # Relationships
    posts: List["BlogPostModel"] = Relationship(
        back_populates="userinfo"
    )
    contact_entries: List["ContactEntryModel"] = Relationship(
        back_populates="userinfo"
    )
    session: List["ChatSession"]  = Relationship(back_populates="userinfo") # User to Session
    
    memories: List["ChatBotMemory"] = Relationship(back_populates="userinfo") # User to ChatBotMemory


    # created_at
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'onupdate': sqlalchemy.func.now(),
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )


class BlogPostModel(rx.Model, table=True):
    # User
    userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
    userinfo: Optional['UserInfo'] = Relationship(back_populates="posts")
    
    title: str
    content: str
    
    # created_at
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'onupdate': sqlalchemy.func.now(),
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )
    
    is_published: bool = False
    publish_date: datetime = Field(
        default=None,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={},
        nullable=True
    )

class ContactEntryModel(rx.Model, table=True):
    user_id: int | None = None
    userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
    userinfo: Optional['UserInfo'] = Relationship(back_populates="contact_entries")
    first_name: str
    last_name: str | None = None
    email: str = Field(nullable=True)
    message: str
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )

class ChatSession(rx.Model, table=True):
    # Optional relationship to UserInfo
    userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
    userinfo: Optional['UserInfo'] = Relationship(back_populates="session")

    # Relationships
    messages: List["ChatMessage"] = Relationship(back_populates="session")

    # Timestamp
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'onupdate': sqlalchemy.func.now(),
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )

class ChatMessage(rx.Model, table=True):
    # Relationship to ChatSession
    session_id: int = Field(default=None, foreign_key="chatsession.id")
    session: ChatSession = Relationship(back_populates="messages")
    
    content: str
    role: str

    # PGVector for message embeddings
    message_embedding: Any = Field(sa_column=Column(Vector(1536)))

    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'onupdate': sqlalchemy.func.now(),
            'server_default': sqlalchemy.func.now()
        },
        nullable=False    
    )

# Collection of User Preferences, Settings, and other related fields to make the Bot more personal feeling.
class ChatBotMemory(rx.Model, table=True):
    # User that the memory is associated with
    userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
    userinfo: Optional["UserInfo"] = Relationship(back_populates="memories")

    # Content of the memory
    memory_key: str # user_name, occupation, family life, etc
    memory_value: str # Value like "Chris", "Programmer", "Dad"

    # Embedding related to this memory,
    memory_embedding: Any = Field(sa_column=Column(Vector(1536)), default=None)

    # Timestamps
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": sqlalchemy.func.now()
        },
        nullable=False 
    )
    updated_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": sqlalchemy.func.now(),
            "server_default": sqlalchemy.func.now()
        },
        nullable=False
    )

class TokenUsage(rx.Model, table=True):
    userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
    session_id: int = Field(default=None, foreign_key="chatsession.id")

    # Token usage fields
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    total_cost: float
    usage_type: str # Chat, Dalle, etc

    # Timestamps
    created_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "server_default": sqlalchemy.func.now()
        },
        nullable=False 
    )
    updated_at: datetime = Field(
        default_factory=utils.timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": sqlalchemy.func.now(),
            "server_default": sqlalchemy.func.now()
        },
        nullable=False
    )