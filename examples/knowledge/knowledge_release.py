"""A knowledge change published only after gates, an independent approval, and a verified bundle.

The objects are compliance knowledge: a requirement from an authoritative
source, the obligation derived from it, and the control that discharges it.
Publication, promotion and rollback are the book's own design; the reference
implementation the chapter follows has no counterpart for them. Synthetic data
only: no real regulation is quoted or paraphrased.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from examples.knowledge.policy_to_rule import SourceRef

# --8<-- example:start
@dataclass(frozen=True)
class Requirement:
    requirement_id: str
    source: SourceRef          # the authoritative span and its document digest


@dataclass(frozen=True)
class Obligation:
    obligation_id: str
    requirement_id: str        # derived from
    subject: str
    scope: str
    effective_from: str


@dataclass(frozen=True)
class Control:
    control_id: str
    obligation_id: str         # discharges
    rule_digest: str           # the enforced rule, identified by content


def discharges(control: Control, objects: tuple) -> tuple[Obligation, Requirement]:
    """A control must trace to the obligation it discharges and that obligation's source."""
    obligation = next(o for o in objects if isinstance(o, Obligation)
                      and o.obligation_id == control.obligation_id)
    requirement = next(o for o in objects if isinstance(o, Requirement)
                       and o.requirement_id == obligation.requirement_id)
    return obligation, requirement


@dataclass(frozen=True)
class Gate:
    name: str
    passed: bool               # no blocking finding; held objects do not fail a gate


@dataclass(frozen=True)
class Approval:
    approver: str
    candidate_digest: str


@dataclass(frozen=True)
class Release:
    stream: str
    version: int
    digest: str
    candidate: Candidate
    approval: Approval


class PublishRefused(Exception):
    """Nothing moved: the previous release is still live."""


# --8<-- region:publish
@dataclass(frozen=True)
class Candidate:
    """One change, frozen at submission. Its digest is what the approver approves."""

    change_id: str
    author: str
    objects: tuple             # Requirement, Obligation, Control records
    pinned_base: str           # the upstream base release it was resolved against
    target_live: str | None    # the live release it expects to replace
    resolver_version: str

    def digest(self) -> str:
        return hashlib.sha256(repr(self).encode("utf-8")).hexdigest()


GATES = ("knowledge-schema", "change-contract", "duplicate-overlap", "grounding",
         "consistency", "regression", "staleness")


@dataclass
class Registry:
    releases: dict[str, Release] = field(default_factory=dict)
    pointers: dict[tuple[str, str], str] = field(default_factory=dict)  # (stream, env)


def publish(registry: Registry, stream: str, env: str, candidate: Candidate,
            gates: list[Gate], approval: Approval) -> Release:
    digest = candidate.digest()
    if digest in registry.releases:            # a retry: no second version
        return registry.releases[digest]
    if {g.name for g in gates if g.passed} != set(GATES):
        raise PublishRefused("gate record incomplete or failed")
    if approval.approver == candidate.author:
        raise PublishRefused("an author cannot approve their own change")
    if approval.candidate_digest != digest:
        raise PublishRefused("the approval names a different candidate")
    if registry.pointers.get((stream, env)) != candidate.target_live:
        raise PublishRefused("stale: the live release moved after submission")
    version = 1 + sum(r.stream == stream for r in registry.releases.values())
    registry.releases[digest] = Release(stream, version, digest, candidate, approval)
    if registry.releases[digest].candidate.digest() != digest:   # verify before activating
        raise PublishRefused("stored bundle does not match its digest")
    registry.pointers[(stream, env)] = digest  # activation: the publication boundary
    return registry.releases[digest]
# --8<-- endregion:publish


# --8<-- region:promote
def promote(registry: Registry, stream: str, source_env: str, target_env: str,
            *, expected: str | None) -> str:
    """Move the identical digest forward; never rebuild for the next environment."""
    digest = registry.pointers[(stream, source_env)]
    if registry.pointers.get((stream, target_env)) != expected:
        raise PublishRefused(f"{target_env} diverged; reconcile before promoting")
    registry.pointers[(stream, target_env)] = digest
    return digest


def rollback(registry: Registry, stream: str, env: str, to_digest: str) -> None:
    """Reassign the pointer to an earlier release. Nothing is rewritten or deleted."""
    prior = registry.releases.get(to_digest)
    if prior is None or prior.stream != stream:
        raise PublishRefused("rollback target is not a release of this stream")
    registry.pointers[(stream, env)] = to_digest


def resolve(registry: Registry, stream: str, env: str) -> str:
    """Admission's one question: which release does a new run pin? Only an active one."""
    if (stream, env) not in registry.pointers:
        raise LookupError(f"no active release of {stream} in {env}")
    return registry.pointers[(stream, env)]
# --8<-- endregion:promote
# --8<-- example:end
