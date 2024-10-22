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
# from ..chat import ChatBotMemory, ChatMessage, ChatSession
# from ..blog import BlogPostModel
# from ..contact import ContactEntryModel

# class UserInfo(rx.Model, table=True):
#     email: str
#     user_id: int = Field(foreign_key='localuser.id')
#     user: LocalUser | None = Relationship() # LocalUser instance based off of user_id in FK

#     # Relationships
#     posts: List["BlogPostModel"] = Relationship(
#         back_populates="userinfo"
#     )
#     contact_entries: List["ContactEntryModel"] = Relationship(
#         back_populates="userinfo"
#     )
#     session: List["ChatSession"]  = Relationship(back_populates="userinfo") # User to Session
    
#     memories: List["ChatBotMemory"] = Relationship(back_populates="userinfo") # User to ChatBotMemory


#     # created_at
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



