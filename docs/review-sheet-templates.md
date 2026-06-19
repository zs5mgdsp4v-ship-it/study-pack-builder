# Review Sheet Templates

`study-pack-builder review-sheet` creates editable Markdown review sheets from a vocabulary CSV. The goal is to help English academy teachers adapt the same word list for different class levels and exam contexts.

## Supported Levels

- `middle-school`
- `high-school`
- `test-prep`

## Example

```bash
study-pack-builder review-sheet examples/english_academy_vocab.csv \
  --markdown outputs/high-school-review.md \
  --level high-school \
  --title "High School Vocabulary Review"
```

## Output Sections

Each review sheet includes:

- Vocabulary Preview
- Meaning Recall
- Example Sentence Fill-in
- Synonym Match
- Teacher Check

## Local-First Rationale

Teachers often adapt review sheets for specific classes, student levels, and school exam scopes. Markdown keeps the generated output easy to edit before printing or sharing.
