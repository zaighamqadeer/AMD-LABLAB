from local_llm import generate_local


def solve_sentiment(prompt: str) -> str:
    system_prompt = "Format strictly as: 'Sentiment: [Positive/Negative/Mixed/Neutral]. Justification: [Reason]'."
    return generate_local(prompt, system_prompt=system_prompt)