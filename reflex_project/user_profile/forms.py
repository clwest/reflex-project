import reflex as rx
from .state import UserProfileState

def user_profile_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.heading("User Profile Setup"),
            rx.input(name="name", placeholder="Enter your name", required=True, width="100%"),
            rx.input(name="occupation", placeholder="Your occupation", required=False, width="100%"),
            rx.text_area(name="goals", placeholder="Your goals", required=False, width="100%"),
            rx.select(
                ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"],
                name="learning_style",
                placeholder="What is your learning style?",
                required=False,
                width="100%"
            ),
            rx.text_area(name="hobbies", placeholder="Hobbies", required=False, width="100%"),
            rx.text_area(name="preferred_topics", placeholder="Preferred Topics", required=False, width="100%"),
            rx.button("Submit", type="submit"),
        ),
        on_submit=UserProfileState.handle_initial_setup,
        reset_on_submit=True
    )