CONTRADICTION_PAIRS = [
    ("may", "must"),
    ("optional", "required"),
    ("closed", "open"),
    ("july", "may"),
    ("future", "current"),
    ("not", "is"),
]


def check_contradiction(source_text: str, claim: str) -> dict:
    """Simple v0.1 contradiction heuristic.

    Flags known contradiction pairs when one appears in the source
    and the conflicting term appears in the claim.
    """
    source_lower = source_text.lower()
    claim_lower = claim.lower()

    detected_pairs = []

    for source_term, claim_term in CONTRADICTION_PAIRS:
        if source_term in source_lower and claim_term in claim_lower:
            detected_pairs.append((source_term, claim_term))

    if detected_pairs:
        return {
            "status": "contradicted",
            "pairs": detected_pairs,
            "explanation": "Potential contradiction detected by keyword-pair heuristic.",
        }

    return {
        "status": "no_clear_contradiction",
        "pairs": [],
        "explanation": "No contradiction detected by v0.1 heuristic.",
    }
