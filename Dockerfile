FROM python:3.10-slim

# Install wget and build tools for llama-cpp-python
RUN apt-get update && apt-get install -y wget build-essential gcc g++ && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Download the quantized Qwen 0.5B model directly into the image
RUN mkdir -p /app/models && \
    wget https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf -O /app/models/qwen2.5-0.5b-instruct-q4_k_m.gguf

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy your codebase
COPY . .

# Run main script
CMD ["python", "main.py"]