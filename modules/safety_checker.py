def check_emergency(symptoms):
    emergency_keywords = [
        "chest pain",
        "difficulty breathing",
        "unconscious",
        "seizure",
        "severe bleeding",
        "stroke",
        "heart attack",
        "very high fever"
    ]

    symptoms_lower = symptoms.lower()

    for keyword in emergency_keywords:
        if keyword in symptoms_lower:
            return True

    return False