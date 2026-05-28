import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

try:
    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

gemini_model = genai.GenerativeModel("gemini-2.0-flash-lite")


def fallback_response(error=None):
    msg = """
AI service is currently unavailable due to quota/API limits.

Demo Fallback Response:

1. Simple Explanation
The provided health information may be related to a common condition, but exact cause cannot be confirmed without medical evaluation.

2. Basic Precautions
- Stay hydrated
- Take rest
- Eat light and balanced food
- Monitor symptoms
- Avoid self-medication

3. When to Consult a Doctor
Consult a doctor if symptoms are severe, continue for a long time, or worsen.

4. Disclaimer
This is an educational fallback response, not a medical diagnosis.
"""

    if error:
        msg += f"\n\nTechnical Note:\n{error}"

    return msg


def generate_response(prompt):
    if not api_key:
        return fallback_response("API key missing.")

    try:
        response = gemini_model.generate_content(prompt)
        return response.text

    except Exception as error:
        return fallback_response(error)


def generate_image_response(prompt, image):
    if not api_key:
        return fallback_response("API key missing.")

    try:
        response = gemini_model.generate_content([prompt, image])
        return response.text

    except Exception as error:
        return fallback_response(error)