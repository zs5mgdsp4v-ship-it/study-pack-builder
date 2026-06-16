from __future__ import annotations

import re


def build_quiz_template(source: str, *, count: int = 10) -> str:
    sentences = _sentences(source)[:count]
    lines = [
        "# Quiz Draft",
        "",
        "Use this draft as a teacher-reviewed starting point. Fill in the final answer choices and explanations before classroom use.",
        "",
    ]
    if not sentences:
        lines.extend(
            [
                "No source sentences found.",
                "",
                "Add lesson notes, reading passages, or vocabulary explanations, then run the command again.",
                "",
            ]
        )
        return "\n".join(lines).rstrip() + "\n"

    lines.extend(
        [
        "## Multiple Choice",
        "",
        ]
    )
    for index, sentence in enumerate(sentences, 1):
        lines.extend(
            [
                f"### Q{index}",
                "",
                f"Source: {sentence}",
                "",
                "Question:",
                "",
                "- A.",
                "- B.",
                "- C.",
                "- D.",
                "",
                "Answer:",
                "",
            ]
        )

    lines.extend(["## OX", ""])
    for index, sentence in enumerate(sentences, 1):
        lines.extend([f"{index}. {sentence}", "", "Answer: O / X", ""])

    lines.extend(["## Answer Key", ""])
    for index, sentence in enumerate(sentences, 1):
        lines.append(f"- Q{index}: Fill after review. Source: {sentence}")
    lines.append("")

    lines.extend(
        [
            "## Teacher Review Answer Key",
            "",
            "| Item | Type | Source | Answer | Notes |",
            "|---|---|---|---|---|",
        ]
    )
    for index, sentence in enumerate(sentences, 1):
        lines.append(f"| MC-{index} | Multiple Choice | {_md(sentence)} |  |  |")
    for index, sentence in enumerate(sentences, 1):
        lines.append(f"| OX-{index} | OX | {_md(sentence)} | O / X |  |")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _sentences(source: str) -> list[str]:
    compact = " ".join(source.split())
    parts = re.split(r"(?<=[.!?])\s+", compact)
    return [part.strip() for part in parts if part.strip()]


def _md(value: str) -> str:
    return value.replace("|", "\\|")
