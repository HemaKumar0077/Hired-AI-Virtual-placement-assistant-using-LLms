from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

def load_llm():
    # GROQ_API_KEY = "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"
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")

    llm = init_chat_model("llama3-70b-8192", model_provider="groq")

    return llm

def load_llm_think():
    llm_think = init_chat_model("deepseek-r1-distill-llama-70b", model_provider="groq")

    return llm_think   
