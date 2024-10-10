import reflex as rx
import reflex_local_auth
from ..ui.base import base_page
from .. import navigation
from . import state
from ..models import BlogPostModel

def blog_post_detail_link(child: rx.Component, post: BlogPostModel):
    
    if post is None:
        return rx.fragment(child) 
    post_id = post.id
    if post_id is None:
        return rx.fragment(child)
    
    root_path = navigation.routes.BLOG_POSTS_ROUTE
    post_detail_url = f"{root_path}/{post_id}"
    return rx.link(
        child,
        rx.heading("Written By: ", post.userinfo.email),
        href=post_detail_url
    )

def blog_post_list_item(post: BlogPostModel):
    return rx.box(
        blog_post_detail_link(
        rx.heading(post.title),
        post
        ),

        padding="2em"
    )

@rx.page()
@reflex_local_auth.require_login
def blog_post_list_page() -> rx.Component:   
    return base_page(
        rx.vstack(
            rx.heading("Unpublished Blogs", size="5"),
            rx.link(
                rx.button("New Post"),
                href=navigation.routes.BLOG_POSTS_ADD_ROUTE
            ),
            # rx.foreach(["abc", "def", "hij"], foreach_callback ),
            rx.foreach(state.BlogPostState.posts,
                    blog_post_list_item),
            spacing="5",
            align="center",
            min_height="85vh",
    ))

