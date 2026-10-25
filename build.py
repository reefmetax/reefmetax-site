#!/usr/bin/env python3
"""Render reefmetax.com: reads data/news.json + live prices, writes index.html and btc-chart.svg."""
import html, json, re, sys, urllib.request, urllib.parse
from datetime import datetime, timezone, time as dtime
from email.utils import format_datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).parent
ET = ZoneInfo("America/New_York")
SITE = "https://reefmetax.com"
COINS = [("BTC", "bitcoin", "Bitcoin"), ("ETH", "ethereum", "Ethereum"), ("SOL", "solana", "Solana"),
         ("DOGE", "dogecoin", "Dogecoin"), ("PYTH", "pyth-network", "Pyth")]
CG = "https://api.coingecko.com/api/v3"
CACHE = ROOT / "data" / "prices_cache.json"
ARTICLES_DIR = ROOT / "data" / "articles"
AUTHOR = "Reef"
AUTHOR_ROLE = "Community Builder"
AUTHOR_URL = "https://x.com/Reefmetax"
AVATAR = "/assets/reef.jpg"
BIO = "Reef \u2014 Community Builder. Doginal Dogs and metax community."

COMMUNITY = [
    ("doginaldogs", "Doginal Dogs", "10,000 pixel dogs inscribed on $DOGE."),
    ("DDLTCG", "Legends TCG", "A premium trading card game by Doginal Dogs."),
    ("PythNetwork", "Pyth Network", "The price layer of the global financial market."),
    ("thePIRB", "PIRB", "Part of the pack."),
    ("barkmeta", "Bark", "Financial trends and commentary. Host of THE GREAT RESET."),
    ("Shieldmetax", "Shield", "Web3 builder. Events, marketing, experiences."),
    ("GodsBurnt", "Shibo", "Financial news and commentary. Host of the Finance Show."),
]


CSS = r""":root{--bg:#0b0f14;--panel:#111822;--line:#1e2a38;--text:#e8eef5;--muted:#8a9bb0;--orange:#ff8a3d;--teal:#2ee6c5;--up:#2ee6c5;--down:#ff6b5e}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;-webkit-font-smoothing:antialiased;
background-image:radial-gradient(900px 400px at 85% -10%,rgba(255,138,61,.14),transparent 60%),radial-gradient(700px 400px at -10% 10%,rgba(46,230,197,.10),transparent 60%);background-repeat:no-repeat}
a{color:inherit;text-decoration:none}
.wrap{max-width:1040px;margin:0 auto;padding:0 18px}
nav{position:sticky;top:0;z-index:5;backdrop-filter:blur(10px);background:rgba(11,15,20,.8);border-bottom:1px solid var(--line)}
nav .wrap{display:flex;gap:18px;align-items:center;height:52px;overflow-x:auto;white-space:nowrap;scrollbar-width:none}
nav b{color:var(--orange);margin-right:auto}
nav a{color:var(--muted);font-size:14px}
nav a:hover{color:var(--teal)}
.hero{padding:56px 0 40px}
.eyebrow{display:inline-block;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);border:1px solid rgba(46,230,197,.4);padding:4px 10px;border-radius:99px}
h1{font-size:clamp(44px,12vw,92px);line-height:1;margin:16px 0 8px;letter-spacing:-.03em}
h1 span{background:linear-gradient(90deg,var(--orange),var(--teal));-webkit-background-clip:text;background-clip:text;color:transparent}
.role{font-size:clamp(18px,4.5vw,24px);color:var(--text)}
.tag-line{color:var(--muted);max-width:560px;margin-top:10px}
.btns{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}
.btn{padding:13px 22px;border-radius:12px;font-weight:600;border:1px solid var(--line);background:var(--panel);min-height:48px;display:inline-flex;align-items:center}
.btn.primary{background:linear-gradient(90deg,var(--orange),#ffb07a);color:#1a1006;border:0}
.btn:hover{transform:translateY(-1px)}
section{padding:34px 0}
h2{font-size:26px;letter-spacing:-.01em;margin-bottom:6px}
h2::before{content:"";display:inline-block;width:8px;height:22px;background:var(--orange);border-radius:3px;margin-right:10px;vertical-align:-3px}
.sub{color:var(--muted);font-size:14px;margin-bottom:16px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:16px}
.grid{display:grid;gap:12px;grid-template-columns:1fr}
.story h3{font-size:17px;line-height:1.3;margin-bottom:6px}
.story p{color:#b9c6d6;font-size:15px}
.src{display:inline-block;margin-top:10px;color:var(--teal);font-size:14px;font-weight:600}
.tag{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:3px 9px;border-radius:99px;margin-bottom:8px;background:rgba(255,138,61,.15);color:var(--orange)}
.tag-pyth{background:rgba(46,230,197,.14);color:var(--teal)}
.tag-ddltcg{background:rgba(255,200,61,.14);color:#ffc83d}
.two{display:grid;gap:12px;grid-template-columns:1fr;margin-bottom:12px}
table{width:100%;border-collapse:collapse}
th{text-align:left;font-size:12px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.08em;padding-bottom:8px}
td{padding:10px 0;border-top:1px solid var(--line)}
.num{text-align:right;font-variant-numeric:tabular-nums}
th.num{text-align:right}
.up{color:var(--up)}.down{color:var(--down)}.flat,.muted{color:var(--muted)}
td .muted{font-size:13px;margin-left:4px}
.chart svg{width:100%;height:180px;display:block;margin-top:10px}
.chart-head{display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;font-size:14px}
.fine{font-size:12.5px;color:var(--muted);margin-top:10px}
.notes{margin-top:14px}
.comm{display:flex;flex-direction:column;gap:2px}
.comm b{color:var(--orange);font-size:17px}
.comm small{color:var(--muted)}
.comm:hover{border-color:var(--teal)}
footer{border-top:1px solid var(--line);margin-top:30px;padding:26px 0 44px;color:var(--muted);font-size:14px}
footer b{color:var(--text)}
@media(min-width:700px){.grid{grid-template-columns:1fr 1fr}.two{grid-template-columns:1fr 1.3fr}.hero{padding:90px 0 60px}}
@media(min-width:980px){.grid.three{grid-template-columns:1fr 1fr 1fr}.comm-grid{grid-template-columns:repeat(4,1fr)}}
.avatar{width:88px;height:88px;border-radius:50%;object-fit:cover;border:2px solid var(--orange);background:var(--panel);image-rendering:pixelated;flex:none}
.about{display:flex;gap:18px;align-items:center}
.about .avatar{width:96px;height:96px}
.about h3{font-size:19px;margin-bottom:4px}
.about p{color:#b9c6d6}
.about a.more{display:inline-block;margin-top:8px;color:var(--teal);font-weight:600;font-size:14px}
.art-card{display:flex;flex-direction:column;gap:6px}
.art-card:hover{border-color:var(--teal)}
.art-card h3{font-size:18px;line-height:1.3}
.art-card p{color:#b9c6d6;font-size:15px}
.meta{display:flex;align-items:center;gap:8px;color:var(--muted);font-size:13px;flex-wrap:wrap}
.meta .avatar{width:26px;height:26px;border-width:1px}
.more-link{display:inline-block;margin-top:14px;color:var(--teal);font-weight:600}
.article{max-width:720px;margin:0 auto;padding:36px 0 10px}
.back{display:inline-block;color:var(--teal);font-size:14px;font-weight:600;margin-bottom:22px}
.article h1{font-size:clamp(28px,6vw,42px);line-height:1.15;letter-spacing:-.02em;margin:0 0 16px}
.byline{display:flex;align-items:center;gap:12px;margin-bottom:26px;padding-bottom:20px;border-bottom:1px solid var(--line)}
.byline .avatar{width:48px;height:48px;border-width:1.5px}
.byline b{display:block}
.byline span{color:var(--muted);font-size:14px}
.prose p,.prose li{font-size:17.5px;line-height:1.7;color:#d3dde9}
.prose p{margin:0 0 18px}
.prose h2{font-size:23px;margin:34px 0 10px}
.prose h2::before{display:none}
.prose ul{margin:0 0 18px 22px}
.prose li{margin-bottom:8px}
.prose a{color:var(--teal);text-decoration:underline;text-underline-offset:3px}
.prose strong{color:var(--text)}
.disclaimer{margin:30px 0 0;padding:14px 16px;border:1px solid var(--line);border-left:3px solid var(--orange);border-radius:10px;background:var(--panel);color:var(--muted);font-size:14px}
.sources li{font-size:15px}
.art-list{display:grid;gap:12px;grid-template-columns:1fr}
.page-head{padding:44px 0 8px}
.page-head h1{font-size:clamp(34px,8vw,56px);margin:0 0 8px}
@media(min-width:700px){.art-list{grid-template-columns:1fr 1fr}}
.news{background:linear-gradient(135deg,rgba(255,138,61,.12),rgba(46,230,197,.08)),var(--panel);border:1px solid var(--line);border-radius:16px;padding:22px 18px}
.news h2{font-size:24px;margin-bottom:6px}
.news p{color:#b9c6d6;font-size:15px;margin-bottom:14px}
.news form{display:flex;flex-direction:column;gap:10px}
.news label{font-size:13px;color:var(--muted);font-weight:600}
.news input[type=email]{width:100%;min-height:48px;padding:12px 14px;border-radius:12px;border:1px solid var(--line);background:var(--bg);color:var(--text);font:inherit;font-size:16px}
.news input[type=email]:focus{outline:2px solid var(--teal);outline-offset:1px;border-color:var(--teal)}
.news input[type=submit]{min-height:48px;padding:12px 22px;border:0;border-radius:12px;background:linear-gradient(90deg,var(--orange),#ffb07a);color:#1a1006;font:inherit;font-weight:700;font-size:16px;cursor:pointer}
.news input[type=submit]:hover{transform:translateY(-1px)}
.news .fine{margin-top:10px}
.news.in-article{margin:34px 0 0}
@media(min-width:700px){.news form{flex-direction:row;flex-wrap:wrap;align-items:flex-end}.news form label{flex:0 0 100%}.news input[type=email]{flex:1 1 260px;width:auto}}
"""


def fetch_json(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "reefmetax-site-builder/1.0", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def get_prices():
    """Live prices from CoinGecko; fall back to last-known cache. Returns (prices, spark, live_ok)."""
    ids = ",".join(c[1] for c in COINS)
    try:
        q = urllib.parse.urlencode({"ids": ids, "vs_currencies": "usd", "include_24hr_change": "true"})
        data = fetch_json(f"{CG}/simple/price?{q}")
        prices = {c[0]: {"usd": data[c[1]]["usd"], "chg": data[c[1]].get("usd_24h_change")} for c in COINS}
        spark = None
        try:
            ch = fetch_json(f"{CG}/coins/bitcoin/market_chart?vs_currency=usd&days=7")
            pts = [p[1] for p in ch["prices"]]
            step = max(1, len(pts) // 84)
            spark = pts[::step] + ([pts[-1]] if (len(pts) - 1) % step else [])
        except Exception as e:
            print("chart fetch failed:", e, file=sys.stderr)
        stamp = datetime.now(timezone.utc).isoformat()
        old = json.loads(CACHE.read_text()) if CACHE.exists() else {}
        CACHE.write_text(json.dumps({"fetched_at": stamp, "prices": prices, "spark": spark or old.get("spark")}))
        return prices, spark or old.get("spark"), stamp, True
    except Exception as e:
        print("live prices failed, using cache:", e, file=sys.stderr)
        if CACHE.exists():
            c = json.loads(CACHE.read_text())
            return c["prices"], c.get("spark"), c["fetched_at"], False
        return None, None, None, False


def fmt_price(sym, v):
    if v is None:
        return "n/a"
    if v >= 1000:
        return f"${v:,.0f}"
    if v >= 1:
        return f"${v:,.2f}"
    return f"${v:,.4f}"


def sparkline_svg(pts, w=640, h=180, standalone=False):
    if not pts or len(pts) < 2:
        return "", 0, 0
    lo, hi = min(pts), max(pts)
    pad = 10
    rng = (hi - lo) or 1
    xy = [(pad + i * (w - 2 * pad) / (len(pts) - 1), pad + (hi - v) * (h - 2 * pad) / rng) for i, v in enumerate(pts)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in xy)
    area = f"{xy[0][0]:.1f},{h} " + line + f" {xy[-1][0]:.1f},{h}"
    up = pts[-1] >= pts[0]
    col = "#2ee6c5" if up else "#ff8a3d"
    ns = ' xmlns="http://www.w3.org/2000/svg"' if standalone else ""
    bg = f'<rect width="{w}" height="{h}" fill="#0f1620"/>' if standalone else ""
    return (f'<svg{ns} viewBox="0 0 {w} {h}" preserveAspectRatio="none" role="img" aria-label="Bitcoin price, last 7 days">'
            f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col}" stop-opacity=".35"/>'
            f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient></defs>{bg}'
            f'<polygon points="{area}" fill="url(#g)"/>'
            f'<polyline points="{line}" fill="none" stroke="{col}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<circle cx="{xy[-1][0]:.1f}" cy="{xy[-1][1]:.1f}" r="4" fill="{col}"/></svg>'), lo, hi


GOATCOUNTER = '<script data-goatcounter="https://reefmetax.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>'


NEWSLETTER_URL = "https://buttondown.com/reefmetax"
NEWSLETTER_FORM = (
    '<form action="https://buttondown.com/api/emails/embed-subscribe/reefmetax" method="post" target="popupwindow" '
    'onsubmit="window.open(\'https://buttondown.com/reefmetax\', \'popupwindow\')" class="newsletter-form">'
    '<label for="bd-email">Enter your email</label> '
    '<input type="email" name="email" id="bd-email" required autocomplete="email" /> '
    '<input type="submit" value="Subscribe" /></form>')


def newsletter_block(extra_class=""):
    cls = ("news " + extra_class).strip()
    return (f'<div class="{cls}"><h2>Join the pack</h2>'
            f"<p><b>Reef's Pack Report</b>: Weekly Doginal Dogs, DDLTCG and crypto news from Reef. No spam.</p>"
            f'{NEWSLETTER_FORM}</div>')


def e(s):
    return html.escape(str(s), quote=True)


def safe_url(u):
    return u if str(u).startswith(("https://x.com/", "https://twitter.com/", "https://reefmetax.com")) else "#"


def story_card(it, tag=None):
    t = f'<span class="tag tag-{e(tag.lower().replace(" ", "-"))}">{e(tag)}</span>' if tag else ""
    return (f'<article class="card story">{t}<h3>{e(it["title"])}</h3><p>{e(it["summary"])}</p>'
            f'<a class="src" href="{e(safe_url(it["url"]))}" target="_blank" rel="noopener">{e(it.get("source", "Source"))} on X &rarr;</a></article>')


def render(news, prices, spark, price_stamp, live, articles=()):
    upd = datetime.fromisoformat(news["updated_at"].replace("Z", "+00:00")).astimezone(ET)
    upd_s = upd.strftime("%b %-d, %Y at %-I:%M %p ET")
    date_label = news.get("date_label") or upd.strftime("%A, %b %-d, %Y")

    rows = ""
    if prices:
        for sym, _id, name in COINS:
            p = prices.get(sym, {})
            chg = p.get("chg")
            cls = "flat" if chg is None else ("up" if chg >= 0 else "down")
            chg_s = "n/a" if chg is None else f"{'+' if chg >= 0 else ''}{chg:.2f}%"
            rows += (f'<tr><td><b>{sym}</b> <span class="muted">{name}</span></td>'
                     f'<td class="num">{fmt_price(sym, p.get("usd"))}</td><td class="num {cls}">{chg_s}</td></tr>')
        ps = datetime.fromisoformat(price_stamp).astimezone(ET).strftime("%b %-d, %-I:%M %p ET")
        note = f"Prices from CoinGecko, as of {ps}." + ("" if live else " Live update failed, showing last known prices.")
        price_html = (f'<div class="card"><table class="prices"><thead><tr><th>Coin</th><th class="num">Price</th>'
                      f'<th class="num">24h</th></tr></thead><tbody>{rows}</tbody></table><p class="fine">{e(note)}</p></div>')
    else:
        price_html = '<div class="card"><p class="muted">Prices are unavailable right now.</p></div>'

    chart_html = ""
    if spark:
        svg, lo, hi = sparkline_svg(spark)
        chart_html = (f'<div class="card chart"><div class="chart-head"><b>BTC, last 7 days</b>'
                      f'<span class="muted">Low {fmt_price("BTC", lo)} &middot; High {fmt_price("BTC", hi)}</span></div>{svg}</div>')

    crypto = "".join(story_card(i) for i in news.get("crypto_headlines", []))
    doginal = "".join(story_card(i, i.get("tag")) for i in news.get("doginal_news", [])) or \
        '<div class="card"><p class="muted">No verified Doginal Dogs news found today. Check back tomorrow.</p></div>'
    notes = f'<p class="fine notes">{e(news["notes"])}</p>' if news.get("notes") else ""
    comm = "".join(
        f'<a class="card comm" href="https://x.com/{h}" target="_blank" rel="noopener"><b>@{e(h)}</b>'
        f'<span>{e(n)}</span><small>{e(d)}</small></a>' for h, n, d in COMMUNITY)

    about_html = about_block()
    teaser_html = "".join(article_card(a) for a in list(articles)[:3]) or '<div class="card"><p class="muted">Articles coming soon.</p></div>'
    desc = "Reef, Community Builder in the Doginal Dogs and metax crypto community. Daily crypto updates and Doginal Dogs news from Louisville, KY."
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Reef | Community Builder | Doginal Dogs &amp; metax</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0b0f14">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="canonical" href="{SITE}/">
<link rel="alternate" type="application/rss+xml" title="Reef | Articles" href="/feed.xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Reef">
<meta property="og:title" content="Reef | Community Builder">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}/">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@Reefmetax">
<meta name="twitter:creator" content="@Reefmetax">
<meta name="twitter:title" content="Reef | Community Builder">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<style>
{CSS}
</style>
</head>
<body>
<nav><div class="wrap"><b>REEF</b><a href="#about">About</a><a href="#crypto">Crypto</a><a href="#doginal">Doginal Dogs</a><a href="/articles/">Articles</a><a href="#community">Community</a></div></nav>
<header class="hero"><div class="wrap">
<span class="eyebrow">Louisville, KY</span>
<h1><span>Reef</span></h1>
<p class="role">Community Builder</p>
<p class="tag-line">Building the Doginal Dogs and metax crypto community, one day at a time. Daily crypto updates and pack news, right here.</p>
<div class="btns"><a class="btn primary" href="https://x.com/Reefmetax" target="_blank" rel="noopener">Follow @Reefmetax on X</a><a class="btn" href="#crypto">Today in Crypto</a><a class="btn" href="#doginal">Doginal Dogs News</a></div>
</div></header>
<main class="wrap">
<section id="about">{about_html}</section>
<section id="crypto"><h2>Today in Crypto</h2><p class="sub">{e(date_label)}</p>
<div class="two">{price_html}{chart_html}</div>
<div class="grid">{crypto}</div></section>
<section id="doginal"><h2>Doginal Dogs News</h2><p class="sub">Doginal Dogs, Legends TCG and Pyth</p>
<div class="grid">{doginal}</div>{notes}</section>
<section id="articles"><h2>Latest Articles</h2><p class="sub">Written by Reef</p>
<div class="art-list">{teaser_html}</div><a class="more-link" href="/articles/">All articles &rarr;</a></section>
<section id="community"><h2>Community</h2><p class="sub">Follow the pack on X</p>
<div class="grid comm-grid">{comm}</div></section>
<section id="newsletter">{newsletter_block()}</section>
</main>
<footer><div class="wrap"><p><b>Last updated:</b> {e(upd_s)}</p><p>Not financial advice. Do your own research.</p><p><a href="/articles/">Articles</a> &middot; <a href="/feed.xml">RSS</a> &middot; <a href="{NEWSLETTER_URL}" target="_blank" rel="noopener">Newsletter</a></p><p>&copy; {upd.year} Reef &middot; <a href="https://x.com/Reefmetax" target="_blank" rel="noopener">@Reefmetax</a></p></div></footer>
{GOATCOUNTER}
</body>
</html>
"""


# ---------- Articles ----------

def inline_md(text):
    """Escape, then apply **bold**, *italic* and [text](url) (http/https links only)."""
    t = html.escape(text, quote=False)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
               lambda m: f'<a href="{html.escape(m.group(2), quote=True)}" target="_blank" rel="noopener">{m.group(1)}</a>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?![*\w])", r"<em>\1</em>", t)
    return t


def render_md(body):
    """Tiny markdown: '## ' headings, '- ' lists, paragraphs. A '## Sources' list gets class="sources".
    A paragraph starting with 'Not financial advice' is rendered as a disclaimer callout."""
    out, in_sources = [], False
    for block in re.split(r"\n\s*\n", body.strip()):
        lines = [l for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        if lines[0].startswith("## "):
            in_sources = lines[0][3:].strip().lower() == "sources"
            out.append(f"<h2>{inline_md(lines[0][3:].strip())}</h2>")
            lines = lines[1:]
            if not lines:
                continue
        if all(l.lstrip().startswith("- ") for l in lines):
            cls = ' class="sources"' if in_sources else ""
            out.append(f"<ul{cls}>" + "".join(f"<li>{inline_md(l.lstrip()[2:])}</li>" for l in lines) + "</ul>")
        else:
            para = " ".join(l.strip() for l in lines)
            out.append(f"<p>{inline_md(para)}</p>")
    return "\n".join(out)


def load_articles():
    arts = []
    for f in sorted(ARTICLES_DIR.glob("*.md")):
        raw = f.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
        if not m:
            print(f"skip {f.name}: missing front matter", file=sys.stderr)
            continue
        meta = {}
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        if not all(meta.get(k) for k in ("title", "date", "description")):
            print(f"skip {f.name}: needs title, date, description", file=sys.stderr)
            continue
        if meta.get("draft", "").lower() == "true":
            continue
        body = m.group(2).strip()
        d = datetime.strptime(meta["date"], "%Y-%m-%d").date()
        words = len(re.sub(r"[#*\[\]()-]", " ", body).split())
        arts.append({"slug": meta.get("slug") or f.stem, "title": meta["title"], "date": d, "description": meta["description"],
                     "body_html": render_md(body), "minutes": max(1, round(words / 200))})
    arts.sort(key=lambda a: (a["date"], a["slug"]), reverse=True)
    return arts


def date_str(d):
    return d.strftime("%b %-d, %Y")


def about_block():
    return (f'<div class="card about"><img class="avatar" src="{AVATAR}" alt="Reef, profile picture" width="96" height="96" loading="lazy">'
            f'<div><h3>About Reef</h3><p>{e(BIO)}</p>'
            f'<a class="more" href="{AUTHOR_URL}" target="_blank" rel="noopener">@Reefmetax on X &rarr;</a></div></div>')


def article_card(a):
    return (f'<a class="card art-card" href="/articles/{e(a["slug"])}/"><div class="meta"><img class="avatar" src="{AVATAR}" alt="" width="26" height="26" loading="lazy">'
            f'<span>By {AUTHOR} &middot; {date_str(a["date"])} &middot; {a["minutes"]} min read</span></div>'
            f'<h3>{e(a["title"])}</h3><p>{e(a["description"])}</p></a>')


def page_shell(title, desc, path, body, og_type="website", extra_head=""):
    url = f"{SITE}{path}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0b0f14">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="canonical" href="{url}">
<link rel="alternate" type="application/rss+xml" title="Reef | Articles" href="/feed.xml">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Reef">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@Reefmetax">
<meta name="twitter:creator" content="@Reefmetax">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/og-image.png">
{extra_head}<style>
{CSS}
</style>
</head>
<body>
<nav><div class="wrap"><b>REEF</b><a href="/">Home</a><a href="/#crypto">Crypto</a><a href="/#doginal">Doginal Dogs</a><a href="/articles/">Articles</a></div></nav>
{body}
<footer><div class="wrap"><p>Not financial advice. Do your own research.</p><p><a href="/articles/">Articles</a> &middot; <a href="/feed.xml">RSS</a> &middot; <a href="{NEWSLETTER_URL}" target="_blank" rel="noopener">Newsletter</a> &middot; <a href="/">Home</a></p><p>&copy; {datetime.now(ET).year} Reef &middot; <a href="{AUTHOR_URL}" target="_blank" rel="noopener">@Reefmetax</a></p></div></footer>
{GOATCOUNTER}
</body>
</html>
"""


def render_article(a):
    path = f"/articles/{a['slug']}/"
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["description"],
                     "datePublished": a["date"].isoformat(), "mainEntityOfPage": f"{SITE}{path}",
                     "author": {"@type": "Person", "name": AUTHOR, "url": AUTHOR_URL},
                     "image": f"{SITE}/og-image.png"}).replace("</", "<\\/")
    extra = (f'<meta property="article:published_time" content="{a["date"].isoformat()}">\n'
             f'<meta property="article:author" content="{AUTHOR_URL}">\n<script type="application/ld+json">{ld}</script>\n')
    body = (f'<main class="wrap"><article class="article"><a class="back" href="/articles/">&larr; All articles</a>'
            f'<h1>{e(a["title"])}</h1>'
            f'<div class="byline"><img class="avatar" src="{AVATAR}" alt="Reef, profile picture" width="48" height="48">'
            f'<div><b>By <a href="{AUTHOR_URL}" target="_blank" rel="noopener">{AUTHOR}</a></b><span>{AUTHOR_ROLE} &middot; {date_str(a["date"])} &middot; {a["minutes"]} min read</span></div></div>'
            f'<div class="prose">{a["body_html"]}</div>'
            f'<p class="disclaimer">Not financial advice. This is general information, not a recommendation to buy or sell anything. Do your own research.</p>'
            f'{newsletter_block("in-article")}'
            f'<a class="back" style="margin-top:26px" href="/articles/">&larr; Back to all articles</a></article></main>')
    return page_shell(f'{a["title"]} | Reef', a["description"], path, body, og_type="article", extra_head=extra)


def render_articles_index(arts):
    cards = "".join(article_card(a) for a in arts) or '<div class="card"><p class="muted">No articles yet.</p></div>'
    body = (f'<main class="wrap"><div class="page-head"><h1><span style="background:linear-gradient(90deg,var(--orange),var(--teal));-webkit-background-clip:text;background-clip:text;color:transparent">Articles</span></h1>'
            f'<p class="sub">Plain-English write-ups on Doginal Dogs, crypto and Pyth, by Reef. <a href="/feed.xml" style="color:var(--teal)">RSS</a></p></div>'
            f'<section style="padding-top:12px"><div class="art-list">{cards}</div></section>'
            f'<section>{newsletter_block()}</section>'
            f'<section>{about_block()}</section></main>')
    return page_shell("Articles | Reef | Community Builder", "Plain-English articles on Doginal Dogs, crypto markets and Pyth Network, written by Reef, Community Builder.", "/articles/", body)


def render_feed(arts):
    items = ""
    for a in arts:
        pub = format_datetime(datetime.combine(a["date"], dtime(12, 0), tzinfo=ET))
        link = f"{SITE}/articles/{a['slug']}/"
        items += (f"<item><title>{e(a['title'])}</title><link>{link}</link><guid isPermaLink=\"true\">{link}</guid>"
                  f"<pubDate>{pub}</pubDate><author>noreply@reefmetax.com (Reef)</author><description>{e(a['description'])}</description></item>\n")
    last = format_datetime(datetime.combine(arts[0]["date"], dtime(12, 0), tzinfo=ET)) if arts else ""
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>\n'
            f'<title>Reef | Articles</title><link>{SITE}/articles/</link><description>Articles on Doginal Dogs, crypto and Pyth by Reef, Community Builder.</description>\n'
            f'<language>en-us</language><lastBuildDate>{last}</lastBuildDate><atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>\n{items}</channel></rss>\n')


def render_sitemap(arts, home_date):
    urls = [(f"{SITE}/", home_date), (f"{SITE}/articles/", arts[0]["date"].isoformat() if arts else home_date)]
    urls += [(f"{SITE}/articles/{a['slug']}/", a["date"].isoformat()) for a in arts]
    body = "".join(f"<url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n'


def build_articles(arts, home_date):
    import shutil
    out = ROOT / "articles"
    keep = {a["slug"] for a in arts}
    if out.exists():  # drop pages for removed articles
        for d in out.iterdir():
            if d.is_dir() and d.name not in keep:
                shutil.rmtree(d)
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(render_articles_index(arts), encoding="utf-8")
    for a in arts:
        (out / a["slug"]).mkdir(exist_ok=True)
        (out / a["slug"] / "index.html").write_text(render_article(a), encoding="utf-8")
    (ROOT / "feed.xml").write_text(render_feed(arts), encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(render_sitemap(arts, home_date), encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")


def main():
    news = json.loads((ROOT / "data" / "news.json").read_text())
    prices, spark, stamp, live = get_prices()
    if spark:
        (ROOT / "btc-chart.svg").write_text(sparkline_svg(spark, standalone=True)[0])
    arts = load_articles()
    (ROOT / "index.html").write_text(render(news, prices, spark, stamp, live, arts))
    home_date = datetime.fromisoformat(news["updated_at"].replace("Z", "+00:00")).astimezone(ET).date().isoformat()
    build_articles(arts, home_date)
    print(f"built index.html | live prices: {live} | headlines: {len(news.get('crypto_headlines', []))} | doginal: {len(news.get('doginal_news', []))} | articles: {len(arts)}")


if __name__ == "__main__":
    main()
