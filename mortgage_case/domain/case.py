"""Canonical synthetic mortgage case and document lineage contracts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .ids import validate_case_id


SYNTHETIC_NOTICE = "SYNTHETIC TRAINING DATA — NOT FOR CREDIT DECISIONS"


class SyntheticDocument(BaseModel):
    """A document reference; raw bytes never enter the model-facing contract."""

    model_config = ConfigDict(extra="forbid")

    document_id: str = Field(pattern=r"^[A-Z0-9-]+$")
    kind: str = Field(min_length=1)
    status: Literal["available", "missing", "unavailable"]
    source_revision: str = Field(min_length=1)
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


class MortgageCase(BaseModel):
    """Synthetic intake facts shared by every cumulative checkpoint."""

    model_config = ConfigDict(extra="forbid")

    synthetic_notice: Literal[SYNTHETIC_NOTICE]
    tenant_id: str = Field(min_length=1)
    case_id: str = Field(pattern=r"^MORT-\d{4}-\d{6}$")
    case_version: int = Field(default=1, ge=1)
    applicant_token: str = Field(pattern=r"^applicant-[0-9]{6}$")
    applicant_display_name: str = Field(min_length=1)
    property_address: str = Field(min_length=1)
    purpose: Literal["mortgage_pre_underwriting_review"]
    purchase_price: str = Field(pattern=r"^USD [0-9]+\.[0-9]{2}$")
    requested_principal: str = Field(pattern=r"^USD [0-9]+\.[0-9]{2}$")
    documents: tuple[SyntheticDocument, ...] = Field(min_length=1)

    @field_validator("case_id")
    @classmethod
    def case_id_is_canonical(cls, value: str) -> str:
        return validate_case_id(value)

    @property
    def available_documents(self) -> tuple[SyntheticDocument, ...]:
        """Return only references that are available to the baseline."""

        return tuple(document for document in self.documents if document.status == "available")

    @property
    def available_document_ids(self) -> tuple[str, ...]:
        return tuple(document.document_id for document in self.available_documents)


def load_anchor_case() -> MortgageCase:
    """Load the immutable anchor fixture from the package."""

    fixture = Path(__file__).parents[1] / "fixtures" / "case_000184.json"
    return MortgageCase.model_validate(json.loads(fixture.read_text(encoding="utf-8")))
