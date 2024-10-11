import asyncio
import sqlmodel
from typing import List
import reflex as rx
from ..models import ChatSession, ChatMessage
from . import ai

class ChatMessageState(rx.Base):
    message: str
    is_bot: bool = False


class ChatSessionState(rx.State):
    chat_session: ChatSession = None
    did_submit: bool = False
    messages: List[ChatMessageState] = []

    @rx.var
    def user_did_submit(self) -> bool:
        return self.did_submit
    
    @rx.var
    def get_session_id(self) -> int:
        try:
            my_session_id = int(self.router.page.params.get("session_id"))
        except:
            my_session_id = None
        return my_session_id

    def create_new_chat_session(self):
        with rx.session() as db_session:
            obj = ChatSession()
            db_session.add(obj)
            db_session.commit() 
            print(obj, obj.id)
            self.chat_session = obj

    def clear_and_start_new(self):
        self.chat_session = None
        self.create_new_chat_session()
        self.messages = []
        yield

    def get_session_from_db(self):
        return 
        """
        Pick up from get_session_from_db.
        """
    def on_detail_load(self):
        session_id = self.get_session_id
        if isinstance(session_id, int):
            self.get_session_from_db()


    def on_load(self):
        print("running on load")
        if self.chat_session is None:
            self.create_new_chat_session()
    
    def insert_message_to_db(self, content, role='unknown'):
        print("Inserting chat session to db")
        if self.chat_session is None:
            return
        if not isinstance(self.chat_session, ChatSession):
            return
        with rx.session() as db_session:
            data = {
                "session_id": self.chat_session.id,
                "content": content,
                "role": role
            }
            obj = ChatMessage(**data)
            db_session.add(obj)
            db_session.commit() 


    def append_message_to_ui(self, message, is_bot:bool=False):
        if self.chat_session is not None:
            print(self.chat_session.id)
        with rx.session() as session:
            session.add(
                ChatSession(
                    title=message
                )
            )
            session.commit()
        self.messages.append(
            ChatMessageState(
                message=message,
                is_bot=is_bot
            )
        )
    
    def get_gpt_messages(self):
        gpt_messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant with a great deal of general knowledge. Respond in markdown"
            }
        ]
        for chat_message in self.messages:
            role = "user"
            if chat_message.is_bot:
                role = "system"
            gpt_messages.append({
                "role": role,
                "content": chat_message.message
            })
        return gpt_messages 

    async def handle_submit(self, form_data:dict):
        print("Form Data is", form_data)
        user_message = form_data.get("message")
        if user_message:
            self.did_submit = True
            self.append_message_to_ui(user_message, is_bot=False)
            self.insert_message_to_db(user_message, "user")
            yield
            gpt_messages = self.get_gpt_messages()
            print(gpt_messages)
            bot_response = ai.get_llm_response(gpt_messages)
            # await asyncio.sleep(2)
            self.did_submit = False
            self.append_message_to_ui(bot_response, is_bot=True)
            self.insert_message_to_db(bot_response, role="system")
            yield

