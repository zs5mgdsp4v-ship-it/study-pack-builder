from __future__ import annotations

from collections.abc import Iterable

from .vocab import VocabEntry


LEVEL_LABELS = {
    "middle-school": "Middle School Vocabulary Review",
    "high-school": "High School Exam Review",
    "test-prep": "Test Prep Vocabulary Review",
}


def render_review_sheet(
    entries: Iterable[VocabEntry],
    *,
    title: str = "Vocabulary Review Sheet",
    level: str = "high-school",
) -> str:
    if level not in LEVEL_LABELS:
        supported = ", ".join(sorted(LEVEL_LABELS))
        raise ValueError(f"Unsupported level: {level}. Supported levels: {supported}")

    vocab = list(entries)
    lines = [
        f"# {title}",
        "",
        f"- Level: {level}",
        f"- Template: {LEVEL_LABELS[level]}",
        f"- Total entries: {len(vocab)}",
        "",
        "## Vocabulary Preview",
        "",
        "| # | Word | Definition | Synonyms |",
        "|---:|---|---|---|",
    ]
    for index, entry in enumerate(vocab, 1):
        lines.append(f"| {index} | {_md(entry.word)} | {_md(entry.definition)} | {_md(entry.synonyms)} |")

    lines.extend(
        [
            "",
            "## Meaning Recall",
            "",
            "| # | Word | Meaning from memory | Correct |",
            "|---:|---|---|---|",
        ]
    )
    for index, entry in enumerate(vocab, 1):
        lines.append(f"| {index} | {_md(entry.word)} |  | [ ] |")

    lines.extend(
        [
            "",
            "## Example Sentence Fill-in",
            "",
            "| # | Sentence | Answer |",
            "|---:|---|---|",
        ]
    )
    for index, entry in enumerate(vocab, 1):
        lines.append(f"| {index} | {_md(_blank_word(entry.example, entry.word))} | {_md(entry.word)} |")

    lines.extend(
        [
            "",
            "## Synonym Match",
            "",
            "| # | Word | Synonym clue | Match |",
            "|---:|---|---|---|",
        ]
    )
    for index, entry in enumerate(vocab, 1):
        clue = entry.synonyms.split(";")[0].strip() if entry.synonyms else ""
        lines.append(f"| {index} | {_md(entry.word)} | {_md(clue)} |  |")

    lines.extend(
        [
            "",
            "## Teacher Check",
            "",
            "| Item | Review note | Done |",
            "|---|---|---|",
            "| Definitions | Confirm level-appropriate wording. | [ ] |",
            "| Examples | Confirm sentences match the class context. | [ ] |",
            "| Quiz readiness | Mark difficult words for extra review. | [ ] |",
            "",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def _blank_word(example: str, word: str) -> str:
    if not example:
        return "Write an example sentence with ____."
    lower_example = example.lower()
    lower_word = word.lower()
    index = lower_example.find(lower_word)
    if index == -1:
        return f"{example} ____"
    return example[:index] + "____" + example[index + len(word) :]


def _md(value: str) -> str:
    return value.replace("|", "\\|")
