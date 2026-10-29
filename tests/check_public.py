#!/usr/bin/env python3
"""Check that the public repository stays public-safe and internally consistent.

Fails on:
  - any data file (CSV, Excel, JSONL, Parquet, ZIP, database, HDF5);
  - any file larger than 2 MB;
  - a missing or invalid figure;
  - a missing README section;
  - a broken relative link in README.md, docs/*.md or docs/*.html;
  - a figure that is not reproducible from scripts/make_figures.py.

Standard library only.
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_SUFFIXES = {".csv", ".tsv", ".xls", ".xlsx", ".jsonl", ".parquet", ".feather",
                 ".zip", ".gz", ".bz2", ".h5", ".hdf5", ".db", ".sqlite", ".bin"}
FIGURES = ["coefficients.svg", "curve.svg", "factor.svg", "pipeline.svg",
           "scorecard.svg", "walkforward.svg"]
REQUIRED = ["## The question", "## The idea in one picture", "## What we found",
            "## How it works", "## What is built, what is in progress, what is researched",
            "## What is not in this repository"]
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HTML_LINK = re.compile(r'href="([^"]+)"')


def fail(message: str) -> None:
    print("FAIL:", message)
    raise SystemExit(1)


def check_no_data() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in DATA_SUFFIXES:
            fail("data-like file present: %s" % path.relative_to(ROOT))
        if path.stat().st_size > 2_000_000:
            fail("file larger than 2 MB: %s" % path.relative_to(ROOT))


def check_figures() -> None:
    for name in FIGURES:
        path = ROOT / "docs" / "figures" / name
        if not path.is_file():
            fail("missing figure: %s" % name)
        text = path.read_text(encoding="utf-8")
        if not text.startswith("<svg") or "</svg>" not in text:
            fail("not an SVG: %s" % name)
    before = {name: hashlib.sha256((ROOT / "docs" / "figures" / name).read_bytes()).hexdigest()
              for name in FIGURES}
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "make_figures.py")],
                            capture_output=True, text=True)
    if result.returncode != 0:
        fail("make_figures.py failed: %s" % result.stderr.strip())
    after = {name: hashlib.sha256((ROOT / "docs" / "figures" / name).read_bytes()).hexdigest()
             for name in FIGURES}
    if before != after:
        fail("figures are not reproducible from scripts/make_figures.py")


def check_readme() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    for heading in REQUIRED:
        if heading not in text:
            fail("README is missing %r" % heading)
    if "No market data" not in text:
        fail("README does not state that no market data is published")


def resolve(target: str, source: pathlib.Path) -> None:
    target = target.split("#", 1)[0].strip()
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return
    path = (source.parent / target).resolve()
    if not path.exists():
        fail("broken link in %s: %s" % (source.relative_to(ROOT), target))


def check_links() -> None:
    for name in ["README.md", "docs/explainer.md", "docs/methodology.md",
                 "docs/roadmap.md", "docs/data-and-licences.md", "docs/research.md",
                 "docs/reproducing.md"]:
        source = ROOT / name
        for target in LINK.findall(source.read_text(encoding="utf-8")):
            resolve(target, source)
    for name in ["docs/index.html", "docs/explainer.html"]:
        source = ROOT / name
        for target in HTML_LINK.findall(source.read_text(encoding="utf-8")):
            resolve(target, source)


def main() -> int:
    check_no_data()
    check_figures()
    check_readme()
    check_links()
    print("ok: no data files, figures reproducible, README complete, links resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())