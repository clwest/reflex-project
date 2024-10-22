import reflex as rx
from ..ui.base import base_page
from .forms import user_profile_form

def user_profile_page() -> rx.Component:
    return base_page(
        rx.vstack(
            rx.heading("Set up your AI Assistant"),
            user_profile_form(),
            align="center",
            spacing="2em",
        )
    )