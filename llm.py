from groq import Groq
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from sentence_transformers import SentenceTransformer


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
_embedding_model=None

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model=SentenceTransformer('all-MiniLM-L6-v2')
    return _embedding_model
    

