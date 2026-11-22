#!/usr/bin/env bash
# Build the report. Three passes: the first starts with no .aux, so its citations
# print as [?] and the pagination shifts once they resolve. Two passes leave the
# PDF from the second, which is still one page-break behind the real text.
set -euo pipefail
cd "$(dirname "$0")"
rm -f main.aux main.out
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode main.tex > build.log 2>&1 || {
    echo "pdflatex failed on pass $pass:"; tail -25 build.log; exit 1; }
  if grep -q "LaTeX Warning: Label(s) may have changed" build.log; then
    echo "pass $pass: labels still moving"
  fi
done
if grep -qE "LaTeX Warning: (Reference|Citation).* undefined" build.log; then
  echo "WARNING: unresolved references in the final pass:"; grep -E "undefined" build.log | head
fi
cp main.pdf F21DL_Group15_Report.pdf
rm -f main.aux main.out main.log build.log
echo "built F21DL_Group15_Report.pdf"
pdfinfo F21DL_Group15_Report.pdf | grep -E "Pages|Page size"
