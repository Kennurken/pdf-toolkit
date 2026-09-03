"""Fill AcroForm PDF fields from CSV rows."""

from __future__ import annotations

import csv
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError


def _form_field_names(reader: PdfReader) -> list[str]:
    fields = reader.get_fields()
    if not fields:
        return []
    return list(fields.keys())


def fill_from_csv(template_path: Path, csv_path: Path, output_dir: Path) -> list[Path]:
    template_path = Path(template_path)
    csv_path = Path(csv_path)
    output_dir = Path(output_dir)

    if not template_path.exists():
        raise FileNotFoundError(f"Template PDF not found: {template_path}")
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    try:
        reader = PdfReader(str(template_path))
    except PdfReadError as exc:
        raise ValueError(f"Could not open template PDF: {exc}") from exc

    field_names = _form_field_names(reader)
    if not field_names:
        raise ValueError(
            f"PDF has no fillable AcroForm fields: {template_path}. "
            "Export a real form PDF or use the sample in sample_files/."
        )

    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        csv_reader = csv.DictReader(handle)
        if not csv_reader.fieldnames:
            raise ValueError(f"CSV has no header row: {csv_path}")

        headers = [h for h in csv_reader.fieldnames if h is not None]
        matched = [name for name in field_names if name in headers]
        if not matched:
            raise ValueError(
                "CSV columns do not match any form field names.\n"
                f"  Form fields: {', '.join(field_names)}\n"
                f"  CSV columns: {', '.join(headers)}"
            )

        rows = list(csv_reader)

    if not rows:
        raise ValueError(f"CSV has no data rows: {csv_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for row_index, row in enumerate(rows, start=1):
        template_reader = PdfReader(str(template_path))
        writer = PdfWriter()
        writer.append(template_reader)
        writer.set_need_appearances_writer(True)

        values = {name: (row.get(name) or "") for name in matched}
        for page in writer.pages:
            writer.update_page_form_field_values(page, values)

        out_path = output_dir / f"{template_path.stem}_row{row_index}.pdf"
        with out_path.open("wb") as handle:
            writer.write(handle)
        written.append(out_path)

    return written
