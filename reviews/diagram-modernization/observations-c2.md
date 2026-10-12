# Content observations, group c2 (recorded, not acted on)

- `reference-architecture` (Figure 4-1): the dotted evidence edges come from three producers (Request validator, Topology . handoffs, Egress proxy) to the OTel collector, and the dashed control edges all leave PDP / PEP. This follows the source and its comment ("one decision point, one collection point"), but the surrounding prose says telemetry and policy apply at every plane; the figure shows only three of each by design.
- `reference-architecture`: plane order in the figure (Runtime, Knowledge, Agent, Gateways, Systems) differs from the band order in `system-overview` (Agent runtime, Collaboration, Knowledge, Control points, Systems of record). Both are as in the sources; the two figures decompose differently (the source comment says so).
- `knowledge-lifecycle` (Figure 5-4): the label "request changes . back to Draft" names a Draft state that the figure does not draw (the dashed edge returns to the knowledge graph). Kept as written.
- `knowledge-lifecycle`: the original had three invisible ordering edges (sources>repair, repair>gates, repair>registry); they carry no meaning and are not drawn, so 17 visible edges remain.
- `system-overview` (Figure 1-3): the "Systems of record" badge is an em dash (no Part), kept as in the source. "Knowledge" carries Part II, which is also in the Channels badge (II . IV); kept.
