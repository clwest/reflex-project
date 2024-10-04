import reflex as rx
from .nav import navbar

def base_page(child: rx.Component, *args, **kwargs) -> rx.Component:
    
    return rx.fragment(
        navbar(),
        rx.box(
        child,        
        # bg=rx.color("accent", 3),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
        id="content-area-em"
        ),
        rx.color_mode.button(position="bottom-left"),
        rx.logo(),
        id="my-base-container"
       
    )