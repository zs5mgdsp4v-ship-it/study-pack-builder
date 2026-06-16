from __future__ import annotations

import re


def build_quiz_template(source: str, *, count: int = 10) -> str:
    sentences = _sentences(source)[:count]
    lines = [
        "# Quiz Draft",
        "",
        "## Multiple Choice",
        "",
    ]
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

    return "\n".join(lines).rstrip() + "\n"


def _sentences(source: str) -> list[str]:
    compact = " ".join(source.split())
    parts = re.split(r"(?<=[.!?])\s+", compact)
    return [part.strip() for part in parts if part.strip()]
