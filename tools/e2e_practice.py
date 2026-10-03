#!/usr/bin/env python3
"""End-to-end check of the practice terminal stack, over real HTTP.

For each sampled problem it takes the *shipped* runnable demo (solution_run.*)
out of site/leetcode/problems.json and POSTs it to the running practice server,
then compares the program's stdout with the first official example's output.
This is exactly what a user does when they press "Load solution" + "Run".
"""
import json
import random
import sys
import urllib.request

BASE = "http://127.0.0.1:8000"
SAMPLE = int(sys.argv[1]) if len(sys.argv) > 1 else 6


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=30) as r:
        return json.load(r)


def run(lang, code, stdin=""):
    req = urllib.request.Request(BASE + "/api/run",
                                 data=json.dumps({"lang": lang, "code": code, "stdin": stdin}).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def norm(s):
    s = s.strip().replace("\r\n", "\n")
    lines = []
    for ln in s.split("\n"):
        ln = ln.strip().strip('"').replace("True", "true").replace("False", "false")
        ln = ln.replace("'", '"').replace(" ", "")
        lines.append(ln)
    return "|".join(lines)


def main():
    health = get("/api/health")
    print("health:", health["ok"], health["runtimes"])
    data = get("/leetcode/problems.json")
    print(f"problems.json: {data['count']} problems ({len(json.dumps(data))/1e6:.2f} MB over HTTP)")

    runnable = [p for p in data["problems"]
                if p.get("solution_run") and all(p["solution_run"].get(l) for l in ("python", "cpp", "java"))
                and p.get("examples")]
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 20261003)
    rng.shuffle(runnable)
    runnable = runnable[:SAMPLE]

    tally = {l: [0, 0] for l in ("python", "cpp", "java")}   # [ok, fail]
    failures = []
    shown = 0
    for p in runnable:
        want = norm(p["examples"][0][1]) if p.get("examples") else None
        for lang in ("python", "cpp", "java"):
            code = (p.get("solution_run") or {}).get(lang)
            if not code:
                continue
            res = run(lang, code, p.get("example_stdin", ""))
            got = norm(res.get("stdout", ""))
            ok = res.get("ok") and (want is None or got == want)
            tally[lang][0 if ok else 1] += 1
            if not ok:
                failures.append((lang, p["slug"], want, got, (res.get("stderr") or "").strip().splitlines()[:2]))
            elif shown < 6:
                shown += 1
                print(f"  e2e  {lang:6} {p['slug']:38} -> {res.get('stdout','').strip()[:40]!r} in {res.get('time_ms')} ms")

    print("\nresults over HTTP (shipped demo vs official example):")
    for lang, (ok, bad) in tally.items():
        print(f"  {lang:6} {ok}/{ok+bad} correct")
    if failures:
        print("\nfailures:")
        for lang, slug, want, got, err in failures[:12]:
            print(f"  {lang:6} {slug:38} want {want[:36]!r} got {got[:36]!r} {err}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
