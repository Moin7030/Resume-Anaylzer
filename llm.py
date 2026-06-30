from groq import Groq
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()

def get_llm():
    api_key=os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("Groq API key not found")

    return ChatGroq(
        model='llama-3.3-70b-versatile',
        temperature=0,
        api_key=api_key
    )

