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
