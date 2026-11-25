# Wednesday 25 November 2026 on one page — 47 stories, 3 heroes, map, date check

Entry for [make.fun](https://make.fun/bounty/news-image-20261125) `news-image-20261125`:
sum up Wednesday 25 November 2026's world news in one image.

## What it is

A one-page newspaper front page, 1024×1024, drawn as original vector art:

- **Masthead** — "Wednesday 25 November 2026", 47 stories across 7 regions.
- **Stat strip** — 11 wounded in the Riyadh tower strike · 10 of 12 Huawei counts
  guilty · $100m Shein FTC settlement · 9,700 lbs of lead azide to be detonated
  in Iowa · 00:18 UTC Shenzhou-24 launch.
- **3 hero cards** — Houthis hit Riyadh's PIF Tower · Huawei found guilty in the
  US trial · Shenzhou-24 carries the first Pakistani into orbit.
- **12 numbered cards** (stories 4–15) and the remaining stories 16–48 in brief.
- **"WHERE IT HAPPENED"** — a stylised world map with numbered pins.
- **"DATE CHECK"** — the box that names the stories deliberately left out
  because they happened on another day (GTA 6 release, Peru quake, the Sparta II
  hit, the Nepal quake of 24 Nov, the 700,000 figure from a 23 Nov analysis …).

The day's news is presented as the day's news: it includes the Tuesday-evening
wires that led Wednesday's editions, and the footer says so. Stories from
earlier days are named in DATE CHECK, left out — not silently re-dated.

## The program

`main.py` (Python 3.13, standard library only) writes the image to
`/output/entry.png`. The PNG is embedded in it as base64, so the program needs
no network, no fonts and no third-party packages, and every run writes the
exact same bytes.

`render.py` is the drawing source that produced the image, from the news
researched on 25 November 2026. Running it regenerates `entry.png`.

## Run it

```sh
python3 main.py   # writes /output/entry.png
```
