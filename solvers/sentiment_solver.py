from local_llm import generate_local

def solve_sentiment(prompt: str) -> str:
    # 0.5B models are excellent at zero-shot sentiment. Use it.
    system_prompt = "Format strictly as: 'Sentiment: [Positive/Negative/Mixed/Neutral]. Justification: [Reason]'."
    return generate_local(prompt, system_prompt=system_prompt)