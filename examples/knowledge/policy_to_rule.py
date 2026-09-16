"""A policy sentence as a typed, scoped rule that carries its own evidence.

The move from prose to knowledge is not parsing; it is committing to a shape.
A rule that cannot say who it binds, where it applies, what it excludes, and
which sentence it came from is a summary, not a constraint -- and a summary
cannot be enforced, diffed, or audited.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Literal

# --8<-- example:start

Modality = Literal["obligation", "permission", "prohibition"]


@dataclass(frozen=True)
class SourceRef:
    """Where a claim came from, precisely enough to check it again later."""

    document_id: str
    section_id: str
    start_offset: int
    end_offset: int
    source_sha256: str

    def excerpt(self, corpus: dict[str, str]) -> str:
        return corpus[self.document_id][self.start_offset:self.end_offset]


@dataclass(frozen=True)
class Predicate:
    variable: str
    operator: Literal["<", "<=", "=", "!=", ">=", ">"]
    value: Decimal | str | bool


@dataclass(frozen=True)
class Rule:
    rule_id: str
    modality: Modality
    conditions: tuple[Predicate, ...]
    outcome: Predicate
    # Scope is required, not optional. A rule whose applicability is implicit
    # will be applied where it does not belong, which is the most common way a
    # correctly extracted rule still produces a wrong decision.
    jurisdiction: str
    responsible_party: str
    effective_from: str
    source: SourceRef
    supersedes: str | None = None
    exceptions: tuple[str, ...] = field(default_factory=tuple)

    def applies_in(self, jurisdiction: str, on_date: str) -> bool:
        return jurisdiction == self.jurisdiction and on_date >= self.effective_from

    def digest(self) -> str:
        """Identity by content, so two extractions of one sentence agree."""
        payload = "|".join([
            self.modality, self.jurisdiction, self.responsible_party,
            *(f"{p.variable}{p.operator}{p.value}" for p in self.conditions),
            f"{self.outcome.variable}{self.outcome.operator}{self.outcome.value}",
        ])
        return hashlib.sha256(payload.encode()).hexdigest()[:16]


# --8<-- example:end
