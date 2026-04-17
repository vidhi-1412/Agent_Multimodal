import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return "openrouter/openai/gpt-3.5-turbo"