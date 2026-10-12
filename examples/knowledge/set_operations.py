"""Union, intersection, difference and contradiction over two rule sets.

An enterprise never has one knowledge base. It has a regulator's and its own, or
last quarter's and this quarter's. Agents have to operate across them, and that
needs defined operations rather than a merge that loses the argument.

Two properties this encodes, both learned the hard way:

* Union is not merge. Combining without keeping each rule's origin destroys the
  only information that can later resolve a conflict.
* A contradiction is a result, not an error. It is a finding about the
  organization, and the architecture's job is to surface it with evidence, not
  to quietly pick a winner.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# --8<-- example:start


@dataclass(frozen=True)
class Attributed:
    """A rule together with every source that asserts it."""

    rule: object
    sources: tuple[str, ...]
    original_ids: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Contradiction:
    """Both sides preserved. Resolution is a human decision, not a merge rule."""

    subject: str
    left: object
    right: object
    left_source: str
    right_source: str
    reason: str


def _key(rule) -> str:
    """Rules align by content, so independent extractions of one policy match."""
    return rule.digest()


def _subject(rule) -> tuple[str, str, str]:
    """What a rule is *about*: the same subject is what makes a clash possible."""
    return (rule.outcome.variable, rule.jurisdiction,
            tuple(sorted((p.variable, p.operator, p.value) for p in rule.conditions)))


def union(left: dict[str, object], right: dict[str, object]) -> list[Attributed]:
    """Every distinct rule, each carrying the sources that assert it."""
    names = list(left) + [n for n in right if n not in left]
    by_key: dict[str, Attributed] = {}
    for source in names:
        for rule in (left.get(source) or right.get(source)):
            key = _key(rule)
            existing = by_key.get(key)
            if existing is None:
                by_key[key] = Attributed(rule, (source,), {source: rule.rule_id})
            else:
                by_key[key] = Attributed(
                    existing.rule, existing.sources + (source,),
                    {**existing.original_ids, source: rule.rule_id},
                )
    return list(by_key.values())


def intersection(left: dict[str, object], right: dict[str, object]) -> list[Attributed]:
    """Rules both sources assert -- corroborated, not yet verified or authorized."""
    both = {s for s in left} | {s for s in right}
    return [a for a in union(left, right) if len(set(a.sources)) == len(both)]


def difference(left: dict[str, object], right: dict[str, object]) -> list[Attributed]:
    """Rules only the left source asserts -- scope-dependent, not yet safe."""
    right_keys = {_key(r) for rules in right.values() for r in rules}
    name = next(iter(left))
    return [Attributed(r, (name,), {name: r.rule_id})
            for r in left[name] if _key(r) not in right_keys]


def contradictions(left: dict[str, object], right: dict[str, object]) -> list[Contradiction]:
    """Rule pairs about the same subject that cannot both be satisfied."""
    left_name, right_name = next(iter(left)), next(iter(right))
    found = []
    for a in left[left_name]:
        for b in right[right_name]:
            if _subject(a) != _subject(b):
                continue
            if a.outcome.value != b.outcome.value or a.modality != b.modality:
                found.append(Contradiction(
                    subject=a.outcome.variable, left=a, right=b,
                    left_source=left_name, right_source=right_name,
                    reason=(f"{left_name} requires {a.outcome.variable}="
                            f"{a.outcome.value} ({a.modality}); {right_name} requires "
                            f"{b.outcome.value} ({b.modality}) under the same conditions"),
                ))
    return found


# --8<-- example:end
