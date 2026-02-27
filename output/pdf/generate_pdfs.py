#!/usr/bin/env python3
"""
Regenerate PDF reports from markdown source files.

Requirements (install once):
    sudo apt-get install -y pandoc texlive-xetex texlive-lang-japanese fonts-noto-cjk

Usage:
    python3 output/pdf/generate_pdfs.py
    python3 output/pdf/generate_pdfs.py --kansei      # kansei brief only
    python3 output/pdf/generate_pdfs.py --executive   # executive report only
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent  # repo root
PDF_DIR = Path(__file__).parent             # output/pdf/

DOCS = {
    "kansei": {
        "source": PDF_DIR / "kansei_brief_pdf.md",
        "output": PDF_DIR / "KANSEI_RESEARCH_BRIEF.pdf",
    },
    "executive": {
        "source": PDF_DIR / "executive_report_pdf.md",
        "output": PDF_DIR / "EXECUTIVE_REPORT.pdf",
    },
}


def check_deps():
    missing = []
    for tool in ("pandoc", "xelatex"):
        if not shutil.which(tool):
            missing.append(tool)
    if missing:
        print(f"[ERROR] Missing tools: {', '.join(missing)}")
        print()
        print("Install with:")
        print("  sudo apt-get install -y pandoc texlive-xetex texlive-lang-japanese fonts-noto-cjk")
        sys.exit(1)

    # Check font
    result = subprocess.run(
        ["fc-list", "Noto Sans CJK JP"],
        capture_output=True, text=True
    )
    if not result.stdout.strip():
        print("[ERROR] Font 'Noto Sans CJK JP' not found.")
        print("  Install with: sudo apt-get install -y fonts-noto-cjk")
        sys.exit(1)


def build(name: str, doc: dict) -> bool:
    source = doc["source"]
    output = doc["output"]

    if not source.exists():
        print(f"[ERROR] Source not found: {source}")
        return False

    print(f"  Building {output.name} ...", end=" ", flush=True)
    result = subprocess.run(
        ["pandoc", str(source), "--pdf-engine=xelatex", "-o", str(output)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        size_kb = output.stat().st_size // 1024
        print(f"OK  ({size_kb} KB)")
        return True
    else:
        print("FAILED")
        print(result.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Regenerate PDF reports.")
    parser.add_argument("--kansei",    action="store_true", help="Build kansei brief only")
    parser.add_argument("--executive", action="store_true", help="Build executive report only")
    args = parser.parse_args()

    # Default: build all
    targets = list(DOCS.keys())
    if args.kansei and not args.executive:
        targets = ["kansei"]
    elif args.executive and not args.kansei:
        targets = ["executive"]

    print("Checking dependencies...")
    check_deps()
    print("  pandoc + xelatex + Noto Sans CJK JP: OK")
    print()

    print("Generating PDFs:")
    results = {name: build(name, DOCS[name]) for name in targets}

    print()
    if all(results.values()):
        print("Done. Output files:")
        for name in targets:
            p = DOCS[name]["output"]
            print(f"  {p.relative_to(ROOT)}")
    else:
        failed = [n for n, ok in results.items() if not ok]
        print(f"[ERROR] Failed: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
