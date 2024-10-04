import reflex as rx
from ..ui.base import base_page

def price_page() -> rx.Component:
    # Welcome Page (Index)
    my_child = rx.vstack(
            rx.heading("Price Page", size="9"),
            rx.text(
                "About our prices"
            ),
            spacing="5",
            justify="center",
            align="center",
            text_align="center",
            min_height="85vh",
        
            id="my-child"
        ),
    
    return base_page(my_child)