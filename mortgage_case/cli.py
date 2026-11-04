"""Offline command line entry point for the cumulative mortgage case."""

from __future__ import annotations

import argparse
import json
import sys

from .stages.c01_baseline import run as run_c01
from .stages.c02_deterministic_shell import run as run_c02
from .stages.c03_agent_runtime import run as run_c03
from .stages.c04_reference_architecture import run as run_c04
from .stages.c05_knowledge import run as run_c05
from .stages.c06_context import run as run_c06
from .stages.c07_paved_road import run as run_c07
from .stages.c08_skills import run as run_c08
from .stages.c09_skill_pack import run as run_c09
from .stages.c10_react import run as run_c10
from .stages.c11_routing import run as run_c11
from .stages.c12_planning import run as run_c12
from .stages.c13_reflection import run as run_c13
from .stages.c14_human_review import run as run_c14
from .stages.c15_durable import run as run_c15
from .stages.c16_patterns import run as run_c16
from .stages.c17_anti_patterns import run as run_c17
from .stages.c18_multi_agent import run as run_c18
from .stages.c19_protocols import run as run_c19
from .stages.c20_containment import run as run_c20
from .stages.c21_identity import run as run_c21
from .stages.c22_effects import run as run_c22
from .stages.c23_sandbox_privacy import run as run_c23
from .stages.c24_tracing import run as run_c24
from .stages.c25_evaluation import run as run_c25
from .stages.c26_governance import run as run_c26
from .stages.c27_release import run as run_c27
from .stages.c28_capacity import run as run_c28


RUNNERS = {
    chapter: runner
    for chapter, runner in enumerate(
        (
            run_c01, run_c02, run_c03, run_c04, run_c05, run_c06, run_c07,
            run_c08, run_c09, run_c10, run_c11, run_c12, run_c13, run_c14,
            run_c15, run_c16, run_c17, run_c18, run_c19, run_c20, run_c21,
            run_c22, run_c23, run_c24, run_c25, run_c26, run_c27, run_c28,
        ),
        start=1,
    )
}


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
            f"C{args.chapter:02d} is not registered; choose a chapter from 1 through 28.",
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
