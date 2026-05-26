import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = st.secrets.get(
    "GEMINI_API_KEY",
    os.getenv("GEMINI_API_KEY")
)

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing."
    )

genai.configure(api_key=api_key)

gemini_model = genai.GenerativeModel(
    "gemini-1.5-flash"
)


def generate_response(prompt):

    try:
        response = gemini_model.generate_content(prompt)
        return response.text

    except Exception as error:

        return f"""
Something went wrong while generating AI response.

Possible reasons:
- API quota exceeded
- Internet issue
- Invalid API key
- Gemini service unavailable

Error details:
{error}
"""