# study-pack-builder

[![CI](https://github.com/zs5mgdsp4v-ship-it/study-pack-builder/actions/workflows/ci.yml/badge.svg)](https://github.com/zs5mgdsp4v-ship-it/study-pack-builder/actions/workflows/ci.yml)

`study-pack-builder` is a small Python CLI for turning study inputs into reusable learning packs.

It currently supports:

- CSV vocabulary files to Markdown study packs
- Validation reports for vocabulary CSV files
- Optional PDF output for vocabulary packs
- Text files to quiz draft templates
- Print-friendly PDF lightening for pages with dark code blocks

The project is early but intentionally structured for maintainable open-source development: tested commands, sample inputs, CI, contribution guidance, and a clear local-first security policy.

## Install

```bash
python3 -m pip install -e ".[dev,pdf]"
```

For Markdown-only use, the PDF extra is optional:

```bash
python3 -m pip install -e ".[dev]"
```

## Usage

Build a vocabulary study pack:

```bash
study-pack-builder vocab examples/vocab.csv --markdown outputs/vocab-pack.md --title "Demo Vocabulary"
```

Build a vocabulary study pack and PDF:

```bash
study-pack-builder vocab examples/vocab.csv --markdown outputs/vocab-pack.md --pdf outputs/vocab-pack.pdf
```

Create a quiz draft from plain text:

```bash
study-pack-builder quiz examples/concepts.txt --markdown outputs/quiz-draft.md --count 5
```

Validate a vocabulary CSV before generating output:

```bash
study-pack-builder validate examples/vocab.csv
```

Example invalid CSV report:

```bash
study-pack-builder validate examples/invalid_vocab.csv
```

Lighten a PDF for printing:

```bash
study-pack-builder pdf-lighten input.pdf output/lightened.pdf
```

## CSV Format

Vocabulary CSV files should include:

```csv
word,definition,synonyms,example
abandon,give up,leave; quit,Do not abandon the plan.
brief,short,concise,Keep the explanation brief.
```

`word` and `definition` are required. `synonyms` and `example` are optional.

## Development

Run tests:

```bash
python3 -m pytest
```

The project uses a `src/` layout and keeps generated output out of version control.

## Maintainer Focus

The next maintenance priorities are:

- keep the CLI local-first and safe for private study materials
- improve validation for OCR-derived CSV and TSV files
- add richer answer-key and review-sheet generation
- document each supported input format with a minimal sample
- use CI to keep behavior stable across supported Python versions

## Roadmap

- Add CSV validation reports for OCR cleanup workflows
- Add answer-key generation for quiz drafts
- Add richer PDF tables for large vocabulary packs
- Add optional AI-assisted summarization and question generation
