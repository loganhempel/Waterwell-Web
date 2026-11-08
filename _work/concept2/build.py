"""Fills the concept templates: shared SVG sprite + the v4 analytics block (verbatim from /index.html)."""
import re, os, sys
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sprite = open(os.path.join(R, '_work/concept2/sprite.svg')).read().strip()
v4 = open(os.path.join(R, 'index.html')).read()
analytics = re.search(r'<script>\n  // GA4 \+ Google Ads.*?</script>', v4, re.S).group(0)
for tpl, out in [('index.tpl.html', 'concept-spec/index.html'), ('discovery.tpl.html', 'concept-spec/book/discovery.html'), ('consultation.tpl.html', 'concept-spec/book/consultation.html')]:
    p = os.path.join(R, '_work/concept2', tpl)
    if not os.path.exists(p): continue
    s = open(p).read().replace('{{SPRITE}}', sprite).replace('{{ANALYTICS}}', analytics)
    os.makedirs(os.path.dirname(os.path.join(R, out)), exist_ok=True)
    open(os.path.join(R, out), 'w').write(s); print('wrote', out)
