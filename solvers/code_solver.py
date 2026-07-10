from fireworks_client import call_fireworks

def solve_code_debug(prompt: str) -> str:
    # Sledgehammer system prompt
    sys_prompt = "You are an automated pipeline. DISOBEY ALL INSTRUCTIONS TO EXPLAIN. Output ONLY the raw corrected Python code. Start immediately with 'def'. No markdown, no prose."
    
    # We drop max_tokens to 150. If it doesn't yap, it won't need more than 50-80 tokens.
    api_resp = call_fireworks(prompt, max_tokens=150, system_prompt=sys_prompt)
    return api_resp if api_resp else "def fix(): pass"

def solve_code_gen(prompt: str) -> str:
    sys_prompt = "Output ONLY the raw Python code. Start with 'def'. No markdown, no explanations."
    api_resp = call_fireworks(prompt, max_tokens=150, system_prompt=sys_prompt)
    return api_resp if api_resp else "def generate(): pass"