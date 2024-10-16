import asyncio
import sqlmodel
from typing import List, Optional
import reflex as rx
from ..auth.state import SessionState
from ..models import ChatSession, ChatMessage, UserInfo
from . import ai

class ChatMessageState(rx.Base):
    message: str
    is_bot: bool = False

""" 
TODO: Start with figuring out why sessions are being created, they seem to be coming from the AI for some reason.
    then move into creating a search for embeddings. After that either add in the loaders or images.
"""
class ChatSessionState(SessionState):
    chat_session: ChatSession = None
    not_found: Optional[bool] = None
    did_submit: bool = False
    messages: List[ChatMessageState] = []

    @rx.var
    def my_userinfo_id(self) -> int:
        return self.get_authenticated_user_id

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


    def create_new_chat_session(self, force_new=False):
        print(f"Creating new chat session for user {self.my_userinfo_id}")

        # If forcing a new session, skip the check for an existing session
        if not force_new:
            if self.chat_session:
                print(f"Using existing chat session: {self.chat_session.id}")
                return self.chat_session
            
            with rx.session() as db_session:
                # Fetch the most recent session for the user
                existing_session = db_session.exec(
                    sqlmodel.select(ChatSession)
                    .where(ChatSession.userinfo_id == self.my_userinfo_id)
                    .order_by(ChatSession.created_at.desc())  # Most recent first
                    .limit(1)
                ).one_or_none()

                if existing_session:
                    print(f"Found existing session: {existing_session.id}")
                    self.chat_session = existing_session
                    return existing_session
        
        if not self.my_userinfo_id:
            print("No userinfo_id provided! Aborting session creation.")
            return None # Ensure we don't create a session with NULL userinfo_id

        # If no session exists (or if force_new=True), create a new one
        print(f"Creating new session for user: {self.my_userinfo_id}")
        with rx.session() as db_session:
            obj = ChatSession(userinfo_id=self.my_userinfo_id)
            db_session.add(obj)
            db_session.commit()
            print(f"New session created with ID: {obj.id}")
            self.chat_session = obj
            return obj

    def clear_ui(self, reset_session=False):
        print(f"Clearing UI - Session: {self.chat_session.id if self.chat_session else 'None'}")
        # Only reset session if explicitly asked to
        if reset_session:
            self.chat_session = None
        self.not_found = None
        self.did_submit = False
        self.messages = []
    
    def create_new_and_redirect(self):

        self.clear_ui(reset_session=True) # Explicitly clear the session
        new_chat_session = self.create_new_chat_session(force_new=True)
        print(f"Creating new session: {new_chat_session.id}")
        return rx.redirect(f"/chat/{new_chat_session.id}")

    def clear_and_start_new(self):
        self.clear_ui()
        new_chat_session = self.create_new_chat_session()
        yield rx.redirect(f"/chat/{new_chat_session.id}")

    def get_session_from_db(self, session_id=None):
        if session_id is None:
            session_id = self.get_session_id
        with rx.session() as db_session:
            sql_statement = sqlmodel.select(
                ChatSession
            ).where(
                ChatSession.id == session_id,
                ChatSession.userinfo_id == self.my_userinfo_id
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
        # Clear UI to start fresh
        self.clear_ui()

        # Check if there's already a chat session for current user
        if not self.chat_session:
            print("No chat session found, creating a new one.")
            self.create_new_chat_session()
        else:
            print(f"Using existing session: {self.chat_session.id}")
    
    def insert_message_to_db(self, content, role='unknown'):
        print("Inserting chat session to db")

        if self.chat_session is None:
            print("Invalid session! Aborting message insertion.")
            return
        if not isinstance(self.chat_session, ChatSession):
            return # Ensure the session is valid
        
        # Create the embedding for the message
        embedding = ai.create_embedding(content)


        with rx.session() as db_session:
            data = {
                "session_id": self.chat_session.id,
                "content": content,
                "role": role,
                "message_embedding": embedding,
                "userinfo_id": self.get_authenticated_userinfo_id
            }
            obj = ChatMessage(**data)
            db_session.add(obj)
            db_session.commit() 
        print(f"Message inserted to session: {self.chat_session.id}")


    def append_message_to_ui(self, message, is_bot:bool=False):
        if self.chat_session is not None:
            print(f"Appending message to UI for session: {self.chat_session.id}")
        
        if not self.chat_session: # Ensure there's no session creation happening
            print("No active session! Aborting message append.")
            return 
        

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
        # print("Form Data is", form_data)
        user_message = form_data.get("message")
        if user_message:
            self.did_submit = True
            
            # Ensure a session exists before processing the message
            if not self.chat_session:
                print("No chat session available, creating new one.")
                self.create_new_chat_session()
            
            # Proceed with appending the user's message
            self.append_message_to_ui(user_message, is_bot=False)
            print(f"Before user message insert - Session: {self.chat_session.id}, User: {self.my_userinfo_id}")
            self.insert_message_to_db(user_message, "user")
            yield

            gpt_messages = self.get_gpt_messages()
            bot_response = ai.get_llm_response(gpt_messages)

            # Log the session status after the AI response
            print(f"Before AI response insert - Session: {self.chat_session.id}, User: {self.my_userinfo_id}")
            
            self.did_submit = False

            self.append_message_to_ui(bot_response, is_bot=True)
            self.insert_message_to_db(bot_response, role="system")
            
            print(f"After AI insert to DB response insert - Session: {self.chat_session.id}, User: {self.my_userinfo_id}")
            yield

