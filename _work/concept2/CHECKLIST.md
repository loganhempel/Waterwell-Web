# Concept 2, phase 1 checklist (8 Nov 2026)
Scope: concept-spec/index.html, concept-spec/book/{discovery,consultation}.html, concept-spec/assets/spec.{css,js}. Phase-2 pages = About, Treatment, Podcast.

## Brief gap list
- [done] Shared CSS/JS extracted to /concept-spec/assets/spec.css + spec.js (absolute paths everywhere)
- [done] Nav "Free discovery call" button (short "Free call" under 640px) -> /concept-spec/book/discovery
- [done] Hero: quiz primary (data-quiz -> QUIZ_URL) + text link "Or book a free 15-min chat with me"
- [done] Book CTAs -> /concept-spec/book/discovery (no CTA points at the paid lander from the homepage; consult page links down to discovery)
- [done] Articles -> the 3 real /blog posts; "Read more" -> /blog
- [done] Privacy -> /privacy, Code -> /code-of-conduct
- [done] Connect: Podcast -> https://linktr.ee/waterwellclinic
- [done] "Get to know Kohei" -> /concept-spec/about, "Find out more" -> /concept-spec/treatment, "Listen to Episodes!" -> /concept-spec/podcast (404 until phase 2 builds them)
- [done] Form wired like v4: same Web3Forms key, payload, honeypot bf_xq7, time zone, city optional, Hives option, mailto fallback, AW conversion in the success branch only, same copy. Handler copied byte-for-byte from assets/v4/site.js (diffed identical)
- [done] Landers in Spec style: v4 copy, first-person steps above the form, 3 fields, credential line, consult downshift, "Back to the main website" -> /concept-spec
- [done] Concept badge kept; noindex on all 3 pages
- [done] Held items held: no "Medical Herbalist", no herbal-medicine sentence (step 03 uses the v4 rewrite), Kohei's skin photos removed from the page AND from concept-spec/img
- [done] Compliance: 3/3 pass via _work/concept2/compliance_concept.py (the v4 tool, unchanged rules; only the allow-list scope maps concept-spec/<page> to <page>). Raw tool: landers pass; homepage fails only on the 2 released location lines (Sydney bullet, AU/NZ FAQ) because LOCATION_CLEARED is keyed on bare v4 paths. tools/ not edited (non-concept file)
- [done] Trim kept: fixes applied without re-adding the cut sentences (eczema para 2, journey "prescription"/"ignited" lines, long FAQ answers)

## Copy audit (_work/audit2/copy/FINDINGS.md)
- [done] C1 hero link text + target
- [skip] A1 /about closing band (phase 2)
- [done] T1 Sydney telehealth bullet. [skip] /about location lines (phase 2)
- [done] F1 medication FAQ (GP line kept after)
- [done] C3 Clear Path close + button, step 03, step 04; "Find out more" kept
- [done] T2 telehealth heading. [skip] /treatment buttons (phase 2)
- [done] L1 landers: steps above form, step copy, success copy, discovery sub, credential line, consult downshift
- [done] F2 dermatologist + international FAQ
- [done] 11 hero lead + both ticks
- [done] 12 "dedicated to supporting". [skip] /about lines (phase 2)
- [done] 13 reviews headline, Kohei's own photo (stock face removed), g.page link without /review, text link
- [done] 14 "my skin slowly settled" + rosacea
- [done] 15 form: city optional, Hives split, lead copy, reply line; validation "so I know" (v4 handler)
- [done] 16 children FAQ
- [skip] 17 "My goal at Waterwell Clinic" paragraph: not in the concept (nothing to cut)
- [done] 18 homepage podcast blurb. [skip] /podcast quiz band + episode 01 (phase 2)
- [done] 19 "1,000+" everywhere; 4-numeral strip per D5 (IICT in the credential line)
- [done] 21 AU spelling (personalised, agonising, wellbeing); grep finds no -ize forms in visible text
- [done] 22 Clear Path intro "Here's"; [skip] blog CTA (blog pages are not concept files)
- [skip] NOT NOW items (fees, ScoreApp copy, herbal ruling, hero scale-up): need Kohei

## Design audit (_work/audit2/design/FINDINGS.md), translated into the Spec system
- [done] D1 nav discovery button + hero free-chat link
- [done] D2 homepage has no dead ends + sticky mobile bar. [skip] closing bands on About/Treatment/Podcast (phase 2; reuse .bw-close + data-mcta-hide)
- [done] D3 hero: tick copy trimmed, GP/credential line lives in the strip. Cut-out kept at its current scale (original photo needed to go bigger)
- [done] D4 mobile CTA on screen one (quiz button top 412px of 844); lander first field 517px; jump button gone
- [done] D5 4 numerals (10+ / 1,000+ / 125k+ / 2) + one credential line, 2x2 on mobile. Kept the Spec white strip, not navy
- [done] D6 secondary actions are text links (Read more, See Reviews, Listen, Get to know Kohei, Find out more); solid buttons = quiz or book only
- [done] D7 lander form in the first screen with credential line
- [done] D8 left-aligned text over photos, measured on the ground (_work/concept2/contrast.py): band h2 4.42:1 / lead 6.78:1, want h2 7.48:1 / body 5.86:1+, split caption 7.04:1+. Washes are 60-84% where the text sits, above the 55% cap, because the cap failed contrast (2.0-2.5:1)
- [done] D9 flat navy / water-tint / paper tiles, no images
- [done] D10 reviews link without /review, text link
- [skip] D11, D12, D19 (treatment/about, phase 2)
- [done] D13 podcast band on a light ground, so no long run of dark
- [done] D14 one accordion type size (22px, same +/x control) for conditions and FAQ; exclusive groups via name=
- [done] D15 Areas of Focus already sits with its panel (no lone heading band)
- [done] D16 no hyphen breaks: .nw on flare-ups, 3-Min, 15-min, 15-minute, 75-minute, Gut-Skin
- [done] D17 duplicate eyebrows removed (About, My story, Contact, Online consultations, Real Client Stories); kept Kohei's own labels (Areas of Focus, A Clear Path, Reading Room)
- [skip] D18 podcast platform marks (phase 2 /podcast; homepage has none)
- [done] Motion: hero H1/sub/cut-out not faded; tile hover only on hover-capable devices; reduced motion respected

## Verification
- [done] Render rounds at 1440 + 390 against Spec v5 (shots/spec-v5-*, r1*, r1b*, r2*)
- [done] No console errors, no horizontal overflow at 320-1440, every internal href 200 except the 3 phase-2 pages
- [done] Form test, Web3Forms stubbed (formtest.py): 3 forms post the v4 payload; success copy + generate_lead + conversion on 200; error copy, no conversion on 500
- [done] Local servers killed

# Phase 2 (8 Nov 2026): About, Treatment, Podcast
- [done] /concept-spec/about, /treatment, /podcast built from _work/concept2/*.tpl.html via build.py (new shared partials: partials/head, nav, connect, foot). Copy = current v4 pages verbatim, same holds (no "Medical Herbalist", no skin photos, no "not curable" line)
- [done] Kohei's structure: About = title in the photo, credibility strip, story, "Waterwell Clinic is" over the image, Outside the Clinic, Connect. Treatment = A Clear Path 5 steps (.bw-list), Tools Behind Your Care, Telehealth (.tele-band glass card), closing CTA. Podcast = big banner, 4 platforms in ONE line with brand marks (no pills), episodes, quiz band, Connect
- [done] Every page: closing .bw-close band with data-mcta-hide, #mcta sticky quiz bar, nav "Free discovery call", Concept badge, noindex, nav logo -> /concept-spec. All book CTAs -> /concept-spec/book/*
- [done] New CSS appended to spec.css only for patterns phase 1 lacked (.band-hero, .intro, .prose-2, .pbreak, .split-night, .want-solo, .trio, .close-sec, .tools, .pod-hero, .plats, .eps)
- [done] Analytics guard in build.py: loader runs only on waterwellclinic.com / www.waterwellclinic.com; constants + success-branch conversion untouched. p2/analytics_test.py: 127.0.0.1 = 0 gtag requests, no window.gtag, no conversion; simulated prod (both hosts, requests intercepted and served from the local build) = tag loads, form submit fires the AW conversion. 18/18 pass. NOTE: formtest.py's conversion=True now only holds on the prod hosts
- [HELD] Podcast episode 06 title "The Healing Power of Movement: …" fails the "heal" rule (v4 /podcast fails on the same line). Listed as "Kimberley James", original title in a HELD comment, link unchanged. Needs Logan/Kohei ruling
- [done] Compliance 6/6 (compliance_concept.py). Contrast on photo text 6.6-13.5:1 (p2/contrast_p2.py)
- [done] p2/check.py: 40 unique hrefs, all 200 (facebook.com returns 400 to scripts, 200 in Chromium), no dangling anchors, no console errors, no overflow at 320/390/1440, reveal rows turn on, sticky bar shows mid-page and steps aside on the closing band
- [done] Render rounds r1, r2/r2b, r3 at 1440 + 390 (p2/shots). Fixes between rounds: podcast cover never crops (contain on the shot's wall colour), "Waterwell Clinic is" column kept off Kohei, mobile hero focal points
