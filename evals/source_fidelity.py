def check_source_fidelity(source_text: str, claim: str) -> dict:
    """Simple v0.1 source support check.

    This prototype uses basic keyword overlap.
    Future versions should use semantic similarity and human labels.
    """
    source_words = set(source_text.lower().replace(".", "").replace(",", "").split())
    claim_words = set(claim.lower().replace(".", "").replace(",", "").split())

    if not claim_words:
        return {
            "status": "unsupported",
            "score": 0.0,
            "explanation": "Empty claim cannot be supported.",
        }

    overlap = claim_words.intersection(source_words)
    score = len(overlap) / len(claim_words)

    if score >= 0.45:
        status = "supported"
        explanation = "Claim has enough word overlap with the source for v0.1."
    else:
        status = "unsupported"
        explanation = "Claim has low word overlap with the source and needs review."

    return {
        "status": status,
        "score": round(score, 2),
        "explanation": explanation,
    }
