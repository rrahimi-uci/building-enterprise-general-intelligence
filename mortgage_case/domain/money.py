"""Deterministic Decimal calculations for illustrative mortgage evidence."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN

from pydantic import BaseModel, ConfigDict, Field

from .errors import MortgageCaseError


QUANTUM = Decimal("0.0001")


class CalculationResult(BaseModel):
    """A recomputable result, not an eligibility or lending decision."""

    model_config = ConfigDict(extra="forbid")

    calculation_id: str
    formula_id: str
    formula_version: str
    value: Decimal
    inputs: dict[str, str]
    rounding: str = "ROUND_HALF_EVEN"
    evidence_refs: tuple[str, ...] = ()
    unit: str = "ratio"


def parse_usd_amount(value: str, name: str = "amount") -> Decimal:
    """Parse a canonical USD string without introducing binary floats."""

    if not isinstance(value, str) or not value.startswith("USD "):
        raise MortgageCaseError("INVALID_MONEY", f"{name} must use the 'USD 0.00' format")
    return _decimal(value.removeprefix("USD "), name)


def _decimal(value: Decimal | int | str, name: str) -> Decimal:
    if isinstance(value, float):
        raise MortgageCaseError("FLOAT_INPUT_REJECTED", f"{name} must be Decimal or a decimal string")
    try:
        parsed = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise MortgageCaseError("INVALID_DECIMAL", f"{name} is not a decimal value") from exc
    if parsed <= 0:
        raise MortgageCaseError("NON_POSITIVE_INPUT", f"{name} must be positive")
    return parsed


def _ratio_result(
    *,
    calculation_id: str,
    formula_id: str,
    numerator: Decimal | int | str,
    denominator: Decimal | int | str,
    numerator_name: str,
    denominator_name: str,
    evidence_refs: tuple[str, ...],
) -> CalculationResult:
    top = _decimal(numerator, numerator_name)
    bottom = _decimal(denominator, denominator_name)
    return CalculationResult(
        calculation_id=calculation_id,
        formula_id=formula_id,
        formula_version="1.0.0",
        value=(top / bottom).quantize(QUANTUM, rounding=ROUND_HALF_EVEN),
        inputs={numerator_name: str(top), denominator_name: str(bottom)},
        evidence_refs=evidence_refs,
    )


def calculate_ltv(
    principal: Decimal | int | str,
    purchase_price: Decimal | int | str,
    *,
    evidence_refs: tuple[str, ...],
) -> CalculationResult:
    """Calculate an illustrative LTV from already verified inputs."""

    return _ratio_result(
        calculation_id="CALC-LTV-000184",
        formula_id="mortgage.ltv",
        numerator=principal,
        denominator=purchase_price,
        numerator_name="requested_principal",
        denominator_name="purchase_price",
        evidence_refs=evidence_refs,
    )


def calculate_dti(
    monthly_obligations: Decimal | int | str,
    gross_monthly_income: Decimal | int | str,
    *,
    evidence_refs: tuple[str, ...],
) -> CalculationResult:
    """Calculate an illustrative DTI from already verified inputs."""

    return _ratio_result(
        calculation_id="CALC-DTI-000184",
        formula_id="mortgage.dti",
        numerator=monthly_obligations,
        denominator=gross_monthly_income,
        numerator_name="monthly_obligations",
        denominator_name="gross_monthly_income",
        evidence_refs=evidence_refs,
    )
