#!/usr/bin/env python3
"""Render reefmetax.com: reads data/news.json + live prices, writes index.html and btc-chart.svg."""
import html, json, sys, urllib.request, urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).parent
ET = ZoneInfo("America/New_York")
SITE = "https://reefmetax.com"
COINS = [("BTC", "bitcoin", "Bitcoin"), ("ETH", "ethereum", "Ethereum"), ("SOL", "solana", "Solana"),
         ("DOGE", "dogecoin", "Dogecoin"), ("PYTH", "pyth-network", "Pyth")]
CG = "https://api.coingecko.com/api/v3"
CACHE = ROOT / "data" / "prices_cache.json"

COMMUNITY = [
    ("doginaldogs", "Doginal Dogs", "10,000 pixel dogs inscribed on $DOGE."),
    ("DDLTCG", "Legends TCG", "A premium trading card game by Doginal Dogs."),
    ("PythNetwork", "Pyth Network", "The price layer of the global financial market."),
    ("thePIRB", "PIRB", "Part of the pack."),
    ("barkmeta", "Bark", "Financial trends and commentary. Host of THE GREAT RESET."),
    ("Shieldmetax", "Shield", "Web3 builder. Events, marketing, experiences."),
    ("GodsBurnt", "Shibo", "Financial news and commentary. Host of the Finance Show."),
]


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


def e(s):
    return html.escape(str(s), quote=True)


def safe_url(u):
    return u if str(u).startswith(("https://x.com/", "https://twitter.com/", "https://reefmetax.com")) else "#"


def story_card(it, tag=None):
    t = f'<span class="tag tag-{e(tag.lower().replace(" ", "-"))}">{e(tag)}</span>' if tag else ""
    return (f'<article class="card story">{t}<h3>{e(it["title"])}</h3><p>{e(it["summary"])}</p>'
            f'<a class="src" href="{e(safe_url(it["url"]))}" target="_blank" rel="noopener">{e(it.get("source", "Source"))} on X &rarr;</a></article>')


def render(news, prices, spark, price_stamp, live):
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
:root{{--bg:#0b0f14;--panel:#111822;--line:#1e2a38;--text:#e8eef5;--muted:#8a9bb0;--orange:#ff8a3d;--teal:#2ee6c5;--up:#2ee6c5;--down:#ff6b5e}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--text);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;-webkit-font-smoothing:antialiased;
background-image:radial-gradient(900px 400px at 85% -10%,rgba(255,138,61,.14),transparent 60%),radial-gradient(700px 400px at -10% 10%,rgba(46,230,197,.10),transparent 60%);background-repeat:no-repeat}}
a{{color:inherit;text-decoration:none}}
.wrap{{max-width:1040px;margin:0 auto;padding:0 18px}}
nav{{position:sticky;top:0;z-index:5;backdrop-filter:blur(10px);background:rgba(11,15,20,.8);border-bottom:1px solid var(--line)}}
nav .wrap{{display:flex;gap:18px;align-items:center;height:52px;overflow-x:auto;white-space:nowrap;scrollbar-width:none}}
nav b{{color:var(--orange);margin-right:auto}}
nav a{{color:var(--muted);font-size:14px}}
nav a:hover{{color:var(--teal)}}
.hero{{padding:56px 0 40px}}
.eyebrow{{display:inline-block;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);border:1px solid rgba(46,230,197,.4);padding:4px 10px;border-radius:99px}}
h1{{font-size:clamp(44px,12vw,92px);line-height:1;margin:16px 0 8px;letter-spacing:-.03em}}
h1 span{{background:linear-gradient(90deg,var(--orange),var(--teal));-webkit-background-clip:text;background-clip:text;color:transparent}}
.role{{font-size:clamp(18px,4.5vw,24px);color:var(--text)}}
.tag-line{{color:var(--muted);max-width:560px;margin-top:10px}}
.btns{{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}}
.btn{{padding:13px 22px;border-radius:12px;font-weight:600;border:1px solid var(--line);background:var(--panel);min-height:48px;display:inline-flex;align-items:center}}
.btn.primary{{background:linear-gradient(90deg,var(--orange),#ffb07a);color:#1a1006;border:0}}
.btn:hover{{transform:translateY(-1px)}}
section{{padding:34px 0}}
h2{{font-size:26px;letter-spacing:-.01em;margin-bottom:6px}}
h2::before{{content:"";display:inline-block;width:8px;height:22px;background:var(--orange);border-radius:3px;margin-right:10px;vertical-align:-3px}}
.sub{{color:var(--muted);font-size:14px;margin-bottom:16px}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:16px}}
.grid{{display:grid;gap:12px;grid-template-columns:1fr}}
.story h3{{font-size:17px;line-height:1.3;margin-bottom:6px}}
.story p{{color:#b9c6d6;font-size:15px}}
.src{{display:inline-block;margin-top:10px;color:var(--teal);font-size:14px;font-weight:600}}
.tag{{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:3px 9px;border-radius:99px;margin-bottom:8px;background:rgba(255,138,61,.15);color:var(--orange)}}
.tag-pyth{{background:rgba(46,230,197,.14);color:var(--teal)}}
.tag-ddltcg{{background:rgba(255,200,61,.14);color:#ffc83d}}
.two{{display:grid;gap:12px;grid-template-columns:1fr;margin-bottom:12px}}
table{{width:100%;border-collapse:collapse}}
th{{text-align:left;font-size:12px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.08em;padding-bottom:8px}}
td{{padding:10px 0;border-top:1px solid var(--line)}}
.num{{text-align:right;font-variant-numeric:tabular-nums}}
th.num{{text-align:right}}
.up{{color:var(--up)}}.down{{color:var(--down)}}.flat,.muted{{color:var(--muted)}}
td .muted{{font-size:13px;margin-left:4px}}
.chart svg{{width:100%;height:180px;display:block;margin-top:10px}}
.chart-head{{display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;font-size:14px}}
.fine{{font-size:12.5px;color:var(--muted);margin-top:10px}}
.notes{{margin-top:14px}}
.comm{{display:flex;flex-direction:column;gap:2px}}
.comm b{{color:var(--orange);font-size:17px}}
.comm small{{color:var(--muted)}}
.comm:hover{{border-color:var(--teal)}}
footer{{border-top:1px solid var(--line);margin-top:30px;padding:26px 0 44px;color:var(--muted);font-size:14px}}
footer b{{color:var(--text)}}
@media(min-width:700px){{.grid{{grid-template-columns:1fr 1fr}}.two{{grid-template-columns:1fr 1.3fr}}.hero{{padding:90px 0 60px}}}}
@media(min-width:980px){{.grid.three{{grid-template-columns:1fr 1fr 1fr}}.comm-grid{{grid-template-columns:repeat(4,1fr)}}}}
</style>
</head>
<body>
<nav><div class="wrap"><b>REEF</b><a href="#crypto">Crypto</a><a href="#doginal">Doginal Dogs</a><a href="#community">Community</a></div></nav>
<header class="hero"><div class="wrap">
<span class="eyebrow">Louisville, KY</span>
<h1><span>Reef</span></h1>
<p class="role">Community Builder</p>
<p class="tag-line">Building the Doginal Dogs and metax crypto community, one day at a time. Daily crypto updates and pack news, right here.</p>
<div class="btns"><a class="btn primary" href="https://x.com/Reefmetax" target="_blank" rel="noopener">Follow @Reefmetax on X</a><a class="btn" href="#crypto">Today in Crypto</a><a class="btn" href="#doginal">Doginal Dogs News</a></div>
</div></header>
<main class="wrap">
<section id="crypto"><h2>Today in Crypto</h2><p class="sub">{e(date_label)}</p>
<div class="two">{price_html}{chart_html}</div>
<div class="grid">{crypto}</div></section>
<section id="doginal"><h2>Doginal Dogs News</h2><p class="sub">Doginal Dogs, Legends TCG and Pyth</p>
<div class="grid">{doginal}</div>{notes}</section>
<section id="community"><h2>Community</h2><p class="sub">Follow the pack on X</p>
<div class="grid comm-grid">{comm}</div></section>
</main>
<footer><div class="wrap"><p><b>Last updated:</b> {e(upd_s)}</p><p>Not financial advice. Do your own research.</p><p>&copy; {upd.year} Reef &middot; <a href="https://x.com/Reefmetax" target="_blank" rel="noopener">@Reefmetax</a></p></div></footer>
</body>
</html>
"""


def main():
    news = json.loads((ROOT / "data" / "news.json").read_text())
    prices, spark, stamp, live = get_prices()
    if spark:
        (ROOT / "btc-chart.svg").write_text(sparkline_svg(spark, standalone=True)[0])
    (ROOT / "index.html").write_text(render(news, prices, spark, stamp, live))
    print(f"built index.html | live prices: {live} | headlines: {len(news.get('crypto_headlines', []))} | doginal: {len(news.get('doginal_news', []))}")


if __name__ == "__main__":
    main()
