import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
OPENAI_MODEL="gpt-4o-mini"


def get_client():
    return OpenAI()

def get_llm_response(gpt_messages):
    client = get_client()
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=gpt_messages
    )

    return completion.choices[0].message.content