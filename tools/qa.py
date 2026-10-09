from playwright.sync_api import sync_playwright
import glob, os
pages = [os.path.basename(f) for f in sorted(glob.glob('/home/user/maples-tech-club/*.html'))]
with sync_playwright() as p:
    b = p.chromium.launch(); bad = 0
    # mobile overflow
    for w in (360, 390, 414):
        pg = b.new_page(viewport={'width': w, 'height': 880})
        for f in pages:
            pg.goto('file:///home/user/maples-tech-club/' + f); pg.wait_for_timeout(260)
            sw = pg.evaluate('document.documentElement.scrollWidth')
            if sw > w + 1: print(f'  OVERFLOW {w}px {f} = {sw}'); bad += 1
        pg.close()
    print(f'  mobile overflow issues: {bad}')

    pg = b.new_page(viewport={'width': 1280, 'height': 900})
    for f in pages:
        pg.goto('file:///home/user/maples-tech-club/' + f); pg.wait_for_timeout(400)
        # nav one line + height cap
        nb = pg.evaluate("()=>{const n=document.querySelector('.navin');const r=n.getBoundingClientRect();"
                         "const as=[...n.querySelectorAll('.links a')].map(a=>a.getBoundingClientRect().top);"
                         "return [r.height, new Set(as.map(t=>Math.round(t))).size];}")
        h1 = pg.evaluate("()=>{const e=document.querySelector('h1');if(!e)return 0;"
                         "const cs=getComputedStyle(e);return Math.round(e.getBoundingClientRect().height/parseFloat(cs.lineHeight));}")
        wrap = pg.evaluate("()=>[...document.querySelectorAll('.btn')].filter(b=>b.getBoundingClientRect().height>58).length")
        ok = nb[0] <= 80 and nb[1] == 1 and wrap == 0
        print(f'  {f:20} nav {nb[0]:.0f}px/{nb[1]}line  h1 {h1} lines  wrapped CTAs {wrap}  {"OK" if ok else "CHECK"}')
        if not ok: bad += 1
    pg.close(); b.close()
    print(f'\n  total issues: {bad}')
