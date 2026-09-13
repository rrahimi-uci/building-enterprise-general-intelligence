"""Keep every example run hermetic: no network, no API key, no shared state."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent
if str(ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ROOT.parent))


@pytest.fixture(scope="session", autouse=True)
def _mlflow_backend(tmp_path_factory):
    """One tracking backend for the whole session.

    MLflow caches its tracking client and the resolved experiment globally, so
    pointing each test at its own database silently splits writes and reads
    across two stores: a trace written by one test is then not found by the
    assertion that follows it. A session-scoped store matches how MLflow is
    actually used and keeps the tests honest.

    MLflow 3.15 also put the filesystem store into maintenance mode for traces,
    so this has to be a database URI -- the same choice a real deployment makes.
    """
    db = tmp_path_factory.mktemp("mlflow") / "mlflow.db"
    os.environ["MLFLOW_TRACKING_URI"] = f"sqlite:///{db}"
    os.environ["MLFLOW_ENABLE_SYSTEM_METRICS_LOGGING"] = "false"
    # Traces export on a background queue by default, so a test that reads one
    # back immediately races the writer. Production keeps the async queue.
    os.environ["MLFLOW_ENABLE_ASYNC_TRACE_LOGGING"] = "false"
    yield


@pytest.fixture(autouse=True)
def _no_credentials(monkeypatch):
    # A missing key is the point: if an example ever reaches a real provider,
    # the test must fail loudly rather than quietly billing someone.
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
