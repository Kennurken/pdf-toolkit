"""Split a PDF by page ranges."""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter


def parse_ranges(ranges_text: str, page_count: int) -> list[tuple[int, int]]:
    """Parse '1-3,4-6,7-' into 1-based inclusive (start, end) tuples."""
    if not ranges_text or not ranges_text.strip():
        raise ValueError("Provide at least one page range via --ranges.")

    parsed: list[tuple[int, int]] = []
    for chunk in ranges_text.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue

        if "-" in chunk:
            left, right = chunk.split("-", 1)
            left = left.strip()
            right = right.strip()
            if not left.isdigit():
                raise ValueError(
                    f"Invalid range '{chunk}'. Use forms like 1-3, 5, or 7-."
                )
            start = int(left)
            if right == "":
                end = page_count
            elif right.isdigit():
                end = int(right)
            else:
                raise ValueError(
                    f"Invalid range '{chunk}'. Use forms like 1-3, 5, or 7-."
                )
        else:
            if not chunk.isdigit():
                raise ValueError(
                    f"Invalid range '{chunk}'. Use forms like 1-3, 5, or 7-."
                )
            start = end = int(chunk)

        if start < 1 or end < 1:
            raise ValueError(f"Page numbers must be >= 1 (got {chunk}).")
        if start > page_count or end > page_count:
            raise ValueError(
                f"Range '{chunk}' is outside the document ({page_count} pages)."
            )
        if start > end:
            raise ValueError(f"Range start > end in '{chunk}'.")
        parsed.append((start, end))

    if not parsed:
        raise ValueError("No valid page ranges found.")
    return parsed


def split_pdf(input_path: Path, ranges_text: str, output_dir: Path) -> list[Path]:
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input PDF not found: {input_path}")

    reader = PdfReader(str(input_path))
    page_count = len(reader.pages)
    if page_count == 0:
        raise ValueError(f"PDF has no pages: {input_path}")

    ranges = parse_ranges(ranges_text, page_count)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    stem = input_path.stem
    for start, end in ranges:
        writer = PdfWriter()
        for page_number in range(start, end + 1):
            writer.add_page(reader.pages[page_number - 1])
        out_path = output_dir / f"{stem}_p{start}-{end}.pdf"
        with out_path.open("wb") as handle:
            writer.write(handle)
        written.append(out_path)
    return written
