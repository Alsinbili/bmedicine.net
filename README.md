# B Medicine's website

The website of B Medicine: teaching by Dr Ahmed Alsinbili, and Hub, a Mac app for projects.
It lives at https://bemedicine.github.io; the name bmedicine.net forwards there.

`src/` holds the pages; `python3 -B M02_build_bmedicine_site.py` builds them into `site/` (and the small
forwarding site for bmedicine.net into `forward/`) and checks the links; `--serve` previews the site at
http://localhost:8642. The `gh-pages` branch holds the built site that GitHub Pages serves.
