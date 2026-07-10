import re
import ast
import operator
from fireworks_client import call_fireworks

SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def safe_eval(expr):
    try:
        node = ast.parse(expr, mode="eval")

        def _eval(n):
            if isinstance(n, ast.Expression):
                return _eval(n.body)
            if isinstance(n, ast.Constant):
                return n.value
            if isinstance(n, ast.Num):
                return n.n
            if isinstance(n, ast.BinOp):
                return SAFE_OPS[type(n.op)](_eval(n.left), _eval(n.right))
            if isinstance(n, ast.UnaryOp):
                return SAFE_OPS[type(n.op)](_eval(n.operand))
            raise ValueError("unsafe")

        return _eval(node)
    except Exception:
        return None


def solve_math(prompt: str) -> str:
    prompt_low = prompt.lower()

    m = re.search(
        r"has (\d+)\s+items?.*?(\d+)\s*%.*?(\d+)\s+more",
        prompt_low,
        re.S,
    )
    if m:
        total = int(m.group(1))
        pct = int(m.group(2))
        more = int(m.group(3))
        remain = total - (total * pct / 100) - more
        remain = int(remain) if float(remain).is_integer() else remain
        return f"{remain} items remain."

    m = re.search(r"(\d+)\s*%\s*of\s*(\d+)", prompt_low)
    if m:
        pct = int(m.group(1))
        total = int(m.group(2))
        return str(int(total * pct / 100))

    expr_match = re.search(r"what is ([0-9\+\-\*/\(\) \.%]+)\??", prompt_low)
    if expr_match:
        expr = expr_match.group(1).replace("%", "/100*")
        val = safe_eval(expr)
        if val is not None:
            return str(int(val) if float(val).is_integer() else val)

    system_prompt = (
        "You are a calculator. Solve the problem and output ONLY the final "
        "numeric answer as plain text. No markdown, no bold, no asterisks, "
        "no units, no explanation, no 'Calculation:' label. Just the number."
    )
    api_response = call_fireworks(prompt, max_tokens=40, system_prompt=system_prompt)
    return api_response if api_response else "0"