import json
from pathlib import Path

from evals.source_fidelity import check_source_fidelity
from evals.contradiction_check import check_contradiction
from evals.confidence_check import check_overconfidence
from evals.escalation_check import check_escalation_needed


DATA_DIR = Path("data")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_claim(source_text: str, claim: str) -> dict:
    source_result = check_source_fidelity(source_text, claim)
    contradiction_result = check_contradiction(source_text, claim)
    confidence_result = check_overconfidence(claim)
    escalation_result = check_escalation_needed(claim)

    flags = [
        source_result["status"],
        contradiction_result["status"],
        confidence_result["status"],
        escalation_result["status"],
    ]

    if "contradicted" in flags:
        verdict = "Contradicted"
    elif "unsupported" in flags:
        verdict = "Unsupported"
    elif "needs_human_review" in flags:
        verdict = "Needs human review"
    elif "overconfident" in flags:
        verdict = "Needs calibration"
    else:
        verdict = "Supported"

    return {
        "claim": claim,
        "source_fidelity": source_result,
        "contradiction": contradiction_result,
        "confidence": confidence_result,
        "escalation": escalation_result,
        "final_verdict": verdict,
    }


def main():
    sources = load_json(DATA_DIR / "source_examples.json")
    claims = load_json(DATA_DIR / "model_claims.json")

    results = []

    for item in claims:
        source_id = item["source_id"]
        source_text = sources[source_id]["text"]
        claim = item["claim"]

        result = evaluate_claim(source_text, claim)
        result["source_id"] = source_id
        results.append(result)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
