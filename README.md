<div align="center">

# pdftool

**Merge, split, watermark PDFs and fill AcroForm fields from a CSV — from the command line, no GUI.**

![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![pypdf](https://img.shields.io/badge/pypdf-4.x-blue?style=flat-square)
[![License](https://img.shields.io/github/license/Kennurken/pdf-toolkit?style=flat-square)](LICENSE)

<img src="assets/demo.gif" width="900" alt="pdftool merging, splitting, watermarking and filling PDFs in a terminal">

</div>

## Install

```bash
pip install git+https://github.com/Kennurken/pdf-toolkit
```

Or from a clone: `pip install -e .`

## Usage

```bash
# Merge in the given order
pdftool merge a.pdf b.pdf c.pdf -o combined.pdf

# Split into page ranges (1-based, inclusive; "7-" means 7 to the end)
pdftool split report.pdf --ranges 1-3,4-6,7- -o parts/

# Diagonal text watermark on every page
pdftool watermark contract.pdf --text CONFIDENTIAL --opacity 0.2 -o out.pdf

# Fill a form template once per CSV row; CSV headers must match field names
pdftool fill intake_form.pdf --data clients.csv -o filled/
```

`split` writes `report_p1-3.pdf`, `report_p4-6.pdf`, ...; `fill` writes `intake_form_row1.pdf`, `intake_form_row2.pdf`, ...

## Form filling details

- Columns whose header matches an AcroForm field name are written; extra columns are ignored.
- Fields missing from the CSV stay blank.
- A template without AcroForm fields exits with an error instead of writing broken files.
- XFA-only forms are not supported. Filled-field appearance depends on the viewer honoring `/NeedAppearances`.

## Try it with the bundled samples

```bash
git clone https://github.com/Kennurken/pdf-toolkit && cd pdf-toolkit
pip install -e .
pdftool fill sample_files/intake_form.pdf --data sample_files/sample_data.csv -o out/
```

Samples are regenerated with `python sample_files/build_samples.py`.

## License

MIT © Eldos Kydyrbek
