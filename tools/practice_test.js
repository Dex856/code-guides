// UI test for practice.html — runs the page's own script in jsdom with a stubbed API.
const fs = require("fs");
const { JSDOM, VirtualConsole } = require("/tmp/domtest/node_modules/jsdom");

const FILE = process.argv[2] || "/home/user/site/practice.html";
const html = fs.readFileSync(FILE, "utf8");
let pass = 0, fail = 0;
const check = (name, cond, extra = "") => {
  if (cond) { pass++; console.log("  ok    " + name); }
  else { fail++; console.log("  FAIL  " + name + (extra ? "  -> " + extra : "")); }
};

const PROBLEM = {
  slug: "sum-two", title: "Sum Two", difficulty: "Easy", topic_n: 1, topic: "Arrays & Strings",
  pattern: "one pass", statement: "Return the sum of the two numbers.",
  examples: [["nums = [1,2], k = 3", "6"]], constraints: ["1 <= n"], approach: "Add them.",
  complexity: ["O(1)", "O(1)"],
  code: { python: "def f(a,k):\n    return a+k", cpp: "int f(int a, int k){ return a+k; }",
          java: "int f(int a, int k){ return a+k; }", c: "int f(int a, int k){ return a + k; }" },
  starter: { python: "def f(a, k):\n    pass", cpp: "// stub", java: "// stub", c: "// c stub" },
  solution_run: { python: "def f(a,k):\n    return a+k\n\nprint(f(1, 3))", cpp: "// full c++",
                  java: "// full java", c: "/* full c */" },
};
const PROBLEM_TWO = Object.assign({}, PROBLEM, { slug: "second", title: "Second One" });

const calls = [];
const vc = new VirtualConsole();
vc.on("jsdomError", (e) => { if (!/Could not parse CSS/.test(String(e.message))) console.log("  jsdom:", String(e.message).slice(0, 120)); });

const dom = new JSDOM(html, {
  runScripts: "dangerously", pretendToBeVisual: true, virtualConsole: vc,
  url: "https://example.test/practice.html" + (process.env.PRACTICE_QUERY || ""),
  beforeParse(window) {
    const STATIC = process.env.STATIC === "1";      // pretend to be GitHub Pages
    window.fetch = (url, opts) => {
      if (STATIC && String(url).includes("api/"))
        return Promise.reject(new TypeError("Failed to fetch"));
      const body = opts && opts.body ? JSON.parse(opts.body) : null;
      calls.push({ url, body });
      if (String(url).includes("api/health"))
        return Promise.resolve({ json: () => Promise.resolve({ ok: true, runtimes: { python: true, cpp: true, java: true, c: true } }) });
      if (String(url).includes("problems.json"))
        return Promise.resolve({ json: () => Promise.resolve({ count: 2, topics: [], problems: [PROBLEM, PROBLEM_TWO] }) });
      if (String(url).includes("api/run")) {
        const broken = body.code.includes("BROKEN");
        return Promise.resolve({ json: () => Promise.resolve(broken
          ? { ok: false, stage: "compile", exit_code: 1, stdout: "", stderr: "main.cpp:3: error: oops", hint: "check the name", lang: body.lang }
          : { ok: true, stage: "run", exit_code: 0, stdout: "6\n", stderr: "", time_ms: 12, lang: body.lang }) });
      }
      return Promise.reject(new Error("unexpected url " + url));
    };
  },
});

const { window } = dom;
const { document } = window;
const el = (id) => document.getElementById(id);
// started from a link to a problem that actually exists in the stubbed bank
const DEEP_SLUG = (process.env.PRACTICE_QUERY || "").match(/p=(sum-two|second)\b/);
const DEEP = !!DEEP_SLUG;
const DEEP_TITLE = DEEP_SLUG && DEEP_SLUG[1] === "sum-two" ? "Sum Two" : "Second One";
const click = (node) => node.dispatchEvent(new window.MouseEvent("click", { bubbles: true }));
const wait = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  await wait(700);                                    // let the stubbed fetches settle

  if (process.env.STATIC === "1") {
    check("static copy says code cannot run here", /static copy/.test(el("health").textContent), el("health").textContent);
    check("static copy explains how to run locally", /practice_server\.py/.test(el("runhelp").textContent) &&
          /localhost:8000/.test(el("runhelp").textContent));
    check("static copy still loaded the problems", el("picker").querySelectorAll("option").length === 3);
    check("static copy still lets you edit code", el("code").value.length > 10);
    click(el("run"));
    await wait(120);
    check("Run explains the runner is unreachable", /not reachable/.test(el("console").textContent) &&
          /practice_server\.py/.test(el("console").textContent), el("console").textContent.slice(0, 120));
    console.log(`\n${pass} passed, ${fail} failed  (practice.html, static mode)`);
    process.exit(fail ? 1 : 0);
  }
  check("health pill reports a live runner", /runner live/.test(el("health").textContent), el("health").textContent);
  check("?p= deep link opens that problem", DEEP
        ? el("ptitle").textContent.includes(DEEP_TITLE) && el("picker").value === DEEP_SLUG[1]
        : el("ptitle").textContent.includes("Scratch pad"), el("ptitle").textContent);
  check("problems loaded into the picker", el("picker").querySelectorAll("option").length === 3,
        "options=" + el("picker").querySelectorAll("option").length);
  check("picker is grouped by topic", el("picker").querySelectorAll("optgroup").length >= 1);
  // with a deep link a problem is already open, so the editor holds its starter
  check(DEEP ? "deep link already loaded the starter" : "editor pre-filled with the python template",
        DEEP ? el("code").value.includes("def f(a, k)") : el("code").value.includes("hello from Python"),
        JSON.stringify(el("code").value.slice(0, 40)));
  check("filename shows main.py", el("filename").textContent === "main.py");

  // ---- language tabs
  const cppTab = document.querySelector('#tabs button[data-lang="cpp"]');
  click(cppTab);
  check("switching to C++ changes the filename", el("filename").textContent === "main.cpp", el("filename").textContent);
  check(DEEP ? "C++ starter loaded for the open problem" : "C++ template loaded",
        el("code").value.includes(DEEP ? "stub" : "hello from C++"));
  el("code").value = "int main(){ /* my cpp */ }";
  el("code").dispatchEvent(new window.Event("input", { bubbles: true }));    // → draft saved
  click(document.querySelector('#tabs button[data-lang="python"]'));
  check("python draft survives the round-trip",
        el("code").value.includes(DEEP ? "def f(a, k)" : "hello from Python"));
  click(cppTab);
  check("C++ draft survives the round-trip", el("code").value.includes("my cpp"));

  // ---- C tab
  click(document.querySelector('#tabs button[data-lang="c"]'));
  check("C tab sets main.c", el("filename").textContent === "main.c", el("filename").textContent);
  check("C template is a runnable program", el("code").value.includes("int main(void)"), JSON.stringify(el("code").value.slice(0, 30)));
  el("picker").value = "sum-two";
  el("picker").dispatchEvent(new window.Event("change", { bubbles: true }));
  await wait(60);
  check("C starter loaded for the problem", el("code").value.includes("c stub"), JSON.stringify(el("code").value.slice(0, 26)));
  click(el("run"));
  await wait(120);
  const cCall = calls.filter((c) => String(c.url).includes("api/run")).pop();
  check("Run posts lang=c", cCall && cCall.body.lang === "c", cCall && cCall.body.lang);
  check("C can also load the shipped solution", (function () {
    click(el("solution"));
    return el("code").value.includes("full c");
  })());
  click(cppTab);                                   // back to C++ for the checks below

  // ---- load a problem
  el("picker").value = "sum-two";
  el("picker").dispatchEvent(new window.Event("change", { bubbles: true }));
  await wait(50);
  check("problem title rendered", el("ptitle").textContent.includes("Sum Two"), el("ptitle").textContent);
  check("statement rendered", el("problem").textContent.includes("Return the sum"));
  check("example rendered", el("problem").textContent.includes("Output: 6"));
  check("C++ starter auto-loaded for the problem", el("code").value.includes("stub"), JSON.stringify(el("code").value.slice(0, 30)));

  // ---- load the full solution
  click(el("solution"));
  check("full solution loaded", el("code").value.includes("full c++"), JSON.stringify(el("code").value));

  // ---- run it (success path)
  calls.length = 0;
  click(el("run"));
  await wait(120);
  const runCall = calls.find((c) => String(c.url).includes("api/run"));
  check("Run posts to api/run", !!runCall);
  check("payload carries the language", runCall && runCall.body.lang === "cpp", runCall && runCall.body.lang);
  check("payload carries the editor text", runCall && runCall.body.code.includes("full c++"));
  check("payload carries stdin", runCall && typeof runCall.body.stdin === "string");
  check("console shows the program output", el("console").textContent.includes("6"), el("console").textContent.slice(0, 60));
  check("verdict confirms the official example", el("verdict").className.includes("good") && el("verdict").textContent.includes("matches Example 1"),
        el("verdict").textContent);
  check("pill reports run + timing", /run · .* s/.test(el("lastrun").textContent), el("lastrun").textContent);

  // ---- run it (compile failure path)
  el("code").value = "int main(){ BROKEN }";
  el("code").dispatchEvent(new window.Event("input", { bubbles: true }));
  click(el("run"));
  await wait(120);
  check("compile errors are surfaced", el("console").textContent.includes("compile failed") && el("console").textContent.includes("oops"));
  check("compiler hint shown", el("console").textContent.includes("check the name"));
  check("verdict cleared on failure", el("verdict").className === "verdict" || !el("verdict").className.includes("good"));

  // ---- starter button + clear
  el("code").value = "// edited";
  click(el("starter"));
  check("Starter button restores the skeleton", el("code").value.includes("stub"));
  click(el("clearprob"));
  check("Clear problem returns to scratch mode", el("ptitle").textContent.includes("Scratch pad"));

  console.log(`\n${pass} passed, ${fail} failed  (practice.html)`);
  process.exit(fail ? 1 : 0);
})();
