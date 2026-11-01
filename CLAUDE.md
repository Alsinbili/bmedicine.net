# bmedicine.net: how to edit the site

This repository is the website of **B Medicine** (a trading name of Dr Ahmed Alsinbili): his cardiology teaching
and Hub, his Mac app. It is a plain static site: hand-written HTML and one CSS file, built by a small Python
script, served free by GitHub Pages at https://bmedicine.net. The owner edits it by talking to Claude, on his Mac
or from claude.ai.

## Where things are

| Path | What |
|---|---|
| `src/_layout.html` | The header, menu and footer of every page |
| `src/index.html` | Home: hero, Teaching (lectures and videos), Apps (Hub), About, Contact |
| `src/hub/index.html` | Hub's page; `src/hub/support/`, `privacy/`, `terms/` are the pages App Store Connect links to |
| `src/privacy/index.html` | The site's own privacy note |
| `src/404.html` | Page not found |
| `src/assets/site.css` | All styling; colours are variables at the top |
| `src/assets/img/` | Logo, B mark, favicon, Hub's icon and screenshots (PNG) |
| `M02_build_bmedicine_site.py` | Builds `src/` into `site/` and checks it (links, images, dashes, placeholders) |
| `.github/workflows/publish.yml` | Every push to `main` builds and publishes the site |

Each page in `src/` starts with an HTML comment holding `title`, `description`, `og_image`, `body_class` and, on
policy pages, `updated`; the rest is the page's content. `{{hub_subnav:<page>}}` puts Hub's own menu on Hub's
pages. The page's address follows its place: `src/hub/privacy/index.html` is `/hub/privacy/`.

## How to make a change

1. Edit the files in `src/` (never `site/`, which the build makes).
2. Run `python3 -B M02_build_bmedicine_site.py`; it must end with "Checks passed".
3. Preview with `python3 -B M02_build_bmedicine_site.py --serve` (http://localhost:8642) and show the owner.
4. **Publish only on the owner's word.** Publishing means getting the change onto `main`: on his Mac,
   `zsh M03_publish_bmedicine_site.sh "What changed"`; in a cloud session, a pull request he merges. GitHub then
   publishes within a minute or two.

## The owner's rules for anything written here

- No em dashes, and no en dashes as punctuation. British English. Plain, factual, conservative wording: no
  hyperbole, no "every/all/never" claims, no promotional verbs.
- His details: Dr Ahmed Alsinbili, MRCP, MSc, MB ChB, AFHEA, RCP Educator; Cardiology Registrar, Oxford University
  Hospitals NHS Foundation Trust; Clinical Research Fellow, University of Oxford. Contact: bmedicineuk@gmail.com.
- Keep Oxford, the NHS and Anthropic out of Hub's pages, with no suggestion of endorsement. Hub's pages say Hub is
  made by "B Medicine (Ahmed Alsinbili)" and is not made by, affiliated with or endorsed by Anthropic.
- The teaching is for healthcare professionals and students, not medical advice for patients.
- The site sets no cookies, has no analytics and loads nothing from other companies (system fonts, local images,
  no embedded videos: lectures and videos are linked). Keep it that way unless the owner decides otherwise, and
  then update `src/privacy/index.html` first.
- What Hub's pages say must match what Hub does. If Hub's privacy, prices or features change, change the pages
  (and the date at the top of a policy page) in the same piece of work.
- Images: PNG. The B logo is B Medicine's own mark: use the files in `src/assets/img/` as they are.
