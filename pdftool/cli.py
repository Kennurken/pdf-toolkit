"""Argparse CLI for pdftool subcommands."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pdftool import fill, merge, split, watermark
from pypdf.errors import PyPdfError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdftool",
        description="Merge, split, watermark, and fill PDF forms.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    merge_p = sub.add_parser("merge", help="Merge PDFs in the given order")
    merge_p.add_argument("inputs", nargs="+", help="Input PDF files")
    merge_p.add_argument("-o", "--output", required=True, help="Output PDF path")

    split_p = sub.add_parser("split", help="Split a PDF by page ranges")
    split_p.add_argument("input", help="Input PDF")
    split_p.add_argument(
        "--ranges",
        required=True,
        help="Comma-separated ranges, e.g. 1-3,4-6,7-",
    )
    split_p.add_argument("-o", "--output", required=True, help="Output directory")

    wm_p = sub.add_parser("watermark", help="Diagonal text watermark on every page")
    wm_p.add_argument("input", help="Input PDF")
    wm_p.add_argument("--text", required=True, help="Watermark text")
    wm_p.add_argument("-o", "--output", required=True, help="Output PDF path")
    wm_p.add_argument("--font-size", type=float, default=54.0, help="Font size (default 54)")
    wm_p.add_argument(
        "--opacity",
        type=float,
        default=0.25,
        help="Opacity 0-1 (default 0.25)",
    )

    fill_p = sub.add_parser("fill", help="Fill AcroForm fields from a CSV (one PDF per row)")
    fill_p.add_argument("template", help="Fillable PDF template")
    fill_p.add_argument("--data", required=True, help="CSV whose headers match field names")
    fill_p.add_argument("-o", "--output", required=True, help="Output directory")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "merge":
            out = merge.merge_pdfs([Path(p) for p in args.inputs], Path(args.output))
            print(f"Wrote {out}")
        elif args.command == "split":
            written = split.split_pdf(Path(args.input), args.ranges, Path(args.output))
            for path in written:
                print(f"Wrote {path}")
        elif args.command == "watermark":
            out = watermark.watermark_pdf(
                Path(args.input),
                Path(args.output),
                text=args.text,
                font_size=args.font_size,
                opacity=args.opacity,
            )
            print(f"Wrote {out}")
        elif args.command == "fill":
            written = fill.fill_from_csv(
                Path(args.template), Path(args.data), Path(args.output)
            )
            for path in written:
                print(f"Wrote {path}")
        else:
            parser.error(f"Unknown command: {args.command}")
            return 2
    except (FileNotFoundError, ValueError, OSError, PyPdfError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
