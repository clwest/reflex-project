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

# class BlogPostModel(rx.Model, table=True):
#     # User
#     userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
#     userinfo: Optional['UserInfo'] = Relationship(back_populates="posts")
    
#     title: str
#     content: str
    
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
    
#     is_published: bool = False
#     publish_date: datetime = Field(
#         default=None,
#         sa_type=sqlalchemy.DateTime(timezone=True),
#         sa_column_kwargs={},
#         nullable=True
#     )
