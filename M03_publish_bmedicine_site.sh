#!/bin/zsh
# Publishes bmedicine.net from this Mac (1 Nov 2026): builds and checks the site, commits every change in this
# folder and pushes it to main on github.com/Alsinbili/bmedicine.net; GitHub then rebuilds and publishes the site
# within a minute or two (.github/workflows/publish.yml). Run only when the user has said to publish.
#   zsh M03_publish_bmedicine_site.sh "What changed"
set -eu
cd ${0:A:h}
python3 -B M02_build_bmedicine_site.py
git add -A
git diff --cached --quiet || git commit -q -m "${1:-Update the site}"
git push -q origin main
echo "Pushed. GitHub publishes it at https://bmedicine.net within a minute or two (see the Actions tab)."
