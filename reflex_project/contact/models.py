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
# from ..models import UserInfo

# class ContactEntryModel(rx.Model, table=True):
#     user_id: int | None = None
#     userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
#     userinfo: Optional['UserInfo'] = Relationship(back_populates="contact_entries")
#     first_name: str
#     last_name: str | None = None
#     email: str = Field(nullable=True)
#     message: str
#     created_at: datetime = Field(
#         default_factory=utils.timing.get_utc_now,
#         sa_type=sqlalchemy.DateTime(timezone=True),
#         sa_column_kwargs={
#             'server_default': sqlalchemy.func.now()
#         },
#         nullable=False
#     )