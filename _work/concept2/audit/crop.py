import asyncio, sys
from playwright.async_api import async_playwright
B=f'http://127.0.0.1:{sys.argv[1]}'; path=sys.argv[2]; text=sys.argv[3]; out=sys.argv[4]; w=int(sys.argv[5]) if len(sys.argv)>5 else 1440
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await (await b.new_context(viewport={'width':w,'height':900 if w>500 else 844},reduced_motion='reduce')).new_page()
        await pg.goto(B+path,wait_until='networkidle')
        el=pg.locator(f'xpath=//*[self::p or self::h2 or self::span][contains(normalize-space(.),"{text}")]').last
        await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(300)
        bb=await el.bounding_box(); print(bb)
        await pg.screenshot(path=out,clip={'x':max(0,bb['x']-40),'y':max(0,bb['y']-60),'width':min(w,bb['width']+300),'height':bb['height']+120})
        await b.close()
asyncio.run(main())
