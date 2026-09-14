"""Traversal answering a question that similarity cannot.

Retrieval finds passages that look like the question. It cannot tell you that a
control three hops away depends on a system you are about to change, because
nothing in the wording of either document resembles the other. That is not a
tuning problem; it is the wrong operation.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

# --8<-- example:start


@dataclass
class KnowledgeGraph:
    """A typed property graph: edges carry meaning, not just adjacency."""

    nodes: dict[str, dict] = field(default_factory=dict)
    edges: list[tuple[str, str, str]] = field(default_factory=list)

    def add(self, node_id: str, **properties) -> None:
        self.nodes[node_id] = properties

    def relate(self, source: str, relation: str, target: str) -> None:
        for end in (source, target):
            if end not in self.nodes:
                raise KeyError(f"unknown node: {end}")
        self.edges.append((source, relation, target))

    def neighbours(self, node_id: str, relation: str | None = None) -> list[str]:
        return [t for s, r, t in self.edges
                if s == node_id and (relation is None or r == relation)]

    def reaches(self, start: str, relation: str, *, max_hops: int = 6) -> list[str]:
        """Everything transitively reachable along one relation.

        Bounded: an unbounded traversal over an enterprise graph is a denial of
        service against your own agent, and a cycle makes it non-terminating.
        """
        seen, order = {start}, []
        queue = deque([(start, 0)])
        while queue:
            node, depth = queue.popleft()
            if depth >= max_hops:
                continue
            for nxt in self.neighbours(node, relation):
                if nxt not in seen:
                    seen.add(nxt)
                    order.append(nxt)
                    queue.append((nxt, depth + 1))
        return order

    def impact_of_changing(self, node_id: str) -> list[str]:
        """What depends on this, however indirectly. The question RAG cannot answer."""
        return self.reaches(node_id, "depends_on_inverse")


# --8<-- example:end
