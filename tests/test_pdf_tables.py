from pathlib import Path

from study_pack_builder.pdf_tables import build_printable_vocab_pdf
from study_pack_builder.vocab import VocabEntry


def test_build_printable_vocab_pdf_writes_pdf(tmp_path: Path) -> None:
    output = tmp_path / "vocab-table.pdf"

    build_printable_vocab_pdf(
        [
            VocabEntry("analyze", "examine carefully", "examine; study", "Students analyze the passage."),
            VocabEntry("retain", "keep or remember", "keep; preserve", "Review helps students retain words."),
        ],
        output,
        title="Printable Vocabulary Table",
    )

    assert output.exists()
    assert output.read_bytes().startswith(b"%PDF")
