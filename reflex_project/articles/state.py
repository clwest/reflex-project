from datetime import datetime
from typing import Optional, List
import reflex as rx 

import sqlalchemy
from sqlmodel import select

from .. import navigation
from ..auth.state import SessionState
from ..models import BlogPostModel, UserInfo

ARTICLE_LIST_ROUTE = navigation.routes.ARTICLE_LIST_ROUTE
if ARTICLE_LIST_ROUTE.endswith("/"):
    ARTICLE_LIST_ROUTE = ARTICLE_LIST_ROUTE[:-1]

class ArticlePublicState(SessionState):
    posts: List['BlogPostModel'] = []
    post: Optional['BlogPostModel'] = None
    post_content: str = ""
    # post_publish_active: bool = False
    is_published_active: bool = False
    limit: int = 20

    @rx.var
    def get_post_id(self):
        return self.router.page.params.get("post_id", "")

    @rx.var
    def post_url(self):
        if not self.post:
            return f"{ARTICLE_LIST_ROUTE}"
        return f"{ARTICLE_LIST_ROUTE}/{self.post.id}"

    def get_post_detail(self):
        lookups = (
            (BlogPostModel.is_published == True) &
            (BlogPostModel.publish_date < datetime.now()) &
            (BlogPostModel.id == self.get_post_id)
        )
        with rx.session() as session:
            if self.get_post_id == "":
                self.post = None
                self.post_content = ""
                self.is_published_active: bool = False
                return
            sql_statement = select(BlogPostModel).options(
                sqlalchemy.orm.joinedload(BlogPostModel.userinfo).joinedload(UserInfo.user)
            ).where(lookups)
            result = session.exec(sql_statement).one_or_none()
            self.post = result
            if result is None:
                self.post_content = ""
                return
            self.post_content = self.post.content
            self.is_published_active = self.post.is_published
        # return

    def set_limit_and_reload(self, new_limit: int=5):
        self.limit = new_limit
        self.load_posts()
        yield

    def load_posts(self, *args, **kwargs):
        lookup_args = ( 
            (BlogPostModel.is_published == True) &
            (BlogPostModel.publish_date < datetime.now())
        )
        with rx.session() as session:
            result = session.exec(
                select(BlogPostModel).options(
                    sqlalchemy.orm.joinedload(BlogPostModel.userinfo)
                ).where(lookup_args).limit(self.limit)
            ).all()
            self.posts = result
    
    def to_post(self):
        if not self.post:
            return rx.redirect(ARTICLE_LIST_ROUTE)
        return rx.redirect(f"{self.post_url}")