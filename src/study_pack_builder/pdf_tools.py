from __future__ import annotations

import io
from pathlib import Path


def lighten_pdf(input_pdf: Path, output_pdf: Path, *, dpi: int = 180) -> None:
    try:
        import fitz
        import numpy as np
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("pdf-lighten requires pymupdf, pillow, and numpy.") from exc

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    source = fitz.open(input_pdf)
    output = fitz.open()
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    try:
        for page in source:
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            processed = _lighten_dark_pixels(image, np)
            encoded = io.BytesIO()
            processed.save(encoded, format="JPEG", quality=96, optimize=True)

            page_out = output.new_page(width=page.rect.width, height=page.rect.height)
            page_out.insert_image(page_out.rect, stream=encoded.getvalue())
        output.save(output_pdf, garbage=4, deflate=True)
    finally:
        output.close()
        source.close()


def _lighten_dark_pixels(image, np):
    arr = np.array(image.convert("RGB"))
    rgb = arr[:, :, :3].astype("int16")
    lum = (0.2126 * rgb[:, :, 0]) + (0.7152 * rgb[:, :, 1]) + (0.0722 * rgb[:, :, 2])
    dark = lum < 80
    arr[dark, :3] = 245
    return image.__class__.fromarray(arr, "RGB")
