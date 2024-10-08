import reflex as rx
from ..ui.base import base_page
import reflex_local_auth

@reflex_local_auth.require_login
def protected_page() -> rx.Component:
    # Welcome Page (Index)
    my_child = rx.vstack(
            rx.heading("Protected Page", size="9"),
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