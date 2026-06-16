from pathlib import Path

from study_pack_builder.validate import ValidationIssue, validate_vocab_csv


def test_validate_vocab_csv_reports_duplicates_and_blank_required_fields(tmp_path: Path) -> None:
    source = tmp_path / "vocab.csv"
    source.write_text(
        "word,definition,synonyms,example\n"
        "abandon,give up,leave,Do not abandon it.\n"
        "abandon,leave behind,quit,Do not abandon the plan.\n"
        "brief,,concise,Keep it brief.\n",
        encoding="utf-8",
    )

    issues = validate_vocab_csv(source)

    assert ValidationIssue(3, "duplicate-word", "Duplicate word: abandon") in issues
    assert ValidationIssue(4, "missing-definition", "Missing required definition") in issues


def test_validate_vocab_csv_accepts_valid_input(tmp_path: Path) -> None:
    source = tmp_path / "vocab.csv"
    source.write_text(
        "word,definition,synonyms,example\n"
        "abandon,give up,leave,Do not abandon it.\n"
        "brief,short,concise,Keep it brief.\n",
        encoding="utf-8",
    )

    assert validate_vocab_csv(source) == []
