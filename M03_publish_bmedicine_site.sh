#!/bin/zsh
# Publishes bmedicine.net (1 Nov 2026): builds site/ from src/ (stopping if the checks fail), then puts site/ on
# the gh-pages branch of github.com/Alsinbili/bmedicine.net, which GitHub Pages serves. The source itself goes to
# the main branch with an ordinary commit and push. Run only when the user has said to publish.
#   zsh M03_publish_bmedicine_site.sh "What changed"
set -eu
here=${0:A:h}
note=${1:-Update the site}
repo=https://github.com/Alsinbili/bmedicine.net.git

python3 -B "$here/M02_build_bmedicine_site.py"

stage=$(mktemp -d)
cp -R "$here/site/." "$stage/"
cd "$stage"
git init -q -b gh-pages
git config user.name "Ahmed Alsinbili"
git config user.email "77195543+Alsinbili@users.noreply.github.com"
git add -A
git commit -q -m "Publish: $note"
git push -q -f "$repo" gh-pages
cd /
rm -rf "$stage"
echo "Published to the gh-pages branch; GitHub Pages updates bmedicine.net within a minute or two."
