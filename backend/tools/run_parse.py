"""
Simple CLI to run ParsePipeline on a local PDF file for development/testing.
Usage:
    python tools/run_parse.py /path/to/file.pdf

This will extract images and print LaTeX outputs to stdout.
"""
import sys
from pathlib import Path

from app.services.parse_pipeline import ParsePipeline


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/run_parse.py /path/to/file.pdf")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])
    if not pdf_path.exists():
        print("File not found:", pdf_path)
        sys.exit(2)

    output_dir = pdf_path.with_suffix("").with_name(pdf_path.stem + "_extracted")
    output_dir = Path("uploads") / output_dir.name
    output_dir.mkdir(parents=True, exist_ok=True)

    parser = ParsePipeline()
    results = parser.parse_pdf(str(pdf_path), str(output_dir))

    print("--- LaTeX outputs ---")
    for i, r in enumerate(results, start=1):
        print(f"[{i}]", r)


if __name__ == "__main__":
    main()
