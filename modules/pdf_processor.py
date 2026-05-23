import fitz
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")


def extract_text_from_pdf(uploaded_file):
    text = ""

    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    for page in pdf_document:
        text += page.get_text()

    return text


def summarize_report(text):
    prompt = f"""
    You are a medical report assistant.
    Summarize this medical report in simple language.
    Do not give final diagnosis.
    Suggest consulting a doctor if needed.

    Report:
    {text}
    """

    response = model.generate_content(prompt)
    return response.text