from modules.prompt_templates import symptom_prompt
from modules.gemini_client import generate_response


def analyze_symptoms(symptoms):
    prompt = symptom_prompt(symptoms)
    return generate_response(prompt)