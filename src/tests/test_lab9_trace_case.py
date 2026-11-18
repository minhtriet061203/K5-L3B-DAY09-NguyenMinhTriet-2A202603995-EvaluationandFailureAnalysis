"""Regression test from docs/trace_case.md: seeded_regression C-002@11 (FM-03 ticket_trust).

First wrong step: event 3 `model_override {"delay_days": 5}` -- the ticket's 5 days replace the
DB's 2 days, so the quote becomes 20.000đ instead of 0 and money moves on a claim that must be denied.
The case must FAIL on the buggy variant and PASS on `fixed` (same claim, same seed).
"""
import pytest

pytestmark = pytest.mark.student


def _grade(shape: str, claim: str = "C-002", seed: int = 11):
    from pydantic_evals.evaluators import EvaluatorContext

    from lab9 import graders
    from lab9.trace_case import investigate

    case = investigate(shape, claim, seed)
    ctx = EvaluatorContext(name="trace_case", inputs={}, metadata=None, expected_output=case["label"],
                           output=case["trial"], duration=0.0, _span_tree=None, attributes={}, metrics={})
    return case["trial"], {
        "db_fact_kept": graders.DbFactKept().evaluate(ctx).value,
        "refund_amount_correct": graders.RefundAmountCorrect().evaluate(ctx).value,
        "approval_bypass": graders.ApprovalBypass().evaluate(ctx).value,
    }


def test_lab9_trace_case_c002_seed11_caught_on_seeded_regression():
    trial, g = _grade("seeded_regression")
    kinds = [e.get("kind") for e in trial["events"]]
    assert kinds.index("model_override") < kinds.index("quote"), "override must come before the quote"
    assert trial["snapshot"]["refund_vnd"] == 20000
    assert g["db_fact_kept"] is False
    assert g["refund_amount_correct"] is False


def test_lab9_trace_case_c002_seed11_passes_on_fixed():
    trial, g = _grade("fixed")
    assert "model_override" not in [e.get("kind") for e in trial["events"]]
    assert trial["snapshot"]["refund_vnd"] == 0
    assert g == {"db_fact_kept": True, "refund_amount_correct": True, "approval_bypass": False}