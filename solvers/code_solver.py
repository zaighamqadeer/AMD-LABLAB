from fireworks_client import call_fireworks

def solve_code_debug(prompt: str) -> str:
    # Ultra-short system prompt saves input tokens
    sys_prompt = "Output ONLY the raw corrected Python code. Start with 'def'. No markdown, no explanations."
    # Max tokens dropped to 150 - enough for a function, not enough for an essay
    api_resp = call_fireworks(prompt, max_tokens=150, system_prompt=sys_prompt)
    return api_resp if api_resp else "def fix(): pass"

def solve_code_gen(prompt: str) -> str:
    sys_prompt = "Output ONLY the raw Python code. Start with 'def'. No markdown, no explanations."
    api_resp = call_fireworks(prompt, max_tokens=150, system_prompt=sys_prompt)
    return api_resp if api_resp else "def generate(): pass"