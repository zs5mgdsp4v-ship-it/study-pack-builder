from pathlib import Path

from study_pack_builder.vocab import VocabEntry, load_vocab_csv, render_vocab_markdown


def test_load_vocab_csv_reads_expected_columns(tmp_path: Path) -> None:
    source = tmp_path / "vocab.csv"
    source.write_text(
        "word,definition,synonyms,example\n"
        "abandon,give up,leave; quit,Do not abandon the plan.\n",
        encoding="utf-8",
    )

    entries = load_vocab_csv(source)

    assert entries == [
        VocabEntry(
            word="abandon",
            definition="give up",
            synonyms="leave; quit",
            example="Do not abandon the plan.",
        )
    ]


def test_render_vocab_markdown_groups_entries() -> None:
    entries = [
        VocabEntry("abandon", "give up", "leave", "Do not abandon it."),
        VocabEntry("brief", "short", "concise", "Keep it brief."),
    ]

    markdown = render_vocab_markdown(entries, title="Sample Pack", group_size=1)

    assert "# Sample Pack" in markdown
    assert "## Set 1" in markdown
    assert "## Set 2" in markdown
    assert "| 1 | abandon | give up | leave | Do not abandon it. |" in markdown
    assert "### Recall Check" in markdown
