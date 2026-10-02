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

echo "→ link check (local files referenced by the pages must exist)"
python3 - <<'PY'
import pathlib, re
missing = []
for page in pathlib.Path(".").glob("*.html"):
    for m in re.finditer(r'href="(?!https?:|#|mailto:)([^"#]+)', page.read_text()):
        target = (page.parent / m.group(1)).resolve()
        if not target.exists():
            missing.append(f"{page.name} -> {m.group(1)}")
print("   missing links:", missing if missing else "none")
PY
echo "done."
