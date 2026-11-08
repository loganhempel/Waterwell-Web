"""Fills the concept templates: shared SVG sprite, shared partials (phase 2 pages) and the v4
analytics block (verbatim from /index.html, plus ONE added host guard: the GA4/Ads loader only
runs on waterwellclinic.com / www.waterwellclinic.com, so preview visits never reach the real
property. Constants and the success-branch conversion call in spec.js are untouched)."""
import re, os, sys
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C = os.path.join(R, '_work/concept2')
sprite = open(os.path.join(C, 'sprite.svg')).read().strip()
v4 = open(os.path.join(R, 'index.html')).read()
analytics = re.search(r'<script>\n  // GA4 \+ Google Ads.*?</script>', v4, re.S).group(0)
old = "  if (/^G-[A-Z0-9]{6,}$/.test(GA4_ID)) {"
assert analytics.count(old) == 1, 'v4 analytics block changed shape'
analytics = analytics.replace(old,
    "  // Concept guard: the tag loads ONLY on the production hosts, so preview\n"
    "  // visits (vercel.app, localhost) never count in the real GA4/Ads property.\n"
    "  const PROD_HOST = ['waterwellclinic.com', 'www.waterwellclinic.com'].indexOf(location.hostname) !== -1;\n"
    "  if (PROD_HOST && /^G-[A-Z0-9]{6,}$/.test(GA4_ID)) {")
parts = {k: open(os.path.join(C, 'partials', k.lower() + '.html')).read().strip() for k in ('HEAD', 'NAV', 'CONNECT', 'FOOT')}
PAGES = [('index.tpl.html', 'concept-spec/index.html'),
         ('discovery.tpl.html', 'concept-spec/book/discovery.html'),
         ('consultation.tpl.html', 'concept-spec/book/consultation.html'),
         ('about.tpl.html', 'concept-spec/about.html'),
         ('treatment.tpl.html', 'concept-spec/treatment.html'),
         ('podcast.tpl.html', 'concept-spec/podcast.html')]
for tpl, out in PAGES:
    p = os.path.join(C, tpl)
    if not os.path.exists(p): continue
    s = open(p).read().replace('{{SPRITE}}', sprite).replace('{{ANALYTICS}}', analytics)
    for k, v in parts.items(): s = s.replace('{{%s}}' % k, v)
    assert '{{' not in s, f'unfilled placeholder in {tpl}'
    os.makedirs(os.path.dirname(os.path.join(R, out)), exist_ok=True)
    open(os.path.join(R, out), 'w').write(s); print('wrote', out)
