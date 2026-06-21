from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from .vocab import VocabEntry


def build_printable_vocab_pdf(
    entries: Iterable[VocabEntry],
    output_path: Path,
    *,
    title: str = "Printable Vocabulary Table",
) -> None:
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_LEFT
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    except ImportError as exc:
        raise RuntimeError("Printable PDF tables require reportlab. Install the pdf extra.") from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    cell = ParagraphStyle(
        "CompactCell",
        parent=styles["BodyText"],
        fontSize=7,
        leading=8.5,
        alignment=TA_LEFT,
    )
    head = ParagraphStyle(
        "CompactHead",
        parent=styles["BodyText"],
        fontSize=7,
        leading=8.5,
        textColor=colors.white,
        alignment=TA_LEFT,
    )

    rows = [
        [
            Paragraph("#", head),
            Paragraph("Word", head),
            Paragraph("Definition", head),
            Paragraph("Synonyms", head),
            Paragraph("Example", head),
        ]
    ]
    for index, entry in enumerate(entries, 1):
        rows.append(
            [
                Paragraph(str(index), cell),
                Paragraph(_escape(entry.word), cell),
                Paragraph(_escape(entry.definition), cell),
                Paragraph(_escape(entry.synonyms), cell),
                Paragraph(_escape(entry.example), cell),
            ]
        )

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=landscape(A4),
        leftMargin=10 * mm,
        rightMargin=10 * mm,
        topMargin=10 * mm,
        bottomMargin=10 * mm,
    )
    table = Table(rows, colWidths=[10 * mm, 34 * mm, 68 * mm, 48 * mm, 100 * mm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F3A44")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#C7CDD3")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FB")]),
            ]
        )
    )
    story = [Paragraph(_escape(title), styles["Title"]), Spacer(1, 4 * mm), table]
    doc.build(story)


def _escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )
