# from typing import Optional, List, Any
# from datetime import datetime
# # Reflex
# import reflex as rx
# from reflex_local_auth.user import LocalUser
# # DB
# import sqlalchemy
# from sqlmodel import Field, Relationship
# from pgvector.sqlalchemy import Vector
# from sqlalchemy import Column
# # utils
# from . import utils

# from ..auth import UserInfo

# class ChatSession(rx.Model, table=True):
#     # Optional relationship to UserInfo
#     userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
#     userinfo: Optional['UserInfo'] = Relationship(back_populates="session")

#     # Relationships
#     messages: List["ChatMessage"] = Relationship(back_populates="session")

#     # Timestamp
#     created_at: datetime = Field(
#         default_factory=utils.timing.get_utc_now,
#         sa_type=sqlalchemy.DateTime(timezone=True),
#         sa_column_kwargs={
#             'server_default': sqlalchemy.func.now()
#         },
#         nullable=False
#     )
#     updated_at: datetime = Field(
#         default_factory=utils.timing.get_utc_now,
#         sa_type=sqlalchemy.DateTime(timezone=True),
#         sa_column_kwargs={
#             'onupdate': sqlalchemy.func.now(),
#             'server_default': sqlalchemy.func.now()
#         },
#         nullable=False
#     )

# class ChatMessage(rx.Model, table=True):
#     # Relationship to ChatSession
#     session_id: int = Field(default=None, foreign_key="chatsession.id")
#     session: ChatSession = Relationship(back_populates="messages")
    
#     content: str
#     role: str

#     # PGVector for message embeddings
#     message_embedding: Any = Field(sa_column=Column(Vector(1536)))

#     created_at: datetime = Field(
#         default_factory=utils.timing.get_utc_now,
#         sa_type=sqlalchemy.DateTime(timezone=True),
#         sa_column_kwargs={
#             'server_default': sqlalchemy.func.now()
#         },
#         nullable=False
#     )
#     updated_at: datetime = Field(
#         default_factory=utils.timing.get_utc_now,
#         sa_type=sqlalchemy.DateTime(timezone=True),
#         sa_column_kwargs={
#             'onupdate': sqlalchemy.func.now(),
#             'server_default': sqlalchemy.func.now()
#         },
#         nullable=False    
#     )

# # Collection of User Preferences, Settings, and other related fields to make the Bot more personal feeling.
# class ChatBotMemory(rx.Model, table=True):
#     # User that the memory is associated with
#     userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
#     userinfo: Optional["UserInfo"] = Relationship(back_populates="memories")

#     # Content of the memory
#     memory_key: str # user_name, occupation, family life, etc
#     memory_value: str # Value like "Chris", "Programmer", "Dad"

#     # Embedding related to this memory,
#     memory_embedding: Any = Field(sa_column=Column(Vector(1536)), default=None)

#     # Timestamps
#     created_at: datetime = Field(
#         default_factory=utils.timing.get_utc_now,
#         sa_type=sqlalchemy.DateTime(timezone=True),
#         sa_column_kwargs={
#             "server_default": sqlalchemy.func.now()
#         },
#         nullable=False 
#     )
#     updated_at: datetime = Field(
#         default_factory=utils.timing.get_utc_now,
#         sa_type=sqlalchemy.DateTime(timezone=True),
#         sa_column_kwargs={
#             "onupdate": sqlalchemy.func.now(),
#             "server_default": sqlalchemy.func.now()
#         },
#         nullable=False
#     )

# class TokenUsage(rx.Model, table=True):
#     userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
#     session_id: int = Field(default=None, foreign_key="chatsession.id")

#     # Token usage fields
#     prompt_tokens: Optional[int] = 0
#     completion_tokens: Optional[int] = 0
#     total_tokens: Optional[int] = 0
#     total_cost: Optional[float] = 0.0
#     usage_type: str # Chat, Dalle, etc

#     # Timestamps
#     created_at: datetime = Field(
#         default_factory=utils.timing.get_utc_now,
#         sa_type=sqlalchemy.DateTime(timezone=True),
#         sa_column_kwargs={
#             "server_default": sqlalchemy.func.now()
#         },
#         nullable=False 
#     )
#     updated_at: datetime = Field(
#         default_factory=utils.timing.get_utc_now,
#         sa_type=sqlalchemy.DateTime(timezone=True),
#         sa_column_kwargs={
#             "onupdate": sqlalchemy.func.now(),
#             "server_default": sqlalchemy.func.now()
#         },
#         nullable=False
#     )