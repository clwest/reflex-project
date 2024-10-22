import reflex as rx
from ..ui.base import base_page

from . import forms

def chat_setup_page() -> rx.Component:
    my_form = forms.initial_setup_form()
    my_child = rx.vstack(
        rx.heading("Set up your AI Assistant", size="9"),
        rx.desktop_only(
            rx.box(
                my_form,
                width="35vw",
                id="desktop-box"
            ),
        ),
        rx.tablet_only(
            rx.box(
                my_form,
                width="75vw",
            )
        ),
        rx.mobile_only(
            rx.box(
                my_form,
                width="95vh"
            )
        ),
        spacing="5",
        align="center",
        text_align="center",
        min_height="95vh",
    ),

    return base_page(my_child)


