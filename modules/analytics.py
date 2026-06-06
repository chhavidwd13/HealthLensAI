def get_dashboard_stats(history):

    stats = {
        "reports": 0,
        "chatbot": 0,
        "rag": 0,
        "image": 0
    }

    for item in history:

        text = item.lower()

        if "report" in text:
            stats["reports"] += 1

        if "chatbot" in text:
            stats["chatbot"] += 1

        if "rag" in text:
            stats["rag"] += 1

        if "skin" in text:
            stats["image"] += 1

    return stats