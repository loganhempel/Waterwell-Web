"""Contrast of text that sits over a photo, measured on the rendered ground (text hidden,
95th-percentile worst pixel under each text box). Usage: python3 contrast.py PORT"""
import asyncio, sys, io
from PIL import Image
from playwright.async_api import async_playwright
B = f'http://127.0.0.1:{sys.argv[1]}'
PAGES = ['/concept-spec', '/concept-spec/about', '/concept-spec/treatment', '/concept-spec/podcast', '/concept-spec/book/discovery', '/concept-spec/book/consultation']
def lum(c):
    c = [x / 255 for x in c[:3]]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)
FIND = """(()=>{const out=[];let k=0;
 document.querySelectorAll('h1,h2,h3,p,li,.eyebrow,small,figcaption').forEach(e=>{
  if(e.closest('nav,.sheet,.mcta,.bk-bar,.concept-badge'))return;
  const t=[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim().length>2); if(!t)return;
  const r=e.getBoundingClientRect(); if(r.width<5||r.height<5)return;
  const sec=e.closest('section,header,figure,div.band,div.want'); if(!sec)return;
  const imgs=[...sec.querySelectorAll('img')].filter(i=>{const q=i.getBoundingClientRect();return q.left<r.right&&q.right>r.left&&q.top<r.bottom&&q.bottom>r.top&&!i.contains(e)&&getComputedStyle(i).visibility!=='hidden'});
  if(!imgs.length)return;
  e.dataset.ck=k++; out.push([e.dataset.ck,e.tagName,e.textContent.trim().slice(0,40),getComputedStyle(e).color,Math.round(r.top+scrollY)]);
 });return out})()"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for path in PAGES:
            for w in (1440, 390):
                ctx = await b.new_context(viewport={'width': w, 'height': 844 if w < 500 else 900}, is_mobile=w < 500, reduced_motion='reduce')
                pg = await ctx.new_page(); await pg.goto(B + path, wait_until='networkidle')
                await pg.add_style_tag(content='.mcta{display:none!important}')
                items = await pg.evaluate(FIND)
                for ck, tag, txt, col, top in items:
                    el = pg.locator(f'[data-ck="{ck}"]')
                    await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(250)
                    box = await el.bounding_box()
                    if not box: continue
                    await el.evaluate("e=>{e.dataset.oc=e.style.color;e.style.setProperty('color','transparent','important');e.querySelectorAll('*').forEach(c=>c.style.setProperty('color','transparent','important'))}")
                    png = await pg.screenshot(clip=box)
                    await el.evaluate("e=>{e.style.color=e.dataset.oc;e.querySelectorAll('*').forEach(c=>c.style.removeProperty('color'))}")
                    im = Image.open(io.BytesIO(png)).convert('RGB'); px = list(im.getdata())
                    import re
                    tc = tuple(int(float(x)) for x in re.findall(r'[\d.]+', col)[:3])
                    rs = sorted(ratio(tc, q) for q in px)
                    worst = rs[int(len(rs) * .05)]
                    flag = 'LOW ' if worst < 4.5 else 'ok  '
                    print(f'{flag}{worst:5.2f}:1 {path:32} @{w} {tag} "{txt}"')
                await ctx.close()
        await b.close()
asyncio.run(main())
