from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class OcrCleanupResult:
    rows: list[dict[str, str]]
    warnings: list[str]


def clean_ocr_text(source: str) -> OcrCleanupResult:
    rows: list[dict[str, str]] = []
    warnings: list[str] = []

    for line_number, raw_line in enumerate(source.splitlines(), start=1):
        line = _normalize_line(raw_line)
        if not line:
            continue
        parsed = _parse_line(line)
        if parsed is None:
            warnings.append(f"line {line_number}: skipped malformed OCR row")
            continue
        rows.append(parsed)

    return OcrCleanupResult(rows=rows, warnings=warnings)


def write_ocr_csv(result: OcrCleanupResult, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["word", "definition", "synonyms", "example"])
        writer.writeheader()
        writer.writerows(result.rows)


def _normalize_line(value: str) -> str:
    value = value.replace("\t", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _parse_line(line: str) -> dict[str, str] | None:
    line = re.sub(r"^\s*\d+[\.)]?\s*", "", line)
    match = re.match(
        r"^(?P<word>[A-Za-z][A-Za-z'/-]*)\s+"
        r"(?P<definition>.+?)\s+"
        r"(?P<synonyms>[A-Za-z][A-Za-z'/-]*(?:\s*;\s*[A-Za-z][A-Za-z'/-]*)+)\s+"
        r"(?P<example>.+[.!?])$",
        line,
    )
    if not match:
        return None
    return {key: _normalize_line(value) for key, value in match.groupdict().items()}
