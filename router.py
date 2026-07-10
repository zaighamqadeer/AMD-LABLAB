import re

def route_task(prompt: str) -> dict:
    """
    Returns a dict with 'category' and 'target' (local vs fireworks).
    Target 'local' costs 0 tokens. Target 'fireworks' costs tokens.
    """
    p = prompt.lower()
    
    # --- FIREWORKS API TASKS (Too hard for 0.5B model) ---
    if "def " in p and ("bug" in p or "fix it" in p):
        return {"category": "code_debug", "target": "fireworks"}
    if "write a python function" in p or "write python" in p:
        return {"category": "code_gen", "target": "fireworks"}
    if any(k in p for k in ["three friends", "different pet", "puzzle", "constraint"]):
        return {"category": "logic", "target": "fireworks"}
    if any(k in p for k in ["multi-step arithmetic", "calculate", "store has"]) or re.search(r"\d+\s*[\+\-\*/%]", p):
        return {"category": "math", "target": "fireworks"}

    # --- LOCAL MODEL TASKS (Zero token cost) ---
    if any(k in p for k in ["sentiment", "review"]):
        return {"category": "sentiment", "target": "local"}
    if any(k in p for k in ["entities", "named entity"]):
        return {"category": "ner", "target": "local"}
    if any(k in p for k in ["summarize", "summarise", "one sentence"]):
        return {"category": "summarization", "target": "local"}
    
    # Fallback to local for basic factual questions
    return {"category": "factual", "target": "local"}