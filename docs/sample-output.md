# Sample Output

This page shows the kind of output an English academy teacher can generate from `examples/english_academy_vocab.csv`.

Command:

```bash
study-pack-builder vocab examples/english_academy_vocab.csv --markdown outputs/academy-vocab-pack.md --title "English Academy Vocabulary Pack"
```

Excerpt:

```markdown
# English Academy Vocabulary Pack

- Total entries: 5
- Group size: 25

## Study Method

| Step | Action | Done |
|---|---|---|
| 1 | Read the word, definition, synonyms, and example aloud. | [ ] |
| 2 | Hide the definition and recall it from the word. | [ ] |
| 3 | Hide the word and recall it from the definition. | [ ] |
| 4 | Mark missed items and repeat them after a short break. | [ ] |

## Set 1

| # | Word | Definition | Synonyms | Example |
|---:|---|---|---|---|
| 1 | analyze | examine something carefully | examine; study | Students analyze the passage before answering the questions. |
| 2 | retain | keep or remember information | keep; preserve | Review sheets help students retain new vocabulary. |
| 3 | infer | understand something from evidence | deduce; conclude | Students infer the meaning from context clues. |
```

Validation example:

```bash
study-pack-builder validate examples/invalid_vocab.csv
```

Output:

```text
Validation issues:
- line 3: duplicate-word: Duplicate word: abandon
- line 4: missing-definition: Missing required definition
```

These examples are intentionally small so they can be copied into bug reports, tests, and documentation without exposing real class material.
