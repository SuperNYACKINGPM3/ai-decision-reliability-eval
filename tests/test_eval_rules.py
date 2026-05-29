from evals.confidence_check import check_overconfidence
from evals.escalation_check import check_escalation_needed


def test_overconfidence_detects_definitely():
    result = check_overconfidence("This is definitely true.")
    assert result["status"] == "overconfident"


def test_escalation_detects_work_authorization():
    result = check_escalation_needed("Work authorization should be verified.")
    assert result["status"] == "needs_human_review"
