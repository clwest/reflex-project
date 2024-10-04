"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .ui.base import base_page
from . import pages, naviagtion



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
app.add_page(index)
app.add_page(pages.about_page, 
             route=naviagtion.routes.ABOUT_US_ROUTE)
app.add_page(pages.price_page,
             route=naviagtion.routes.PRICE_ROUTE)
