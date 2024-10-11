import reflex as rx

from .. import navigation
from ..articles.list import article_public_list_component

def landing_component() -> rx.Component:
    return rx.vstack(
        rx.heading("Welcome to Donkey Betz", size="9", color_scheme="cyan"),
        rx.text("Recent Articles", size="9", color_scheme="cyan"),
        article_public_list_component(columns=1, limit=1),
        spacing="5",
        justify="center",
        align="center",
        min_height="85vh",
        id="my-child",
    )