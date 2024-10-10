from typing import Optional
import sqlmodel
import reflex as rx
import reflex_local_auth
from ..models import UserInfo



class SessionState(reflex_local_auth.LocalAuthState):

    @rx.var(cache=True)
    # Access .user from class
    def my_userinfo_id(self) -> str | None:
        if self.authenticated_user_info is None:
            return None
        return self.authenticated_user_info.id
    
    @rx.var(cache=True)
    def my_user_id(self) -> str | None:
        if self.authenticated_user.id < 0:
            return None
        return self.authenticated_user.id

    @rx.var(cache=True)
    def authenticated_username(self) -> str | None:
        if self.authenticated_user.id < 0:
            return None
        return self.authenticated_user.username
    

    @rx.var(cache=True)
    def authenticated_user_info(self) -> UserInfo | None:
        if self.authenticated_user.id < 0:
            return
        with rx.session() as session:
            result = session.exec(
                sqlmodel.select(UserInfo).where(
                    UserInfo.user_id == self.authenticated_user.id
                ),
            ).one_or_none()
            if result is None:
                return None
            # Database lookup for user
            # result.user
            # user_obj = result.user
            # print(result.user)
            return(result)
    
    def on_load(self):
        if not self.is_authenticated:
            return reflex_local_auth.LoginState.redir
        print(self.is_authenticated)
        print(self.authenticated_user_info)

    def perform_logout(self):
        self.do_logout()
        return rx.redirect("/")

class MyRegisterState(reflex_local_auth.RegistrationState):
    # This event handler must be named something besides `handle_registration`!!!
    
    def handle_registration_email(self, form_data):
        registration_result = self.handle_registration(form_data)
        if self.new_user_id >= 0:
            with rx.session() as session:
                session.add(
                    UserInfo(
                        email=form_data["email"],
                        # created_from_ip=self.router.headers.get(
                        #     "x_forwarded_for",
                        #     self.router.session.client_ip,
                        # ),
                        user_id=self.new_user_id,
                    )
                )
                session.commit()
        return registration_result




