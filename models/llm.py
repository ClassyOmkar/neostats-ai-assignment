import os
# Use generic OpenAI client which works with Groq's OpenAI-compatible API
from langchain_community.chat_models import ChatOpenAI

def get_chatgroq_model():
    """
    Returns a ChatOpenAI instance configured for Groq API.
    Uses 'llama3-70b-8192' or similar model.
    """
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
        
    return ChatOpenAI(
        model_name="llama-3.3-70b-versatile",
        openai_api_key=groq_api_key,
        openai_api_base="https://api.groq.com/openai/v1"
    )