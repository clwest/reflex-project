import reflex as rx

from reflex_local_auth.pages.login import LoginState, login_form
from reflex_local_auth.pages.registration import RegistrationState, register_form

from ..ui.base import base_page
from .forms import my_register_form
from .state import SessionState
from .. import navigation

def my_login_page()->rx.Component:
    return base_page(
        rx.center(
            rx.cond(
                LoginState.is_hydrated,  # type: ignore
                rx.card(login_form()),
            ),
            min_height="85vh",
            # padding_top=PADDING_TOP,
        ),
    )

def my_register_page()->rx.Component:
    return base_page(
        rx.center(
            rx.cond(
                RegistrationState.success,
                rx.vstack(
                    rx.text("Registration successful!"),
                ),
                rx.card(my_register_form()),
            ),
        min_height="85vh",
        # padding_top=PADDING_TOP,
        )
    )

def my_logout_page() -> rx.Component:
    # Welcome Page (Index)
    my_child = rx.vstack(
            rx.heading("You are about to log out.", size="7"),
            rx.link(
            rx.button("No", color_scheme="crimson"),
            href=navigation.routes.HOME_ROUTE,
            ),
            rx.button("Yes, logout", on_click=SessionState.perform_logout, color_scheme="amber"),
            spacing="5",
            justify="center",
            align="center",
            text_align="center",
            min_height="85vh",
        
            id="my-child"
        ),
    
    return base_page(my_child)
