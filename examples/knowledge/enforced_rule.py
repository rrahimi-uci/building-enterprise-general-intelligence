"""A policy rule enforced at the effect boundary, not quoted in a prompt.

The difference between a rule an agent reads and a rule the platform enforces is
the difference between a system that explains its policy and one that follows
it. Enforcement happens where intent becomes action -- after the model has
decided, before anything commits.

The three-valued rules here match the reference evaluator in Policy Logic Forge
[R48] (utils/feel.py, commit c22dc450, MIT): a missing input is unknown, never
false, and unknown refuses. The ``pinned`` region is the book's own: a control
point evaluates only the rules of the knowledge release its run pinned.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# --8<-- example:start


class PolicyViolation(Exception):
    """Refused by an enforceable rule. Carries the rule that refused it."""

    def __init__(self, message: str, rule_id: str, source_section: str) -> None:
        super().__init__(message)
        self.rule_id = rule_id
        self.source_section = source_section


class UnknownUnderPolicy(Exception):
    """A required input was missing, so the rule could not be evaluated.

    Refusing here is the whole point: a rule check that treats 'unknown' as
    'permitted' is not a control. The three-valued reading -- true, false,
    unknown -- is what keeps a missing field from silently authorizing an effect.
    """


@dataclass(frozen=True)
class EnforcedRule:
    rule: object

    def _satisfied(self, facts: dict) -> bool:
        """Kleene AND: one false condition decides; otherwise a missing one is unknown."""
        missing = []
        for predicate in self.rule.conditions:
            if predicate.variable not in facts:
                missing.append(predicate.variable)
                continue
            value = facts[predicate.variable]
            checks = {">": value > predicate.value, ">=": value >= predicate.value,
                      "<": value < predicate.value, "<=": value <= predicate.value,
                      "=": value == predicate.value, "!=": value != predicate.value}
            if not checks[predicate.operator]:
                return False
        if missing:
            raise UnknownUnderPolicy(
                f"{self.rule.rule_id} needs {', '.join(missing)}, which was not supplied"
            )
        return True

    def enforce(self, facts: dict, *, jurisdiction: str, on_date: str) -> None:
        """Raise if this effect may not proceed. Silence means permitted."""
        if not self.rule.applies_in(jurisdiction, on_date):
            return  # out of scope: this rule has nothing to say here
        if not self._satisfied(facts):
            return  # conditions not met: the rule does not fire
        required = self.rule.outcome
        actual = facts.get(required.variable)
        if actual != required.value:
            raise PolicyViolation(
                f"{self.rule.rule_id} requires {required.variable}="
                f"{required.value}, got {actual!r}",
                rule_id=self.rule.rule_id,
                source_section=self.rule.source.section_id,
            )


def guarded_dispatch(effect, facts: dict, rules, *, jurisdiction: str, on_date: str):
    """Every enforced rule must pass before the effect is allowed to run."""
    for rule in rules:
        rule.enforce(facts, jurisdiction=jurisdiction, on_date=on_date)
    return effect()


# --8<-- example:end


# --8<-- region:pinned
ReleaseStatus = Literal["draft", "certified", "approved", "active", "deprecated", "revoked"]


class ReleaseNotEvaluable(Exception):
    """The run's pin names a release no control point may evaluate."""


@dataclass(frozen=True)
class PinnedRelease:
    """One knowledge release as a run pinned it at admission (RunManifest)."""

    stream: str
    digest: str
    status: ReleaseStatus
    rules: tuple[EnforcedRule, ...]


def rules_for(pins: dict[str, PinnedRelease], stream: str) -> tuple[EnforcedRule, ...]:
    """The rules this run may evaluate: from its own pin, never from 'current'.

    Only an activated release is evaluable. Deprecated still serves the run that
    pinned it; revoked serves nobody; anything not yet active was never released.
    """
    pin = pins.get(stream)
    if pin is None:
        raise UnknownUnderPolicy(f"the run pinned no release of {stream}")
    if pin.status not in ("active", "deprecated"):
        raise ReleaseNotEvaluable(f"{stream}@{pin.digest[:12]} is {pin.status}")
    return pin.rules


def pinned_dispatch(effect, facts: dict, pins: dict[str, PinnedRelease], stream: str,
                    *, jurisdiction: str, on_date: str):
    """Enforce the pinned release; every outcome cites the digest it was decided on."""
    rules = rules_for(pins, stream)
    try:
        result = guarded_dispatch(effect, facts, rules,
                                  jurisdiction=jurisdiction, on_date=on_date)
    except PolicyViolation as refusal:
        refusal.release = pins[stream].digest
        raise
    return result, pins[stream].digest
# --8<-- endregion:pinned
