# Waterwell — AU + NZ Google Ads Split Plan

Prepared by Emporom Media · 12 July 2026 · Account: Waterwell Clinic (ID 1256973392, currency NZD)
Supersedes the campaign structures in `relaunch-2026-06/` and `gads-build-2026-07-05/` (both pre-date the Australia move; the 07-05 build is Wellington-local and is dead on arrival for a virtual-first clinic).

**Governing document for everything AU: `AUS-compliance-note-2026-07-11.md`. Where anything in this plan or the CSVs conflicts with that note, the note wins.**

---

## 1. Campaign architecture

Five campaigns, split hard by market. NZ campaigns land on `nz.html`, AU campaigns on `au.html` — never cross the streams, because the AU page (once remediated, see §7) is the compliance-safe asset and the NZ page carries reviews/results content that must not sit behind an AU ad click.

| Campaign | Ad groups | Landing page | Budget (NZD/day) |
|---|---|---|---|
| WW \| NZ \| Brand | Brand — Waterwell | nz.html | $2 |
| WW \| NZ \| Online Naturopath | Online Naturopath Consult · General Naturopathy | nz.html | $8 |
| WW \| NZ \| Skin Conditions | Eczema · Topical Steroid Withdrawal · Other Skin Conditions | nz.html | $10 |
| WW \| AU \| Online Naturopath | Online Naturopath Consult AU | au.html | $3 |
| WW \| AU \| Skin Conditions | Eczema AU · TSW AU · Skin Support AU | au.html | $4 |

Settings (set manually in the UI after import — Editor CSVs don't carry them):
- **Networks:** Google Search only. Display OFF, Search Partners OFF (the old audit showed Display/Partners ate 72% of impressions on junk).
- **Locations:** NZ campaigns = all of New Zealand, **Presence only**. AU campaigns = all of Australia, **Presence only**. Never "Presence or interest".
- **Bidding:** Maximise Clicks with a max-CPC cap (~$3.50 NZD; brand ~$1.50). Zero valid conversion history in the account, so Smart Bidding has nothing to model on. Switch to Max Conversions per market after ~15–20 tracked conversions in that market.
- **Audiences:** none. No remarketing lists, no Customer Match, no health-interest audiences on ANY campaign. Google's personalised-ads health policy bans them for condition-related ads, and the compliance note gates AU unpause on it. Search intent only, observation audiences off.
- **All campaigns import as Paused.** Nothing goes live until every gate in `LAUNCH-GATES.md` is green.

Why a brand campaign now: June was the best month on record (10 enquiries) and the June report is circulating — brand searches exist and they're the cheapest conversions in the account. $2/day caps it.

## 2. Budget split and reasoning

**Recommended: $20/day NZ ($600/mo) + $7/day AU ($210/mo) — roughly 74/26. Total ~$810 NZD/mo. Logan's call on the absolute number.**

Reasoning:
- NZ has everything that converts cold clicks: 32 five-star reviews, the MoneyHub "Best Naturopath in Auckland" badge, a decade of local word-of-mouth, and the enquiry momentum from June. NZ is where a dollar works hardest today.
- AU is a cold market with zero review visibility (the AU page correctly carries no reviews), a compliance-constrained pitch, and an unresolved Google telemedicine-certification question. It gets a probe budget, not a bet.
- AU also launches later than NZ by design — NZ can go live the day tracking is verified; AU has extra gates (§7 + LAUNCH-GATES). Budget sitting on a paused campaign costs nothing.
- **Rebalance rule:** after 30 days with both markets live and ≥15 total conversions, shift budget toward whichever market has the cheaper cost per booked discovery call. Cap AU at 40% of total until it has produced at least 5 enquiries on its own.

## 3. Account settings — facts and decisions

Facts (not opinions):
- Account 1256973392 is **NZD**. Google Ads account currency and timezone are **permanent** — changing either means a brand-new account with zero history.
- Running AU campaigns from an NZD account is fully supported: AU auction CPCs are simply converted and billed in NZD. Reporting is all-NZD.
- Ad schedules and reports run on the **account timezone (NZ)**. AEST is 2 hours behind NZST (3 during NZ daylight saving). At launch both markets run all-hours so this is moot; if dayparting is added later, AU windows must be shifted +2/+3h in account time.

Decision for Logan (recommendation attached):
- **Keep the single NZD account.** Recommended. One login, one billing chain, shared negative discipline, and the NZ history stays attached. A separate AUD account only becomes worth it if Kohei establishes an AU business entity and wants AUD invoicing/GST treatment — revisit then, not now.
- **Pricing display:** au.html must show pricing in AUD or clearly flag NZD (compliance-note §5 checklist item). Currently the page shows no pricing at all — Kohei/Logan to decide which way to satisfy it.

## 4. Keyword strategy per market

**123 keywords total, 100% phrase + exact, zero broad.** NZ 75 (60 phrase / 15 exact) · AU 48 (40 phrase / 8 exact). Exact layered on head terms only, per the 07-05 build's pattern — exact wins the auction where volume lives, phrase catches the tail.

**NZ — carry-over:** all 55 NZ keywords from the June build survive. They already match the virtual-first positioning (the June build was written online-first). Added: 5 brand terms and an exact-match layer on head terms.

**AU — what carried from the 65 and what didn't:**
- **Carried (generic online-intent terms):** online/virtual/telehealth naturopath, video consult variants, book/see a naturopath online, eczema/TSW/skin condition terms. These are market-agnostic.
- **Swapped:** every `nz` / `new zealand` modifier → `australia` equivalents (online naturopath australia, telehealth naturopath australia, skin naturopath australia, etc.).
- **Dropped for compliance: `online herbalist`, `online medical herbalist`.** Herbalist search intent is herbal *products* — serving an ad against it invites a goods-framed ad click and drags the whole ad into TGA Advertising Code scope. NZ keeps both.
- **Dropped for focus:** the General Naturopathy set (gut/fatigue/hormones/stress) stays NZ-only at launch. AU's probe budget goes where Waterwell out-specialises everyone: eczema, TSW, skin. Expand AU into general terms only after skin proves out.
- Kept in AU: searcher-language terms like "eczema natural treatment" — a user's search phrasing is not our claim; our ad copy against those terms uses support/discuss framing only.

**No AU physical presence = no local pack, no "near me" plays.** Everything AU is virtual-consult intent. `near me` is a negative in every campaign.

## 5. Negatives per market (126 rows)

- **Shared set, all non-brand campaigns (19 terms):** free, jobs, salary, course/courses, training, become a naturopath, school, degree, university, what is, definition, reddit, forum, cream, cure, near me, **detox, cleanse** (the last two are new — compliance note bans detox claims, and detox searchers want a product we must never appear beside).
- **Cross-geo hygiene:** NZ campaigns block `australia`; AU campaigns block `nz`, `new zealand`, `auckland`, `wellington`.
- **AU-only funding-intent set:** medicare, bulk billing, rebate, health fund — Kohei can offer none of these; those clicks are guaranteed waste and set a false expectation.
- **Ad-group product/medical blockers:** eczema groups block ointment, steroid cream, prescription, dupixent; TSW groups block "how long does tsw last", pictures; skin groups block dermatologist, medication, prescription.
- **Routing negatives:** the online-consult and general ad groups block eczema/tsw/psoriasis/acne so condition searches always hit the condition ad group with the matched ad.
- **Brand campaign:** jobs, careers only.

## 6. AU ad-copy rules (applied to every AU RSA; the note is the source)

1. **Service ads only, never goods ads.** Zero mentions of herbs, herbal medicine, supplements, tests, products, dispensaries. One goods reference puts the ad inside the TGA Advertising Code with its full compliance burden.
2. **Soft verbs only.** "Support", "discuss", "book a consultation" — mirroring the TGA's own safe example. No "treat", "cure", "heal", "fix", "resolve". (NZ ads keep "Treat The Cause" — NZ rules differ; that copy never serves in AU.)
3. **No testimonials, no review counts.** "32 Five-Star Reviews" is NZ-only. The note permits service-experience testimonials in theory but says safest is none in AU assets — so none.
4. **No before/after or transformation framing.** Kohei's own recovery story ("He Beat Eczema Himself") is out of all AU copy — it functions as an outcome claim.
5. **Honest credentials, NZ-flagged.** "Qualified NZ Naturopath" — never anything implying Australian or Ahpra registration (he holds none; naturopathy isn't Ahpra-registrable).
6. **Delivery disclosed.** "Delivered Online From NZ" appears as a headline in every AU RSA.
7. **Conditions in non-serious form only.** Eczema, TSW, psoriasis, acne, rosacea — named, but only as "support for / discuss your". Zero references ever to cancer, mental illness, STIs, hepatitis; no diabetes/depression/arthritis "treatment" language.
8. **No guarantees, speed claims, "proven", or anti-medicine positioning.** No drug names anywhere.
9. Every substantive claim left in AU copy is substantiable from the site today: qualification (BNatMed, BSc), 10+ years in practice, free 15-min discovery call, secure-video delivery, personalised plans.

These rules were enforced mechanically: the CSV generator lints every AU headline/description against a banned-pattern list (review, five-star, beat, treat, cure, detox, herb, supplement, test, guarantee, proven, heal, medication, prescri-, transform, registered) and the build fails on any hit.

## 7. Compliance conflicts found and how they were resolved

| Conflict | Resolution |
|---|---|
| June AU RSAs used "32 Five-Star Reviews" + review-based descriptions | Removed from all AU copy (note §4: outcome/testimonial risk; "safest is none") |
| June copy leads with Kohei's eczema recovery ("He Beat Eczema Himself") | NZ-only. Removed from AU — before/after transformation implication |
| "Treat The Cause/Root" headlines | NZ-only. AU uses "A Root-Cause Approach" + support/discuss verbs |
| "Lab Tests, Done From Home" / functional-tests descriptions | NZ-only — tests/goods reference pulls AU ads into TGA scope |
| "Works Alongside Your Meds" / medication descriptions | NZ-only — medication references risk Google's AU prescription-term filters |
| `online herbalist`, `online medical herbalist` keywords | Dropped from AU (goods-intent searches); kept in NZ |
| **au.html itself currently FAILS the note's §5 landing-page checklist** | **Flagged as a hard launch gate — not fixable from the ads side.** Failures: before/after results gallery (drag-compare images), the "99.9% eczema-free" recovery story, "Herbal medicine" + "Nutritional supplements (prescription-only, practitioner-grade)" service cards, "detox pathways" line in Step 03, "international dispensaries" FAQ line, footer says "in Sydney, Australia" (implies AU presence that doesn't exist — the reverse of the required "delivered online from NZ" disclosure), and no pricing in AUD/flagged-NZD. The AU campaigns must not unpause until au.html passes the checklist — the landing page is legally part of the ad. |

## 8. Import runbook (Google Ads Editor)

CSVs in `editor/`: `campaigns.csv`, `adgroups.csv`, `keywords.csv`, `negatives.csv`, `rsas.csv`.

1. Download the current account in Editor first.
2. Import order: campaigns → adgroups → keywords → rsas → negatives. Review each proposed-changes screen, **Keep**, don't Post.
3. Set the manual settings from §1 (networks, locations/Presence, bidding, no audiences).
4. Pause/leave-paused every legacy campaign (the old "New Marketing", "Eczema Treatments", and anything from the 06/07-05 structures that got posted). Don't delete — keep history.
5. Add sitelinks/callouts manually (Free Discovery Call · How It Works · Conditions · About Kohei). AU versions must pass the §6 rules — no goods, no outcomes.
6. **Final URL check before Post:** CSVs point at `https://waterwellclinic.co.nz/nz` and `/au` (cleanUrls). These paths must return 200 on the live domain before posting — if the pages ship at different paths or the WordPress migration lands differently, find-and-replace the Final URL column first. ⚠ TODO(verify): as of 12 Jul the live domain is still the old WordPress site; nz.html/au.html exist only in the repo/Vercel preview.
7. **Post nothing until `LAUNCH-GATES.md` is fully green.** NZ can post once the four universal gates clear. AU additionally needs the §7 landing-page remediation + the compliance-note §6 sign-offs (no-Ahpra confirmation from Kohei, telemedicine-certification question resolved, Kohei's written sign-off on the note).
