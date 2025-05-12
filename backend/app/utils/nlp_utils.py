# Original risk keywords from the NLP setup
RISK_KEYWORDS = {
    "indemnification": ["indemnify", "hold harmless"],
    "termination": ["terminate", "expiry"],
    "liability": ["liability", "damages"],
    "confidentiality": ["confidential", "non-disclosure"]
}

# Original ambiguous terms list from identify_legal_risks()
AMBIGUOUS_TERMS = [
    "reasonable",
    "material adverse effect", 
    "sole discretion"
]