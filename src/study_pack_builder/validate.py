from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ValidationIssue:
    line: int
    code: str
    message: str


def validate_vocab_csv(path: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    seen_words: set[str] = set()

    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        fieldnames = {name.strip().lower() for name in (reader.fieldnames or [])}
        if "word" not in fieldnames:
            issues.append(ValidationIssue(1, "missing-column", "Missing required column: word"))
        if "definition" not in fieldnames and "meaning" not in fieldnames:
            issues.append(ValidationIssue(1, "missing-column", "Missing required column: definition"))
        if issues:
            return issues

        for row_number, row in enumerate(reader, start=2):
            normalized = {key.strip().lower(): (value or "").strip() for key, value in row.items() if key}
            word = normalized.get("word", "")
            definition = normalized.get("definition") or normalized.get("meaning", "")

            if not word:
                issues.append(ValidationIssue(row_number, "missing-word", "Missing required word"))
                continue
            lowered = word.casefold()
            if lowered in seen_words:
                issues.append(ValidationIssue(row_number, "duplicate-word", f"Duplicate word: {word}"))
            seen_words.add(lowered)

            if not definition:
                issues.append(ValidationIssue(row_number, "missing-definition", "Missing required definition"))

    return issues


def format_issues(issues: list[ValidationIssue]) -> str:
    if not issues:
        return "No validation issues found.\n"
    lines = ["Validation issues:"]
    for issue in issues:
        lines.append(f"- line {issue.line}: {issue.code}: {issue.message}")
    return "\n".join(lines) + "\n"
