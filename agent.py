import json

def load_catalog():
    with open('catalog.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def decide_intent(text: str) -> str:
    text = text.lower()

    if "difference" in text or "vs" in text or "compare" in text:
        return "compare"

    if "add" in text or "also" in text or "what about" in text:
        return "refine"

    # Simple keyword heuristic for recommendation
    if any(kw in text for kw in ["java", "python", "developer", "engineer", "manager", "mid-level", "senior"]):
        return "recommend"

    return "clarify"

def search_catalog(query: str, catalog: list):
    query = query.lower()
    results = []
    
    # Try to match based on keywords in query
    # E.g., if query has "java", return the Java test
    for item in catalog:
        if "java" in query and "java" in item["name"].lower():
            results.append(item)
        elif "python" in query and "python" in item["name"].lower():
            results.append(item)
        elif ("personality" in query or "behavior" in query or "opq" in query) and "opq" in item["name"].lower():
            results.append(item)
        elif ("cognitive" in query or "ability" in query or "gsa" in query) and "gsa" in item["name"].lower():
            results.append(item)
            
    # If no specific matches but it's a recommend intent, just return something generic or everything
    if not results:
        results = catalog

    # Format strictly for the expected schema
    formatted_results = []
    for r in results:
        formatted_results.append({
            "name": r["name"],
            "url": r["url"],
            "test_type": r["test_type"]
        })
        
    return formatted_results[:10]
