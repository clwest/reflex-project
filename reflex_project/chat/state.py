import asyncio
import sqlmodel
from typing import List, Optional
import reflex as rx
from ..auth.state import SessionState
from ..models import ChatSession, ChatMessage, ChatBotMemory, TokenUsage
from ..user_profile.state import UserProfileState
from . import ai
from ..utils.token_counter import TokenCounterFactory


class ChatMessageState(rx.Base):
    message: str
    is_bot: bool = False


class ChatSessionState(SessionState):
    token_info: dict = {}
    chat_session: ChatSession = None
    not_found: Optional[bool] = None
    did_submit: bool = False
    messages: List[ChatMessageState] = []
    suggested_prompts: List[str] = []

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
        print(f"clear_ui method called to Clear UI - Session: {self.chat_session.id if self.chat_session else 'None'}")
        # Only reset session if explicitly asked to
        if reset_session:
            self.chat_session = None
        self.not_found = None
        self.did_submit = False
        self.messages = []
    
    def create_new_and_redirect(self):
        # Call on_load here to trigger the prompt suggestions and memory loading
        self.on_load() # This will ensure prompts are set when creating a new chat
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
        # Ensure the on_load method runs here
        self.on_load() # Load memory and prompts
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

    def load_user_memory(self):
        with rx.session() as db_session:
            memories = db_session.exec(
                sqlmodel.select(ChatBotMemory).where(
                    ChatBotMemory.userinfo_id == self.my_userinfo_id
                )
            ).all()

            user_memory = {memory.memory_key: memory.memory_value for memory in memories}
            print(f"Loaded memory from load_user_memory method {self.my_userinfo_id}: {user_memory}")
            return user_memory

    def on_load(self):
        print("running on load")
        # Clear UI to start fresh
        self.clear_ui()

        # Load user memory at the start
        user_memory = self.load_user_memory()
        print(f"User memory from on_load method: {user_memory}")

        # Suggest prompts
        self.suggested_prompts = UserProfileState.suggest_prompts(user_memory)
        print(f"Suggested prompts in ChatSessionState: {self.suggested_prompts}")
        
        if self.suggested_prompts:
            prompt_message = "Here are some suggestions to get started:\n"
            for idx, prompt in enumerate(self.suggested_prompts):
                prompt_message += f"{idx + 1}. {prompt}\n"
            self.append_message_to_ui(prompt_message, is_bot=True)

        # Continue with chat setup....
        if not self.chat_session:
            print("No chat session found, creating a new one.")
            self.create_new_chat_session()
        else:
            print(f"Using existing session: {self.chat_session.id}")
        
        # if user_memory:
        #     memory_message = f"Recalling information: {user_memory}"
        #     self.append_message_to_ui(memory_message, is_bot=True)

    # When bot learns something about the user we store that information
    def store_user_memory(self, key: str, value: str):
        with rx.session() as db_session:
            # Check if memory already exists
            existing_memory = db_session.exec(
                sqlmodel.select(ChatBotMemory).where(
                    ChatBotMemory.userinfo_id == self.my_userinfo_id,
                    ChatBotMemory.memory_key == key
                )
            ).one_or_none()

            if existing_memory:
                print(f"Updating existing memory: {key} = {value}")
                existing_memory.memory_value = value
            else:
                print(f"Storing new memory: {key} = {value}")
                new_memory = ChatBotMemory(
                    userinfo_id=self.my_userinfo_id,
                    memory_key=key,
                    memory_value=value
                )
                db_session.add(new_memory)
            db_session.commit()

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
        # Load the user's memory and include it in the system prompt
        user_memory = self.load_user_memory()

        system_prompt = "You are a helpful assistant with a great deal of general knowledge. Respond in markdown."

        # If user memory exists, add it to the system prompt

        if user_memory:
            memory_info = "\n".join([f"{key}: {value}" for key, value in user_memory.items()])
            system_prompt += f" You remember the following about the user:\n{memory_info}"


        gpt_messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

        # Fetch relevant prompts and suggest them
        relevant_prompts = UserProfileState.get_relevant_prompts(self.my_userinfo_id)
        if relevant_prompts:
            suggestion_prompts = "Here are some suggestions based on your saved preferences:\n" + "\n".join([f"{i+1}. {prompt}" for i, prompt in enumerate(relevant_prompts)])
            gpt_messages.append({"role": "system", "content": suggestion_prompts})

        for chat_message in self.messages:
            role = "user"
            if chat_message.is_bot:
                role = "system"
            gpt_messages.append({
                "role": role,
                "content": chat_message.message
            })
        return gpt_messages 

    def handle_suggested_prompts(self, prompt: str):
        """Handle the user clicking on a suggested prompt."""
        print(f"Suggested prompt clicked: {prompt}")

        # Treat the suggested prompt like a normal message
        self.append_message_to_ui(prompt, is_bot=False)
        self.insert_message_to_db(prompt, "user")

        # Send the prompt to the AI for processing
        gpt_messages = self.get_gpt_messages()

        userinfo_id = self.my_userinfo_id
        token_counter_factory = TokenCounterFactory(self, userinfo_id)

        def agent(query):
            return ai.get_llm_response(query)
        
        count_tokens = token_counter_factory.create_token_counter(ai.get_llm_response)
        bot_response = count_tokens(gpt_messages)

        # Append AI Response
        self.append_message_to_ui(bot_response, is_bot=True)
        self.insert_message_to_db(bot_response, role="system")

        print(f"Processed suggested prompt - Session: {self.chat_session.id}")

    async def handle_submit(self, form_data:dict):
        
        user_message = form_data.get("message")
        if user_message:
            self.did_submit = True
            if not self.chat_session:
                print("No chat session available, creating new one.")
                self.create_new_chat_session()
            self.append_message_to_ui(user_message, is_bot=False)
            print(f"Before user message insert - Session: {self.chat_session.id}, User: {self.my_userinfo_id}")
            self.insert_message_to_db(user_message, "user")
            yield


            if "my name is" in user_message.lower():
                name = user_message.split("my name is")[1].strip() # Simplistic extraction
                self.store_user_memory("user_name", name)

            gpt_messages = self.get_gpt_messages()

            userinfo_id = self.my_userinfo_id
            token_counter_factory = TokenCounterFactory(self, userinfo_id)

            def agent(query):
                return ai.get_llm_response(query)
            
            count_tokens = token_counter_factory.create_token_counter(ai.get_llm_response)
            bot_response = count_tokens(gpt_messages)

            
            self.did_submit = False

            # Append AI Response
            self.append_message_to_ui(bot_response, is_bot=True)
            self.insert_message_to_db(bot_response, role="system")
            
            print(f"After AI insert to DB response insert - Session: {self.chat_session.id}, User: {self.my_userinfo_id}")
            yield

class ChatSetupState(rx.State):
    user_preferences: dict = {}

    def handle_initial_setup(self, form_data: dict):
        """Handle the form submission and store the user preferences."""
        user_id = self.my_userinfo_id

        if not user_id:
            print("No user logged in!")
            return
        
        # Extract data from the form
        name = form_data.get("name")
        occupation = form_data.get("occupation")
        goals = form_data.get("goals")
        learning_style = form_data.get("learning_style")
        hobbies = form_data.get("hobbies")
        preferred_topics = form_data.get("preferred_topics")

        # Save each as memory
        self.save_to_memory(user_id, "user_name", name)
        self.save_to_memory(user_id, "occupation", occupation)
        self.save_to_memory(user_id, "goals", goals)
        self.save_to_memory(user_id, "learning_style", learning_style)
        self.save_to_memory(user_id, "hobbies", hobbies)
        self.save_to_memory(user_id, "preferred_topics", preferred_topics)
        
        print(f"User {user_id} preferences saved!")
