# OCR Cleanup Workflow

English academy teachers often start with vocabulary material copied from scans, PDFs, or OCR output. That text is usually good enough for review, but it often has inconsistent numbering, spacing, and line breaks.

`study-pack-builder clean-ocr` converts a simple OCR vocabulary draft into a CSV file that can be reviewed, validated, and turned into a study pack.

## Example

Clean OCR text into CSV:

```bash
study-pack-builder clean-ocr examples/english_academy_ocr.txt --csv outputs/ocr-cleaned.csv
```

Validate the CSV:

```bash
study-pack-builder validate outputs/ocr-cleaned.csv
```

Build a vocabulary pack:

```bash
study-pack-builder vocab outputs/ocr-cleaned.csv --markdown outputs/ocr-vocab-pack.md --title "OCR Cleaned Vocabulary Pack"
```

## Expected OCR Row Format

The parser is intentionally conservative. It expects rows that roughly look like this:

```text
1. analyze   examine something carefully   examine; study   Students analyze the passage.
```

The generated CSV has these columns:

```csv
word,definition,synonyms,example
```

Malformed rows are skipped and reported as warnings so teachers can review the source text.

## Local-First Rationale

OCR text can come from classroom handouts, school materials, or teacher-created notes. The cleanup workflow runs locally by default so users can prepare drafts without uploading private class material to a hosted service.
