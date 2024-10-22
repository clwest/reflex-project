from langchain_community.callbacks import get_openai_callback
from pprint import pprint
from ..chat.token_state import TokenUsageState 


class TokenCounterFactory:
    def __init__(self, chat_session_state, userinfo_id):
        self.chat_session_state = chat_session_state
        self.userinfo_id = userinfo_id

    def create_token_counter(self, agent):
        def count_tokens(query):
            with get_openai_callback() as cb:
                result = agent(query)
                print(f"Captured tokens - Prompt: {cb.prompt_tokens}, Completion: {cb.completion_tokens}, Total: {cb.total_tokens}, Cost: {cb.total_cost}")
                self._log_token_usage(cb)
            return result

        return count_tokens

    def _log_token_usage(self, callback):
        """Logs token usage to TokenUsageState."""
        session_id=self.chat_session_state.chat_session.id

        TokenUsageState.track_token_usage(
            session_id=session_id,
            prompt_tokens=callback.prompt_tokens,
            completion_tokens=callback.completion_tokens,
            total_tokens=callback.total_tokens,
            total_cost=callback.total_cost,
            userinfo_id=self.userinfo_id,
            usage_type="chat"
        )

        pprint(f"Spent a total of {callback.total_tokens} tokens")
        pprint(f"Prompt Tokens: {callback.prompt_tokens}")
        pprint(f"Completion Tokens: {callback.completion_tokens}")
        pprint(f"Total Cost (USD): ${callback.total_cost}")
        # Set the values for the TokenUsageState



# Usage
# token_counter_factory = TokenCounterFactory()
# token_counter = token_counter_factory.create_token_counter(your_agent)
# result = token_counter("Your query here")
