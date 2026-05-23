import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing. Please add it inside .env file.")

genai.configure(api_key=api_key)

gemini_model = genai.GenerativeModel("gemini-1.5-flash")


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