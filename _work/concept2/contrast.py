"""Ground contrast: hide text, sample the pixels behind each text block, report worst-case (95th pct luminance) contrast vs the text colour."""
import asyncio, sys, io
from playwright.async_api import async_playwright
from PIL import Image
URL = sys.argv[1]
SEL = ['.band .h2', '.band .lead', '.want h2', '.want h2 span', '.want-cols p', '.want .whisper', '.split-cap', '.hero h1 .soft', '.hero-sub']
def lum(c):
    c = [v/255 for v in c[:3]]; c = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in c]
    return .2126*c[0]+.7152*c[1]+.0722*c[2]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w, h in ((1440, 900), (390, 844)):
            pg = await (await b.new_context(viewport={'width': w, 'height': h}, reduced_motion='reduce')).new_page()
            await pg.goto(URL, wait_until='networkidle')
            await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
            await pg.wait_for_function('[...document.images].every(i=>i.complete)')
            await pg.add_style_tag(content='.nav,.mcta,.draft-tag,.sheet{display:none!important}')
            for s in SEL:
                els = await pg.query_selector_all(s)
                for el in els[:2]:
                    col = await el.evaluate("e=>getComputedStyle(e).color")
                    await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(150)
                    await el.evaluate("e=>{if(!document.getElementById('hx')){const st=document.createElement('style');st.id='hx';st.textContent='.hx,.hx *{color:transparent!important}.hx{width:fit-content!important}';document.head.append(st)}e.classList.add('hx')}")
                    png = await el.screenshot()
                    await el.evaluate("e=>e.classList.remove('hx')")
                    im = Image.open(io.BytesIO(png)).convert('RGB'); px = sorted(lum(c) for c in im.getdata())
                    bg = px[int(len(px)*.95)]
                    nums = [float(x) for x in col[col.index('(')+1:-1].split(',')]
                    a = nums[3] if len(nums) > 3 else 1
                    # text colour composited over that ground
                    bgc = [v for v in im.getdata()][0]
                    fg_l = lum([255*a + 0*(1-a)]*3) if nums[0] > 200 else lum(nums)
                    # approx: composite white@a over ground luminance
                    if nums[0] > 200: fg_l = a*1 + (1-a)*bg
                    hi, lo = max(fg_l, bg), min(fg_l, bg)
                    print(w, f'{s:18}', f'{(hi+.05)/(lo+.05):.2f}:1')
        await b.close()
asyncio.run(main())
