"""Copy the Atlas of Ancient Jade and Bronze Diagnostics into the portal.

Source: a local clone of https://github.com/Nona1960/Atlas-of-Ancient-Jade-and-Bronze-Diagnostics
Target: /jade-bronze-atlas/ on the portal (served by Vercel).

Each page gets a slim "Chinese Antiques portal" bar at the top, a canonical URL
and Vercel Web Analytics. The atlas pages themselves are not otherwise changed.

Usage:
    git clone https://github.com/Nona1960/Atlas-of-Ancient-Jade-and-Bronze-Diagnostics /tmp/jb-atlas
    python3 tools/sync_jade_atlas.py /tmp/jb-atlas
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "jade-bronze-atlas"
BASE = "https://chinese-antiques-portal.vercel.app/jade-bronze-atlas/"

BAR = '''<div class="portal-bar" style="background:#f6f1e4;border-bottom:1px solid #d9c9a3;font:500 13px/1.4 Inter,system-ui,sans-serif;padding:7px 16px;display:flex;flex-wrap:wrap;gap:6px 18px;align-items:center;justify-content:center;position:relative;z-index:1000">
<a href="/" style="color:#7a5a1e;text-decoration:none">&larr; Chinese Antiques &mdash; Scientific Library</a>
<span style="color:#9a8a6a">Porcelain &middot; Jade &middot; Bronze</span>
<a href="/jade-bronze.html" style="color:#7a5a1e;text-decoration:none">Bronze &amp; Jade</a>
<a href="/atlas.html" style="color:#7a5a1e;text-decoration:none">Atlas of Porcelain</a>
<a href="/library.html" style="color:#7a5a1e;text-decoration:none">Library</a>
</div>
'''
ANALYTICS = '<script defer src="/_vercel/insights/script.js"></script>\n'


def process(html: str, name: str) -> str:
    url = BASE if name == "index.html" else BASE + name
    if 'rel="canonical"' not in html:
        html = html.replace("</head>", f'<link rel="canonical" href="{url}">\n</head>', 1)
    if "portal-bar" not in html:
        html = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + BAR, html, count=1)
    if "/_vercel/insights/script.js" not in html:
        html = html.replace("</body>", ANALYTICS + "</body>", 1)
    return html


def main(src: str) -> None:
    src_dir = Path(src)
    if not (src_dir / "index.html").exists():
        sys.exit(f"{src_dir} does not look like the atlas repository")
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir()
    count = 0
    for f in sorted(src_dir.rglob("*")):
        rel = f.relative_to(src_dir)
        if f.is_dir() or rel.parts[0].startswith(".") or f.name == "README.md":
            continue
        out = DEST / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        if f.suffix == ".html":
            out.write_text(process(f.read_text(encoding="utf-8"), rel.as_posix()), encoding="utf-8")
            count += 1
        else:
            shutil.copy2(f, out)
    print(f"{count} pages copied to {DEST.relative_to(ROOT)}/")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/jb-atlas")
