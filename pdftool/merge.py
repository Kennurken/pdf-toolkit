"""Merge PDFs in order."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter


def merge_pdfs(input_paths: list[Path], output_path: Path) -> Path:
    if not input_paths:
        raise ValueError("Provide at least one input PDF to merge.")

    writer = PdfWriter()
    for path in input_paths:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Input PDF not found: {path}")
        if path.suffix.lower() != ".pdf":
            raise ValueError(f"Not a PDF file: {path}")
        reader = PdfReader(str(path))
        if len(reader.pages) == 0:
            raise ValueError(f"PDF has no pages: {path}")
        for page in reader.pages:
            writer.add_page(page)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        writer.write(handle)
    return output_path
