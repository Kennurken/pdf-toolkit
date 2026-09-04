"""Regenerate sample PDFs and CSV used in the README demos."""

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

BASE = Path(__file__).resolve().parent


def write_simple(path: Path, title: str, subtitle: str) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(72, 720, title)
    c.setFont("Helvetica", 12)
    c.drawString(72, 680, subtitle)
    c.showPage()
    c.save()


def main() -> None:
    write_simple(BASE / "page_a.pdf", "Sample page A", "First page for merge demos.")
    write_simple(BASE / "page_b.pdf", "Sample page B", "Second page for merge demos.")

    multi = canvas.Canvas(str(BASE / "multi.pdf"), pagesize=letter)
    for page_number in range(1, 6):
        multi.setFont("Helvetica-Bold", 18)
        multi.drawString(72, 720, f"Multi-page sample — page {page_number}")
        multi.setFont("Helvetica", 12)
        multi.drawString(72, 680, "Used for split / watermark demos.")
        multi.showPage()
    multi.save()

    form = canvas.Canvas(str(BASE / "intake_form.pdf"), pagesize=letter)
    form.setFont("Helvetica-Bold", 16)
    form.drawString(72, 720, "Client intake form")
    form.setFont("Helvetica", 11)
    form.drawString(72, 680, "Full name")
    form.acroForm.textfield(
        name="name", x=72, y=655, width=300, height=20, borderWidth=1, forceBorder=True
    )
    form.drawString(72, 620, "Email")
    form.acroForm.textfield(
        name="email", x=72, y=595, width=300, height=20, borderWidth=1, forceBorder=True
    )
    form.drawString(72, 560, "Company")
    form.acroForm.textfield(
        name="company", x=72, y=535, width=300, height=20, borderWidth=1, forceBorder=True
    )
    form.drawString(72, 500, "Notes")
    form.acroForm.textfield(
        name="notes",
        x=72,
        y=430,
        width=400,
        height=60,
        borderWidth=1,
        forceBorder=True,
        fieldFlags="multiline",
    )
    form.save()

    (BASE / "sample_data.csv").write_text(
        "name,email,company,notes\n"
        "Ada Lovelace,ada@example.com,Analytical Engines,Prefers morning calls\n"
        "Grace Hopper,grace@example.com,US Navy,Asked about bulk pricing\n",
        encoding="utf-8",
    )
    print(f"Wrote samples in {BASE}")


if __name__ == "__main__":
    main()
