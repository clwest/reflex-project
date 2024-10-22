import reflex as rx

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
