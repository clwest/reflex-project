import asyncio
import sqlmodel
from typing import List, Optional
import reflex as rx
from ..models import ChatSession, ChatMessage
from . import ai

class ChatMessageState(rx.Base):
    message: str
    is_bot: bool = False


class ChatSessionState(rx.State):
    chat_session: ChatSession = None
    not_found: Optional[bool] = None
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
            return obj


    def clear_ui(self):
        self.chat_session = None
        self.not_found = None
        self.did_submit = False
        self.messages = []
    
    def create_new_and_redirect(self):
        self.clear_ui()
        new_chat_session = self.create_new_chat_session()
        return rx.redirect(f"/chat/{new_chat_session.id}")
    

    def clear_and_start_new(self):
        self.clear_ui()
        self.create_new_chat_session()
        yield

    def get_session_from_db(self, session_id=None):
        if session_id is None:
            session_id = self.get_session_id
        with rx.session() as db_session:
            sql_statement = sqlmodel.select(
                ChatSession
            ).where(
                ChatSession.id == session_id
            )
            result = db_session.exec(sql_statement).one_or_none()
            if result is None:
                self.not_found = True
            else:
                self.not_found = False
            self.chat_session = result
            messages = result.messages
            for msg_obj in messages:
                msg_text = msg_obj.content
                is_bot = False if msg_obj.role == "user" else True
                self.append_message_to_ui(msg_text, is_bot=True)


    def on_detail_load(self):
        session_id = self.get_session_id
        reload_detail = False
        if not self.chat_session:
            reload_detail = True
        
        else:
            """Has a session"""
            if self.chat_session.id != session_id:
                reload_detail = True
        
        if reload_detail:
            self.clear_ui()
            if isinstance(session_id, int):
                self.get_session_from_db()


    def on_load(self):
        print("running on load")
        self.clear_ui()
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

