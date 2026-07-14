# Waterwell — Launch Gates (no spend until ALL four are green)

Account 1256973392 · 12 July 2026 · All campaigns import as **Paused** and stay paused until this page is green.

| # | Gate | Status | What "green" means |
|---|---|:---:|---|
| 1 | **Conversion tracking verified end-to-end** | ❌ | Current state: $470 spent / 1,282 clicks / **0 conversions recorded** — Gravity Forms never fired an event. Green = thank-you redirect live → GA4 `generate_lead` key event → imported into Google Ads → **one real test submission visible in the Ads UI**. No spend on modelled hope. |
| 2 | **WordPress admin access from Kohei** | ❌ | Chase drafted 12 Jul. Needed to wire the redirect/snippet (gate 1) and to ship nz/au pages at their final URLs. Green = Logan logged in, snippet installed. |
| 3 | **Billing confirmed** | ❓ | Active payment method on the account, no suspension. 2-minute check in the UI — do it before Post, not after. |
| 4 | **Cal.com booking live** | ❌ | Both pages ship a "book straight off the calendar" flow; paid clicks leak without it. Green = a test booking completed from nz.html AND au.html on the live domain. |

**NZ campaigns:** may post the day gates 1–4 are green.

**AU campaigns:** gates 1–4 PLUS the AU-only gates from `AUS-compliance-note-2026-07-11.md` §6:
- au.html passes the note's §5 checklist — it currently **fails** (before/after gallery, herbal/supplement service cards, "detox pathways", "international dispensaries", "in Sydney, Australia" footer, no AUD/flagged pricing, no delivered-from-NZ disclosure). Fix the page, save a dated audit screenshot to this folder.
- Kohei confirms in writing he holds no Ahpra registration in any profession.
- Google telemedicine-certification question resolved (clean ad review, written confirmation, or LegitScript). If ads are disapproved for certification: STOP, don't resubmit-spam.
- Kohei signs off on the compliance note, including the residual cross-border ambiguity.
- No remarketing / Customer Match / health-interest audiences attached (verify at post time).

Also before Post: Final URLs `waterwellclinic.co.nz/nz` and `/au` must return 200 (see plan §8 — pages aren't on the live domain yet).
