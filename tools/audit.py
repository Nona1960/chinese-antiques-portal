#!/usr/bin/env python3
"""Site audit: run a local server on :8765 from the repo root, then `python3 tools/audit.py`."""
import json, os, re, sys, urllib.parse
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "http://localhost:8765/"
pages = []
for dp, dn, fn in os.walk(ROOT):
    if "/." in dp or "/tools" in dp:
        continue
    for f in fn:
        if f.endswith(".html"):
            pages.append(os.path.relpath(os.path.join(dp, f), ROOT))
pages.sort()
problems = []
def P(*a):
    problems.append(" ".join(str(x) for x in a))

JS_CROP = """() => [...document.querySelectorAll('img')].filter(i=>i.complete && i.naturalWidth).map(i=>{
  const cs=getComputedStyle(i); const r=i.getBoundingClientRect();
  const na=i.naturalWidth/i.naturalHeight, ra=r.width/r.height;
  return {src:i.getAttribute('src'), fit:cs.objectFit, crop: cs.objectFit==='cover' && Math.abs(na-ra)/na>0.04, alt:i.getAttribute('alt'), w:r.width}})"""
JS_ALIGN = """() => { const out=[]; for (const sel of ['.cards','.books','.split']) { document.querySelectorAll(sel).forEach((g,gi)=>{
  const btns=[...g.children].map(c=>[...c.querySelectorAll('.btn,.more')].pop()).filter(Boolean);
  if (btns.length>1 && getComputedStyle(g).gridTemplateColumns.split(' ').length>1){ const tops=btns.map(b=>Math.round(b.getBoundingClientRect().top)); if (Math.max(...tops)-Math.min(...tops)>3) out.push(sel+'#'+gi+' '+tops.join('/')); } }); } return out; }"""

with sync_playwright() as p:
    b = p.chromium.launch()
    for vw in (1366, 768, 390):
        pg = b.new_page(viewport={"width": vw, "height": 900})
        for u in pages:
            url = BASE + u
            pg.goto(url, wait_until="load")
            pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            pg.wait_for_timeout(150)
            pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
            pg.wait_for_timeout(250)
            sw = pg.evaluate("document.documentElement.scrollWidth")
            if sw > vw: P(f"[{vw}] OVERFLOW {u} scrollWidth={sw}")
            for im in pg.evaluate(JS_CROP):
                if im["crop"]: P(f"[{vw}] CROPPED {u} {im['src']}")
                if not im["alt"]: P(f"[{vw}] NO-ALT {u} {im['src']}")
            for a in pg.evaluate(JS_ALIGN): P(f"[{vw}] MISALIGNED {u} {a}")
            if vw == 1366:
                # links
                hrefs = pg.evaluate("[...document.querySelectorAll('a[href]')].map(a=>a.href)")
                for h in set(hrefs):
                    if h.startswith(BASE):
                        path, _, frag = h[len(BASE):].partition("#")
                        path = urllib.parse.unquote(path) or "index.html"
                        if path.endswith("/"): path += "index.html"
                        fp = os.path.join(ROOT, path)
                        if not os.path.exists(fp): P(f"BROKEN-LINK {u} -> {h}"); continue
                        if frag and fp.endswith(".html"):
                            if f'id="{frag}"' not in open(fp, encoding="utf-8").read(): P(f"BROKEN-ANCHOR {u} -> {h}")
                srcs = pg.evaluate("[...document.querySelectorAll('img[src],source[srcset],link[href]')].map(e=>e.src||e.srcset||e.href)")
                for s in set(srcs):
                    if s.startswith(BASE) and not os.path.exists(os.path.join(ROOT, urllib.parse.unquote(s[len(BASE):]))):
                        P(f"MISSING-ASSET {u} -> {s}")
                html = open(os.path.join(ROOT, u), encoding="utf-8").read()
                t = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
                d = re.search(r'name="description" content="([^"]*)"', html)
                if not (25 <= len(t) <= 70): P(f"TITLE-LEN {len(t)} {u}: {t}")
                if not d or not (70 <= len(d.group(1)) <= 165): P(f"DESC-LEN {len(d.group(1)) if d else 0} {u}")
                if html.count("<h1") != 1: P(f"H1-COUNT {html.count('<h1')} {u}")
                if u != "index.html" and "Back to Home" not in html: P(f"NO-BACK {u}")
                for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
                    try: json.loads(m)
                    except Exception as e: P(f"JSONLD {u} {e}")
        pg.close()
    b.close()

titles = {}
for u in pages:
    t = re.search(r"<title>(.*?)</title>", open(os.path.join(ROOT, u), encoding="utf-8").read(), re.S).group(1)
    titles.setdefault(t, []).append(u)
for t, us in titles.items():
    if len(us) > 1: P(f"DUP-TITLE {t} {us}")
sm = open(os.path.join(ROOT, "sitemap.xml")).read()
for u in pages:
    if u == "404.html": continue
    loc = "/" + ("" if u == "index.html" else u.replace("index.html", ""))
    if loc not in sm: P(f"NOT-IN-SITEMAP {u}")
print(f"{len(pages)} pages audited")
print("\n".join(sorted(set(problems))) or "NO PROBLEMS")
