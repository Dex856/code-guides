# Code Guides — status & next steps

_Last updated: 2026-10-02_

## Done and verified

| Deliverable | File | Verified |
|---|---|---|
| Python guide (25 chapters, full language reference) | `site/python-guide.html` (357 KB) | ✅ 0 parser errors, 96 runnable snippets, 34 SVG figures |
| **C++ for LeetCode** (16 chapters, STL-first) | `site/cpp-guide.html` (168 KB) | ✅ 0 parser errors, 34 snippets compile-checked with g++ 14 / C++20 |
| **Java for LeetCode** (16 chapters, Collections-first) | `site/java-guide.html` (248 KB) | ✅ 0 parser errors, 63 snippets compile-checked with javac 11, 13 SVG figures |
| Site hub | `site/index.html` | ✅ all internal links resolve |
| **Question banks, topics 1–7** — Arrays & Strings · Two Pointers & Sliding Window · Hashing & Frequency Maps · Stacks, Queues & Monotonic Structures · Binary Search & Sorted Structures · Linked Lists · Trees & BSTs · 210 problems (42 easy · 84 medium · 84 hard) | `site/{cpp,java,python}-leetcode.html` | ✅ **all 210 C++ and 210 Java solutions compile** (judge-API stubs included so every snippet is self-contained); Python solutions pass 250 example checks plus thousands of randomised brute-force comparisons; documented example inputs cross-checked against LeetCode where they were transcribed from memory |
| GitHub Pages workflow | `.github/workflows/pages.yml` | ✅ pages artifact + deploy job |
| One-command publisher | `push.sh` | ✅ ready (needs a token, see below) |
| Rebuild script | `site/build-all.sh` | ✅ regenerates both guides + the three banks |

## Question banks — remaining work

The bank engine is finished: `site/leetcode/build.py` renders **one** authored bank into the three
language pages, so each problem is written once and appears with C++, Java and Python solutions.

**Topics 8–16 still to author** (270 problems per language):

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

## Authoring workflow (per topic — keep identical)

1. Write `site/leetcode/bank_NN_<topic>.py`: `TOPIC` metadata + exactly 6 Easy / 12 Medium / 12 Hard, in a constant slope.
2. Compile sweep: C++ `g++ -std=c++20 -fsyntax-only` (wrapped in `namespace snip`), Java `javac` (wrapped in `class Snip`, never `public`),
   Python `compile()`. Judge-provided APIs (`isBadVersion`, `MountainArray`, …) must be declared inside the snippet so it stands alone.
3. Behavioural check: run every documented example against the Python solution, then brute-force the tricky problems on hundreds of random
   small inputs. When a check fails, decide which side is wrong before "fixing" anything — several apparent failures were bad expectations.
4. Example values taken from memory are the riskiest part: cross-check them against LeetCode's own statement before finishing a topic.
   `POST https://leetcode.com/graphql` with `{"query":"query($t:String!){question(titleSlug:$t){content difficulty}}","variables":{"t":"<title-slug>"}}`
   returns the official examples (no auth needed) — two inputs in topic 5 were mis-remembered and this is how they were caught.
5. Unique Python function names inside one topic (several LeetCode problems are all called `search` or `findKthNumber`).
6. `bash site/build-all.sh` (rebuilds pages, mirrors `docs/`, link check) → commit → push.

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
