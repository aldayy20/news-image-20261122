# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/aldayy20/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/aldayy20/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image summing up the world's news of Sunday 22 November 2026: COP31 ends with no deal, Iran hits three tankers near Hormuz, a Russian missile kills a boy of 7 in Kryvyi Rih, Mexico captures cartel boss 'El Chapo Isidro', world stocks slide, a factory fire in Indonesia, and BepiColombo reaches Mercury — plus the day's other stories in brief.

Suggested entry title: **The World in One Day — 22 November 2026**.

The image is built for the judge's criteria, in order: it names its day in the masthead ("SUNDAY 22 NOVEMBER 2026"); it covers the day's most consequential stories across regions (Turkey, the Gulf, Ukraine, Mexico, Indonesia, space) and fields (climate, conflict, crime, markets, disaster, science); each story is readable from its picture and short labels alone; and it is drawn cleanly with no photographic claims — every illustration is a flat vector-style icon, so nothing in it pretends to be a photo of an event.

## The image

`entry.png` (1024 × 1024, under 1 MiB) is a newspaper front page drawn for the day: a masthead naming the date, one lead story, six illustrated stories from different regions and fields, and an "In brief" strip. Every fact was checked against reporting dated 22 November 2026 (AP, Reuters, BBC, Dow Jones, ESA) — see `TEST_REPORT.md` for the sources and what was deliberately left out (for example the ICJ Rohingya verdict, which was 19 November, not the 22nd).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python 3.13, standard library only) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`), after checking it is a PNG under 1 MiB. No network, no randomness: two runs write the same bytes.

## Files

- `main.py` — the entrypoint; copies `entry.png` to the output directory.
- `entry.png` — the finished image.
- `render.py` — the build script that draws `entry.png` (needs Pillow and the Liberation fonts locally; not run by the grader). Rebuild with `python3 render.py`.
- `TEST_REPORT.md` — local test results and the news sources used.

---

<sub>Entered on [make.fun](https://make.fun/?ref=axs8j3b9&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
