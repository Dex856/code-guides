#!/usr/bin/env python3
"""
Build the LeetCode question-bank pages.

    python3 site/leetcode/build.py

Reads every  bank_*.py  module in this folder (sorted by filename), each of which
defines  TOPIC  (metadata) and  PROBLEMS  (a list of dicts), and renders three
standalone pages:

    site/cpp-leetcode.html
    site/java-leetcode.html
    site/python-leetcode.html

Every page is self-contained: inline CSS, inline SVG (none needed in entries),
inline JS with search / TOC / copy buttons / theme. No external requests.

Difficulty contract: each topic must contain exactly
    6 Easy  ·  12 Medium  ·  12 Hard
in gentle, monotonically increasing order (easy 1→6, medium 1→12, hard 1→12).
"""
from __future__ import annotations

import importlib.util
import html
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent
LANGS = ["cpp", "java", "python"]

LANG_META = {
    "cpp": dict(
        guide="cpp-guide.html", title="C++ LeetCode Question Bank",
        brand="C++ bank", sub="C++17/20/23 solutions · compiled with g++ 14",
        accent="#5b4b8a", accent2="#b07219", key="cppb-theme",
        keywords=("alignas alignof and asm auto bool break case catch char class concept const consteval constexpr "
                  "constinit const_cast continue co_await co_return co_yield decltype default delete do double "
                  "dynamic_cast else enum explicit export extern false float for friend goto if inline int long "
                  "mutable namespace new noexcept nullptr operator or private protected public register "
                  "reinterpret_cast requires return short signed sizeof static static_assert static_cast struct "
                  "switch template this throw true try typedef typeid typename union unsigned using virtual void "
                  "volatile while xor override final not").split(),
        builtins=("vector string map set unordered_map unordered_set multiset multimap queue deque stack "
                  "priority_queue pair tuple array bitset sort stable_sort min_element max_element accumulate "
                  "lower_bound upper_bound binary_search equal_range unique reverse rotate iota gcd lcm "
                  "min max abs swap next_permutation emplace_back push_back pop_back reserve resize substr "
                  "find npos size begin end rbegin push pop top front back emplace count cout cin endl "
                  "make_pair tie move to_string stoi stoll push_rear").split(),
        extra_builtins=["ListNode", "TreeNode", "Solution", "DSU", "Node", "Trie", "greater", "less"],
    ),
    "java": dict(
        guide="java-guide.html", title="Java LeetCode Question Bank",
        brand="Java bank", sub="Java 21/25 solutions · Java 11-compatible where marked",
        accent="#b07219", accent2="#0f766e", key="javab-theme",
        keywords=("abstract assert boolean break byte case catch char class const continue default do double else "
                  "enum extends final finally float for if implements import instanceof int interface long native "
                  "new package private protected public return short static strictfp super switch synchronized this "
                  "throw throws transient try var void volatile while true false null record").split(),
        builtins=("System String StringBuilder Character Integer Long Double Float Boolean Math Arrays Collections "
                  "List ArrayList LinkedList Map HashMap LinkedHashMap TreeMap Set HashSet LinkedHashSet TreeSet "
                  "Deque ArrayDeque Queue PriorityQueue Stack Iterator Optional Stream Collectors BigInteger "
                  "BitSet Comparator Comparable Objects Random StringTokenizer BufferedReader InputStreamReader "
                  "StringTokenizer Map Entry Solution ListNode TreeNode DSU Trie Node").split(),
        extra_builtins=["Solution", "ListNode", "TreeNode", "DSU", "Trie"],
    ),
    "python": dict(
        guide="python-guide.html", title="Python LeetCode Question Bank",
        brand="Python bank", sub="Python 3.12+ solutions · idiomatic and fast",
        accent="#2f6f4f", accent2="#0f766e", key="pyb-theme",
        keywords=("and as assert async await break class continue def del elif else except finally for from global "
                  "if import in is lambda None nonlocal not or pass raise return True False try while with yield "
                  "match case self").split(),
        builtins=("list dict set tuple str int float bool len range enumerate zip sorted sort append pop insert "
                  "remove add update get setdefault defaultdict Counter deque heapify heappush heappop bisect_left "
                  "bisect_right lru_cache cache defaultdict accumulate combinations permutations product gcd lcm "
                  "isqrt sqrt inf defaultdict defaultdict deque Counter heapq bisect itertools functools math "
                  "collections typing Optional List Dict Set Tuple defaultdict").split(),
        extra_builtins=["TreeNode", "ListNode", "Node"],
    ),
}


# --------------------------------------------------------------------------- #
# subprocess-free module loading                                              #
# --------------------------------------------------------------------------- #
def load_banks() -> list[dict]:
    banks = []
    for path in sorted(HERE.glob("bank_*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)          # type: ignore[union-attr]
        banks.append({"topic": mod.TOPIC, "problems": mod.PROBLEMS, "file": path.name})
    return banks


def esc_code(code: str) -> str:
    return html.escape(code.strip("\n"), quote=False)


def inline_md(text: str) -> str:
    """Escape, then allow `code`, **bold** — the two markers used in statements."""
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    return text


DIFF_CLASS = {"Easy": "pill", "Medium": "pill", "Hard": "pill hot"}
PREFIX = {"Easy": "E", "Medium": "M", "Hard": "H"}


def render_problem(prob: dict, counters: dict, lang: str, flat: list, pos: dict) -> str:
    d = prob["difficulty"]
    counters[d] = counters.get(d, 0) + 1
    tag = f"{PREFIX[d]}{counters[d]}"
    pid = prob["slug"]
    i = pos[pid]
    prev = flat[i - 1] if i > 0 else None
    nxt = flat[i + 1] if i + 1 < len(flat) else None
    out = []
    out.append(f'  <section class="sub" id="{pid}" data-diff="{d}" data-slug="{pid}">')
    out.append(f'    <h3><span class="pn">{tag}</span> {inline_md(prob["title"])} '
               f'<span class="{DIFF_CLASS[d]}">{d}</span> <span class="muted small">· {inline_md(prob["pattern"])}</span>'
               f'<button class="donebtn" type="button" data-slug="{pid}" title="Mark this problem as done">✓ Done</button></h3>')
    out.append(f'    <p><b>Problem.</b> {inline_md(prob["statement"])}</p>')
    for i, ex in enumerate(prob.get("examples", []), 1):
        inp, outp = ex
        out.append(f'    <div class="ex"><div class="exh">Example {i}</div>'
                   f'<pre><code class="nohl">Input:  {inp}\nOutput: {outp}</code></pre></div>')
    cons = prob.get("constraints") or []
    if cons:
        out.append('    <p class="cons"><b>Constraints:</b> ' + "; ".join(inline_md(c) for c in cons) + ".</p>")
    out.append(f'    <p><b>Approach.</b> {inline_md(prob["approach"])}</p>')
    code = prob["code"][lang]
    out.append(f'    <pre><code>{esc_code(code)}</code></pre>')
    t, s = prob["complexity"]
    out.append(f'    <p class="cx"><b>Complexity:</b> {inline_md(t)} time · {inline_md(s)} space.</p>')
    # previous / next problem — keeps the gentle slope one click away
    left = (f'<a class="pnav-a prev" href="#{prev[0]}"><span class="d">{prev[1]}</span> {inline_md(prev[2])}</a>'
            if prev else '<span class="pnav-a off">start of the bank</span>')
    right = (f'<a class="pnav-a next" href="#{nxt[0]}"><span class="d">{nxt[1]}</span> {inline_md(nxt[2])}</a>'
             if nxt else '<span class="pnav-a off">end of the bank</span>')
    out.append(f'    <div class="pnav">{left}{right}</div>')
    out.append("  </section>")
    return "\n".join(out)


def flat_entries(banks: list[dict]) -> list[tuple]:
    """[(slug, label, title, difficulty, topic number)] in reading order."""
    flat = []
    for ti, bank in enumerate(banks, 1):
        seen: dict[str, int] = {}
        for prob in bank["problems"]:
            d = prob["difficulty"]
            seen[d] = seen.get(d, 0) + 1
            flat.append((prob["slug"], f"{PREFIX[d]}{seen[d]}", prob["title"], d, ti))
    return flat


def render_topic(idx: int, bank: dict, lang: str, flat: list, pos: dict) -> str:
    topic = bank["topic"]
    probs = bank["problems"]
    counters: dict[str, int] = {}
    body = [f'<section class="chapter" id="t{idx:02d}">',
            f'  <h2><span class="num">{idx}</span> {inline_md(topic["name"])}</h2>',
            f'  <p class="tagline">{inline_md(topic["tagline"])}</p>',
            '  <div class="card"><p><b>What this topic trains.</b> ' + inline_md(topic["focus"]) + '</p>',
            '<p class="small muted">Ordering: ' + inline_md(topic.get("ordering", "")) + '</p></div>']
    for prob in probs:
        body.append(render_problem(prob, counters, lang, flat, pos))
    body.append("</section>")
    return "\n".join(body)


def build_shell(lang: str, banks: list[dict]) -> str:
    meta = LANG_META[lang]
    counts = {"Easy": 0, "Medium": 0, "Hard": 0}
    for bank in banks:
        for prob in bank["problems"]:
            counts[prob["difficulty"]] += 1
    total = sum(counts.values())
    head = f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{meta["title"]} — C++, Java &amp; Python for LeetCode</title>
<meta name="description" content="{meta["title"]}: 16 topics, each with 6 easy, 12 medium and 12 hard problems with full statements, examples, constraints and complete commented solutions.">
<style>
:root{{
  --bg:#ffffff; --fg:#141b26; --muted:#57637a; --line:#e2e8f2; --card:#f5f8fd; --card2:#eef3fa;
  --accent:{meta["accent"]}; --accent-soft:#f1ecfb; --accent2:{meta["accent2"]};
  --warn:#b3342a; --warn-soft:#fdecea; --ok:#166534; --ok-soft:#e8f6ee; --zebra:#fafbfe;
  --code:#0d1425; --codefg:#e2ebf8; --shadow:0 1px 2px rgba(16,24,40,.06),0 8px 24px rgba(16,24,40,.06);
}}
html[data-theme=dark]{{
  --bg:#0c1117; --fg:#e6edf7; --muted:#95a3b8; --line:#212b3a; --card:#141c27; --card2:#1a2331;
  --accent-soft:#221a30; --zebra:#111823; --code:#080d16; --codefg:#e2ebf8;
  --shadow:0 1px 2px rgba(0,0,0,.5),0 8px 24px rgba(0,0,0,.35);
}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth;scroll-padding-top:104px}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15.5px/1.66 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}}
code,pre,kbd,.mono{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace}}
a{{color:var(--accent);text-decoration:none}} a:hover{{text-decoration:underline}}
#progress{{position:fixed;top:0;left:0;height:3px;background:linear-gradient(90deg,{meta["accent"]},{meta["accent2"]});width:0;z-index:60}}
.head{{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--bg) 94%,transparent);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}}
.topbar{{display:flex;gap:10px;align-items:center;padding:9px 16px;flex-wrap:wrap}}
.filterbar{{display:flex;gap:7px;align-items:center;flex-wrap:wrap;padding:0 16px 9px;font-size:12.6px}}
.brand{{display:flex;align-items:center;gap:9px;font-weight:700;white-space:nowrap}}
.brand .logo{{width:26px;height:26px;border-radius:7px;background:linear-gradient(145deg,{meta["accent"]},{meta["accent2"]});color:#fff;display:grid;place-items:center;font-size:12px;font-weight:800}}
.brand small{{font-weight:500;color:var(--muted);font-size:11.5px}}
.searchwrap{{position:relative;flex:1;max-width:560px;margin-left:auto}}
#q{{width:100%;padding:9px 34px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--fg);font-size:14px;outline:none}}
#q:focus{{border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}}
.searchwrap .hint{{position:absolute;right:9px;top:7px;font-size:11px;color:var(--muted);border:1px solid var(--line);border-radius:6px;padding:1px 6px;background:var(--bg)}}
#results{{position:absolute;top:46px;left:0;right:0;background:var(--bg);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);max-height:60vh;overflow:auto;display:none;padding:6px}}
#results.on{{display:block}}
#results a{{display:block;padding:7px 10px;border-radius:8px;color:var(--fg)}}
#results a:hover,#results a.sel{{background:var(--card2);text-decoration:none}}
#results .rp{{color:var(--muted);font-size:12px}}
.btn{{border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:9px;padding:7px 10px;font-size:13px;cursor:pointer;white-space:nowrap}}
.btn:hover{{border-color:var(--accent)}}
.layout{{display:grid;grid-template-columns:290px minmax(0,1fr);gap:28px;max-width:1440px;margin:0 auto;padding:0 18px 80px}}
#toc{{position:sticky;top:104px;align-self:start;max-height:calc(100vh - 128px);overflow:auto;padding:14px 6px 40px 0;font-size:13.4px;border-right:1px solid var(--line)}}
#toc .navhead{{font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);margin:8px 8px 6px}}
.navch>a{{display:block;padding:5px 9px;border-radius:8px;color:var(--fg);font-weight:600}}
.navch>a:hover{{background:var(--card);text-decoration:none}}
.navch.active>a{{background:var(--accent-soft);color:var(--accent)}}
.navch ul{{list-style:none;margin:0 0 6px;padding:0 0 0 10px;columns:1}}
.navch ul a{{display:block;padding:2px 8px;border-radius:6px;color:var(--muted);font-size:12.3px;border-left:2px solid var(--line)}}
.navch ul a:hover{{color:var(--accent);border-left-color:var(--accent);text-decoration:none;background:var(--card)}}
main{{min-width:0;padding-top:8px}}
@media(max-width:1030px){{.layout{{grid-template-columns:1fr}}#toc{{position:static;max-height:none;border-right:0;border-bottom:1px solid var(--line)}}}}
.hero{{margin:20px 0 6px;border:1px solid var(--line);border-radius:18px;padding:26px 24px;background:radial-gradient(1000px 340px at 4% -30%,rgba(91,75,138,.14),transparent 62%),var(--card)}}
.hero h1{{margin:0 0 6px;font-size:clamp(25px,4.2vw,38px);line-height:1.14;letter-spacing:-.4px}}
.hero p.lede{{color:var(--muted);font-size:15.6px;margin:.4rem 0 1rem;max-width:78ch}}
.badges{{display:flex;flex-wrap:wrap;gap:7px;margin-top:13px}}
.pill{{font-size:11.5px;border:1px solid var(--line);background:var(--bg);border-radius:999px;padding:3px 10px;color:var(--muted);white-space:nowrap}}
.pill.hot{{border-color:var(--warn);color:var(--warn)}}
.chapter{{margin:42px 0 0;scroll-margin-top:108px}}
.chapter>h2{{display:flex;align-items:center;gap:12px;font-size:clamp(19px,2.9vw,26px);margin:0 0 4px;letter-spacing:-.3px}}
.chapter>h2 .num{{flex:0 0 auto;display:grid;place-items:center;width:38px;height:38px;border-radius:11px;background:linear-gradient(145deg,{meta["accent"]},{meta["accent"]});color:#fff;font-size:14px;font-weight:700}}
.chapter>.tagline{{color:var(--muted);margin:0 0 6px;font-size:14.4px}}
.sub{{margin:26px 0 0;scroll-margin-top:108px;border-top:1px solid var(--line);padding-top:14px}}
.sub h3{{font-size:17.2px;margin:0 0 8px;display:flex;flex-wrap:wrap;align-items:center;gap:9px}}
.sub h3 .pn{{display:inline-grid;place-items:center;min-width:34px;height:26px;padding:0 7px;border-radius:8px;background:var(--accent);color:#fff;font-size:12.5px;font-weight:700}}
h4{{font-size:15px;margin:15px 0 6px}}
p{{margin:.55rem 0}}
ul,ol{{margin:.5rem 0 .5rem 1.1rem;padding:0}} li{{margin:.22rem 0}}
pre{{position:relative;background:var(--code);color:var(--codefg);border-radius:12px;padding:15px 16px;overflow:auto;font-size:13.2px;line-height:1.58;border:1px solid #1b2436;margin:.6rem 0}}
pre code{{white-space:pre}}
.copy{{position:absolute;top:8px;right:8px;font-size:11px;background:#1b2635;color:#9fb2c9;border:1px solid #2b3a4d;border-radius:7px;padding:3px 8px;cursor:pointer;opacity:0;transition:.15s}}
pre:hover .copy{{opacity:1}} .copy:hover{{color:#fff;border-color:#4d6b8f}}
:not(pre)>code{{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:1px 5px;font-size:.88em;color:var(--accent)}}
.tok-k{{color:#ff7ab2;font-weight:600}}.tok-s{{color:#9ae08a}}.tok-c{{color:#7b8ba3;font-style:italic}}
.tok-n{{color:#f2cc60}}.tok-f{{color:#79c0ff}}.tok-b{{color:#ffa657;font-style:italic}}.tok-t{{color:#7fd1c4}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:13px;padding:14px 16px;margin:.8rem 0}}
.ex{{border:1px solid var(--line);border-radius:12px;overflow:hidden;margin:.7rem 0;background:var(--card2)}}
.ex .exh{{font-size:11.6px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);padding:7px 12px;border-bottom:1px solid var(--line)}}
.ex pre{{margin:0;border-radius:0;background:var(--code)}}
.cons{{font-size:13.8px;color:var(--fg)}}
.cons b,.cx b{{color:var(--fg)}}
.cx{{font-size:13.8px;color:var(--muted)}}
.muted{{color:var(--muted)}} .small{{font-size:13px}}
.reslist{{list-style:none;margin-left:0}} .reslist li{{border-bottom:1px dashed var(--line);padding:6px 0}}
#top{{position:fixed;right:18px;bottom:18px;z-index:50;display:none}} #top.on{{display:block}}
footer{{border-top:1px solid var(--line);margin-top:56px;padding:22px 18px 60px;color:var(--muted);font-size:13.4px;text-align:center}}
mark{{background:var(--accent2);color:#08110f;border-radius:3px;padding:0 2px}}
@media print{{.head,.filterbar,#toc,#top,.copy,#progress,.pnav,.donebtn,.sel,.donebadge,.menu{{display:none!important}} .layout{{display:block;max-width:none}} .sub{{page-break-inside:avoid}} body{{font-size:11.5pt}} pre{{background:#f5f7fa;color:#111;border-color:#ccc}} .tok-k,.tok-s,.tok-c,.tok-n,.tok-f,.tok-b,.tok-t{{color:#111!important;font-style:normal}}}}
</style>
</head>
<body>
<div id="progress"></div>

<div class="head">
<header class="topbar">
  <a class="brand" href="index.html" title="Back to the home page"><span class="logo">{lang.upper() if lang != "python" else "PY"}</span>
    <div>{meta["brand"]}<br><small>{total} problems · 16 topics · 6 easy · 12 medium · 12 hard</small></div>
  </a>
  <div class="searchwrap">
    <input id="q" type="search" placeholder="Search all {total} problems — try “window”, “palindrome”, “heap”, “prefix”…" autocomplete="off" spellcheck="false">
    <span class="hint">/</span>
    <div id="results"></div>
  </div>
  <select id="jump" class="btn sel" aria-label="Jump to a topic"><option value="">Jump to topic…</option></select>
  <span class="donebadge" id="donebadge" title="Problems you marked as done">✓ 0 / {total} done</span>
  <details class="menu">
    <summary class="btn" title="All pages">☰ Pages</summary>
    <div class="menubody">
      <a href="index.html">🏠 Home</a>
      <div class="mh">Guides</div>
      <a href="cpp-guide.html">C++ for LeetCode</a>
      <a href="java-guide.html">Java for LeetCode</a>
      <a href="python-guide.html">Ultimate Python</a>
      <div class="mh">Question banks</div>
      <a href="cpp-leetcode.html">C++ bank</a>
      <a href="java-leetcode.html">Java bank</a>
      <a href="python-leetcode.html">Python bank</a>
    </div>
  </details>
  <button class="btn" id="theme" title="Toggle dark / light">🌙</button>
  <button class="btn" id="print" title="Print or save as PDF">🖨</button>
</header>
<div class="filterbar">
  <span class="fslab">Show</span>
  <button class="fchip on" data-f="all" type="button">All <b>{total}</b></button>
  <button class="fchip" data-f="Easy" type="button">Easy <b>{counts["Easy"]}</b></button>
  <button class="fchip" data-f="Medium" type="button">Medium <b>{counts["Medium"]}</b></button>
  <button class="fchip" data-f="Hard" type="button">Hard <b>{counts["Hard"]}</b></button>
  <span class="fslab">Topic list</span>
  <button class="btn mini" id="toggleall" type="button">Expand all</button>
  <button class="btn mini" id="resetdone" type="button">Reset “done”</button>
</div>
</div>

<div class="layout">
  <nav id="toc" aria-label="Contents"></nav>
  <main id="content">

<section class="chapter" id="start">
  <h2><span class="num">0</span> How to use this bank</h2>
  <div class="hero">
    <h1>{meta["title"]}</h1>
    <p class="lede">Sixteen topics, each with a fixed shape: <b>6 easy</b> problems to establish the pattern,
    <b>12 medium</b> to make it flexible, and <b>12 hard</b> to master the variants. Within every topic the order is a
    gentle, constant slope — the next problem adds exactly one new idea, never two.</p>
    <div class="badges">
      <span class="pill hot">Every problem: statement · examples · constraints · solution</span>
      <span class="pill">{meta["sub"]}</span>
      <span class="pill">Complexity stated for every solution</span>
      <span class="pill">Works offline</span>
    </div>
  </div>
  <div class="card">
    <p><b>How to work a topic.</b> Read the topic box, then do the problems in order without skipping: the easy six define
    the pattern, the first four mediums are direct variations, mediums 5–8 combine two ideas, mediums 9–12 add a constraint
    that kills the naive approach, and the hard twelve walk through the classic variants one at a time. If a problem takes
    more than 25 minutes, read the solution, then re-implement it from memory the next day.</p>
    <p><b>Companion guides.</b> Language mechanics live in the guides:
    <a href="cpp-guide.html">C++</a> · <a href="java-guide.html">Java</a> · <a href="python-guide.html">Python</a>.
    Every shortcut used in a solution is explained in the matching chapter.</p>
  </div>
</section>
'''
    return head


def build_index_sidebar(banks: list[dict], lang: str) -> str:
    return ""


def render(lang: str, banks: list[dict]) -> str:
    meta = LANG_META[lang]
    flat = flat_entries(banks)
    pos = {e[0]: i for i, e in enumerate(flat)}
    parts = [build_shell(lang, banks)]
    for i, bank in enumerate(banks, 1):
        parts.append(render_topic(i, bank, lang, flat, pos))
    total = sum(len(b["problems"]) for b in banks)
    parts.append(f'''
  </main>
</div>

<footer>
  <p><b>{meta["brand"]}</b> — {total} problems across {len(banks)} topics, with complete solutions in
  {meta["sub"].split("·")[0].strip()}.</p>
  <p class="small">Same problems in every language:
    <a href="cpp-leetcode.html">C++</a> · <a href="java-leetcode.html">Java</a> · <a href="python-leetcode.html">Python</a>
    &nbsp;|&nbsp; Guides: <a href="cpp-guide.html">C++</a> · <a href="java-guide.html">Java</a> · <a href="python-guide.html">Python</a>
    &nbsp;|&nbsp; <a href="index.html">Home</a></p>
</footer>

<button id="top" class="btn" title="Back to top">↑ Top</button>
''')
    # NOTE: this string is spliced into a JS *string literal*, so every backslash
    # must be doubled here or the literal collapses and new RegExp() throws.
    comment_alt = (r"(\\/\\/[^\\n]*|#[^\\n]*|\\/\\*[\\s\\S]*?\\*\\/)" if lang == "python"
                   else r"(\\/\\/[^\\n]*|\\/\\*[\\s\\S]*?\\*\\/)")
    parts.append(SCRIPT.replace("__KEY__", meta["key"])
                 .replace("__KEYWORDS__", ",".join(f'"{k}"' for k in meta["keywords"]))
                 .replace("__BUILTINS__", ",".join(f'"{b}"' for b in meta["builtins"] + meta.get("extra_builtins", [])))
                 .replace("__COMMENT__", comment_alt))
    parts.append("</body>\n</html>\n")
    return "\n".join(parts)


EXTRA_CSS = r"""
/* ---- navigation additions (added by the UI upgrade) ---- */
.brand:hover{{text-decoration:none}}
.brand>div{{line-height:1.25}}
.btn.mini{{padding:4px 9px;font-size:12.2px}}
.sel{{font-size:12.8px;padding:6px 8px;max-width:190px}}
.fslab{{color:var(--muted);font-size:11.4px;letter-spacing:.06em;text-transform:uppercase}}
.fchip{{border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:999px;padding:3px 11px;cursor:pointer;font:inherit;font-size:12.5px}}
.fchip b{{font-weight:700;opacity:.75}}
.fchip:hover{{border-color:var(--accent)}}
.fchip.on{{background:var(--accent);border-color:transparent;color:#fff}}
.fchip.on b{{opacity:1}}
.donebadge{{font-size:12.4px;border:1px solid var(--line);background:var(--card);border-radius:999px;padding:4px 11px;color:var(--muted);white-space:nowrap}}
.donebadge.full{{border-color:var(--ok);color:var(--ok)}}
details.menu{{position:relative}}
details.menu>summary{{list-style:none;cursor:pointer}}
details.menu>summary::-webkit-details-marker{{display:none}}
details.menu[open]>summary{{border-color:var(--accent)}}
.menubody{{position:absolute;right:0;top:36px;z-index:70;background:var(--bg);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);padding:8px;min-width:230px}}
.menubody a{{display:block;padding:6px 9px;border-radius:8px;color:var(--fg);font-size:13.4px}}
.menubody a:hover{{background:var(--card2);text-decoration:none}}
.menubody .mh{{font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:8px 9px 3px}}
/* collapsible topic list */
.navch>a{{display:flex;align-items:center;gap:6px}}
.navch>a .nch-num{{opacity:.55;min-width:14px}}
.navch>a .nch-cnt{{margin-left:auto;font-size:11px;font-weight:600;color:var(--muted);background:var(--card2);border-radius:999px;padding:1px 7px}}
.navch.has-children>a::before{{content:"▸";font-size:10px;opacity:.6}}
.navch.open.has-children>a::before{{content:"▾"}}
.navch:not(.open)>ul{{display:none}}
.navch.done>a .nch-cnt{{color:var(--ok);background:var(--ok-soft)}}
.navch.tophide{{display:none}}
/* per-problem controls */
.sub h3{{position:relative}}
.donebtn{{margin-left:auto;border:1px solid var(--line);background:var(--card);color:var(--muted);border-radius:999px;padding:3px 11px;font:inherit;font-size:12px;cursor:pointer;white-space:nowrap}}
.donebtn:hover{{border-color:var(--ok);color:var(--ok)}}
.donebtn.on{{background:var(--ok);border-color:transparent;color:#fff}}
.sub.done{{opacity:.72}}
.sub.done .pn{{background:var(--ok)}}
.sub.done h3::after{{content:" ✓";color:var(--ok)}}
.sub.fhide{{display:none}}
.pnav{{display:flex;gap:10px;justify-content:space-between;margin:16px 0 2px;font-size:13px}}
.pnav-a{{flex:1 1 0;min-width:0;border:1px solid var(--line);border-radius:10px;padding:7px 11px;color:var(--fg);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;background:var(--card)}}
.pnav-a:hover{{border-color:var(--accent);text-decoration:none;color:var(--accent)}}
.pnav-a.next{{text-align:right}}
.pnav-a .d{{font-weight:700;opacity:.7;margin-right:4px}}
.pnav-a.next .d{{margin:0 0 0 4px}}
.pnav-a.off{{border-style:dashed;color:var(--muted);text-align:center}}
@media(max-width:720px){{.pnav{{flex-direction:column}}}}
@media print{{.sub.done{{opacity:1}}}}
"""

EXTRA_SCRIPT = r'''
<script>
/* ---------------------------------------------------------------- *
 *  Navigation upgrade: done-tracking, difficulty filter, collapsing
 *  topic list, topic jump.  Pure client-side, no storage of anything
 *  but "which problems you marked done", kept in localStorage.
 * ---------------------------------------------------------------- */
(function () {
  "use strict";
  var DONE_KEY = "__DONEKEY__";
  var store = {};
  try { store = JSON.parse(localStorage.getItem(DONE_KEY) || "{}") || {}; } catch (e) { store = {}; }
  var save = function () { try { localStorage.setItem(DONE_KEY, JSON.stringify(store)); } catch (e) {} };

  var chapters = [].slice.call(document.querySelectorAll("section.chapter"));
  var subs = [].slice.call(document.querySelectorAll(".sub"));
  var total = subs.length;

  /* ---- done marks ------------------------------------------------ */
  var badge = document.getElementById("donebadge");
  function countsByChapter() {
    var out = [];
    chapters.forEach(function (ch) {
      var list = [].slice.call(ch.querySelectorAll(".sub"));
      var done = list.filter(function (s) { return store[s.getAttribute("data-slug")]; }).length;
      out.push({ ch: ch, done: done, size: list.length, pct: list.length ? done / list.length : 0 });
    });
    return out;
  }
  function refresh() {
    var done = 0;
    subs.forEach(function (s) {
      var on = !!store[s.getAttribute("data-slug")];
      s.classList.toggle("done", on);
      if (on) done++;
      var btn = s.querySelector(".donebtn");
      if (btn) { btn.classList.toggle("on", on); btn.textContent = on ? "✓ Done" : "✓ Done"; }
    });
    if (badge) {
      badge.textContent = "✓ " + done + " / " + total + " done";
      badge.classList.toggle("full", done === total && total > 0);
    }
    countsByChapter().forEach(function (c) {
      var nav = document.querySelector('.navch[data-ch="' + c.ch.id + '"]');
      if (!nav) return;
      var span = nav.querySelector(".nch-cnt");
      if (span) span.textContent = c.done + "/" + c.size;
      nav.classList.toggle("done", c.size > 0 && c.done === c.size);
    });
  }
  document.addEventListener("click", function (ev) {
    var btn = ev.target.closest && ev.target.closest(".donebtn");
    if (!btn) return;
    var slug = btn.getAttribute("data-slug");
    if (store[slug]) delete store[slug]; else store[slug] = 1;
    save(); refresh();
  });
  var resetBtn = document.getElementById("resetdone");
  if (resetBtn) resetBtn.addEventListener("click", function () {
    if (!Object.keys(store).length) return;
    if (window.confirm("Clear all “done” marks on this page?")) { store = {}; save(); refresh(); }
  });

  /* ---- difficulty filter ---------------------------------------- */
  var chips = [].slice.call(document.querySelectorAll(".fchip"));
  var filter = "all";
  function applyFilter() {
    subs.forEach(function (s) {
      var d = s.getAttribute("data-diff");
      s.classList.toggle("fhide", filter !== "all" && d !== filter);
    });
    // sidebar: hide entries and topics that have nothing to show
    document.querySelectorAll("#toc .navch").forEach(function (nav) {
      var any = false;
      nav.querySelectorAll("li").forEach(function (li) {
        var diff = li.getAttribute("data-diff");
        var hide = filter !== "all" && diff !== filter;
        li.style.display = hide ? "none" : "";
        if (!hide) any = true;
      });
      nav.classList.toggle("tophide", !any);
    });
    chips.forEach(function (c) { c.classList.toggle("on", c.getAttribute("data-f") === filter); });
    try { localStorage.setItem(DONE_KEY + "-filter", filter); } catch (e) {}
  }
  chips.forEach(function (c) {
    c.addEventListener("click", function () { filter = c.getAttribute("data-f"); applyFilter(); });
  });
  try {
    var savedFilter = localStorage.getItem(DONE_KEY + "-filter");
    if (savedFilter && ["all", "Easy", "Medium", "Hard"].indexOf(savedFilter) >= 0) {
      filter = savedFilter;
      chips.forEach(function (c) { c.classList.toggle("on", c.getAttribute("data-f") === filter); });
    }
  } catch (e) {}

  /* ---- topic list: collapse / expand ----------------------------- */
  subs.forEach(function (s) {
    var li = document.createElement("li");
    li.setAttribute("data-diff", s.getAttribute("data-diff"));
    var nav = document.querySelector('#toc a[href="#' + s.id + '"]');
    if (nav && nav.parentNode) { li = nav.parentNode; li.setAttribute("data-diff", s.getAttribute("data-diff")); }
  });
  document.querySelectorAll("#toc .navch").forEach(function (nav) {
    if (nav.querySelector("ul li")) nav.classList.add("has-children");
    var head = nav.querySelector(":scope > a");
    if (head) head.addEventListener("click", function () { nav.classList.add("open"); });
  });
  var toggleAll = document.getElementById("toggleall");
  var allOpen = false;
  if (toggleAll) toggleAll.addEventListener("click", function () {
    allOpen = !allOpen;
    document.querySelectorAll("#toc .navch").forEach(function (n) { n.classList.toggle("open", allOpen); });
    toggleAll.textContent = allOpen ? "Collapse all" : "Expand all";
  });

  /* ---- jump to topic --------------------------------------------- */
  var jump = document.getElementById("jump");
  if (jump) {
    chapters.forEach(function (ch) {
      var h2 = ch.querySelector("h2");
      var opt = document.createElement("option");
      opt.value = ch.id;
      opt.textContent = h2 ? h2.textContent.replace(/\\s+/g, " ").trim() : ch.id;
      jump.appendChild(opt);
    });
    jump.addEventListener("change", function () {
      if (!jump.value) return;
      var nav = document.querySelector('.navch[data-ch="' + jump.value + '"]');
      if (nav) nav.classList.add("open");
      window.location.hash = jump.value;
      jump.value = "";
    });
  }

  /* ---- keep the active topic open -------------------------------- */
  var current = null;
  function markActive() {
    var best = null, bestTop = -Infinity;
    chapters.forEach(function (ch) {
      var t = ch.getBoundingClientRect().top;
      if (t < 150 && t > bestTop) { bestTop = t; best = ch; }
    });
    if (best && best !== current) {
      current = best;
      var nav = document.querySelector('.navch[data-ch="' + best.id + '"]');
      if (nav) nav.classList.add("open");
    }
  }
  var ticking = false;
  window.addEventListener("scroll", function () {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () { markActive(); ticking = false; });
  }, { passive: true });

  refresh();
  applyFilter();
  markActive();
})();
</script>
'''

SCRIPT = r'''
<script>
(function () {
  "use strict";
  var root = document.documentElement, stored = null;
  try { stored = localStorage.getItem("__KEY__"); } catch (e) {}
  if (!stored && window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) stored = "dark";
  if (stored) root.setAttribute("data-theme", stored);
  var themeBtn = document.getElementById("theme");
  function label(){ themeBtn.textContent = root.getAttribute("data-theme") === "dark" ? "☀️" : "🌙"; }
  label();
  themeBtn.addEventListener("click", function(){
    var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try { localStorage.setItem("__KEY__", next); } catch(e){}
    label();
  });
  document.getElementById("print").addEventListener("click", function(){ window.print(); });

  var KEYWORDS = [__KEYWORDS__];
  var BUILTINS = [__BUILTINS__];
  var esc = function(s){ return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); };
  var RE = new RegExp(
    "__COMMENT__" +
    "|(\"\"\"[\\s\\S]*?\"\"\"|\x27\x27\x27[\\s\\S]*?\x27\x27\x27|\"(?:\\\\.|[^\"\\\\\\n])*\"|'(?:\\\\.|[^'\\\\\\n])*')" +
    "|\\b(" + KEYWORDS.join("|") + ")\\b" +
    "|\\b(0[xX][0-9a-fA-F_']+|0[bB][01_']+|\\d[\\d_']*\\.?[\\d_']*(?:[eE][-+]?\\d+)?)(?:[uUlLfFdD]{0,3})\\b" +
    "|\\b(" + BUILTINS.join("|") + ")\\b" +
    "|\\b([A-Z][A-Za-z0-9_]*)\\b" +
    "|\\b([a-z_][A-Za-z0-9_]*)(?=\\s*\\()",
    "g");
  function highlight(code){
    return code.replace(RE, function(m, c, s, k, num, b, cls, fn){
      if (c) return '<span class="tok-c">' + c + '</span>';
      if (s) return '<span class="tok-s">' + s + '</span>';
      if (k) return '<span class="tok-k">' + k + '</span>';
      if (num) return '<span class="tok-n">' + num + '</span>';
      if (b) return '<span class="tok-b">' + b + '</span>';
      if (cls) return '<span class="tok-t">' + cls + '</span>';
      if (fn) return '<span class="tok-f">' + fn + '</span>';
      return m;
    });
  }
  var blocks = document.querySelectorAll("pre > code");
  Array.prototype.forEach.call(blocks, function(code){
    if (code.dataset.hl) return;
    var text = code.textContent;
    var isPlain = code.classList.contains("nohl");
    if (!isPlain) code.innerHTML = highlight(esc(text));
    code.dataset.hl = "1";
    var pre = code.parentNode;
    if (getComputedStyle(pre).position === "static") pre.style.position = "relative";
    var btn = document.createElement("button");
    btn.className = "copy"; btn.type = "button"; btn.textContent = "copy";
    btn.addEventListener("click", function(){
      var done = function(){ btn.textContent = "copied ✓"; setTimeout(function(){ btn.textContent = "copy"; }, 1400); };
      var fallback = function(){
        var ta = document.createElement("textarea");
        ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
        document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); done(); } catch(e){ btn.textContent = "Ctrl+C"; }
        document.body.removeChild(ta);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, fallback);
      else fallback();
    });
    pre.appendChild(btn);
  });

  var chapters = document.querySelectorAll("section.chapter");
  var toc = document.getElementById("toc");
  var slugOf = function(s){ return s.toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"").slice(0,48); };
  var html = ['<div class="navhead">Topics</div>'];
  Array.prototype.forEach.call(chapters, function(ch){
    var h2 = ch.querySelector("h2");
    var num = h2.querySelector(".num") ? h2.querySelector(".num").textContent : "";
    var title = h2.textContent.replace(/^\s*\d+\s*/, "").trim();
    html.push('<div class="navch" data-ch="' + ch.id + '"><a href="#' + ch.id + '"><span class="nch-num">' + num + '</span> ' + title + '<span class="nch-cnt"></span></a>');
    var subs = ch.querySelectorAll("h3");
    if (subs.length) {
      html.push("<ul>");
      Array.prototype.forEach.call(subs, function(h3){
        if (!h3.parentNode.id) h3.parentNode.id = ch.id + "-" + slugOf(h3.textContent);
        var hClone = h3.cloneNode(true);
        var hBtn = hClone.querySelector(".donebtn"); if (hBtn) hBtn.remove();
        html.push('<li><a href="#' + h3.parentNode.id + '">' + hClone.textContent + "</a></li>");
      });
      html.push("</ul>");
    }
    html.push("</div>");
  });
  toc.innerHTML = html.join("");

  var INDEX = [];
  Array.prototype.forEach.call(chapters, function(ch){
    var chtitle = ch.querySelector("h2").textContent.replace(/^\s*\d+\s*/,"").trim();
    var list = ch.querySelectorAll(".sub");
    if (!list.length) list = [ch];
    Array.prototype.forEach.call(list, function(blk){
      var heading = blk.querySelector("h3");
      var title = chtitle;
      if (heading) {
        var hClone = heading.cloneNode(true);
        var dbtn = hClone.querySelector(".donebtn"); if (dbtn) dbtn.remove();
        title = hClone.textContent.replace(/\s+/g, " ").trim();
      }
      var id = blk.id || ch.id;
      var clone = blk.cloneNode(true);
      clone.querySelectorAll(".donebtn,.pnav").forEach(function(n){ n.remove(); });
      var text = clone.textContent.replace(/\s+/g," ").trim();
      INDEX.push({ id: id, title: title, ch: chtitle, text: text, lower: (title + " " + text).toLowerCase() });
    });
  });

  var q = document.getElementById("q"), res = document.getElementById("results"), sel = -1;
  function snippet(text, term){
    var i = text.toLowerCase().indexOf(term), raw;
    if (i < 0) raw = text.slice(0,130) + "…";
    else { var start = Math.max(0, i-60); raw = (start?"…":"") + text.slice(start, start+170) + "…"; }
    var safe = esc(raw);
    var rxTerm = esc(term).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    try { return safe.replace(new RegExp("(" + rxTerm + ")", "ig"), "<mark>$1</mark>"); }
    catch(e){ return safe; }
  }
  function render(){
    var term = q.value.trim().toLowerCase();
    if (term.length < 2) { res.classList.remove("on"); res.innerHTML = ""; sel = -1; return; }
    var scored = [];
    for (var i = 0; i < INDEX.length; i++) {
      var e = INDEX[i], pos = e.lower.indexOf(term);
      if (pos < 0) continue;
      scored.push({ e: e, score: (e.title.toLowerCase().indexOf(term) >= 0 ? 0 : 1000) + pos });
    }
    scored.sort(function(a,b){ return a.score - b.score; });
    var top = scored.slice(0, 30);
    if (!top.length) { res.innerHTML = '<div style="padding:10px 12px;color:var(--muted)">No match for “' + esc(term) + '”.</div>'; res.classList.add("on"); return; }
    res.innerHTML = top.map(function(t){
      return '<a href="#' + t.e.id + '"><b>' + esc(t.e.title) + '</b><div class="rp">' + esc(t.e.ch) + " · " + snippet(t.e.text, term) + "</div></a>";
    }).join("");
    res.classList.add("on"); sel = -1;
  }
  q.addEventListener("input", render);
  q.addEventListener("focus", function(){ if (q.value.trim().length >= 2) render(); });
  q.addEventListener("keydown", function(ev){
    var links = res.querySelectorAll("a");
    if (ev.key === "ArrowDown" || ev.key === "ArrowUp") {
      if (!links.length) return; ev.preventDefault();
      sel += ev.key === "ArrowDown" ? 1 : -1;
      if (sel < 0) sel = links.length - 1;
      if (sel >= links.length) sel = 0;
      Array.prototype.forEach.call(links, function(a,i){ a.classList.toggle("sel", i === sel); });
      links[sel].scrollIntoView({block:"nearest"});
    } else if (ev.key === "Enter") {
      var t = links[sel >= 0 ? sel : 0];
      if (t) { window.location.hash = t.getAttribute("href"); res.classList.remove("on"); q.blur(); }
    }
  });
  document.addEventListener("click", function(ev){
    if (!res.contains(ev.target) && ev.target !== q) res.classList.remove("on");
    if (ev.target.closest && ev.target.closest("#results a")) res.classList.remove("on");
  });
  document.addEventListener("keydown", function(ev){
    var typing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName);
    if (ev.key === "/" && !typing) { ev.preventDefault(); q.focus(); q.select(); }
    if (ev.key === "Escape") { res.classList.remove("on"); q.blur(); }
  });

  var progress = document.getElementById("progress"), topBtn = document.getElementById("top");
  function onScroll(){
    var h = document.documentElement, max = h.scrollHeight - h.clientHeight;
    progress.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + "%";
    topBtn.classList.toggle("on", h.scrollTop > 800);
    var best = null, bestTop = -Infinity;
    Array.prototype.forEach.call(chapters, function(ch){
      var t = ch.getBoundingClientRect().top;
      if (t < 140 && t > bestTop) { bestTop = t; best = ch; }
    });
    if (best) Array.prototype.forEach.call(toc.querySelectorAll(".navch"), function(n){
      n.classList.toggle("active", n.getAttribute("data-ch") === best.id);
    });
  }
  var ticking = false;
  window.addEventListener("scroll", function(){
    if (ticking) return; ticking = true;
    requestAnimationFrame(function(){ onScroll(); ticking = false; });
  }, { passive: true });
  topBtn.addEventListener("click", function(){ window.scrollTo({top:0, behavior:"smooth"}); });
  onScroll();
})();
</script>
'''


def main() -> int:
    banks = load_banks()
    if not banks:
        print("no bank_*.py files found", file=sys.stderr)
        return 1
    for lang in LANGS:
        page = render(lang, banks)
        page = page.replace("</style>", EXTRA_CSS + "</style>", 1)
        page = page.replace("</body>", EXTRA_SCRIPT.replace("__DONEKEY__", LANG_META[lang]["key"] + "-done") + "</body>", 1)
        out = SITE / f"{lang}-leetcode.html"
        out.write_text(page)
        print(f"{out.name:24s} {len(page)/1024:8.1f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
