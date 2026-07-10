import re
import ast
import operator
from fireworks_client import call_fireworks
from local_llm import generate_local

SAFE_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
    ast.USub: operator.neg,
}

def safe_eval(expr):
    try:
        node = ast.parse(expr, mode='eval')
        def _eval(n):
            if isinstance(n, ast.Expression): return _eval(n.body)
            if isinstance(n, ast.Constant): return n.value
            if isinstance(n, ast.Num): return n.n
            if isinstance(n, ast.BinOp): return SAFE_OPS[type(n.op)](_eval(n.left), _eval(n.right))
            if isinstance(n, ast.UnaryOp): return SAFE_OPS[type(n.op)](_eval(n.operand))
            raise ValueError("unsafe")
        return _eval(node)
    except:
        return None

def solve_math(prompt: str) -> str:
    prompt_low = prompt.lower()

    # 1. Generic parsing for direct equations ONLY (e.g., "What is 45 * 2 + 10?")
    expr_match = re.search(r"([0-9]+(?:\.[0-9]+)?\s*[\+\-\*/]\s*[0-9]+(?:\.[0-9]+)?(?:[\s\+\-\*/0-9\.]+)*)", prompt_low)
    if expr_match:
        val = safe_eval(expr_match.group(1))
        if val is not None:
            return str(int(val) if float(val).is_integer() else val)

    # 2. LOCAL FIRST (0 Tokens)
    sys_prompt_local = "Solve the problem. Output ONLY the final numeric answer. Nothing else."
    local_ans = generate_local(prompt, system_prompt=sys_prompt_local)
    
    # Validation: If the 0.5B model outputs a clean number, trust it and save the tokens.
    if local_ans and re.fullmatch(r"-?\d+(?:\.\d+)?", local_ans.strip()):
        return local_ans.strip()

    # 3. ESCALATE TO API (Token Spend)
    sys_prompt_api = "Output only the final numeric answer."
    api_resp = call_fireworks(prompt, max_tokens=10, system_prompt=sys_prompt_api)
    return api_resp if api_resp else "0"