#!/usr/bin/env bash
# Build the report. Two passes are needed so cross-references settle.
set -euo pipefail
cd "$(dirname "$0")"
pdflatex -interaction=nonstopmode main.tex > build.log 2>&1
pdflatex -interaction=nonstopmode main.tex > build.log 2>&1
cp main.pdf F21DL_Group15_Report.pdf
rm -f main.aux main.out main.log build.log
echo "built F21DL_Group15_Report.pdf"
pdfinfo F21DL_Group15_Report.pdf | grep -E "Pages|Page size"
