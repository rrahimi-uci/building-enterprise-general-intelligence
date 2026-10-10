from __future__ import annotations

import asyncio

from mortgage_case.adapters.openai_responses import OpenAIResponsesSummaryModel
from mortgage_case.domain.case import load_anchor_case
from mortgage_case.domain.evidence import CaseSummaryCandidate


class _FakeResponses:
    def __init__(self) -> None:
        self.kwargs: dict[str, object] | None = None

    async def parse(self, **kwargs: object):
        self.kwargs = kwargs

        class _Response:
            output_parsed = CaseSummaryCandidate(
                status="NEEDS_INPUT",
                summary="A required income document is missing.",
                available_document_ids=("APP-000184", "PAY-000184-01", "PUR-000184"),
                missing_document_kinds=("pay_statement",),
                proposed_next_control="Request the missing document",
            )

        return _Response()


class _FakeAsyncClient:
    def __init__(self) -> None:
        self.responses = _FakeResponses()


def test_direct_openai_responses_adapter_uses_pinned_structured_output_contract():
    client = _FakeAsyncClient()
    result = asyncio.run(
        OpenAIResponsesSummaryModel(client=client).summarize(load_anchor_case())
    )

    assert result.status == "NEEDS_INPUT"
    assert result.lending_decision == "not_provided"
    assert client.responses.kwargs is not None
    assert client.responses.kwargs["model"] == "gpt-4.1-mini"
    assert client.responses.kwargs["text_format"] is CaseSummaryCandidate
    prompt = str(client.responses.kwargs["input"])
    assert "Alex Morgan" not in prompt
    assert "101 Example Avenue" not in prompt
