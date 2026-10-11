from __future__ import annotations

import pytest

from dataclasses import FrozenInstanceError

from examples.knowledge.knowledge_graph import (
    GraphRelease, GraphSchema, KnowledgeGraph, validate,
)


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


SCHEMA = GraphSchema(
    version="3.2.0",
    node_kinds=frozenset({"requirement", "obligation", "control"}),
    edge_kinds=frozenset({("obligation", "derived_from", "requirement"),
                          ("control", "discharges", "obligation")}),
    required={"requirement": ("source_digest",), "obligation": ("scope", "effective_from"),
              "control": ("owner",)},
)


def compliance_graph() -> KnowledgeGraph:
    g = KnowledgeGraph()
    g.add("REQ-income-current", kind="requirement", source_digest="a" * 64)
    g.add("OBL-income-evidence", kind="obligation", scope="US", effective_from="2026-10-01")
    g.add("CTL-age-window", kind="control", owner="underwriting_policy_owner")
    g.relate("OBL-income-evidence", "derived_from", "REQ-income-current")
    g.relate("CTL-age-window", "discharges", "OBL-income-evidence")
    return g


def test_a_conforming_graph_has_no_violations():
    assert validate(compliance_graph(), SCHEMA) == []


def test_an_edge_between_kinds_the_schema_forbids_is_a_violation():
    g = compliance_graph()
    g.relate("REQ-income-current", "discharges", "CTL-age-window")
    assert [v.subject for v in validate(g, SCHEMA)] == ["REQ-income-current discharges CTL-age-window"]


def test_a_node_missing_a_required_property_is_a_violation():
    g = compliance_graph()
    g.add("OBL-unscoped", kind="obligation", effective_from="2026-10-01")
    assert [(v.subject, v.reason) for v in validate(g, SCHEMA)] == [
        ("OBL-unscoped", "obligation must carry scope")]


def test_validate_reports_every_violation_and_repairs_nothing():
    g = compliance_graph()
    g.add("OBL-unscoped", kind="obligation")
    g.add("X-guess", kind="unplaced")
    before = (dict(g.nodes), list(g.edges))
    assert len(validate(g, SCHEMA)) == 3   # scope, effective_from, unknown kind
    assert (dict(g.nodes), list(g.edges)) == before


def test_two_identical_graphs_freeze_to_one_digest():
    assert (GraphRelease.freeze(compliance_graph(), SCHEMA).digest
            == GraphRelease.freeze(compliance_graph(), SCHEMA).digest)


def test_the_release_digest_changes_when_one_property_changes():
    g = compliance_graph()
    g.nodes["OBL-income-evidence"]["effective_from"] = "2026-11-01"
    assert GraphRelease.freeze(g, SCHEMA).digest != GraphRelease.freeze(compliance_graph(), SCHEMA).digest


def test_a_release_cannot_be_mutated_after_freezing():
    g = compliance_graph()
    release = GraphRelease.freeze(g, SCHEMA)
    with pytest.raises(FrozenInstanceError):
        release.digest = "0" * 64
    g.nodes["CTL-age-window"]["owner"] = "someone_else"   # the working graph moves on
    assert release == GraphRelease.freeze(compliance_graph(), SCHEMA)


def test_a_non_conforming_graph_cannot_be_frozen():
    g = compliance_graph()
    g.add("X-guess", kind="unplaced")
    with pytest.raises(ValueError):
        GraphRelease.freeze(g, SCHEMA)
