#!/bin/zsh
# Publishes B Medicine's site (1 Nov 2026). Builds site/ and forward/ from src/ (stopping if the checks fail),
# then puts site/ on the gh-pages branch of github.com/bmedicine/bmedicine.github.io, which GitHub Pages serves at
# https://bmedicine.github.io, and forward/ on the gh-pages branch of github.com/Alsinbili/bmedicine.net, which
# serves the name bmedicine.net and sends every visitor to the same page on bmedicine.github.io. The source goes
# to the main branch of the first with an ordinary commit and push. Run only when the user has said to publish.
#   zsh M03_publish_bmedicine_site.sh "What changed"
set -eu
here=${0:A:h}
note=${1:-Update the site}

python3 -B "$here/M02_build_bmedicine_site.py"

publish() {   # publish <folder> <repository>
    local stage=$(mktemp -d)
    cp -R "$1/." "$stage/"
    (
        cd "$stage"
        git init -q -b gh-pages
        git config user.name "Ahmed Alsinbili"
        git config user.email "77195543+Alsinbili@users.noreply.github.com"
        git add -A
        git commit -q -m "Publish: $note"
        git push -q -f "$2" gh-pages
    )
    rm -rf "$stage"
    echo "Published $1:t to $2"
}

publish "$here/site" https://github.com/bmedicine/bmedicine.github.io.git
publish "$here/forward" https://github.com/Alsinbili/bmedicine.net.git
echo "GitHub Pages updates both within a minute or two."
