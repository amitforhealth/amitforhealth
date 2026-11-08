import re, glob, os, yaml, markdown, html, datetime, shutil, json

ROOT = os.path.dirname(os.path.abspath(__file__))
POSTS = f"{ROOT}/posts"
OUT = f"{ROOT}/site"
SITE_URL = "https://amitforhealth.in"

SECTIONS = [
    ("asthma", "Asthma in India", "Why a controllable disease kills so many Indians, and where the gap opens.",
     ["the-breath-india-keeps-losing", "the-inhaler-nobody-picks-up", "the-long-wait-to-say-asthma",
      "gasping-for-relief", "the-united-airway", "the-right-to-inhalation", "every-breath-matters"]),
    ("medicines", "Medicines we misuse", "Relievers sold as treatment, tablets sold as controllers, and the inhaler left on the shelf.",
     ["the-wrong-best-seller", "montelukast-friend-or-enemy", "nebuliser-in-every-home",
      "zoya-deserves-ice-cream", "expensive-air"]),
    ("business", "The business of respiratory care", "What twenty-six years inside Indian pharma taught me about why this market keeps failing patients.",
     ["deep-pockets-shallow-breaths", "the-sales-model-nobody-changed", "the-ethics-of-influence"]),
    ("doctors", "When doctors are attacked", "A three-part series on violence against India's doctors, and who really pays for it.",
     ["the-wages-of-fear", "the-poster-will-not-save-you", "the-man-who-beat-his-own-hospital"]),
]
START_HERE = "the-breath-india-keeps-losing"
COL = {}
_i = 0
for _sec in SECTIONS:
    for _s in _sec[3]:
        COL[_s] = _i % 5; _i += 1
LINKEDIN = "https://www.linkedin.com/in/amitforhealth"
BUTTONDOWN = "amitforhealth"


def subscribe_box(idsuffix=""):
    return f'''<section class="subscribe col3" id="subscribe{idsuffix}">
<h2>Get the monthly email</h2>
<p>One email a month with new essays and field reports from Indian healthcare. No spam; unsubscribe any time.</p>
<form action="https://buttondown.com/api/emails/embed-subscribe/{BUTTONDOWN}" method="post" class="sub-form">
<label for="bd-email{idsuffix}" class="sr">Email address</label>
<input type="email" name="email" id="bd-email{idsuffix}" placeholder="you@example.com" required autocomplete="email">
<input type="hidden" value="1" name="embed">
<button type="submit">Subscribe</button>
</form>
<p class="sub-note">Prefer a feed reader? <a href="/feed.xml">RSS</a></p>
</section>'''

BAYU = "https://www.bayuhealthcare.com"


def load():
    posts = {}
    for f in glob.glob(f"{POSTS}/*.md"):
        raw = open(f).read()
        _, fm, body = raw.split("---", 2)
        meta = yaml.safe_load(fm)
        meta["body_md"] = body.strip()
        meta["words"] = len(re.findall(r"\w+", body))
        meta["minutes"] = max(1, round(meta["words"] / 230))
        d = meta["date"]
        if isinstance(d, str):
            d = datetime.date.fromisoformat(d)
        meta["date"] = d
        meta["date_label"] = d.strftime("%B %Y")
        posts[meta["slug"]] = meta
    return posts


def render_body(md_text, link):
    # split off sources section
    m = re.search(r"(?m)^## (Sources?\b.*)$", md_text)
    main, sources = (md_text[: m.start()], md_text[m.start():]) if m else (md_text, "")
    # internal links: (slug) -> link(slug)
    def fix(t):
        return re.sub(r"\]\(([a-z0-9-]+)\)", lambda mm: f"]({link(mm.group(1))})", t)
    ext = ["tables", "sane_lists", "smarty"]
    h = markdown.markdown(fix(main), extensions=ext)
    if sources:
        s = markdown.markdown(fix(sources), extensions=ext)
        s = re.sub(r"<a href=\"http", "<a rel=\"noopener\" href=\"http", s)
        h += f'<aside class="sources">{s}</aside>'
    h = re.sub(r"<table>", '<div class="table-wrap"><table>', h).replace("</table>", "</table></div>")
    # strip the dateline bold for Gasping
    return h


def esc(s):
    return html.escape(str(s), quote=True)


CSS = open(f"{ROOT}/assets/style.css").read()
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Lora:ital,wght@0,400;0,600;1,400&family=Lato:wght@400;700&display=swap">'


def index_html(posts, link):
    sh = posts[START_HERE]
    parts = []
    parts.append(f'''<header class="top"><a href="#subscribe">subscribe</a> · <a href="{link('feed')}">rss</a> · <a href="{LINKEDIN}" rel="noopener">linkedin</a></header>
<section class="hero">
<h1>Every breath is a right.</h1>
<p>Personal site and notebook of <a href="{link('#about')}">Amit Kumar</a>. Twenty-six years in Indian respiratory medicine, ten of them at Cipla and sixteen building <a href="{BAYU}" rel="noopener">Bayu Healthcare</a>.</p>
<p>Currently writing about why India loses so many people to diseases we already know how to control, and building <strong>#RTI, the Right to Inhalation</strong>: <em>Saans Ka Adhikaar</em>.</p>
</section>
<section class="start">
<h2>Start here</h2>
<a class="feature col{COL[START_HERE]}" href="{link(sh['slug'])}"><span class="feature-title">{esc(sh['title'])}</span><span class="feature-dek">{esc(sh['dek'])}</span></a>
</section>
<section class="essays"><h2>Essays</h2>''')
    for key, name, blurb, slugs in SECTIONS:
        items = "".join(
            f'<li class="col{COL[s]}"><a href="{link(s)}">{esc(posts[s]["title"])}</a></li>' for s in slugs)
        parts.append(f'<div class="group" id="{key}"><h3>{esc(name)}</h3><p class="blurb">{esc(blurb)}</p><ul>{items}</ul></div>')
    total = sum(len(s[3]) for s in SECTIONS)
    parts.append(f'<p class="count">{total} essays, written for doctors, pharma leaders, policymakers and anyone who has watched a family member struggle to breathe.</p></section>')
    parts.append(subscribe_box())
    parts.append(f'''<section class="about col1" id="about">
<h2>About</h2>
<p>I'm Amit Kumar, co-founder and director of Bayu Healthcare, a respiratory-focused pharmaceutical company based in Lucknow and working across Uttar Pradesh, Bihar, Jharkhand and Madhya Pradesh. Before Bayu I spent a formative decade at Cipla, helping build its respiratory division.</p>
<p>This site is about a question I can't stop asking. In a country where tens of millions of people live with asthma, COPD and allergic airway disease, why is inhalation therapy still treated as a last resort instead of a first-line right? <strong>#RTI, the Right to Inhalation</strong>, is my attempt at an answer, built in conversation with chest physicians, paediatricians, ENT specialists and the field teams who meet patients every day.</p>
<p>I write about the parts of this business I have spent a career inside, including the parts the industry would prefer stayed in the drawer. I name dysfunctions, not individuals, and I lean on evidence wherever it exists. If you think I'm wrong, or you have a field story I can't see from where I stand, <a href="{LINKEDIN}" rel="noopener">write to me on LinkedIn</a>.</p>
<p class="small">MBA, P.I.M.R. Indore · Executive education, IIM Ahmedabad</p>
</section>
<footer class="foot">© {datetime.date.today().year} Amit Kumar · AmitForHealth · <a href="{link('feed')}">rss</a><br>Personal views, not those of Bayu Healthcare. Nothing on this site is medical advice; please talk to your doctor.</footer>''')
    return "\n".join(parts)


def post_html(posts, slug, link, order):
    p = posts[slug]
    sec = next(s for s in SECTIONS if slug in s[3])
    i = sec[3].index(slug)
    nxt = sec[3][i + 1] if i + 1 < len(sec[3]) else None
    prv = sec[3][i - 1] if i > 0 else None
    nav = ""
    if prv or nxt:
        nav = '<nav class="pn">'
        nav += f'<a class="prev" href="{link(prv)}"><span>Previous</span>{esc(posts[prv]["title"])}</a>' if prv else "<span></span>"
        nav += f'<a class="next" href="{link(nxt)}"><span>Next in {esc(sec[1])}</span>{esc(posts[nxt]["title"])}</a>' if nxt else "<span></span>"
        nav += "</nav>"
    return f'''<header class="top"><a href="{link('')}">← Amit Kumar</a> · <a href="#subscribe">subscribe</a></header>
<article class="post col{COL[slug]}">
<p class="kicker"><a href="{link('#' + sec[0])}">{esc(sec[1])}</a></p>
<h1>{esc(p['title'])}</h1>
<p class="dek">{esc(p['dek'])}</p>
<p class="meta">{p['date_label']} · {p['minutes']} min read</p>
<div class="body">{render_body(p['body_md'], link)}</div>
</article>
<section class="signoff"><p><strong>Amit Kumar</strong> is co-founder of Bayu Healthcare and has spent twenty-six years in Indian respiratory medicine. Disagree, or have a field story to share? <a href="{LINKEDIN}" rel="noopener">Write to me on LinkedIn</a>.</p></section>
{subscribe_box()}
{nav}
<footer class="foot"><a href="{link('')}">All essays</a> · © {datetime.date.today().year} Amit Kumar<br>Personal views, not those of Bayu Healthcare. Nothing on this site is medical advice; please talk to your doctor.</footer>'''


FAVICON = "data:image/svg+xml," + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect x='3' y='4' width='5' height='24' fill='%23112f41'/%3E%3Crect x='10' y='8' width='5' height='20' fill='%23b58427'/%3E%3Crect x='17' y='12' width='5' height='16' fill='%2347ab6c'/%3E%3Crect x='24' y='6' width='5' height='22' fill='%23ed553b'/%3E%3C/svg%3E"


FEED_XSL = open(os.path.join(ROOT, "assets", "feed.xsl")).read()


def build_static(posts):
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(f"{OUT}/essays")
    open(f"{OUT}/style.css", "w").write(CSS)

    def link(target):
        if target == "":
            return "/"
        if target == "feed":
            return "/feed.xml"
        if target.startswith("#"):
            return "/" + target
        return f"/essays/{target}"

    def page(title, desc, body, path, kind="website"):
        url = SITE_URL + path
        return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}"><link rel="icon" href="{FAVICON}">
<link rel="alternate" type="application/rss+xml" title="AmitForHealth" href="/feed.xml">
<meta property="og:type" content="{kind}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:site_name" content="AmitForHealth"><meta name="twitter:card" content="summary">
<meta name="author" content="Amit Kumar">
{FONTS}<link rel="stylesheet" href="/style.css"></head>
<body><main class="wrap">{body}</main></body></html>'''

    open(f"{OUT}/index.html", "w").write(page("Amit Kumar · AmitForHealth",
        "Personal site and notebook of Amit Kumar: essays on respiratory care, pharma sales, marketing and analytics in India.",
        index_html(posts, link), "/"))
    for s, p in posts.items():
        open(f"{OUT}/essays/{s}.html", "w").write(page(f"{p['title']} · Amit Kumar", p["dek"], post_html(posts, s, link, None), f"/essays/{s}", "article"))
    open(f"{OUT}/404.html", "w").write(page("Page not found · AmitForHealth", "Page not found",
        f'<header class="top"><a href="/">← Amit Kumar</a></header><article class="post col4"><h1>This page took a deep breath and vanished.</h1><p class="dek">The link may be old or mistyped.</p><p><a href="/">Go to all essays</a></p></article>', "/404"))
    # RSS
    items = sorted(posts.values(), key=lambda p: p["date"], reverse=True)
    def rfc(d): return datetime.datetime(d.year, d.month, d.day, 9, 0).strftime("%a, %d %b %Y %H:%M:%S +0530")
    rss = "".join(f"<item><title>{esc(p['title'])}</title><link>{SITE_URL}/essays/{p['slug']}</link><guid>{SITE_URL}/essays/{p['slug']}</guid><pubDate>{rfc(p['date'])}</pubDate><description>{esc(p['dek'])}</description></item>" for p in items)
    open(f"{OUT}/feed.xsl", "w").write(FEED_XSL)
    open(f"{OUT}/feed.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?><?xml-stylesheet type="text/xsl" href="/feed.xsl"?><rss version="2.0"><channel><title>AmitForHealth</title><link>{SITE_URL}/</link><description>Essays by Amit Kumar on respiratory care and the business of Indian pharma.</description><language>en-in</language>{rss}</channel></rss>')
    urls = [SITE_URL + "/"] + [f"{SITE_URL}/essays/{s}" for s in posts]
    open(f"{OUT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{u}</loc></url>" for u in urls) + "</urlset>")
    open(f"{OUT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")


def build_artifact(posts):
    def link(target):
        if target == "":
            return "#home"
        if target == "feed":
            return "#home"
        if target.startswith("#"):
            return target if target != "#about" else "#about"
        return f"#{target}"
    views = [f'<div class="view" data-view="home">{index_html(posts, link)}</div>']
    for s in posts:
        views.append(f'<div class="view" data-view="{s}" hidden>{post_html(posts, s, link, None)}</div>')
    sections = [s[0] for s in SECTIONS] + ["about"]
    js = """
const views=[...document.querySelectorAll('.view')];
const anchors=%s;
function route(){
  let h=(location.hash||'#home').slice(1);
  let target=h, anchor=null;
  if(anchors.includes(h)){target='home';anchor=h;}
  if(!views.some(v=>v.dataset.view===target)){target='home';}
  views.forEach(v=>v.hidden=v.dataset.view!==target);
  const t=views.find(v=>v.dataset.view===target).querySelector('h1');
  document.title = target==='home' ? 'AmitForHealth' : t.textContent+' · Amit Kumar';
  if(anchor){const el=document.getElementById(anchor); if(el){el.scrollIntoView();return;}}
  window.scrollTo(0,0);
}
addEventListener('hashchange',route); route();
""" % json.dumps(sections)
    doc = f'''<title>AmitForHealth</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}
<style>{CSS}</style>
<main class="wrap">{"".join(views)}</main>
<script>{js}</script>'''
    open(f"{ROOT}/preview.html", "w").write(doc)


posts = load()
missing = [s for sec in SECTIONS for s in sec[3] if s not in posts]
extra = [s for s in posts if not any(s in sec[3] for sec in SECTIONS)]
assert not missing and not extra, (missing, extra)
build_static(posts)
build_artifact(posts)
print(len(posts), "posts;", sum(p["words"] for p in posts.values()), "words")
