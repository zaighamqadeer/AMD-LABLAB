import re
import itertools
from fireworks_client import call_fireworks

KNOWN_NAMES = ["Sam", "Jo", "Lee", "Alice", "Bob", "Carol", "John", "Maria", "Alex", "Jordan"]
KNOWN_PETS = ["cat", "dog", "bird", "fish", "rabbit", "hamster"]

def solve_logic(prompt: str) -> str:
    low = prompt.lower()

    names = [n for n in KNOWN_NAMES if re.search(rf"\b{n}\b", prompt)]
    pets = []
    for p in KNOWN_PETS:
        if re.search(rf"\b{p}\b", low) and p not in pets:
            pets.append(p)

    if len(names) >= 3 and len(pets) >= 3:
        constraints = []
        # Check "does not own" FIRST so it isn't misread as a positive match,
        # and do NOT use re.I here (case-insensitivity lets [A-Z] match
        # lowercase letters too, corrupting name capture).
        for sent in prompt.split("."):
            neg = re.search(r"([A-Z][a-z]+)\s+does not own the (\w+)", sent)
            if neg:
                constraints.append((neg.group(1), "!=", neg.group(2).lower()))
                continue
            pos = re.search(r"([A-Z][a-z]+)\s+owns the (\w+)", sent)
            if pos:
                constraints.append((pos.group(1), "==", pos.group(2).lower()))

        for perm in itertools.permutations(pets, len(names)):
            assignment = dict(zip(names, perm))
            ok = True
            for person, op, pet in constraints:
                if person not in assignment:
                    continue
                if op == "==" and assignment[person] != pet:
                    ok = False; break
                if op == "!=" and assignment[person] == pet:
                    ok = False; break
            if ok:
                # Figure out which pet is actually being asked about
                asked_pet = None
                q = re.search(r"who owns the (\w+)", low)
                if q:
                    asked_pet = q.group(1)
                target_pet = asked_pet if asked_pet in pets else "cat"
                for person, pet in assignment.items():
                    if pet == target_pet:
                        return f"{person} owns the {target_pet}."
                return "Solution resolved."

    # CRITICAL FALLBACK: Pass complex relational problems to Fireworks
    anti_yap_prompt = prompt + "\n\nCRITICAL INSTRUCTION: Output ONLY the final answer as a full sentence, e.g. 'Name owns the item.' Do not explain your reasoning."
    api_response = call_fireworks(anti_yap_prompt, max_tokens=20)
    return api_response if api_response else "Constraint logic error."