import reflex as rx
from .state import ChatMessageState, ChatSessionState
from typing import List, Optional



def chat_form(suggested_prompts: List[str] = [])-> rx.Component:
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
                    rx.cond(
                        suggested_prompts,                        
                        rx.box(
                            rx.heading("Suggested Prompts:", color_scheme="cyan"),
                            rx.foreach(
                                suggested_prompts,
                                lambda prompt: rx.button(
                                    prompt, 
                                    on_click=lambda: ChatSessionState.handle_suggested_prompts(prompt),
                                    style={"margin": "0.5em"}
                                )
                            ),
                            spacing="0.5em",
                        ),
                        rx.fragment()
                    ),
        ),
        on_submit=ChatSessionState.handle_submit,
        reset_on_submit=True
    )


