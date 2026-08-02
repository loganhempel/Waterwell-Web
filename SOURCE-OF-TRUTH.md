# Waterwell Naturopath (Kohei Iguchi) — Source of Truth
Updated: 2026-07-20

## Canonical
- **Website:** this folder (git repo → github.com/loganhempel/Waterwell-Web). `index.html`, `nz.html`, `au.html` (11 Jul) reflect the virtual-first / Australia move. `AUS-compliance-note-2026-07-11.md` governs AU page claims. `wordpress-booking-snippet/` ready to install.
- **Google Ads:** `gads-build-2026-07-16/` — 5 campaigns (NZ Brand / NZ Online Naturopath / NZ Skin Conditions / AU Online Naturopath / AU Skin Conditions) / 24 ad groups / **441 unique terms (expanded 20 Jul, up from 224)**, all phrase+exact paired, zero broad. Adds Gut & Digestive Health, Hormones & Women's Health, Fatigue & Energy, and Stress & Sleep ad groups (NZ + AU); splits Skin Conditions into all 6 condition pages (Eczema / TSW / Psoriasis / Acne / Rosacea / Skin Infections) on both sides; adds a General Naturopathy AU ad group with city-modified AU terms (Sydney/Melbourne/Brisbane/Perth/Adelaide). **20 Jul: every ad group's RSA copy rewritten from scratch** — the account previously recycled the same handful of headlines/descriptions across nearly all 24 groups; each group now has genuinely distinct copy grounded in real differentiators (dual Naturopath+Medical Herbalist qualification, 32 five-star reviews, functional/lab testing posted to the door, works alongside the patient's GP). AU copy re-audited against `AUS-compliance-note-2026-07-11.md` — no goods references, no outcome/testimonial claims, no serious-condition claims, no detox language, explicit "delivered online from NZ" / NZ-registered framing throughout. Sheet: https://docs.google.com/spreadsheets/d/19a2IUjy0NERVSLm8VxndInU5ULN-8OAqgRQZ0qYMZHA/edit — original pre-expansion JSON backed up to `Google Ads Buildout 2026-07-05/_backups/waterwell.backup-pre-2026-07-20-expansion.json`. See `gads-build-2026-07-16/README.md`.
- Prior builds kept as history: `gads-split-2026-07-12/` (first AU/NZ split, hand-built) and `gads-build-2026-07-05/` (original NZ-only JSON pipeline build) + `relaunch-2026-06/` (LAUNCH-PACKAGE-GOOGLE.md 4 Jul).
- June report: `Waterwell-June-Report-2026.pdf` (best month on record — 10 enquiries).

## AU page status (12 Jul)
`au.html` remediated against the compliance note §5 — see `AU-REMEDIATION-2026-07-12.md` (+ dated audit screenshots in root). NEEDS-KOHEI: AUD pricing, AU privacy policy, §6 sign-offs. ⚠ AU-only extra gate: the six `/conditions/` pages linked from au.html are un-audited AU click-paths — audit or de-link before AU campaigns unpause. Cal.com URL still a placeholder.

## Gates before spend
1. **WordPress admin access from Kohei** (chase drafted 12 Jul) → wire thank-you redirect → GA4 `generate_lead` → import to Ads. Audit found $470 / 1,282 clicks / 0 recorded conversions — Gravity Forms never fired an event.
2. Test conversion end-to-end before any budget.
3. Cal.com one-click booking added.
4. Billing confirmed.

## Next action
Build the Aus+NZ campaign split plan (geo, currency, landing pages nz.html/au.html, compliance-safe AU copy), then launch once tracking verified.

## Note
Folder renamed from `waterwell-preview` 12 Jul (git + Vercel links unaffected — all inside the folder).
