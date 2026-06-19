from study_pack_builder.review_sheet import render_review_sheet
from study_pack_builder.vocab import VocabEntry


def test_render_review_sheet_for_high_school_level() -> None:
    markdown = render_review_sheet(
        [
            VocabEntry("analyze", "examine carefully", "examine; study", "Students analyze the passage."),
            VocabEntry("retain", "keep or remember", "keep; preserve", "Review helps students retain words."),
        ],
        title="High School Review",
        level="high-school",
    )

    assert "# High School Review" in markdown
    assert "- Level: high-school" in markdown
    assert "## Meaning Recall" in markdown
    assert "| 1 | analyze |  | [ ] |" in markdown
    assert "## Example Sentence Fill-in" in markdown
    assert "Students ____ the passage." in markdown
    assert "## Teacher Check" in markdown


def test_render_review_sheet_rejects_unknown_level() -> None:
    try:
        render_review_sheet([], title="Review", level="college")
    except ValueError as exc:
        assert "Unsupported level" in str(exc)
    else:
        raise AssertionError("Expected unsupported level to raise ValueError")
