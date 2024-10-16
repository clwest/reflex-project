from langchain_community.callbacks.manager import get_openai_callback
from pprint import pprint


class TokenCounterFactory:
    def __init__(self, chat_session_state):
        self.chat_session_state = chat_session_state

    def create_token_counter(self, agent):
        def count_tokens(query):
            with get_openai_callback() as cb:
                result = agent(query)
                self._log_token_usage(cb)
            return result

        return count_tokens

    def _log_token_usage(self, callback):
        # Log token usage into the database using the 'log_token_usage' method in ChatSessionState
        session_id = self.chat_session_state.chat_session.id
        self.chat_session_state.log_token_usage(
            session_id=session_id,
            prompt_tokens=callback.prompt_tokens,
            completion_tokens=callback.completion_tokens,
            total_tokens=callback.total_tokens,
            total_cost=callback.total_cost,
            usage_type="chat" # Can change based on usage
        )
        
    # Also print the token usage for debugging purposes
        pprint(f"Spent a total of {callback.total_tokens} tokens")
        pprint(f"Prompt Tokens: {callback.prompt_tokens}")
        pprint(f"Completion Tokens: {callback.completion_tokens}")
        pprint(f"Total Cost (USD): ${callback.total_cost}")


# Usage
# token_counter_factory = TokenCounterFactory()
# token_counter = token_counter_factory.create_token_counter(your_agent)
# result = token_counter("Your query here")
