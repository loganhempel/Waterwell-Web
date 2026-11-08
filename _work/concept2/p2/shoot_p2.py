"""Usage: python3 shoot.py URL TAG [full]. Fold + optional full-page shots at 1440 and 390; prints metrics."""
import asyncio, sys
from playwright.async_api import async_playwright
URL, TAG = sys.argv[1], sys.argv[2]; FULL = 'full' in sys.argv[3:]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h in ((1440, 900), (390, 844)):
            ctx = await b.new_context(viewport={'width': w, 'height': h}, is_mobile=w < 500, has_touch=w < 500, device_scale_factor=1)
            pg = await ctx.new_page()
            errs = []
            pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.route('https://www.googletagmanager.com/**', lambda r: r.fulfill(status=200, body='', content_type='application/javascript'))
            await pg.goto(URL, wait_until='networkidle'); await pg.wait_for_timeout(2600)
            await pg.screenshot(path=f'shots/{TAG}-{w}-fold.png')
            if FULL:
                H = await pg.evaluate('document.documentElement.scrollHeight')
                for y in range(0, H, 600): await pg.evaluate(f"scrollTo({{top:{y},behavior:'instant'}})"); await pg.wait_for_timeout(90)
                await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
                await pg.wait_for_function('[...document.images].every(i=>i.complete)', timeout=15000)
                await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(500)
                await pg.screenshot(path=f'shots/{TAG}-{w}-full.png', full_page=True)
            m = await pg.evaluate('''() => {
              const vis = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el); return r.width>0 && r.height>0 && s.visibility!=='hidden' && s.display!=='none'; };
              const ctas = [...document.querySelectorAll('main a.btn, main button.btn, .nav a.btn')].filter(vis).map(a => ({t:a.textContent.trim().slice(0,40), top:Math.round(a.getBoundingClientRect().top+scrollY), bottom:Math.round(a.getBoundingClientRect().bottom+scrollY)}));
              const f = document.querySelector('form input:not([type=hidden]):not([tabindex="-1"])');
              return {H: document.documentElement.scrollHeight, sw: document.documentElement.scrollWidth, ctas: ctas.slice(0,6), firstField: f ? Math.round(f.getBoundingClientRect().top+scrollY) : null};
            }''')
            print(w, m, 'errors:', errs)
            await ctx.close()
        await b.close()
asyncio.run(main())
