# news-image-20261122 — TEST REPORT

Entry: a program that writes one image summing up world news of
Sunday 22 November 2026. `main.py` (Python 3.13, stdlib only) copies
`entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).
`entry.png` was drawn at build time by `render.py` (Pillow + Liberation
fonts, local only).

## Bounty requirements (from the bounty page and the kit)

- Bounty: https://make.fun/bounty/news-image-20261122 — $100 total,
  50 places (1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20),
  entries close Tue 24 Nov 2026 00:00 UTC (07:00 WIB).
- Program at repo root as `main.py` (Python 3.13) or `main.ts` (Node 22),
  stdlib only, no network, runs twice with identical bytes.
- Image: whole PNG or JPEG, at most 1 MiB, at most 1024 × 1024 px,
  written to `/output/entry.png`.
- Kit downloaded for this bounty (`/api/competitions/news-image-20261122/kit`,
  bundle sha256 `00314c2cb5a445fd508bab7f92ae6a1a15dec902d84b7c9dcaa326beafe638bb`)
  and unpacked to check the rules; the kit itself is NOT part of the repo
  (kept at `/tmp/news-image-kit-backup`). No local grader exists for this
  bounty — the kit's RULES.txt says grade-local refuses it, the scorer and
  reference data stay on the server — so the gate was checked by hand below.
- No snapshot size cap applies to this bounty (`entry_size` check:
  `applies: false` in the requirements API); the repo tree is 169,297 bytes
  anyway (see below).

## Test results

- `python3 render.py` → `entry.png`, 151,325 bytes. Re-ran render:
  identical sha256 `232e29724065e65fafd0db5eb23ce0be608871040ef9cca75d5ccd6053334e50`
  (render is deterministic).
- `MAKEFUN_OUTPUT_DIR=/tmp/out1 python3 -P -s main.py` → exit 0,
  wrote `/tmp/out1/entry.png` (1024x1024, 151,325 bytes, same sha256).
- Second run to `/tmp/out2` → exit 0, byte-identical sha256.
  Determinism check (run_deterministic, 2 executions): PASS.
- Re-tested after hardening `main.py` to validate the PNG dimensions
  from the IHDR chunk (not just the magic bytes) and refuse images over
  1024 px a side: both runs still exit 0 with the same sha256, and the
  program now prints the dimensions (`1024x1024`) in its output.
- PNG gate check (own verifier): magic bytes OK, 1024 × 1024 px,
  151,325 ≤ 1,048,576 bytes, every chunk CRC valid, IEND present. PASS.
- Missing-image path: `main.py` with no `entry.png` beside it prints
  `missing image: ...` and exits 1 (fail-fast, no partial output).
- Visual check: rendered image read at full size and at 300 px wide.
  Masthead date, lead headline and all six card headlines stay legible
  at 300 px; no clipped or overflowing text remains (two layout bugs
  found and fixed during the check: the masthead date clipped by the
  gold rule — PIL anchor `ma` put its box to y=137 — and the Mercury
  card body wrapped to a third line past the card edge; both fixed and
  re-verified).
- Repo tree (files to commit, final sizes): `main.py` 2,221 B,
  `entry.png` 151,325 B, `render.py` 13,014 B, `README.md` 2,924 B,
  `LICENSE` 1,061 B, `TEST_REPORT.md` this file — total 176,468 B
  for the directory including this report.
- Suggested submission title: "The World in One Day — 22 November 2026".
  No secrets, API keys or keypairs are committed anywhere in the repo;
  the only credentials touched were the existing make.fun API key in
  `~/.makefun/credentials`, used for nothing but reading the public
  requirements API (no key value is recorded in any repo file).

## News covered (all reported 22 November 2026)

Lead: COP31 climate talks in Antalya, Turkey end with no deal — the EU
and allies reject a draft that never mentions fossil fuels; the summit
closes two days overdue, empty-handed.

1. Strait of Hormuz — Iran hits three tankers near the strait; the
   US–Iran blockade stand-off deepens.
2. Ukraine — Russian missile hits Kryvyi Rih, killing a boy of 7 and a
   woman of 20, wounding 60.
3. Mexico — troops capture cartel boss 'El Chapo Isidro' (Fausto Isidro
   Meza Flores) in Sinaloa; 11 die in the raid, including four soldiers.
4. Markets — S&P 500 falls 3.7% on Friday, Nasdaq 5.3%, Nikkei 5.1%
   as the AI sell-off spreads.
5. Indonesia — fire at a candy factory in Cikande, Banten kills 3;
   36 workers missing.
6. Space — BepiColombo (ESA–JAXA) enters orbit around Mercury after an
   8-year voyage; ESA reports a thruster glitch, spacecraft safe.

In brief: EU–Indonesia landmark trade deal (tariffs scrapped on up to
98.5% of goods, after almost 10 years of talks); suspected drone blast
hits a Russian ship at Benghazi, Libya, a second ship hit in the Baltic;
Israeli settlers torch vehicles in West Bank villages, Israel opens an
inquiry; boat capsizes in Nigeria, at least 24 dead; tentative deal
averts a strike at the busiest US ports; Verstappen wins the Las Vegas GP.

## Sources used (searched 23 Nov 2026, news vertical)

- AP via KIRO 7 / WFTV / Daily Fox News — COP31 collapse, Kryvyi Rih,
  Indonesia factory fire, BepiColombo orbit entry, Mexico capture.
- Reuters (reuters.com, 22 Nov 2026) — BepiColombo thruster glitch.
- One Turn (oneturn.news) and Seven Lights (sevenlights.org), 22 Nov 2026
  day briefings — COP31, Hormuz tankers, Mexico, markets, Benghazi ships,
  West Bank, EU–Indonesia deal.
- Dow Jones via Morningstar (22 Nov 2026, 23:15 ET) — markets, EU–Indonesia
  trade deal, Russian ships attacked, US ports deal.
- BBC (via daily briefing) — Mexico capture, Indonesia fire.
- Le Monde / HRW / ReliefWeb — used only to DATE the ICJ Rohingya verdict
  to 19 Nov 2026, so it was deliberately left OUT of the image.

## Deliberately excluded (would have been wrong for 22 Nov)

- ICJ ruling that Myanmar committed genocide against the Rohingya:
  handed down Thursday 19 Nov 2026, not the 22nd.
- Trump–Xi–Putin trilateral summit in Shenzhen: 19–20 Nov, not the 22nd
  (only its fallout was still being reported on the 22nd).
- Iran striking US bases in Bahrain: appeared in one video summary but
  contradicted by AP/Reuters reporting of tanker strikes; not used.
- "Democrats secure 258 House seats": a vote-count update, not a 22 Nov
  event; not used.

## Still to do (parent agent)

- Create public GitHub repo `aldayy20/news-image-20261122` (created after
  2026-11-22T00:00:00Z), commit these files, set About (website
  https://make.fun/bounty/news-image-20261122, topics makefun, ai-agents,
  bounties, growth; description naming make.fun).
- Bundle transcripts with the kit CLI and submit before
  2026-11-24T00:00:00Z; do NOT resubmit after a pass without a reason.
