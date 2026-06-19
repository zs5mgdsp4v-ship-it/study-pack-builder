from __future__ import annotations

import argparse
from pathlib import Path

from .pdf_tools import lighten_pdf
from .ocr import clean_ocr_text, write_ocr_csv
from .quiz import build_quiz_template
from .review_sheet import render_review_sheet
from .validate import format_issues, validate_vocab_csv
from .vocab import load_vocab_csv, render_vocab_markdown, write_vocab_pdf


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="study-pack-builder")
    subparsers = parser.add_subparsers(dest="command", required=True)

    vocab = subparsers.add_parser("vocab", help="Build a study pack from a CSV vocabulary file.")
    vocab.add_argument("csv", type=Path)
    vocab.add_argument("--markdown", type=Path)
    vocab.add_argument("--pdf", type=Path)
    vocab.add_argument("--title", default="Study Pack")
    vocab.add_argument("--group-size", type=int, default=25)

    quiz = subparsers.add_parser("quiz", help="Create a quiz draft template from text.")
    quiz.add_argument("source", type=Path)
    quiz.add_argument("--markdown", type=Path, required=True)
    quiz.add_argument("--count", type=int, default=10)

    validate = subparsers.add_parser("validate", help="Validate a vocabulary CSV before building.")
    validate.add_argument("csv", type=Path)

    clean_ocr = subparsers.add_parser("clean-ocr", help="Convert OCR vocabulary text into a CSV draft.")
    clean_ocr.add_argument("source", type=Path)
    clean_ocr.add_argument("--csv", type=Path, required=True)

    review_sheet = subparsers.add_parser("review-sheet", help="Build a level-specific vocabulary review sheet.")
    review_sheet.add_argument("csv", type=Path)
    review_sheet.add_argument("--markdown", type=Path, required=True)
    review_sheet.add_argument("--level", choices=["middle-school", "high-school", "test-prep"], default="high-school")
    review_sheet.add_argument("--title", default="Vocabulary Review Sheet")

    pdf = subparsers.add_parser("pdf-lighten", help="Lighten dark PDF blocks for printing.")
    pdf.add_argument("input_pdf", type=Path)
    pdf.add_argument("output_pdf", type=Path)
    pdf.add_argument("--dpi", type=int, default=180)

    args = parser.parse_args(argv)

    if args.command == "vocab":
        entries = load_vocab_csv(args.csv)
        markdown = render_vocab_markdown(entries, title=args.title, group_size=args.group_size)
        if not args.markdown and not args.pdf:
            print(markdown, end="")
            return 0
        if args.markdown:
            args.markdown.parent.mkdir(parents=True, exist_ok=True)
            args.markdown.write_text(markdown, encoding="utf-8")
        if args.pdf:
            write_vocab_pdf(markdown, args.pdf)
        return 0

    if args.command == "quiz":
        source = args.source.read_text(encoding="utf-8")
        markdown = build_quiz_template(source, count=args.count)
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(markdown, encoding="utf-8")
        return 0

    if args.command == "validate":
        issues = validate_vocab_csv(args.csv)
        print(format_issues(issues), end="")
        return 1 if issues else 0

    if args.command == "clean-ocr":
        source = args.source.read_text(encoding="utf-8")
        result = clean_ocr_text(source)
        write_ocr_csv(result, args.csv)
        print(f"Wrote {len(result.rows)} rows to {args.csv}")
        for warning in result.warnings:
            print(warning)
        return 0

    if args.command == "review-sheet":
        entries = load_vocab_csv(args.csv)
        markdown = render_review_sheet(entries, title=args.title, level=args.level)
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(markdown, encoding="utf-8")
        return 0

    if args.command == "pdf-lighten":
        lighten_pdf(args.input_pdf, args.output_pdf, dpi=args.dpi)
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2
