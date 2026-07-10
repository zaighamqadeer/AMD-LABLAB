import re
from local_llm import generate_local

def split_sentences(text):
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()]

def solve_summarization(prompt: str) -> str:
    m = re.search(r"summarize.+?:\s*(.+)", prompt, re.I | re.S)
    text = m.group(1).strip() if m else prompt
    text = text.strip('[]"\'')
    
    # Fast-path fallback direct to local LLM for clean summary generation
    system_prompt = (
        "Summarize the following text in exactly one clear sentence. "
        "Do not include any introductory or meta prose. Output only the summary sentence."
    )
    
    local_summary = generate_local(text, system_prompt=system_prompt)
    
    # Guardrails to ensure output conforms to 'exactly one sentence'
    sentences = split_sentences(local_summary)
    if sentences:
        best = sentences[0]
        if not best.endswith("."):
            best += "."
        return best
        
    return local_summary if local_summary else text[:100]