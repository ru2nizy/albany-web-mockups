#!/usr/bin/env python3
"""Fail CI if published mockups are missing, unaffiliated copy is gone, or Pages got slower.

This is the repo's automated gate for GitHub Pages health. It is intentionally
strict about remote image/font hosts: those extra DNS/TLS hops and multi-hundred-KB
heroes (including a 1.7MB Wix PNG) are what made the published concepts feel slow.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

# Existing concept folders only. Do not add a slug here unless a real mockup
# already exists for that business — this list is not a lead-generation queue.
KNOWN_MOCKUPS = (
    "1st-hand-seconds-unique-boutique",
    "albany-antique-mall",
    "brick-and-mortar-cafe",
    "emma-downtown",
    "millies-vintage-resale",
    "mudpie-and-roses-boutique",
    "restyle-albany",
    "rogers-restaurant",
    "sybaris-bistro",
    "the-barn-at-hickory-station",
    "the-depot-restaurant",
    "the-natty-dresser",
    "the-squeaky-cork",
    "vitos-trattoria",
    "wicked-comics",
)

SHARED_CSS = Path("assets/mockup.css")
SHARED_CSS_HREF = "../assets/mockup.css"

# Third-party asset hosts that add DNS, TLS, and often 150KB–1.7MB per hero.
BLOCKED_ASSET_HOSTS = (
    "images.unsplash.com",
    "plus.unsplash.com",
    "static.wixstatic.com",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "cdnjs.cloudflare.com",
    "unpkg.com",
    "jsdelivr.net",
)

REMOTE_CSS_URL = re.compile(r"url\(\s*['\"]?https?://", re.I)
INDEX_HREF = re.compile(r'href="\./([^"/]+)/"', re.I)
MAX_MOCKUP_HTML_BYTES = 16_384  # 16 KiB — layout lives in the shared stylesheet
MAX_SHARED_CSS_BYTES = 12_288


def _has_disclaimer(text: str) -> bool:
    # "Concept Redesign" in the title is not enough — require affiliation language.
    return "not affiliated" in text.lower()


def _blocked_hosts_in(text: str) -> list[str]:
    low = text.lower()
    return [host for host in BLOCKED_ASSET_HOSTS if host in low]


def _index_slugs(index_text: str) -> list[str]:
    return INDEX_HREF.findall(index_text)


def main() -> int:
    fails: list[str] = []

    index = ROOT / "index.html"
    if not index.is_file():
        fails.append("missing index.html")
        index_text = ""
    else:
        index_text = index.read_text(encoding="utf-8", errors="replace")
        if not _has_disclaimer(index_text):
            fails.append("index.html is missing concept/disclaimer language")
        blocked = _blocked_hosts_in(index_text)
        if blocked:
            fails.append(f"index.html loads blocked remote assets: {', '.join(blocked)}")

    css_path = ROOT / SHARED_CSS
    if not css_path.is_file():
        fails.append(f"missing {SHARED_CSS} (shared mockup stylesheet)")
        css_text = ""
    else:
        css_text = css_path.read_text(encoding="utf-8", errors="replace")
        css_size = css_path.stat().st_size
        if css_size > MAX_SHARED_CSS_BYTES:
            fails.append(f"{SHARED_CSS} is {css_size} bytes (budget {MAX_SHARED_CSS_BYTES})")
        if REMOTE_CSS_URL.search(css_text):
            fails.append(f"{SHARED_CSS} contains a remote url() — keep assets local")
        blocked = _blocked_hosts_in(css_text)
        if blocked:
            fails.append(f"{SHARED_CSS} references blocked hosts: {', '.join(blocked)}")
        for needle in (".nav {", ".hero {", ".info-grid {", ".cta-band {", ".disclaimer {"):
            if needle not in css_text:
                fails.append(f"{SHARED_CSS} is missing expected layout rule {needle!r}")

    if not (ROOT / ".nojekyll").is_file():
        fails.append("missing .nojekyll (skip Jekyll on GitHub Pages)")

    linked = _index_slugs(index_text)
    missing_from_index = [slug for slug in KNOWN_MOCKUPS if f"./{slug}/" not in index_text]
    for slug in missing_from_index:
        fails.append(f"index.html does not link to {slug}")

    unknown = [slug for slug in linked if slug not in KNOWN_MOCKUPS]
    for slug in unknown:
        fails.append(
            f"index.html links to {slug}, which is not in KNOWN_MOCKUPS "
            "(do not invent new client work in this health check)"
        )

    for slug in KNOWN_MOCKUPS:
        page = ROOT / slug / "index.html"
        rel = page.relative_to(ROOT).as_posix()
        if not page.is_file():
            fails.append(f"missing {rel}")
            continue
        text = page.read_text(encoding="utf-8", errors="replace")
        size = page.stat().st_size
        if size > MAX_MOCKUP_HTML_BYTES:
            fails.append(f"{rel} is {size} bytes (budget {MAX_MOCKUP_HTML_BYTES}; move layout CSS to {SHARED_CSS})")
        if not _has_disclaimer(text):
            fails.append(f"{rel} is missing disclaimer language")
        if SHARED_CSS_HREF not in text:
            fails.append(f"{rel} does not link {SHARED_CSS_HREF}")
        if REMOTE_CSS_URL.search(text):
            fails.append(f"{rel} has a remote CSS url() (hotlinked image/font)")
        blocked = _blocked_hosts_in(text)
        if blocked:
            fails.append(f"{rel} references blocked remote assets: {', '.join(blocked)}")

    if fails:
        print("pages-health failed:")
        for line in fails:
            print(f"  - {line}")
        return 1
    print(
        f"ok: {len(KNOWN_MOCKUPS)} mockups + index + {SHARED_CSS} "
        f"(no remote heroes/fonts)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
