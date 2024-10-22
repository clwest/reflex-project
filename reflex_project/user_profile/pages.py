import reflex as rx
from ..ui.base import base_page
from .forms import user_profile_form, prompt_form
from .state import UserProfileState


def prompt_display_box(prompt) -> rx.Component:
    return rx.box(
        rx.text(f"{prompt.prompt_text} (Category: {prompt.prompt_category})"),
        margin="1em",
    )

# Component to handle the profile settings page
def user_profile_settings_page() -> rx.Component:
    return rx.vstack(
        rx.heading("User Profile Settings", size="5"),
        rx.box(
            rx.heading("Create AI Prompts", size="5"),
            prompt_form(),
            rx.foreach(UserProfileState.get_user_prompts, prompt_display_box), # Same as foreach in chat
        ),
        spacing="2em",
        width="100%",
    )

# The main user profile page
def user_profile_page() -> rx.Component:
    return base_page(
        rx.vstack(
            user_profile_settings_page(),
            user_profile_form(),
            align="center",
            spacing="2em",
        )
    )