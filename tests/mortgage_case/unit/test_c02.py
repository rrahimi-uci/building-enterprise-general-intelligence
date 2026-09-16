from __future__ import annotations

from decimal import Decimal

import pytest
from pydantic import ValidationError

from mortgage_case.domain.decisions import AgentProposal
from mortgage_case.domain.errors import MortgageCaseError
from mortgage_case.domain.money import calculate_dti, calculate_ltv, parse_usd_amount
from mortgage_case.stages.c02_deterministic_shell import run


def test_ltv_is_decimal_and_recomputable():
    result = calculate_ltv(
        Decimal("500000.00"), Decimal("625000.00"), evidence_refs=("APP-000184", "PUR-000184")
    )
    assert result.value == Decimal("0.8000")
    assert result.inputs == {"requested_principal": "500000.00", "purchase_price": "625000.00"}
    assert result.formula_version == "1.0.0"


def test_dti_is_decimal_and_recomputable():
    result = calculate_dti(
        Decimal("4200.00"), Decimal("12500.00"), evidence_refs=("PAY-000184-01",)
    )
    assert result.value == Decimal("0.3360")


def test_float_inputs_are_rejected():
    with pytest.raises(MortgageCaseError, match="FLOAT_INPUT_REJECTED"):
        calculate_ltv(500000.0, Decimal("625000.00"), evidence_refs=())


def test_fixture_money_is_parsed_without_float_round_trip():
    assert parse_usd_amount("USD 625000.00", "purchase_price") == Decimal("625000.00")
    with pytest.raises(MortgageCaseError, match="INVALID_MONEY"):
        parse_usd_amount("625000.00", "purchase_price")


def test_stale_proposal_is_refused_before_dispatch():
    report = run("stale_case_version")
    assert report.status == "refused"
    assert report.failures == ("STALE_CASE_VERSION",)


def test_model_cannot_add_a_lending_decision_to_the_platform_contract():
    with pytest.raises(ValidationError):
        AgentProposal(
            case_id="MORT-2026-000184",
            case_version=1,
            summary="unsafe",
            lending_decision="approve",  # type: ignore[call-arg]
        )


def test_unsupported_lending_decision_scenario_is_refused():
    report = run("unsupported_lending_decision")
    assert report.status == "refused"
    assert report.failures == ("ValidationError",)
