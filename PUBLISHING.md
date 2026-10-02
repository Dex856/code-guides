# Publishing the Code Guides site to GitHub Pages

> **Status (2026-10-02):** the token you supplied authenticates as **Dex856** and can see
> `Dex856/code-guides`, but it has **no write permissions** — every write probe returned
> `403 Resource not accessible by personal access token`:
> `git push`, creating a file via the REST API, enabling Pages, and creating the workflow file.
>
> **Fix — edit the existing token, no new token needed:**
> <https://github.com/settings/personal-access-tokens> → click the token → *Repository permissions* →
> set **Contents: Read and write**, **Workflows: Read and write**, **Pages: Read and write** → **Save**.
> The token value stays valid, so nothing has to be pasted again.
>
> Minimal alternative if you prefer fewer permissions: give **Contents: Read and write** only. I will
> push (the site also exists pre-mirrored in `docs/`), and you click once:
> repo → **Settings → Pages → Source: Deploy from a branch → main → /docs**.
>
> The repository is committed locally and ready: 4 commits, 53 files, working tree clean.

Two paths. **Path A** is if you want me to do the push; **Path B** is if you want to keep the credential
entirely on your side.

---

## Path A — you give me a token, I push

### 1. Create an empty repository (30 seconds, avoids a permission problem)

A fine-grained token cannot reliably *create* a repository, so create it by hand first:

1. Go to <https://github.com/new>
2. Repository name: `code-guides` (anything you like), **Public** (Pages needs public on free accounts)
3. **Do not** add a README, .gitignore or licence — the repo must start empty
4. Create repository

### 2. Create a fine-grained token for just that repository

1. Go to <https://github.com/settings/personal-access-tokens/new>
   (or: GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token)
2. **Token name:** `arena-push`
3. **Expiration:** 7 days (or 1 day — it only needs to survive one push)
4. **Repository access:** *Only select repositories* → pick `code-guides`
5. **Permissions** — set exactly these three, nothing else:

   | Permission (under *Repository permissions*) | Access | Why |
   |---|---|---|
   | **Contents** | Read and write | push commits |
   | **Workflows** | Read and write | push `.github/workflows/pages.yml` |
   | **Pages** | Read and write | enable GitHub Pages via the API |

   `Metadata: Read-only` is added automatically and cannot be removed.

6. Click **Generate token**, then copy the value — it starts with `github_pat_`.

### 3. Paste it in the chat

```
here is the token: github_pat_XXXXXXXXXXXX
```

I will run, from the workspace root:

```bash
GH_TOKEN=… GH_OWNER=<your-username> ./push.sh code-guides
```

which commits the site, pushes to `main`, and switches Pages to “GitHub Actions”. Then I verify that
`https://<your-username>.github.io/code-guides/` returns HTTP 200.

### 4. Revoke it immediately afterwards

<https://github.com/settings/tokens?type=beta> → `arena-push` → **Delete**.
The deploy keeps working after revocation: the workflow in the repository authenticates itself with
GitHub's own `GITHUB_TOKEN`, not with yours.

### What I do and do not do with it

* The token is used **only** as an environment variable inside the push command. It is never written to a
  file, never printed, and never stored in the workspace.
* The git remote is configured with the token inline; afterwards I remove the remote so nothing is left in
  `.git/config` (that file is also excluded from workspace snapshots).
* I cannot use it for anything else even if I wanted to: the token is scoped to one repository, with no
  account-level permissions.

### If you would rather not hand over a token at all

Use an **SSH deploy key**, which is scoped to the single repository and nothing else:

```bash
# on your machine
ssh-keygen -t ed25519 -f ~/.ssh/code-guides -N ""
# GitHub → your repo → Settings → Deploy keys → Add deploy key
#   paste ~/.ssh/code-guides.pub  and tick "Allow write access"
# then paste the PRIVATE key here, and I will push with it
```

Deploy keys cannot enable Pages, so also do: repo → **Settings → Pages → Source: GitHub Actions** (one click).

---

## Path B — you run it yourself (no credential ever leaves your machine)

```bash
# 1. get the workspace files onto your machine (download the folder from the workspace, or copy it)
cd code-guides

# 2. create the empty repo at https://github.com/new, then:
GH_TOKEN=<your fine-grained PAT with Contents + Workflows + Pages: write> \
GH_OWNER=<your-username> \
./push.sh code-guides
```

Or, if you prefer plain git and your own SSH setup:

```bash
git init -q && git add -A
git -c user.email=you@example.com -c user.name="You" commit -m "Code Guides site"
git branch -M main
git remote add origin git@github.com:<you>/code-guides.git
git push -u origin main
```

Then repo → **Settings → Pages → Source: GitHub Actions**. The included workflow
(`.github/workflows/pages.yml`) uploads `site/` on every push to `main`.

---

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `403 Resource not accessible by personal access token` on push | Token lacks **Contents: write**, or was issued for a different repository |
| Push rejected: `refusing to allow a PAT to create or update workflow` | Token lacks **Workflows: write** |
| `404 Not Found` when enabling Pages | Token lacks **Pages: write**, or the repo is private on a free account |
| Pages URL shows 404 for a minute or two | Normal — the first deployment takes 1–3 minutes; watch the **Actions** tab |
| Pages builds but the site is unstyled/blank | Pages source was left on “Deploy from a branch”; switch it to **GitHub Actions** |
| Repo is private and Pages will not enable | GitHub Pages on private repos needs a paid plan; make the repository public |

---

## What gets published

```
index.html              hub page
cpp-guide.html          C++ for LeetCode — 16 chapters   (168 KB, self-contained)
java-guide.html         Java for LeetCode — 16 chapters  (248 KB, self-contained)
python-guide.html       Ultimate Python Guide — 25 chapters (357 KB, self-contained)
cpp-leetcode.html       C++ question bank
java-leetcode.html      Java question bank
python-leetcode.html    Python question bank
.nojekyll               tells Pages to serve the files as-is
README.md               repository description
```

Sources (`site/cpp/part*.html`, `site/java/part*.html`, `site/leetcode/bank_*.py`) ship too, so the
repository doubles as the buildable source for every page: `site/build-all.sh` regenerates all of them.
