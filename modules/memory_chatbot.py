from modules.gemini_client import gemini_model


def get_memory_response(user_question, chat_history):

    history_text = ""

    for message in chat_history:
        role = message["role"]
        content = message["content"]

        history_text += f"{role}: {content}\n"

    prompt = f"""
You are HealthLens AI, a safe healthcare assistant.

Previous conversation:
{history_text}

Current user question:
{user_question}

Answer using the conversation context.

Rules:
- Do not give final diagnosis
- Do not prescribe medicines
- Keep answer simple
- Recommend doctor consultation when needed
"""

    response = gemini_model.generate_content(prompt)

    return response.text