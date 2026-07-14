# Waterwell — Tracking Verification (end-to-end)

Run the same session as the install. Ads-side confirmation lags 24–72h — the tag firing is confirmable immediately, the import is not. Don't re-flag as broken early.

## Same-session (immediate)

1. **GA4 base:** open waterwellclinic.co.nz with Tag Assistant (tagassistant.google.com) connected, or GA4 → Admin → DebugView with the GA Debugger extension on. Confirm `page_view` fires.
2. **Form — Contact:** submit a real test enquiry (name it "TEST — Logan", tell Kohei to ignore).
   - Path A: confirm you land on `/thank-you/` and `generate_lead` appears in DebugView with `method: gravity_forms_redirect`.
   - Path B: confirm the inline confirmation shows and `generate_lead` appears with the right `form_id`.
   - Either path: confirm the entry still lands in WP admin → Forms → Entries AND the notification email still reaches Kohei. Tracking must never break delivery.
3. **Form — Health Questionnaire:** repeat the test submit. Confirm the event carries the questionnaire form name/param, not the contact one.
4. **Double-fire check:** in DebugView, one submit = exactly one `generate_lead`. Two = you have both Path A and Path B live on that form — remove one.
5. **Cal.com (if installed):** make a test booking in the inline embed. Confirm `book_discovery_call` in DebugView, then cancel the booking in Cal so Kohei's calendar stays clean.

## 24–72h later (platform confirmation)

1. GA4 → Reports → Engagement → Events: `generate_lead` count ≥ your test submits.
2. GA4 → Admin → Key events: `generate_lead` listed and counting.
3. Google Ads 1256973392 → Goals → Conversions: the imported `generate_lead` action shows status **Recording** (test submits from organic/direct sessions may not attribute to Ads — the status flip is the signal, not the count).
4. Cross-check: conversions in Ads should reconcile roughly with Gravity Forms entry count for the same window once spend resumes. Entries ≫ conversions is normal (organic leads); conversions > entries means double-firing.

## Import confirmation before relaunch

- [ ] `generate_lead` = **Primary**, count **One**, "Include in Conversions" = Yes
- [ ] It is the ONLY Primary action (no page-view junk actions set Primary)
- [ ] GA4 ↔ Ads link active (GA4 Admin → Product links)
- [ ] Bid strategy stays **Max Clicks + CPC cap** until ~15–20 recorded conversions (per relaunch package §3) — do not hand Smart Bidding an empty conversion history

Only when every box above is ticked does relaunch gate #1 (SOURCE-OF-TRUTH) clear. Then build the AUS/NZ split and launch.
