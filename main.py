import json
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from router import route_task
from local_llm import generate_local
from fireworks_client import call_fireworks

# Import your newly optimized solvers
from solvers.sentiment_solver import solve_sentiment
from solvers.ner_solver import solve_ner
from solvers.summarizer import solve_summarization
from solvers.math_solver import solve_math
from solvers.code_solver import solve_code_debug, solve_code_gen
from solvers.logic_solver import solve_logic

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
        category = route["category"]
        target = route["target"]
        
        print(f"-> Task {task_id} routed to {category} ({target})", flush=True)
        
        # 1. API ONLY (Tasks the 0.5B model physically cannot do)
        if target == "fireworks":
            if category == "code_debug":
                answer = solve_code_debug(prompt)
            elif category == "code_gen":
                answer = solve_code_gen(prompt)
            else:
                answer = call_fireworks(prompt, max_tokens=150)
                
        # 2. LOCAL FIRST W/ API ESCALATION (The Token Saver!)
        elif target == "local_escalatable":
            if category == "math":
                answer = solve_math(prompt)
            elif category == "logic":
                answer = solve_logic(prompt)
                
        # 3. ZERO-TOKEN LOCAL ONLY (Tasks the 0.5B model dominates)
        else:
            if category == "sentiment":
                answer = solve_sentiment(prompt)
            elif category == "ner":
                answer = solve_ner(prompt)
            elif category == "summarization":
                answer = solve_summarization(prompt)
            else:
                # Factual fallback
                answer = generate_local(prompt, system_prompt="Answer concisely in 1-2 sentences.")
                
        results.append({"task_id": task_id, "answer": answer})
        
    # Write exact schema
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"Successfully processed {len(tasks)} tasks.")

if __name__ == "__main__":
    main()