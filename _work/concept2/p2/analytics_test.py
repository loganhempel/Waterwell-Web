"""Analytics host guard test. Preview = the local server (127.0.0.1). Production is SIMULATED:
the browser opens https://www.waterwellclinic.com/... and https://waterwellclinic.com/..., and
every request to those hosts is intercepted and answered from the local server (nothing reaches
the real site). googletagmanager.com is stubbed and recorded; Web3Forms is stubbed (never real).
Checks per page: is the gtag loader requested, is window.gtag defined; on the homepage it also
submits the form (stubbed 200) and checks the Ads conversion call fires only in production."""
import asyncio, json, sys
from urllib.parse import urlsplit
from playwright.async_api import async_playwright
LOCAL = 'http://127.0.0.1:8231'
PAGES = ['/concept-spec', '/concept-spec/about', '/concept-spec/treatment', '/concept-spec/podcast',
         '/concept-spec/book/discovery', '/concept-spec/book/consultation']
async def run(b, base, path):
    ctx = await b.new_context(); pg = await ctx.new_page(); gtm = []
    async def tag(route): gtm.append(route.request.url); await route.fulfill(status=200, body='', content_type='application/javascript')
    await pg.route('https://www.googletagmanager.com/**', tag)
    await pg.route('https://api.web3forms.com/**', lambda r: r.fulfill(status=200, content_type='application/json', body=json.dumps({'success': True})))
    if 'waterwellclinic.com' in base:
        async def proxy(route):
            u = urlsplit(route.request.url)
            resp = await route.fetch(url=LOCAL + u.path + (('?' + u.query) if u.query else ''))
            await route.fulfill(response=resp)
        await pg.route(base + '/**', proxy)
    await pg.goto(base + path, wait_until='networkidle')
    host = await pg.evaluate('location.hostname')
    has_gtag = await pg.evaluate("typeof window.gtag === 'function'")
    conv = None
    if path == '/concept-spec':
        f = pg.locator('#bookform')
        await f.locator('input[name=name]').fill('Test Person'); await f.locator('input[name=email]').fill('test@example.com')
        await f.locator('textarea[name=msg]').fill('stub test')
        await f.locator('[type=submit]').click(); await pg.wait_for_timeout(1200)
        dl = await pg.evaluate("JSON.stringify((window.dataLayer||[]).map(x=>x&&x.length!==undefined?Array.from(x):x))")
        conv = ('"conversion"' in dl and 'AW-18419793511/Mk14CKn756IdEOf8ns9E' in dl)
    await ctx.close()
    return host, len(gtm), has_gtag, conv
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); bad = 0
        for base, want in ((LOCAL, False), ('https://www.waterwellclinic.com', True), ('https://waterwellclinic.com', True)):
            for path in PAGES:
                host, n, g, conv = await run(b, base, path)
                ok = (n > 0) == want and g == want and (conv is None or conv == want)
                bad += not ok
                print(f"{'PASS' if ok else 'FAIL'} host={host:24} {path:34} gtag_js_requests={n} window.gtag={g}" + ('' if conv is None else f' ads_conversion_on_submit={conv}'))
        await b.close(); sys.exit(1 if bad else 0)
asyncio.run(main())
