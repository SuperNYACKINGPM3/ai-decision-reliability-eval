import json
from datetime import datetime
from pathlib import Path

from evals.source_fidelity import check_source_fidelity
from evals.contradiction_check import check_contradiction
from evals.confidence_check import check_overconfidence
from evals.escalation_check import check_escalation_needed


DATA_DIR = Path("data")
REPORTS_DIR = Path("reports")


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


def summarize_verdicts(results: list[dict]) -> dict[str, int]:
    summary = {}

    for result in results:
        verdict = result["final_verdict"]
        summary[verdict] = summary.get(verdict, 0) + 1

    return summary


def format_detail_list(items: list | tuple) -> str:
    if not items:
        return "None"

    return ", ".join(str(item) for item in items)


def generate_markdown_report(results: list[dict]) -> str:
    generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    summary = summarize_verdicts(results)

    lines = [
        "# AI Decision Reliability Audit Report",
        "",
        f"Generated: {generated_at}",
        "",
        "## Summary",
        "",
        "| Verdict | Count |",
        "|---|---:|",
    ]

    for verdict, count in sorted(summary.items()):
        lines.append(f"| {verdict} | {count} |")

    lines.extend([
        "",
        "## Evaluated Claims",
        "",
    ])

    for index, result in enumerate(results, start=1):
        source_fidelity = result["source_fidelity"]
        contradiction = result["contradiction"]
        confidence = result["confidence"]
        escalation = result["escalation"]

        lines.extend([
            f"### Claim {index}: {result['final_verdict']}",
            "",
            f"**Source ID:** `{result['source_id']}`",
            "",
            f"> {result['claim']}",
            "",
            "| Check | Status | Notes |",
            "|---|---|---|",
            f"| Source fidelity | {source_fidelity['status']} | Score: {source_fidelity.get('score', 'n/a')}. {source_fidelity['explanation']} |",
            f"| Contradiction | {contradiction['status']} | Pairs: {format_detail_list(contradiction.get('pairs', []))}. {contradiction['explanation']} |",
            f"| Confidence | {confidence['status']} | Markers: {format_detail_list(confidence.get('markers', []))}. {confidence['explanation']} |",
            f"| Escalation | {escalation['status']} | Terms: {format_detail_list(escalation.get('terms', []))}. {escalation['explanation']} |",
            "",
        ])

    lines.extend([
        "## Method Note",
        "",
        "Version 0.1 uses simple rule-based heuristics. It is designed as an inspectable prototype, not a production-grade evaluator.",
        "",
        "## Next Improvements",
        "",
        "- Add semantic source-support scoring.",
        "- Add model-assisted judging with human review labels.",
        "- Add a larger benchmark dataset.",
        "- Export both Markdown and JSON audit artifacts.",
    ])

    return "\n".join(lines) + "\n"


def save_markdown_report(results: list[dict]) -> Path:
    REPORTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_DIR / f"audit_report_{timestamp}.md"
    report_path.write_text(generate_markdown_report(results), encoding="utf-8")
    return report_path


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

    report_path = save_markdown_report(results)

    print(json.dumps(results, indent=2))
    print(f"\nMarkdown report saved to: {report_path}")


if __name__ == "__main__":
    main()
