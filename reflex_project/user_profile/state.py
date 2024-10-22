import reflex as rx
from ..auth.state import SessionState
import sqlmodel
from ..models import ChatBotMemory, UserPrompts
from typing import List, Optional


class UserProfileState(SessionState):
    user_preferences: dict = {}

    @rx.var
    def my_userinfo_id(self) -> int:
        return self.get_authenticated_user_id

    @rx.var
    def get_user_prompts(self) -> List[UserPrompts]:
        with rx.session() as db_session:
            return db_session.exec(
                sqlmodel.select(UserPrompts).where(
                    UserPrompts.userinfo_id == self.my_userinfo_id
                )
            ).all() or []


    def handle_initial_setup(self, form_data: dict):
        """Handle the form submission and store the user preferences."""
        my_userinfo_id = self.get_authenticated_userinfo_id

        if not my_userinfo_id:
            print("No user logged in")
            return 
        
        # Extract data from the form
        name = form_data.get("name")
        occupation = form_data.get("occupation")
        goals = form_data.get("goals")
        learning_style = form_data.get("learning_style")
        hobbies = form_data.get("hobbies")  
        preferred_topics = form_data.get("preferred_topics")

        # Save each piece of the information as memory
        self.store_user_memory("user_name", name)
        self.store_user_memory("occupation", occupation)
        self.store_user_memory("goals", goals)
        self.store_user_memory("learning_style", learning_style)
        self.store_user_memory("hobbies", hobbies)
        self.store_user_memory("preferred_topics", preferred_topics)

    def store_user_memory(self, key: str, value: str):
        # reuse store_user_memory
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

    def handle_prompt_submit(self, form_data: dict):
        """Handle prompt form submissions"""
        prompt_text = form_data.get("prompt_text")
        prompt_category = form_data.get("prompt_category", "General")

        if prompt_text:
            with rx.session() as db_session:
                new_prompt = UserPrompts(
                    userinfo_id = self.my_userinfo_id,
                    prompt_text=prompt_text,
                    prompt_category=prompt_category
                )
                db_session.add(new_prompt)
                db_session.commit()
                print(f"Saved new prompt: {prompt_text} under category {prompt_category}")

    @classmethod
    def get_relevant_prompts(cls, user_id: int) -> List[str]:
        """Fetch relevant prompts based on user preferences or context."""
        with rx.session() as db_session:
            prompts = db_session.exec(
                sqlmodel.select(UserPrompts).where(
                    UserPrompts.userinfo_id == user_id
                )
            ).all()

            return [prompt.prompt_text for prompt in prompts if prompt.prompt_text] # Returns a list of relevant prompts