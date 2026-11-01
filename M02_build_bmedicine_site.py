#!/usr/bin/env python3
"""Builds B Medicine's site from src/ into site/ (1 Nov 2026). Plain Python 3, nothing to install.

    python3 -B M02_build_bmedicine_site.py            # build site/
    python3 -B M02_build_bmedicine_site.py --serve    # build, then preview at http://localhost:8642

src/_layout.html is the frame of every page (header, footer). Each other .html file in src/ is one page: an
HTML comment at its top gives title, description, og_image, body_class and, for policies, updated; the rest is
the page's content. {{hub_subnav:<page>}} puts Hub's own menu on Hub's pages. Pages keep their place:
src/hub/privacy/index.html becomes bmedicine.net/hub/privacy/. src/assets/ is copied as it is.

The site lives at https://bmedicine.net, served free by GitHub Pages from github.com/Alsinbili/bmedicine.net.
Every push to that repository's main branch rebuilds and publishes it (.github/workflows/publish.yml).

The build checks what it can: every internal link and image leads somewhere, no em or en dashes in the text,
no placeholder left. site/ is what gets published; never edit it by hand.
"""
import datetime, html, re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC, OUT = HERE / "src", HERE / "site"
SITE_URL = "https://bmedicine.net"
DOMAIN = "bmedicine.net"

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
    (OUT / "CNAME").write_text(DOMAIN + "\n")
    (OUT / ".nojekyll").write_text("")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    urls = "".join(f"  <url><loc>{SITE_URL}{u}</loc></url>\n" for r, u, _ in pages if r.name != "404.html")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     f"{urls}</urlset>\n")
    return pages


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
