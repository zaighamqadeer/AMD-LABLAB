import re

def route_task(prompt: str) -> dict:
    p = prompt.lower()
    
    # Route coding directly to API (0.5B models completely fail at writing Python)
    if "def " in p and ("bug" in p or "fix it" in p or "identify" in p):
        return {"category": "code_debug", "target": "fireworks"}
    if "write a python function" in p or "write python" in p:
        return {"category": "code_gen", "target": "fireworks"}
    
    # EVERYTHING else goes to the solvers where Local-First Escalation happens
    if any(k in p for k in ["sentiment", "review", "classify"]):
        return {"category": "sentiment", "target": "local"}
    if any(k in p for k in ["entities", "named entity", "extract"]):
        return {"category": "ner", "target": "local"}
    if any(k in p for k in ["summarize", "summarise", "one sentence"]):
        return {"category": "summarization", "target": "local"}
    if any(k in p for k in ["three friends", "different pet", "puzzle", "constraint", "logic"]):
        return {"category": "logic", "target": "local_escalatable"}
        
    # Tightened math regex to require digits on BOTH sides of the operator
    if any(k in p for k in ["arithmetic", "calculate", "store has", "math"]) or re.search(r"\b\d+\s*[\+\-\*\/]\s*\d+\b", p):
        return {"category": "math", "target": "local_escalatable"}
    
    return {"category": "factual", "target": "local"}