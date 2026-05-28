import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

if not api_key:
    api_key = None

if api_key:
    genai.configure(api_key=api_key)

gemini_model = genai.GenerativeModel("gemini-2.0-flash-lite")


def generate_response(prompt):
    if not api_key:
        return fallback_response()

    try:
        response = gemini_model.generate_content(prompt)
        return response.text

    except Exception as error:
        return fallback_response(error)


def fallback_response(error=None):
    message = """
AI service is currently unavailable, so HealthLens AI is showing a safe demo fallback response.

1. Simple Explanation
The entered health information may be related to a common condition, but the exact cause cannot be confirmed without medical evaluation.

2. Basic Precautions
- Stay hydrated
- Take proper rest
- Monitor symptoms
- Eat light and balanced food
- Avoid self-medication

3. When to Consult a Doctor
Consult a doctor if symptoms are severe, continue for a long time, or become worse.

4. Important Note
This is an educational fallback response, not a medical diagnosis.
"""

    if error:
        message += f"""

Technical Note:
{error}
"""

    return message