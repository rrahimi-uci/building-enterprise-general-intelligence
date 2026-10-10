"""Resolving a skill version under policy, not just by recency.

A skill registry that only tracked "latest" would quietly change behaviour under
a running workflow. This one resolves against the requirement -- capability,
purpose, region, risk ceiling, data classes -- and only then picks the highest
eligible SemVer, so a resolution is reproducible and explainable.

Lifecycle state is not in the manifest. The manifest is immutable and digested,
so its state lives in the registry's release record and changes as evidence
arrives without moving the digest.

Packs extend the registry: a pack pins exact Skill versions as one release
unit, may become active only when every Skill it pins is active, and resolves
deprecated content only in explicit replay mode.

The SemVer precedence parser below is deliberately complete: getting prerelease
ordering wrong is how a registry silently promotes 1.0.0-rc1 over 1.0.0.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Literal

from pydantic import BaseModel, field_validator, model_validator

from examples.contracts import Risk, SkillRequirement

LifecycleState = Literal["draft", "certified", "staged", "active", "deprecated", "revoked"]


_SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def _semver_key(version: str) -> tuple[object, ...]:
    """Return a SemVer 2.0 precedence key; build metadata has no precedence."""

    match = _SEMVER.fullmatch(version)
    if match is None:
        raise ValueError(f"invalid semantic version: {version}")
    major, minor, patch = (int(match.group(i)) for i in range(1, 4))
    prerelease = match.group(4)
    if prerelease is None:
        return major, minor, patch, 1, ()
    identifiers: list[tuple[int, int | str]] = []
    for identifier in prerelease.split("."):
        if identifier.isdigit():
            if len(identifier) > 1 and identifier.startswith("0"):
                raise ValueError("numeric prerelease identifiers cannot have leading zeroes")
            identifiers.append((0, int(identifier)))
        else:
            identifiers.append((1, identifier))
    return major, minor, patch, 0, tuple(identifiers)


class SkillManifest(BaseModel):
    skill_id: str
    version: str
    description: str
    owner: str
    capabilities: frozenset[str]
    tool_versions: tuple[str, ...]
    instruction_ref: str
    knowledge_refs: tuple[str, ...] = ()
    workflow_ref: str | None = None
    allowed_purposes: frozenset[str]
    allowed_data_classes: frozenset[str]
    allowed_regions: frozenset[str]
    risk_ceiling: Risk
    digest: str | None = None

    @field_validator("version")
    @classmethod
    def version_is_semver(cls, value: str) -> str:
        _semver_key(value)
        return value

    @model_validator(mode="after")
    def validate_digest(self) -> "SkillManifest":
        body = self.model_dump(mode="json", exclude={"digest"})
        expected = "sha256:" + hashlib.sha256(
            json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        if self.digest is not None and self.digest != expected:
            raise ValueError("skill digest mismatch")
        object.__setattr__(self, "digest", expected)
        return self


# --8<-- region:resolution
class SkillRegistry:
    def __init__(self) -> None:
        self._skills: dict[str, SkillManifest] = {}
        # Release records: lifecycle state per version, outside the digest.
        self._skill_state: dict[str, LifecycleState] = {}

    def register_skill(self, skill: SkillManifest) -> str:
        key = f"{skill.skill_id}@{skill.version}"
        if key in self._skills:
            raise ValueError(f"skill already exists: {key}")
        self._skills[key] = skill
        self._skill_state[key] = "draft"
        return key

    def set_skill_state(self, key: str, state: LifecycleState) -> None:
        if key not in self._skills:
            raise LookupError(f"unknown skill: {key}")
        self._skill_state[key] = state

    def resolve(self, requirement: SkillRequirement) -> SkillManifest:
        candidates = [
            skill
            for key, skill in self._skills.items()
            if self._skill_state[key] == "active"
            and requirement.capability in skill.capabilities
            and requirement.purpose in skill.allowed_purposes
            and requirement.region in skill.allowed_regions
            and requirement.risk_ceiling <= skill.risk_ceiling
            and requirement.required_data_classes <= skill.allowed_data_classes
        ]
        if not candidates:
            raise LookupError("no eligible skill")
        # Production resolution also uses evaluation, health, cost, and rollout policy.
        return max(candidates, key=lambda skill: _semver_key(skill.version))


# --8<-- endregion:resolution


# --8<-- region:packs
class SkillPackManifest(BaseModel):
    pack_id: str
    version: str
    domain: str
    owner: str
    skill_versions: tuple[str, ...]
    policy_bundle_ref: str
    evaluation_suite_ref: str

    @field_validator("version")
    @classmethod
    def version_is_semver(cls, value: str) -> str:
        _semver_key(value)
        return value


class SkillPackRegistry(SkillRegistry):
    """A pack is a release unit: it pins Skill versions and grants nothing."""

    def __init__(self) -> None:
        super().__init__()
        self._packs: dict[str, SkillPackManifest] = {}
        self._pack_state: dict[str, LifecycleState] = {}

    def register_pack(self, pack: SkillPackManifest) -> str:
        key = f"{pack.pack_id}@{pack.version}"
        if key in self._packs:
            raise ValueError(f"skill pack already exists: {key}")
        missing = set(pack.skill_versions) - self._skills.keys()
        if missing:
            raise ValueError(f"pack references unknown skills: {sorted(missing)}")
        self._packs[key] = pack
        self._pack_state[key] = "draft"
        return key

    def set_pack_state(self, key: str, state: LifecycleState) -> None:
        if key not in self._packs:
            raise LookupError(f"unknown skill pack: {key}")
        if state == "active" and any(
            self._skill_state[skill_key] != "active"
            for skill_key in self._packs[key].skill_versions
        ):
            raise ValueError("active pack must reference only active skills")
        self._pack_state[key] = state

    def resolve_pack(
        self, pack_key: str, *, allow_deprecated_for_replay: bool = False
    ) -> tuple[SkillManifest, ...]:
        try:
            pack = self._packs[pack_key]
        except KeyError as error:
            raise LookupError("unknown skill pack") from error
        permitted = {"active"}
        if allow_deprecated_for_replay:
            # Chapter 8's compatibility window: pinned runs may replay deprecated content.
            permitted.add("deprecated")
        if self._pack_state[pack_key] not in permitted:
            raise LookupError("skill pack is not available for this resolution mode")
        if any(self._skill_state[key] not in permitted for key in pack.skill_versions):
            raise LookupError("skill pack contains unavailable skill")
        return tuple(self._skills[key] for key in pack.skill_versions)


# --8<-- endregion:packs
