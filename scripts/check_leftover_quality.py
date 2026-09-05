#!/usr/bin/env python3
"""Quality bar for the four leftover Albany mockups approved for public Pages."""
from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

PAGES = {
    "brasa-restaurant": {
        "tel": "tel:+15417917105",
        "display": "(541) 791-7105",
        "site": "https://www.dinebrasa.com/",
        "mailto": None,
        "hours_phrase": "Call for hours",
    },
    "sweet-red-bistro": {
        "tel": "tel:+15417040510",
        "display": "(541) 704-0510",
        "site": "http://sweetredwinebistro.com/",
        "mailto": None,
        "hours_phrase": "4pm – 10ish",
    },
    "vault-244": {
        "tel": "tel:+15417919511",
        "display": "(541) 791-9511",
        "site": "http://www.vault244.com/",
        "mailto": "mailto:info@vault244.com",
        "hours_phrase": "4:00PM – 10:00PM",
    },
    "loafers-station": {
        "tel": "tel:+15419268183",
        "display": "(541) 926-8183",
        "site": "https://www.loaferstation.com/",
        "mailto": None,
        "hours_phrase": "Call for hours",
    },
}

HREF = re.compile(r'href="(#[^"]+)"')
ID = re.compile(r'\bid="([^"]+)"')
MAILTO = re.compile(r'href="mailto:[^"]+"', re.I)
IMG = re.compile(r"<img\b", re.I)
VIEWPORT = 'name="viewport"'
OFFICIAL = re.compile(
    r'href="([^"]+)"[^>]*target="_blank"[^>]*rel="noopener"[^>]*>\s*Official site',
    re.I | re.S,
)
OFFICIAL_ALT = re.compile(
    r'target="_blank"[^>]*rel="noopener"[^>]*href="([^"]+)"[^>]*>\s*Official site',
    re.I | re.S,
)


def main() -> int:
    fails: list[str] = []
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    for slug in PAGES:
        if f'href="./{slug}/"' not in index:
            fails.append(f"index.html is missing card for {slug}")

    for slug, spec in PAGES.items():
        rel = f"{slug}/index.html"
        page = ROOT / rel
        if not page.is_file():
            fails.append(f"missing {rel}")
            continue
        text = page.read_text(encoding="utf-8")
        if VIEWPORT not in text:
            fails.append(f"{rel} missing meta viewport")
        if "<img" in text.lower():
            fails.append(f"{rel} contains an <img> tag")
        if "position: sticky" not in (ROOT / "assets/mockup.css").read_text():
            fails.append("shared CSS lost sticky header")
        if spec["tel"] not in text:
            fails.append(f"{rel} missing {spec['tel']}")
        if spec["display"] not in text:
            fails.append(f"{rel} missing display phone {spec['display']}")
        if spec["hours_phrase"] not in text:
            fails.append(f"{rel} missing hours phrase {spec['hours_phrase']!r}")
        if "Design Concept Mockup" not in text:
            fails.append(f"{rel} missing Design Concept Mockup footer")
        if "not affiliated" not in text.lower() or "not the official" not in text.lower():
            fails.append(f"{rel} missing not-official / not-affiliated language")
        official = OFFICIAL.search(text) or OFFICIAL_ALT.search(text)
        if not official:
            fails.append(f"{rel} missing Official site button with target=_blank rel=noopener")
        elif spec["site"] not in official.group(1):
            fails.append(f"{rel} Official site href is {official.group(1)!r}")
        mailtos = MAILTO.findall(text)
        if spec["mailto"] is None:
            if mailtos:
                fails.append(f"{rel} has mailto but none was published for this mockup")
        else:
            if spec["mailto"] not in text:
                fails.append(f"{rel} missing {spec['mailto']}")
        ids = set(ID.findall(text))
        for href in HREF.findall(text):
            target = href[1:]
            if target not in ids:
                fails.append(f"{rel} nav/CTA {href} has no matching id")
        if "Monday" in text and slug == "vault-244":
            # Allowed only as "Monday hours were not listed"
            if "Monday hours were not listed" not in text:
                fails.append(f"{rel} invents Monday hours")

    if fails:
        print("leftover quality failed:")
        for line in fails:
            print(f"  - {line}")
        return 1
    print(f"ok: {len(PAGES)} leftover mockups meet the quality bar")
    return 0


if __name__ == "__main__":
    sys.exit(main())
