from __future__ import annotations

import csv
import html
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class VocabEntry:
    word: str
    definition: str
    synonyms: str = ""
    example: str = ""


def load_vocab_csv(path: Path) -> list[VocabEntry]:
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError("CSV must include a header row.")

        normalized = {name.strip().lower(): name for name in reader.fieldnames}
        word_key = normalized.get("word")
        definition_key = normalized.get("definition") or normalized.get("meaning")
        if not word_key or not definition_key:
            raise ValueError("CSV must include word and definition columns.")

        entries: list[VocabEntry] = []
        for row in reader:
            word = _clean(row.get(word_key, ""))
            definition = _clean(row.get(definition_key, ""))
            if not word or not definition:
                continue
            entries.append(
                VocabEntry(
                    word=word,
                    definition=definition,
                    synonyms=_clean(_optional_value(row, normalized, "synonyms")),
                    example=_clean(_optional_value(row, normalized, "example")),
                )
            )
    return entries


def render_vocab_markdown(
    entries: Iterable[VocabEntry],
    *,
    title: str = "Study Pack",
    group_size: int = 25,
) -> str:
    grouped = _groups(list(entries), group_size)
    lines = [
        f"# {title}",
        "",
        f"- Total entries: {sum(len(group) for group in grouped)}",
        f"- Group size: {group_size}",
        "",
        "## Study Method",
        "",
        "| Step | Action | Done |",
        "|---|---|---|",
        "| 1 | Read the word, definition, synonyms, and example aloud. | [ ] |",
        "| 2 | Hide the definition and recall it from the word. | [ ] |",
        "| 3 | Hide the word and recall it from the definition. | [ ] |",
        "| 4 | Mark missed items and repeat them after a short break. | [ ] |",
        "",
    ]

    for group_index, group in enumerate(grouped, 1):
        lines.extend(
            [
                f"## Set {group_index}",
                "",
                "| # | Word | Definition | Synonyms | Example |",
                "|---:|---|---|---|---|",
            ]
        )
        for offset, entry in enumerate(group, 1):
            number = ((group_index - 1) * group_size) + offset
            lines.append(
                f"| {number} | {_md(entry.word)} | {_md(entry.definition)} | "
                f"{_md(entry.synonyms)} | {_md(entry.example)} |"
            )
        lines.extend(
            [
                "",
                "### Recall Check",
                "",
                "| # | Word | Definition from memory | Correct |",
                "|---:|---|---|---|",
            ]
        )
        for offset, entry in enumerate(group, 1):
            number = ((group_index - 1) * group_size) + offset
            lines.append(f"| {number} | {_md(entry.word)} |  | [ ] |")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_vocab_pdf(markdown: str, output_path: Path) -> None:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    except ImportError as exc:
        raise RuntimeError("PDF output requires reportlab. Install the pdf extra.") from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    story = []
    for line in markdown.splitlines():
        if not line.strip():
            story.append(Spacer(1, 8))
            continue
        if line.startswith("# "):
            story.append(Paragraph(html.escape(line[2:]), styles["Title"]))
        elif line.startswith("## "):
            story.append(Paragraph(html.escape(line[3:]), styles["Heading2"]))
        elif line.startswith("|") or line.startswith("- "):
            story.append(Paragraph(html.escape(line), styles["BodyText"]))
        else:
            story.append(Paragraph(html.escape(line), styles["BodyText"]))
    SimpleDocTemplate(str(output_path), pagesize=A4).build(story)


def _optional_value(row: dict[str, str], normalized: dict[str, str], key: str) -> str:
    source_key = normalized.get(key)
    if source_key is None:
        return ""
    return row.get(source_key, "")


def _clean(value: str | None) -> str:
    return " ".join((value or "").strip().split())


def _groups(entries: list[VocabEntry], group_size: int) -> list[list[VocabEntry]]:
    if group_size < 1:
        raise ValueError("group_size must be at least 1.")
    return [entries[index : index + group_size] for index in range(0, len(entries), group_size)]


def _md(value: str) -> str:
    return value.replace("|", "\\|")
