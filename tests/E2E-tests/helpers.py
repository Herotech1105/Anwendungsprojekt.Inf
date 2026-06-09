"""Shared formatting helpers for E2E test output."""

import sys
from datetime import datetime

PASS = "[PASS]"
FAIL = "[FAIL]"
SKIP = "[SKIP]"
DIVIDER = "-" * 70

results: list[tuple[str, str, str]] = []


def record(status: str, name: str, detail: str = "") -> None:
    results.append((status, name, detail))
    print(f"  {status}  {name}")
    if detail:
        for line in detail.strip().split("\n"):
            print(f"         {line}")


def print_header(title: str) -> None:
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 70}\n")


def print_summary() -> None:
    passed = sum(1 for s, _, _ in results if s == PASS)
    failed = sum(1 for s, _, _ in results if s == FAIL)
    skipped = sum(1 for s, _, _ in results if s == SKIP)
    total = len(results)

    print(f"\n{'=' * 70}")
    print(f"  RESULT:  {passed} passed / {failed} failed / {skipped} skipped / {total} total")
    print(f"{'=' * 70}")

    if failed > 0:
        print(f"\n  Failed:")
        for status, name, detail in results:
            if status == FAIL:
                print(f"    - {name}: {detail}")
    print()
    return failed


def exit_with_result() -> None:
    failed = print_summary()
    sys.exit(1 if failed > 0 else 0)
