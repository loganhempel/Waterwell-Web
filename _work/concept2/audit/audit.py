"""Independent audit of the 6 concept-spec pages. Usage: python3 audit.py PORT TAG
Shots (1440 + 390, fold + full), overflow 320/390/1440, console errors, first-screen CTA at 390,
lander first field, keyboard (menu sheet, accordions), focus ring, reduced motion,
stubbed form (success converts, failure does not). Web3Forms + gtag are ALWAYS stubbed."""
import asyncio, sys, json, os
from playwright.async_api import async_playwright
PORT, TAG = sys.argv[1], sys.argv[2]
B = f'http://127.0.0.1:{PORT}'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots', TAG); os.makedirs(OUT, exist_ok=True)
PAGES = {'home': '/concept-spec', 'discovery': '/concept-spec/book/discovery', 'consultation': '/concept-spec/book/consultation',
         'about': '/concept-spec/about', 'treatment': '/concept-spec/treatment', 'podcast': '/concept-spec/podcast'}
R = []
def log(*a): s = ' '.join(str(x) for x in a); print(s); R.append(s)

async def stub(pg, ok=True):
    async def w3(route):
        await route.fulfill(status=200 if ok else 500, content_type='application/json',
                            body=json.dumps({'success': ok}), headers={'access-control-allow-origin': '*'})
    await pg.route('https://api.web3forms.com/**', w3)
    await pg.route('https://www.googletagmanager.com/**', lambda r: r.fulfill(status=200, body=''))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, path in PAGES.items():
            for w in (1440, 390, 320):
                mob = w < 500
                ctx = await b.new_context(viewport={'width': w, 'height': 844 if mob else 900}, is_mobile=mob, has_touch=mob, device_scale_factor=1)
                pg = await ctx.new_page(); errs = []
                pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
                pg.on('pageerror', lambda e: errs.append(str(e)))
                await stub(pg)
                await pg.goto(B + path, wait_until='networkidle'); await pg.wait_for_timeout(500)
                sw = await pg.evaluate('document.documentElement.scrollWidth')
                if sw > w: log(f'OVERFLOW {name}@{w} scrollWidth={sw}')
                if errs: log(f'CONSOLE {name}@{w} {errs}')
                if w == 320: await ctx.close(); continue
                await pg.screenshot(path=f'{OUT}/{name}-{w}-fold.png')
                if mob:
                    # first-screen CTA: any visible a.btn / button inside 844 (not the nav sheet/menu)
                    cta = await pg.evaluate("""[...document.querySelectorAll('main a.btn, main button[type=submit], header a.btn:not(.nav a), section a.btn')].filter(e=>{const r=e.getBoundingClientRect();return r.height>0&&r.bottom<=innerHeight&&r.top>=0}).map(e=>e.textContent.trim().replace(/\\s+/g,' ').slice(0,40)+' @'+Math.round(e.getBoundingClientRect().top))""")
                    log(f'{name}@390 first-screen CTAs: {cta or "NONE"}')
                    f1 = await pg.evaluate("(()=>{const e=document.querySelector('form[data-enquiry] input:not([type=hidden]):not([tabindex=\"-1\"])');return e?Math.round(e.getBoundingClientRect().top):null})()")
                    sb = await pg.evaluate("(()=>{const f=document.querySelector('form[data-enquiry]');if(!f)return null;const e=f.querySelector('[type=submit]');return Math.round(e.getBoundingClientRect().bottom)})()")
                    if f1 is not None and name in ('discovery','consultation'): log(f'{name}@390 first field top={f1} submit bottom={sb}')
                # full page: scroll through to trigger reveals
                H = await pg.evaluate('document.documentElement.scrollHeight')
                for y in range(0, H, 400):
                    await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(60)
                await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(400)
                await pg.screenshot(path=f'{OUT}/{name}-{w}-full.png', full_page=True)
                # low-res stretched images
                imgs = await pg.evaluate("""[...document.images].filter(i=>i.naturalWidth&&i.getBoundingClientRect().width>0).map(i=>{const r=i.getBoundingClientRect();const fit=getComputedStyle(i).objectFit;return [i.getAttribute('src').split('/').pop(),i.naturalWidth,i.naturalHeight,Math.round(r.width),Math.round(r.height),fit]}).filter(a=>{const s=Math.max(a[3]/a[1],a[4]/a[2]);return s>1.25})""")
                if imgs: log(f'UPSCALE {name}@{w}: {imgs}')
                await ctx.close()

        # keyboard: menu sheet at 390, accordions on home at 1440, focus ring
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        pg = await ctx.new_page(); await stub(pg)
        await pg.goto(B + '/concept-spec', wait_until='networkidle')
        await pg.focus('#menuBtn'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(200)
        op = await pg.evaluate("!document.getElementById('sheet').hidden && document.getElementById('menuBtn').getAttribute('aria-expanded')")
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200)
        cl = await pg.evaluate("document.getElementById('sheet').hidden && document.activeElement.id")
        log(f'menu sheet: Enter opens={op} Esc closes+refocus={cl}')
        await ctx.close()
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900})
        pg = await ctx.new_page(); await stub(pg)
        await pg.goto(B + '/concept-spec', wait_until='networkidle')
        n = await pg.locator('details > summary').count()
        if n:
            s = pg.locator('details > summary').first
            await s.focus(); ring = await s.evaluate("e=>{const c=getComputedStyle(e);return c.outlineStyle+' '+c.outlineWidth+' '+c.outlineColor+' | '+c.boxShadow}")
            await pg.keyboard.press('Enter'); o1 = await s.evaluate('e=>e.parentElement.open')
            await pg.keyboard.press('Space'); o2 = await s.evaluate('e=>e.parentElement.open')
            log(f'accordion: {n} summaries; Enter open={o1}, Space closes={not o2}; focus style: {ring}')
        # focus ring sweep: tab 25 times, record elements with no visible focus style
        nofocus = []
        await pg.evaluate('document.activeElement.blur(); scrollTo(0,0)')
        for i in range(40):
            await pg.keyboard.press('Tab')
            r = await pg.evaluate("""(()=>{const e=document.activeElement;const c=getComputedStyle(e);const vis=(c.outlineStyle!=='none'&&parseFloat(c.outlineWidth)>0)||c.boxShadow!=='none';return [e.tagName+'.'+e.className+' '+(e.textContent||'').trim().slice(0,25),vis]})()""")
            if not r[1]: nofocus.append(r[0])
        log(f'focus sweep (40 tabs, home): no visible ring on {nofocus or "none"}')
        await ctx.close()

        # reduced motion
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900}, reduced_motion='reduce')
        pg = await ctx.new_page(); await stub(pg)
        await pg.goto(B + '/concept-spec', wait_until='networkidle'); await pg.wait_for_timeout(300)
        rm = await pg.evaluate("""(()=>{const anim=document.getAnimations().filter(a=>a.playState==='running').map(a=>(a.animationName||a.transitionProperty||'?')+' on '+a.effect.target.className);const hidden=[...document.querySelectorAll('.bw-row,.j-step,.reveal,[data-reveal]')].filter(e=>getComputedStyle(e).opacity<0.99).length;return {anim,hidden}})()""")
        log(f'reduced motion: running animations={rm["anim"]} hidden reveal items={rm["hidden"]}')
        await ctx.close()

        # forms: success converts (simulate prod gtag), failure does not; mailto intercepted
        for name in ('home', 'discovery', 'consultation'):
            for ok in (True, False):
                ctx = await b.new_context(viewport={'width': 1440, 'height': 900})
                pg = await ctx.new_page(); await stub(pg, ok); posts = []
                pg.on('request', lambda r: posts.append(r.url) if 'web3forms' in r.url else None)
                await pg.goto(B + PAGES[name], wait_until='networkidle')
                await pg.evaluate("window.__ev=[];window.gtag=function(){__ev.push([...arguments].slice(0,2).join(':'))};window.AW_LEAD=window.AW_LEAD||'AW-test/x';window.__mailto=0;")
                f = pg.locator('form[data-enquiry]').first
                await f.locator('[name=name]').fill('Audit Test'); await f.locator('[name=email]').fill('audit@example.com')
                await pg.evaluate("Object.defineProperty(window,'location',{configurable:true})" if False else '0')
                await f.locator('[type=submit]').click(); await pg.wait_for_timeout(800)
                st = await f.locator('.bf-status').text_content()
                ev = await pg.evaluate('window.__ev')
                log(f'form {name} stub={"200" if ok else "500"}: posts={len(posts)} status="{st}" gtag={ev}')
                await ctx.close()
        await b.close()
    open(os.path.join(OUT, 'report.txt'), 'w').write('\n'.join(R))
asyncio.run(main())
