import reflex as rx
from .state import ChatMessageState, ChatSessionState

def chat_form()-> rx.Component:
    
    return rx.form(
        rx.vstack(
                    rx.text_area(
                        name="message",
                        placeholder="Start a chat",
                        width="100%",
                        required=True,
                    ),
                    rx.hstack(
                        rx.button("Submit", type="submit"),
                        rx.cond(
                            ChatSessionState.user_did_submit,
                            rx.text("Success"),
                            rx.fragment(),
                        ),
                    ),
        ),
        on_submit=ChatSessionState.handle_submit,
        reset_on_submit=True
    )

def initial_setup_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.heading("Let's get to know you!"),

            # Name input
            rx.input(
                name="name",
                placeholder="Enter your name",
                required=True,
            ),

            # Occupation input
            rx.input(
                name="occupation",
                placeholder="What is your current profession?",
                required=False,
            ),

            # Goals input
            rx.text_area(
                name="goals",
                placeholder="What are your goals?",
                required=False,
            ),
            
            # Learning style input (select)
            rx.select(
                name="learning_style",
                options=["Visual", "Auditory", "Reading/Writing", "Kinesthetic"],
                placeholder="What's your learning style?",
                required=False,
            ),

            # Hobbies input
            rx.text_area(
                name="hobbies",
                placeholder="List some of your hobbies or interests",
                required=False,
            ),

            # Preferred topics input
            rx.text_area(
                name="preferred_topics",
                placeholder="Topics you'd like to explore or learn more about.",
                required=False,
            ),

            # Submit button
            rx.button("Submit", type="submit"),
        ),
        on_submit=ChatSessionState.handle_initial_setup, # Handle the form data.
        reset_on_submit=True
    )