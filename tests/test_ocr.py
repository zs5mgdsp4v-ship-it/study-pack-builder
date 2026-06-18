from pathlib import Path

from study_pack_builder.ocr import OcrCleanupResult, clean_ocr_text, write_ocr_csv


def test_clean_ocr_text_extracts_numbered_vocabulary_rows() -> None:
    source = """
    1. analyze   examine something carefully   examine; study   Students analyze the passage.
    2 retain keep or remember information keep; preserve Review sheets help students retain vocabulary.
    broken line without enough columns
    3. infer   understand from evidence   deduce; conclude   Infer the meaning from context.
    """

    result = clean_ocr_text(source)

    assert result == OcrCleanupResult(
        rows=[
            {
                "word": "analyze",
                "definition": "examine something carefully",
                "synonyms": "examine; study",
                "example": "Students analyze the passage.",
            },
            {
                "word": "retain",
                "definition": "keep or remember information",
                "synonyms": "keep; preserve",
                "example": "Review sheets help students retain vocabulary.",
            },
            {
                "word": "infer",
                "definition": "understand from evidence",
                "synonyms": "deduce; conclude",
                "example": "Infer the meaning from context.",
            },
        ],
        warnings=["line 4: skipped malformed OCR row"],
    )


def test_write_ocr_csv_outputs_vocab_columns(tmp_path: Path) -> None:
    output = tmp_path / "cleaned.csv"
    result = OcrCleanupResult(
        rows=[
            {
                "word": "precise",
                "definition": "exact and accurate",
                "synonyms": "accurate; exact",
                "example": "Use precise definitions.",
            }
        ],
        warnings=[],
    )

    write_ocr_csv(result, output)

    assert output.read_text(encoding="utf-8") == (
        "word,definition,synonyms,example\n"
        "precise,exact and accurate,accurate; exact,Use precise definitions.\n"
    )
