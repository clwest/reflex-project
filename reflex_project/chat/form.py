import reflex as rx

from .state import ChatSessionState

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