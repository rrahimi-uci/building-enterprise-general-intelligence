"""Resolution must obey policy and SemVer precedence, not recency."""
from __future__ import annotations

import pytest

from examples.contracts import SkillRequirement
from examples.platform.skills_registry import SkillManifest, SkillRegistry


def skill(version: str, *, status="active", risk=3, regions=("us",),
          purposes=("mortgage_pre_underwriting_review",),
          data=("public",)) -> SkillManifest:
    return SkillManifest(
        skill_id="mortgage_evidence_review", version=version,
        description="review mortgage evidence",
        owner="mortgage-platform-team", capabilities=frozenset({"mortgage.evidence.review"}),
        tool_versions=("mortgage.case.read@1", "mortgage.policy.read@1"),
        instruction_ref="ref:mortgage-evidence-review",
        allowed_purposes=frozenset(purposes), allowed_data_classes=frozenset(data),
        allowed_regions=frozenset(regions), maximum_risk=risk, status=status,
    )


def requirement(**kw) -> SkillRequirement:
    base = dict(capability="mortgage.evidence.review",
                purpose="mortgage_pre_underwriting_review", maximum_risk=2, region="us")
    base.update(kw)
    return SkillRequirement(**base)


def registry(*skills) -> SkillRegistry:
    r = SkillRegistry()
    for s in skills:
        r.register_skill(s)
    return r


def test_highest_eligible_semver_wins_not_the_newest_registered():
    r = registry(skill("1.2.0"), skill("1.10.0"), skill("1.9.0"))
    # 1.10.0 > 1.9.0 numerically; string ordering would pick 1.9.0.
    assert r.resolve(requirement()).version == "1.10.0"


def test_prerelease_never_outranks_the_release():
    r = registry(skill("1.0.0"), skill("1.0.0-rc.1"))
    assert r.resolve(requirement()).version == "1.0.0"


def test_region_mismatch_makes_a_skill_ineligible():
    r = registry(skill("2.0.0", regions=("us",)), skill("1.0.0", regions=("eu",)))
    # The newer skill is not permitted in the requested region, so it is not a candidate.
    assert r.resolve(requirement(region="eu")).version == "1.0.0"


def test_risk_ceiling_is_enforced():
    # A skill certified only to risk class 1 cannot serve a class-4 requirement.
    r = registry(skill("1.0.0", risk=1))
    with pytest.raises(LookupError):
        r.resolve(requirement(maximum_risk=4))


def test_requirement_risk_is_bounded_by_the_contract_itself():
    with pytest.raises(Exception):
        requirement(maximum_risk=5)


def test_non_active_versions_are_not_resolvable():
    r = registry(skill("3.0.0", status="deprecated"), skill("1.0.0"))
    assert r.resolve(requirement()).version == "1.0.0"


def test_no_eligible_skill_raises_rather_than_guessing():
    with pytest.raises(LookupError):
        registry(skill("1.0.0", purposes=("marketing",))).resolve(requirement())


def test_invalid_version_is_rejected_at_registration_time():
    with pytest.raises(Exception):
        registry(skill("1.0"))
