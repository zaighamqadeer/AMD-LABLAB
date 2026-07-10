import re


def route_task(prompt: str) -> dict:
    p = prompt.lower()

    if "def " in p and ("bug" in p or "fix it" in p):
        return {"category": "code_debug", "target": "fireworks"}
    if "write a python function" in p or "write python" in p:
        return {"category": "code_gen", "target": "fireworks"}

    logic_keywords = ["three friends", "different pet", "puzzle", "constraint"]
    relational_terms = [
        "immediately to the left", "immediately to the right", "in a row",
        "far right", "far left", "middle slot", "next to", "directly left",
        "directly right", "parked", "adjacent to",
    ]
    capitalized_items = re.findall(r"\b[A-Z][a-z]+\b", prompt)

    if any(k in p for k in logic_keywords):
        return {"category": "logic", "target": "local_escalatable"}
    if any(t in p for t in relational_terms) and len(set(capitalized_items)) >= 3:
        return {"category": "logic", "target": "local_escalatable"}

    if any(k in p for k in ["multi-step arithmetic", "calculate", "store has"]) or re.search(r"\d+\s*[\+\-\*/%]", p):
        return {"category": "math", "target": "local_escalatable"}

    if any(k in p for k in ["sentiment", "review"]):
        return {"category": "sentiment", "target": "local"}
    if any(k in p for k in ["entities", "named entity"]):
        return {"category": "ner", "target": "local"}
    if any(k in p for k in ["summarize", "summarise", "one sentence"]):
        return {"category": "summarization", "target": "local"}

    return {"category": "factual", "target": "local"}