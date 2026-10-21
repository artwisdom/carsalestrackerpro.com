#!/usr/bin/env python3
"""Publish every Dealer Ops Daily issue as a page on carsalestrackerpro.com.

Reads the newsletter's public RSS feed (no credentials) and, for each issue:
  brief/<YYYY-MM-DD>/index.html  — the issue, signup, app and calculator links
  brief/<YYYY-MM-DD>/card.png    — the shareable huddle card (also the OG image)
then refreshes the "Recent issues" list on /brief/ and the sitemap.

Idempotent: files are only rewritten when their content changes, so a run with
nothing new produces no commit. Runs from .github/workflows/brief-archive.yml.

Usage:
  python scripts/build_brief.py              # build from the live feed
  python scripts/build_brief.py --feed FILE  # build from a saved feed (testing)
  python scripts/build_brief.py --ping URLS_FILE  # tell IndexNow about new pages
"""
from __future__ import annotations

import argparse
import email.utils
import html
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brief_card import render_card  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BRIEF = ROOT / "brief"
SITE = "https://carsalestrackerpro.com"
FEED_URL = "https://buttondown.com/dube/rss"
NEW_URLS_FILE = ROOT / ".brief-new-urls"
INDEXNOW_KEY = "f94f86596256e1597287ad38cee3f9cf"  # public by design; served at /<key>.txt

UA = "CarSalesTrackerPro-BriefArchive/1.0 (+https://carsalestrackerpro.com/brief/)"

# ---------------------------------------------------------------- feed

def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def parse_feed(xml: str) -> list[dict]:
    items = []
    for raw in re.findall(r"<item>(.*?)</item>", xml, re.S):
        def tag(name: str) -> str:
            m = re.search(rf"<{name}[^>]*>(.*?)</{name}>", raw, re.S)
            v = m.group(1).strip() if m else ""
            v = re.sub(r"^<!\[CDATA\[(.*)\]\]>$", r"\1", v, flags=re.S)
            return html.unescape(v)
        published = email.utils.parsedate_to_datetime(tag("pubDate")).astimezone(timezone.utc)
        items.append({"title": tag("title"), "link": tag("link"), "published": published,
                      "body": tag("description")})
    return sorted(items, key=lambda i: i["published"])

# ---------------------------------------------------------------- cleaning

ALLOWED = {"p", "h2", "h3", "strong", "b", "em", "i", "a", "ul", "ol", "li",
           "blockquote", "hr", "br", "small", "code"}
VOID = {"hr", "br"}
DROP_WITH_CONTENT = {"script", "style", "iframe", "object", "embed", "form", "svg"}


class _Sanitizer(HTMLParser):
    """Allowlist sanitizer: issue text comes from public news feeds via an LLM, so
    nothing but plain editorial markup and http(s) links reaches the page."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in DROP_WITH_CONTENT:
            self.skip += 1
            return
        if self.skip or tag not in ALLOWED:
            return
        if tag == "a":
            href = dict(attrs).get("href") or ""
            if not href.startswith(("https://", "http://")):
                self.out.append("<a>")
                return
            ext = not href.startswith(SITE)
            extra = ' target="_blank" rel="noopener"' if ext else ""
            self.out.append(f'<a href="{html.escape(href, quote=True)}"{extra}>')
            return
        self.out.append(f"<{tag}>" if tag not in VOID else f"<{tag}/>")

    def handle_endtag(self, tag):
        if tag in DROP_WITH_CONTENT:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip or tag not in ALLOWED or tag in VOID:
            return
        self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(html.escape(data, quote=False))


def sanitize(fragment: str) -> str:
    s = _Sanitizer()
    s.feed(fragment)
    s.close()
    return "".join(s.out)


# A US street address pattern. The email footer carries the sender's postal address
# (required in email by CAN-SPAM, not on web pages); it is stripped below, and this
# is the backstop in case the footer markup ever changes.
STREET_ADDRESS = re.compile(
    r"\b\d{1,6}\s+(?:[A-Z][a-z]+\s+){1,3}(?:St|Street|Ave|Avenue|Rd|Road|Blvd|Ln|Lane|Dr|Drive|Ct|Way)\b"
    r"\.?,?\s+[A-Z][A-Za-z ]+,\s*[A-Z]{2}\s+\d{5}(?:-\d{4})?")


def clean_body(body: str) -> tuple[str, str, str]:
    """Return (h1 title, cold open, cleaned html) from a rendered issue."""
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    title = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else ""
    body = re.sub(r"<h1[^>]*>.*?</h1>", "", body, count=1, flags=re.S)
    body = re.sub(r"<p>\s*<img[^>]*>\s*</p>", "", body, flags=re.S)           # masthead / hero
    body = re.sub(r"<p>(?:(?!</p>).)*utm_campaign=forwarded(?:(?!</p>).)*</p>", "", body, flags=re.S)
    body = re.sub(r"<p>\s*<small>.*?</small>\s*</p>\s*$", "", body.strip(), flags=re.S)  # email footer
    first_em = re.search(r"<p>\s*<em>(.*?)</em>\s*</p>", body, re.S)
    cold_open = re.sub(r"<[^>]+>", "", first_em.group(1)).strip() if first_em else ""
    cleaned = STREET_ADDRESS.sub("", sanitize(body))
    return title, " ".join(cold_open.split()), cleaned


def huddle_from(cleaned: str) -> dict | None:
    q = re.search(r"<blockquote>(.*?)</blockquote>", cleaned, re.S)
    if not q or "HUDDLE STARTER" not in q.group(1):
        return None
    block = q.group(1)
    num = re.search(r"<strong>([^<]+)</strong>\s*[—–-]\s*(.*?)</p>", block, re.S)
    ask = re.search(r"Ask the team:</strong>\s*(.*?)</p>", block, re.S)
    if not num:
        return None
    strip = lambda t: " ".join(html.unescape(re.sub(r"<[^>]+>", "", t)).split())
    return {"number": strip(num.group(1)), "talking_point": strip(num.group(2)),
            "question": strip(ask.group(1)) if ask else ""}

# ---------------------------------------------------------------- pages

HEAD_FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" '
              'href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/'
              'css2?family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">')

SITE_HEADER = '''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-hdr"><div class="site-hdr-in">
  <a class="site-logo" href="/"><img src="/assets/icon.png" alt="CarSales Tracker Pro" width="180" height="180">CarSales Tracker Pro</a>
  <nav class="site-nav"><a class="ghost" href="/brief/">Daily brief</a><a class="cta" href="/tracker/">Open the tracker</a></nav>
</div></header>'''

SITE_FOOTER = '''<footer class="site-foot"><div class="site-foot-in">
  <p class="tag">Your deals. Your pipeline. Your edge.</p>
  <p class="sub">Free commission tools, practical pay-plan guides, and a private deal tracker for automotive sales professionals.</p>
  <nav aria-label="Footer navigation"><a href="/">Commission hub</a><a href="/tracker/">Free web tracker</a><a href="/tools/">Tools</a><a href="/blog/">Guides</a><a href="/brief/">Daily brief</a><a href="/about/">About</a><a href="/editorial-policy/">Editorial policy</a><a href="/contact/">Contact</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a><a href="/disclaimer/">Disclaimer</a></nav>
  <p class="copy">© 2026 CarSales Tracker Pro · <a href="https://andromedakinship.com" target="_blank" rel="noopener" style="color:inherit">Andromeda Kinship</a></p>
</div></footer>'''

PAGE_CSS = '''<style>
.brief-meta{color:var(--text3);font-size:.9rem;margin:6px 0 22px}
.brief-card{display:block;width:100%;height:auto;border-radius:var(--radius);border:1px solid var(--border);box-shadow:var(--shadow)}
.brief-share{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:12px 0 30px}
.brief-share span{font-size:.88rem;color:var(--text2);margin-right:4px}
.brief-body h2{margin-top:30px}
.brief-body blockquote{margin:22px 0;padding:16px 20px;border-left:4px solid #F59E0B;background:var(--surface2);border-radius:0 12px 12px 0}
.brief-body blockquote p{margin:6px 0}
.brief-nav{display:flex;justify-content:space-between;gap:12px;margin:34px 0 8px;font-size:.92rem}
.brief-list{list-style:none;padding:0;margin:0;display:grid;gap:10px}
.brief-list a{display:flex;gap:14px;align-items:baseline;padding:12px 14px;border:1px solid var(--border);border-radius:12px;background:var(--surface);color:var(--text)!important;text-decoration:none!important}
.brief-list a:hover{border-color:var(--primary)}
.brief-list time{flex:none;width:96px;color:var(--text3);font-size:.85rem;font-variant-numeric:tabular-nums}
</style>'''

SHARE_JS = '''<script>
(function(){
  var bar=document.querySelector('.brief-share'); if(!bar) return;
  var url=document.querySelector('link[rel="canonical"]').href, title=document.title;
  var status=bar.querySelector('[role=status]');
  function copy(){ if(navigator.clipboard){navigator.clipboard.writeText(url).then(function(){status.textContent='Link copied.'},function(){status.textContent='Copy unavailable here.'})} }
  bar.querySelector('[data-share]').addEventListener('click',function(){
    if(navigator.share){navigator.share({title:title,url:url}).catch(function(e){if(e&&e.name!=='AbortError')copy()})}else{copy()}
  });
  bar.querySelector('[data-copy]').addEventListener('click',copy);
})();
</script>'''


def human_date(d: datetime) -> str:
    return f"{d:%A}, {d:%B} {d.day}, {d.year}"


def issue_page(it: dict, slug: str, prev_it: dict | None, next_it: dict | None) -> str:
    url = f"{SITE}/brief/{slug}/"
    title = it["h1"] or it["title"]
    desc = (it["cold_open"] or it["title"])[:155].rstrip()
    card = f"{url}card.png"
    ld = {
        "@context": "https://schema.org", "@type": "NewsArticle",
        "headline": title[:110], "description": desc, "image": [card],
        "datePublished": it["published"].isoformat(), "dateModified": it["published"].isoformat(),
        "mainEntityOfPage": url, "isAccessibleForFree": True,
        "author": {"@type": "Organization", "name": "Dealer Ops Daily", "url": f"{SITE}/brief/"},
        "publisher": {"@type": "Organization", "name": "Dealer Ops Daily",
                      "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/icon.png"}},
    }
    hud = it["huddle"]
    alt = (f"Huddle starter: {hud['number']} — {hud['talking_point']}" if hud else title)
    nav = '<nav class="brief-nav" aria-label="More issues">'
    nav += (f'<a href="/brief/{prev_it["slug"]}/">← {html.escape(prev_it["h1"] or prev_it["title"])}</a>'
            if prev_it else "<span></span>")
    nav += (f'<a href="/brief/{next_it["slug"]}/">{html.escape(next_it["h1"] or next_it["title"])} →</a>'
            if next_it else "<span></span>")
    nav += "</nav>"
    e = lambda t: html.escape(t, quote=True)
    # The card is always the link-preview image, but it's only worth showing on the
    # page when it carries a huddle starter — otherwise it repeats the headline.
    card_img = (f'<img class="brief-card" src="card.png" width="1200" height="630" alt="{e(alt)}">'
                if hud else "")
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)} — Dealer Ops Daily, {it["published"]:%b} {it["published"].day}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0F172A">
<meta property="og:type" content="article">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{card}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="article:published_time" content="{it["published"].isoformat()}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{card}">
<link rel="icon" type="image/png" href="/assets/icon.png">
{HEAD_FONTS}
<link rel="stylesheet" href="/assets/site.css?v=2">
{PAGE_CSS}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<script src="/assets/newsletter.js?v=2" defer></script>
</head>
<body>
{SITE_HEADER}

<main class="wrap" id="main">
  <p class="crumbs"><a href="/">Home</a> › <a href="/brief/">Daily brief</a> › {it["published"]:%b} {it["published"].day}</p>
  <article>
    <h1 class="page-title">{e(title)}</h1>
    <p class="brief-meta">Dealer Ops Daily · {human_date(it["published"])} · 5-minute read</p>
    {card_img}
    <div class="brief-share" aria-label="Share this issue">
      <span>Running the morning meeting?</span>
      <button class="tool-action primary" type="button" data-share>Share with your team</button>
      <button class="tool-action" type="button" data-copy>Copy link</button>
      <a class="tool-action" href="card.png" download="dealer-ops-daily-{slug}.png">Save card</a>
      <span class="tool-status" role="status" aria-live="polite"></span>
    </div>
    <div class="brief-body">
{it["html"]}
    </div>
    <div data-dod-mount="issue"></div>
    <div class="cards">
      <a class="card" href="/tools/car-salesman-commission-calculator/"><span class="k">Calculator</span><h3>Commission calculator</h3><p>Estimate this month's check from units, gross, pack and minis.</p></a>
      <a class="card" href="/tools/pay-plan-comparison-calculator/"><span class="k">Comparison</span><h3>Pay plan comparison</h3><p>Put two plans side by side under the same month.</p></a>
      <a class="card" href="/tracker/"><span class="k">Free tracker</span><h3>Track every deal</h3><p>Log each car and watch your month-to-date pay climb.</p></a>
    </div>
    {nav}
    <div class="editor-note"><strong>How this is made:</strong> Dealer Ops Daily is written by AI from public industry sources, and every issue passes automated editorial and accuracy checks before it sends. It isn't financial, legal, or tax advice. Spot an error? <a href="/contact/">Tell us</a> and we'll correct it.</div>
  </article>
</main>

{SITE_FOOTER}
{SHARE_JS}
</body>
</html>
'''


def brief_list_html(items: list[dict], limit: int = 15) -> str:
    rows = []
    for it in reversed(items[-limit:]):
        rows.append(f'      <li><a href="/brief/{it["slug"]}/"><time datetime="{it["published"]:%Y-%m-%d}">'
                    f'{it["published"]:%b} {it["published"].day}</time>'
                    f'<span>{html.escape(it["h1"] or it["title"])}</span></a></li>')
    return ("    <h2>Recent issues</h2>\n    <ul class=\"brief-list\">\n" + "\n".join(rows) + "\n    </ul>")


def write_if_changed(path: Path, text: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def replace_between(text: str, start: str, end: str, inner: str) -> str:
    a, b = text.index(start) + len(start), text.index(end)
    return text[:a] + "\n" + inner + "\n" + text[b:]

# ---------------------------------------------------------------- build

def build(feed_xml: str) -> list[str]:
    items = parse_feed(feed_xml)
    seen: dict[str, int] = {}
    for it in items:
        base = f"{it['published']:%Y-%m-%d}"
        seen[base] = seen.get(base, 0) + 1
        it["slug"] = base if seen[base] == 1 else f"{base}-{seen[base]}"
        it["h1"], it["cold_open"], it["html"] = clean_body(it["body"])
        it["huddle"] = huddle_from(it["html"])

    new_urls = []
    for i, it in enumerate(items):
        page = BRIEF / it["slug"] / "index.html"
        is_new = not page.exists()
        prev_it = items[i - 1] if i > 0 else None
        next_it = items[i + 1] if i + 1 < len(items) else None
        if write_if_changed(page, issue_page(it, it["slug"], prev_it, next_it)) and is_new:
            new_urls.append(f"{SITE}/brief/{it['slug']}/")
        h = it["huddle"] or {}
        render_card(BRIEF / it["slug"] / "card.png",
                    date_label=f"{it['published']:%a, %b} {it['published'].day}, {it['published'].year}",
                    number=h.get("number"), talking_point=h.get("talking_point"),
                    question=h.get("question"), title=it["h1"] or it["title"], subtitle=it["cold_open"])

    index = BRIEF / "index.html"
    write_if_changed(index, replace_between(index.read_text(encoding="utf-8"),
                                            "<!-- BRIEF-LIST:START -->", "<!-- BRIEF-LIST:END -->",
                                            brief_list_html(items)))

    sm = ROOT / "sitemap.xml"
    entries = "\n".join(
        f"  <url><loc>{SITE}/brief/{it['slug']}/</loc><lastmod>{it['published']:%Y-%m-%d}</lastmod>"
        f"<changefreq>yearly</changefreq><priority>0.6</priority></url>" for it in items)
    write_if_changed(sm, replace_between(sm.read_text(encoding="utf-8"),
                                         "<!-- BRIEF-ISSUES:START -->", "<!-- BRIEF-ISSUES:END -->", entries))
    if new_urls:
        new_urls.append(f"{SITE}/brief/")
    return new_urls


def ping_indexnow(urls: list[str]) -> None:
    body = json.dumps({"host": "carsalestrackerpro.com", "key": INDEXNOW_KEY,
                       "keyLocation": f"{SITE}/{INDEXNOW_KEY}.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"IndexNow accepted {len(urls)} URLs (HTTP {r.status})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--feed", help="build from a saved feed file instead of the live URL")
    ap.add_argument("--ping", help="file of URLs to submit to IndexNow")
    args = ap.parse_args()
    if args.ping:
        urls = [u for u in Path(args.ping).read_text().split() if u]
        if urls:
            ping_indexnow(urls)
        return 0
    xml = Path(args.feed).read_text(encoding="utf-8") if args.feed else fetch(FEED_URL)
    new_urls = build(xml)
    NEW_URLS_FILE.write_text("\n".join(new_urls) + ("\n" if new_urls else ""))
    print(f"built archive; {len(new_urls)} new URLs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
