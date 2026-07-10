import os
import re
from llama_cpp import Llama

MODEL_FILENAME = "Qwen3.5-0.8B-Q4_K_M.gguf"

_candidates = [
    f"./models/{MODEL_FILENAME}",
    f"/app/models/{MODEL_FILENAME}",
]
MODEL_PATH = next((p for p in _candidates if os.path.exists(p)), _candidates[-1])

_model = None


def get_local_model():
    global _model
    if _model is None:
        try:
            print(f"[local_llm] Loading {MODEL_PATH} via llama.cpp...", flush=True)
            _model = Llama(
                model_path=MODEL_PATH,
                n_ctx=512,
                n_threads=2,
                verbose=False,
            )
        except Exception as e:
            print(f"[local_llm] Critical failure loading GGUF: {e}", flush=True)
            return None
    return _model


def _clean_output(text: str) -> str:
    if not text:
        return text
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)
    text = re.sub(r"</?think>", "", text)
    return text.strip()


def generate_local(prompt: str, system_prompt="You are a helpful, precise assistant.") -> str:
    llm = get_local_model()
    if not llm:
        return "Error: Local model unavailable."

    formatted_prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"

    response = llm(
        formatted_prompt,
        max_tokens=100,
        stop=["<|im_end|>"],
        temperature=0.0,
    )
    raw = response["choices"][0]["text"].strip()
    return _clean_output(raw)