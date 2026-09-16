from __future__ import annotations

import pytest

from examples.knowledge.knowledge_graph import KnowledgeGraph


def graph() -> KnowledgeGraph:
    g = KnowledgeGraph()
    for node, kind in [("loan_origination_api", "system"), ("mortgage_case_store", "data_store"),
                       ("evidence_freshness_control", "control"),
                       ("underwriting_review_queue", "obligation"),
                       ("servicing_site", "system")]:
        g.add(node, kind=kind)
    # The freshness control depends on the case store, which depends on the LOS.
    g.relate("loan_origination_api", "depends_on_inverse", "mortgage_case_store")
    g.relate("mortgage_case_store", "depends_on_inverse", "evidence_freshness_control")
    g.relate("evidence_freshness_control", "depends_on_inverse", "underwriting_review_queue")
    return g


def test_impact_reaches_a_control_three_hops_away():
    # No wording links an LOS change to an underwriting obligation.
    # The graph does, and that is the point.
    assert graph().impact_of_changing("loan_origination_api") == ["mortgage_case_store", "evidence_freshness_control", "underwriting_review_queue"]


def test_unrelated_systems_are_not_reached():
    assert "servicing_site" not in graph().impact_of_changing("loan_origination_api")


def test_traversal_terminates_on_a_cycle():
    g = graph()
    g.relate("underwriting_review_queue", "depends_on_inverse", "loan_origination_api")
    assert "underwriting_review_queue" in g.impact_of_changing("loan_origination_api")


def test_hop_budget_bounds_the_walk():
    assert graph().reaches("loan_origination_api", "depends_on_inverse", max_hops=1) == ["mortgage_case_store"]


def test_an_edge_to_an_unknown_node_is_refused():
    g = graph()
    with pytest.raises(KeyError):
        g.relate("loan_origination_api", "depends_on_inverse", "ghost_system")
