# Code Guides — status & next steps

_Last updated: 2026-10-02_

## Done and verified

| Deliverable | File | Verified |
|---|---|---|
| Python guide (25 chapters, full language reference) | `site/python-guide.html` (357 KB) | ✅ 0 parser errors, 96 runnable snippets, 34 SVG figures |
| **C++ for LeetCode** (16 chapters, STL-first) | `site/cpp-guide.html` (168 KB) | ✅ 0 parser errors, 34 snippets compile-checked with g++ 14 / C++20 |
| **Java for LeetCode** (16 chapters, Collections-first) | `site/java-guide.html` (248 KB) | ✅ 0 parser errors, 63 snippets compile-checked with javac 11, 13 SVG figures |
| Site hub | `site/index.html` | ✅ all internal links resolve |
| **Question banks, topics 1–4** — Arrays & Strings, Two Pointers & Sliding Window, Hashing & Frequency Maps, Stacks/Queues/Monotonic Structures · 120 problems (24 easy · 48 medium · 48 hard) | `site/{cpp,java,python}-leetcode.html` | ✅ **all 120 C++ and 120 Java solutions compile**; Python solutions pass 190 example checks plus thousands of randomised brute-force comparisons (monotonic stacks, parsers, ring buffer, stock spanner, car fleets) |
| GitHub Pages workflow | `.github/workflows/pages.yml` | ✅ pages artifact + deploy job |
| One-command publisher | `push.sh` | ✅ ready (needs a token, see below) |
| Rebuild script | `site/build-all.sh` | ✅ regenerates both guides + the three banks |

## Question banks — remaining work

The bank engine is finished: `site/leetcode/build.py` renders **one** authored bank into the three
language pages, so each problem is written once and appears with C++, Java and Python solutions.

**Topics 5–16 still to author** (360 problems per language):

5. Binary Search & Sorted Structures
6. Linked Lists
7. Trees & BSTs
8. Graphs & Union-Find
9. Dynamic Programming
10. Greedy & Intervals
11. Heaps, Top-K & Design
12. Tries & String Algorithms
13. Backtracking & Recursion
14. Bit Manipulation
15. Math & Number Theory
16. Prefix Sums & Range Queries

Each topic is a single file `site/leetcode/bank_NN_<slug>.py` holding `TOPIC` (metadata) and `PROBLEMS`
(30 entries, each with statement, examples, constraints, approach, three solutions and complexity).
Adding a file and running `python3 site/leetcode/build.py` is all that is needed — the pages, the table
of contents and the search index update automatically.

## GitHub deployment

The repository content is ready; publishing needs a credential the sandbox does not have. Two options:

1. **You paste a fine-grained PAT** (Contents: read/write, Pages: read/write) and I run
   `GH_TOKEN=… ./push.sh code-guides` — this also creates the repository and enables Pages.
2. **You run it yourself**: create an empty repo, then from the workspace root run
   `GH_TOKEN=<token> ./push.sh <repo-name>`.

Pages then serves `https://<owner>.github.io/<repo>/` on every push to `main`.

## Local preview

```bash
cd site && python3 -m http.server 8000     # http://localhost:8000
```
