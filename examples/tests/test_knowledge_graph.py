from __future__ import annotations

import pytest

from examples.knowledge.knowledge_graph import KnowledgeGraph


def graph() -> KnowledgeGraph:
    g = KnowledgeGraph()
    for node, kind in [("payments_api", "system"), ("txn_store", "data_store"),
                       ("aml_control", "control"), ("sar_filing", "obligation"),
                       ("marketing_site", "system")]:
        g.add(node, kind=kind)
    # aml_control depends on txn_store, which depends on payments_api
    g.relate("payments_api", "depends_on_inverse", "txn_store")
    g.relate("txn_store", "depends_on_inverse", "aml_control")
    g.relate("aml_control", "depends_on_inverse", "sar_filing")
    return g


def test_impact_reaches_a_control_three_hops_away():
    # No wording links a payments API change to a regulatory filing obligation.
    # The graph does, and that is the point.
    assert graph().impact_of_changing("payments_api") == ["txn_store", "aml_control", "sar_filing"]


def test_unrelated_systems_are_not_reached():
    assert "marketing_site" not in graph().impact_of_changing("payments_api")


def test_traversal_terminates_on_a_cycle():
    g = graph()
    g.relate("sar_filing", "depends_on_inverse", "payments_api")
    assert "sar_filing" in g.impact_of_changing("payments_api")


def test_hop_budget_bounds_the_walk():
    assert graph().reaches("payments_api", "depends_on_inverse", max_hops=1) == ["txn_store"]


def test_an_edge_to_an_unknown_node_is_refused():
    g = graph()
    with pytest.raises(KeyError):
        g.relate("payments_api", "depends_on_inverse", "ghost_system")
