"""Offline command line entry point for the cumulative mortgage case."""

from __future__ import annotations

import argparse
import json
import sys

from .stages.c01_baseline import run as run_c01
from .stages.c02_deterministic_shell import run as run_c02
from .stages.c03_agent_runtime import run as run_c03


RUNNERS = {1: run_c01, 2: run_c02, 3: run_c03}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a synthetic mortgage checkpoint.")
    parser.add_argument("--chapter", type=int, required=True, help="chapter/checkpoint number")
    parser.add_argument("--scenario", default="happy_path")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="use deterministic local components (the default execution profile)",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    runner = RUNNERS.get(args.chapter)
    if runner is None:
        print(
            f"C{args.chapter:02d} is not implemented in this checkpoint; "
            "the current foundation covers Chapters 1-3.",
            file=sys.stderr,
        )
        return 2
    try:
        report = runner(args.scenario)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(report.model_dump(mode="json"), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
