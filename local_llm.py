import os
from llama_cpp import Llama

# Dynamically find the NEW Qwen 3.5 model
if os.path.exists("./models/Qwen3.5-0.8B-Q4_K_M.gguf"):
    MODEL_PATH = "./models/Qwen3.5-0.8B-Q4_K_M.gguf"
else:
    MODEL_PATH = "/app/models/Qwen3.5-0.8B-Q4_K_M.gguf"

_model = None

def get_local_model():
    global _model
    if _model is None:
        try:
            print(f"[local_llm] Loading {MODEL_PATH} via llama.cpp...", flush=True)
            _model = Llama(
                model_path=MODEL_PATH,
                n_ctx=512,       # Keep context window small to save RAM
                n_threads=2,     # Maximize the 2 vCPUs
                verbose=False
            )
        except Exception as e:
            print(f"[local_llm] Critical failure loading GGUF: {e}", flush=True)
            return None
    return _model


def generate_local(prompt: str, system_prompt="You are a helpful, precise assistant.") -> str:
    llm = get_local_model()
    if not llm:
        return "Error: Local model unavailable."

    # Qwen/Llama chat formatting
    formatted_prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
    
    response = llm(
        formatted_prompt,
        max_tokens=100, # Keep outputs short
        stop=["<|im_end|>"],
        temperature=0.0
    )
    return response['choices'][0]['text'].strip()