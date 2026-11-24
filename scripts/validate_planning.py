#!/usr/bin/env python3
"""Validate the repository's planning CSVs and README-relative links."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


MILESTONE_COLUMNS = [
    "id",
    "start_week",
    "end_week",
    "title",
    "gate",
    "owner",
    "exit_criterion",
]
BACKLOG_COLUMNS = [
    "id",
    "milestone",
    "discipline",
    "title",
    "depends_on",
    "gate",
    "definition_of_done",
]
EXPECTED_MILESTONES = {f"M{number}" for number in range(10)}
EXPECTED_MILESTONE_ORDER = [f"M{number}" for number in range(10)]
EXPECTED_GATES = {"G0", "G1", "G2", "G3", "G4a", "G4b", "G4", "POST_G4", "G5", "NEW_GATES"}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")


def _read_csv(root: Path, relative_path: str, columns: list[str], errors: list[str]) -> list[dict[str, str]]:
    path = root / relative_path
    try:
        with path.open(newline="", encoding="utf-8-sig") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != columns:
                errors.append(
                    f"{relative_path}: expected columns {columns}, got {reader.fieldnames}"
                )
                return []

            rows: list[dict[str, str]] = []
            for line_number, row in enumerate(reader, start=2):
                if None in row:
                    errors.append(f"{relative_path}:{line_number}: unexpected extra CSV cells")
                    continue
                cleaned = {key: (value or "").strip() for key, value in row.items()}
                rows.append(cleaned)
            return rows
    except OSError as exc:
        errors.append(f"{relative_path}: cannot read file: {exc}")
        return []
    except csv.Error as exc:
        errors.append(f"{relative_path}: invalid CSV: {exc}")
        return []


def _check_unique_ids(rows: list[dict[str, str]], key: str, label: str, errors: list[str]) -> set[str]:
    seen: set[str] = set()
    for index, row in enumerate(rows, start=2):
        value = row.get(key, "")
        if not value:
            errors.append(f"{label}:{index}: {key} is required")
        elif value in seen:
            errors.append(f"{label}:{index}: duplicate {key} {value!r}")
        seen.add(value)
    return seen


def _check_readme_links(root: Path, errors: list[str]) -> int:
    readme = root / "README.md"
    try:
        content = readme.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"README.md: cannot read file: {exc}")
        return 0

    checked = 0
    repository_root = root.resolve()
    for match in MARKDOWN_LINK.finditer(content):
        target = match.group(1)
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue

        checked += 1
        resolved = (readme.parent / unquote(parsed.path)).resolve()
        try:
            resolved.relative_to(repository_root)
        except ValueError:
            errors.append(f"README.md: relative link escapes repository: {target}")
            continue
        if not resolved.exists():
            errors.append(f"README.md: relative link target does not exist: {target}")
    return checked


def validate_repository(root: Path) -> tuple[list[str], dict[str, int]]:
    root = root.resolve()
    errors: list[str] = []
    milestones = _read_csv(root, "planning/milestones_506c.csv", MILESTONE_COLUMNS, errors)
    backlog = _read_csv(root, "planning/backlog_506c.csv", BACKLOG_COLUMNS, errors)

    milestone_ids = _check_unique_ids(
        milestones, "id", "planning/milestones_506c.csv", errors
    )
    milestone_order = [milestone.get("id", "") for milestone in milestones]
    if milestone_order != EXPECTED_MILESTONE_ORDER:
        errors.append(
            "planning/milestones_506c.csv: expected row order M0-M9; "
            f"got {milestone_order}"
        )
    if milestone_ids != EXPECTED_MILESTONES:
        missing = sorted(EXPECTED_MILESTONES - milestone_ids)
        unexpected = sorted(milestone_ids - EXPECTED_MILESTONES)
        errors.append(
            "planning/milestones_506c.csv: expected M0-M9; "
            f"missing={missing}, unexpected={unexpected}"
        )

    milestone_gates: dict[str, str] = {}
    for index, milestone in enumerate(milestones, start=2):
        milestone_id = milestone.get("id", "")
        gate = milestone.get("gate", "")
        milestone_gates[milestone_id] = gate
        if gate not in EXPECTED_GATES:
            errors.append(
                f"planning/milestones_506c.csv:{index}: unknown gate {gate!r}"
            )
        try:
            start_week = int(milestone.get("start_week", ""))
            end_week = int(milestone.get("end_week", ""))
            if start_week < 1 or end_week < start_week:
                raise ValueError
        except ValueError:
            errors.append(
                f"planning/milestones_506c.csv:{index}: expected positive week range with start_week <= end_week"
            )

    backlog_ids = _check_unique_ids(backlog, "id", "planning/backlog_506c.csv", errors)
    dependencies: dict[str, list[str]] = {}
    for index, task in enumerate(backlog, start=2):
        task_id = task.get("id", "")
        milestone_id = task.get("milestone", "")
        gate = task.get("gate", "")
        if gate not in EXPECTED_GATES:
            errors.append(
                f"planning/backlog_506c.csv:{index}: unknown gate {gate!r}"
            )
        if milestone_id not in milestone_ids:
            errors.append(
                f"planning/backlog_506c.csv:{index}: unknown milestone {milestone_id!r}"
            )
        elif gate != milestone_gates.get(milestone_id):
            errors.append(
                f"planning/backlog_506c.csv:{index}: gate {gate!r} does not match "
                f"milestone {milestone_id!r} gate {milestone_gates[milestone_id]!r}"
            )
        task_dependencies = [
            value.strip()
            for value in task.get("depends_on", "").split(";")
            if value.strip()
        ]
        dependencies[task_id] = task_dependencies
        for dependency in task_dependencies:
            if dependency not in backlog_ids:
                errors.append(
                    f"planning/backlog_506c.csv:{index}: unknown dependency {dependency!r}"
                )
            if dependency == task_id:
                errors.append(
                    f"planning/backlog_506c.csv:{index}: task {task_id!r} depends on itself"
                )

    state: dict[str, int] = {}  # 0/unseen, 1/visiting, 2/complete

    def visit(task_id: str, trail: list[str]) -> None:
        current = state.get(task_id, 0)
        if current == 2:
            return
        if current == 1:
            cycle = " -> ".join([*trail, task_id])
            errors.append(f"planning/backlog_506c.csv: dependency cycle: {cycle}")
            return
        state[task_id] = 1
        for dependency in dependencies.get(task_id, []):
            if dependency in dependencies:
                visit(dependency, [*trail, task_id])
        state[task_id] = 2

    for task_id in dependencies:
        visit(task_id, [])

    readme_links = _check_readme_links(root, errors)
    summary = {
        "milestones": len(milestones),
        "backlog_items": len(backlog),
        "readme_relative_links": readme_links,
    }
    return errors, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the parent of scripts/)",
    )
    args = parser.parse_args()
    errors, summary = validate_repository(args.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "Planning validation passed: "
        f"{summary['milestones']} milestones, "
        f"{summary['backlog_items']} backlog items, "
        f"{summary['readme_relative_links']} README relative links."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
