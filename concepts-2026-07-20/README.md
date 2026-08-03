# Four landing-page concepts — 20 July 2026

Recovered 3 August 2026. These are **concept explorations, not production pages.**

## What they are

Four from-scratch landing page directions for Waterwell, built 20 Jul. Each is a
genuinely different design language with its own DOM and CSS — not four skins on
one layout. The only fixed points are the brand colours: navy `#0E3A64` and
cream `#F4EEE4`.

| File | Concept | Design language |
|---|---|---|
| `waterwell-concept-current.html` | **Deep Current** | Bold geometric sans. Live canvas water-ripple background (cursor-reactive), asymmetric hover-expanding specialties list, vertical connected-dot process path, marquee strip. |
| `waterwell-concept-dossier.html` | **The Dossier** | Editorial/magazine. Serif masthead, drop-cap belief section, dotted-leader contents, rotated case-file clippings, scroll-linked progress rule, paper grain. |
| `waterwell-concept-vitals.html` | **Vitals** | Clinical/brutalist lab. Monospace throughout, hard-bordered specimen grid, scrolling data ticker, scroll-triggered typewriter belief statement, terminal-style CTA. |
| `waterwell-concept-bloom.html` | **Root & Bloom** | Organic/botanical. Slow-drifting blob shapes, staggered leaf-shaped condition cards, winding node path, hand-drawn SVG underline. |

All four include the 20 Jul polish pass — nav legibility fix on Deep Current,
mobile masthead stacking on The Dossier, the four-corner crosshair frame on
Vitals, the pulse-line TSW icon on Root & Bloom, plus `prefers-reduced-motion`
handling and focus-visible states throughout.

## How they were recovered

They were built in a Claude Code session scratchpad and never copied into the
repo. The scratchpad (`/private/tmp/claude-501/.../93f8eb6b-.../scratchpad/`) is
gone, and a full-disk search on 29 Jul found nothing — the vault recorded them as
permanently lost.

They were reconstructed from the session transcript
(`~/.claude/projects/-Users-loganhempel/93f8eb6b-….jsonl`, 14 MB), which retains
every `Write` and `Edit` tool call. Replaying the original Write plus each
subsequent Edit in order rebuilt the final polished state of all four: **19 edits
replayed, 0 failures.** Verified in headless Chromium — all four render with no
JS errors and no missing assets.

**The general lesson:** work lost to a scratchpad is often still recoverable from
the session transcript, provided the session ID is known. A session handoff doc
records that ID, which is what made this possible.

## ⚠ Before any of these goes anywhere near production

1. **No AU compliance treatment.** These were built as NZ/world concepts against
   the July compliance note. All four reference *medical herbalism* in hero or
   body copy, which is a therapeutic-goods reference banned in AU assets under
   `AUS-compliance-note-2026-08-03.md`. They would need the `<!--AU:cut-->`
   marker treatment that `tools/build_geo.py` applies to the production site.
2. **Kohei has since relocated to Australia** (confirmed 3 Aug). Any concept
   taken forward must not carry NZ-location or NZ-registration claims.
3. **Static and disconnected.** No booking wire-up, no form handler, no
   conversion tracking. The production site's booking form was rebuilt on 3 Aug
   to POST server-side and fire `generate_lead`; none of that exists here.
4. Kohei has never seen these, and Logan has not picked a direction.

## Viewing

    cd "/Users/loganhempel/Client Work/Waterwell"
    python3 -m http.server 8899
    # then open http://localhost:8899/concepts-2026-07-20/waterwell-concept-current.html

Source handoff: `.claude/handoffs/2026-07-20-211811-kohei-session-prep-and-4-concept-redesigns.md`
