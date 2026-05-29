OVERCONFIDENCE_MARKERS = [
    "definitely",
    "guaranteed",
    "always",
    "never",
    "certainly",
    "no doubt",
    "100%",
    "must",
]


def check_overconfidence(claim: str) -> dict:
    claim_lower = claim.lower()

    markers = [marker for marker in OVERCONFIDENCE_MARKERS if marker in claim_lower]

    if markers:
        return {
            "status": "overconfident",
            "markers": markers,
            "explanation": "Claim uses strong certainty language that may need calibration.",
        }

    return {
        "status": "calibrated",
        "markers": [],
        "explanation": "No obvious overconfidence markers found.",
    }
