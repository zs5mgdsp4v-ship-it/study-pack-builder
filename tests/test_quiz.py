from study_pack_builder.quiz import build_quiz_template


def test_build_quiz_template_uses_source_sentences() -> None:
    source = "Encapsulation protects internal state. Inheritance reuses behavior."

    markdown = build_quiz_template(source, count=2)

    assert "# Quiz Draft" in markdown
    assert "Encapsulation protects internal state." in markdown
    assert "Inheritance reuses behavior." in markdown
    assert "## Multiple Choice" in markdown
    assert "## OX" in markdown
    assert "## Answer Key" in markdown
    assert "- Q1:" in markdown
