#!/usr/bin/env bash
# Rebuild every generated page in the site from its sources.
# Sources: site/cpp/part*.html · site/java/part*.html · site/leetcode/bank_*.py
set -euo pipefail
cd "$(dirname "$0")"

echo "→ C++ guide"
python3 - <<'PY'
import pathlib
parts = sorted(pathlib.Path("cpp").glob("part*.html"), key=lambda p: int(p.stem[4:]))
pathlib.Path("cpp-guide.html").write_text("".join(p.read_text() for p in parts))
print("   cpp-guide.html", f"{pathlib.Path('cpp-guide.html').stat().st_size/1024:.1f} KB")
PY

echo "→ Java guide"
python3 - <<'PY'
import pathlib
parts = sorted(pathlib.Path("java").glob("part*.html"), key=lambda p: int(p.stem[4:]))
pathlib.Path("java-guide.html").write_text("".join(p.read_text() for p in parts))
print("   java-guide.html", f"{pathlib.Path('java-guide.html').stat().st_size/1024:.1f} KB")
PY

echo "→ LeetCode banks"
python3 leetcode/build.py
python3 leetcode/build_bank_json.py

echo "→ link check (local files referenced by the pages must exist)"
python3 - <<'PY'
import pathlib, re
missing = []
for page in pathlib.Path(".").glob("*.html"):
    for m in re.finditer(r'href="(?!https?:|#|mailto:)([^"#]+)', page.read_text()):
        link = m.group(1)
        if "'" in link or "+" in link or link.startswith("api/"):   # runtime / API routes
            continue
        target = (page.parent / link.split("?")[0]).resolve()
        if not target.exists():
            missing.append(f"{page.name} -> {link}")
print("   missing links:", missing if missing else "none")
PY
echo "done."

echo "→ docs/ mirror (branch-deployable copy of the site, for Pages from a branch)"
python3 - <<'PY'
import pathlib, re, shutil
site = pathlib.Path(".")                 # build-all.sh runs inside site/
docs = pathlib.Path("../docs")           # docs/ must sit at the repository root
docs.mkdir(exist_ok=True)
names = ["index.html", "cpp-guide.html", "java-guide.html", "python-guide.html",
         "cpp-leetcode.html", "java-leetcode.html", "python-leetcode.html", "practice.html",
         "leetcode/problems.json", ".nojekyll"]
for n in names:
    (docs / n).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(site / n, docs / n)
for f in docs.glob("*.html"):
    f.write_text(f.read_text().replace('href="../', 'href="'))
missing = []
for f in docs.glob("*.html"):
    for m in re.finditer(r'href="(?!https?:|#|mailto:)([^"#]+)', f.read_text()):
        link = m.group(1)
        if "'" in link or "+" in link or link.startswith("api/"):   # runtime / API routes
            continue
        if not (docs / link.split("?")[0]).exists():
            missing.append(f"{f.name} -> {link}")
print("   docs/ updated:", len(names), "files · missing links:", missing or "none")
PY
echo "done."
