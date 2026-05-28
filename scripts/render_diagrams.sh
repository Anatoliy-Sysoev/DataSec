#!/usr/bin/env bash
set -euo pipefail

mkdir -p images/plantuml images/mermaid

if command -v plantuml >/dev/null 2>&1; then
  plantuml -tpng -o ../images/plantuml plantuml/*.puml
else
  echo "plantuml not found, skipping PlantUML render"
fi

if command -v mmdc >/dev/null 2>&1; then
  for file in mermaid/*.mmd; do
    name=$(basename "$file" .mmd)
    mmdc -i "$file" -o "images/mermaid/${name}.png"
  done
else
  echo "mmdc not found, skipping Mermaid render"
fi
