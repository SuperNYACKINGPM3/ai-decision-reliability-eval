# AI Decision Reliability Eval

This project explores practical evaluation methods for testing whether AI-generated outputs remain faithful to source evidence, avoid unsupported claims, detect contradictions, preserve uncertainty, and escalate high-stakes ambiguity to human judgment.

## Why this matters

Language models can produce fluent, confident answers that appear reliable even when they drift from source material, miss contradictions, or overstate what the evidence supports. This project creates a small, inspectable Python framework for evaluating AI-assisted decision reliability.

## What this evaluates

- **Source fidelity** — Is the claim supported by the source?
- **Contradiction risk** — Does the claim conflict with the source?
- **Overconfidence** — Does the claim sound more certain than the evidence allows?
- **Escalation need** — Should the output recommend human review?
- **Safety risk** — Could the output cause harm if followed?

## Project structure

```text
ai-decision-reliability-eval/
├── README.md
├── main.py
├── requirements.txt
├── data/
│   ├── source_examples.json
│   └── model_claims.json
├── evals/
│   ├── source_fidelity.py
│   ├── contradiction_check.py
│   ├── confidence_check.py
│   └── escalation_check.py
├── reports/
│   └── sample_report.md
└── docs/
    └── research_memo.md
```

## Quick start

```bash
python main.py
```

## Current status

Version `0.1` is a simple rule-based prototype. Future versions can add semantic similarity, model-assisted judging, human review labels, and benchmark datasets.

## Research direction

This project is intended as a small proof artifact for AI safety/evaluation work, especially around source-groundedness, contradiction detection, calibrated uncertainty, and safe human escalation.
