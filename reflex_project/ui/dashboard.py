import reflex as rx
from .sidebar import sidebar

def base_dashboard_page(child: rx.Component, *args, **kwargs) -> rx.Component:

    return rx.fragment(
        rx.hstack(
            sidebar(),
            rx.box(
            child,        
            padding="1em",
            width="100%",
            id="content-area-el"
            ),
        ),
        # rx.color_mode.button(position="bottom-left"),
        # id="my-base-container"
    )