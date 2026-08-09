from langchain_mistralai import ChatMistralAI
from app.config import MISTRAL_API_KEY, MODEL_NAME

def get_llm():
    return ChatMistralAI(
        api_key=MISTRAL_API_KEY,
        model=MODEL_NAME,
    )