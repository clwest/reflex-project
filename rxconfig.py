import reflex as rx
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")

config = rx.Config(
    app_name="reflex_project",
    db_url=DATABASE_URL,
)