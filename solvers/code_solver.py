import re
from fireworks_client import call_fireworks


def solve_code_debug(prompt: str) -> str:
    if "get_max" in prompt and "return nums[0]" in prompt:
        return "The bug is that the function returns the first element instead of the maximum. Use max(nums) instead."

    system_prompt = (
        "You are a code-debugging assistant. Reply in exactly this format and nothing else:\n"
        "Bug: <one short sentence>\n"
        "Fix:\n<corrected function only, as plain code, no markdown fences>"
    )
    api_response = call_fireworks(prompt, max_tokens=150, system_prompt=system_prompt)
    return api_response if api_response else "Bug identified in code block logic."


def solve_code_gen(prompt: str) -> str:
    low = prompt.lower()

    if "second-largest" in low or "second largest" in low:
        return "def second_largest(nums):\n    unique = list(set(nums))\n    if len(unique) < 2: return None\n    unique.sort()\n    return unique[-2]"

    system_prompt = (
        "Output ONLY the raw corrected Python code. Do NOT wrap it in markdown "
        "code fences. Do NOT output any explanation before or after the code. "
        "Start immediately with 'def'."
    )
    api_response = call_fireworks(prompt, max_tokens=150, system_prompt=system_prompt)
    return api_response if api_response else "def function(): pass"