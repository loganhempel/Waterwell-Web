"""Form test with Web3Forms STUBBED (never submits for real). Checks payload, success/error copy, conversion only on success."""
import asyncio, json
from playwright.async_api import async_playwright
B='http://127.0.0.1:8231'
CASES=[('/concept-spec','#bookform',True),('/concept-spec/book/discovery','#bookform',True),('/concept-spec/book/consultation','#bookform',True),('/concept-spec','#bookform',False)]
async def run(b, path, sel, ok):
    ctx=await b.new_context(); pg=await ctx.new_page(); posts=[]; real=[]
    async def w3(route):
        posts.append(json.loads(route.request.post_data))
        await route.fulfill(status=200 if ok else 500, content_type='application/json', body=json.dumps({'success':ok}))
    await pg.route('https://api.web3forms.com/**', w3)
    await pg.route('https://www.googletagmanager.com/**', lambda r: r.fulfill(status=200, body='', content_type='application/javascript'))
    pg.on('request', lambda r: real.append(r.url) if 'web3forms' in r.url and False else None)
    await pg.goto(B+path, wait_until='networkidle')
    # mailto fallback: record instead of navigating
    await pg.evaluate("""()=>{window.__mail=null;}""")
    f=pg.locator(sel)
    await f.locator('[type=submit]').click(); await pg.wait_for_timeout(200)
    v1=await f.locator('.bf-status').inner_text()
    await f.locator('input[name=name]').fill('Test Person'); await f.locator('input[name=email]').fill('test@example.com')
    if await f.locator('select[name=concern]').count(): await f.locator('select[name=concern]').select_option('Hives (urticaria)')
    await f.locator('textarea[name=msg]').fill('stub test')
    nav=[]; pg.on('framenavigated', lambda fr: nav.append(fr.url))
    await f.locator('[type=submit]').click(); await pg.wait_for_timeout(1200)
    st=await f.locator('.bf-status').inner_text()
    dl=await pg.evaluate("JSON.stringify((window.dataLayer||[]).map(x=>Array.from ? (x.length!==undefined?Array.from(x):x):x))")
    conv='"conversion"' in dl; lead='generate_lead' in dl
    p=posts[0] if posts else {}
    print(f"{path:32} stub={'success' if ok else 'HTTP500'} | validation='{v1}' | posts={len(posts)} subject='{p.get('subject')}' booking={p.get('booking_type')} concern='{p.get('concern')}' page={p.get('page')} tz={'yes' if p.get('timezone') else 'no'} key={p.get('access_key','')[:8]}… | status='{st}' | generate_lead={lead} conversion={conv}")
    await ctx.close()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for c in CASES: await run(b,*c)
        await b.close()
asyncio.run(main())
