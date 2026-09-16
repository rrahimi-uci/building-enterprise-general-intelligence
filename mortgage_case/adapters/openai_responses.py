"""Optional direct OpenAI Python SDK adapter for Chapter 1.

The adapter sends document metadata, not raw document bytes. It is never used
by the mandatory offline path and it cannot create a lending decision or effect.
"""

from __future__ import annotations

from typing import Any

from ..domain.case import MortgageCase
from ..domain.evidence import CaseSummaryCandidate


class OpenAIResponsesSummaryModel:
    """Translate the optional Responses API result into a platform-owned schema."""

    def __init__(self, *, client: Any = None, model: str = "gpt-4.1-mini") -> None:
        self.client = client
        self.model = model

    async def summarize(self, case: MortgageCase) -> CaseSummaryCandidate:
        """Run one synthetic, read-only structured-output request."""

        client = self.client
        if client is None:
            from openai import AsyncOpenAI  # optional dependency, imported on use

            client = AsyncOpenAI()
        response = await client.responses.parse(
            model=self.model,
            input=(
                "Summarize the available mortgage document metadata. "
                "Do not decide eligibility or approval.\n"
                + "\n".join(f"{d.document_id}: {d.kind}" for d in case.available_documents)
            ),
            text_format=CaseSummaryCandidate,
        )
        return CaseSummaryCandidate.model_validate(response.output_parsed)
