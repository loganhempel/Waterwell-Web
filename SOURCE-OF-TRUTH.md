# Waterwell Naturopath (Kohei Iguchi) — Source of Truth
Updated: 2026-07-12

## Canonical
- **Website:** this folder (git repo → github.com/loganhempel/Waterwell-Web). `index.html`, `nz.html`, `au.html` (11 Jul) reflect the virtual-first / Australia move. `AUS-compliance-note-2026-07-11.md` governs AU page claims. `wordpress-booking-snippet/` ready to install.
- **Google Ads:** `gads-build-2026-07-05/` (5 Jul workbook build) + `relaunch-2026-06/` (LAUNCH-PACKAGE-GOOGLE.md 4 Jul; 7 ad groups, 65 phrase kw, 36 negatives). ⚠ Both pre-date the AU move — **Aus+NZ campaign split still to be built.**
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
