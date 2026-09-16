"""Stable errors exposed by the teaching boundary."""


class MortgageCaseError(ValueError):
    """A safe, typed failure that does not expose provider or document payloads."""

    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


class ProposalRejected(MortgageCaseError):
    """A proposal failed deterministic validation before any tool dispatch."""
