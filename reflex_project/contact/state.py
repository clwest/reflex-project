from typing import List
import reflex as rx
import asyncio
from sqlmodel import select

from ..auth.state import SessionState
from ..models import ContactEntryModel

class ContactState(SessionState):
    form_data: dict = {}
    entries: List['ContactEntryModel'] = []
    did_submit: bool = False

    @rx.var
    def thank_you(self):
        first_name = self.form_data.get("first_name") or ""
        return f"Thank you {first_name}".strip() + "!"

    async def handle_submit(self, form_data: dict):
        """Handle the form submit."""
        # print(form_data)
        self.form_data = form_data
        data = {}
        for k, v in form_data.items():
            if v == "" or v is None:
                continue
            data[k] = v
        if self.my_user_id is not None:
            data['user_id'] = self.my_user_id

        if self.get_authenticated_userinfo_id is not None:
            data['userinfo_id'] = self.get_authenticated_userinfo_id
        # print("Contact data", data)
        with rx.session() as session:
            db_entry = ContactEntryModel(
                **data
            )
            session.add(db_entry)
            session.commit()    
            self.did_submit = True
            yield
            
        await asyncio.sleep(5)
        self.did_submit = False
    
    def list_entries(self):
        with rx.session() as session:
            entries = session.exec(
                select(ContactEntryModel)
            ).all()
            self.entries = entries
    

