from datetime import datetime
import reflex as rx
import sqlalchemy
from sqlmodel import Field
from .. import utils


class BlogPostModel(rx.Model, table=True):
    # User
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
    #Todo Need to add migrations and migrate before starting over!
    is_published: bool = False
    # published_at
    # published_time
    
    