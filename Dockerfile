FROM python:3.10-slim

# Install wget and build tools for llama-cpp-python
RUN apt-get update && apt-get install -y wget build-essential gcc g++ && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Download the quantized Qwen 0.5B model directly into the image
RUN mkdir -p /app/models && \
    wget -O /app/models/Qwen3.5-0.8B-Q4_K_M.gguf https://huggingface.co/unsloth/Qwen3.5-0.8B-GGUF/resolve/main/Qwen3.5-0.8B-Q4_K_M.gguf

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy your codebase
COPY . .

# Run main script
CMD ["python", "main.py"]