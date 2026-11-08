"""Viewport shots of every top-level section, scrolled in naturally (reveals + lazy images fire).
Usage: python3 sections.py PORT TAG [page ...]"""
import asyncio, sys, os
from playwright.async_api import async_playwright
PORT, TAG = sys.argv[1], sys.argv[2]
B = f'http://127.0.0.1:{PORT}'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots', TAG, 'sec'); os.makedirs(OUT, exist_ok=True)
PAGES = {'home': '/concept-spec', 'discovery': '/concept-spec/book/discovery', 'consultation': '/concept-spec/book/consultation',
         'about': '/concept-spec/about', 'treatment': '/concept-spec/treatment', 'podcast': '/concept-spec/podcast'}
want = sys.argv[3:] or list(PAGES)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name in want:
            for w in (1440, 390):
                mob = w < 500
                ctx = await b.new_context(viewport={'width': w, 'height': 844 if mob else 900}, is_mobile=mob, has_touch=mob)
                pg = await ctx.new_page()
                await pg.route('https://api.web3forms.com/**', lambda r: r.fulfill(status=200, body='{"success":true}'))
                await pg.goto(B + PAGES[name], wait_until='networkidle')
                n = await pg.evaluate("document.querySelectorAll('body > section, main > section, body > header, main > header, body > footer, main > div.sec, body > div.connect').length")
                tops = await pg.evaluate("[...document.querySelectorAll('body > section, main > section, body > header, main > header, body > footer, body > div.connect')].map(e=>e.getBoundingClientRect().top+scrollY)")
                for i, t in enumerate(tops):
                    y = max(0, t - (70 if i else 0))
                    for yy in range(int(max(0, y - 600)), int(y) + 1, 150):
                        await pg.evaluate(f'scrollTo(0,{yy})'); await pg.wait_for_timeout(30)
                    await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(900)
                    await pg.screenshot(path=f'{OUT}/{name}-{w}-{i:02d}.png')
                await ctx.close()
        await b.close()
asyncio.run(main())
