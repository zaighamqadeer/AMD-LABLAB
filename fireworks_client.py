import os
from openai import OpenAI

def get_fireworks_config():
    api_key = os.environ.get("FIREWORKS_API_KEY")
    base_url = os.environ.get("FIREWORKS_BASE_URL")
    allowed = os.environ.get("ALLOWED_MODELS", "")
    models = [m.strip() for m in allowed.split(",") if m.strip()]
    return api_key, base_url, models

def call_fireworks(prompt: str, max_tokens=256, system_prompt="Be precise and concise.") -> str:
    api_key, base_url, models = get_fireworks_config()
    if not api_key or not base_url or not models:
        return None
    
    model_id = models[0]
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key, base_url=base_url)
        resp = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.0,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[fireworks] error: {e}", flush=True)
        return None