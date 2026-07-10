import re
from local_llm import generate_local

try:
    import spacy
    _nlp = None
    def get_nlp():
        global _nlp
        if _nlp is None:
            try:
                _nlp = spacy.load("en_core_web_sm")
            except:
                _nlp = None
        return _nlp
except ImportError:
    def get_nlp(): return None

# Words that strongly signal "this is a company/organization", used to correct
# spaCy's common mistake of tagging unfamiliar brand names as PERSON.
ORG_SIGNAL_WORDS = {
    "ai", "inc", "inc.", "corp", "corp.", "labs", "llc", "ltd", "ltd.",
    "technologies", "systems", "solutions", "group", "holdings", "co",
    "co.", "company", "enterprises", "industries", "partners"
}

def _looks_like_org(text: str) -> bool:
    tokens = re.findall(r"[A-Za-z]+\.?", text.lower())
    return any(tok in ORG_SIGNAL_WORDS for tok in tokens)

def solve_ner(prompt: str) -> str:
    m = re.search(r"from:\s*(.+)", prompt, re.I | re.S)
    text = m.group(1).strip() if m else prompt.split(":")[-1].strip()

    nlp = get_nlp()
    entities = []
    if nlp:
        doc = nlp(text)
        for ent in doc.ents:
            typ = ent.label_
            if typ in ["PERSON", "ORG", "GPE", "LOC", "DATE", "TIME"]:
                if typ in ["GPE", "LOC"]:
                    typ = "LOCATION"
                elif typ == "ORG":
                    typ = "ORGANIZATION"
                elif typ == "PERSON" and _looks_like_org(ent.text):
                    # spaCy's small model frequently mistags unfamiliar
                    # brand/company names (e.g. "Fireworks AI") as PERSON.
                    typ = "ORGANIZATION"
                entities.append(f"{ent.text} ({typ})")
        if entities:
            return "Entities: " + ", ".join(entities)

    # CRITICAL FALLBACK: Use the local zero-token model to pull missing structured tags
    system_prompt = (
        "Extract all named entities (PERSON, ORGANIZATION, LOCATION, DATE). "
        "Format strictly as: 'Entities: Name (TYPE), Name (TYPE)'."
    )
    return generate_local(text, system_prompt=system_prompt)