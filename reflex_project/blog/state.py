import reflex as rx
from typing import List, Optional
from sqlmodel import select

from .. import naviagtion
from .model import BlogPostModel

BLOG_POSTS_ROUTE = naviagtion.routes.BLOG_POSTS_ROUTE
if BLOG_POSTS_ROUTE.endswith("/"):
    BLOG_POSTS_ROUTE = BLOG_POSTS_ROUTE[:-1] 


class BlogPostState(rx.State):
    posts: List['BlogPostModel'] = []
    post: Optional['BlogPostModel'] = None
    post_content: str = ""
    
    @rx.var
    def blog_post_id(self):
        return self.router.page.params.get("blog_id", "")
    
    @rx.var
    def blog_post_url(self):
        if not self.post:
            return f"{BLOG_POSTS_ROUTE}"
        return f"{BLOG_POSTS_ROUTE}/{self.post.id}" 

    @rx.var
    def blog_post_edit_url(self):
        if not self.post:
            return f"{BLOG_POSTS_ROUTE}"
        return f"{BLOG_POSTS_ROUTE}/{self.post.id}/edit"     
    
    
    def get_post_detail(self):
        with rx.session() as session:
            if self.blog_post_id == "":
                self.post = None
                return
            
            result = session.exec(
                select(BlogPostModel).where(
                    BlogPostModel.id == self.blog_post_id
                )
            ).one_or_none()
            self.post = result
            if result is None:
                self.post_content = ""
                return
            self.post_content = self.post.content
    
    def load_posts(self):
        with rx.session() as session:
            result = session.exec(
                select(BlogPostModel)
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
    
      
    # def get_post(self):
    #     with rx.session() as session:
    #         result = session.exec(
    #             select(BlogPostModel)
    #         )
    #         self.posts = result


# inheirets from PostState to add form_data to add_post
class BlogAddFormState(BlogPostState):
    form_data: dict = {}
    
    def handle_submit(self, form_data):
        self.form_data = form_data
        self.add_post(form_data)
        return self.to_blog_post(edit_page=True)
        
class BlogEditFormState(BlogPostState):
    form_data: dict = {}
    # post_content: str = ""
    
    def handle_submit(self, form_data):
        self.form_data = form_data
        post_id = form_data.pop('post_id')
        updated_data = {**form_data}
        print(post_id, updated_data)
        self.edit_post(post_id, updated_data)   
        # self.add_post(form_data)
        return self.to_blog_post()