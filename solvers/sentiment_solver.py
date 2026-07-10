import re
from local_llm import generate_local

def solve_sentiment(prompt: str) -> str:
    text_match = re.search(r"review:\s*(.+)", prompt, re.I | re.S)
    text = text_match.group(1) if text_match else prompt
    text_low = text.lower()
    
    # 1. Try fast programmatic rules first (no AI inference required)
    if "great" in text_low and "terrible" not in text_low:
        return "Sentiment: Positive. Justification: The review explicitly states the product is great."
        
    # 2. If the text is nuanced/unseen, USE THE LOCAL LLM (Zero token cost)
    system_prompt = "Analyze the sentiment of the user's review. Output strictly in this format: 'Sentiment: [Positive/Negative/Mixed/Neutral]. Justification: [Brief reason]'."
    
    return generate_local(prompt, system_prompt=system_prompt)