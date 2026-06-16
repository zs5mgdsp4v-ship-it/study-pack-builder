# English Academy Workflow

`study-pack-builder` is designed for local study-material workflows that are common in Korean English academies and test-prep classrooms.

Teachers often need to prepare the same types of material every week:

- vocabulary lists from textbooks, OCR scans, or hand-cleaned CSV files
- memorization sheets for class or homework
- short quizzes for review sessions
- printable material for school exams, CSAT prep, and language-test prep
- answer keys or explanation drafts that can be reviewed before class

The project focuses on making those repeated steps easier while keeping class material local.

## Example

Validate an academy vocabulary file:

```bash
study-pack-builder validate examples/english_academy_vocab.csv
```

Generate a study pack:

```bash
study-pack-builder vocab examples/english_academy_vocab.csv --markdown outputs/academy-vocab-pack.md --title "English Academy Vocabulary Pack"
```

Create a quiz draft from lesson notes:

```bash
study-pack-builder quiz examples/concepts.txt --markdown outputs/quiz-draft.md --count 5
```

## Why Local First

Study materials can include classroom-specific content, student-level notes, or licensed textbook excerpts. The core CLI works locally so teachers can validate and format their own files without sending them to a hosted service. Future AI-assisted features should remain optional and document when data is sent to an external API.
