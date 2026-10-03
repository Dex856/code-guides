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
| [`practice.html`](site/practice.html) | **Practice terminal** — write, compile and run Python / C++ / Java against any of the 480 problems |

## Practice terminals

`site/practice.html` is a three-language scratch pad wired to the 480-problem bank:

* pick any problem from the picker (grouped by topic) — statement, examples, constraints and approach appear on the left;
* **Starter** loads the skeleton for the current language, **Load solution** loads the complete, verified solution;
* **Run** compiles and executes the code and prints stdout, stderr, the exit code and wall-clock time;
* when the program's output matches the problem's first official example, the page says so.

Compilers cannot live inside a static HTML file, so the page talks to a small local runner that ships with the project:

```bash
python3 tools/practice_server.py          # serves site/ on http://localhost:8000
# then open http://localhost:8000/practice.html
```

It needs `python3`, `g++` and `javac` on the machine. Every run happens in a temporary directory with a 10-second time
limit, a 30-second compile limit, a 512 MB memory cap and truncated output — nothing leaves your computer.

The copy on GitHub Pages is static: it still loads all 480 problems and lets you edit, save and copy code, and it says
plainly that running needs the local server. Deep links work both ways — every problem in the banks has a
**⌨ practice it** link straight into the terminal (`practice.html?p=<slug>`).

Every runnable demo is executed against its problem's first official example by `tools/check_demos.py`
(`python3 tools/check_demos.py --lang python|cpp|java`):

| language | demos | exact match | alt formatting | prints nothing | alternate valid answer | broken |
|---|---|---|---|---|---|---|
| Python | 262 | 252 | 4 | 3 | 5 | 0 |
| C++ | 242 | 229 | 6 | 2 | 7 | 0 |
| Java | 235 | 223 | 5 | 2 | 7 | 0 |

The three languages never disagree with each other; the "alt" and "alternate valid answer" rows are problems that
accept several correct outputs (`subsets`, `remove-invalid-parentheses`, `sliding-window-median`, …) or print with a
different but equivalent formatting.

Try it end to end with the checks that built it:

```bash
python3 tools/practice_server.py 8000 &    # 1. start the runner
python3 tools/e2e_practice.py 6            # 2. shipped demos vs official examples, over HTTP
node tools/practice_test.js                # 3. page UI (add STATIC=1 for the Pages fallback)
```

## Design rules

* **One command to rebuild.** `bash site/build-all.sh` regenerates the guides from `site/*/part*.html`, the three banks from `site/leetcode/bank_*.py`, `problems.json` for the terminal, and the `docs/` mirror.
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
