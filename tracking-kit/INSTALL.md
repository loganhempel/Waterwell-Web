# Waterwell — Conversion Tracking Install Kit
Emporom Media · 2026-07-12 · Site: waterwellclinic.co.nz (WordPress + Gravity Forms) · Ads account: Waterwell Clinic 1256973392 (NZD)

**Broken/missing:** $470 / 1,282 clicks / 0 recorded conversions — Gravity Forms (2,204 Contact + 628 Questionnaire entries) has never fired any event; no conversion action exists in the Ads account.
**Fix:** Gravity Forms confirmation → GA4 `generate_lead` key event → import into Google Ads as the Primary conversion. Cal.com booking event added once the booking block goes in.
**Access needed:** WordPress admin from Kohei (chase sent 12 Jul). Everything below is pre-built — install is ~30 min once the login lands.

Rule from the house SOP: one tracking method per event. Pick Path A **or** Path B per form — never both, or you double-count.

---

## Step 0 — GA4 setup check (do first, 5 min)

The live WP site's tag state is unknown from here. When you're in:

1. View source on the homepage. Look for a `G-XXXXXXXXXX` gtag, a GTM container (`gtm.js`), or a plugin (Site Kit / MonsterInsights) in WP admin → Plugins.
2. **VERIFY-IN-ACCOUNT:** does a GA4 property exist for waterwellclinic.co.nz? Check analytics.google.com under Kohei's / our access.
3. Outcomes:
   - **GA4 installed sitewide** → skip to Step 1. Note whether events go through `gtag()` directly or a plugin's dataLayer — the snippets assume `gtag()` is global. If only a plugin is present, test `typeof gtag` in the console; if undefined, add `snippets/ga4-base.html` anyway (one property, one stream — don't create a second property).
   - **No GA4 at all** → create a GA4 property (NZ timezone, NZD), get the `G-` ID, install `snippets/ga4-base.html` site-wide via WPCode (Code Snippets → Header) or the theme's header hook. Replace `G-XXXXXXXXXX` in the snippet first.
4. Confirm `page_view` shows in GA4 DebugView before wiring form events. No page_view = nothing downstream will work.

## Step 1 — Gravity Forms → GA4 `generate_lead`

Two forms matter: **Contact Form** and **Health Questionnaire**. Get their form IDs from WP admin → Forms (the ID column). **VERIFY:** IDs are unknown until we're in — the snippets carry placeholders.

### Path A (preferred) — confirmation redirect to a thank-you page

1. WP admin → Pages → Add New → create `/thank-you/` — one line of copy ("Thanks — Kohei will reply within one business day") + the booking CTA if it's live. Publish. Set noindex if an SEO plugin is present.
2. Forms → (Contact Form) → Settings → **Confirmations** → edit the default confirmation → change type from **Text** to **Redirect** → URL `https://waterwellclinic.co.nz/thank-you/` → Save. Repeat for the Health Questionnaire (same page is fine; add `?form=questionnaire` if you want to split them in GA4 later).
3. Add `snippets/thank-you-ga4.html` to the `/thank-you/` page only — Custom HTML block at the bottom of the page (or a WPCode snippet with a page condition). This fires `generate_lead` on load.
4. Caveat: anyone who bookmarks/refreshes `/thank-you/` fires the event again. Acceptable at this volume; the import to Ads is click-gated anyway.

### Path B (fallback) — `gform_confirmation_loaded` JS listener

Use this if Kohei wants to keep the inline "thanks" message instead of a redirect, or if a plugin fights the redirect.

1. Requirement: the forms must be embedded with **AJAX on** (`[gravityform id="X" ajax="true"]` or the block's AJAX toggle) — `gform_confirmation_loaded` only fires on AJAX confirmations. Check the embed on the page; flip AJAX on if it isn't.
2. Install `snippets/ga4-gform-listener.html` site-wide (WPCode → Footer). Update the form-ID map at the top of the snippet with the real IDs from Step 1.
3. Do **not** also set a redirect confirmation on the same form — one method per form.

## Step 2 — Mark the key event + link the accounts

1. GA4 → Admin → Events: confirm `generate_lead` appears after a test submit (DebugView first, Events list within ~24h).
2. GA4 → Admin → Key events → mark `generate_lead` as a **Key event**.
3. GA4 → Admin → Product links → Google Ads → confirm/create the link to **1256973392**. **VERIFY-IN-ACCOUNT:** no link is confirmed to exist today.

## Step 3 — Import into Google Ads

1. Google Ads (1256973392) → Goals → Conversions → **New conversion action → Import → Google Analytics 4 → Web** → select `generate_lead`.
2. Settings: **Primary**, category Submit lead form, count **One**, default click-through window. This becomes the only Primary conversion at launch.
3. Status will read "No recent conversions" until the first post-import fire — that's normal. What matters is the test in TEST.md.

## Step 4 — Cal.com booking event (when the booking block ships)

The booking section (`wordpress-booking-snippet/booking-cta.html`) has an inline Cal.com embed + a button link. Once it's installed (and the `[CONFIRM CAL.COM URL]` placeholders are replaced):

1. Add `snippets/cal-booking-listener.html` to the same page (same Custom HTML block is fine, below the embed). It listens for Cal's `bookingSuccessful` event and fires GA4 `book_discovery_call`.
2. Coverage note: the listener only catches bookings made in the **inline embed**. Bookings via the button (opens cal.com in a new tab) can't fire on-site — track those via a Cal.com → GA4 webhook later if the button turns out to be the main path, or just accept the undercount.
3. Once bookings flow: mark `book_discovery_call` a Key event and import to Ads as a second **Primary** (it's the real business goal). `generate_lead` stays Primary too — they're different actions, not duplicates.

## Order of operations

Step 0 → 1 → test submit → 2 → 3 → end-to-end test (TEST.md) → only then is the Ads relaunch gate #1 clear. Step 4 whenever the booking block lands — don't hold the form tracking for it.
