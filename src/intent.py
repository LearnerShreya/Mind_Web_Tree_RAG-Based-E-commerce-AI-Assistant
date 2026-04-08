def detect_intent(query):
    query = query.lower()

    if any(word in query for word in ["under", "less than", "budget"]):
        return "price_filter"
    elif any(word in query for word in ["compare", "vs"]):
        return "comparison"
    elif any(word in query for word in ["recommend", "best", "suggest"]):
        return "recommendation"
    elif any(word in query for word in ["hello", "hi"]):
        return "casual"
    else:
        return "search"