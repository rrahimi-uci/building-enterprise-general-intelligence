"""AP-11: unbounded delegation versus one budget that every child draws on.

Local limits do not compose. If each hop grants a fresh budget, the ceiling of
the whole tree is depth times fan-out. The correction makes delegation a
withdrawal from the parent's remaining balance, so the root's admission bounds
the entire subtree, and checks depth and ownership cycles at the same point.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Protocol


class DelegationDepthExceeded(Exception):
    """The task tree is already as deep as the run allows."""


class DelegationCycle(Exception):
    """The child's owner already appears above it in the task tree."""


class BudgetExhausted(Exception):
    """The parent cannot fund what the child asks for."""


@dataclass(frozen=True)
class Task:
    id: str
    owner: str
    estimate: int  # tokens the child asks for


class Worker(Protocol):
    def run(self, task: Task, budget: "Budget") -> object: ...


# --8<-- example:start
@dataclass
class Budget:
    tokens: int
    depth: int
    ancestors: frozenset[str] = frozenset()

    def withdraw(self, tokens: int, owner: str) -> "Budget":
        """Fund a child from this budget; a child never holds more than its parent."""
        if self.depth <= 0:
            raise DelegationDepthExceeded(owner)
        if owner in self.ancestors:              # acyclic ownership
            raise DelegationCycle(owner)
        if tokens > self.tokens:
            raise BudgetExhausted(owner)
        self.tokens -= tokens                    # the parent's balance falls
        return Budget(tokens, self.depth - 1, self.ancestors | {owner})


# Anti-pattern: every child starts fresh, so the ceiling is depth x fan-out.
def delegate_naive(task: Task, worker: Worker) -> object:
    return worker.run(task, Budget(tokens=20_000, depth=3))   # reset on every hop


# Correction: delegation is a withdrawal from the parent's remaining budget,
# so the whole subtree is bounded by the root's admission.
def delegate(task: Task, worker: Worker, parent: Budget) -> object:
    child = parent.withdraw(task.estimate, owner=task.owner)
    return worker.run(task, child)
# --8<-- example:end


@dataclass
class FanOutWorker:
    """Test double: every task spawns `fan_out` children until something stops it."""

    fan_out: int
    spawn: Callable[[Task, "FanOutWorker", Budget], object]
    granted: int = 0
    tasks_run: int = 0
    max_tasks: int = 200  # a safety net for the anti-pattern, not a control

    def run(self, task: Task, budget: Budget) -> object:
        self.tasks_run += 1
        self.granted += budget.tokens
        if self.tasks_run >= self.max_tasks:
            return "stopped by the test harness"
        for n in range(self.fan_out):
            child = Task(f"{task.id}.{n}", owner=f"{task.owner}/{n}", estimate=task.estimate)
            try:
                self.spawn(child, self, budget)
            except (DelegationDepthExceeded, BudgetExhausted):
                break
        return "done"
