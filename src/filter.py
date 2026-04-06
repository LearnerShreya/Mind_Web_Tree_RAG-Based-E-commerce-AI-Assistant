import re

def extract_price(query):
    match = re.search(r'(\d+)', query)
    if match:
        return int(match.group(1))
    return None


def apply_filters(results, query):
    price_limit = extract_price(query)

    if price_limit:
        filtered = []
        for doc in results:
            if "price" in doc.metadata and doc.metadata["price"] <= price_limit:
                filtered.append(doc)
        return filtered

    return results