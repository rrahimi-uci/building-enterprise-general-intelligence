"""Traversal answering a question that similarity cannot.

Retrieval finds passages that look like the question. It cannot tell you that a
control three hops away depends on a system you are about to change, because
nothing in the wording of either document resembles the other. That is not a
tuning problem; it is the wrong operation.

The ``shapes`` region adds the schema the graph must conform to and the frozen,
content-addressed instance a release carries. The checks are the book's own,
stated in plain graph terms; the property that validation reports every
violation and repairs none follows the reference implementation's information-
model tests in Policy Logic Forge [R48] (commit c22dc450, MIT).
"""
from __future__ import annotations

import hashlib
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


# --8<-- region:shapes
@dataclass(frozen=True)
class GraphSchema:
    """The ontology: which kinds exist, how they may relate, what each must carry."""

    version: str                                  # MAJOR.MINOR.PATCH
    node_kinds: frozenset[str]
    edge_kinds: frozenset[tuple[str, str, str]]   # (source kind, relation, target kind)
    required: dict[str, tuple[str, ...]]          # kind -> properties it must carry


@dataclass(frozen=True)
class Violation:
    subject: str
    reason: str


def validate(graph: KnowledgeGraph, schema: GraphSchema) -> list[Violation]:
    """Report every violation and repair nothing: a checker that fixes what it
    finds can no longer say how good the graph was."""
    found = []
    for node, props in sorted(graph.nodes.items()):
        kind = props.get("kind")
        if kind not in schema.node_kinds:
            found.append(Violation(node, f"kind {kind!r} is not in ontology {schema.version}"))
            continue
        found += [Violation(node, f"{kind} must carry {name}")
                  for name in schema.required.get(kind, ()) if name not in props]
    for source, relation, target in graph.edges:
        edge_kind = (graph.nodes[source].get("kind"), relation, graph.nodes[target].get("kind"))
        if edge_kind not in schema.edge_kinds:
            found.append(Violation(f"{source} {relation} {target}",
                                   f"ontology {schema.version} does not allow {edge_kind}"))
    return found


@dataclass(frozen=True)
class GraphRelease:
    """A conforming graph frozen for release: identity is the digest of its content."""

    ontology_version: str
    nodes: tuple
    edges: tuple
    digest: str

    @classmethod
    def freeze(cls, graph: KnowledgeGraph, schema: GraphSchema) -> "GraphRelease":
        if violations := validate(graph, schema):
            raise ValueError(f"{len(violations)} violations; a non-conforming graph is not released")
        nodes = tuple(sorted((n, tuple(sorted(p.items()))) for n, p in graph.nodes.items()))
        edges = tuple(sorted(graph.edges))
        content = repr((schema.version, nodes, edges)).encode("utf-8")
        return cls(schema.version, nodes, edges, hashlib.sha256(content).hexdigest())
# --8<-- endregion:shapes
