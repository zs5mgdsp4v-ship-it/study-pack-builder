import subprocess
import sys
import os
from pathlib import Path


def test_cli_vocab_writes_markdown(tmp_path: Path) -> None:
    source = tmp_path / "vocab.csv"
    output = tmp_path / "pack.md"
    source.write_text(
        "word,definition,synonyms,example\n"
        "abandon,give up,leave,Do not abandon it.\n",
        encoding="utf-8",
    )

    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "study_pack_builder",
            "vocab",
            str(source),
            "--markdown",
            str(output),
            "--title",
            "Demo",
        ],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert output.exists()
    assert "# Demo" in output.read_text(encoding="utf-8")


def test_cli_validate_reports_invalid_csv(tmp_path: Path) -> None:
    source = tmp_path / "vocab.csv"
    source.write_text(
        "word,definition\n"
        "abandon,give up\n"
        "abandon,leave behind\n"
        "brief,\n",
        encoding="utf-8",
    )

    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "study_pack_builder",
            "validate",
            str(source),
        ],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )

    assert result.returncode == 1
    assert "duplicate-word" in result.stdout
    assert "missing-definition" in result.stdout


def test_cli_quiz_writes_teacher_review_answer_key(tmp_path: Path) -> None:
    source = tmp_path / "lesson.txt"
    output = tmp_path / "quiz.md"
    source.write_text(
        "Students infer word meaning from context. Teachers review answer keys before class.",
        encoding="utf-8",
    )

    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "study_pack_builder",
            "quiz",
            str(source),
            "--markdown",
            str(output),
            "--count",
            "2",
        ],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    markdown = output.read_text(encoding="utf-8")
    assert "## Teacher Review Answer Key" in markdown
    assert "| MC-1 | Multiple Choice | Students infer word meaning from context. |  |  |" in markdown


def test_cli_clean_ocr_writes_csv_and_reports_warnings(tmp_path: Path) -> None:
    source = tmp_path / "ocr.txt"
    output = tmp_path / "cleaned.csv"
    source.write_text(
        "1. analyze   examine carefully   examine; study   Students analyze text.\n"
        "bad row\n",
        encoding="utf-8",
    )

    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "study_pack_builder",
            "clean-ocr",
            str(source),
            "--csv",
            str(output),
        ],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert "Wrote 1 rows" in result.stdout
    assert "line 2: skipped malformed OCR row" in result.stdout
    assert output.read_text(encoding="utf-8").startswith("word,definition,synonyms,example\n")


def test_cli_review_sheet_writes_level_specific_markdown(tmp_path: Path) -> None:
    source = tmp_path / "vocab.csv"
    output = tmp_path / "review.md"
    source.write_text(
        "word,definition,synonyms,example\n"
        "analyze,examine carefully,examine; study,Students analyze the passage.\n",
        encoding="utf-8",
    )

    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "study_pack_builder",
            "review-sheet",
            str(source),
            "--markdown",
            str(output),
            "--level",
            "test-prep",
            "--title",
            "Test Prep Review",
        ],
        cwd=Path(__file__).resolve().parents[1],
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    markdown = output.read_text(encoding="utf-8")
    assert "# Test Prep Review" in markdown
    assert "- Level: test-prep" in markdown
    assert "## Synonym Match" in markdown
