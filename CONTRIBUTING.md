# Contributing

Thanks for helping improve `study-pack-builder`.

## Development Setup

```bash
git clone https://github.com/zs5mgdsp4v-ship-it/study-pack-builder.git
cd study-pack-builder
python3 -m pip install -e ".[dev,pdf]"
python3 -m pytest
```

For Markdown-only changes, the `pdf` extra is optional:

```bash
python3 -m pip install -e ".[dev]"
```

## Pull Requests

- Keep changes focused on one workflow or command.
- Add or update tests for behavior changes.
- Include a small sample input when adding a new parser or output format.
- Run `python3 -m pytest` before opening a pull request.

## Project Scope

The project focuses on practical study-material generation:

- vocabulary packs from structured CSV
- quiz drafts from plain text or Markdown
- validation reports for OCR-cleanup workflows
- print-friendly document post-processing

Large hosted services, account systems, and proprietary content datasets are out of scope.
