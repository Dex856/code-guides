# Publish the guides — step by step (GitHub Pages via GitHub Actions)

Repo: **Dex856/code-guides** · Expected URL: **https://Dex856.github.io/code-guides/**

---

## Step 0 — get the code into the repo (once)

Everything is built and committed locally (16 commits, up to topic 16 / 480 problems per language).
The push needs a credential.

**Option A — let the agent push** (paste a fine-grained PAT in chat):

- Contents: Read and write — required
- Pages: Read and write — so Pages can be enabled via API
- Administration: Read and write — optional, only if the repo has to be created

**Option B — push it yourself:**

```bash
cd /home/user && GH_TOKEN=<your-token> bash push.sh code-guides
```

Done when: the repo page shows the newest commit *"Topic 16: Prefix Sums & Range Queries … 480 problems per language"*.

---

## Step 1 — open the repository Settings

1. Go to **https://github.com/Dex856/code-guides**
2. Click the **Settings** tab (top bar, right of *Insights*; gear icon).

---

## Step 2 — open the Pages panel

3. In the left sidebar, scroll to the **Code and automation** group.
4. Click **Pages**.

You now see **"GitHub Pages"** with a **Build and deployment** section.

---

## Step 3 — switch the Source to GitHub Actions  ← this is the change you asked about

5. Under **Build and deployment → Source**, open the dropdown.
   It currently says *"Deploy from a branch"* (or *"None"*).
6. Choose **GitHub Actions**.
7. That's it — **there is no Save button** for this option; the selection applies immediately.
   A blue box confirms: *"GitHub Actions: Build and deployment is handled by your workflow."*

> This does **not** touch the `docs/` folder. The branch-deploy option stays available as a fallback
> (see the end of this file).

---

## Step 4 — run the workflow

The workflow in the repo (`.github/workflows/pages.yml`) is called
**"Deploy static guides to GitHub Pages"**.

8. Click the **Actions** tab.
9. In the left sidebar, click **Deploy static guides to GitHub Pages**.
10. Click **Run workflow** (right-hand side) → branch **main** → green **Run workflow** button.

*(If you enabled Pages **before** pushing, you can skip this — the push starts the workflow by itself.)*

---

## Step 5 — watch it deploy

11. A run appears at the top of the list. Click it.
12. Two jobs run one after the other:
    - **build** — checkout → assemble `_site` → configure Pages → upload artifact (~20 s)
    - **deploy** — publishes the artifact; when it turns green it shows a URL box.

Done when: **deploy** is green and the run shows ~**1 min** total.
The run also prints the live link, e.g. `https://Dex856.github.io/code-guides/`.

---

## Step 6 — open the site

13. Visit **https://Dex856.github.io/code-guides/**
14. First load can 404 for ~60–90 s while the CDN warms up — then **hard-refresh**: `Ctrl+Shift+R` (Windows) / `Cmd+Shift+R` (Mac).

You should see the hub, and from it:
- `practice.html` — the three-language practice terminal (code runs with `python3 tools/practice_server.py`; on Pages it explains that and stays editable)
- `cpp-guide.html`, `java-guide.html`, `python-guide.html`
- `cpp-leetcode.html`, `java-leetcode.html`, `python-leetcode.html` — **480 problems each**, 16 topics, 6/12/12 per topic

---

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| Workflow not listed in the Actions sidebar | The file isn't on the default branch yet → do Step 0 (push) first. |
| deploy job fails: *"Get Pages site failed"* / *"Resource not accessible by integration"* | Pages wasn't enabled when it ran → do Step 3, then **Re-run all jobs**. |
| Actions tab says Actions are disabled | Settings → **Actions** → General → **Allow all actions and reusable workflows** → Save. |
| Pages panel shows *"Your site is live at …"* already | Nothing to enable — just re-run the workflow (Step 4). |
| URL still 404 after 2 minutes | Open the run → **deploy** job → its output shows the exact `page_url`; make sure you're using that address and hard-refreshing. |
| Repo is private | GitHub Pages on a Free account needs a **public** repo: Settings → General → Danger Zone → Change visibility. |

---

## Fallback — no Actions at all (branch deploy, ~1 minute)

1. Make sure the push is done — `docs/` in the repo is already a ready-built mirror of the site
   (the same 480-problem pages).
2. **Settings → Pages → Source: "Deploy from a branch"**.
3. Branch: **`main`**, folder: **`/docs`** → **Save**.
4. Wait ~1 minute, then open **https://Dex856.github.io/code-guides/** and hard-refresh.

Both routes can coexist: switching the Source back to *GitHub Actions* at any time re-enables the workflow path.

---

## After it's live

Every future `git push` to `main` re-deploys automatically (the workflow triggers on `push`), so the site
stays in sync with the repo with no extra clicks.

Local preview meanwhile: `cd /home/user/site && python3 -m http.server 8000` → http://localhost:8000
