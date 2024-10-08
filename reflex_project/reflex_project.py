"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import reflex_local_auth
from rxconfig import config
from .ui.base import base_page
from . import  blog, contact, navigation, pages 

from .auth.pages import (
    my_login_page,
    my_register_page,
    my_logout_page,
)

from .auth.state import SessionState

class State(rx.State):
    """The app state."""
    label = "Welcome to Donkey Betz!"
    
    def handle_input_change(self, val):
        self.label = val

    def did_click(self):
        print("Hello World")
        return rx.redirect(navigation.routes.ABOUT_US_ROUTE)




def index() -> rx.Component:
    # Welcome Page (Index)
    my_child = rx.vstack(
            rx.heading(State.label, size="9"),
            rx.text(
                "Under Development ",
                size="7",
            ),
            rx.link(
                rx.button("About Us", on_click=rx.redirect(navigation.routes.ABOUT_US_ROUTE)),
            ),
            spacing="5",
            justify="center",
            align="center",
            text_align="center",
            min_height="85vh",
        
            id="my-child"
        ),
    
    return base_page(my_child)




app = rx.App()

# Home and About Routes
app.add_page(index)

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
app.add_page(pages.about_page, 
            route=navigation.routes.ABOUT_US_ROUTE)

app.add_page(
    pages.protected_page, 
    route="/protected",
    on_load=SessionState.on_load)

app.add_page(pages.price_page,
            route=navigation.routes.PRICE_ROUTE)


# Blogs and Details
app.add_page(
    blog.blog_post_list_page,
    route=navigation.routes.BLOG_POSTS_ROUTE,
    on_load=blog.BlogPostState.load_posts
)

app.add_page(
    blog.blog_post_add_page,
    route=navigation.routes.BLOG_POSTS_ADD_ROUTE,
    on_load=blog.BlogPostState.load_posts
)

app.add_page(
    blog.blog_post_detail,
    route="/blog/[blog_id]",
    on_load=blog.BlogPostState.get_post_detail
)

app.add_page(
    blog.blog_post_edit_page,
    route="/blog/[blog_id]/edit",
    # on_load=blog.BlogPostState.get_post_detail
)

# app.add_page(
#     "/published",
#     route=navigation.routes.BLOG_POSTS_ROUTE    ,
#     # on_load=blog.BlogPostState.get_post_detail
# )

# Contact Routes.
app.add_page(contact.contact_page,
            route=navigation.routes.CONTACT_US_ROUTE)
app.add_page(contact.contact_entries_list_page,
            route=navigation.routes.CONTACT_ENTRIES_ROUTE,
            on_load=contact.ContactState.list_entries,
            )
