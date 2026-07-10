import json
import os
from router import route_task
from local_llm import generate_local
from fireworks_client import call_fireworks

# Importing from your 'solvers' directory
from solvers.sentiment_solver import solve_sentiment
from solvers.ner_solver import solve_ner
from solvers.summarizer import solve_summarization
from solvers.math_solver import solve_math
from solvers.code_solver import solve_code_debug, solve_code_gen
from solvers.logic_solver import solve_logic
from dotenv import load_dotenv
load_dotenv()
# Hackathon expects /input and /output, but we allow local paths for Codespace testing
INPUT_PATH = os.environ.get("INPUT_PATH", "/input/tasks.json")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/output/results.json")

def main():
    if not os.path.exists(INPUT_PATH):
        print(f"Error: Could not find {INPUT_PATH}")
        return
        
    with open(INPUT_PATH, "r") as f:
        tasks = json.load(f)
        
    results = []
    
    for task in tasks:
        task_id = task["task_id"]
        prompt = task["prompt"]
        
        route = route_task(prompt)
        answer = ""
        category = route["category"]
        target = route["target"]
        
        if target == "fireworks":
            if category == "math":
                answer = solve_math(prompt)
            elif category == "code_debug":
                answer = solve_code_debug(prompt)
            elif category == "code_gen":
                answer = solve_code_gen(prompt)
            elif category == "logic":
                answer = solve_logic(prompt)
            else:
                answer = call_fireworks(prompt)
        else:
            if category == "sentiment":
                answer = solve_sentiment(prompt)
            elif category == "ner":
                answer = solve_ner(prompt)
            elif category == "summarization":
                answer = solve_summarization(prompt)
            else:
                answer = generate_local(prompt, "Be concise and answer the prompt directly.")
                
        results.append({"task_id": task_id, "answer": answer})
        
    # Ensure output directory exists and write results
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Successfully processed {len(tasks)} tasks.")

if __name__ == "__main__":
    main()