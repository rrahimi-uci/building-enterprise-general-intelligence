"""Resolution must obey policy and SemVer precedence, not recency."""
from __future__ import annotations

import pytest

from examples.contracts import RiskClass, SkillRequirement
from examples.platform.skills_registry import SkillManifest, SkillPackManifest, SkillRegistry


def skill(version: str, *, risk=RiskClass.R3, regions=("us",),
          purposes=("mortgage_pre_underwriting_review",),
          data=("public",)) -> SkillManifest:
    return SkillManifest(
        skill_id="mortgage_evidence_review", version=version,
        description="review mortgage evidence",
        owner="mortgage-platform-team", capabilities=frozenset({"mortgage.evidence.review"}),
        tool_versions=("mortgage.case.read@1", "mortgage.policy.read@1"),
        instruction_ref="ref:mortgage-evidence-review",
        allowed_purposes=frozenset(purposes), allowed_data_classes=frozenset(data),
        allowed_regions=frozenset(regions), risk_ceiling=risk,
    )


def requirement(**kw) -> SkillRequirement:
    base = dict(capability="mortgage.evidence.review",
                purpose="mortgage_pre_underwriting_review", risk_ceiling=RiskClass.R2, region="us")
    base.update(kw)
    return SkillRequirement(**base)


def registry(*skills, state="active") -> SkillRegistry:
    r = SkillRegistry()
    for s in skills:
        r.set_skill_state(r.register_skill(s), state)
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
    # A skill certified only to R1 cannot serve an R4 requirement.
    r = registry(skill("1.0.0", risk=RiskClass.R1))
    with pytest.raises(LookupError):
        r.resolve(requirement(risk_ceiling=RiskClass.R4))


def test_requirement_risk_is_bounded_by_the_contract_itself():
    with pytest.raises(Exception):
        requirement(risk_ceiling="R5")


def test_non_active_versions_are_not_resolvable():
    r = registry(skill("3.0.0"), skill("1.0.0"))
    r.set_skill_state("mortgage_evidence_review@3.0.0", "deprecated")
    assert r.resolve(requirement()).version == "1.0.0"


def test_lifecycle_state_lives_outside_the_digest():
    manifest = skill("1.0.0")
    digest = manifest.digest
    r = SkillRegistry()
    key = r.register_skill(manifest)
    # A new version starts as a draft and is not resolvable until it is promoted.
    with pytest.raises(LookupError):
        r.resolve(requirement())
    for state in ("certified", "staged", "active"):
        r.set_skill_state(key, state)
    assert r.resolve(requirement()).digest == digest
    r.set_skill_state(key, "revoked")
    with pytest.raises(LookupError):
        r.resolve(requirement())
    assert manifest.digest == digest, "promotion and revocation never move the digest"


def test_an_active_pack_references_only_active_skills():
    r = SkillRegistry()
    key = r.register_skill(skill("1.0.0"))
    pack = r.register_pack(SkillPackManifest(
        pack_id="mortgage-evidence", version="1.0.0", domain="mortgage",
        owner="mortgage-platform-team", skill_versions=(key,),
        policy_bundle_ref="policy://mortgage@2026.09",
        evaluation_suite_ref="mortgage-evidence-regression@1",
    ))
    with pytest.raises(ValueError, match="only active skills"):
        r.set_pack_state(pack, "active")
    r.set_skill_state(key, "active")
    r.set_pack_state(pack, "active")
    assert r.resolve_pack(pack)[0].version == "1.0.0"


def test_no_eligible_skill_raises_rather_than_guessing():
    with pytest.raises(LookupError):
        registry(skill("1.0.0", purposes=("marketing",))).resolve(requirement())


def test_invalid_version_is_rejected_at_registration_time():
    with pytest.raises(Exception):
        registry(skill("1.0"))
