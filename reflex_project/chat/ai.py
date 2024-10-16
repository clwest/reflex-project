import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
OPENAI_MODEL="gpt-4o-mini"
EMBEDDING_MODEL="text-embedding-3-small"

def get_client():
    return OpenAI()

def get_llm_response(gpt_messages):
    client = get_client()
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=gpt_messages
    )
    return completion.choices[0].message.content


def create_embedding(text, model=EMBEDDING_MODEL):
    client = get_client()
    text = text.replace("\n", "")
    response = client.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding

def get_embedding(text, model=EMBEDDING_MODEL):
    client = get_client()
    text = text.replace("\n", "")

    return client.embeddings.create(input=[text], model=model).data[0].embedding