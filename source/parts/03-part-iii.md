# PART III — AGENTIC DEVELOPER PLATFORM & SDK

This Part turns the reference architecture into a paved road for delivery teams. It separates reusable platform capabilities from domain logic, defines portable SDK contracts, and shows how Skills and domain packs move through local development, evaluation, promotion, deployment, and support.

# 06 — Agentic Developer Platform and SDK

> **Evidence note.** The portability layer is informed by current public agent abstractions from OpenAI, Microsoft, and Google; capability parity is not assumed and must be proven by adapter conformance tests. [R29][R31][R32]

## Platform promise

The developer platform is a reusable paved road that lets teams build differentiated agents without repeatedly rebuilding identity, policy, tool safety, tracing, evaluation, durable execution, and delivery infrastructure. It is not a mandatory monolith: applications use platform-owned contracts and replaceable adapters.

[[DIAGRAM:developer-platform|Figure 6-1 — Agentic developer platform and SDK capability stack]]

| **Capability** | **Reusable platform responsibility** | **Application-specific responsibility** |
| --- | --- | --- |
| Agent Runtime | Run context, budgets, typed outputs, interruption, cancellation, adapter | Domain instructions, acceptance, specialist roles |
| Workflow/Orchestration | Durable state, timers, retries, joins, compensation, replay | Domain process graph and deadlines |
| Tool SDK | Schema, identity context, idempotency, effect protocol, mocks, telemetry | Domain operation and compensation semantics |
| MCP Integration | Server registry, trust, gateway, discovery cache, compatibility tests | Approved servers/tools and domain interpretation |
| Agent-to-Agent Communication | Task/artifact envelopes, delegation, identity, deadline, cancellation | Collaboration topology and child acceptance |
| Context/RAG | Connectors, ACL filtering, snapshot/provenance, ranking hooks, budgets | Sources, retrieval policy, evidence requirements |
| Memory | Eligibility, scope, TTL, provenance, correction/deletion, encryption | Purpose, schema, confidence, business ownership |
| Skills | Manifest, versioning, dependencies, signing, registry, tests | Capability logic, knowledge, examples, acceptance suite |
| Identity & Permissions | Subject/workload identity, policy, short-lived credentials | Declared permissions and resource scopes |
| Guardrails | Injection, input/output safety, DLP, action policy | Domain risk rules, safe responses, escalation |
| LLM Gateway | Provider adapters, routing, budgets, filtering, cache, fallback, telemetry | Quality/cost/latency policy and needed capabilities |
| Evaluation | Dataset/evaluator registry, experiments, regression gates | Domain truth, rubrics, thresholds, reviewers |
| Observability/Tracing | Unified run graph, schemas, sampling, redaction, correlation | Domain events and outcome linkage |
| Durable Execution | Checkpoints, leases, deduplication, recovery, reconciliation | Domain state machine and compensation choices |
| Human-in-the-Loop | Proposal, preview, grants, queues, SLAs, recourse | Reviewer policy, domain evidence, decision rights |
| Deployment & Versioning | Packaging, manifests, environments, gates, canary, rollback | Application release and risk sign-off |

## Portable contracts and multi-framework support

[[DIAGRAM:portability|Figure 6-2 — Platform contracts with replaceable framework and provider adapters]]

Use AgentSpec, RunContext, TaskEnvelope, ToolSpec/ToolCall, ContextManifest, MemoryRecord, EvaluationResult, and ReleaseManifest as stable contracts. Compile them into framework/provider adapters. Standardized contracts, MCP, APIs, events, agent-to-agent protocols, gateways, and shared platform services provide interoperability without leaking vendor-native message objects into applications. Compatibility suites verify cancellation, tools, streaming, approvals, errors, telemetry, usage, and version behavior.

## Developer lifecycle

[[DIAGRAM:developer-lifecycle|Figure 6-3 — Local-to-production agent lifecycle]]

Create from an approved template; attach tools, Skills, context, and memory; configure model policy, permissions, budgets, and review; test deterministic logic, contracts, simulations, adversarial cases, and failures; evaluate quality, safety, latency, and cost; package immutable artifacts with locks, SBOM, signature, provenance, and ReleaseManifest; promote through policy gates; observe correlated production traces; improve through controlled ChangeBundles.

## SDK example

PYTHON · implementation excerpt

```python
agent = platform.agent(
    spec="supplier_onboarding@3.2.0",
    model_policy="quality-balanced@7",
    permissions=["supplier:read", "screening:propose"],
    budgets={"tokens": 18_000, "usd": 0.45, "deadline_s": 90},
)
agent.attach_skill("supplier-screening@2.4.1")
agent.attach_tool(screen_supplier, risk="protected", effect="screening.create")
agent.use_context(source="supplier-policy", snapshot="approved-latest")
agent.use_memory(policy="tenant-user-preferences@3")
report = platform.test(agent).simulate("supplier-onboarding-regression")
platform.release(agent, require=["quality", "security", "cost", "rollback"])
```

The fluent API is convenience. The compiled contracts, policy decisions, tool/effect evidence, traces, and release manifest are the stable interface.


## Transition to Chapter 7

With platform responsibilities separated from application logic, Chapter 7 specifies the developer workflow that makes the paved road usable.

# 07 — Developer Experience, Testing, and Delivery Lifecycle

## Golden path

Developer experience should compress setup and diagnosis time while making authority, versions, risk, evidence, and cost visible. A convenient SDK that hides those concerns transfers complexity to production incidents.

[[DIAGRAM:dx-golden-path|Figure 7-1 — Developer golden path from scaffold to operated release]]

| **Stage** | **Developer action** | **Platform assistance** | **Evidence** |
| --- | --- | --- | --- |
| Scaffold | Select template and risk tier | AgentSpec, ownership, tests, eval, deployment skeleton | Purpose, owner, acceptance, data/effect class |
| Develop | Add instructions, tools, Skills, context, workflow | Local runtime, mocks, seeded simulation, hot reload | Unit/contract tests and permissions |
| Debug | Inspect and compare run graphs | Trace viewer, state/time travel, prompt/context diff, replay | Reproducible failure and first divergence |
| Evaluate | Run golden, adversarial, failure, load suites | Dataset/evaluator registry and slice reports | Thresholds, reviewers, baseline, uncertainty |
| Package | Build immutable bundle | Lock, SBOM, signing, provenance, compatibility | ReleaseManifest and rollback target |
| Promote | Bind environment and canary | Policy gate, approval, progressive delivery | ValidationReport and risk approval |
| Operate | Observe SLO, quality, safety, cost | Alerts, runbooks, reconciliation, incident tools | On-call and operational ownership |
| Improve | Build ChangeBundle from evidence | Trace mining, dataset curation, experiment workflow | Causal hypothesis, tests, approval, learning record |

## Testing and simulation pyramid

[[DIAGRAM:test-pyramid|Figure 7-2 — Testing and simulation pyramid]]

Deterministic units verify schemas, policy helpers, acceptance, routes, reducers, calculations, and state transitions. Contract tests verify identity, idempotency, timeout/unknown-effect semantics, protocol capability, errors, and telemetry. Component evaluations measure retrieval, tools, arguments, structured output, safety, and memory. Trajectory simulation tests planning, handoffs, loops, deadlines, cancellation, duplicates, dependency degradation, and human delay. End-to-end staging uses exact model, identity, gateway, data, and integration versions. Canary and shadow evaluation use explicit stop and rollback conditions.

## CLI and delivery workflow

BASH · implementation excerpt

```bash
agentctl init supplier-onboarding --template regulated-workflow --risk high
agentctl dev --scenario late-sanctions-response --trace
agentctl test --unit --contracts --failure-injection
agentctl eval --dataset supplier-regression@12 --compare production
agentctl package --lock --sbom --sign
agentctl promote --from staging --to production --canary 5%
agentctl traces diff run:failed run:accepted
agentctl rollback supplier-onboarding@3.2.0 --to 3.1.4
```

Use one immutable artifact across environments; bind endpoints, identities, secrets, sources, quotas, regions, and review queues at deployment. Pin SDKs, adapters, model aliases, tool schemas, Skills, MCP servers, policy bundles, evaluators, and knowledge snapshots. A model/provider swap is a behavior change—not harmless configuration.

## Troubleshooting

Start from accepted business outcome and walk backward through the causal run graph. Find the first divergent span: input classification, source/freshness, prompt, route, model, tool, arguments, policy, effect, approval, or acceptance. Do not “fix the prompt” until evidence locates the failing responsibility.


## Transition to Chapter 8

The delivery path is established; Chapter 8 packages repeatable behavior as versioned Skills with explicit contracts and lifecycle controls.

# 08 — Skills as Versioned Capabilities

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  Teams begin copying prompts and tool wrappers between agents. Results diverge, fixes do not propagate, and no owner can prove which behavior reached production. Northstar introduces a Skill as the unit of reusable capability. |

|  |
| --- |
| **DESIGN DECISION**  Make the Skill manifest the versioned capability contract and resolve exact releases through policy and evaluation evidence. |

## What this chapter delivers

Define Skills as governed packages of instructions, tools, knowledge, policy, workflows, tests, and operations metadata.

## Solution blueprint


Figure 10. Skills as Versioned Capabilities.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Skill Registry and resolver | semantic discovery to policy-bound resolution | skill family · registry partition | one skill version | SkillManifest · SkillRequirement · SkillRelease |

## Skill anatomy

A Skill is the smallest independently owned and versioned package that lets an agent perform a meaningful capability. Its manifest names interface schemas, instructions, eligible tools, knowledge sources, optional workflow template, policy constraints, side-effect class, observability fields, evaluation suite, owner, lifecycle, and immutable digest.

Skills separate reuse from copy-and-paste. An application requests a capability such as supplier.evidence.read; it does not embed a specific prompt and connector. Discovery searches a catalog. Resolution then filters by tenant, purpose, subject and actor grants, data class, region, risk, compatibility, release stage, health, and cost before pinning one exact version.

### Skill lifecycle

Draft → Certified → Staged → Active → Deprecated → Revoked is evidence-driven. Certification includes contract, unit, simulation, trajectory, threat, failure-injection, load, and operator-readiness checks. Deprecation retains a compatibility window for active runs. Revocation removes the Skill from new resolution immediately and may trigger workflow pause or migration by risk class.

### Skill contract surface

* describe(requirement) -> candidates
* resolve(requirement, run\_envelope) -> SkillRelease
* invoke(step\_request) -> AgentStepResult
* evaluate(release, dataset\_version) -> EvaluationReport
* promote(release, stage, evidence) -> ReleaseDecision

The registry scales as a read-heavy control-plane service with immutable manifests, version indexes, cached eligibility metadata, and regional last-known-good replicas. Runtime execution remains in regional cells.

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Terminology | Skill is a platform-owned package in this book. It is not an OpenAI Agents SDK primitive and is not identical to A2A AgentSkill metadata or Skills over MCP. Interchange requires an explicit adapter and loss analysis. | A2A-101; MCP-2026 |

Evidence anchors: SLSA; MCP-2026. Full URLs, authority, version, and scope appear in Appendix M.

## Implementation reference


### Skill manifest and resolver

PYTHON · implementation excerpt

```python
from __future__ import annotations

import hashlib
import json
import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from .contracts import SkillRequirement


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
    maximum_risk: int = Field(ge=0, le=4)
    status: Literal["draft", "active", "deprecated", "revoked"] = "draft"
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


class SkillPackManifest(BaseModel):
    pack_id: str
    version: str
    domain: str
    owner: str
    skill_versions: tuple[str, ...]
    policy_bundle_ref: str
    evaluation_suite_ref: str
    status: Literal["draft", "active", "deprecated", "revoked"] = "draft"

    @field_validator("version")
    @classmethod
    def version_is_semver(cls, value: str) -> str:
        _semver_key(value)
        return value


class SkillRegistry:
    def __init__(self) -> None:
        self._skills: dict[str, SkillManifest] = {}
        self._packs: dict[str, SkillPackManifest] = {}

    def register_skill(self, skill: SkillManifest) -> str:
        key = f"{skill.skill_id}@{skill.version}"
        if key in self._skills:
            raise ValueError(f"skill already exists: {key}")
        self._skills[key] = skill
        return key

    def register_pack(self, pack: SkillPackManifest) -> str:
        key = f"{pack.pack_id}@{pack.version}"
        if key in self._packs:
            raise ValueError(f"skill pack already exists: {key}")
        missing = set(pack.skill_versions) - self._skills.keys()
        if missing:
            raise ValueError(f"pack references unknown skills: {sorted(missing)}")
        if pack.status == "active" and any(
            self._skills[skill_key].status != "active"
            for skill_key in pack.skill_versions
        ):
            raise ValueError("active pack must reference only active skills")
        self._packs[key] = pack
        return key

    def resolve(self, requirement: SkillRequirement) -> SkillManifest:
        candidates = [
            skill
            for skill in self._skills.values()
            if skill.status == "active"
            and requirement.capability in skill.capabilities
            and requirement.purpose in skill.allowed_purposes
            and requirement.region in skill.allowed_regions
            and requirement.maximum_risk <= skill.maximum_risk
            and requirement.required_data_classes <= skill.allowed_data_classes
        ]
        if not candidates:
            raise LookupError("no eligible skill")
        # Production resolution also uses evaluation, health, cost, and rollout policy.
        return max(candidates, key=lambda skill: _semver_key(skill.version))

    def resolve_pack(
        self, pack_key: str, *, allow_deprecated_for_replay: bool = False
    ) -> tuple[SkillManifest, ...]:
        try:
            pack = self._packs[pack_key]
        except KeyError as error:
            raise LookupError("unknown skill pack") from error
        permitted_pack_states = {"active"}
        permitted_skill_states = {"active"}
        if allow_deprecated_for_replay:
            permitted_pack_states.add("deprecated")
            permitted_skill_states.add("deprecated")
        if pack.status not in permitted_pack_states:
            raise LookupError("skill pack is not available for this resolution mode")
        skills = tuple(self._skills[key] for key in pack.skill_versions)
        if any(skill.status not in permitted_skill_states for skill in skills):
            raise LookupError("skill pack contains unavailable skill")
        return skills
```

## Debugging playbook

1. Resolve a Skill version from the recorded requirement and compare registry evidence.
2. Diff Skill manifests across a regression.
3. Verify no hidden tool, knowledge, or policy dependency exists outside the manifest.

## Production checklist

**✓** Every Skill has an owner, immutable version, digest, lifecycle, and support window.

**✓** Inputs, outputs, side effects, risk, data, region, and observability are explicit.

**✓** Discovery is semantic; resolution is deterministic and policy-bound.

**✓** Tool and knowledge dependencies are pinned and compatible.

**✓** Contract, trajectory, threat, failure, and load evidence gate promotion.

## Exercises

1. Author a Skill manifest for supplier evidence retrieval.
2. Define a certification suite that catches a cross-tenant retrieval defect.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| What is a Skill? | A versioned capability package combining contract, instructions, tools, knowledge, policy, workflow, tests, release evidence, and ownership. |
| How is Skill discovery different from resolution? | Discovery finds semantic candidates; resolution applies deterministic eligibility, compatibility, health, policy, and release rules to pin one version. |
| What makes a Skill portable? | Provider-neutral typed interfaces and artifact references, with SDK-specific adapters kept behind the runtime boundary. |
| How should a Skill be tested? | Contract, deterministic unit, simulation, trajectory, threat, data-boundary, failure-injection, regression, load, and canary tests. |
| When should behavior remain application-specific? | When it encodes one product transaction, unstable workflow, private data boundary, or ownership model that should not be generalized. |


## Transition to Chapter 9

Individual Skills are governable; Chapter 9 composes them into domain packs without dissolving ownership or compatibility boundaries.

# 09 — Skill Packs and Domain Platforms

|  |
| --- |
| **NORTHSTAR AT THIS POINT**  Procurement needs a complete domain experience, not isolated Skills. Evidence retrieval, document validation, sanctions screening, policy explanation, and approval preparation must ship as a compatible, evaluated pack. |

|  |
| --- |
| **DESIGN DECISION**  Ship domain behavior as immutable Skill Packs with compatibility, policy, evaluation, and promotion metadata. |

## What this chapter delivers

Compose compatible Skills into certified, distributable domain capability releases.

## Solution blueprint


Figure 11. Skill Packs and Domain Platforms.

| **State owner** | **Trust boundary** | **Scale unit** | **Failure containment** | **Core contracts** |
| --- | --- | --- | --- | --- |
| Skill Pack Registry and release pipeline | pack authoring to tenant/runtime use | domain pack · tenant rollout cohort | one pack release | SkillPackManifest · CompatibilityReport · EvaluationSuite |

## From individual capability to domain platform

A Skill Pack composes a coherent domain experience. Northstar’s supplier-onboarding pack pins evidence retrieval, document validation, sanctions screening, policy explanation, approval preparation, and supplier-record creation Skills. It also pins shared policy, taxonomy, knowledge strategy, workflow templates, evaluation datasets, dashboards, and runbooks.

A pack is not a directory of prompts. The pack manifest declares dependency constraints, schema compatibility, required runtime capabilities, data and region policy, risk ceiling, evaluation gates, release aliases, owner, and support window. A pack can expose a smaller capability surface to each agent even though the complete domain distribution contains more Skills.

### Pack governance and sharing

Packs move through signed releases and aliases such as development, staging, and production. Tenant rollout policy can pin a version or cohort. Sharing across business units requires explicit policy and data-boundary review; installing a pack never grants access to its data sources or tools.

### Domain pack examples

* **Supplier onboarding:** evidence, screening, tax, policy, approval, ERP write.
* **Customer support:** account read, entitlement, troubleshooting, refund proposal, escalation.
* **Software delivery:** repository context, test planning, code change, review, deployment evidence.
* **Financial close:** reconciliation, variance explanation, exception routing, controlled posting.

## Grounding, corrections, and evidence boundary

| **Claim or correction** | **Grounded statement** | **Source IDs** |
| --- | --- | --- |
| Distribution security | A Skill Pack is executable supply chain: pin dependencies and tool schemas, produce SBOM and signed provenance, scan transitive content and binaries, enforce publisher trust, and support revocation without rewriting historical runs. | SLSA; OWASP-CHEAT |

Evidence anchors: SLSA; OWASP-CHEAT. Full URLs, authority, version, and scope appear in Appendix M.

## Implementation reference


### Skill Pack contract

PYTHON · implementation excerpt

```python
from __future__ import annotations
import hashlib
import json
import re
from typing import Literal
from pydantic import BaseModel, Field, field_validator, model_validator
from .contracts import SkillRequirement

class SkillPackManifest(BaseModel):
    pack_id: str
    version: str
    domain: str
    owner: str
    skill_versions: tuple[str, ...]
    policy_bundle_ref: str
    evaluation_suite_ref: str
    status: Literal["draft", "active", "deprecated", "revoked"] = "draft"

    @field_validator("version")
    @classmethod
    def version_is_semver(cls, value: str) -> str:
        _semver_key(value)
        return value
```

## Debugging playbook

1. Expand the pack dependency graph and locate the incompatible version.
2. Compare pack alias history with active run manifests.
3. Run the pack-level evaluation suite on the failing tenant slice.

## Production checklist

**✓** The pack manifest pins exact compatible Skill and dependency versions.

**✓** Shared policy, knowledge, workflows, and evaluations are explicit artifacts.

**✓** Installation does not grant runtime authority.

**✓** Promotion, deprecation, rollback, and tenant rollout use aliases and evidence.

**✓** Pack-level failures can be isolated without disabling unrelated capabilities.

## Exercises

1. Compose a supplier-onboarding Skill Pack and define compatibility rules.
2. Design a deprecation plan for one Skill without breaking the pack.

## Technical review questions

| **Question** | **Strong answer** |
| --- | --- |
| Why create a Skill Pack? | To distribute a compatible domain capability set with shared policy, knowledge, workflows, evaluation, and lifecycle controls. |
| What must pack compatibility cover? | Skill and tool schemas, policy obligations, workflow contracts, knowledge versions, runtime and model requirements, and deprecation windows. |
| Can installing a pack grant authority? | No. Installation exposes definitions; tenant policy and each run envelope still determine eligibility and exact authorization. |
| How should packs be promoted? | As signed immutable releases through dev, staging, shadow, canary, production, and rollback aliases backed by evaluation evidence. |
| What is the main pack anti-pattern? | A monolithic prompt-and-tools bundle with hidden dependencies, no owner, no tests, and no independent versioning. |


## Transition to Chapter 10

The platform and capability model are complete; Chapter 10 begins the pattern sequence with the smallest bounded reasoning loop.
