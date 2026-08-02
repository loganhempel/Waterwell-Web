# Waterwell Naturopath — Google Ads Build v2
2026-07-16 · Client: Kohei Iguchi · waterwellclinic.co.nz · Emporom Media internal

## What changed vs the 12 Jul split build

| | Before (`gads-split-2026-07-12`) | Now (`gads-build-2026-07-16`) |
|---|---|---|
| Campaigns | 5 (NZ Brand / NZ Online Naturopath / NZ Skin Conditions / AU Online Naturopath / AU Skin Conditions) | Same 5 — structure kept, density added |
| Ad groups | 10 | 24 |
| Unique keyword terms | ~85 (100 phrase + only 23 exact — inconsistent pairing) | **224**, every term phrase **and** exact |
| Negatives | 127 rows | 1,546 rows (cross-negatived across all 24 groups) |
| RSAs | 9 of 10 ad groups had one (Other Skin Conditions NZ had none) | 24 of 24 ad groups have a full, char-validated RSA |

## New ad groups

**NZ | Online Naturopath campaign** — split the old "Online Naturopath Consult" + "General Naturopathy" pair into six:
- Online Naturopath Consult, General Naturopathy (expanded — city-modified: Auckland/Wellington/Christchurch/Hamilton/Tauranga/Dunedin)
- **Gut & Digestive Health** (new)
- **Hormones & Women's Health** (new)
- **Fatigue & Energy** (new)
- **Stress & Sleep** (new)

**NZ | Skin Conditions campaign** — split into all six condition pages that already exist on the site (`/conditions/*.html`), matching site structure 1:1: Eczema, Topical Steroid Withdrawal, **Psoriasis** (new), **Acne** (new), **Rosacea** (new), **Skin Infections** (new — this ad group previously had keywords but zero RSA copy, a live gap now fixed).

**AU | Online Naturopath campaign** — added **General Naturopathy AU** (city-modified: Sydney/Melbourne/Brisbane/Perth/Adelaide), **Gut & Digestive Health AU**, **Hormones & Women's Health AU**, **Fatigue & Energy AU**.

**AU | Skin Conditions campaign** — split the old single "Skin Support AU" catch-all into **Psoriasis AU**, **Acne AU**, **Rosacea AU**, **Skin Infections AU**, alongside the existing Eczema AU / TSW AU.

## Keyword expansion approach

Per the google-ads-sheet-builder skill's playbook: dropped the geo suffix where it made sense (bare "naturopath auckland" style city terms alongside "online naturopath" terms — a real volume lever since Kohei is NZ/AU-wide online, not location-fenced), added symptom/concern long-tail (leaky gut, hormonal acne, adrenal fatigue, red skin syndrome, etc.), and kept every term paired phrase + exact, zero broad — same standard as the Singh Pest Control reference build.

## AU compliance — re-audited against `AUS-compliance-note-2026-07-11.md`

Every new AU ad group follows the note's section 3/4 rules: soft "book a consultation to discuss X" framing (no cure/treat claims), no goods/supplement references, no before/after or outcome testimonials (the "he beat eczema himself" personal-credibility line stays NZ-only, deliberately excluded from every AU RSA), explicit "delivered online from NZ" / "NZ-registered naturopath" disclosure, no serious-condition claims. Added precautionary negatives on the AU Hormones group (pcos, hashimoto, thyroid disease, autoimmune disease, cancer, diabetes, depression) so Google's phrase-match query expansion can't pull in serious-condition-adjacent searches on a group that wasn't built to serve them.

**This does not change the AU launch gate.** AU campaigns stay paused until every box in `AUS-compliance-note-2026-07-11.md` §6 and `LAUNCH-GATES.md` is green — landing-page audit, Kohei's Ahpra confirmation, the telemedicine-certification question, and Kohei's written sign-off are all still open.

## Launch gates — unchanged, still open

Copied into this folder: `LAUNCH-GATES.md`. Nothing in this rebuild touches conversion tracking, WordPress access, or Cal.com booking — all four gates from the 12 Jul build are still red. **This build is launch-ready, not launch-cleared.** See `SOURCE-OF-TRUTH.md` for the live status.

## Files

- `editor/` — Google Ads Editor import CSVs (campaigns → adgroups → keywords → ads → negatives, import in that order)
- `Waterwell Naturopath-PLAN.xlsx` — full planning workbook, one tab per ad group
- `waterwell-MASTER.csv` — human-readable match-type-formatted master sheet (also uploaded to Drive as a Sheet for review)
- `LAUNCH-GATES.md` — the four gates that must be green before NZ spend, plus the AU-only compliance gates
