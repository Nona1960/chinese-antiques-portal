#!/usr/bin/env python3
"""Static site builder for the Chinese Antiques portal.

Run from the repository root:  python3 tools/build.py
Pages are generated into the repository root. Chapter texts live in
tools/content/<book>/chNN.md (Markdown, converted with pandoc).
"""
import html, json, os, re, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://chinese-antiques-portal.vercel.app"
SITE = "Chinese Antiques"
TAGLINE = "Scientific Library & Expert Reference"
TODAY = datetime.date.today().isoformat()
ORCID = "https://orcid.org/0009-0007-4867-9074"
ATLAS = "https://nona1960.github.io/atlas-of-chinese-porcelain-diagnostics/"
ATLAS_JB = "https://nona1960.github.io/Atlas-of-Ancient-Jade-and-Bronze-Diagnostics/"
STUDIO = "https://nona-dronova-art-studio.vercel.app/"

PERSON_ID = BASE + "/author.html#person"
PERSON = {
    "@type": "Person", "@id": PERSON_ID, "name": "Nona Dmitrievna Dronova",
    "alternateName": "Nona Dmitrievna Dronova",
    "jobTitle": "Professor, Doctor of Technical Sciences; Chair of the Collegium of Expert Gemmologists of the Russian Federation",
    "description": "Gemmologist and researcher; author of non-destructive methods for the authentication of Chinese porcelain (BEINOS, DEE, LIE, PLIC), jade (STA) and bronze (TETA).",
    "alumniOf": ["Moscow School of Art Crafts", "Moscow State Geological Prospecting Institute"],
    "url": BASE + "/author.html", "image": BASE + "/images/nona-dronova.jpg",
    "sameAs": [ORCID, STUDIO, ATLAS, ATLAS_JB],
    "knowsAbout": ["Chinese porcelain", "Chinese jade", "Chinese bronze", "Gemmology",
                   "Gemmological optical microscopy", "Authentication of antiques", "Attribution"],
}

NAV = [("index.html", "Home"), ("porcelain.html", "Porcelain"), ("jade-bronze.html", "Bronze & Jade"),
       ("atlas.html", "Diagnostic Atlas"), ("library.html", "Library"), ("author.html", "About the Author")]

FOOTER = [
    ("about.html", "About the Project", "Purpose and scope of the scientific library."),
    ("author.html", "About the Author", "Biography and research of Professor Nona Dmitrievna Dronova."),
    ("literature.html", "Scientific Literature", "The author’s scientific articles on Zenodo."),
    ("library.html", "Library", "Monographs, articles and reference works."),
    ("publications.html", "Zenodo Publications", "Open-access research papers with DOI."),
]

# ------------------------------------------------------------------ books
PORCELAIN = {
    "slug": "monographs/antique-chinese-porcelain",
    "title": "What You Need to Know About Antique Chinese Porcelain",
    "orig": "Что надо знать о старинном китайском фарфоре",
    "kind": "Reference encyclopaedia",
    "year": "2016", "place": "Moscow", "isbn": "978-5-9908782-6-6", "doi": "10.5281/zenodo.16794377",
    "publisher": "KEM Printing House LLC", "publisher_ru": "ООО «Типография КЕМ»", "pages": "288", "udc": "621.315.612", "bbk": "35.41+65.304.9",
    "kind_ru": "Справочник-энциклопедия",
    "cover": "/images/porcelain-book-cover.jpg",
    "abstract": ("A reference encyclopaedia that provides the information needed to attribute antique Chinese "
                 "porcelain in accordance with international standards. Separate chapters are devoted to the "
                 "appraisal and diagnosis of export, imperial and monochrome porcelain; the book examines the "
                 "development of porcelain styles and the marks found on antique Chinese porcelain, and gives "
                 "practical recommendations for detecting forgeries."),
    "chapters": [
        (1, "On Collecting Chinese Porcelain", "Особенности коллекционирования китайского фарфора", "chapter-01-collecting-chinese-porcelain"),
        (2, "How to Distinguish Genuine Antique Porcelain from a Fake", "Как отличить подлинный старинный фарфор от подделки", "chapter-02-genuine-or-fake"),
        (3, "Appraisal of Chinese Antique Porcelain", "Оценка китайских антикварных фарфоровых изделий", "chapter-03-appraisal"),
        (4, "Features of the Attribution of Antique Chinese Porcelain", "Особенности атрибуции старинного китайского фарфора", "chapter-04-attribution"),
        (5, "Styles in Chinese Antique Porcelain", "Стили в китайских антикварных фарфоровых изделиях", "chapter-05-styles"),
        (6, "Symbols in Chinese Porcelain", "Символы китайского фарфора", "chapter-06-symbols"),
        (7, "Attribution of Wares Painted in Underglaze Cobalt Blue", "Атрибуция изделий с росписью подглазурным кобальтом", "chapter-07-underglaze-cobalt"),
        (8, "Export Porcelain", "Экспортный фарфор", "chapter-08-export-porcelain"),
        (9, "Imperial Porcelain", "Императорский фарфор", "chapter-09-imperial-porcelain"),
        (10, "Varieties of Antique Chinese Monochrome Porcelain", "Разновидности старинного китайского монохромного фарфора", "chapter-10-monochrome-porcelain"),
    ],
}
JADE = {
    "slug": "monographs/antique-chinese-jade",
    "content": "jade",
    "title": "What You Need to Know About Antique Chinese Jade",
    "subtitle": "A Handbook in Questions and Answers",
    "orig": "Что надо знать о старинном китайском нефрите",
    "kind": "Handbook in questions and answers",
    "year": "2017", "place": "Moscow", "isbn": "978-5-9909531-3-0", "cover": "/images/jade-book-cover.jpg", "doi": "10.5281/zenodo.16794851",
    "publisher": "KEM LLC", "publisher_ru": "ООО «КЕМ»", "pages": "196", "udc": "621.315.612", "bbk": "35.41+65.304.9",
    "kind_ru": "Справочник в виде вопросов и ответов",
    "abstract": ("A handbook in the form of questions and answers on the natural ageing of jade in burials and the "
                 "diagnostic signs of its antiquity. Particular attention is given to the causes of the characteristic "
                 "ring-shaped iron-rich formations crystallised on the surface of carved artefacts and to the zoning of "
                 "external corrosion on ancient Chinese jades. A separate chapter examines the noble patinas of "
                 "ancient bronzes."),
    "chapters": [
        (0, "Preface", "Введение", "preface"),
        (1, "General Information on Nephrite and Jadeite", "Общие сведения о нефрите и жадеите", "chapter-01-nephrite-and-jadeite"),
        (2, "How to Distinguish Nephrite and Jadeite from Imitations", "Как отличить нефрит и жадеит от подделок", "chapter-02-imitations"),
        (3, "The History of Jade Working", "История обработки жадеита", "chapter-03-history-of-jade-working"),
        (4, "Signs of Antiquity in Jade", "Признаки древности нефритов", "chapter-04-signs-of-antiquity"),
        (5, "Appraisal of Nephrite and Nephrite Objects", "Оценка нефрита и изделий из него", "chapter-05-appraisal"),
        (6, "Scientific Study of Ancient Chinese Bronzes", "Особенности научных исследований древних китайских бронз", "chapter-06-ancient-bronzes"),
    ],
}
PORCELAIN["content"] = "porcelain"
PORCELAIN["subtitle"] = "A Reference Encyclopaedia"
PORCELAIN["pdf"] = {"title": "The Contemporary Relevance of N. D. Dronova’s Monograph What Should One Know About Antique Chinese Porcelain?: An Integrated Approach to Attribution, Authentication, and Microscopic Diagnostics",
                    "date": "17 October 2026", "year": "2026", "doi": "10.5281/zenodo.23439580"}
JADE["pdf"] = {"title": "Natural Aging, Surface Corrosion, and Scientific Authentication of Ancient Chinese Nephrite: The Contemporary Relevance of N. D. Dronova’s 2017 Monograph",
               "date": "18 October 2026", "year": "2026", "doi": "10.5281/zenodo.23446188"}
BOOKS = [PORCELAIN, JADE]

def pdf_note(b, short=False):
    a = b["pdf"]
    link = f'<a href="https://doi.org/{a["doi"]}" target="_blank" rel="noopener">doi:{a["doi"]}</a>'
    if short:
        return f'<p class="pdf-note"><strong>Original Russian edition (PDF):</strong> attached to the Zenodo article {link}</p>'
    return (f'<div class="note"><strong>Original printed edition — PDF.</strong> The complete original Russian edition of the book is attached as a PDF to the open-access Zenodo article '
            f'<a href="https://doi.org/{a["doi"]}" target="_blank" rel="noopener"><em>{esc(a["title"])}</em></a> (Zenodo, {a["date"]}, {link}).</div>')

def esc(s):
    return html.escape(s, quote=True)

def chapter_file(b, n):
    return os.path.join(ROOT, "tools", "content", b["content"], f"ch{n:02d}.md")

def available(b, n):
    return os.path.exists(chapter_file(b, n))

def label(n):
    return "Preface" if n == 0 else f"Chapter {n}"

def toc_html(b, prefix):
    rows = []
    for n, t, o, s_ in b["chapters"]:
        ok = available(b, n)
        title = f'<a href="{prefix}{s_}.html">{esc(t)}</a>' if ok else esc(t)
        num = "—" if n == 0 else f"{n:02d}"
        rows.append(f'<li><span class="n">{num}</span><span class="t">{title}<small>{esc(o)}</small></span>'
                    f'<span class="s{" ok" if ok else ""}">{"Read" if ok else "In translation"}</span></li>')
    return '<ol class="toc">' + "".join(rows) + '</ol>'

def cover_html(b, cls="cover", width=None):
    if b["cover"]:
        return f'<img class="{cls}" src="{b["cover"]}" alt="Cover of the book «{esc(b["orig"])}» by Nona Dmitrievna Dronova" loading="lazy">'
    st = f' style="width:{width}px"' if width else ""
    return (f'<div class="cover-placeholder"{st} role="img" aria-label="Title of the book"><span class="a">Nona Dmitrievna Dronova</span>'
            f'<span class="t">{esc(b["orig"])}</span><span class="s">{esc(b["place"])} · {b["year"]}</span></div>')

def book_meta(b):
    return f'{b["kind"]} · {b["place"]}: {b["publisher"]}, {b["year"]} · {b["pages"]} pp. · ISBN {b["isbn"]}'

def biblio_html(b, full=True):
    en = (f'<strong>Dronova, Nona Dmitrievna.</strong> <em>{esc(b["orig"])}</em> [{esc(b["title"])}]: {esc(b["kind"].lower())}. '
          f'{b["place"]}: {esc(b["publisher"])}, {b["year"]}. {b["pages"]} pp. ISBN {b["isbn"]}.')
    ru = (f'Дронова Н. Д. {esc(b["orig"])}: {esc(b["kind_ru"].lower())}. — М.: {esc(b["publisher_ru"])}, {b["year"]}. — {b["pages"]} с. — ISBN {b["isbn"]}.')
    extra = f'<br><span class="udc">UDC {b["udc"]} · BBK {b["bbk"]}</span>' if full else ""
    return f'<div class="biblio-rec"><span class="eyebrow">Bibliographic record</span><p>{en}</p><p class="ru">{ru}{extra}</p></div>'

# ------------------------------------------------------------------ layout
def header(cur):
    items = "".join(
        f'<li><a href="/{h}"{" aria-current=\"page\"" if h == cur else ""}>{esc(t)}</a></li>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
 <div class="wrap header-inner">
  <a class="brand" href="/index.html" aria-label="{SITE} — home">
   <img src="/images/sun-logo-rect.jpg" alt="Sun emblem of the Chinese Antiques library — painting by Nona Dmitrievna Dronova" width="62" height="48">
   <span><span class="brand-name">CHINESE ANTIQUES</span><span class="brand-tag">{TAGLINE}</span></span>
  </a>
  <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" onclick="var n=document.getElementById('nav');n.classList.toggle('open');this.setAttribute('aria-expanded',n.classList.contains('open'))"><span></span><span></span><span></span></button>
  <nav class="nav" id="nav" aria-label="Main"><ul>{items}</ul></nav>
 </div>
</header>'''

def footer():
    cols = "".join(f'<div class="footer-col"><h4><a href="/{h}">{esc(t)}</a></h4><p>{esc(d)}</p></div>' for h, t, d in FOOTER)
    return f'''<footer class="site-footer">
 <div class="wrap footer-grid">
  <div class="footer-brand">
   <img src="/images/sun-logo-rect.jpg" alt="Sun emblem — painting by Nona Dmitrievna Dronova" width="96" height="74" loading="lazy">
   <div class="n">CHINESE ANTIQUES</div>
   <p>{TAGLINE}<br>Porcelain · Jade · Bronze</p>
   <a class="btn btn-small btn-gold" href="/index.html" style="margin-top:14px">← Back to Home</a>
  </div>
  {cols}
 </div>
 <div class="wrap footer-bottom">
  <span>&copy; 2026 Nona Dmitrievna Dronova. All rights reserved. Author of all texts, monographs and research: Professor Nona Dmitrievna Dronova.</span>
  <span><a href="{ORCID}" target="_blank" rel="noopener">ORCID 0009-0007-4867-9074</a> · <a href="{ATLAS}" target="_blank" rel="noopener">Diagnostic Atlas</a> · <a href="{STUDIO}" target="_blank" rel="noopener">Art Studio</a></span>
 </div>
</footer>'''

def page(path, title, desc, body, cur=None, og_image="/images/og-home.jpg", og_type="website",
         graph=None, crumbs=None, lang_note=None):
    url = BASE + "/" + ("" if path == "index.html" else path)
    full_title = title if path == "index.html" else f"{title} — {SITE}"
    nodes = [{"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": f"{SITE} — {TAGLINE}",
              "inLanguage": "en", "publisher": {"@id": PERSON_ID}}]
    if crumbs:
        items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"}]
        for i, (n, h) in enumerate(crumbs, 2):
            items.append({"@type": "ListItem", "position": i, "name": n, "item": BASE + "/" + h})
        nodes.append({"@type": "BreadcrumbList", "itemListElement": items})
    nodes += graph or []
    ld = json.dumps({"@context": "https://schema.org", "@graph": nodes}, ensure_ascii=False, indent=1)
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="author" content="Nona Dmitrievna Dronova">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#fbf9f5">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{SITE} — {TAGLINE}">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(full_title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{BASE}{og_image}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
{header(cur)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(doc)
    PAGES.append(path)

PAGES = []

def head_band(title, lead=None, crumbs=None, eyebrow=None):
    c = ""
    if crumbs:
        c = '<div class="crumbs"><a href="/index.html">Home</a>' + "".join(
            f' / <a href="/{h}">{esc(n)}</a>' for n, h in crumbs[:-1]) + f' / <span>{esc(crumbs[-1][0])}</span></div>'
    e = f'<span class="eyebrow">{esc(eyebrow)}</span>' if eyebrow else ""
    l = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<section class="page-head"><div class="wrap">{c}{e}<h1>{title}</h1>{l}<p class="back"><a class="btn btn-small" href="/index.html">← Back to Home</a></p></div></section>'

def book_card(b, link=True):
    ch = sum(1 for c in b["chapters"] if available(b, c[0]))
    tag = f'<span class="tag">English · {ch} of {len(b["chapters"])} parts online</span>'
    more = f'<p style="margin-top:14px"><a class="btn" href="/{b["slug"]}/">Open the book</a></p>' if link else ""
    return (f'<article class="book">{cover_html(b)}<div class="book-body"><h3>{esc(b["title"])}</h3><div class="orig">{esc(b["orig"])}</div><div class="byline">Author: Nona Dmitrievna Dronova</div>'
            f'{biblio_html(b)}<p>{esc(b["abstract"])}</p>{pdf_note(b, True)}<div class="book-actions">{tag}{more}</div></div></article>')

# ------------------------------------------------------------------ pages
def build_home():
    photos = [
        ("yellow-vase", "Yellow-glazed bottle vase · Chenghua mark and period"),
        ("celadon-vase", "Ru ware · Northern Song dynasty"),
        ("jade-bat", "Black jade bat · Neolithic period, shamanic cultures"),
        ("jade-sun-god", "Sun God · Hongshan culture"),
    ]
    figs = "".join(
        f'<figure><picture><source srcset="/images/{f}.webp" type="image/webp"><img src="/images/{f}.jpg" alt="{esc(a)}" width="480" height="640"{" loading=\"lazy\"" if i > 1 else ""}></picture><figcaption>{esc(a)}</figcaption></figure>'
        for i, (f, a) in enumerate(photos))
    body = f'''
<section class="hero">
 <div class="wrap hero-grid">
  <div class="title-card">
   <h1>Chinese Antiques</h1>
   <div class="rule"></div>
   <p class="sub">Scientific Library of Research and Attribution</p>
   <p class="fields">Porcelain · Jade · Bronze</p>
   <p class="desc">Author's monographs, scientific publications and reference materials on the expert examination and authentication of Chinese works of art.</p>
   <p class="byline" style="margin-top:14px">Author: Professor Nona Dmitrievna Dronova</p>
   <div class="actions"><a class="btn btn-gold" href="/library.html">Enter the Library</a><a class="btn" href="/atlas.html">Diagnostic Atlas</a></div>
  </div>
  <div class="photo-grid">{figs}</div>
 </div>
</section>

<section class="section">
 <div class="wrap">
  <div class="section-head"><span class="eyebrow">Fields of study</span><h2>Three materials, one method</h2>
  <p>The library brings together research on the three principal materials of Chinese antique art. Each is studied through the same principle: authenticity is established not by a single feature, but by a coherent system of material, technological and stylistic evidence.</p></div>
  <div class="cards">
   <article class="card"><img src="/images/celadon-green-vase.jpg" alt="Green celadon-glazed vase with bird-shaped handles" loading="lazy"><div class="card-body"><h3>Porcelain</h3><p>History, styles, marks and symbols; export, imperial and monochrome wares; criteria for distinguishing genuine antique porcelain from later copies and forgeries.</p><a class="more" href="/porcelain.html">Explore porcelain →</a></div></article>
   <article class="card"><img src="/images/jade-rhino.jpg" alt="White jade rhinoceros-form vessel with cover" loading="lazy"><div class="card-body"><h3>Jade</h3><p>Nephrite and its imitations, carving techniques and tool marks, surface alteration and patina as evidence of age.</p><a class="more" href="/jade-bronze.html#jade">Explore jade →</a></div></article>
   <article class="card"><img src="/images/bronze-ding-036.jpg" alt="Bronze ritual tripod vessel of ding type, Atlas reference object RO-BRONZE-036" loading="lazy"><div class="card-body"><h3>Bronze</h3><p>Ritual bronze forms, casting technology, corrosion layers and patina, and the diagnostic value of trace elements.</p><a class="more" href="/jade-bronze.html#bronze">Explore bronze →</a></div></article>
  </div>
 </div>
</section>

<section class="section alt">
 <div class="wrap">
  <div class="section-head"><span class="eyebrow">Scientific publications of the author</span><h2>Monographs</h2>
  <p>The foundation of the library: two reference monographs by Professor Nona Dmitrievna Dronova, published in Russian and presented here in English translation.</p>
  <p>The original printed editions are available in full as PDF files, attached to two open-access articles on Zenodo that examine the contemporary relevance of each monograph: <a href="https://doi.org/{PORCELAIN["pdf"]["doi"]}" target="_blank" rel="noopener">porcelain (doi:{PORCELAIN["pdf"]["doi"]})</a> and <a href="https://doi.org/{JADE["pdf"]["doi"]}" target="_blank" rel="noopener">jade (doi:{JADE["pdf"]["doi"]})</a>.</p></div>
  <div class="books">{book_card(PORCELAIN)}{book_card(JADE)}</div>
 </div>
</section>

<section class="section">
 <div class="wrap split">
  <img class="contain" src="/images/yellow-vase-chenghua-mark.jpg" alt="Base of a yellow-glazed vase with the six-character Chenghua reign mark in underglaze blue" loading="lazy">
  <div class="prose"><span class="eyebrow">Diagnostic Atlas</span><h2 style="margin-top:0">Diagnostic Atlas of Chinese Porcelain</h2>
  <p>A scientific reference system of documented objects from the Tang to the Qing dynasty. Each entry records the image, the diagnostic feature, its description, the method of observation and the limits of its interpretation.</p>
  <p><a class="btn" href="/atlas.html">About the Atlas</a></p></div>
 </div>
</section>

<section class="section alt">
 <div class="wrap split rev">
  <div class="prose"><span class="eyebrow">About the author</span><h2 style="margin-top:0">Professor Nona Dmitrievna Dronova</h2>
  <p>Doctor of Technical Sciences, Ph.D. in Geology and Mineralogy, gemmologist with more than forty years of practice; Chair of the Collegium of Expert Gemmologists of the Russian Federation and Scientific Director of the Global Diagnostic Atlas of Ancient Chinese Ceramics.</p>
  <p>Author of non-destructive methods for the authentication of Chinese porcelain (BEINOS, DEE, LIE, PLIC), jade (STA) and bronze (TETA).</p>
  <p><a class="btn" href="/author.html">Read the biography</a></p></div>
  <img src="/images/nona-dronova.jpg" alt="Professor Nona Dmitrievna Dronova" loading="lazy" style="max-width:420px;justify-self:center">
 </div>
</section>'''
    graph = [{"@type": "WebPage", "@id": BASE + "/#webpage", "url": BASE + "/", "name": "Chinese Antiques — Scientific Library of Research and Attribution",
              "isPartOf": {"@id": BASE + "/#website"}, "about": ["Chinese porcelain", "Chinese jade", "Chinese bronze"], "author": {"@id": PERSON_ID}},
             PERSON]
    page("index.html", "Chinese Antiques — Scientific Library of Research and Attribution · Porcelain, Jade, Bronze",
         "Scientific library and expert reference on Chinese antiques by Professor Nona Dmitrievna Dronova: monographs, research and methods for the attribution and authentication of porcelain, jade and bronze.",
         body, cur="index.html", graph=graph)

def build_porcelain():
    toc = toc_html(PORCELAIN, "/" + PORCELAIN["slug"] + "/")
    body = head_band("Porcelain", "Antique Chinese porcelain: history, styles, symbols and marks; the appraisal of export, imperial and monochrome wares; and the criteria that separate genuine antique pieces from later copies and forgeries.",
                     crumbs=[("Porcelain", "porcelain.html")], eyebrow="Field of study") + f'''
<section class="section">
 <div class="wrap split">
  <img src="/images/celadon-vase.jpg" alt="Pale blue crackle-glazed baluster vase" loading="lazy" style="max-width:440px">
  <div class="prose">
   <h2 style="margin-top:0">Porcelain as a historical document</h2>
   <p>The character and forms of porcelain reflect the life and development of society, its ideas, culture and daily life in a given epoch. Every object carries the evidence of its own manufacture: the composition of its body and glaze, the method of forming and firing, the style of its decoration and the traces of natural ageing.</p>
   <p>The research presented in this section approaches attribution as a sequence: examination of the object, identification of its material, dating of the period of manufacture, analysis of the decoration and marks, assessment of condition and, finally, appraisal.</p>
  </div>
 </div>
</section>
<section class="section alt">
 <div class="wrap">
  <div class="section-head"><span class="eyebrow">Monograph</span><h2>{esc(PORCELAIN["title"])}</h2><p>{esc(PORCELAIN["abstract"])}</p></div>
  {toc}
  <p style="margin-top:26px"><a class="btn btn-gold" href="/{PORCELAIN["slug"]}/">About the book</a></p>
 </div>
</section>
<section class="section">
 <div class="wrap split rev">
  <div class="prose"><span class="eyebrow">Reference collection</span><h2 style="margin-top:0">Diagnostic Atlas of Chinese Porcelain</h2>
   <p>Documented reference objects from the Tang to the Qing dynasty, examined by gemmological optical microscopy. The Atlas is the practical companion to the monograph: what the book describes, the Atlas shows at the level of glaze, body and surface.</p>
   <p><a class="btn" href="/atlas.html">Open the Atlas section</a></p></div>
  <img src="/images/atlas-song-002-phase-sep.jpg" alt="Liquid–liquid phase separation in Ru-type glaze under the microscope, reference object RO-SONG-002" loading="lazy">
 </div>
</section>'''
    page("porcelain.html", "Antique Chinese Porcelain — Attribution, Styles and Authentication",
         "Antique Chinese porcelain: history, styles, symbols and marks, export, imperial and monochrome wares, and criteria for distinguishing genuine pieces from forgeries.",
         body, cur="porcelain.html", og_image="/images/celadon-vase.jpg", crumbs=[("Porcelain", "porcelain.html")],
         graph=[{"@type": "CollectionPage", "url": BASE + "/porcelain.html", "name": "Antique Chinese Porcelain", "about": "Chinese porcelain", "author": {"@id": PERSON_ID}}])

def build_jade_bronze():
    body = head_band("Bronze &amp; Jade", "Ancient Chinese jade and ritual bronze: materials, working techniques, surface alteration and the diagnostic evidence of age.",
                     crumbs=[("Bronze & Jade", "jade-bronze.html")], eyebrow="Fields of study") + f'''
<section class="section" id="jade">
 <div class="wrap split">
  <img src="/images/jade-bat.jpg" alt="Carved dark jade figure of a bat with outspread wings" loading="lazy" style="max-width:380px;justify-self:center">
  <div class="prose">
   <span class="eyebrow">Jade</span><h2 style="margin-top:0">Antique Chinese jade</h2>
   <p>Jade occupies a unique place in Chinese culture, from the ritual objects of the Neolithic to the carvings of the Qing court. For the expert, every jade carries two records: the stone itself — nephrite, its structure and colour — and the history of its working, preserved in tool marks, polish and drilling.</p>
   <p>Authentication rests on the study of the surface: the alteration zones, burial patina and natural transformation that form over centuries and that are extremely difficult to reproduce artificially.</p>
   <p>The monograph <em>{esc(JADE["title"])}</em> ({JADE["place"]}, {JADE["year"]}), a handbook in questions and answers, is published in this library in English translation.</p>
   <p><a class="btn" href="/{JADE["slug"]}/">Open the jade monograph</a></p>
  </div>
 </div>
</section>
<section class="section alt" id="bronze">
 <div class="wrap split rev">
  <div class="prose">
   <span class="eyebrow">Bronze</span><h2 style="margin-top:0">Ancient Chinese bronze</h2>
   <p>Ritual bronze vessels and archaistic objects are studied through their form and decoration, casting technology, corrosion layers and patina. Microstructural and chemical evidence — including the trace elements of the alloy and of the corrosion products — makes it possible to distinguish natural long-term change from artificial patination.</p>
   <p>Documented reference objects in jade and bronze are published in the companion Atlas.</p>
   <p><a class="btn" href="{ATLAS_JB}" target="_blank" rel="noopener">Atlas of Ancient Jade and Bronze ↗</a></p>
  </div>
  <img src="/images/bronze-ding-036.jpg" alt="Bronze ritual tripod vessel of ding type, Atlas reference object RO-BRONZE-036" loading="lazy">
 </div>
</section>'''
    page("jade-bronze.html", "Ancient Chinese Jade and Bronze — Materials and Authentication",
         "Ancient Chinese jade and ritual bronze: materials, working techniques, surface alteration, patina and the diagnostic evidence of age.",
         body, cur="jade-bronze.html", og_image="/images/jade-bat.jpg", crumbs=[("Bronze & Jade", "jade-bronze.html")],
         graph=[{"@type": "CollectionPage", "url": BASE + "/jade-bronze.html", "name": "Ancient Chinese Jade and Bronze", "about": ["Chinese jade", "Chinese bronze"], "author": {"@id": PERSON_ID}}])

def build_atlas():
    feats = [
        ("RO-MING-028", "ro-ming-028.html", "atlas-ming-028-anhua.jpg",
         "Anhua — “hidden” incised decoration",
         "Imperial sacrificial-yellow tianqiuping · Ming, Chenghua period (1465–1487) · Imperial kilns, Jingdezhen",
         "Anhua (暗花): a five-clawed dragon and cloud scrolls incised into the body before glazing, legible only through the even jiaohuang yellow glaze.",
         "The decoration reads as darker yellow lines where the glaze pools in the incisions; it encircles the globular body in a continuous composition without cartouches.",
         "Macroscopic examination under raking (oblique) illumination; gemmological optical microscopy of the glaze surface.",
         "Incised decoration is a stylistic indicator only. It supports attribution in conjunction with the reign mark, the foot rim and the microstructure of the glaze — never on its own.",
         "Fig. Anhua on the body under oblique illumination: dragon, scales, cloud scrolls."),
        ("RO-SONG-002", "ro-song-002.html", "atlas-song-002-phase-sep.jpg",
         "Liquid–liquid phase separation in the glaze",
         "Ru-type vase with sky-blue glaze and crackle · Northern Song, late 11th – early 12th century",
         "A bimodal glaze microstructure: pale bluish rounded domains within a darker blue-grey interstitial matrix.",
         "The phase-separated structure is the physical origin of the soft internal luminosity of the sky-blue Ru glaze.",
         "Gemmological optical microscopy of the glaze surface, non-destructive, no sampling.",
         "The feature describes the glaze chemistry and firing; it is evaluated together with the body, the spur marks and the crackle network. Attribution follows the accompanying documentation.",
         "Fig. Liquid–liquid phase separation in the glaze."),
        ("RO-SONG-004", "ro-song-004.html", "atlas-song-004-overall.jpg",
         "Double crackle — jin si tie xian (金絲鐵線)",
         "Bottle vase with dense crackle · Ge-type, Southern Song, 12th–13th century",
         "Two generations of cracks: large primary polygons (“iron wire”, tie xian) subdivided by finer secondary cracks (“golden thread”, jin si).",
         "The two crack generations are differentiated by width and colour; dark iron–manganese deposits line the walls of the primary cracks.",
         "Visual examination and low magnification; microscopy of crack walls (approx. 120×).",
         "Crackle can be induced deliberately and stained artificially. Only the gradual colour transition of naturally diffused deposits, together with the body and kiln evidence, is diagnostic.",
         "Fig. Overall view of the vase."),
    ]
    cards = "".join(f'''<article class="feature">
 <div><img src="/images/{img}" alt="{esc(ttl)} — {esc(ro)}" loading="lazy"><p class="fig">{esc(fig)} {esc(ro)}.</p></div>
 <div><span class="ro">{esc(ro)}</span><h3>{esc(ttl)}</h3><p style="color:var(--muted);font-size:.9rem;margin-top:4px">{esc(obj)}</p>
  <dl><dt>Diagnostic feature</dt><dd>{esc(feat)}</dd><dt>Description</dt><dd>{esc(descr)}</dd><dt>Method of observation</dt><dd>{esc(meth)}</dd><dt>Limits of interpretation</dt><dd>{esc(lim)}</dd></dl>
  <p style="margin-top:16px"><a href="{ATLAS}{link}" target="_blank" rel="noopener">Full entry in the Atlas ↗</a></p></div>
</article>''' for ro, link, img, ttl, obj, feat, descr, meth, lim, fig in feats)
    body = head_band("Diagnostic Atlas of Chinese Porcelain",
                     "A scientific reference system for the authentication of ancient Chinese ceramics and porcelain — not a gallery of photographs, but a structured body of diagnostic evidence.",
                     crumbs=[("Diagnostic Atlas", "atlas.html")], eyebrow="Reference collection") + f'''
<section class="section">
 <div class="wrap">
  <div class="section-head"><h2>How each entry is structured</h2><p>Every diagnostic observation in the Atlas is recorded in the same five parts, so that it can be checked, compared and reproduced.</p></div>
  <div class="schema">
   <div><i>01</i><b>Image</b><span>Overall view, details and micrographs of the object.</span></div>
   <div><i>02</i><b>Diagnostic feature</b><span>The named feature being documented.</span></div>
   <div><i>03</i><b>Description</b><span>What is observed, in controlled vocabulary.</span></div>
   <div><i>04</i><b>Method of observation</b><span>Lighting, magnification and instrument.</span></div>
   <div><i>05</i><b>Limits of interpretation</b><span>What the feature can and cannot prove.</span></div>
  </div>
  <div class="note"><strong>Foundational principle.</strong> Authenticity is determined not by any single visual feature, but by a system of interrelated material characteristics. No single feature is individually diagnostic — it is the coherent conjunction of multiple parameters that supports attribution.</div>
 </div>
</section>
<section class="section alt">
 <div class="wrap">
  <div class="section-head"><span class="eyebrow">Examples from the reference collection</span><h2>Diagnostic features</h2></div>
  {cards}
 </div>
</section>
<section class="section">
 <div class="wrap split">
  <img src="/images/atlas-yuan-017-micro.jpg" alt="Glaze surface under the microscope at 40× magnification, reference object RO-YUAN-017" loading="lazy">
  <div class="prose"><h2 style="margin-top:0">The complete Atlas</h2>
  <p>The full reference collection — objects from the Tang through the Qing dynasties, each documented by the Dronova method of non-destructive gemmological optical microscopy (BEINOS) — together with the methodology and an index of more than 240 open-access publications.</p>
  <p><a class="btn btn-gold" href="{ATLAS}" target="_blank" rel="noopener">Open the Atlas ↗</a> <a class="btn" href="{ATLAS}methodology.html" target="_blank" rel="noopener">Methodology ↗</a></p>
  <p style="font-size:.85rem;color:var(--muted)">Attribution of reference objects follows their accompanying documentation; no independent authentication is claimed.</p></div>
 </div>
</section>'''
    page("atlas.html", "Diagnostic Atlas of Chinese Porcelain — Reference Collection",
         "Diagnostic Atlas of Chinese Porcelain: documented reference objects with image, diagnostic feature, description, method of observation and limits of interpretation.",
         body, cur="atlas.html", og_image="/images/atlas-ming-028-anhua.jpg", crumbs=[("Diagnostic Atlas", "atlas.html")],
         graph=[{"@type": "CollectionPage", "url": BASE + "/atlas.html", "name": "Diagnostic Atlas of Chinese Porcelain", "author": {"@id": PERSON_ID},
                 "relatedLink": ATLAS}])

def build_library():
    body = head_band("Library", "The author's own works: monographs, scientific articles and reference materials on the attribution and authentication of Chinese antiques.",
                     crumbs=[("Library", "library.html")], eyebrow="Scientific library") + f'''
<section class="section">
 <div class="wrap">
  <div class="section-head"><h2>Monographs</h2></div>
  <div class="books">{book_card(PORCELAIN)}{book_card(JADE)}</div>
 </div>
</section>
<section class="section alt">
 <div class="wrap split">
  <div class="prose"><h2 style="margin-top:0">Scientific articles</h2>
  <p>More than 240 open-access articles on the authentication of individual objects and on diagnostic method are published on Zenodo, each with its own DOI.</p>
  <p><a class="btn" href="/publications.html">Zenodo publications</a></p></div>
  <div class="prose"><h2 style="margin-top:0">Complete list of articles</h2>
  <p>All scientific articles of the author, grouped by dynasty and period, with their DOIs.</p>
  <p><a class="btn" href="/literature.html">Scientific literature</a></p></div>
 </div>
</section>'''
    page("library.html", "Library — Monographs and Research by Nona Dmitrievna Dronova",
         "Monographs, scientific articles and reference materials by Professor Nona Dmitrievna Dronova on the attribution and authentication of Chinese porcelain, jade and bronze.",
         body, cur="library.html", og_image="/images/porcelain-book-cover.jpg", crumbs=[("Library", "library.html")],
         graph=[{"@type": "CollectionPage", "url": BASE + "/library.html", "name": "Library", "author": {"@id": PERSON_ID},
                 "hasPart": [{"@id": BASE + "/" + b["slug"] + "/#book"} for b in BOOKS]}])

def book_graph(b):
    url = BASE + "/" + b["slug"] + "/"
    parts = [{"@type": "Chapter", "position": n, "name": t, "url": url + s_ + ".html"} for n, t, o, s_ in b["chapters"] if available(b, n)]
    g = {"@type": "Book", "@id": url + "#book", "name": b["orig"], "alternateName": b["title"],
         "author": {"@id": PERSON_ID}, "datePublished": b["year"], "inLanguage": "ru", "url": url,
         "description": b["abstract"], "genre": b["kind"],
         "workTranslation": {"@type": "Book", "name": b["title"], "inLanguage": "en", "url": url, "hasPart": parts}}
    if b["isbn"]: g["isbn"] = b["isbn"]
    g["publisher"] = {"@type": "Organization", "name": b["publisher"], "alternateName": b["publisher_ru"]}
    g["numberOfPages"] = int(b["pages"])
    g["sameAs"] = ["https://doi.org/" + b["pdf"]["doi"], "https://doi.org/" + b["doi"]]
    g["subjectOf"] = {"@type": "ScholarlyArticle", "name": b["pdf"]["title"], "datePublished": b["pdf"]["year"], "url": "https://doi.org/" + b["pdf"]["doi"], "author": {"@id": PERSON_ID}}
    g["identifier"] = {"@type": "PropertyValue", "propertyID": "DOI", "value": b["doi"]}
    if b["cover"]: g["image"] = BASE + b["cover"]
    return g

def build_book(b):
    isbn = f'<dt>ISBN</dt><dd>{b["isbn"]}</dd>' if b["isbn"] else ""
    isbn += f'<dt>Original edition (PDF)</dt><dd><a href="https://doi.org/{b["pdf"]["doi"]}" target="_blank" rel="noopener">doi:{b["pdf"]["doi"]}</a> — Zenodo, {b["pdf"]["date"]}</dd>'
    isbn += f'<dt>Earlier Zenodo record</dt><dd><a href="https://doi.org/{b["doi"]}" target="_blank" rel="noopener">doi:{b["doi"]}</a></dd>'
    body = head_band(esc(b["title"]), f'{esc(b["subtitle"])}<br><em>{esc(b["orig"])}</em>', crumbs=[("Library", "library.html"), (b["title"], b["slug"] + "/")], eyebrow="Monograph") + f'''
<section class="section">
 <div class="wrap split cover-split">
  {cover_html(b, "cover-lg", 300)}
  <div class="prose">
   <dl class="facts"><dt>Author</dt><dd>Nona Dmitrievna Dronova, Professor, Doctor of Technical Sciences</dd><dt>Type</dt><dd>{esc(b["kind"])}</dd><dt>Original title</dt><dd>{esc(b["orig"])}: {esc(b["kind_ru"].lower())}</dd><dt>Publisher</dt><dd>{b["place"]}: {esc(b["publisher"])} ({esc(b["publisher_ru"])}), {b["year"]}</dd><dt>Extent</dt><dd>{b["pages"]} pages</dd>{isbn}<dt>UDC · BBK</dt><dd>{b["udc"]} · {b["bbk"]}</dd><dt>Original language</dt><dd>Russian</dd><dt>English edition</dt><dd>Published chapter by chapter on this site</dd></dl>
   {biblio_html(b)}
   <h2>Abstract</h2><p>{esc(b["abstract"])}</p>
   {pdf_note(b)}
   <p style="font-size:.85rem;color:var(--muted)">The author thanks the SUNLIGHT company for its assistance in the preparation of this book.</p>
  </div>
 </div>
</section>
<section class="section alt">
 <div class="wrap"><div class="section-head"><h2>Contents</h2></div>{toc_html(b, "")}</div>
</section>'''
    page(b["slug"] + "/index.html", f'{b["title"]}: {b["subtitle"]}', f'{b["title"]} by Nona Dmitrievna Dronova ({b["place"]}, {b["year"]}). ' + b["abstract"][:110].rsplit(" ", 1)[0] + "… English edition.",
         body, cur="library.html", og_image=b["cover"] or "/images/jade-bat.jpg", og_type="book", crumbs=[("Library", "library.html"), (b["title"], b["slug"] + "/")],
         graph=[book_graph(b)])

def md_to_html(path):
    return subprocess.run(["pandoc", path, "-f", "markdown", "-t", "html5", "--wrap=none"],
                          capture_output=True, text=True, check=True).stdout

def build_chapters(b):
    chs = b["chapters"]
    avail = [c for c in chs if available(b, c[0])]
    for n, t, o, s_ in avail:
        h = md_to_html(chapter_file(b, n))
        h = re.sub(r"<h1[^>]*>.*?</h1>", "", h, count=1, flags=re.S)
        side = "".join(
            f'<li class="{"cur" if c[0] == n else ("off" if not available(b, c[0]) else "")}">' +
            (f'<a href="{c[3]}.html">{"" if c[0] == 0 else str(c[0]) + ". "}{esc(c[1])}</a>' if available(b, c[0]) else f'{"" if c[0] == 0 else str(c[0]) + ". "}{esc(c[1])}') + '</li>' for c in chs)
        i = [c[0] for c in avail].index(n)
        prev = avail[i - 1] if i > 0 else None
        nxt = avail[i + 1] if i + 1 < len(avail) else None
        nav = '<div class="chapter-nav">' + (f'<a href="{prev[3]}.html">← {esc(prev[1])}</a>' if prev else '<a href="./">← Contents</a>') + \
              (f'<a href="{nxt[3]}.html">{esc(nxt[1])} →</a>' if nxt else '<a href="./">Contents →</a>') + '</div>'
        isbn = f' ISBN {b["isbn"]}.' if b["isbn"] else ""
        body = f'''<div class="wrap reader">
 <aside><h4>{esc(b["title"])}</h4><ol>{side}</ol><p style="margin-top:16px"><a href="./">About the book</a></p><p style="margin-top:14px"><a class="btn btn-small" href="/index.html">← Back to Home</a></p></aside>
 <article class="prose">
  <div class="crumbs"><a href="/index.html">Home</a> / <a href="/library.html">Library</a> / <a href="./">{esc(b["title"])}</a> / {label(n)}</div>
  <span class="eyebrow">{label(n)}</span>
  <h1>{esc(t)}</h1>
  <p style="font-family:var(--serif);font-style:italic;color:var(--muted);margin-top:-.6em">{esc(o)}</p>
  <p class="byline">Author: Nona Dmitrievna Dronova</p>
  {h}
  <p style="font-size:.85rem;color:var(--muted);margin-top:32px">From: Dronova, Nona Dmitrievna. <em>{esc(b["orig"])}</em> [<em>{esc(b["title"])}</em>]: {esc(b["kind"].lower())}. {b["place"]}: {esc(b["publisher"])}, {b["year"]}. {b["pages"]} pp. ISBN {b["isbn"]}. English translation. The original Russian edition is available as a PDF via <a href="https://doi.org/{b["pdf"]["doi"]}" target="_blank" rel="noopener">doi:{b["pdf"]["doi"]}</a>.</p>
  {nav}
 </article>
</div>'''
        words = len(re.sub("<[^>]+>", " ", h).split())
        url = BASE + "/" + b["slug"] + "/" + s_ + ".html"
        g = [{"@type": "Chapter", "@id": url + "#chapter", "name": t, "alternateName": o, "position": n, "url": url,
              "inLanguage": "en", "wordCount": words, "author": {"@id": PERSON_ID},
              "isPartOf": {"@id": BASE + "/" + b["slug"] + "/#book"}}]
        first = re.sub("<[^>]+>", "", re.search(r"<p>(.*?)</p>", h, re.S).group(1))
        desc = f"{label(n)} of “{b['title']}” by Nona Dmitrievna Dronova. " + (first[:150].rsplit(" ", 1)[0] + "…")
        page(f'{b["slug"]}/{s_}.html', f"{t} — {label(n)}" if n else f"{t} — {b['title']}", desc, body, cur="library.html", og_image=b["cover"] or "/images/jade-bat.jpg", og_type="article",
             crumbs=[("Library", "library.html"), (b["title"], b["slug"] + "/"), (t, f'{b["slug"]}/{s_}.html')], graph=g)

def build_author():
    bio = md_to_html(os.path.join(ROOT, "tools", "content", "author.md"))
    toc_items = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', bio)
    toc = "".join(f'<li><a href="#{i}">{t}</a></li>' for i, t in toc_items)
    body = head_band("Professor Nona Dmitrievna Dronova", "Doctor of Technical Sciences · Ph.D. in Geology and Mineralogy · Professor · Gemmologist, researcher and artist", crumbs=[("About the Author", "author.html")], eyebrow="About the author") + f'''
<section class="section">
 <div class="wrap split cover-split">
  <img src="/images/nona-dronova.jpg" alt="Professor Nona Dmitrievna Dronova" width="380" height="500">
  <div class="prose">
   <dl class="facts">
    <dt>Full name</dt><dd>Nona Dmitrievna Dronova (Дронова Нона Дмитриевна)</dd>
    <dt>Degrees</dt><dd>Doctor of Technical Sciences; Ph.D. (Candidate of Sciences) in Geology and Mineralogy; Professor</dd>
    <dt>Positions</dt><dd>Chair of the Collegium of Expert Gemmologists of the Russian Federation; Scientific Director of the Global Diagnostic Atlas of Ancient Chinese Ceramics and of the Atlas of Ancient Chinese Jade and Bronze</dd>
    <dt>Experience</dt><dd>More than forty years of gemmological practice</dd>
    <dt>Publications</dt><dd>More than 79 scientific and methodological works including eight monographs; more than 280 open-access articles with DOI</dd>
    <dt>Methods</dt><dd>Gemmological optical microscopy (GOM) · BEINOS · DEE · SDE · LIE · PLIC · STA · TETA</dd>
    <dt>Art</dt><dd>Painter and art theorist; Member of the Union of Artists of Russia since 2002</dd>
    <dt>ORCID</dt><dd><a href="{ORCID}" target="_blank" rel="noopener">0009-0007-4867-9074</a></dd>
   </dl>
   <h3>On this page</h3>
   <ul class="mini-toc">{toc}</ul>
  </div>
 </div>
</section>
<section class="section alt"><div class="wrap prose author-bio">
 {bio}
 <h2>In this library</h2>
 <ul>
  <li><a href="/{PORCELAIN["slug"]}/">{esc(PORCELAIN["title"])}</a> ({PORCELAIN["year"]})</li>
  <li><a href="/{JADE["slug"]}/">{esc(JADE["title"])}</a> ({JADE["year"]})</li>
  <li><a href="/literature.html">Scientific articles</a> · <a href="/publications.html">Zenodo publications</a></li>
 </ul>
 <h2>Other projects</h2>
 <ul>
  <li><a href="{ATLAS}" target="_blank" rel="noopener">Global Diagnostic Atlas of Ancient Chinese Ceramics</a></li>
  <li><a href="{ATLAS_JB}" target="_blank" rel="noopener">Global Diagnostic Atlas of Ancient Chinese Jade and Bronze</a></li>
  <li><a href="{STUDIO}" target="_blank" rel="noopener">Nona Dronova Art Studio</a> — painting, textile art and jewellery</li>
 </ul>
</div></section>'''
    p = dict(PERSON); p["image"] = BASE + "/images/nona-dronova.jpg"
    page("author.html", "About the Author — Professor Nona Dmitrievna Dronova",
         "Professor Nona Dmitrievna Dronova: Doctor of Technical Sciences, Ph.D. in Geology and Mineralogy, gemmologist. Her methods for the non-destructive authentication of Chinese porcelain, jade and bronze: BEINOS, DEE, LIE, PLIC, STA and TETA.",
         body, cur="author.html", og_image="/images/nona-dronova.jpg", og_type="profile", crumbs=[("About the Author", "author.html")],
         graph=[{"@type": "ProfilePage", "url": BASE + "/author.html", "mainEntity": {"@id": PERSON_ID}}, p])

def build_about():
    body = head_band("About the Project", "A scientific digital library on the attribution and authentication of Chinese antiques.", crumbs=[("About the Project", "about.html")], eyebrow="Purpose") + f'''
<section class="section"><div class="wrap prose">
 <h2 style="margin-top:0">Purpose</h2>
 <p><strong>Chinese Antiques — Scientific Library of Research and Attribution</strong> brings together, in English, the monographs, research papers and reference materials of Professor Nona Dmitrievna Dronova on Chinese porcelain, jade and bronze.</p>
 <p>The aim is to make the methods of expert attribution transparent and verifiable: to show not only the conclusions, but the evidence on which they rest and the limits of that evidence.</p>
 <h2>Structure</h2>
 <ul>
  <li><strong>Library</strong> — the author's own works: monographs, articles and reference books.</li>
  <li><strong>Diagnostic Atlas</strong> — documented reference objects with their diagnostic features.</li>
  <li><strong>Scientific literature</strong> — the complete list of the author’s scientific articles, grouped by dynasty.</li>
  <li><strong>Zenodo publications</strong> — selected methodological papers and the Zenodo records of the monographs.</li>
 </ul>
 <h2>Language</h2>
 <p>The monographs were written and published in Russian. The English edition is prepared chapter by chapter; each chapter page gives the original Russian title. Terms of Chinese origin are given in pinyin, with Chinese characters where they help identification.</p>
 <div class="note">Information on this site is provided for scientific and educational purposes. It does not constitute an authentication or valuation of any particular object.</div>
</div></section>'''
    page("about.html", "About the Project", "Purpose and structure of the Chinese Antiques scientific library: monographs, diagnostic atlas, literature and open-access publications on Chinese porcelain, jade and bronze.",
         body, crumbs=[("About the Project", "about.html")], graph=[{"@type": "AboutPage", "url": BASE + "/about.html", "name": "About the Project"}])

def build_literature():
    por = json.load(open(os.path.join(ROOT, "tools", "content", "zenodo_publications.json"), encoding="utf-8"))
    jad = json.load(open(os.path.join(ROOT, "tools", "content", "zenodo_jade_bronze.json"), encoding="utf-8"))
    jad = [{"id": "jade-" + re.sub(r"[^a-z]+", "-", g["title"].lower()).strip("-"), "title": g["title"].replace(" Reference Objects", ""),
            "span": "", "items": [i for i in g["items"] if "Reference Book" not in i["title"]]} for g in jad]
    jad = [g for g in jad if g["items"]]
    short = lambda t: t.replace("Qing Dynasty — ", "").replace(" Period", "").replace(" Dynasty", "")
    arts = []
    def render(groups):
        out = []
        for g in groups:
            lis = []
            for it in sorted(g["items"], key=lambda x: (x["year"], x["title"])):
                doi = it["url"].split("doi.org/")[-1].lower()
                repo = "Zenodo" if "zenodo" in doi else "Figshare"
                obj = (" · Atlas object " + ", ".join(it["objects"])) if it.get("objects") else ""
                lis.append(f'<li><div class="pt"><a href="{esc(it["url"])}" target="_blank" rel="noopener">{esc(it["title"])}</a></div>'
                           f'<div class="pm">Dronova, Nona Dmitrievna · {esc(it["year"])} · {repo} · doi:{esc(doi)}{esc(obj)}</div></li>')
                arts.append({"@type": "ScholarlyArticle", "name": it["title"], "datePublished": it["year"], "url": it["url"], "author": {"@id": PERSON_ID}})
            span = f'{esc(g["span"])} · ' if g["span"] else ""
            out.append(f'<h3 id="{g["id"]}">{esc(g["title"])} <small style="font-family:var(--sans);font-size:.85rem;color:var(--muted)">{span}{len(g["items"])}</small></h3><ul class="pubs">{"".join(lis)}</ul>')
        return "".join(out)
    np_, nj = sum(len(g["items"]) for g in por), sum(len(g["items"]) for g in jad)
    jump = lambda groups: " ".join(f'<a class="tag" href="#{g["id"]}">{esc(short(g["title"]))}</a>' for g in groups)
    por_html, jad_html = render(por), render(jad)
    total = np_ + nj
    body = head_band("Scientific Literature", f"The scientific articles of Professor Nona Dmitrievna Dronova: {total} open-access publications with DOI on the authentication of ancient Chinese porcelain, jade and bronze.",
                     crumbs=[("Scientific Literature", "literature.html")], eyebrow="Author’s scientific articles") + f'''
<section class="section"><div class="wrap prose" style="max-width:900px">
 <p>All articles are published in open access (CC BY 4.0), most of them in the Zenodo community <em>Global Archive for Authentication of Antique Porcelain</em>, each with a permanent DOI. The lists follow the publication indexes of the <a href="{ATLAS}publications.html" target="_blank" rel="noopener">Diagnostic Atlas of Chinese Porcelain</a> and the <a href="{ATLAS_JB}publications.html" target="_blank" rel="noopener">Atlas of Ancient Jade and Bronze</a>.</p>
 <p style="display:flex;flex-wrap:wrap;gap:6px"><a class="tag" href="#porcelain">Porcelain · {np_}</a> <a class="tag" href="#jade">Jade &amp; bronze · {nj}</a></p>
 <h2 id="porcelain">Porcelain</h2>
 <p style="display:flex;flex-wrap:wrap;gap:6px">{jump(por)}</p>
 {por_html}
 <h2 id="jade">Jade and bronze</h2>
 <p style="display:flex;flex-wrap:wrap;gap:6px">{jump(jad)}</p>
 {jad_html}
</div></section>'''
    page("literature.html", "Scientific Literature — Articles by Nona Dmitrievna Dronova", f"{total} open-access scientific articles by Professor Nona Dmitrievna Dronova on the authentication of ancient Chinese porcelain, jade and bronze, with DOI.",
         body, crumbs=[("Scientific Literature", "literature.html")],
         graph=[{"@type": "CollectionPage", "url": BASE + "/literature.html", "name": "Scientific Literature", "author": {"@id": PERSON_ID},
                 "mainEntity": {"@type": "ItemList", "numberOfItems": total,
                                "itemListElement": [{"@type": "ListItem", "position": k + 1, "item": a} for k, a in enumerate(arts)]}}])

def build_publications():
    pubs = [
        ("Methodological Foundations of Genetic Analysis in Authenticity Diagnostics of Ancient Chinese Porcelain (New Approaches by Prof. Nona Dmitrievna Dronova)", "2025", "16755260"),
        ("The Dry Earth Effect (DEE) and Optical Depth in Ru Yao Glaze: A New Diagnostic Framework", "2025", "16724189"),
        ("Scientific Diagnostic Framework for Authenticating Ancient Chinese Porcelain", "2026", "21081327"),
        ("Optical Microstructural Diagnostics of Chinese Porcelain Glazes: Six Criteria for Distinguishing Authentic Song–Yuan Production from Modern Reproduction", "2026", "21196249"),
        ("Gemological Optical Microscopy as a Non-Destructive Diagnostic Method for Authenticating Ru Yao Ceramics of the Northern Song Dynasty", "2026", "20777296"),
    ]
    li = "".join(f'<li><div class="pt">{esc(t)}</div><div class="pm">Nona Dmitrievna Dronova · {y} · <a href="https://doi.org/10.5281/zenodo.{d}" target="_blank" rel="noopener">doi:10.5281/zenodo.{d}</a></div></li>' for t, y, d in pubs)
    body = head_band("Zenodo Publications", "Open-access scientific papers by Professor Nona Dmitrievna Dronova, each archived on Zenodo with a permanent DOI.",
                     crumbs=[("Zenodo Publications", "publications.html")], eyebrow="Open access") + f'''
<section class="section"><div class="wrap prose">
 <p>Several hundred records are published in the Zenodo community <em>Global Archive for Authentication of Antique Porcelain</em> (CC BY 4.0). The complete index, grouped by dynasty and linked to the reference objects, is maintained in the Atlas.</p>
 <p><a class="btn btn-gold" href="{ATLAS}publications.html" target="_blank" rel="noopener">Full index of publications ↗</a> <a class="btn" href="{ORCID}" target="_blank" rel="noopener">ORCID profile ↗</a></p>
 <h2>Selected methodological papers</h2>
 <ul class="pubs">{li}</ul>
 <h2>Monographs on Zenodo</h2>
 <p>The complete original Russian editions of both monographs are attached as PDF files to these open-access articles:</p>
 <ul class="pubs">{"".join(f'<li><div class="pt"><a href="https://doi.org/{b["pdf"]["doi"]}" target="_blank" rel="noopener">{esc(b["pdf"]["title"])}</a></div><div class="pm">Nona Dmitrievna Dronova · Zenodo, {b["pdf"]["date"]} · doi:{b["pdf"]["doi"]} · includes the PDF of the {b["year"]} edition · <a href="/{b["slug"]}/">English edition on this site</a></div></li>' for b in BOOKS)}</ul>
 <p>Earlier Zenodo records of the monographs:</p>
 <ul class="pubs">{"".join(f'<li><div class="pt"><a href="https://doi.org/{b["doi"]}" target="_blank" rel="noopener">{esc(b["title"])}: {esc(b["subtitle"])}</a></div><div class="pm">Nona Dmitrievna Dronova · original edition {b["place"]}, {b["year"]} · doi:{b["doi"]} · <a href="/{b["slug"]}/">English edition on this site</a></div></li>' for b in BOOKS)}</ul>
 <p><a href="https://zenodo.org/search?q=metadata.creators.person_or_org.name:%22NONA,+Dronova%22" target="_blank" rel="noopener">All records by Nona Dmitrievna Dronova on Zenodo ↗</a> · <a href="/literature.html">Complete list of articles on this site</a></p>
</div></section>'''
    page("publications.html", "Zenodo Publications — Open-Access Research with DOI", "Open-access scientific publications by Professor Nona Dmitrievna Dronova on the authentication of Chinese porcelain, archived on Zenodo with DOI.",
         body, crumbs=[("Zenodo Publications", "publications.html")],
         graph=[{"@type": "CollectionPage", "url": BASE + "/publications.html", "name": "Zenodo Publications",
                 "hasPart": [{"@type": "ScholarlyArticle", "name": t, "datePublished": y, "url": f"https://doi.org/10.5281/zenodo.{d}", "author": {"@id": PERSON_ID}} for t, y, d in pubs]}])

def build_404():
    body = head_band("Page not found", 'The page you are looking for does not exist. <a href="/index.html">Return to the home page</a>.')
    page("404.html", "Page not found", "Page not found.", body)
    PAGES.remove("404.html")

def build_seo():
    prio = {"index.html": "1.0", "library.html": "0.9", "porcelain.html": "0.9", "atlas.html": "0.9"}
    urls = []
    for p in PAGES:
        loc = BASE + "/" + ("" if p == "index.html" else p.replace("index.html", ""))
        urls.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><priority>{prio.get(p, '0.7')}</priority></url>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
    open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {BASE}/sitemap.xml\n")

if __name__ == "__main__":
    build_home(); build_porcelain(); build_jade_bronze(); build_atlas(); build_library()
    [ (build_book(b), build_chapters(b)) for b in BOOKS ]; build_author(); build_about()
    build_literature(); build_publications(); build_404(); build_seo()
    print("\n".join(PAGES))
