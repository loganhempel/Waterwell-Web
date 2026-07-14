# Waterwell booking CTA — WordPress install

Adds the "Book a free discovery call" section (Cal.com embed) to the live WordPress site. Takes about 5 minutes. Do this once Kohei grants WP editor access.

**Before you start:** replace `waterwell/discovery` with Kohei's real Cal.com link in `booking-cta.html`. It appears **twice** — the button `href` and the `calLink` in the script. Search the file for `[CONFIRM CAL.COM URL]` to find both spots. Do not paste the snippet live with the placeholder in — visitors get a Cal 404.

## Step 1 — Copy the snippet

Open `booking-cta.html` (this folder) and copy the entire file contents.

## Step 2 — Add a Custom HTML block

In WP admin: **Pages → edit the target page** (homepage, or wherever the booking section should sit). In the block editor, click **+ → search "Custom HTML"** → add the block where you want the section (recommended: after the services/story section, before the final CTA/footer). Paste the whole snippet into the block.

If the site uses Elementor instead of the block editor: drag in an **HTML widget** and paste there — same result.

## Step 3 — Preview, then publish

Click **Preview** first. Check:

- Navy card with white "Book your free call" button renders on the left
- Cal.com calendar loads on the right (real availability, no error message)
- On a phone (or narrow browser window) the card stacks to one column
- Clicking the button opens the Cal.com booking page in a new tab

All good → **Update/Publish**.

## Notes

- The snippet is fully self-contained (scoped `wwcal-` CSS, no theme dependencies). Only external load is `app.cal.com/embed/embed.js`.
- If the calendar area shows "Error Code: 404", the Cal.com link is wrong — recheck both `[CONFIRM CAL.COM URL]` spots.
- If a security/optimisation plugin strips `<script>` tags from Custom HTML blocks, the inline calendar won't load but the button still works (it's a plain link). Whitelist the page in the plugin or ask me.
- Fonts: headings fall back to Georgia if Instrument Serif isn't loaded on the WP theme. If Kohei wants the exact preview-site heading font, add Instrument Serif via the theme's font settings — not required.
