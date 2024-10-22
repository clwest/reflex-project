import reflex as rx

from ..ui.base import base_page
from .state import ChatSessionState, ChatMessageState
from .forms import chat_form



message_style = dict(display="inline-block", padding="1em", border_radius="8px", max_width=["30em", "30em", "50em", "50em", "50em", "50em"])

def message_box(chat_message: ChatMessageState) -> rx.Component:
    return rx.box(
        rx.box(
            rx.markdown(
                chat_message.message,
                background_color=rx.cond(chat_message.is_bot, rx.color("crimson", 12), rx.color('green', 12)),
                color=rx.cond(chat_message.is_bot, rx.color("amber", 12), rx.color('crimson', 12)),
                **message_style,
            ),
            text_align=rx.cond(chat_message.is_bot, "left", "right"),
            margin_top="1em",
        ),
        width="100%",
    )




def chat_page() -> rx.Component:
    from ..ui.base import base_page
    my_child = rx.vstack(
        rx.heading("ChatBot", size="9", color_scheme="cyan"),
        rx.cond(ChatSessionState.not_found, "Not Found", "Found"),
        rx.hstack(
        rx.text("GPT-4o-Mini"),
        rx.button("New Chat", on_click=ChatSessionState.create_new_and_redirect)
        ),
        rx.box(
            rx.foreach(ChatSessionState.messages, message_box),
            width="100%",
        ),

        chat_form(),
            # rx.cond(
            # ChatSessionState.token_info,
            # rx.box(
            #         rx.text(f"Total Tokens: {ChatSessionState.token_info['total_tokens']}"),
            #         rx.text(f"Prompt Tokens: {ChatSessionState.token_info['prompt_tokens']}"),
            #         rx.text(f"Completion Tokens: {ChatSessionState.token_info['completion_tokens']}"),
            #         rx.text(f"Total Cost (USD): ${ChatSessionState.token_info['total_cost']:.6f}"),
            #         width="100%"
            #     ),
            # rx.fragment(),
            # ),
        margin="3rem",
        spacing="5",
        justify="center",
        align="center",
        text_align="center",
        min_height="85vh",

        id="chat-bot"
    )
    return base_page(my_child)