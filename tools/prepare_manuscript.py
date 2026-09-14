#!/usr/bin/env python3
"""Create the editorially normalized Book v1.0.0 canonical Markdown.

The script is intentionally deterministic: the same source, registry, and config
produce byte-identical Markdown. It performs version normalization, removes known
boilerplate duplication, inserts part orientations and chapter transitions, adds
scoped evidence notes, and generates the authoritative References and claim ledger.
"""
from pathlib import Path
import json,re,hashlib
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'source/original/Enterprise-Agentic-AI-Guide-v3.1-source.md'
OUT=ROOT/'book/manuscript.md'
DIST=ROOT/'dist/Enterprise-General-Intelligence-v1.0.0.md'
REFS=json.loads((ROOT/'config/references.json').read_text(encoding='utf-8'))['references']

s=SRC.read_text(encoding='utf-8').replace('\r\n','\n')
s=s.replace('Final Edition v3.1 · September 2026','Book v1.0.0 · Publication Release · September 2026')
s=s.replace('v3.1 architecture and developer-platform restructuring','v1.0.0 publication architecture and developer-platform foundation')
s=s.replace('Final Edition v3.1','Book v1.0.0')
s=s.replace('v3.1','v1.0.0')
# Apply robust corrections where Markdown escaping can vary.
s=re.sub(r"\| MLflow baseline \|.*?\| MLFLOW-3152; MLFLOW-MCP \|", "| MLflow baseline | This book pins MLflow 3.15.2 as a reproducibility baseline for its examples. It is not labeled latest; feature availability, experimental status, and compatibility must be re-verified against release notes and current documentation before implementation. | MLFLOW-3152; MLFLOW-MCP |", s, count=1)
s=re.sub(r"\* MLflow 3\.15\.2 \(the pinned 3\.15 patch baseline; MLflow 3\.16\.0 also exists\)", "* MLflow 3.15.2 (the pinned example baseline; re-verify current releases before implementation)", s, count=1)
s=re.sub(r"\| Medium \| MLflow version status needed stronger caveats \|.*?\|", "| Medium | MLflow version status needed stronger caveats | Retain the 3.15.2 reproducibility baseline without claiming it is latest; re-verify experimental features and distinguish synchronous evaluation orchestration from an async predict function. |", s, count=1)
s=re.sub(r"\| Amazon Bedrock Agents / AgentCore \|.*?\n", "| Amazon Bedrock Agents Classic / AgentCore | Bedrock Agents Classic documents a supervisor/collaborator model; its documentation states that the service is in maintenance mode and closed to new customers, with AgentCore identified for similar capabilities. | AWS lock-in, lifecycle status, and supervisor-centric topology; inspect portability, observability, migration, and service-specific limits. | Existing Classic estates or AWS-native evaluations that explicitly account for maintenance status; wrap source-system authorization and evidence externally. |\n", s, count=1)
# Repair one escaped URL inherited from the conversion pipeline.
s=s.replace('available\\_metrics/agents','available_metrics/agents')

# Preserve one package note in front matter; remove 22 chapter-level duplicates.
boiler='The companion package keeps platform contracts separate from OpenAI and MLflow adapters so deterministic behavior can be tested without credentials or network access.'
removed=s.count(boiler)
s=s.replace('\n'+boiler+'\n','\n')

preface='''# Preface to Book v1.0.0

Book v1.0.0 is the publication baseline for this guide and the canonical starting point for all future editions. It treats an agentic application as a governed distributed system: models may propose, while deterministic services own authority, state, effects, evidence, acceptance, and release.

The narrative follows one dependency chain. Foundations establish the deterministic shell; the reference architecture assigns ownership; the developer platform makes those controls reusable; patterns and anti-patterns guide topology; gateways and security enforce boundaries; observability and evaluation produce evidence; continuous learning converts evidence into governed change; and production operations keep the resulting system reliable and economical.

## Scope and claim discipline

External facts, protocol behavior, framework capabilities, research findings, standards, and legal or regulatory context use numbered citations such as [R05]. Architecture choices without citations are recommendations authored for this book; they must be validated against the reader’s workload, jurisdiction, threat model, provider terms, and operating constraints. A source supports only the claim stated beside it—vendor documentation does not establish production fitness, community guidance is not law, and a benchmark result does not guarantee enterprise outcomes.

## Reproducible edition

The accompanying Book v1.0.0 development package contains this canonical Markdown, the generated DOCX, source files, cover and diagrams, a reference registry, style tokens, templates, skills, build tools, validation tools, and release evidence. Future agents should modify the canonical Markdown and registries, never hand-format the release DOCX. The build and validation workflow is documented in the package README.
'''
marker='# How to use this guide'
if '# Preface to Book v1.0.0' not in s:
    s=s.replace(marker,preface+'\n'+marker,1)

part_intro={
'I':('Foundations','This Part defines the vocabulary and invariants used everywhere else. It begins with the progression from model call to production system, then turns model outputs into typed tool proposals, and finally places bounded reasoning behind a framework-neutral runtime contract. Read it before selecting orchestration patterns or products.'),
'II':('Enterprise Reference Architecture','This Part converts the foundational invariants into an enterprise system of record. It assigns ownership across experience, application, runtime, knowledge, gateway, security, governance, and operations planes, then specifies the APIs and records that let those planes evolve independently.'),
'III':('Agentic Developer Platform & SDK','This Part turns the reference architecture into a paved road for delivery teams. It separates reusable platform capabilities from domain logic, defines portable SDK contracts, and shows how Skills and domain packs move through local development, evaluation, promotion, deployment, and support.'),
'IV':('Patterns','This Part selects the smallest topology that resolves the uncertainty at hand. The chapters progress from bounded reason–act loops through routing, planning, evaluation, human control, durable execution, and a cross-category decision catalog.'),
'V':('Anti-Patterns','This Part reverses the lens. It exposes recurring architecture shapes that hide authority, state, effects, security, reliability, or operating cost, and pairs each failure with a measurable replacement pattern.'),
'VI':('Multi-Agent & Platform Integration','This Part expands beyond one runtime. It shows when specialized agents are justified and how MCP, A2A, APIs, events, and shared services can cross platform boundaries without transferring hidden authority or trust.'),
'VII':('LLM Gateway','This Part isolates model-provider concerns behind a control plane for routing, authorization, policy, privacy, budgets, resilience, telemetry, and evaluation hooks. It also distinguishes the LLM Gateway from API, agent, MCP, and workflow layers.'),
'VIII':('Security & Guardrails','This Part applies defense in depth to untrusted content, identity, delegated authority, tools, code, data, memory, multi-agent traffic, MCP servers, and the software supply chain. Each control is tied to a trust boundary, runtime decision, detection signal, and recovery path.'),
'IX':('Observability & Evaluation','This Part establishes the evidence plane. Traces reconstruct trajectories and effects; evaluations measure outcomes, safety, reliability, latency, cost, and human burden; debugging turns those signals into actionable diagnoses.'),
'X':('Continuous Learning','This Part closes the evidence-to-change loop. It separates bounded runtime adaptation from governed offline improvement and defines who may recommend, validate, approve, deploy, monitor, and reverse changes to prompts, models, tools, memory, routing, workflows, and architecture.'),
'XI':('Governance','This Part defines decision rights, risk tiers, evidence requirements, exceptions, accountability, and lifecycle oversight. It connects technical release controls to an operating model rather than treating governance as a review gate at the end.'),
'XII':('Deployment & Production Operations','This Part operationalizes the complete architecture. It covers immutable releases, promotion, rollback, disaster recovery, capacity, queueing, cost, latency, reliability, and the economics of verified—not merely generated—outcomes.'),
}
for roman,(title,intro) in part_intro.items():
    pat=rf'(# PART {roman} — [^\n]+\n\n)(?:A cohesive architecture section in the Foundations-to-Production narrative\.\n\n)?'
    s,n=re.subn(pat,lambda m:m.group(1)+intro+'\n\n',s,count=1)
    if n!=1: raise SystemExit(f'part intro not found: {roman}')

# Scoped evidence notes are deliberately narrow so every citation supports the
# adjacent external claim, not the book-authored architecture recommendation.
evidence={
3:'> **Evidence note.** Concrete adapter examples use OpenAI Agents SDK v0.22.2 and its documented agent, tool, guardrail, handoff, result, and tracing surfaces; the platform contracts remain framework-neutral. [R29][R30]',
5:'> **Evidence note.** CloudEvents defines the portable event envelope used here, while the transactional-outbox source supports atomic state/event publication and warns that consumers still require duplicate handling. [R03][R04]',
6:'> **Evidence note.** The portability layer is informed by current public agent abstractions from OpenAI, Microsoft, and Google; capability parity is not assumed and must be proven by adapter conformance tests. [R29][R31][R32]',
10:'> **Evidence note.** ReAct was introduced as a prompting paradigm that interleaves reasoning and action; its reported benchmark results motivate the loop, not an assertion that unrestricted production autonomy is safe. [R01]',
12:'> **Evidence note.** Published engineering guidance distinguishes predefined workflows from model-directed agents and recommends adding complexity only when simpler compositions are insufficient. [R27]',
14:'> **Evidence note.** Human-review interfaces should be tested against WCAG 2.2 accessibility criteria; accessibility conformance does not by itself eliminate automation bias or establish decision fairness. [R41]',
15:'> **Evidence note.** Durable-execution systems preserve workflow progress across failures and long waits; concrete integrations and replay semantics vary by backend. [R02][R36][R38]',
18:'> **Evidence note.** Public multi-agent implementation reports describe supervisor/specialist designs and substantial token/context trade-offs; these observations justify explicit topology and cost tests rather than universal multi-agent adoption. [R28][R33]',
19:'> **Evidence note.** MCP 2026-07-28 defines a stateless, self-contained protocol core for resources, prompts, and tools, while A2A v1.0.1 defines agent cards and task/message/artifact exchange. Neither protocol transfers application authorization or business acceptance automatically. [R05][R06][R07]',
21:'> **Evidence note.** The threat catalog is cross-checked against OWASP agentic-security guidance, while the trust-boundary model follows zero-trust principles that require explicit policy decisions around protected resources. [R11][R15][R16]',
23:'> **Evidence note.** The delegated-authority examples use OAuth token exchange, resource indicators, and protected-resource metadata as protocol building blocks; deployment still requires workload-specific issuer, audience, proof, revocation, and policy controls. [R08][R09][R10]',
25:'> **Evidence note.** SBOM inventory and SLSA build provenance answer different supply-chain questions. Privacy obligations depend on jurisdiction; the GDPR source is cited only for EU legal context, not as universal legal advice. [R17][R18][R39]',
26:'> **Evidence note.** OpenTelemetry GenAI semantic conventions remain in Development and have moved to a dedicated repository; isolate them behind an internal mapping layer. Phoenix is one implementation option for OpenInference/OTel-based tracing and evaluation. [R19][R23]',
27:'> **Evidence note.** The evaluation architecture maps to current capabilities documented by MLflow, DeepEval, Ragas, LangSmith, and OpenAI. Tool names and APIs are examples; the durable contract is dataset + release graph + scorer versions + trace/effect evidence. [R20][R21][R22][R24][R25][R26]',
29:'> **Evidence note.** NIST AI RMF and its Generative AI Profile are voluntary risk guidance; ISO/IEC 42001 specifies an AI management system; the EU AI Act source provides official implementation context. Applicability and legal obligations require qualified jurisdiction-specific review. [R12][R13][R14][R40]',
30:'> **Evidence note.** The incident lifecycle aligns with NIST SP 800-61 Rev. 3’s integration of incident response into cybersecurity risk management; agent-specific containment and recovery remain workload-defined. [R42]',
31:'> **Evidence note.** Little’s Law relates average items in a stable system to arrival rate and average time in system. The capacity equations in this chapter are planning approximations and must be calibrated by load tests. [R43]',
}
for num,note in evidence.items():
    pat=rf'(^# {num:02d} — [^\n]+\n)'
    s,n=re.subn(pat,lambda m:m.group(1)+'\n'+note+'\n',s,count=1,flags=re.M)
    if n!=1: raise SystemExit(f'chapter evidence insertion failed: {num}')

# Add framework ecosystem citation scope to Appendix D.
appd='''> **Evidence note.** The landscape summary is based on current framework documentation for OpenAI Agents SDK, Microsoft Agent Framework, Google ADK, Amazon Bedrock multi-agent collaboration, LangGraph, LlamaIndex Workflows, PydanticAI durable execution, Dapr Agents, and DBOS. It records declared capabilities, not a comparative production certification. [R29][R31][R32][R33][R34][R35][R36][R37][R38]
'''
s=s.replace('# Appendix D — Framework landscape\n','# Appendix D — Framework landscape\n\n'+appd,1)

transitions={
1:'With the system boundary established, Chapter 2 converts model intent into typed, validated tool proposals and a deterministic commit path.',
2:'With tools bounded, Chapter 3 defines the runtime contract that keeps applications portable across agent frameworks and model providers.',
3:'The runtime now has a stable boundary; Chapter 4 places it inside the complete enterprise reference architecture.',
4:'The planes are visible; Chapter 5 turns their responsibilities into APIs, records, event envelopes, and trust boundaries.',
5:'The reference architecture is now concrete enough to productize; Chapter 6 defines the reusable developer platform and SDK.',
6:'With platform responsibilities separated from application logic, Chapter 7 specifies the developer workflow that makes the paved road usable.',
7:'The delivery path is established; Chapter 8 packages repeatable behavior as versioned Skills with explicit contracts and lifecycle controls.',
8:'Individual Skills are governable; Chapter 9 composes them into domain packs without dissolving ownership or compatibility boundaries.',
9:'The platform and capability model are complete; Chapter 10 begins the pattern sequence with the smallest bounded reasoning loop.',
10:'A bounded reason–act loop handles local uncertainty; Chapter 11 adds routing and handoff when known paths or specialists should own the work.',
11:'Routing selects among known capabilities; Chapter 12 addresses tasks whose decomposition must itself be proposed and validated.',
12:'Planning creates an executable structure; Chapter 13 adds independent evaluation and bounded revision without self-certification.',
13:'Automated evaluation can improve candidates; Chapter 14 identifies decisions that require explicit human authority, correction, or recourse.',
14:'Human control introduces waits and resumptions; Chapter 15 makes those waits durable and gives long-running work explicit state and recovery.',
15:'The core patterns are now defined; Chapter 16 compares them across uncertainty, authority, latency, evidence, and operating cost.',
16:'Pattern selection is easier when failure shapes are visible; Chapter 17 recasts recurring anti-patterns as measurable replacement decisions.',
17:'After removing unsafe local architectures, Chapter 18 considers when multiple agents add justified specialization rather than accidental complexity.',
18:'Multi-agent collaboration inside one platform is only part of the problem; Chapter 19 governs cross-platform tools, agents, APIs, and events.',
19:'External integrations are bounded; Chapter 20 isolates model-provider access and policy in the LLM Gateway control plane.',
20:'The gateway controls model access, but not the entire attack surface; Chapter 21 introduces defense in depth across all agentic trust boundaries.',
21:'The threat model is established; Chapter 22 applies it to context, retrieval, memory, and state—the data surfaces most likely to carry hidden instructions.',
22:'Context and state are bounded; Chapter 23 determines whose authority may flow through the system and how that authority narrows across hops.',
23:'Identity and delegated authority answer who may ask; Chapter 24 proves whether a specific tool effect may execute, commit, retry, or recover.',
24:'Protected effects are governed; Chapter 25 contains the remaining execution, egress, data, privacy, and supply-chain blast radius.',
25:'Security controls now produce events and evidence; Chapter 26 turns those signals into end-to-end traces that operators can reconstruct.',
26:'Tracing explains what happened; Chapter 27 determines whether the trajectory and outcome were acceptable and whether a change is safe to ship.',
27:'Evaluation supplies comparable evidence; Chapter 28 turns that evidence into a governed learning and improvement lifecycle.',
28:'The improvement loop proposes and validates change; Chapter 29 assigns decision rights, risk tiers, approvals, exceptions, and accountability.',
29:'Governance defines who may release change; Chapter 30 makes releases immutable, promotable, observable, reversible, and recoverable.',
30:'The release lifecycle is controlled; Chapter 31 sizes the system and optimizes cost, latency, capacity, and reliability around verified outcomes.',
31:'The architecture narrative is complete. The appendices provide decision aids, runbooks, contracts, framework evidence, references, maintenance criteria, and production acceptance checks for implementation and future editions.',
}
# Insert transitions before the next chapter/appendix/part heading.
chap=list(re.finditer(r'^# (\d{2}) — .+$',s,re.M))
for m in reversed(chap):
    n=int(m.group(1)); start=m.start(); nextm=re.search(r'^# (?:(?:\d{2}) —|PART |Appendix )',s[m.end():],re.M)
    end=m.end()+nextm.start() if nextm else len(s)
    block=s[start:end].rstrip()
    if '## Transition to' in block: continue
    label='the appendices' if n==31 else f'Chapter {n+1}'
    addition=f'\n\n## Transition to {label}\n\n{transitions[n]}\n\n'
    s=s[:end]+addition+s[end:]

# Build a professional numbered bibliography.
category_order=[
 ('Research foundations',{'research'}),
 ('Protocols, identity, and event standards',{'protocol specification','internet standard','standard','observability standard'}),
 ('Security, governance, law, and assurance',{'official guidance','community guidance','community standard','law','official legal guidance'}),
 ('Frameworks, evaluation, and industry implementation guidance',{'framework documentation','framework release','vendor documentation','industry guidance','industry report','architecture pattern'}),
]
used=set(re.findall(r'\[(R\d{2})\]',s))
lines=['# Appendix K — References','',
'## Citation policy','',
'References are numbered by stable registry identifier. Each citation supports only the scoped claim recorded in `config/references.json`; access dates document the verification point for online material. Standards, official guidance, community guidance, vendor documentation, research, and law are deliberately labeled rather than treated as equivalent authority.','']
seen=set()
for heading,types in category_order:
    group=[r for r in REFS if r['type'] in types and r['id'] not in seen]
    if not group: continue
    lines+=['## '+heading,'']
    for r in group:
        seen.add(r['id'])
        lines.append(f"* **[{r['id']}]** {r['author_or_organization']} ({r['year']}). *{r['title']}*. {r['publication_or_version']}. [Primary or authoritative source]({r['url']}). Accessed 13 September 2026. **Supports:** {r['supports']}")
    lines.append('')
# Any uncategorized entries.
for r in REFS:
    if r['id'] not in seen:
        lines.append(f"* **[{r['id']}]** {r['author_or_organization']} ({r['year']}). *{r['title']}*. {r['publication_or_version']}. [Source]({r['url']}). Accessed 13 September 2026. **Supports:** {r['supports']}")
refs_md='\n'.join(lines).rstrip()+'\n\n'
s,n=re.subn(r'# Appendix K — Selected primary references\n.*?(?=^# Appendix L — )',refs_md,s,count=1,flags=re.S|re.M)
if n!=1: raise SystemExit('Appendix K replacement failed')

# Replace the former link list with a concise claim-to-source matrix.
ledger='''# Appendix M — Citation and Claim Traceability Matrix

| **Claim family** | **Book locations** | **Source IDs** | **What the sources establish** | **What remains a book recommendation** |
| --- | --- | --- | --- | --- |
| ReAct reasoning/action loop | Chapter 10 | R01 | Published ReAct method and reported experiments | Production bounds, budgets, authorization, and acceptance |
| Durable execution | Chapters 15, 30 | R02, R36, R38 | Declared durable workflow concepts and integrations | Backend selection, state model, recovery objectives, and replay tests |
| Events and outbox | Chapter 5 | R03, R04 | Event envelope and outbox pattern semantics | Northstar schemas, ownership, deduplication window, and reconciliation |
| MCP and A2A | Chapter 19 | R05–R07 | Normative protocol behavior and authorization surfaces | Enterprise policy, trust, compatibility, and business acceptance |
| Delegated OAuth authority | Chapter 23 | R08–R10 | Token exchange, resource indicators, and protected-resource metadata | Capability envelope, spend/purpose narrowing, and revocation architecture |
| Zero trust and agent security | Chapter 21 | R11, R15, R16 | Zero-trust principles and current agentic threat guidance | Defense-in-depth topology, control ownership, and recovery design |
| AI governance | Chapter 29 | R12–R14, R40 | Voluntary NIST guidance, ISO management-system scope, and EU implementation context | Risk tiers, committees, evidence gates, and enterprise applicability decisions |
| Supply chain and privacy | Chapter 25 | R17, R18, R39 | SLSA provenance, SBOM resources, and EU privacy law | Build policy, retention design, jurisdiction mapping, and acceptance tests |
| Observability semantics | Chapter 26 | R19, R23 | Emerging GenAI telemetry semantics and Phoenix capabilities | Internal canonical span model, redaction policy, retention, and SLOs |
| Evaluation systems | Chapter 27 | R20–R26 | Current documented evaluation, feedback, dataset, and tracing capabilities | Metric selection, thresholds, judges, sampling, and promotion policy |
| Agent frameworks | Chapters 3, 6; Appendix D | R29–R38 | Declared framework capabilities at the verification date | Portability contracts, conformance matrix, support tier, and vendor choice |
| Human-interface accessibility | Chapter 14 | R41 | WCAG 2.2 success criteria | Approval UX, anti-bias prompts, reviewer staffing, and recourse |
| Incident response | Chapter 30 | R42 | NIST incident-response integration guidance | Agent-specific kill switches, evidence capture, and recovery runbooks |
| Queueing and capacity | Chapter 31 | R43 | Little’s Law | Workload model, retry multiplier, utilization target, and cost limits |

## Verification rule

A future agent may update a cited claim only when the adjacent source still supports it or when the reference registry and this matrix are revised in the same change. Link availability alone is insufficient: the title, version, source class, claim scope, and relevant text must be checked. Legal and regulatory statements always require qualified review for the applicable jurisdiction and date.

'''
s,n=re.subn(r'# Appendix M — Grounding and primary-source ledger\n.*?(?=^# Appendix N — )',ledger,s,count=1,flags=re.S|re.M)
if n!=1: raise SystemExit('Appendix M replacement failed')

# Add release-specific editorial record to Appendix L.
release_note='''## Book v1.0.0 publication release

* Established semantic version 1.0.0 as the canonical publication and future-development baseline.
* Reviewed all 31 chapters and 15 appendices as one dependency-ordered narrative; added specific Part orientations and chapter-to-chapter transitions.
* Removed repeated package boilerplate and consolidated maintenance instructions in the development package.
* Replaced duplicate source lists with a numbered References section and a claim-to-source traceability matrix.
* Added scoped evidence notes for protocols, frameworks, standards, research, security guidance, governance, accessibility, incident response, and queueing claims.
* Encoded the visual and structural system in machine-readable configuration, reusable build/validation scripts, templates, and agent Skills.

'''
s=s.replace('# Appendix L — Final correction and closure log\n','# Appendix L — Release history and editorial closure\n\n'+release_note,1)

# Front-matter package guidance.
package_note='''## Canonical-source rule

The Markdown manuscript is the semantic source of truth. DOCX, Notion release metadata, split chapter files, and rendered validation artifacts are generated or synchronized representations. Typography and pagination may differ by medium; chapter order, prose, examples, tables, code, diagrams, captions, citations, and references must remain semantically aligned.
'''
s=s.replace('# Hierarchical Table of Contents',package_note+'\n# Hierarchical Table of Contents',1)

# Normalize trailing whitespace and blank runs without touching code lines.
lines=s.splitlines(); clean=[]; in_code=False; blank=0
for line in lines:
    if line.startswith('```'): in_code=not in_code
    line=line.rstrip() if not in_code else line.rstrip('\n')
    if not line:
        blank+=1
        if blank>2: continue
    else: blank=0
    clean.append(line)
s='\n'.join(clean).strip()+'\n'
OUT.parent.mkdir(parents=True,exist_ok=True); DIST.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(s,encoding='utf-8'); DIST.write_text(s,encoding='utf-8')

# Deterministic split: front, 12 Parts, appendices.
parts_dir=ROOT/'source/parts'; parts_dir.mkdir(parents=True,exist_ok=True)
for p in parts_dir.glob('*.md'): p.unlink()
part_matches=list(re.finditer(r'^# PART ([IVX]+) — .+$',s,re.M))
app_match=re.search(r'^# Appendix A — ',s,re.M)
front_end=part_matches[0].start()
(parts_dir/'00-front-matter.md').write_text(s[:front_end].rstrip()+'\n',encoding='utf-8')
for i,m in enumerate(part_matches):
    end=part_matches[i+1].start() if i+1<len(part_matches) else app_match.start()
    (parts_dir/f'{i+1:02d}-part-{m.group(1).lower()}.md').write_text(s[m.start():end].rstrip()+'\n',encoding='utf-8')
(parts_dir/'13-appendices.md').write_text(s[app_match.start():].rstrip()+'\n',encoding='utf-8')

used=set(re.findall(r'\[(R\d{2})\]',s)); known={r['id'] for r in REFS}
report={'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'canonical_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'source_bytes':SRC.stat().st_size,'canonical_bytes':OUT.stat().st_size,'removed_repeated_package_paragraphs':removed,'parts':len(part_matches),'chapters':len(re.findall(r'^# \d{2} — ',s,re.M)),'appendices':len(re.findall(r'^# Appendix [A-O] — ',s,re.M)),'diagram_markers':len(re.findall(r'^\[\[DIAGRAM:',s,re.M)),'code_blocks':len(re.findall(r'^```',s,re.M))//2,'citation_occurrences':len(re.findall(r'\[R\d{2}\]',s)),'cited_reference_ids':sorted(used),'uncited_registry_ids':sorted(known-used),'unknown_citation_ids':sorted(used-known),'stale_version_labels':sorted(set(re.findall(r'v(?:2\.[01]|3\.[01])',s))),'split_files':len(list(parts_dir.glob('*.md')))}
(ROOT/'reports/editorial-transformation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
