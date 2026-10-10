"""AP-06: a Boolean approval versus a decision bound to the exact proposal.

A flag on the run approves whatever the arguments happen to be at commit time.
The correction reuses Chapter 14's commit-time check: the decision must cover
this exact proposal, by an eligible approver, under the same policy, before it
expires, and against the case version the approver saw. The idempotency key is
the logical effect key -- the business intent -- not the proposal hash, so a
retry of the same approved effect cannot commit twice.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from examples.patterns.approval_verification import (
    ApprovalDecision, ApprovalRequest, verify_approval,
)


class Underwriting(Protocol):
    def submit_evidence_package(self, *, idempotency_key: str | None = None,
                                **arguments: object) -> str: ...


@dataclass
class Run:
    approved: bool
    case_id: str


# --8<-- example:start
# Anti-pattern: consent is a flag on the run, detached from what executes.
def submit_naive(run: Run, underwriting: Underwriting) -> str | None:
    if run.approved:
        return underwriting.submit_evidence_package(case_id=run.case_id)
    return None


# Correction: the decision covers this exact proposal, now, against the
# current policy and case version, immediately before commit.
def submit(proposal: ApprovalRequest, decision: ApprovalDecision,
           underwriting: Underwriting, *, now: datetime, case_version: int) -> str:
    verify_approval(proposal, decision, now=now, actual_resource_version=case_version)
    return underwriting.submit_evidence_package(
        **proposal.arguments,
        idempotency_key=proposal.logical_effect_key,   # business intent, not the hash
    )
# --8<-- example:end
