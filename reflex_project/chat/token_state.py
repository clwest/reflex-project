import reflex as rx
from ..models import TokenUsage


class TokenUsageState(rx.State):
    token_session_id: int
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    total_cost: float

    # def track_token_usage(self):
    #     print(f"Tracking token usage - Session ID: {self.token_session_id}, Prompt: {self.prompt_tokens}, Completion: {self.completion_tokens}, Total: {self.total_tokens}, Cost: {self.total_cost}")
    #     with rx.session() as db_session:
    #         token_entry = TokenUsage(
    #             userinfo_id=self.my_userinfo_id,
    #             session_id=self.token_session_id,
    #             prompt_tokens=self.prompt_tokens,
    #             completion_tokens=self.completion_tokens,
    #             total_tokens=self.total_tokens,
    #             total_cost=self.total_cost,
    #             usage_type="chat"
    #         )
    #         db_session.add(token_entry)
    #         db_session.commit()

    @staticmethod
    def track_token_usage(session_id, prompt_tokens, completion_tokens, total_tokens, total_cost, userinfo_id, usage_type):
        """Logs token usage to the TokenUsage table."""
        print(f"Logging token usage for session {session_id}, user {userinfo_id}")
        with rx.session() as db_session:
            token_data = TokenUsage(
                userinfo_id=userinfo_id,
                session_id=session_id,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                total_cost=total_cost,
                usage_type=usage_type,
            )
            db_session.add(token_data)
            db_session.commit()