def get_health_dashboard_data(history):

    data = {
        "total_activities": len(history),
        "symptom_reports": 0,
        "pdf_reports": 0,
        "chatbot_queries": 0,
        "rag_queries": 0,
        "skin_reports": 0
    }

    for item in history:

        text = item.lower()

        if "symptom" in text:
            data["symptom_reports"] += 1

        if "pdf" in text or "medical report" in text:
            data["pdf_reports"] += 1

        if "chatbot" in text:
            data["chatbot_queries"] += 1

        if "rag" in text:
            data["rag_queries"] += 1

        if "skin" in text:
            data["skin_reports"] += 1

    return data