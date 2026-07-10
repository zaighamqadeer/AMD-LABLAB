from fireworks_client import call_fireworks
from local_llm import generate_local

def solve_logic(prompt: str) -> str:
    # 1. LOCAL FIRST (0 Tokens)
    sys_local = "Solve the logic puzzle. Output ONLY the final answer in 1 to 3 words. No explanation."
    local_ans = generate_local(prompt, system_prompt=sys_local)
    
    # Validation: If the local model gives a short answer, it understood the constraint.
    if local_ans and len(local_ans.split()) <= 3 and "error" not in local_ans.lower():
        return local_ans.strip()

    # 2. ESCALATE TO API (Token Spend)
    sys_api = "Output ONLY the final answer in 1 to 3 words. No reasoning."
    api_resp = call_fireworks(prompt, max_tokens=10, system_prompt=sys_api)
    return api_resp if api_resp else "Unknown"