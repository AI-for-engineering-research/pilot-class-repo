#!/usr/bin/env bash
#
# Build the class site into ./_site for GitHub Pages.
# Static for now (no generator), but this is the one place to assemble the
# published output — keep it the single source of truth for what ships.
#
# Local preview:
#   ./build.sh && python3 -m http.server -d _site 8000   # http://localhost:8000
#
set -euo pipefail

OUT="_site"
rm -rf "$OUT"
mkdir -p "$OUT"

# Landing page.
cp index.html "$OUT/"

# Session pages: publish the deck, plan, and light media. The raw multi-hundred-MB
# screen capture and frame dumps are gitignored (absent in CI) and never copied,
# so this stays safe both locally and on the runner.
if [ -d session-1 ]; then
  mkdir -p "$OUT/session-1/assets"
  cp session-1/lesson1.html      "$OUT/session-1/"
  cp session-1/session-1-plan.md "$OUT/session-1/"
  # Quiz QR code shown on the diagnostic slide (lesson1.html references assets/aistuff.png).
  [ -f session-1/assets/aistuff.png ] && cp session-1/assets/aistuff.png "$OUT/session-1/assets/"
  [ -f session-1/assets/making-of.mp4 ] && cp session-1/assets/making-of.mp4 "$OUT/session-1/assets/"
fi

# Student-project thumbnails, once they exist:
#   cp -R thumbs "$OUT/thumbs"

echo "Built $(find "$OUT" -type f | wc -l | tr -d ' ') file(s) into $OUT/:"
find "$OUT" -type f | sed "s|^$OUT/|  |" | sort
