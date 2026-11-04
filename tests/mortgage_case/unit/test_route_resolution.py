from decimal import Decimal

import pytest

from mortgage_case.domain.errors import ProposalRejected
from mortgage_case.platform.enterprise import RouteDecision
from mortgage_case.platform.route_resolution import resolve_route


def _candidate(route: str, confidence: str, *, eligible: bool = True) -> RouteDecision:
    return RouteDecision(
        route=route,
        reason_code=f"{route.upper()}_REASON",
        confidence=Decimal(confidence),
        eligible=eligible,
        owner=f"{route}-specialist",
    )


def test_resolve_route_selects_unique_highest_confidence_candidate():
    lower = _candidate("income", "0.72")
    winner = _candidate("property", "0.91")

    assert resolve_route((lower, winner)) is winner


def test_resolve_route_ignores_ineligible_candidates():
    eligible = _candidate("income", "0.61")
    ineligible = _candidate("property", "0.99", eligible=False)

    assert resolve_route((ineligible, eligible)) is eligible


@pytest.mark.parametrize("candidates", [(), (_candidate("income", "0.8", eligible=False),)])
def test_resolve_route_rejects_when_no_candidate_is_eligible(candidates):
    with pytest.raises(ProposalRejected) as raised:
        resolve_route(candidates)

    assert raised.value.code == "NO_ELIGIBLE_ROUTE"


def test_resolve_route_rejects_tied_top_confidence():
    candidates = (
        _candidate("income", "0.9"),
        _candidate("property", "0.9"),
        _candidate("policy", "0.7"),
    )

    with pytest.raises(ProposalRejected) as raised:
        resolve_route(candidates)

    assert raised.value.code == "ROUTE_AMBIGUOUS"


@pytest.mark.parametrize("confidence", ["-0.1", "1.01"])
def test_resolve_route_rejects_confidence_outside_probability_range(confidence):
    with pytest.raises(ProposalRejected) as raised:
        resolve_route((_candidate("income", confidence),))

    assert raised.value.code == "ROUTE_SCORE_INVALID"
