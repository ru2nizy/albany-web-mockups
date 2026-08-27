# Albany Web Mockups

Free redesign concept mockups for local businesses in Albany, Oregon.

**These are design concepts only.**  
They are **not affiliated** with the businesses shown and are not official websites.

The goal is to demonstrate what a modern, clean, mobile-friendly website could look like for real local businesses — both as portfolio pieces and as a potential starting point for actual collaboration.

---

## Current Mockups

Published from the hub at [`index.html`](./index.html):

| Business | Type | Folder |
|----------|------|--------|
| The Depot Restaurant | Fish & chips (est. 1976) | [`the-depot-restaurant/`](./the-depot-restaurant/) |
| Millie's Vintage Resale | Vintage / resale | [`millies-vintage-resale/`](./millies-vintage-resale/) |
| Brick & Mortar Cafe | Breakfast / brunch | [`brick-and-mortar-cafe/`](./brick-and-mortar-cafe/) |
| 1st Hand Seconds Unique Boutique + Chicee Chicee Bridal | Nonprofit resale & bridal | [`1st-hand-seconds-unique-boutique/`](./1st-hand-seconds-unique-boutique/) |
| Roger's Restaurant | Hometown diner (est. 1980) | [`rogers-restaurant/`](./rogers-restaurant/) |
| Vito's Trattoria | Italian | [`vitos-trattoria/`](./vitos-trattoria/) |
| The Squeaky Cork | Wine bar / Scottish pub | [`the-squeaky-cork/`](./the-squeaky-cork/) |
| Albany Antique Mall | Antiques | [`albany-antique-mall/`](./albany-antique-mall/) |
| Wicked Comics & Collectibles | Comics | [`wicked-comics/`](./wicked-comics/) |
| ReStyle Albany | Consignment | [`restyle-albany/`](./restyle-albany/) |
| Mudpie and Roses Boutique | Boutique / IOD | [`mudpie-and-roses-boutique/`](./mudpie-and-roses-boutique/) |
| Emma Downtown | Boutique | [`emma-downtown/`](./emma-downtown/) |
| The Natty Dresser | Menswear | [`the-natty-dresser/`](./the-natty-dresser/) |
| Sybaris Bistro | Farm-to-table bistro | [`sybaris-bistro/`](./sybaris-bistro/) |
| The Barn at Hickory Station | Taproom / venue | [`the-barn-at-hickory-station/`](./the-barn-at-hickory-station/) |

---

## Philosophy

- Keep the designs honest to the actual businesses
- Prioritize mobile experience
- Clear hierarchy, readable typography, and strong CTAs
- Always include a clear disclaimer that this is a concept

---

## How the pages are built

Each concept is a static `index.html` plus one shared stylesheet, [`assets/mockup.css`](./assets/mockup.css). Palettes and hero treatments stay in a short `:root` block on the page so a hours/copy tweak does not mean restyling fifteen files.

Heroes use CSS gradients (the same overlays the old photo backgrounds sat under). There are no Unsplash or Wix hotlinks, so GitHub Pages does not wait on a second origin or a 1.7MB brick-wall PNG. `.nojekyll` skips Jekyll processing on Pages.

`python scripts/check_pages.py` (and `.github/workflows/pages-health.yml`) refuses a missing mockup, missing disclaimer, remote image/font host, or a page that skipped the shared stylesheet.

---

## How to view

Open [`index.html`](./index.html), open the `index.html` inside a business folder, or use GitHub Pages:

https://ru2nizy.github.io/albany-web-mockups/

---

*Built as free design concepts for the Albany / mid-Willamette Valley community.*
