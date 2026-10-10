"""A scoped operational kill switch.

A kill switch stops new risky work at the narrowest safe scope. A rule must name
at least one scope; a rule with no scope would stop the whole platform, which is
an outage, not containment. A request is blocked when every scope the rule names
matches it. Unnamed scopes match anything, so a rule naming only a tool version
stops that version for every tenant, agent, and model route.
"""
from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

# --8<-- example:start


class KillSwitchRule(BaseModel):
    tenant_id: str | None = None
    agent_version: str | None = None
    tool_version: str | None = None
    model_route: str | None = None
    reason: str = Field(min_length=1)

    @model_validator(mode="after")
    def at_least_one_scope(self) -> "KillSwitchRule":
        if not any((self.tenant_id, self.agent_version, self.tool_version, self.model_route)):
            raise ValueError("kill switch requires a scope")
        return self

    def blocks(self, *, tenant_id: str, agent_version: str, tool_version: str | None,
               model_route: str) -> bool:
        checks = (
            self.tenant_id in (None, tenant_id),
            self.agent_version in (None, agent_version),
            self.tool_version in (None, tool_version),
            self.model_route in (None, model_route),
        )
        return all(checks)


# --8<-- example:end
