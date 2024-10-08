import reflex as rx
from .sidebar import sidebar

def base_dashboard_page(child: rx.Component, *args, **kwargs) -> rx.Component:
    # if not isinstance(child, rx.Component):
    #     child = rx.heading("This is for testing child elements")
    return rx.fragment(
        rx.hstack(
            sidebar(),
            rx.box(
            child,        
            rx.logo(),
            padding="1em",
            width="100%",
            id="content-area-em"
            ),
        ),
        # rx.color_mode.button(position="bottom-left"),
        id="my-base-container"
    )