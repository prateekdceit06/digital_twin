import os
from openai import OpenAI

def get_openai_client() -> OpenAI:
    # Uses default env OPENAI_API_KEY
    return OpenAI()

def get_gemini_client() -> OpenAI:
    # OpenAI-compatible endpoint for Gemini
    return OpenAI(
        api_key=os.getenv("GOOGLE_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
