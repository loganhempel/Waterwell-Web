"""All 6 concept pages: every href (internal via the local cleanUrls server, external live GET),
in-page #anchors exist, console errors, horizontal overflow at 320/390/1440, scroll-reveal rows
turn on, sticky CTA shows mid-page and steps aside on the closing band (390)."""
import asyncio, urllib.request, ssl
from urllib.parse import urljoin, urldefrag
from playwright.async_api import async_playwright
B = 'http://127.0.0.1:8231'
PAGES = ['/concept-spec', '/concept-spec/about', '/concept-spec/treatment', '/concept-spec/podcast', '/concept-spec/book/discovery', '/concept-spec/book/consultation']
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'
def status(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=20, context=ssl.create_default_context())
        return r.status
    except urllib.error.HTTPError as e: return e.code
    except Exception as e: return type(e).__name__
async def main():
    hrefs = {}; problems = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for path in PAGES:
            for w in (320, 390, 1440):
                ctx = await b.new_context(viewport={'width': w, 'height': 844 if w < 500 else 900}, is_mobile=w < 500, has_touch=w < 500)
                pg = await ctx.new_page(); errs = []
                pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
                pg.on('pageerror', lambda e: errs.append(str(e)))
                await pg.route('https://www.googletagmanager.com/**', lambda r: r.fulfill(status=200, body=''))
                await pg.goto(B + path, wait_until='networkidle')
                sw = await pg.evaluate('document.documentElement.scrollWidth')
                if sw > w: problems.append(f'{path} @{w}: overflow scrollWidth={sw}')
                if errs: problems.append(f'{path} @{w}: console {errs}')
                if w == 1440:
                    links = await pg.evaluate("[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))")
                    for h in links: hrefs.setdefault(h, set()).add(path)
                    ids = await pg.evaluate("[...document.querySelectorAll('[id]')].map(e=>e.id)")
                    for h in links:
                        if h.startswith('#') and len(h) > 1 and h[1:] not in ids: problems.append(f'{path}: dangling {h}')
                if w == 390:
                    H = await pg.evaluate('document.documentElement.scrollHeight')
                    for y in range(0, H, 300):
                        await pg.evaluate(f"scrollTo({{top:{y},behavior:'instant'}})"); await pg.wait_for_timeout(80)
                    rows = await pg.evaluate("[...document.querySelectorAll('.bw-row,.j-step')].map(r=>r.classList.contains('in'))")
                    if rows and not all(rows): problems.append(f'{path}: reveal rows not all on {rows}')
                    if await pg.locator('#mcta').count():
                        await pg.evaluate("scrollTo({top:innerHeight*1.6,behavior:'instant'})"); await pg.wait_for_timeout(400)
                        mid = await pg.evaluate("document.getElementById('mcta').classList.contains('show')")
                        hide = await pg.evaluate("(()=>{const e=document.querySelector('[data-mcta-hide]'); if(!e) return null; e.scrollIntoView({block:'center',behavior:'instant'}); return true})()")
                        await pg.wait_for_timeout(400)
                        onclose = await pg.evaluate("document.getElementById('mcta').classList.contains('show')")
                        print(f'{path:34} 390 sticky CTA mid-page={mid} on closing band={onclose}')
                        if not mid or onclose: problems.append(f'{path}: sticky CTA mid={mid} close={onclose}')
                await ctx.close()
        await b.close()
    bad = 0; n = 0
    for h, pages in sorted(hrefs.items()):
        if h.startswith('#') or h.startswith('mailto:'): continue
        u = urldefrag(urljoin(B + '/concept-spec/x', h))[0] if not h.startswith('http') else h
        s = status(u); n += 1
        ok = s == 200
        if not ok: bad += 1
        print(f"{'OK ' if ok else 'BAD'} {s} {h[:100]}")
    print(f'\n{n} unique hrefs checked, {bad} not 200')
    print('problems:', problems or 'none')
asyncio.run(main())
