from PIL import Image

from modules.gemini_client import gemini_model


def analyze_skin_image(uploaded_image):

    image = Image.open(uploaded_image)

    prompt = """
You are a healthcare vision assistant.

Analyze this skin image carefully.

Provide:

1. General Observation
2. Possible Skin Condition Category
3. Basic Precautions
4. When to Consult Dermatologist

Rules:
- Do NOT give final diagnosis.
- Do NOT prescribe medicines.
- Keep response safe and educational.
"""

    response = gemini_model.generate_content(
        [prompt, image]
    )

    return response.text