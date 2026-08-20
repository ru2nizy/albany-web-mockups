#!/usr/bin/env python3
"""Fail CI if a published Albany mockup is missing or loses its disclaimer."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "the-depot-restaurant",
    "millies-vintage-resale",
    "brick-and-mortar-cafe",
    "1st-hand-seconds-unique-boutique",
    "rogers-restaurant",
]


def main() -> int:
    fails: list[str] = []
    index = ROOT / "index.html"
    if not index.is_file():
        fails.append("missing index.html")
        index_text = ""
    else:
        index_text = index.read_text(encoding="utf-8", errors="replace")
        low = index_text.lower()
        if "not affiliated" not in low and "concepts only" not in low:
            fails.append("index.html is missing concept/disclaimer language")

    for slug in REQUIRED:
        page = ROOT / slug / "index.html"
        if not page.is_file():
            fails.append(f"missing {page.relative_to(ROOT)}")
            continue
        if f"./{slug}/" not in index_text and f"{slug}/" not in index_text:
            fails.append(f"index.html does not link to {slug}")
        text = page.read_text(encoding="utf-8", errors="replace").lower()
        if "not affiliated" not in text and "concept" not in text:
            fails.append(f"{page.relative_to(ROOT)} is missing disclaimer language")

    if fails:
        print("pages-health failed:")
        for line in fails:
            print(f"  - {line}")
        return 1
    print(f"ok: {len(REQUIRED)} mockups + index")
    return 0


if __name__ == "__main__":
    sys.exit(main())
