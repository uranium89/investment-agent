#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
SRC=..

# Manual mapping: filename_slug "Display Title"
pages=(
  architecture "Kiến trúc hệ thống"
  mvp-status "MVP Status"
  pipeline-guide "Hướng dẫn vận hành Pipeline"
  strategy "Chiến lược VMQ30"
  risk-management "Quản trị rủi ro"
  roadmap "Lộ trình phát triển"
)

i=0
while [ $i -lt ${#pages[@]} ]; do
  slug="${pages[$i]}"
  title="${pages[$((i+1))]}"
  md="${slug}.md"
  html="${slug}.html"
  i=$((i+2))

  echo "→ $md → $html  ($title)"

  pandoc "$SRC/$md" \
    --template template.html \
    --metadata title="$title" \
    --toc --toc-depth 2 \
    -o "$html"

  sed -i '' "s|href=\"${html}\"|href=\"${html}\" class=\"active\"|" "$html"
done

echo "✅ All pages generated in docs/html/"
