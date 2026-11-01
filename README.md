# bmedicine.net

The website of B Medicine: teaching by Dr Ahmed Alsinbili, and Hub, a Mac app for projects.

- `src/` holds the pages (`_layout.html` is the header and footer of every page).
- `python3 -B M02_build_bmedicine_site.py` builds them into `site/` and checks links, images and wording;
  `--serve` previews the site at http://localhost:8642.
- Every push to `main` rebuilds the site and publishes it at https://bmedicine.net
  (`.github/workflows/publish.yml`).
- `CLAUDE.md` tells Claude how to edit the site.
