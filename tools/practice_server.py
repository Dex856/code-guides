#!/usr/bin/env python3
"""
Code Guides — practice server.

Serves the static site AND a tiny code-running API so the on-site terminals can
really compile and run Python, C++ and Java:

    python3 tools/practice_server.py [port]        # default 8000

    GET  /                 → site/index.html
    GET  /practice.html    → the terminals
    POST /api/run          → {"lang": "python|cpp|java", "code": "...", "stdin": "..."}

Safety: it is a local practice tool, not a hardened public service. Every run
happens in a throw-away temp directory with a wall-clock timeout, a CPU limit,
a file-size limit and capped output. Do not expose it to the internet.

If g++ / javac / java are missing, the matching language reports a clear message
instead of failing silently.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import resource
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent / "site"

MAX_CODE_BYTES = 200_000
MAX_OUTPUT = 64_000            # characters returned to the browser
COMPILE_TIMEOUT = 30           # seconds
RUN_TIMEOUT = 10               # seconds
MEMORY_MB = 512
_SLOT = threading.Semaphore(2)  # at most two concurrent runs


# --------------------------------------------------------------------------- #
#  helpers
# --------------------------------------------------------------------------- #
def have(tool: str) -> bool:
    return shutil.which(tool) is not None


def limits() -> None:
    """Applied in the child process just before exec."""
    resource.setrlimit(resource.RLIMIT_CPU, (RUN_TIMEOUT, RUN_TIMEOUT + 2))
    resource.setrlimit(resource.RLIMIT_FSIZE, (8 * 1024 * 1024, 8 * 1024 * 1024))
    try:
        resource.setrlimit(resource.RLIMIT_NPROC, (256, 256))
    except (ValueError, OSError):
        pass


def run(cmd: list[str], cwd: str, stdin_text: str = "", timeout: int = RUN_TIMEOUT,
        limit_memory: bool = True):
    """Run a command, capture output, never raise."""
    preexec = None
    if limit_memory:
        def preexec():                              # noqa: E306  (child-side limits)
            limits()
            resource.setrlimit(resource.RLIMIT_AS, (MEMORY_MB * 1024 * 1024,) * 2)
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=cwd, input=stdin_text, capture_output=True,
                              text=True, timeout=timeout, preexec_fn=preexec)
        return proc.returncode, proc.stdout, proc.stderr, int((time.time() - started) * 1000)
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        err = exc.stderr.decode() if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        return 124, out, err + f"\n[timed out after {timeout}s]", int((time.time() - started) * 1000)
    except FileNotFoundError:
        return 127, "", f"[command not found: {cmd[0]}]", 0


def clip(text: str) -> str:
    if len(text) <= MAX_OUTPUT:
        return text
    return text[:MAX_OUTPUT] + f"\n… [output truncated at {MAX_OUTPUT} characters]"


# --------------------------------------------------------------------------- #
#  language runners
# --------------------------------------------------------------------------- #
PY_PRELUDE = ""
CPP_PRELUDE = "#include <bits/stdc++.h>\nusing namespace std;\n"
JAVA_PRELUDE = "import java.util.*;\nimport java.io.*;\n"


def run_python(code: str, stdin_text: str) -> dict:
    if not have("python3"):
        return {"ok": False, "stage": "setup", "stderr": "python3 is not installed on this machine."}
    with tempfile.TemporaryDirectory() as d:
        pathlib.Path(d, "main.py").write_text(code)
        rc, out, err, ms = run(["python3", "-X", "utf8", "main.py"], d, stdin_text, RUN_TIMEOUT)
    return {"ok": rc == 0, "stage": "run", "exit_code": rc, "stdout": clip(out),
            "stderr": clip(err), "time_ms": ms}


def run_cpp(code: str, stdin_text: str) -> dict:
    if not have("g++"):
        return {"ok": False, "stage": "setup", "stderr": "g++ is not installed on this machine."}
    src = code if "#include" in code else CPP_PRELUDE + code
    with tempfile.TemporaryDirectory() as d:
        pathlib.Path(d, "main.cpp").write_text(src)
        rc, out, err, ms = run(["g++", "-std=c++20", "-O2", "-o", "prog", "main.cpp"], d, timeout=COMPILE_TIMEOUT)
        if rc != 0:
            return {"ok": False, "stage": "compile", "exit_code": rc,
                    "stdout": clip(out), "stderr": clip(err), "time_ms": ms,
                    "hint": fallback_hint(err, "cpp")}
        rc, out, err, ms = run(["./prog"], d, stdin_text, RUN_TIMEOUT)
    return {"ok": rc == 0, "stage": "run", "exit_code": rc, "stdout": clip(out),
            "stderr": clip(err), "time_ms": ms}


def run_java(code: str, stdin_text: str) -> dict:
    if not have("javac") or not have("java"):
        return {"ok": False, "stage": "setup", "stderr": "javac/java are not installed on this machine."}
    src = code
    if "import java." not in src:
        src = JAVA_PRELUDE + src
    match = re.search(r'public\s+(?:final\s+|abstract\s+)?class\s+(\w+)', src)
    cls = match.group(1) if match else "Main"
    if not re.search(r'static\s+void\s+main\s*\(', src):
        return {"ok": False, "stage": "compile", "exit_code": 1, "stdout": "",
                "stderr": "This Java snippet has no entry point.\n\n"
                          "The terminal runs a whole program, so a runnable Java file needs:\n"
                          "    public class Main {\n"
                          "        public static void main(String[] args) {\n"
                          "            // your code / calls here\n"
                          "        }\n"
                          "    }\n\n"
                          "Tip: press “Starter template” (or load a problem) — the templates already include main().",
                "time_ms": 0}
    with tempfile.TemporaryDirectory() as d:
        pathlib.Path(d, cls + ".java").write_text(src)
        # the JVM reserves a large virtual address space, so no RLIMIT_AS here —
        # the -Xmx flag below is what actually caps Java memory
        rc, out, err, ms = run(["javac", "-encoding", "UTF-8", "-d", d, cls + ".java"], d,
                               timeout=COMPILE_TIMEOUT, limit_memory=False)
        if rc != 0:
            return {"ok": False, "stage": "compile", "exit_code": rc,
                    "stdout": clip(out), "stderr": clip(err), "time_ms": ms,
                    "hint": fallback_hint(err, "java")}
        rc, out, err, ms = run(["java", "-Xss64m", "-Xmx" + str(MEMORY_MB) + "m", "-cp", d, cls], d,
                               stdin_text, RUN_TIMEOUT, limit_memory=False)
    return {"ok": rc == 0, "stage": "run", "exit_code": rc, "stdout": clip(out),
            "stderr": clip(err), "time_ms": ms}


def fallback_hint(err: str, lang: str) -> str:
    """A nudge for the most common beginner compile errors."""
    low = err.lower()
    if "no main" in low or "undefined reference to `main'" in low or "missing main" in low:
        return "Your program has no entry point — add a main()."
    if lang == "cpp" and "was not declared" in low:
        return "A name (or a needed #include) is missing — the terminal already adds bits/stdc++.h + using namespace std when you omit includes."
    if lang == "java" and "cannot find symbol" in low:
        return "Java needs an import for that class — the terminal adds java.util.* and java.io.* automatically when you omit imports."
    return ""


RUNNERS = {"python": run_python, "cpp": run_cpp, "java": run_java}


# --------------------------------------------------------------------------- #
#  HTTP layer
# --------------------------------------------------------------------------- #
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SITE), **kwargs)

    def log_message(self, fmt, *args):           # quieter console
        if "/api/" in (self.path or ""):
            sys.stderr.write("  api %s\n" % (fmt % args))

    def _json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):                            # noqa: N802
        if self.path.rstrip("/") == "/api/health":
            return self._json({
                "ok": True,
                "runtimes": {name: have(tool) for name, tool in
                             (("python", "python3"), ("cpp", "g++"), ("java", "javac"))},
                "limits": {"run_timeout_s": RUN_TIMEOUT, "compile_timeout_s": COMPILE_TIMEOUT,
                           "memory_mb": MEMORY_MB, "max_output_chars": MAX_OUTPUT},
            })
        return super().do_GET()

    def do_HEAD(self):                           # noqa: N802
        # browsers, proxies and uptime pings sometimes probe with HEAD;
        # answer the health check properly instead of a confusing 404
        if self.path.rstrip("/") == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return
        return super().do_HEAD()

    def do_POST(self):                           # noqa: N802
        if self.path.rstrip("/") != "/api/run":
            return self._json({"ok": False, "stderr": "unknown endpoint"}, 404)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, TypeError):
            return self._json({"ok": False, "stage": "request", "stderr": "malformed JSON body"}, 400)

        lang = str(payload.get("lang", "")).lower()
        code = str(payload.get("code", ""))
        stdin_text = str(payload.get("stdin", ""))
        if lang not in RUNNERS:
            return self._json({"ok": False, "stage": "request", "stderr": f"unknown language {lang!r}"}, 400)
        if not code.strip():
            return self._json({"ok": False, "stage": "request", "stderr": "the editor is empty"})
        if len(code.encode()) > MAX_CODE_BYTES:
            return self._json({"ok": False, "stage": "request", "stderr": "code is too large"})

        with _SLOT:
            try:
                result = RUNNERS[lang](code, stdin_text)
            except Exception as exc:             # never take the server down
                result = {"ok": False, "stage": "server", "stderr": f"{type(exc).__name__}: {exc}"}
        result["lang"] = lang
        return self._json(result)


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    missing = [t for t in ("python3", "g++", "javac") if not have(t)]
    print("Code Guides practice server")
    print(f"  site : {SITE}")
    print(f"  url  : http://localhost:{port}/          (practice: /practice.html)")
    print(f"  runs : python3={'yes' if have('python3') else 'NO'}"
          f"  g++={'yes' if have('g++') else 'NO'}  javac={'yes' if have('javac') else 'NO'}")
    if missing:
        print(f"  note : missing {', '.join(missing)} — those terminals will report it")
    print(f"  limits: {RUN_TIMEOUT}s run · {COMPILE_TIMEOUT}s compile · {MEMORY_MB} MB · "
          f"{MAX_OUTPUT} chars output · 2 concurrent runs")
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
