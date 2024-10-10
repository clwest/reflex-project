from datetime import datetime
import reflex as rx
from typing import List, Optional

import sqlalchemy
from sqlmodel import select

from .. import navigation
from ..auth.state import SessionState
from ..models import BlogPostModel, UserInfo

BLOG_POSTS_ROUTE = navigation.routes.BLOG_POSTS_ROUTE
if BLOG_POSTS_ROUTE.endswith("/"):
    BLOG_POSTS_ROUTE = BLOG_POSTS_ROUTE[:-1] 


class BlogPostState(SessionState):
    posts: List['BlogPostModel'] = []
    post: Optional['BlogPostModel'] = None
    post_content: str = ""
    is_published_active: bool = False
    
    @rx.var
    def blog_post_id(self):
        return self.router.page.params.get("blog_id", "")
    
    @rx.var
    def blog_post_url(self):
        if not self.post:
            return f"{BLOG_POSTS_ROUTE}"
        return f"{BLOG_POSTS_ROUTE}/{self.post.id}" 

    # @rx.var
    # def blog_post_edit_url(self):
    #     if not self.post:
    #         return f"{BLOG_POSTS_ROUTE}"
    #     return f"{BLOG_POSTS_ROUTE}/{self.post.id}/edit"     
    @rx.var
    def blog_post_edit_url(self):
        if not self.post:
            return f"{BLOG_POSTS_ROUTE}"
        return f"{BLOG_POSTS_ROUTE}/{self.post.id}/edit"
    
    
    def get_post_detail(self):
        lookups = (
            (BlogPostModel.userinfo_id == self.my_userinfo_id) &
            (BlogPostModel.id == self.blog_post_id)
        )
        with rx.session() as session:
            if self.blog_post_id == "":
                self.post = None
                return
            
            sql_statement = select(BlogPostModel).options(
                sqlalchemy.orm.joinedload(BlogPostModel.userinfo).joinedload(UserInfo.user)
            ).where(
                    lookups
                )
            result = session.exec(
                sql_statement
            ).one_or_none()
            # if result.userinfo: # Db lookup
            #     print("I'm at blog/state.py")
            #     result.userinfo.user
            self.post = result
            if result is None:
                self.post_content = ""
                return
            self.post_content = self.post.content
            self.is_published_active = self.post.is_published
    
    def load_posts(self, *args, **kwargs):
        lookup_args = ()
        # if published_only:
        #     lookup_args = (
        #             (BlogPostModel.is_published == True) &
        #             (BlogPostModel.publish_date < datetime.now())
        #     )
        with rx.session() as session:
            result = session.exec(
                select(BlogPostModel).options(
                    sqlalchemy.orm.joinedload(BlogPostModel.userinfo)
                ).where(
                    BlogPostModel.userinfo_id == self.my_userinfo_id
                )
            ).all()
            self.posts = result
        # return
    
    def add_post(self, form_data:dict):
        with rx.session() as session:
            post = BlogPostModel(**form_data)
            # print("adding", post)
            session.add(post)
            session.commit()
            session.refresh(post) # should have post_id
            # print("Added", post)
            self.post = post
        # return

    def edit_post(self, post_id: id, updated_data:dict):
        with rx.session() as session:
            post = session.exec(
                select(BlogPostModel).where(
                    BlogPostModel.id == post_id
                )
            ).one_or_none()
            if post is None:
                return
            for key, value in updated_data.items():
                setattr(post, key, value)
            session.add(post)
            session.commit()
            session.refresh(post)
            self.post = post
        # return
        
    def to_blog_post(self, edit_page=False):
        if not self.post:
            return rx.redirect(BLOG_POSTS_ROUTE)
        if edit_page:
            return rx.redirect(f"{self.blog_post_edit_url}")
        return rx.redirect(f"{self.blog_post_url}")
    



# inherits from PostState to add form_data to add_post
class BlogAddFormState(BlogPostState):
    form_data: dict = {}
    
    def handle_submit(self, form_data):
        data = form_data.copy()
        if self.my_userinfo_id is not None:
            data['userinfo_id'] = self.my_userinfo_id
        self.form_data = data 
        self.add_post(data)
        return self.to_blog_post(edit_page=True)
        
class BlogEditFormState(BlogPostState):
    form_data: dict = {}
    # post_content: str = ""

    @rx.var
    def publish_display_date(self) -> str:
        if not self.post:
            return datetime.now().strftime("%Y-%m-%d")
        if not self.post.publish_date:
            return datetime.now().strftime("%Y-%m-%d")
        return self.post.publish_date.strftime("%Y-%m-%d")
    
    
    @rx.var
    def publish_display_time(self) -> str:
        if not self.post:
            return datetime.now().strftime("%H:%M:%S")
        if not self.post.publish_date:
            return datetime.now().strftime("%H:%M:%S")
        return self.post.publish_date.strftime("%H:%M:%S")  
    

    def handle_submit(self, form_data):
        self.form_data = form_data
        post_id = form_data.pop('post_id')

        publish_date = None
        if "publish_date" in form_data:
            publish_date = form_data.pop('publish_date')

        publish_time = None
        if "publish_time" in form_data:
            publish_time = form_data.pop('publish_time')


        # print("Printing date and time")
        # print(publish_date, publish_time)

        publish_input_string = f"{publish_date} {publish_time}"

        try:
            final_publish_date = datetime.strptime(publish_input_string, '%Y-%m-%d %H:%M:%S')
        except:
            final_publish_date = None
        is_published = False

        if 'is_published'in form_data:
            is_published = form_data.pop('is_published') == "on"
        updated_data = {**form_data}
        updated_data['is_published'] = is_published
        updated_data['publish_date'] = final_publish_date

        self.edit_post(post_id, updated_data)   
        # self.add_post(form_data)
        return self.to_blog_post()