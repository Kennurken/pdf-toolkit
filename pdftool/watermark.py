"""Diagonal semi-transparent text watermark."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas


def _make_watermark_page(width: float, height: float, text: str, font_size: float, opacity: float) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(width, height))
    c.setFillColorRGB(0.35, 0.35, 0.35, alpha=max(0.0, min(1.0, opacity)))
    c.setFont("Helvetica-Bold", font_size)
    c.saveState()
    c.translate(width / 2, height / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, text)
    c.restoreState()
    c.save()
    buffer.seek(0)
    return buffer.read()


def watermark_pdf(
    input_path: Path,
    output_path: Path,
    text: str,
    font_size: float = 54.0,
    opacity: float = 0.25,
) -> Path:
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input PDF not found: {input_path}")
    if not text or not text.strip():
        raise ValueError("Watermark --text cannot be empty.")
    if font_size <= 0:
        raise ValueError("--font-size must be positive.")
    if not 0 <= opacity <= 1:
        raise ValueError("--opacity must be between 0 and 1.")

    reader = PdfReader(str(input_path))
    if len(reader.pages) == 0:
        raise ValueError(f"PDF has no pages: {input_path}")

    writer = PdfWriter()
    for page in reader.pages:
        box = page.mediabox
        width = float(box.width)
        height = float(box.height)
        stamp_bytes = _make_watermark_page(width, height, text.strip(), font_size, opacity)
        stamp_page = PdfReader(BytesIO(stamp_bytes)).pages[0]
        page.merge_page(stamp_page)
        writer.add_page(page)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        writer.write(handle)
    return output_path
