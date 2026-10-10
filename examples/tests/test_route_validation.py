"""The router computes eligibility before the model and falls back, never guesses."""
from __future__ import annotations

import pytest

from examples.contracts import RiskClass
from examples.patterns.route_validation import DeterministicRouter, Route, RouteProposal

ROUTES = (
    Route("policy-explanation", "mortgage.policy.explain", RiskClass.R1),
    Route("document-validation", "mortgage.document.validate", RiskClass.R2),
    Route("income-verification", "mortgage.income.verify", RiskClass.R2, healthy=False),
    Route("case-admin", "mortgage.case.admin", RiskClass.R4),
)
ALLOWED = frozenset({
    "mortgage.policy.explain", "mortgage.document.validate", "mortgage.income.verify",
})
router = DeterministicRouter(ROUTES, fallback="human-triage")


def classifier(route: str, confidence: float = 0.95):
    seen: list[tuple[str, ...]] = []

    async def classify(request, names):
        seen.append(names)
        return RouteProposal(route, confidence, "intent matched")

    return classify, seen


async def test_the_model_sees_only_the_eligible_set():
    classify, seen = classifier("document-validation")
    decision = await router.route(
        "Is the second pay statement valid?", classify, ALLOWED, RiskClass.R2
    )
    # case-admin is outside the envelope; income-verification is unhealthy;
    # policy-explanation's ceiling (R1) is below the request's R2.
    assert seen == [("document-validation",)]
    assert decision.route == "document-validation" and not decision.fallback


async def test_selecting_a_privileged_route_does_not_grant_it():
    classify, _ = classifier("case-admin")
    decision = await router.route("Close the case.", classify, ALLOWED, RiskClass.R1)
    assert decision.route == "human-triage"
    assert decision.reason == "not_eligible"


async def test_low_confidence_falls_back_instead_of_guessing():
    classify, _ = classifier("policy-explanation", confidence=0.4)
    decision = await router.route("Hmm?", classify, ALLOWED, RiskClass.R1)
    assert (decision.route, decision.fallback, decision.reason) == (
        "human-triage", True, "low_confidence"
    )


async def test_an_empty_eligible_set_never_reaches_the_model():
    classify, seen = classifier("policy-explanation")
    decision = await router.route("Anything", classify, frozenset(), RiskClass.R0)
    assert seen == [] and decision.reason == "no_eligible_route"


def test_a_bare_number_is_not_a_risk_class():
    with pytest.raises(TypeError, match="R0-R4"):
        Route("bad", "x", 4)
