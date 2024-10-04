import reflex as rx
from ..ui.base import base_page

def about_page() -> rx.Component:
    # Welcome Page (Index)
    my_child = rx.vstack(
            rx.heading("About Us", size="9"),
            rx.text(
                "About me "
            ),
            spacing="5",
            justify="center",
            align="center",
            text_align="center",
            min_height="85vh",
        
            id="my-child"
        ),
    
    return base_page(my_child)