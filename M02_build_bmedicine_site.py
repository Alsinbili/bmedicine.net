#!/usr/bin/env python3
"""Builds B Medicine's site from src/ into site/ (1 Nov 2026). Plain Python 3, nothing to install.

    python3 -B M02_build_bmedicine_site.py            # build site/
    python3 -B M02_build_bmedicine_site.py --serve    # build, then preview at http://localhost:8642

src/_layout.html is the frame of every page (header, footer). Each other .html file in src/ is one page: an
HTML comment at its top gives title, description, og_image, body_class and, for policies, updated; the rest is
the page's content. {{hub_subnav:<page>}} puts Hub's own menu on Hub's pages. Pages keep their place:
src/hub/privacy/index.html becomes bmedicine.net/hub/privacy/. src/assets/ is copied as it is.

The site lives at https://bemedicine.github.io (free, GitHub Pages). The build also makes forward/, a small site
for the bmedicine.net name: every address there sends the visitor to the same page on bemedicine.github.io.

The build checks what it can: every internal link and image leads somewhere, no em or en dashes in the text,
no placeholder left. site/ and forward/ are what get uploaded; never edit them by hand.
"""
import datetime, html, re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC, OUT, FORWARD = HERE / "src", HERE / "site", HERE / "forward"
SITE_URL = "https://bemedicine.github.io"
FORWARDING_NAME = "bmedicine.net"

HUB_PAGES = [("home", "/hub/", "Hub"), ("support", "/hub/support/", "Support"),
             ("privacy", "/hub/privacy/", "Privacy Policy"), ("terms", "/hub/terms/", "Terms")]


def hub_subnav(current):
    links = []
    for key, href, label in HUB_PAGES[1:]:
        cur = ' aria-current="page"' if key == current else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    home_cur = ' aria-current="page"' if current == "home" else ""
    return ('<nav class="subnav" aria-label="Hub"><div class="wrap">'
            f'<a class="sub-title" href="/hub/"{home_cur}><img src="/assets/img/hub-icon.png" alt="" width="26" '
            f'height="26">Hub</a>{"".join(links)}</div></nav>')


def read_page(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\s*<!--(.*?)-->\s*", text, re.S)
    meta = {}
    if m:
        for line in m.group(1).strip().splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
        text = text[m.end():]
    return meta, text


def url_for(rel):
    rel = rel.as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC / "assets", OUT / "assets")
    layout = (SRC / "_layout.html").read_text(encoding="utf-8")
    year = str(datetime.date.today().year)
    pages = []
    for path in sorted(SRC.rglob("*.html")):
        rel = path.relative_to(SRC)
        if rel.name.startswith("_") or rel.parts[0] == "assets":
            continue
        meta, body = read_page(path)
        body = re.sub(r"\{\{hub_subnav:(\w+)\}\}", lambda m: hub_subnav(m.group(1)), body)
        page = layout.replace("{{content}}", body)
        values = {"title": meta.get("title", "B Medicine"), "description": meta.get("description", ""),
                  "og_image": meta.get("og_image", "logo-wide.png"), "body_class": meta.get("body_class", ""),
                  "updated": meta.get("updated", ""), "year": year, "path": url_for(rel), "site_url": SITE_URL}
        for key, value in values.items():
            page = page.replace("{{" + key + "}}", html.escape(value, quote=True) if key in ("title", "description") else value)
        target = OUT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page, encoding="utf-8")
        pages.append((rel, url_for(rel), page))
    (OUT / ".nojekyll").write_text("")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    urls = "".join(f"  <url><loc>{SITE_URL}{u}</loc></url>\n" for r, u, _ in pages if r.name != "404.html")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     f"{urls}</urlset>\n")
    return pages


FORWARD_PAGE = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>B Medicine</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{site}/">
<meta http-equiv="refresh" content="0; url={site}/">
<script>location.replace("{site}" + location.pathname + location.search + location.hash);</script>
<style>body{{font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;background:#F7FBFC;
color:#1A1A1A;display:grid;place-items:center;min-height:90vh;margin:0}}a{{color:#BC1922}}</style>
</head>
<body><p>B Medicine is now at <a href="{site}/">{name}</a>.</p></body>
</html>
"""


def build_forward():
    """bmedicine.net's own small site: the same page at bemedicine.github.io, wherever the visitor arrives."""
    if FORWARD.exists():
        shutil.rmtree(FORWARD)
    FORWARD.mkdir()
    page = FORWARD_PAGE.format(site=SITE_URL, name=SITE_URL.split("//")[1])
    (FORWARD / "index.html").write_text(page, encoding="utf-8")
    (FORWARD / "404.html").write_text(page, encoding="utf-8")
    (FORWARD / "CNAME").write_text(FORWARDING_NAME + "\n")
    (FORWARD / ".nojekyll").write_text("")
    (FORWARD / "robots.txt").write_text("User-agent: *\nDisallow:\n")


def check(pages):
    problems = []
    for rel, url, page in pages:
        visible = re.sub(r"<[^>]+>", " ", page)
        if "—" in page or re.search(r"\s–\s", visible):
            problems.append(f"{rel}: an em or en dash")
        if re.search(r"\{\{|\[n\]|\[date", page):
            problems.append(f"{rel}: a placeholder is left")
        for ref in re.findall(r'(?:href|src)="(/[^"#?]*)', page):
            target = OUT / ref.lstrip("/")
            if not (target.is_file() or (target / "index.html").is_file()):
                problems.append(f"{rel}: {ref} leads nowhere")
    return problems


def main():
    pages = build()
    build_forward()
    problems = check(pages)
    for rel, url, _ in pages:
        print(f"{url:22} <- src/{rel.as_posix()}")
    print("\n".join(problems) if problems else "Checks passed: links, images, dashes, placeholders.")
    if "--serve" in sys.argv:
        import functools, http.server
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        print("Preview: http://localhost:8642 (Ctrl-C to stop)")
        http.server.ThreadingHTTPServer(("127.0.0.1", 8642), handler).serve_forever()
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
