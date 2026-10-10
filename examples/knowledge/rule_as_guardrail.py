"""A policy rule enforced at the effect boundary, not quoted in a prompt.

The difference between a rule an agent reads and a rule the platform enforces is
the difference between a system that explains its policy and one that follows
it. Enforcement happens where intent becomes action -- after the model has
decided, before anything commits.
"""
from __future__ import annotations

from dataclasses import dataclass

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
        for predicate in self.rule.conditions:
            if predicate.variable not in facts:
                raise UnknownUnderPolicy(
                    f"{self.rule.rule_id} needs {predicate.variable}, which was not supplied"
                )
            value = facts[predicate.variable]
            checks = {">": value > predicate.value, ">=": value >= predicate.value,
                      "<": value < predicate.value, "<=": value <= predicate.value,
                      "=": value == predicate.value, "!=": value != predicate.value}
            if not checks[predicate.operator]:
                return False
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
