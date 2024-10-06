"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .ui.base import base_page
from . import blog, contact, naviagtion, pages 



class State(rx.State):
    """The app state."""
    label = "Welcome to Donkey Betz!"
    
    def handle_input_change(self, val):
        self.label = val

    def did_click(self):
        print("Hello World")
        return rx.redirect(naviagtion.routes.ABOUT_US_ROUTE)




def index() -> rx.Component:
    # Welcome Page (Index)
    my_child = rx.vstack(
            rx.heading(State.label, size="9"),
            rx.text(
                "Under Development ",
                size="7",
            ),
            rx.link(
                rx.button("About Us", on_click=rx.redirect(naviagtion.routes.ABOUT_US_ROUTE)),
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
app.add_page(pages.about_page, 
             route=naviagtion.routes.ABOUT_US_ROUTE)
app.add_page(pages.price_page,
             route=naviagtion.routes.PRICE_ROUTE)


# Blogs and Details
app.add_page(
    blog.blog_post_list_page,
    route=naviagtion.routes.BLOG_POSTS_ROUTE,
    on_load=blog.BlogPostState.load_posts
)

app.add_page(
    blog.blog_post_add_page,
    route=naviagtion.routes.BLOG_POSTS_ADD_ROUTE,
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


# Contact Routes.
app.add_page(contact.contact_page,
             route=naviagtion.routes.CONTACT_US_ROUTE)
app.add_page(contact.contact_entries_list_page,
             route=naviagtion.routes.CONTACT_ENTRIES_ROUTE,
             on_load=contact.ContactState.list_entries,
             )
