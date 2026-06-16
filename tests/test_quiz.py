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


def test_build_quiz_template_adds_teacher_review_answer_key_table() -> None:
    source = "Students infer meaning from context. Precise definitions reduce confusion."

    markdown = build_quiz_template(source, count=2)

    assert "## Teacher Review Answer Key" in markdown
    assert "| Item | Type | Source | Answer | Notes |" in markdown
    assert "| MC-1 | Multiple Choice | Students infer meaning from context. |  |  |" in markdown
    assert "| OX-2 | OX | Precise definitions reduce confusion. | O / X |  |" in markdown


def test_build_quiz_template_handles_empty_source() -> None:
    markdown = build_quiz_template("   ", count=3)

    assert "# Quiz Draft" in markdown
    assert "No source sentences found." in markdown
