# Waterwell Naturopath (Kohei Iguchi) — Source of Truth
Updated: 2026-08-03

## ⚠ Premise change — read first
**Kohei has relocated to Australia and practises from there.** This invalidates
`AUS-compliance-note-2026-07-11.md` at the premise — that note is banner-marked
SUPERSEDED. Use **`AUS-compliance-note-2026-08-03.md` (v2)**. Two things v1
*required* (state NZ registration; disclose delivery from New Zealand) are now
false statements under ACL s.18/s.29.

**Blocking unknown: which Australian state/territory.** The National Code of
Conduct is administered per jurisdiction and the complaints body differs. This
blocks `code-of-conduct.html` and part of the AU landing-page checklist.

## Canonical
- **Website:** this folder (git → github.com/loganhempel/Waterwell-Web).
  `index.html`, `nz.html`, `au.html` + **10** `conditions/` pages (6 skin,
  4 whole-body added 3 Aug). `privacy.html` and `code-of-conduct.html` exist
  but **are NOT deployable** — 7 NEEDS-KOHEI placeholders between them.
- **Google Ads:** `gads-build-2026-08-03/` — 5 campaigns / 24 ad groups /
  878 keyword rows / 407 unique terms. Source of truth is
  `~/Client Work/Google Ads Buildout 2026-07-05/data/waterwell.json`.
  Regenerate artefacts with `build_master_csv.py` + `build_workbooks.py`.
- **Kohei's review pack:** `Waterwell-Ad-Copy-FOR-KOHEI-2026-08-03.html` —
  tall format, one line per row, live char counts. The 20 Jul sheet was WIDE
  and he could not widen columns past H, so **his 12 comments were never a
  complete review.** Send the HTML, not a sheet.
- Prior builds kept as history: `gads-build-2026-07-16/`, `gads-split-2026-07-12/`,
  `gads-build-2026-07-05/`, `relaunch-2026-06/`.
- June report: `Waterwell-June-Report-2026.pdf` (best month on record, 10 enquiries).

## ⚠ index.html is the master — nz.html and au.html are GENERATED
Never hand-edit `nz.html` or `au.html`. Edit `index.html`, then run
`python3 tools/build_geo.py`.

**AU compliance is part of generation** (moved there 3 Aug). It used to be a
post-hoc patch applied to the generated au.html, while `index.html` still
contained every banned pattern — so re-running the generator silently
reintroduced all of them. That is how the 12 Jul remediation was lost.
`build_geo.py` now applies the 20 AU compliance edits during generation and
**refuses to write au.html if anything banned survives**, auditing visible copy
*and* JSON-LD (structured data was a blind spot: "medical herbalism" had
survived in the MedicalClinic description).

Content that is legitimate in NZ — herbal medicine, supplements, testimonials,
MNMHNZ — stays on index/nz and is stripped only for AU.

`remediate_au.py` is now **audit-only** (`--check`); its patch mode refuses to
run, so there is one source of truth.

## Tooling (all in tools/, all gated — they fail loudly rather than silently no-op)
- `build_conditions.py` — the 10 condition pages, with an AU compliance gate
- `build_ad_review_pack.py` — Kohei's tall CSV + branded HTML from the JSON
- `remediate_au.py [--check]` — au.html compliance pass / audit
- `build_legal.py` — privacy + code-of-conduct pages
- `add_wholebody_section.py`, `fix_booking_conversion.py` — one-shot site patches
- `build_geo.py`, `build_blog.py` — pre-existing

## Ad-group → landing page (all 24 now have a real destination)
Brand / Online Naturopath / General Naturopathy → `/nz` or `/au` (correct).
Every condition ad group, both geos → its own `conditions/` page.


## Concepts + section harvest (3 Aug)
`concepts-2026-07-20/` holds the four 20 Jul landing-page concepts (Deep Current,
The Dossier, Vitals, Root & Bloom), recovered from the session transcript after
the scratchpad was lost. `SECTION-HARVEST.html` in that folder is the decision
page: nine candidate sections, ranked, with the outcome recorded.

**Ported into production:** A1 numbered conditions list (replaced the card grid,
which was built for six conditions and had to carry ten) and C1 alternating
zig-zag process path. A2 was already present. A3 / B3 / B2 / A4 / D1 were
dropped — production already does each of those jobs as well or better.

The concepts themselves are NOT production-ready: all four reference medical
herbalism and none carry AU compliance treatment. Anything further must go
through `index.html` and `build_geo.py`.


## Craft pass (3 Aug) — measured, not eyeballed
A Playwright audit of every section produced the fix list; all 16 pages now
measure clean: **0 WCAG AA contrast failures, 0 tap targets under 40px, 0 images
without intrinsic dimensions, 0 JS errors, no horizontal scroll at 390px.**

Two accessible text tokens were added because `--sage` (3.25:1) and `--sand`
(2.07:1) were used as the colour for eyebrows, meta pills, step numbers and star
ratings across every section, and both fail AA for small text:
- `--sage-text:#5A715D` (4.60:1)
- `--sand-text:#7E694C` (4.54:1)

**The brand tokens are unchanged.** `--sage` and `--sand` still drive every
decorative use — icons, rules, gradients, borders, large display type. Only
small text moved. Before/After pills were white on brand sage (3.75:1) and are
now on #4E6151 (6.66:1).

The same tokens were pushed into `build_conditions.py`, `build_legal.py` and
`blog.html` so the whole site is consistent.

⚠ `tools/build_blog.py` cannot run — it reads `/tmp/ww_posts.json`, which is
gone. `blog.html` was patched directly. Rebuild that data source before touching
the blog again.

## Gates before spend
1. **Conversion tracking.** Audit found $470 / 1,282 clicks / 0 conversions.
   TWO root causes: (a) Gravity Forms never fired; (b) **the site's own booking
   form was a `mailto:` handoff, which cannot fire a conversion at all** —
   fixed 3 Aug, now a Web3Forms POST + `generate_lead`, but **needs a real
   Web3Forms access key**; until then it falls back to mailto. Never add
   `ccemail` (HTTP 400 on free, kills the submission invisibly).
2. WordPress admin access from Kohei (chase drafted 12 Jul, still open).
3. Cal.com link — `cal.com/waterwell/discovery` **404s** (verified 3 Aug).
   CTA repointed at `#visit`; swap back when the real calLink lands.
4. Which Australian state (see above).
5. Privacy policy live — now a HARD gate, not "low urgency": naturopaths are
   health service providers and the Privacy Act small-business exemption does
   not apply to them.
6. Google telemedicine/LegitScript question — riskier now he is AU-based.
7. Billing confirmed.

## Note
Folder renamed from `waterwell-preview` 12 Jul. `build_conditions.py` still had
the stale path until 3 Aug.
