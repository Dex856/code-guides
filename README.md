# Code Guides — C++, Java &amp; Python for LeetCode

Self-contained, offline study material for coding interviews: three language guides plus matching
LeetCode-style question banks, published as a static site with GitHub Pages.

**Live site:** <https://Dex856.github.io/code-guides/>

## Contents

| Page | What it is |
|---|---|
| [`index.html`](site/index.html) | Hub with a side-by-side language comparison |
| [`cpp-guide.html`](site/cpp-guide.html) | **C++ for LeetCode** — 16 chapters: STL containers and algorithms, comparators, pitfalls, paste-ready templates, complexity planning, interview Q&amp;A |
| [`java-guide.html`](site/java-guide.html) | **Java for LeetCode** — 16 chapters: Collections framework, boxing and overflow, the JVM cost model, sorting and Comparators, templates, interview Q&amp;A |
| [`python-guide.html`](site/python-guide.html) | **Ultimate Python Guide** — 25 chapters, the full language reference from version history to packaging, concurrency and performance |
| [`cpp-leetcode.html`](site/cpp-leetcode.html) | C++ question bank — per topic: 6 easy · 12 medium · 12 hard |
| [`java-leetcode.html`](site/java-leetcode.html) | Java question bank — same problems, Java solutions |
| [`python-leetcode.html`](site/python-leetcode.html) | Python question bank — same problems, Python solutions |

## Design rules

* **No external requests.** CSS, JavaScript and every diagram (inline SVG) ship inside each HTML file — no CDN, no web fonts, no analytics.
* **Works offline.** Download the repository and open `site/index.html`; search (`/`), the theme toggle, copy buttons and print/PDF all work from `file://`.
* **One file per guide.** Each guide is a single HTML document, so it can be emailed, archived or read on a phone.

## Repository layout

```
site/                     the published site (this is what GitHub Pages serves)
  index.html              hub
  *-guide.html            the three guides (generated)
  *-leetcode.html         the three question banks (generated)
  cpp/part*.html          C++ guide sources — edit these, never the merged file
  java/part*.html         Java guide sources
  leetcode/build.py       bank renderer: one authored bank → three language pages
  leetcode/bank_*.py      the authored problems (one file per topic)
  build-all.sh            rebuild every generated page
.github/workflows/pages.yml   GitHub Pages deployment
push.sh                   one-command publish (create repo, push, enable Pages)
ROADMAP.md                what is finished and what is still being written
PUBLISHING.md             how to publish, and how to revoke a token afterwards
```

## Rebuilding

```bash
site/build-all.sh          # regenerates both guides and the three bank pages
cd site && python3 -m http.server 8000    # local preview at http://localhost:8000
```

## Progress

Both language guides are complete and verified: every C++ snippet compiles with GCC 14 (`-std=c++17/20`),
every Java snippet compiles with `javac`, and each guide's HTML validates with zero unclosed tags.

The question-bank engine and **topic 1 of 16** are done: 30 problems (6 easy · 12 medium · 12 hard) with
statements, examples, constraints, approaches, three complete solutions each and stated complexity —
90 verified solutions so far. Topics 2–16 are listed in [ROADMAP.md](ROADMAP.md).
