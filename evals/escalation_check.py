ESCALATION_TERMS = [
    "legal",
    "medical",
    "financial",
    "visa",
    "work authorization",
    "safety",
    "security",
    "high-stakes",
    "submit application",
]


def check_escalation_needed(claim: str) -> dict:
    claim_lower = claim.lower()

    terms = [term for term in ESCALATION_TERMS if term in claim_lower]

    if terms:
        return {
            "status": "needs_human_review",
            "terms": terms,
            "explanation": "Claim touches a high-stakes area where human verification is recommended.",
        }

    return {
        "status": "no_escalation_needed",
        "terms": [],
        "explanation": "No escalation trigger found by v0.1 heuristic.",
    }
