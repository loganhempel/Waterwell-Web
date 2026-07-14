# au.html — AU Landing-Page Remediation

**Date:** 12 July 2026 · **By:** Emporom Media
**Governing doc:** `AUS-compliance-note-2026-07-11.md` (§5 checklist, §6 sign-offs)
**Evidence:** `au-audit-desktop-2026-07-12.png` + `au-audit-mobile-2026-07-12.png` (full-page renders, this folder). Verified in headless Chromium at 1440px and 390px — no layout breakage, no horizontal overflow at either width. Page not deployed; no commits made.

---

## §5 checklist — item by item

**1. Zero product/supplement/herb/brand names (body, alt text, meta, FAQ, footer, JSON-LD)** — **FIXED**
- Removed the "Herbal medicine", "Nutritional supplements (prescription-only, practitioner-grade)" and "Functional tests" (DUTCH, heavy metals, etc.) service cards. Services section rebuilt as consultation-only framing: Free discovery call / Initial consultation / Personalised care plan / Follow-up & review / Dietary & lifestyle advice.
- Removed goods from MedicalClinic JSON-LD (`availableService` now consultation + dietary/lifestyle only; "medical herbalism" cut from description; `medicalSpecialty: Dermatology` also cut — he is not a dermatologist).
- "herbal medicine" stripped from stepping-stone 3, the dermatologist FAQ (visible + JSON-LD), and the footer tagline.
- "a range of functional tests" cut from Step 01; "natural remedies" cut from Step 03; "natural antimicrobial support" cut from the skin-infections card.
- "Medical Herbalist" and "Live Blood Analyst" titles removed from all AU-facing credential blocks (title/jobTitle/signoff/footer) — herbalist framing drags goods association (same reason the split plan dropped the AU herbalist keywords), and live blood analysis is a speculative-diagnostic red flag for Google. These are real credentials — see NEEDS-KOHEI below if he wants the herbalist title reinstated on AU.
- Mechanical grep for herb/supplement/dispens/remed/detox/etc: zero hits remaining.

**2. Zero testimonials / clinical-outcome content** — **PASS (was already testimonial-free) + FIXED residuals**
- Page carried no testimonial section (placeholder comment only). Removed the outcome-adjacent residuals: "Hundreds of eczema patients treated" trust stat (→ "BNatMed · BSc — Qualified NZ naturopath"), "great success rate" (children FAQ), "no difference in effectiveness" (online FAQ), hero rotator line "from a naturopath who has been exactly where you are".

**3. No serious-condition claims** — **PASS after edits**
- No cancer/mental-illness/STI/hep-C/diabetes/depression/arthritis references anywhere. "mental-emotional health" in stone 2 replaced with "sleep, stress". Treat/cure/heal verbs softened page-wide to the AU RSA framing (support / discuss / address / approach) — e.g. "Treating the underlying cause" → "Addressing the underlying cause", "How does a naturopath treat eczema…" → "How is a naturopath's approach to eczema different…". "Topical Steroid Withdrawal" stays — it is the condition name and matches the AU ad groups.

**4. No detox/cleanse/toxins language** — **FIXED**
- "detox pathways" cut from Step 03 (list now: gut function, hormones, microbiome, stress response, skin integrity — via dietary and lifestyle care). No other detox/cleanse/toxin instances existed.

**5. No before/after stories, imagery, or "results in X weeks" framing** — **FIXED**
- Entire Results section deleted: drag-compare acne slider, 3 before/after cards (hand/infant/baby eczema), captions, disclaimer, plus the compare-slider and hover-reveal JS. Nav/drawer/footer "Results" links removed; grid closes cleanly (verified in renders).
- Kohei's recovery story rewritten: "bed-ridden for five months", "steroids and antibiotics", "99.9% eczema-free" transformation arc all removed. Section is now "About Kohei" — lived experience with severe eczema (fact, no outcome claim), training, decade in practice, NZ-based clinic. Microscope-image alt text de-clinicalised.
- "How long until I see results?" FAQ → "How long does the process take?" — "changes within weeks" and "Estimated Progress Timeline" cut, explicit "no outcome can be promised" added. Journey headline "from flare-ups to healthy skin" and "skin that looks after itself" also removed. Stones heading "towards your desired results" → "at your pace".

**6. Credentials state NZ explicitly, no implied AU registration** — **FIXED (wording: see NEEDS-KOHEI)**
- "Qualified NZ naturopath" now used in hero sub, trust bar, intro, signoff, footer, meta description. No AU/Ahpra implication anywhere. "Reg. MNMHNZ" badge retained (NZ professional body, named as on his existing material).
- Note: the §5 checklist's literal phrase is "NZ-registered naturopath"; the AU RSAs use "Qualified NZ Naturopath". I used the RSA wording (naturopathy has no statutory register in NZ either, so "registered" could overstate). Kohei/Logan to confirm final phrasing — see below.

**7. Clear disclosure: delivered online from New Zealand** — **FIXED**
- Added in: hero eyebrow ("Delivered From NZ"), hero sub, trust bar, intro, virtual-care pill ("100% online · from New Zealand"), nav email label ("Online from NZ"), booking panel ("Online from New Zealand · Australia-wide"), FAQ answers, footer tagline + badge, foot-bottom disclosure ("Waterwell Clinic is based in New Zealand; all consultations are delivered online from New Zealand by an NZ-qualified naturopath"), and JSON-LD. The footer's fabricated "in Sydney, Australia" is gone.

**8. "Complements, does not replace, medical care — see your GP" line** — **FIXED**
- In the foot-bottom disclosure verbatim-equivalent, plus woven into the dermatologist FAQ ("naturopathy complements that care, it does not replace it… For diagnosis, always see your GP or specialist") and the medication FAQ (no more "wean off medications" — decisions "stay between you and your doctor").

**9. Pricing in AUD or clearly flagged NZD** — **FIXED (minimally) / NEEDS-KOHEI**
- Page showed no pricing at all. Added a Fees row to the booking panel: "Billed in NZD — confirmed on your free call". That satisfies the currency-flag requirement without inventing numbers. The split plan (§3) leaves AUD-display vs NZD-flag as a Kohei/Logan decision — if he wants actual fees on the page, that's his call and his numbers.

**10. Every efficacy claim substantiable or cut** — **FIXED**
- Remaining claims match the split plan's substantiable set: BNatMed/BSc, 10+ years' practice, free 15-min discovery call, 75-min initial consult, secure-video delivery, personalised plans, Reg. MNMHNZ. Everything else (hundreds treated, success rate, results timeframes, effectiveness parity, 99.9%) was cut rather than substantiated.

**11. Privacy policy covers AU visitors** — **NEEDS-KOHEI** (note flags this as low-urgency)
- No privacy policy exists on the page and the enquiry form collects name/email (mailto-composed, no server capture). A privacy page + footer link is needed before scale; needs Kohei's business details. Not invented.

**12. No prescription drug names** — **PASS**
- None present. Generic "medication"/"prescribed" appears only in the complementary-care FAQ (no drug names, no anti-medicine positioning — "wean off" line removed). "Steroid" appears only inside the condition name Topical Steroid Withdrawal and its card description, consistent with the AU ad groups.

**13. Conversion tracking present and firing** — **NEEDS-KOHEI / NEEDS-BUILD (still failing)**
- No GA4/Ads tag exists on the page and none was fabricated. This was already a known open gate (tracking unbuilt across Waterwell). Must be built and verified on the AU booking flow before spend — separate task.

---

## Also flagged (outside au.html, do not unpause without resolving)

- **/conditions/* links** — the six condition cards link to `/conditions/eczema` etc. Those pages become part of the AU click-path and have NOT been audited against this note. Either audit them or make the AU cards non-linking before launch.
- **Cal.com URL** — the embed still carries `[CONFIRM CAL.COM URL]` placeholders and 404s (`waterwell/discovery`). Pre-existing; needs Kohei's real booking link.
- **§6 sign-offs untouched and still required:** Kohei's written no-Ahpra confirmation, his substantiation confirmation, his sign-off on the note itself, and the Google telemedicine-certification question. None of these are page fixes.
- **Herbalist title (NEEDS-KOHEI):** "Medical Herbalist" is a genuine credential but was removed from AU assets for TGA goods-association reasons. If Kohei wants it shown to AU visitors, that's a deliberate risk decision for him + Logan against §1 of the note.

## Verdict

au.html now passes §5 items 1–8, 10 and 12. Item 9 passes on the minimal NZD-flag basis pending Kohei's pricing decision. Items 11 (privacy) and 13 (conversion tracking) remain open — 13 is a hard launch gate. AU campaigns stay paused until 13 + the §6 sign-offs are green.
