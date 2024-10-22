"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import reflex_local_auth

from rxconfig import config
from .ui.base import base_page

from .auth.pages import (
    my_login_page,
    my_register_page,
    my_logout_page,
)

from .auth.state import SessionState

from .articles.detail import article_detail_page
from .articles.list import article_public_list_page, article_public_list_component
from .articles.state import ArticlePublicState

from . import  blog, contact, navigation, pages , chat, user_profile



def index() -> rx.Component:
    # Welcome Page (Index)
    
    return base_page(
        rx.cond(SessionState.is_authenticated,
                pages.dashboard_component(),
                pages.landing_component(),
                )
    )




app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="cyan",
        gray_color="slate",
    )
)

# Home and About Routes
app.add_page(index,
            on_load=ArticlePublicState.load_posts)

# Reflex local auth pages
app.add_page(
    my_login_page,
    route=reflex_local_auth.routes.LOGIN_ROUTE,
    title="Login",
)
app.add_page(
    my_register_page,
    route=reflex_local_auth.routes.REGISTER_ROUTE,
    title="Register",
)
app.add_page(
    my_logout_page,
    route=navigation.routes.LOGOUT_ROUTE,
    title="Logout",
)



# my pages

app.add_page(
    user_profile.user_profile_page,
    route=navigation.routes.USER_PROFILE
)

app.add_page(pages.about_page, 
            route=navigation.routes.ABOUT_US_ROUTE)

app.add_page(
    pages.protected_page, 
    route="/protected/",
    on_load=SessionState.on_load)


app.add_page(
    article_public_list_page,
    route=navigation.routes.ARTICLE_LIST_ROUTE,
    on_load=ArticlePublicState.load_posts
)

app.add_page(
    article_detail_page,
    # href=f"/blog/{state.BlogPostState.blog_post_id}/edit")
    route=f"{navigation.routes.ARTICLE_LIST_ROUTE}/[post_id]",
    on_load=ArticlePublicState.get_post_detail
)





# Blogs and Details


app.add_page(
    blog.blog_post_list_page,
    route=navigation.routes.BLOG_POSTS_ROUTE,
    on_load=blog.BlogPostState.load_posts
)

app.add_page(
    blog.blog_post_add_page,
    route=navigation.routes.BLOG_POSTS_ADD_ROUTE
)

app.add_page(
    blog.blog_post_detail,
    route="/blog/[blog_id]",
    on_load=blog.BlogPostState.get_post_detail
)

app.add_page(
    blog.blog_post_edit_page,
    route="/blog/[blog_id]/edit",
    on_load=blog.BlogPostState.get_post_detail
)



# Contact Routes.
app.add_page(contact.contact_page,
            route=navigation.routes.CONTACT_US_ROUTE)
app.add_page(contact.contact_entries_list_page,
            route=navigation.routes.CONTACT_ENTRIES_ROUTE,
            on_load=contact.ContactState.list_entries,
            )


app.add_page(
            pages.price_page,
            route=navigation.routes.PRICE_ROUTE)

app.add_page(
            chat.chat_page,
            route=navigation.routes.CHATBOT_ROUTE,
            on_load=chat.state.ChatSessionState.create_new_and_redirect
            )

app.add_page(
    chat.chat_page,
    route=f"{navigation.routes.CHATBOT_ROUTE}/[session_id]",
    on_load=chat.state.ChatSessionState.on_detail_load,
)