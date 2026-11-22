# THE WORLD IN ONE DAY — Sunday 22 November 2026

[![Competition](https://img.shields.io/badge/make.fun-news--image--20261122-1a2a4a)](https://make.fun/bounty/news-image-20261122)
[![Entry](https://img.shields.io/badge/entry-35_stories_%C2%B7_7_regions-b22222)](https://make.fun/bounty/news-image-20261122)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A one-page front-page infographic summing up the world's news of
**Sunday 22 November 2026** — 35 stories across 7 regions, every one dated
that day. Built for the make.fun bounty
[`news-image-20261122`](https://make.fun/bounty/news-image-20261122)
($100 pot, top 50 paid, free entry).

## The day

- **COP31 collapses** — no deal in Antalya: the EU, UK and Panama object to a
  final text that never names fossil fuels. First COP to end with no deal
  since Copenhagen 2009.
- **Russia fires 186 drones** at Ukraine overnight; 161 downed or jammed.
  A five-storey block in Dymer is destroyed.
- **Iran claims two US radars hit; Bahrain denies it** — the IRGC says its
  strikes hit Patriot radars at Al-Riffa and Awali Sakhir; Bahrain says its
  defences intercepted the attacks.

Plus Verstappen's Las Vegas GP win, India's record 720/9 in New Zealand,
Hong Kong's Election Committee vote, the Bayelsa boat toll, BepiColombo
entering Mercury orbit — and 22 more stories, a world map with pins, a UTC
timeline, and a DATE CHECK box listing what was left out as another day's
news.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

Requirements: Python 3 + Pillow 10, Liberation fonts
(`/usr/share/fonts/truetype/liberation/`). No network access; two runs
produce identical bytes.

## Files

- `main.py` — the whole generator: layout, TrueType text, drawn
  illustrations, and the world map, all in code.
- `entry.png` — the rendered 1024×1024 front page (≤ 1 MiB).
- `.makefun/owner.json` — payout wallet for the bounty.

## Verification

Every story carries a source and a tag — CONFIRMED (2+ outlets), OFFICIAL
(on the record), REPORTED (one outlet), CLAIM (one side's account).
Numbers are attributed; claims are framed as claims; nothing from the
DATE CHECK exclusion list appears on the page.
