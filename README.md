# study-pack-builder

[![CI](https://github.com/zs5mgdsp4v-ship-it/study-pack-builder/actions/workflows/ci.yml/badge.svg)](https://github.com/zs5mgdsp4v-ship-it/study-pack-builder/actions/workflows/ci.yml)

`study-pack-builder` is a small Python CLI for turning study inputs into reusable learning packs.

The first use case is English education in Korea, where private academies, test-prep programs, and classroom teachers repeatedly prepare vocabulary lists, memorization sheets, quizzes, answer keys, and printable review materials. The tool keeps that workflow local-first: teachers can start from CSV exports, OCR-cleaned word lists, or plain text notes and generate consistent study packs without uploading private class material to a hosted service.

It currently supports:

- CSV vocabulary files to Markdown study packs
- Validation reports for vocabulary CSV files
- Optional PDF output for vocabulary packs
- Text files to quiz draft templates
- Print-friendly PDF lightening for pages with dark code blocks

The project is early but intentionally structured for maintainable open-source development: tested commands, sample inputs, CI, contribution guidance, and a clear local-first security policy.

## Who This Helps

- English academy teachers preparing weekly vocabulary packets and review quizzes
- Test-prep instructors building school-exam, CSAT, TOEIC, or TOEFL practice material
- Students who want structured recall sheets from CSV vocabulary notes
- Education-content creators who need repeatable local tooling for study-pack generation

## Current Status

`study-pack-builder` is an early-stage maintained OSS project. The current release focuses on reliable local CLI workflows: vocabulary CSV validation, Markdown study-pack generation, quiz draft scaffolding, PDF output, examples, CI, issue templates, contribution guidance, and a security policy. The next planned work is tracked in GitHub issues and focuses on OCR cleanup, English academy answer keys, printable vocabulary tables, and level-specific review sheets.

## English Academy Workflow

For an English academy or test-prep class, the intended workflow is:

1. Export or clean a vocabulary list into CSV.
2. Validate missing definitions and duplicate words.
3. Generate a Markdown study pack for editing or printing.
4. Create quiz drafts from class notes or reading passages.
5. Keep outputs local so student or class material stays private.

Example academy vocabulary input:

```bash
study-pack-builder validate examples/english_academy_vocab.csv
study-pack-builder vocab examples/english_academy_vocab.csv --markdown outputs/academy-vocab-pack.md --title "English Academy Vocabulary Pack"
```

See [docs/english-academy-workflow.md](docs/english-academy-workflow.md) for the workflow and [docs/sample-output.md](docs/sample-output.md) for example output.

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

Build an English academy vocabulary pack:

```bash
study-pack-builder vocab examples/english_academy_vocab.csv --markdown outputs/academy-vocab-pack.md --title "English Academy Vocabulary Pack"
```

Build a vocabulary study pack and PDF:

```bash
study-pack-builder vocab examples/vocab.csv --markdown outputs/vocab-pack.md --pdf outputs/vocab-pack.pdf
```

Create a quiz draft from plain text:

```bash
study-pack-builder quiz examples/concepts.txt --markdown outputs/quiz-draft.md --count 5
```

Create an English academy quiz draft with a teacher review answer key:

```bash
study-pack-builder quiz examples/english_academy_lesson.txt --markdown outputs/academy-quiz-draft.md --count 4
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
- add richer answer-key and review-sheet generation for English academy classes
- document supported input formats with English education examples
- use CI to keep behavior stable across supported Python versions

## Roadmap

- Add CSV validation reports for OCR cleanup workflows
- Add answer-key generation for quiz drafts
- Add richer PDF tables for English vocabulary packs
- Add review-sheet templates for school exams, CSAT prep, and language-test prep
- Add optional AI-assisted summarization and question generation
