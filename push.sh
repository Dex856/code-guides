#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# One-command publishing for the Code Guides site.
#
#   GH_TOKEN=ghp_xxx ./push.sh [repo-name]        # default repo name: code-guides
#
# The token needs, for the account that owns the repo:
#   - "Contents: Read and write"      (to push)
#   - "Pages:  Read and write"        (to enable Pages)
#   - "Administration: Read and write" (optional: creates the repo if missing)
# Create it at https://github.com/settings/personal-access-tokens/new (fine-grained).
# ---------------------------------------------------------------------------
set -euo pipefail

REPO="${1:-code-guides}"
TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"
OWNER="${GH_OWNER:-}"

if [[ -z "$TOKEN" ]]; then
  echo "ERROR: set GH_TOKEN (a GitHub personal access token)." >&2
  echo "       example: GH_TOKEN=ghp_xxx ./push.sh code-guides" >&2
  exit 1
fi

api() { curl -sS -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" "$@"; }

if [[ -z "$OWNER" ]]; then
  OWNER=$(api https://api.github.com/user | python3 -c 'import sys,json; print(json.load(sys.stdin)["login"])')
fi
echo "→ account: $OWNER   repo: $REPO"

# 1 · create the repository if it does not exist ---------------------------------
code=$(curl -sS -o /tmp/repo.json -w '%{http_code}' -X POST \
  -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
  https://api.github.com/user/repos \
  -d "{\"name\":\"$REPO\",\"description\":\"C++, Java and Python guides + LeetCode question banks\",\"private\":false,\"has_issues\":true}")
if [[ "$code" == "201" ]]; then echo "→ created repository"; else echo "→ repository already exists (or creation not permitted)"; fi

# 2 · commit and push -----------------------------------------------------------
git init -q 2>/dev/null || true
git add -A
git -c user.email="guides@local" -c user.name="Code Guides" commit -q -m "Site: C++/Java/Python guides + LeetCode banks (update $(date -u +%Y-%m-%d))" || echo "→ nothing new to commit"
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "https://x-access-token:$TOKEN@github.com/$OWNER/$REPO.git"
git push -u origin main --force

# 3 · enable GitHub Pages (workflow build) --------------------------------------
api -X POST "https://api.github.com/repos/$OWNER/$REPO/pages" \
  -d '{"build_type":"workflow"}' >/dev/null || \
api -X PUT  "https://api.github.com/repos/$OWNER/$REPO/pages" \
  -d '{"build_type":"workflow"}' >/dev/null || echo "→ enable Pages manually: Settings → Pages → Source: GitHub Actions"

echo
echo "✅ pushed.  Pages will be live in a minute at:"
echo "   https://$OWNER.github.io/$REPO/"
echo "   (Actions tab: https://github.com/$OWNER/$REPO/actions)"
