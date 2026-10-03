# Code Guides — C++, Java and Python for LeetCode

Three self-contained, offline guides plus matching LeetCode question banks, published as a static site.

| Page | What it is |
|---|---|
| `index.html` | Hub page with the language comparison table |
| `cpp-guide.html` | **C++ for LeetCode** — 16 chapters: STL, comparators, pitfalls, templates, interview Q&A |
| `practice.html` | **Practice terminal** — run Python / C++ / Java for any of the 480 problems (needs `python3 tools/practice_server.py`) |
| `java-guide.html` | **Java for LeetCode** — 16 chapters: Collections, boxing, JVM costs, templates, interview Q&A |
| `python-guide.html` | **Ultimate Python Guide** — 25 chapters, the full language reference |
| `cpp-leetcode.html` | C++ question bank — per topic: 6 easy · 12 medium · 12 hard |
| `java-leetcode.html` | Java question bank — same topics, Java solutions |
| `python-leetcode.html` | Python question bank — same topics, Python solutions |

## Design rules

* **No external requests.** Everything is inlined: CSS, JavaScript, SVG diagrams. No CDN, no fonts, no analytics.
* **Works offline.** Download the folder and open `index.html`; every feature (search with `/`, theme toggle, copy
  buttons, print/PDF) works from `file://`.
* **One file per guide.** Each guide is a single HTML document so it can be emailed, archived or read on a phone.

## Local preview

```bash
python3 -m http.server 8000     # from this directory
# → http://localhost:8000
```

## Publishing to GitHub Pages

```bash
GH_TOKEN=<fine-grained PAT with Contents + Pages write> ./push.sh code-guides
```

The included workflow (`.github/workflows/pages.yml`) uploads the `site/` directory as a Pages artifact on every push to
`main`, so the URL becomes `https://<owner>.github.io/<repo>/`.

## Rebuilding a guide

Each guide is assembled by concatenating its parts in filename order:

```bash
bash site/build-all.sh        # guides + banks + problems.json + the docs/ mirror
```

That assembles `cpp-guide.html` from `cpp/part*.html`, `java-guide.html` from `java/part*.html`, regenerates the three
banks with `site/leetcode/build.py`, refreshes `site/leetcode/problems.json` with `build_bank_json.py` (the data behind
the practice terminal), and copies everything into the `docs/` mirror the Pages workflow serves.

Edit the `part*.html` sources, never the merged guide file. Question banks are generated from the per-topic Python
sources `site/leetcode/bank_*.py`, which carry the same problems in C++, Java and Python.
