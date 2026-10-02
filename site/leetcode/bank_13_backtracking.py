# Topic 13 · Backtracking & Recursion
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.

TOPIC = {
    "name": "Backtracking & Recursion",
    "tagline": "Recursion is a promise you keep to yourself: trust the smaller case, and make exactly one decision per level.",
    "focus": "Every problem here is the same shape: a decision tree where each level fixes one choice permanently for that branch. Three tools keep it "
             "fast. Pruning cuts a branch before its leaves are enumerated (a partial sum already past the target, a board square that is already "
             "attacked). Grouping and ordering handle duplicates (sort, then skip equal choices at the same level). And the recursion contract — what "
             "one call returns and what state it may touch — is what separates a clean solution from one that \"almost works\".",
    "ordering": "easy 1–3 are plain recursion on numbers, 4–5 walk trees and accumulate a path, 6 mutates in place with two recursive pointers; medium "
                "1–4 are the include/exclude and start-index templates (case choices, subsets, combinations, permutations), 5–8 add constraints "
                "(Gray code ordering, palindromic partitions, IP addresses, balanced parentheses), 9–12 add reuse, duplicate skipping, multiset "
                "counting and structural generation; hard 1–5 are counting searches with bitmask or coverage state, 6–9 prune whole search levels, "
                "10–12 are the largest combinatorial searches with the strongest pruning.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "power-of-two",
        "title": "Power of Two",
        "difficulty": "Easy",
        "pattern": "recursive halving",
        "statement": "Return true if n is a power of two, false otherwise.",
        "examples": [("n = 1", "true"), ("n = 16", "true"), ("n = 3", "false")],
        "constraints": ["-2^31 <= n <= 2^31 - 1", "n = 1 counts as 2^0"],
        "approach": "A power of two is either 1 or an even number whose half is also a power of two. That sentence is the recursion: test the base case, "
                     "reject non-positive and odd values, and recurse on n / 2 — each call strictly shrinks the problem.",
        "complexity": ("O(log n) time", "O(log n) stack"),
        "code": {
            "cpp": r"""// A power of two is 1, or an even number whose half is also one
bool isPowerOfTwo(int n) {
    if (n <= 0) return false;                // powers of two are positive
    if (n == 1) return true;                 // the base case: 2^0
    return n % 2 == 0 && isPowerOfTwo(n / 2);
}   // O(log n) time · O(log n) stack space""",
            "java": r"""// A power of two is 1, or an even number whose half is also one
boolean isPowerOfTwo(int n) {
    if (n <= 0) return false;                // powers of two are positive
    if (n == 1) return true;                 // the base case: 2^0
    return n % 2 == 0 && isPowerOfTwo(n / 2);
}   // O(log n) time · O(log n) stack space""",
            "python": r"""def is_power_of_two(n):
    if n <= 0:
        return False                 # powers of two are positive
    if n == 1:
        return True                  # the base case: 2^0
    return n % 2 == 0 and is_power_of_two(n // 2)""",
        },
    },
    {
        "slug": "power-of-three",
        "title": "Power of Three",
        "difficulty": "Easy",
        "pattern": "recursive division by a fixed base",
        "statement": "Return true if n is a power of three, false otherwise.",
        "examples": [("n = 27", "true"), ("n = 0", "false"), ("n = -1", "false")],
        "constraints": ["-2^31 <= n <= 2^31 - 1", "n = 1 counts as 3^0"],
        "approach": "The same shape as the power-of-two recursion with the base changed: 1 is a power of three, and any larger value must be divisible "
                     "by three with a power-of-three quotient. Reusing the halving idea with a different base is worth noticing — the recurrence does "
                     "not care which base it is.",
        "complexity": ("O(log n) time", "O(log n) stack"),
        "code": {
            "cpp": r"""// 1 is a power of three; anything larger must divide by three cleanly
bool isPowerOfThree(int n) {
    if (n <= 0) return false;                // 0 and negatives never qualify
    if (n == 1) return true;                 // the base case: 3^0
    return n % 3 == 0 && isPowerOfThree(n / 3);
}   // O(log n) time · O(log n) stack space""",
            "java": r"""// 1 is a power of three; anything larger must divide by three cleanly
boolean isPowerOfThree(int n) {
    if (n <= 0) return false;                // 0 and negatives never qualify
    if (n == 1) return true;                 // the base case: 3^0
    return n % 3 == 0 && isPowerOfThree(n / 3);
}   // O(log n) time · O(log n) stack space""",
            "python": r"""def is_power_of_three(n):
    if n <= 0:
        return False                 # 0 and negatives never qualify
    if n == 1:
        return True                  # the base case: 3^0
    return n % 3 == 0 and is_power_of_three(n // 3)""",
        },
    },
    {
        "slug": "fibonacci-number",
        "title": "Fibonacci Number",
        "difficulty": "Easy",
        "pattern": "recursion plus memoisation",
        "statement": "Return F(n) where F(0) = 0, F(1) = 1 and F(n) = F(n-1) + F(n-2).",
        "examples": [("n = 2", "1"), ("n = 3", "2"), ("n = 4", "3")],
        "constraints": ["0 <= n <= 30", "the answer fits in a 32-bit integer"],
        "approach": "The definition is already recursive, but the naive translation recomputes the same values exponentially often. Storing each "
                     "answer in a table the first time it is computed turns the recursion into a linear pass — the standard first lesson in "
                     "memoisation, and the reason \"recursion\" and \"dynamic programming\" are the same idea seen from two ends.",
        "complexity": ("O(n) time with memoisation", "O(n)"),
        "code": {
            "cpp": r"""// The definition is recursive; the table removes all repeated work
int fib(int n) {
    if (n < 2) return n;
    vector<int> memo(n + 1, -1);
    memo[0] = 0; memo[1] = 1;
    function<int(int)> go = [&](int x) {
        if (memo[x] != -1) return memo[x];   // computed before
        return memo[x] = go(x - 1) + go(x - 2);
    };
    return go(n);
}   // O(n) time · O(n) space""",
            "java": r"""// The definition is recursive; the table removes all repeated work
int fib(int n) {
    if (n < 2) return n;
    int[] memo = new int[n + 1];
    Arrays.fill(memo, -1);
    memo[0] = 0; memo[1] = 1;
    return go(n, memo);
}
int go(int x, int[] memo) {
    if (memo[x] != -1) return memo[x];       // computed before
    memo[x] = go(x - 1, memo) + go(x - 2, memo);
    return memo[x];
}   // O(n) time · O(n) space""",
            "python": r"""def fib(n, memo=None):
    if n < 2:
        return n                     # F(0) = 0, F(1) = 1
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]               # computed before
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]""",
        },
    },
    {
        "slug": "binary-tree-paths",
        "title": "Binary Tree Paths",
        "difficulty": "Easy",
        "pattern": "DFS that carries a path",
        "statement": "Return all root-to-leaf paths as strings like \"1->2->5\".",
        "examples": [("root = [1,2,3,null,5]", "[\"1->2->5\",\"1->3\"]"), ("root = [1]", "[\"1\"]")],
        "constraints": ["1 <= nodes <= 100", "-100 <= node values <= 100", "a path ends at a leaf"],
        "approach": "Walk down passing the path built so far, and record it when a node has no children — that is the moment a path is complete. The "
                     "path is rebuilt per branch rather than shared and undone, which keeps the recursion easy to read; a leaf is detected by both "
                     "children being empty, not by depth.",
        "complexity": ("O(n · h) time (each path is copied as a string)", "O(h) stack"),
        "code": {
            "cpp": r"""// Carry the path down; a node with no children closes it
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
vector<string> binaryTreePaths(TreeNode* root) {
    vector<string> out;
    function<void(TreeNode*, string)> walk = [&](TreeNode* node, string path) {
        if (!node) return;
        path += to_string(node->val);
        if (!node->left && !node->right) {      // a leaf: the path is complete
            out.push_back(path);
            return;
        }
        walk(node->left, path + "->");
        walk(node->right, path + "->");
    };
    walk(root, "");
    return out;
}   // O(n · h) time · O(h) stack space""",
            "java": r"""// Carry the path down; a node with no children closes it
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
List<String> binaryTreePaths(TreeNode root) {
    List<String> out = new ArrayList<>();
    walk(root, "", out);
    return out;
}
void walk(TreeNode node, String path, List<String> out) {
    if (node == null) return;
    path += node.val;
    if (node.left == null && node.right == null) {   // a leaf: path complete
        out.add(path);
        return;
    }
    walk(node.left, path + "->", out);
    walk(node.right, path + "->", out);
}   // O(n · h) time · O(h) stack space""",
            "python": r"""def binary_tree_paths(root):
    out = []

    def walk(node, path):
        if not node:
            return
        path = path + [str(node.val)]
        if not node.left and not node.right:
            out.append('->'.join(path))     # a leaf closes the path
            return
        walk(node.left, path)
        walk(node.right, path)

    walk(root, [])
    return out""",
        },
    },
    {
        "slug": "sum-of-left-leaves",
        "title": "Sum of Left Leaves",
        "difficulty": "Easy",
        "pattern": "DFS with one extra flag",
        "statement": "Return the sum of all left leaves of a binary tree.",
        "examples": [("root = [3,9,20,null,null,15,7]", "24"), ("root = [1]", "0")],
        "constraints": ["1 <= nodes <= 1000", "-1000 <= node values <= 1000"],
        "approach": "A node needs to know something its children cannot see — whether it arrived as a left child. Passing that one boolean down makes "
                     "the test exact: add the value when the flag is true *and* the node is a leaf. Carrying a tiny piece of context through the "
                     "recursion is the same technique the harder backtracking problems use for partial sums.",
        "complexity": ("O(n) time", "O(h) stack"),
        "code": {
            "cpp": r"""// The flag says how the node was reached; left + leaf is what counts
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
int sumOfLeftLeaves(TreeNode* root) {
    function<int(TreeNode*, bool)> walk = [&](TreeNode* node, bool fromLeft) {
        if (!node) return 0;
        if (fromLeft && !node->left && !node->right) return node->val;   // left leaf
        return walk(node->left, true) + walk(node->right, false);
    };
    return walk(root, false);
}   // O(n) time · O(h) stack space""",
            "java": r"""// The flag says how the node was reached; left + leaf is what counts
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
int sumOfLeftLeaves(TreeNode root) {
    return walk(root, false);
}
int walk(TreeNode node, boolean fromLeft) {
    if (node == null) return 0;
    if (fromLeft && node.left == null && node.right == null) return node.val;   // left leaf
    return walk(node.left, true) + walk(node.right, false);
}   // O(n) time · O(h) stack space""",
            "python": r"""def sum_of_left_leaves(root):
    def walk(node, from_left):
        if not node:
            return 0
        if from_left and not node.left and not node.right:
            return node.val                 # a left leaf
        return walk(node.left, True) + walk(node.right, False)
    return walk(root, False)""",
        },
    },
    {
        "slug": "reverse-string",
        "title": "Reverse String",
        "difficulty": "Easy",
        "pattern": "two pointers, recursively",
        "statement": "Reverse the array of characters s in place using O(1) extra memory.",
        "examples": [("s = [\"h\",\"e\",\"l\",\"l\",\"o\"]", "[\"o\",\"l\",\"l\",\"e\",\"h\"]"),
                     ("s = [\"H\",\"a\",\"n\",\"n\",\"a\",\"h\"]", "[\"h\",\"a\",\"n\",\"n\",\"a\",\"H\"]")],
        "constraints": ["1 <= s.length <= 10^5", "s[i] is a printable ASCII character", "the reversal must happen in place"],
        "approach": "Swap the two ends, then ask the same question about the inner slice. Written recursively the loop becomes a call that swaps once "
                     "and hands the rest on, and the base case is when the pointers meet or cross — the recursion is the loop, spelled differently.",
        "complexity": ("O(n) time", "O(n) stack (O(1) with a loop)"),
        "code": {
            "cpp": r"""// Swap the ends, then recurse on the inside
void reverseString(vector<char>& s) {
    function<void(int,int)> go = [&](int i, int j) {
        if (i >= j) return;                  // base case: pointers met or crossed
        swap(s[i], s[j]);
        go(i + 1, j - 1);
    };
    go(0, (int)s.size() - 1);
}   // O(n) time · O(n) stack space""",
            "java": r"""// Swap the ends, then recurse on the inside
void reverseString(char[] s) {
    go(s, 0, s.length - 1);
}
void go(char[] s, int i, int j) {
    if (i >= j) return;                      // base case: pointers met or crossed
    char t = s[i]; s[i] = s[j]; s[j] = t;
    go(s, i + 1, j - 1);
}   // O(n) time · O(n) stack space""",
            "python": r"""def reverse_string(s):
    def go(i, j):
        if i >= j:
            return                  # base case: pointers met or crossed
        s[i], s[j] = s[j], s[i]
        go(i + 1, j - 1)            # the same question for the inner slice
    go(0, len(s) - 1)""",
        },
    },
    # ---------------------------------------------------------------- MEDIUM
    {
        "slug": "letter-case-permutation",
        "title": "Letter Case Permutation",
        "difficulty": "Medium",
        "pattern": "one branch per character",
        "statement": "Return all strings that can be made by changing the case of some letters of s (the order of the answer does not matter).",
        "examples": [("s = \"a1b2\"", "[\"a1b2\",\"a1B2\",\"A1b2\",\"A1B2\"]"), ("s = \"3z4\"", "[\"3z4\",\"3Z4\"]")],
        "constraints": ["1 <= s.length <= 12", "s consists of letters and digits"],
        "approach": "Each position contributes a fixed set of choices: two for a letter, one for a digit. Walking positions left to right and trying "
                     "every choice is a full decision tree whose leaves are the answers — the plainest possible backtracking template, and the reason "
                     "digits need no special case beyond a single-option loop.",
        "complexity": ("O(2^letters · n) time", "O(2^letters) output"),
        "code": {
            "cpp": r"""// Two choices per letter, one per digit: the plainest template
vector<string> letterCasePermutation(string s) {
    vector<string> out;
    string cur = s;
    function<void(int)> dfs = [&](int i) {
        if (i == (int)s.size()) { out.push_back(cur); return; }
        char c = s[i];
        if (!isalpha((unsigned char)c)) { dfs(i + 1); return; }   // only one option
        cur[i] = tolower(c);
        dfs(i + 1);
        cur[i] = toupper(c);
        dfs(i + 1);
        cur[i] = c;                          // restore for the caller
    };
    dfs(0);
    return out;
}   // O(2^letters · n) time · O(2^letters · n) output space""",
            "java": r"""// Two choices per letter, one per digit: the plainest template
List<String> letterCasePermutation(String s) {
    List<String> out = new ArrayList<>();
    char[] cur = s.toCharArray();
    dfs(s.toCharArray(), 0, cur, out);
    return out;
}
void dfs(char[] s, int i, char[] cur, List<String> out) {
    if (i == s.length) { out.add(new String(cur)); return; }
    char c = s[i];
    if (!Character.isLetter(c)) { dfs(s, i + 1, cur, out); return; }   // one option
    cur[i] = Character.toLowerCase(c);
    dfs(s, i + 1, cur, out);
    cur[i] = Character.toUpperCase(c);
    dfs(s, i + 1, cur, out);
    cur[i] = c;                              // restore for the caller
}   // O(2^letters · n) time · O(2^letters · n) output space""",
            "python": r"""def letter_case_permutation(s):
    out = []
    cur = list(s)

    def dfs(i):
        if i == len(s):
            out.append(''.join(cur))
            return
        if not s[i].isalpha():
            dfs(i + 1)                       # digits have only one option
            return
        cur[i] = s[i].lower()
        dfs(i + 1)
        cur[i] = s[i].upper()
        dfs(i + 1)
        cur[i] = s[i]                        # restore for the caller

    dfs(0)
    return out""",
        },
    },
    {
        "slug": "subsets",
        "title": "Subsets",
        "difficulty": "Medium",
        "pattern": "include or exclude each element",
        "statement": "Return all subsets of the distinct integers in nums (the order of the answer does not matter).",
        "examples": [("nums = [1,2,3]", "[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]"), ("nums = [0]", "[[],[0]]")],
        "constraints": ["1 <= nums.length <= 10", "-10 <= nums[i] <= 10", "all numbers are distinct"],
        "approach": "Every element is a yes/no decision, so the tree has 2^n leaves. The trick that makes the code short is recording the current "
                     "partial set at *every* node rather than only at the leaves — a node's path from the root already is a complete subset, so no "
                     "extra bookkeeping is needed.",
        "complexity": ("O(2^n · n) time", "O(2^n) output"),
        "code": {
            "cpp": r"""// Record the partial set at every node: a path already is a subset
vector<vector<int>> subsets(vector<int>& nums) {
    vector<vector<int>> out;
    vector<int> cur;
    function<void(int)> dfs = [&](int start) {
        out.push_back(cur);                  // every node is an answer
        for (int i = start; i < (int)nums.size(); i++) {
            cur.push_back(nums[i]);
            dfs(i + 1);
            cur.pop_back();                  // undo the choice
        }
    };
    dfs(0);
    return out;
}   // O(2^n · n) time · O(2^n · n) output space""",
            "java": r"""// Record the partial set at every node: a path already is a subset
List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> out = new ArrayList<>();
    dfs(nums, 0, new ArrayList<>(), out);
    return out;
}
void dfs(int[] nums, int start, List<Integer> cur, List<List<Integer>> out) {
    out.add(new ArrayList<>(cur));           // every node is an answer
    for (int i = start; i < nums.length; i++) {
        cur.add(nums[i]);
        dfs(nums, i + 1, cur, out);
        cur.remove(cur.size() - 1);          // undo the choice
    }
}   // O(2^n · n) time · O(2^n · n) output space""",
            "python": r"""def subsets(nums):
    out = []
    cur = []

    def dfs(start):
        out.append(cur[:])                   # every node is an answer
        for i in range(start, len(nums)):
            cur.append(nums[i])              # take nums[i]
            dfs(i + 1)                       # and only look to its right
            cur.pop()                        # undo the choice

    dfs(0)
    return out""",
        },
    },
    {
        "slug": "combinations",
        "title": "Combinations",
        "difficulty": "Medium",
        "pattern": "start index plus a length target",
        "statement": "Return all k-element combinations of the numbers 1..n (the order of the answer does not matter).",
        "examples": [("n = 4, k = 2", "[[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]"), ("n = 1, k = 1", "[[1]]")],
        "constraints": ["1 <= n <= 20", "1 <= k <= n"],
        "approach": "The subsets template with a finish line: keep a start index so each combination is built in increasing order (which is what stops "
                     "1,2 and 2,1 both appearing), and record only when the current list reaches length k. Trimming the loop at n - (k - len) skips "
                     "branches that can no longer be completed.",
        "complexity": ("O(C(n,k) · k) time", "O(C(n,k)) output"),
        "code": {
            "cpp": r"""// Start index keeps order; the loop bound skips unfinishable branches
vector<vector<int>> combine(int n, int k) {
    vector<vector<int>> out;
    vector<int> cur;
    function<void(int)> dfs = [&](int start) {
        if ((int)cur.size() == k) { out.push_back(cur); return; }
        int need = k - cur.size();
        for (int v = start; v <= n - need + 1; v++) {   // room for the rest
            cur.push_back(v);
            dfs(v + 1);
            cur.pop_back();
        }
    };
    dfs(1);
    return out;
}   // O(C(n,k) · k) time · O(C(n,k) · k) output space""",
            "java": r"""// Start index keeps order; the loop bound skips unfinishable branches
List<List<Integer>> combine(int n, int k) {
    List<List<Integer>> out = new ArrayList<>();
    dfs(n, k, 1, new ArrayList<>(), out);
    return out;
}
void dfs(int n, int k, int start, List<Integer> cur, List<List<Integer>> out) {
    if (cur.size() == k) { out.add(new ArrayList<>(cur)); return; }
    int need = k - cur.size();
    for (int v = start; v <= n - need + 1; v++) {    // room for the rest
        cur.add(v);
        dfs(n, k, v + 1, cur, out);
        cur.remove(cur.size() - 1);
    }
}   // O(C(n,k) · k) time · O(C(n,k) · k) output space""",
            "python": r"""def combine(n, k):
    out = []
    cur = []

    def dfs(start):
        if len(cur) == k:
            out.append(cur[:])               # the combination is complete
            return
        need = k - len(cur)
        for v in range(start, n - need + 2):  # leave room for the rest
            cur.append(v)
            dfs(v + 1)
            cur.pop()

    dfs(1)
    return out""",
        },
    },
    {
        "slug": "permutations",
        "title": "Permutations",
        "difficulty": "Medium",
        "pattern": "used array",
        "statement": "Return all permutations of the distinct integers in nums (the order of the answer does not matter).",
        "examples": [("nums = [1,2,3]", "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]"),
                     ("nums = [0,1]", "[[0,1],[1,0]]"), ("nums = [1]", "[[1]]")],
        "constraints": ["1 <= nums.length <= 6", "-10 <= nums[i] <= 10", "all numbers are distinct"],
        "approach": "Unlike subsets, order matters here, so the state that stops a repeat is not a start index but a used flag per element: at every "
                     "level try each unused element, and the recursion depth is the position being filled. The permutation is complete when the "
                     "partial list reaches the full length.",
        "complexity": ("O(n! · n) time", "O(n! · n) output"),
        "code": {
            "cpp": r"""// Try every unused element at each position; depth is the position
vector<vector<int>> permute(vector<int>& nums) {
    vector<vector<int>> out;
    vector<int> cur;
    vector<bool> used(nums.size(), false);
    function<void()> dfs = [&]() {
        if (cur.size() == nums.size()) { out.push_back(cur); return; }
        for (int i = 0; i < (int)nums.size(); i++) {
            if (used[i]) continue;           // already placed earlier
            used[i] = true;
            cur.push_back(nums[i]);
            dfs();
            cur.pop_back();
            used[i] = false;                 // undo the choice
        }
    };
    dfs();
    return out;
}   // O(n! · n) time · O(n! · n) output space""",
            "java": r"""// Try every unused element at each position; depth is the position
List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> out = new ArrayList<>();
    dfs(nums, new boolean[nums.length], new ArrayList<>(), out);
    return out;
}
void dfs(int[] nums, boolean[] used, List<Integer> cur, List<List<Integer>> out) {
    if (cur.size() == nums.length) { out.add(new ArrayList<>(cur)); return; }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;               // already placed earlier
        used[i] = true;
        cur.add(nums[i]);
        dfs(nums, used, cur, out);
        cur.remove(cur.size() - 1);
        used[i] = false;                     // undo the choice
    }
}   // O(n! · n) time · O(n! · n) output space""",
            "python": r"""def permute(nums):
    out = []
    cur = []
    used = [False] * len(nums)

    def dfs():
        if len(cur) == len(nums):
            out.append(cur[:])               # the permutation is complete
            return
        for i in range(len(nums)):
            if used[i]:
                continue                     # already placed earlier
            used[i] = True
            cur.append(nums[i])
            dfs()
            cur.pop()
            used[i] = False                  # undo the choice

    dfs()
    return out""",
        },
    },
    {
        "slug": "gray-code",
        "title": "Gray Code",
        "difficulty": "Medium",
        "pattern": "reflected recursion (and a one-line formula)",
        "statement": "Return any sequence of the 2^n integers 0..2^n - 1 in which consecutive values differ by exactly one bit, and the first and last "
                     "also differ by one bit.",
        "examples": [("n = 2", "[0,1,3,2]"), ("n = 1", "[0,1]")],
        "constraints": ["1 <= n <= 16", "all 2^n values must appear exactly once"],
        "approach": "Two equivalent views. Recursively, the code for n is the code for n-1 written forwards (top bit 0) followed by the same sequence "
                     "backwards with the top bit set — reversing the second half is exactly what keeps the join edge legal. Algebraically the same "
                     "sequence is i XOR (i >> 1) for i = 0, 1, 2, ….",
        "complexity": ("O(2^n) time", "O(2^n)"),
        "code": {
            "cpp": r"""// i ^ (i >> 1) walks the reflected Gray code in order
vector<int> grayCode(int n) {
    vector<int> out;
    out.reserve(1 << n);
    for (int i = 0; i < (1 << n); i++)
        out.push_back(i ^ (i >> 1));         // one bit changes each step
    return out;
}   // O(2^n) time · O(2^n) space""",
            "java": r"""// i ^ (i >> 1) walks the reflected Gray code in order
List<Integer> grayCode(int n) {
    List<Integer> out = new ArrayList<>();
    for (int i = 0; i < (1 << n); i++)
        out.add(i ^ (i >> 1));               // one bit changes each step
    return out;
}   // O(2^n) time · O(2^n) space""",
            "python": r"""def gray_code(n):
    # i ^ (i >> 1) is the reflected Gray code: neighbours differ by one bit
    return [i ^ (i >> 1) for i in range(1 << n)]""",
        },
    },
    {
        "slug": "palindrome-partitioning",
        "title": "Palindrome Partitioning",
        "difficulty": "Medium",
        "pattern": "partition DFS with a validity check",
        "statement": "Split s into substrings so that every piece is a palindrome; return all such partitions (the order of the answer does not matter).",
        "examples": [("s = \"aab\"", "[[\"a\",\"a\",\"b\"],[\"aa\",\"b\"]]"), ("s = \"a\"", "[[\"a\"]]")],
        "constraints": ["1 <= s.length <= 16", "s consists of lowercase letters"],
        "approach": "Partitioning is a choice of cut positions, so the recursion fixes one cut at a time: take s[start..end], keep it only if it reads the "
                     "same both ways, and recurse on what follows. The palindrome test is the only pruning needed, and it is what keeps the tree small "
                     "on most inputs.",
        "complexity": ("O(2^n · n) time", "O(2^n · n) output"),
        "code": {
            "cpp": r"""// Fix one cut at a time; only palindromic pieces may be kept
vector<vector<string>> partition(string s) {
    vector<vector<string>> out;
    vector<string> cur;
    function<bool(int,int)> isPal = [&](int i, int j) {
        while (i < j) {
            if (s[i] != s[j]) return false;
            i++; j--;
        }
        return true;
    };
    function<void(int)> dfs = [&](int start) {
        if (start == (int)s.size()) { out.push_back(cur); return; }
        for (int end = start; end < (int)s.size(); end++) {
            if (!isPal(start, end)) continue;      // this piece cannot be used
            cur.push_back(s.substr(start, end - start + 1));
            dfs(end + 1);
            cur.pop_back();
        }
    };
    dfs(0);
    return out;
}   // O(2^n · n) time · O(2^n · n) output space""",
            "java": r"""// Fix one cut at a time; only palindromic pieces may be kept
List<List<String>> partition(String s) {
    List<List<String>> out = new ArrayList<>();
    dfs(s, 0, new ArrayList<>(), out);
    return out;
}
void dfs(String s, int start, List<String> cur, List<List<String>> out) {
    if (start == s.length()) { out.add(new ArrayList<>(cur)); return; }
    for (int end = start; end < s.length(); end++) {
        if (!isPal(s, start, end)) continue;     // this piece cannot be used
        cur.add(s.substring(start, end + 1));
        dfs(s, end + 1, cur, out);
        cur.remove(cur.size() - 1);
    }
}
boolean isPal(String s, int i, int j) {
    while (i < j) {
        if (s.charAt(i) != s.charAt(j)) return false;
        i++; j--;
    }
    return true;
}   // O(2^n · n) time · O(2^n · n) output space""",
            "python": r"""def partition_palindromes(s):
    out = []
    cur = []

    def is_pal(i, j):
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1; j -= 1
        return True                      # reads the same both ways

    def dfs(start):
        if start == len(s):
            out.append(cur[:])           # every piece was a palindrome
            return
        for end in range(start, len(s)):
            if not is_pal(start, end):
                continue                 # this piece cannot be used
            cur.append(s[start:end+1])
            dfs(end + 1)                 # continue after the cut
            cur.pop()

    dfs(0)
    return out""",
        },
    },
    {
        "slug": "restore-ip-addresses",
        "title": "Restore IP Addresses",
        "difficulty": "Medium",
        "pattern": "partition DFS with numeric constraints",
        "statement": "Insert three dots into s so that the result is a valid IP address (four parts, each 0..255, no part with a leading zero); return "
                     "all valid addresses (the order of the answer does not matter).",
        "examples": [("s = \"25525511135\"", "[\"255.255.11.135\",\"255.255.111.35\"]"), ("s = \"0000\"", "[\"0.0.0.0\"]"),
                     ("s = \"101023\"", "[\"1.0.10.23\",\"1.0.102.3\",\"10.1.0.23\",\"10.10.2.3\",\"101.0.2.3\"]")],
        "constraints": ["1 <= s.length <= 20", "s consists of digits only"],
        "approach": "Same cut-by-cut recursion as palindromic partitioning, with an IP rule instead of a palindrome rule: a piece may have at most "
                     "three characters, at most the value 255, and may not start with zero unless it is the single character \"0\". Four parts must "
                     "cover s exactly, so the depth of the recursion is the depth of the address.",
        "complexity": ("O(3^4 · n) time (each part has at most three choices)", "O(1) parts per answer"),
        "code": {
            "cpp": r"""// Four parts, each <= 255 and without a leading zero
vector<string> restoreIpAddresses(string s) {
    vector<string> out;
    vector<string> parts;
    function<void(int)> dfs = [&](int i) {
        if ((int)parts.size() == 4) {
            if (i == (int)s.size()) {                // the address used all of s
                string ip = parts[0];
                for (int t = 1; t < 4; t++) ip += "." + parts[t];
                out.push_back(ip);
            }
            return;
        }
        for (int len = 1; len <= 3 && i + len <= (int)s.size(); len++) {
            string piece = s.substr(i, len);
            if (piece.size() > 1 && piece[0] == '0') break;   // no leading zero
            if (stoi(piece) > 255) break;                     // longer pieces are larger
            parts.push_back(piece);
            dfs(i + len);
            parts.pop_back();
        }
    };
    dfs(0);
    return out;
}   // O(3^4) recursion nodes · O(1) extra space per answer""",
            "java": r"""// Four parts, each <= 255 and without a leading zero
List<String> restoreIpAddresses(String s) {
    List<String> out = new ArrayList<>();
    dfs(s, 0, new ArrayList<>(), out);
    return out;
}
void dfs(String s, int i, List<String> parts, List<String> out) {
    if (parts.size() == 4) {
        if (i == s.length()) {                   // the address used all of s
            out.add(String.join(".", parts));
        }
        return;
    }
    for (int len = 1; len <= 3 && i + len <= s.length(); len++) {
        String piece = s.substring(i, i + len);
        if (piece.length() > 1 && piece.charAt(0) == '0') break;   // leading zero
        if (Integer.parseInt(piece) > 255) break;                  // so are the rest
        parts.add(piece);
        dfs(s, i + len, parts, out);
        parts.remove(parts.size() - 1);
    }
}   // O(3^4) recursion nodes · O(1) extra space per answer""",
            "python": r"""def restore_ip_addresses(s):
    out = []
    parts = []

    def dfs(i):
        if len(parts) == 4:
            if i == len(s):
                out.append('.'.join(parts))     # the address used all of s
            return
        for size in range(1, 4):
            if i + size > len(s):
                break
            piece = s[i:i+size]
            if len(piece) > 1 and piece[0] == '0':
                break                           # a leading zero is not allowed
            if int(piece) > 255:
                break                           # longer pieces only get larger
            parts.append(piece)
            dfs(i + size)
            parts.pop()

    dfs(0)
    return out""",
        },
    },
    {
        "slug": "generate-parentheses",
        "title": "Generate Parentheses",
        "difficulty": "Medium",
        "pattern": "validity-driven construction",
        "statement": "Given n pairs of parentheses, return all balanced strings of n pairs (the order of the answer does not matter).",
        "examples": [("n = 3", "[\"((()))\",\"(()())\",\"(())()\",\"()(())\",\"()()()\"]"), ("n = 1", "[\"()\"]")],
        "constraints": ["1 <= n <= 8"],
        "approach": "Instead of generating all 2^(2n) strings and filtering, only ever make legal moves: open a group while fewer than n have been "
                     "opened, and close one only while more have been opened than closed. The second rule is the whole problem — it guarantees that no "
                     "prefix ever has more closing than opening parentheses.",
        "complexity": ("O(4^n / sqrt(n)) time (the Catalan number of answers)", "O(n) stack"),
        "code": {
            "cpp": r"""// Only legal moves: open if you can, close only when it stays balanced
vector<string> generateParenthesis(int n) {
    vector<string> out;
    function<void(int,int,string)> dfs = [&](int open, int close, string cur) {
        if ((int)cur.size() == 2 * n) { out.push_back(cur); return; }
        if (open < n) dfs(open + 1, close, cur + "(");       // room to open
        if (close < open) dfs(open, close + 1, cur + ")");   // never unbalanced
    };
    dfs(0, 0, "");
    return out;
}   // O(4^n / sqrt(n)) time · O(n) stack space""",
            "java": r"""// Only legal moves: open if you can, close only when it stays balanced
List<String> generateParenthesis(int n) {
    List<String> out = new ArrayList<>();
    dfs(n, 0, 0, new StringBuilder(), out);
    return out;
}
void dfs(int n, int open, int close, StringBuilder cur, List<String> out) {
    if (cur.length() == 2 * n) { out.add(cur.toString()); return; }
    if (open < n) {                          // room to open another group
        cur.append('(');
        dfs(n, open + 1, close, cur, out);
        cur.deleteCharAt(cur.length() - 1);
    }
    if (close < open) {                      // closing keeps it balanced
        cur.append(')');
        dfs(n, open, close + 1, cur, out);
        cur.deleteCharAt(cur.length() - 1);
    }
}   // O(4^n / sqrt(n)) time · O(n) stack space""",
            "python": r"""def generate_parenthesis(n):
    out = []

    def dfs(open_count, close_count, cur):
        if len(cur) == 2 * n:
            out.append(cur)                  # n pairs, perfectly balanced
            return
        if open_count < n:
            dfs(open_count + 1, close_count, cur + '(')   # room to open
        if close_count < open_count:
            dfs(open_count, close_count + 1, cur + ')')   # stays legal

    dfs(0, 0, '')
    return out""",
        },
    },
    {
        "slug": "combination-sum",
        "title": "Combination Sum",
        "difficulty": "Medium",
        "pattern": "choose with reuse allowed",
        "statement": "Given distinct positive candidates and a target, return all unique combinations that sum to the target, where each candidate may "
                     "be used any number of times (the order of the answer does not matter).",
        "examples": [("candidates = [2,3,6,7], target = 7", "[[2,2,3],[7]]"), ("candidates = [2,3,5], target = 8", "[[2,2,2,2],[2,3,3],[3,5]]"),
                     ("candidates = [2], target = 1", "[]")],
        "constraints": ["1 <= candidates.length <= 30", "2 <= candidates[i] <= 40", "1 <= target <= 40", "candidates are distinct"],
        "approach": "The start index returns, but the recursive call keeps it instead of moving past it — that single difference is \"reuse allowed\". "
                     "Two prunes matter: stop the loop once a candidate exceeds the remaining target (after sorting, everything later is larger), and "
                     "never look left of the current index, which is what keeps each combination from being emitted in many orders.",
        "complexity": ("O(n^(target/min)) worst case", "O(target/min) stack"),
        "code": {
            "cpp": r"""// Start index stays put for reuse; sorted order makes the prune exact
vector<vector<int>> combinationSum(vector<int>& candidates, int target) {
    sort(candidates.begin(), candidates.end());
    vector<vector<int>> out;
    vector<int> cur;
    function<void(int,int)> dfs = [&](int start, int remaining) {
        if (remaining == 0) { out.push_back(cur); return; }
        for (int i = start; i < (int)candidates.size(); i++) {
            if (candidates[i] > remaining) break;     // sorted: nothing later fits
            cur.push_back(candidates[i]);
            dfs(i, remaining - candidates[i]);        // i, not i + 1: reuse allowed
            cur.pop_back();
        }
    };
    dfs(0, target);
    return out;
}   // O(n^(target/minCandidate)) worst case · O(target/minCandidate) stack""",
            "java": r"""// Start index stays put for reuse; sorted order makes the prune exact
List<List<Integer>> combinationSum(int[] candidates, int target) {
    Arrays.sort(candidates);
    List<List<Integer>> out = new ArrayList<>();
    dfs(candidates, 0, target, new ArrayList<>(), out);
    return out;
}
void dfs(int[] cand, int start, int remaining, List<Integer> cur, List<List<Integer>> out) {
    if (remaining == 0) { out.add(new ArrayList<>(cur)); return; }
    for (int i = start; i < cand.length; i++) {
        if (cand[i] > remaining) break;          // sorted: nothing later fits
        cur.add(cand[i]);
        dfs(cand, i, remaining - cand[i], cur, out);   // i, not i + 1: reuse
        cur.remove(cur.size() - 1);
    }
}   // O(n^(target/minCandidate)) worst case · O(target/minCandidate) stack""",
            "python": r"""def combination_sum(candidates, target):
    candidates.sort()
    out = []
    cur = []

    def dfs(start, remaining):
        if remaining == 0:
            out.append(cur[:])               # the target is reached exactly
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break                        # sorted: nothing later fits
            cur.append(candidates[i])
            dfs(i, remaining - candidates[i])   # same i: reuse allowed
            cur.pop()

    dfs(0, target)
    return out""",
        },
    },
    {
        "slug": "subsets-ii",
        "title": "Subsets II",
        "difficulty": "Medium",
        "pattern": "duplicates handled by sorting and skipping",
        "statement": "Return all subsets of nums, which may contain duplicates, without repeating any subset (the order of the answer does not matter).",
        "examples": [("nums = [1,2,2]", "[[],[1],[1,2],[1,2,2],[2],[2,2]]"), ("nums = [0]", "[[],[0]]")],
        "constraints": ["1 <= nums.length <= 10", "-10 <= nums[i] <= 10"],
        "approach": "Sort first, then at each level of the recursion skip a value that equals the previous value tried at that same level. Sorting means "
                     "equal values sit together, so \"same as the one before\" is exactly \"this branch would duplicate the previous branch\" — the "
                     "subsets template with one extra line.",
        "complexity": ("O(2^n · n) time", "O(2^n · n) output"),
        "code": {
            "cpp": r"""// Sort, then skip a value equal to the one tried at the same level
vector<vector<int>> subsetsWithDup(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> out;
    vector<int> cur;
    function<void(int)> dfs = [&](int start) {
        out.push_back(cur);
        for (int i = start; i < (int)nums.size(); i++) {
            if (i > start && nums[i] == nums[i-1]) continue;   // duplicate branch
            cur.push_back(nums[i]);
            dfs(i + 1);
            cur.pop_back();
        }
    };
    dfs(0);
    return out;
}   // O(2^n · n) time · O(2^n · n) output space""",
            "java": r"""// Sort, then skip a value equal to the one tried at the same level
List<List<Integer>> subsetsWithDup(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> out = new ArrayList<>();
    dfs(nums, 0, new ArrayList<>(), out);
    return out;
}
void dfs(int[] nums, int start, List<Integer> cur, List<List<Integer>> out) {
    out.add(new ArrayList<>(cur));
    for (int i = start; i < nums.length; i++) {
        if (i > start && nums[i] == nums[i-1]) continue;   // duplicate branch
        cur.add(nums[i]);
        dfs(nums, i + 1, cur, out);
        cur.remove(cur.size() - 1);
    }
}   // O(2^n · n) time · O(2^n · n) output space""",
            "python": r"""def subsets_with_dup(nums):
    nums.sort()                          # equal values end up side by side
    out = []
    cur = []

    def dfs(start):
        out.append(cur[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i-1]:
                continue                 # this branch repeats the previous one
            cur.append(nums[i])
            dfs(i + 1)
            cur.pop()

    dfs(0)
    return out""",
        },
    },
    {
        "slug": "letter-tile-possibilities",
        "title": "Letter Tile Possibilities",
        "difficulty": "Medium",
        "pattern": "multiset counting without enumerating strings",
        "statement": "Given a string of tiles, count how many different non-empty sequences can be made using each tile at most once.",
        "examples": [("tiles = \"AAB\"", "8"), ("tiles = \"AAABBC\"", "188"), ("tiles = \"V\"", "1")],
        "constraints": ["1 <= tiles.length <= 7", "tiles consists of uppercase letters"],
        "approach": "Forget the strings and count the prefixes: keep 26 counters and, at every level, try each letter that still has a copy left. Each "
                     "step of the recursion *is* one new sequence, so the count is just the number of recursive steps taken — a counting backtracking "
                     "problem with no output list at all.",
        "complexity": ("O(number of sequences) time", "O(n) stack"),
        "code": {
            "cpp": r"""// Count the prefixes instead of building the strings
int numTilePossibilities(string tiles) {
    int count[26] = {0};
    for (char c : tiles) count[c - 'A']++;
    int total = 0;
    function<void()> dfs = [&]() {
        for (int c = 0; c < 26; c++) {
            if (!count[c]) continue;
            count[c]--;                      // use one tile of this letter
            total++;                         // this prefix is a new sequence
            dfs();
            count[c]++;                      // give it back
        }
    };
    dfs();
    return total;
}   // O(number of sequences) time · O(n) stack space""",
            "java": r"""// Count the prefixes instead of building the strings
int numTilePossibilities(String tiles) {
    int[] count = new int[26];
    for (char c : tiles.toCharArray()) count[c - 'A']++;
    return dfs(count);
}
int dfs(int[] count) {
    int total = 0;
    for (int c = 0; c < 26; c++) {
        if (count[c] == 0) continue;
        count[c]--;                          // use one tile of this letter
        total += 1 + dfs(count);              // this prefix plus its extensions
        count[c]++;                          // give it back
    }
    return total;
}   // O(number of sequences) time · O(n) stack space""",
            "python": r"""def num_tile_possibilities(tiles):
    counts = [0] * 26
    for ch in tiles:
        counts[ord(ch) - 65] += 1
    total = 0

    def dfs():
        nonlocal total
        for i in range(26):
            if counts[i] == 0:
                continue
            counts[i] -= 1                   # use one tile of this letter
            total += 1                       # this prefix is a new sequence
            dfs()
            counts[i] += 1                   # give it back

    dfs()
    return total""",
        },
    },
    {
        "slug": "unique-binary-search-trees-ii",
        "title": "Unique Binary Search Trees II",
        "difficulty": "Medium",
        "pattern": "recursive structure generation",
        "statement": "Return all structurally different binary search trees holding the values 1..n (the order of the answer does not matter).",
        "examples": [("n = 3", "[[1,null,2,null,3],[1,null,3,2],[2,1,3],[3,1,null,null,2],[3,2,null,1]]"), ("n = 1", "[[1]]")],
        "constraints": ["1 <= n <= 8"],
        "approach": "Every BST over a range has a root, and once the root is fixed the left and right subtrees are BSTs over the two smaller ranges. So "
                     "the recursion returns all trees for a range, and the answer is the cross product of left and right choices around each possible "
                     "root — recursion that builds values instead of just counting them.",
        "complexity": ("O(Catalan(n)) trees, each O(n) nodes", "O(Catalan(n) · n)"),
        "code": {
            "cpp": r"""// Every root splits the range; the answer is left x right around it
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
vector<TreeNode*> generateTrees(int n) {
    function<vector<TreeNode*>(int,int)> build = [&](int lo, int hi) -> vector<TreeNode*> {
        vector<TreeNode*> trees;
        if (lo > hi) { trees.push_back(nullptr); return trees; }   // one empty tree
        for (int rootVal = lo; rootVal <= hi; rootVal++) {
            vector<TreeNode*> lefts = build(lo, rootVal - 1);
            vector<TreeNode*> rights = build(rootVal + 1, hi);
            for (TreeNode* l : lefts)
                for (TreeNode* r : rights) {
                    TreeNode* root = new TreeNode(rootVal);
                    root->left = l;
                    root->right = r;
                    trees.push_back(root);
                }
        }
        return trees;
    };
    return n == 0 ? vector<TreeNode*>() : build(1, n);
}   // O(Catalan(n) · n) time and space""",
            "java": r"""// Every root splits the range; the answer is left x right around it
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
List<TreeNode> generateTrees(int n) {
    return build(1, n);
}
List<TreeNode> build(int lo, int hi) {
    List<TreeNode> trees = new ArrayList<>();
    if (lo > hi) { trees.add(null); return trees; }        // one empty tree
    for (int rootVal = lo; rootVal <= hi; rootVal++) {
        for (TreeNode l : build(lo, rootVal - 1))
            for (TreeNode r : build(rootVal + 1, hi)) {
                TreeNode root = new TreeNode(rootVal);
                root.left = l;
                root.right = r;
                trees.add(root);
            }
    }
    return trees;
}   // O(Catalan(n) · n) time and space""",
            "python": r"""def generate_trees(n):
    class TreeNode:                      # the judge provides this class
        def __init__(self, val=0, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    def build(lo, hi):
        if lo > hi:
            return [None]                # one empty tree
        trees = []
        for root_val in range(lo, hi + 1):
            for l in build(lo, root_val - 1):
                for r in build(root_val + 1, hi):
                    trees.append(TreeNode(root_val, l, r))
        return trees

    return build(1, n)""",
        },
    },
    {
        "slug": "n-queens-ii",
        "title": "N-Queens II",
        "difficulty": "Hard",
        "pattern": "bitmask backtracking (counting only)",
        "statement": "Return the number of ways to place n queens on an n x n board so that no two attack each other.",
        "examples": [("n = 4", "2"), ("n = 1", "1")],
        "constraints": ["1 <= n <= 9"],
        "approach": "Place one queen per row and remember, in three bitmasks, which columns and both diagonals are already occupied. A diagonal is "
                     "identified by row + col (one direction) and row - col (the other), so attacks are two shifts and an AND. Counting instead of "
                     "printing lets the same recursion skip board construction entirely.",
        "complexity": ("O(n!) with heavy pruning", "O(n) stack"),
        "code": {
            "cpp": r"""// One queen per row; three bitmasks rule out columns and diagonals
int totalNQueens(int n) {
    int count = 0;
    function<void(int,int,int,int)> dfs = [&](int row, int cols, int diag1, int diag2) {
        if (row == n) { count++; return; }
        int free = ((1 << n) - 1) & ~(cols | diag1 | diag2);   // legal columns
        while (free) {
            int bit = free & -free;                 // lowest legal column
            free -= bit;
            dfs(row + 1, cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1);
        }
    };
    dfs(0, 0, 0, 0);
    return count;
}   // O(n!) with pruning · O(n) stack space""",
            "java": r"""// One queen per row; three bitmasks rule out columns and diagonals
int totalNQueens(int n) {
    return dfs(0, 0, 0, 0, n);
}
int dfs(int row, int cols, int diag1, int diag2, int n) {
    if (row == n) return 1;
    int free = ((1 << n) - 1) & ~(cols | diag1 | diag2);   // legal columns
    int count = 0;
    while (free != 0) {
        int bit = free & -free;                     // lowest legal column
        free -= bit;
        count += dfs(row + 1, cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1, n);
    }
    return count;
}   // O(n!) with pruning · O(n) stack space""",
            "python": r"""def total_n_queens(n):
    count = 0
    full = (1 << n) - 1

    def dfs(row, cols, diag1, diag2):
        nonlocal count
        if row == n:
            count += 1                   # every row got its queen
            return
        free = full & ~(cols | diag1 | diag2)     # legal columns for this row
        while free:
            bit = free & -free           # lowest legal column
            free -= bit
            dfs(row + 1, cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1)

    dfs(0, 0, 0, 0)
    return count""",
        },
    },
    {
        "slug": "n-queens",
        "title": "N-Queens",
        "difficulty": "Hard",
        "pattern": "bitmask backtracking with board building",
        "statement": "Return every distinct solution of the n-queens puzzle, each board written as n strings (the order of the answer does not matter).",
        "examples": [("n = 4", "[[\".Q..\",\"...Q\",\"Q...\",\"..Q.\"],[\"..Q.\",\"Q...\",\"...Q\",\".Q..\"]]"), ("n = 1", "[[\"Q\"]]")],
        "constraints": ["1 <= n <= 9"],
        "approach": "The counting version plus one more thing to carry: the board itself. Write the queen into the current row, recurse, then erase it — "
                     "the same place-and-undo rhythm as the subsets template, with the three bitmasks doing the legality test in constant time per row.",
        "complexity": ("O(n!) with pruning, times O(n) to record each board", "O(n²) board plus O(n) stack"),
        "code": {
            "cpp": r"""// Place, recurse, erase: the board is carried along as mutable state
vector<vector<string>> solveNQueens(int n) {
    vector<vector<string>> out;
    vector<string> board(n, string(n, '.'));
    function<void(int,int,int,int)> dfs = [&](int row, int cols, int diag1, int diag2) {
        if (row == n) { out.push_back(board); return; }
        int free = ((1 << n) - 1) & ~(cols | diag1 | diag2);
        while (free) {
            int bit = free & -free;
            free -= bit;
            int col = __builtin_ctz(bit);
            board[row][col] = 'Q';                   // place
            dfs(row + 1, cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1);
            board[row][col] = '.';                   // undo
        }
    };
    dfs(0, 0, 0, 0);
    return out;
}   // O(n! · n^2) time · O(n^2) space""",
            "java": r"""// Place, recurse, erase: the board is carried along as mutable state
List<List<String>> solveNQueens(int n) {
    List<List<String>> out = new ArrayList<>();
    char[][] board = new char[n][n];
    for (char[] row : board) Arrays.fill(row, '.');
    dfs(0, 0, 0, 0, n, board, out);
    return out;
}
void dfs(int row, int cols, int diag1, int diag2, int n, char[][] board, List<List<String>> out) {
    if (row == n) {
        List<String> snapshot = new ArrayList<>();
        for (char[] r : board) snapshot.add(new String(r));
        out.add(snapshot);
        return;
    }
    int free = ((1 << n) - 1) & ~(cols | diag1 | diag2);
    while (free != 0) {
        int bit = free & -free;
        free -= bit;
        int col = Integer.numberOfTrailingZeros(bit);
        board[row][col] = 'Q';                       // place
        dfs(row + 1, cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1, n, board, out);
        board[row][col] = '.';                       // undo
    }
}   // O(n! · n^2) time · O(n^2) space""",
            "python": r"""def solve_n_queens(n):
    out = []
    board = [['.'] * n for _ in range(n)]
    full = (1 << n) - 1

    def dfs(row, cols, diag1, diag2):
        if row == n:
            out.append([''.join(r) for r in board])   # a complete solution
            return
        free = full & ~(cols | diag1 | diag2)
        while free:
            bit = free & -free
            free -= bit
            col = bit.bit_length() - 1
            board[row][col] = 'Q'                     # place
            dfs(row + 1, cols | bit, (diag1 | bit) << 1, (diag2 | bit) >> 1)
            board[row][col] = '.'                     # undo

    dfs(0, 0, 0, 0)
    return out""",
        },
    },
    {
        "slug": "number-of-squareful-arrays",
        "title": "Number of Squareful Arrays",
        "difficulty": "Hard",
        "pattern": "permutation search with an adjacency test",
        "statement": "Count the permutations of nums in which the sum of every pair of adjacent elements is a perfect square.",
        "examples": [("nums = [1,17,8]", "2"), ("nums = [2,2,2]", "1")],
        "constraints": ["1 <= nums.length <= 12", "0 <= nums[i] <= 10^9"],
        "approach": "A permutation search with adjacency: try each unused element that forms a perfect square with the last placed one. Duplicates are "
                     "handled the subsets-II way — sort and skip an equal value at the same level — so [2,2,2] is counted once rather than six times, "
                     "and precomputing which pairs are squareful turns the inner test into a table lookup.",
        "complexity": ("O(n!) worst case with duplicate pruning", "O(n²)"),
        "code": {
            "cpp": r"""// Permute with an adjacency test; skip equal values at the same level
int numSquarefulPerms(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    int n = nums.size();
    vector<vector<bool>> ok(n, vector<bool>(n, false));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            if (i == j) continue;
            long long s = (long long)nums[i] + nums[j];
            long long r = (long long)sqrt((double)s);
            ok[i][j] = (r * r == s) || ((r+1) * (r+1) == s);   // perfect square?
        }
    vector<bool> used(n, false);
    int total = 0;
    function<void(int,int)> dfs = [&](int last, int depth) {
        if (depth == n) { total++; return; }
        for (int i = 0; i < n; i++) {
            if (used[i]) continue;
            if (i > 0 && nums[i] == nums[i-1] && !used[i-1]) continue;   // duplicate
            if (last >= 0 && !ok[last][i]) continue;                     // not squareful
            used[i] = true;
            dfs(i, depth + 1);
            used[i] = false;
        }
    };
    dfs(-1, 0);
    return total;
}   // O(n!) with duplicate pruning · O(n^2) space""",
            "java": r"""// Permute with an adjacency test; skip equal values at the same level
int numSquarefulPerms(int[] nums) {
    Arrays.sort(nums);
    int n = nums.length;
    boolean[][] ok = new boolean[n][n];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            if (i == j) continue;
            long s = (long) nums[i] + nums[j];
            long r = (long) Math.sqrt(s);
            ok[i][j] = (r * r == s);             // a perfect square?
        }
    return dfs(nums, new boolean[n], -1, 0, ok);
}
int dfs(int[] nums, boolean[] used, int last, int depth, boolean[][] ok) {
    if (depth == nums.length) return 1;
    int total = 0;
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        if (i > 0 && nums[i] == nums[i-1] && !used[i-1]) continue;   // duplicate
        if (last >= 0 && !ok[last][i]) continue;                     // not squareful
        used[i] = true;
        total += dfs(nums, used, i, depth + 1, ok);
        used[i] = false;
    }
    return total;
}   // O(n!) with duplicate pruning · O(n^2) space""",
            "python": r"""def num_squareful_perms(nums):
    nums.sort()
    n = len(nums)

    def squareful(a, b):
        s = a + b
        r = int(s ** 0.5)
        return r * r == s                    # is the sum a perfect square?

    ok = [[squareful(nums[i], nums[j]) if i != j else False for j in range(n)]
          for i in range(n)]
    used = [False] * n
    total = 0

    def dfs(last, depth):
        nonlocal total
        if depth == n:
            total += 1                       # every adjacent pair was squareful
            return
        for i in range(n):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue                     # this copy repeats the previous branch
            if last >= 0 and not ok[last][i]:
                continue
            used[i] = True
            dfs(i, depth + 1)
            used[i] = False

    dfs(-1, 0)
    return total""",
        },
    },
    {
        "slug": "unique-paths-iii",
        "title": "Unique Paths III",
        "difficulty": "Hard",
        "pattern": "coverage search (Hamiltonian style)",
        "statement": "Walking in four directions over the non-obstacle squares, count the paths from the start square to the end square that step on "
                     "every non-obstacle square exactly once.",
        "examples": [("grid = [[1,0,0,0],[0,0,0,0],[0,0,2,-1]]", "2"), ("grid = [[1,0,0,0],[0,0,0,0],[0,0,0,2]]", "4"),
                     ("grid = [[0,1],[2,0]]", "0")],
        "constraints": ["1 <= rows, cols <= 20", "1 <= non-obstacle squares <= 20", "grid contains exactly one 1 and one 2"],
        "approach": "The answer must use every walkable square, so the search carries a count of squares already visited and only accepts a path that "
                     "arrives at the end with that count equal to the total. Marking the current square as an obstacle on the way down (and restoring "
                     "it after) is the visited set — cheap, and impossible to forget to undo.",
        "complexity": ("O(4^k) for k walkable squares (k <= 20, heavily pruned)", "O(k) stack"),
        "code": {
            "cpp": r"""// Must cover every walkable square; mark and restore on the way
int uniquePathsIII(vector<vector<int>>& grid) {
    int R = grid.size(), C = grid[0].size();
    int total = 0, sr = 0, sc = 0;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) {
            if (grid[r][c] != -1) total++;       // squares that must be walked
            if (grid[r][c] == 1) { sr = r; sc = c; }
        }
    int count = 0;
    int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    function<void(int,int,int)> dfs = [&](int r, int c, int walked) {
        if (grid[r][c] == 2) {                   // reached the end
            if (walked == total) count++;        // ... having covered everything
            return;
        }
        grid[r][c] = -1;                         // mark visited
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= R || nc < 0 || nc >= C || grid[nr][nc] == -1) continue;
            dfs(nr, nc, walked + 1);
        }
        grid[r][c] = 0;                          // restore for other paths
    };
    dfs(sr, sc, 1);
    return count;
}   // O(4^k) with pruning · O(k) stack space""",
            "java": r"""// Must cover every walkable square; mark and restore on the way
int uniquePathsIII(int[][] grid) {
    int R = grid.length, C = grid[0].length;
    int total = 0, sr = 0, sc = 0;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) {
            if (grid[r][c] != -1) total++;       // squares that must be walked
            if (grid[r][c] == 1) { sr = r; sc = c; }
        }
    return dfs(grid, sr, sc, 1, total);
}
int dfs(int[][] grid, int r, int c, int walked, int total) {
    if (grid[r][c] == 2) return walked == total ? 1 : 0;   // end, fully covered?
    grid[r][c] = -1;                             // mark visited
    int count = 0;
    int[] dr = {1,-1,0,0}, dc = {0,0,1,-1};
    for (int d = 0; d < 4; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= grid.length || nc < 0 || nc >= grid[0].length) continue;
        if (grid[nr][nc] == -1) continue;
        count += dfs(grid, nr, nc, walked + 1, total);
    }
    grid[r][c] = 0;                              // restore for other paths
    return count;
}   // O(4^k) with pruning · O(k) stack space""",
            "python": r"""def unique_paths_iii(grid):
    R, C = len(grid), len(grid[0])
    total = sum(1 for r in range(R) for c in range(C) if grid[r][c] != -1)
    start = next((r, c) for r in range(R) for c in range(C) if grid[r][c] == 1)
    count = 0

    def dfs(r, c, walked):
        nonlocal count
        if grid[r][c] == 2:                  # reached the end square
            if walked == total:              # ... having covered everything
                count += 1
            return
        grid[r][c] = -1                      # mark visited
        for nr, nc in ((r+1,c), (r-1,c), (r,c+1), (r,c-1)):
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != -1:
                dfs(nr, nc, walked + 1)
        grid[r][c] = 0                       # restore for other paths

    dfs(start[0], start[1], 1)
    return count""",
        },
    },
    {
        "slug": "maximum-score-words-formed-by-letters",
        "title": "Maximum Score Words Formed by Letters",
        "difficulty": "Hard",
        "pattern": "choose or skip with a shared budget",
        "statement": "Each word has a score obtained by adding the scores of its letters, and the given letters are a limited pool that each word "
                     "consumes. Return the largest total score of any set of words that can be spelled with the pool.",
        "examples": [("words = [\"dog\",\"cat\",\"dad\",\"good\"], letters = [\"a\",\"a\",\"c\",\"d\",\"d\",\"d\",\"g\",\"o\",\"o\"], score = 26 values starting 1,0,9,5,0,0,3,...",
                      "23"),
                     ("words = [\"leetcode\"], letters = [\"l\",\"e\",\"t\",\"c\",\"o\",\"d\"], score = letter scores", "0")],
        "constraints": ["1 <= words.length <= 14", "1 <= words[i].length <= 15", "1 <= letters.length <= 100", "score.length == 26"],
        "approach": "Take the letters as a 26-slot budget and run the include/exclude recursion over the words: taking a word spends its letters for "
                     "the whole subtree and gives them back afterwards. A suffix-sum bound — the total score of all words still to be considered — "
                     "cuts a branch the moment even the best case cannot beat the current best, which is what keeps 14 words tractable.",
        "complexity": ("O(2^n · 26) with pruning", "O(n) stack"),
        "code": {
            "cpp": r"""// Include/exclude over words with a shared 26-slot letter budget
int maxScoreWords(vector<string>& words, vector<char>& letters, vector<int>& score) {
    int have[26] = {0};
    for (char c : letters) have[c - 'a']++;
    int n = words.size();
    vector<array<int,26>> need(n);
    vector<int> worth(n, 0);
    for (int i = 0; i < n; i++) {
        need[i].fill(0);
        for (char c : words[i]) { need[i][c - 'a']++; worth[i] += score[c - 'a']; }
    }
    vector<int> suffix(n + 1, 0);
    for (int i = n - 1; i >= 0; i--) suffix[i] = suffix[i + 1] + worth[i];
    int best = 0;
    function<void(int,int)> dfs = [&](int i, int got) {
        if (got + suffix[i] <= best) return;     // cannot beat the best any more
        if (i == n) { best = max(best, got); return; }
        bool fits = true;
        for (int c = 0; c < 26; c++) if (need[i][c] > have[c]) { fits = false; break; }
        if (fits) {                              // take the word
            for (int c = 0; c < 26; c++) have[c] -= need[i][c];
            dfs(i + 1, got + worth[i]);
            for (int c = 0; c < 26; c++) have[c] += need[i][c];   // give back
        }
        dfs(i + 1, got);                         // skip the word
    };
    dfs(0, 0);
    return best;
}   // O(2^n · 26) with pruning · O(n) stack""",
            "java": r"""// Include/exclude over words with a shared 26-slot letter budget
int maxScoreWords(String[] words, char[] letters, int[] score) {
    int[] have = new int[26];
    for (char c : letters) have[c - 'a']++;
    int n = words.length;
    int[][] need = new int[n][26];
    int[] worth = new int[n];
    for (int i = 0; i < n; i++)
        for (char c : words[i].toCharArray()) {
            need[i][c - 'a']++;
            worth[i] += score[c - 'a'];
        }
    int[] suffix = new int[n + 1];
    for (int i = n - 1; i >= 0; i--) suffix[i] = suffix[i + 1] + worth[i];
    best = 0;
    dfs(0, 0, have, need, worth, suffix, n);
    return best;
}
private int best;
void dfs(int i, int got, int[] have, int[][] need, int[] worth, int[] suffix, int n) {
    if (got + suffix[i] <= best) return;         // cannot beat the best any more
    if (i == n) { best = Math.max(best, got); return; }
    boolean fits = true;
    for (int c = 0; c < 26; c++) if (need[i][c] > have[c]) { fits = false; break; }
    if (fits) {                                  // take the word
        for (int c = 0; c < 26; c++) have[c] -= need[i][c];
        dfs(i + 1, got + worth[i], have, need, worth, suffix, n);
        for (int c = 0; c < 26; c++) have[c] += need[i][c];   // give back
    }
    dfs(i + 1, got, have, need, worth, suffix, n);            // skip the word
}   // O(2^n · 26) with pruning · O(n) stack""",
            "python": r"""def max_score_words(words, letters, score):
    have = [0] * 26
    for ch in letters:
        have[ord(ch) - 97] += 1

    need = []
    worth = []
    for w in words:
        counts = [0] * 26
        total = 0
        for ch in w:
            counts[ord(ch) - 97] += 1
            total += score[ord(ch) - 97]
        need.append(counts)
        worth.append(total)

    suffix = [0] * (len(words) + 1)          # best possible still ahead
    for i in range(len(words) - 1, -1, -1):
        suffix[i] = suffix[i + 1] + worth[i]

    best = 0

    def dfs(i, got):
        nonlocal best
        if got + suffix[i] <= best:
            return                           # cannot beat the best any more
        if i == len(words):
            best = max(best, got)
            return
        if all(need[i][c] <= have[c] for c in range(26)):
            for c in range(26):
                have[c] -= need[i][c]        # spend the letters
            dfs(i + 1, got + worth[i])
            for c in range(26):
                have[c] += need[i][c]        # give them back
        dfs(i + 1, got)                      # skip the word

    dfs(0, 0)
    return best""",
        },
    },
    {
        "slug": "remove-invalid-parentheses",
        "title": "Remove Invalid Parentheses",
        "difficulty": "Hard",
        "pattern": "level-by-level removal (BFS over strings)",
        "statement": "Remove the fewest parentheses needed to make s balanced, and return all distinct results of that minimal length (the order of the "
                     "answer does not matter).",
        "examples": [("s = \"()())()\"", "[\"(())()\",\"()()()\"]"), ("s = \"(a)())()\"", "[\"(a())()\",\"(a)()()\"]"), ("s = \")(\"", "[\"\"]")],
        "constraints": ["1 <= s.length <= 25", "s consists of lowercase letters and parentheses"],
        "approach": "Because the answer needs the *fewest* removals, search breadth-first over removal counts: keep the set of strings reachable by "
                     "deleting exactly k characters, test each level for balance, and stop at the first level that contains a balanced string. Working "
                     "level by level is what guarantees minimality, and a set per level removes duplicate work.",
        "complexity": ("O(2^n · n) worst case", "O(2^n · n)"),
        "code": {
            "cpp": r"""// BFS over deletion counts: the first balanced level is minimal
vector<string> removeInvalidParentheses(string s) {
    auto valid = [](const string& t) {
        int bal = 0;
        for (char c : t) {
            if (c == '(') bal++;
            else if (c == ')') {
                bal--;
                if (bal < 0) return false;       // a closing with nothing open
            }
        }
        return bal == 0;                          // nothing left open
    };
    unordered_set<string> level{s};
    while (!level.empty()) {
        vector<string> good;
        for (const string& t : level) if (valid(t)) good.push_back(t);
        if (!good.empty()) return good;           // fewest removals reached
        unordered_set<string> next;
        for (const string& t : level)
            for (size_t i = 0; i < t.size(); i++)
                if (t[i] == '(' || t[i] == ')')
                    next.insert(t.substr(0, i) + t.substr(i + 1));   // delete one
        level = move(next);
    }
    return {""};
}   // O(2^n · n) worst case · O(2^n · n) space""",
            "java": r"""// BFS over deletion counts: the first balanced level is minimal
List<String> removeInvalidParentheses(String s) {
    Set<String> level = new HashSet<>();
    level.add(s);
    while (!level.isEmpty()) {
        List<String> good = new ArrayList<>();
        for (String t : level) if (valid(t)) good.add(t);
        if (!good.isEmpty()) return good;         // fewest removals reached
        Set<String> next = new HashSet<>();
        for (String t : level)
            for (int i = 0; i < t.length(); i++)
                if (t.charAt(i) == '(' || t.charAt(i) == ')')
                    next.add(t.substring(0, i) + t.substring(i + 1));   // delete one
        level = next;
    }
    return List.of("");
}
boolean valid(String t) {
    int bal = 0;
    for (char c : t.toCharArray()) {
        if (c == '(') bal++;
        else if (c == ')') {
            bal--;
            if (bal < 0) return false;             // a closing with nothing open
        }
    }
    return bal == 0;                               // nothing left open
}   // O(2^n · n) worst case · O(2^n · n) space""",
            "python": r"""def remove_invalid_parentheses(s):
    def valid(t):
        bal = 0
        for ch in t:
            if ch == '(':
                bal += 1
            elif ch == ')':
                bal -= 1
                if bal < 0:
                    return False             # a closing with nothing open
        return bal == 0                      # nothing left open

    level = {s}
    while level:
        good = [t for t in level if valid(t)]
        if good:
            return good                      # fewest removals reached
        nxt = set()
        for t in level:
            for i, ch in enumerate(t):
                if ch in '()':
                    nxt.add(t[:i] + t[i+1:])  # delete exactly one character
        level = nxt
    return ['']""",
        },
    },
    {
        "slug": "expression-add-operators",
        "title": "Expression Add Operators",
        "difficulty": "Hard",
        "pattern": "expression building with precedence",
        "statement": "Insert '+', '-' or '*' between the digits of num (keeping their order) so that the expression evaluates to target; return all "
                     "such expressions (the order of the answer does not matter).",
        "examples": [("num = \"123\", target = 6", "[\"1*2*3\",\"1+2+3\"]"), ("num = \"232\", target = 8", "[\"2*3+2\",\"2+3*2\"]"),
                     ("num = \"3456237490\", target = 9191", "[]")],
        "constraints": ["1 <= num.length <= 10", "num consists of digits", "-2^31 <= target <= 2^31 - 1", "no number may have a leading zero"],
        "approach": "The recursion consumes digits in groups (a group is the next number) and folds each group in with an operator. Multiplication is "
                     "the subtlety: because it binds tighter, the running total must be corrected by *undoing* the previous term — so the recursion "
                     "carries the value of the last term alongside the total, and a multiplication replaces that term with last × group.",
        "complexity": ("O(4^n) expressions with pruning", "O(n) stack"),
        "code": {
            "cpp": r"""// Carry the last term so '*' can undo it instead of reassociating
vector<string> addOperators(string num, int target) {
    vector<string> out;
    int n = num.size();
    function<void(int,string,long long,long long)> dfs =
        [&](int i, string expr, long long value, long long last) {
        if (i == n) {
            if (value == target) out.push_back(expr);
            return;
        }
        for (int j = i; j < n; j++) {
            if (j > i && num[i] == '0') break;      // a group cannot start with 0
            long long piece = stoll(num.substr(i, j - i + 1));
            string text = num.substr(i, j - i + 1);
            if (i == 0) {
                dfs(j + 1, text, piece, piece);     // the first group has no sign
            } else {
                dfs(j + 1, expr + "+" + text, value + piece, piece);
                dfs(j + 1, expr + "-" + text, value - piece, -piece);
                dfs(j + 1, expr + "*" + text, value - last + last * piece, last * piece);
            }
        }
    };
    dfs(0, "", 0, 0);
    return out;
}   // O(4^n) with pruning · O(n) stack space""",
            "java": r"""// Carry the last term so '*' can undo it instead of reassociating
List<String> addOperators(String num, int target) {
    List<String> out = new ArrayList<>();
    dfs(num, target, 0, "", 0L, 0L, out);
    return out;
}
void dfs(String num, int target, int i, String expr, long value, long last, List<String> out) {
    if (i == num.length()) {
        if (value == target) out.add(expr);
        return;
    }
    for (int j = i; j < num.length(); j++) {
        if (j > i && num.charAt(i) == '0') break;      // a group cannot start with 0
        long piece = Long.parseLong(num.substring(i, j + 1));
        String text = num.substring(i, j + 1);
        if (i == 0) {
            dfs(num, target, j + 1, text, piece, piece, out);   // first group
        } else {
            dfs(num, target, j + 1, expr + "+" + text, value + piece, piece, out);
            dfs(num, target, j + 1, expr + "-" + text, value - piece, -piece, out);
            dfs(num, target, j + 1, expr + "*" + text, value - last + last * piece, last * piece, out);
        }
    }
}   // O(4^n) with pruning · O(n) stack space""",
            "python": r"""def add_operators(num, target):
    out = []
    n = len(num)

    def dfs(i, expr, value, last):
        if i == n:
            if value == target:
                out.append(expr)
            return
        for j in range(i, n):
            if j > i and num[i] == '0':
                break                        # a group cannot start with 0
            piece = int(num[i:j+1])
            text = num[i:j+1]
            if i == 0:
                dfs(j + 1, text, piece, piece)          # the first group
            else:
                dfs(j + 1, expr + '+' + text, value + piece, piece)
                dfs(j + 1, expr + '-' + text, value - piece, -piece)
                # '*' binds tighter: undo the last term, then rescale it
                dfs(j + 1, expr + '*' + text, value - last + last * piece, last * piece)

    dfs(0, '', 0, 0)
    return out""",
        },
    },
    {
        "slug": "valid-permutations-for-di-sequence",
        "title": "Valid Permutations for DI Sequence",
        "difficulty": "Hard",
        "pattern": "rank DP over a growing permutation",
        "statement": "s is a string of 'I' and 'D'. Count the permutations p of 0..n (where n = len(s)) such that p[i] < p[i+1] where s[i] is 'I' "
                     "and p[i] > p[i+1] where it is 'D', modulo 10^9 + 7.",
        "examples": [("s = \"DID\"", "5"), ("s = \"D\"", "1")],
        "constraints": ["1 <= s.length <= 200", "s consists of 'D' and 'I'"],
        "approach": "Build the permutation one position at a time, tracking only the *rank* of the last value among the values used so far — the actual "
                     "numbers never matter, because inserting the next value only depends on whether it is bigger or smaller. dp[j] counts partial "
                     "arrangements ending with the j-th smallest value, and prefix or suffix sums make each step linear.",
        "complexity": ("O(n²) time", "O(n)"),
        "code": {
            "cpp": r"""// dp[j]: partial arrangements whose last value has rank j among those used
int numPermsDISequence(string s) {
    const long long MOD = 1e9 + 7;
    int m = s.size();
    vector<long long> dp(m + 1, 1);              // length 1: one arrangement
    for (int i = 1; i <= m; i++) {
        vector<long long> ndp(i + 1, 0);
        if (s[i-1] == 'I') {                     // the new value outranks the last
            long long run = 0;
            for (int j = 0; j <= i; j++) {
                ndp[j] = run;                    // ranks strictly below j
                if (j < i) run = (run + dp[j]) % MOD;
            }
        } else {                                 // the new value must rank below
            long long run = 0;
            for (int j = i; j >= 0; j--) {
                if (j < i) run = (run + dp[j]) % MOD;
                ndp[j] = run;
            }
        }
        dp = move(ndp);
    }
    long long total = 0;
    for (long long v : dp) total = (total + v) % MOD;
    return (int) total;
}   // O(n^2) time · O(n) space""",
            "java": r"""// dp[j]: partial arrangements whose last value has rank j among those used
int numPermsDISequence(String s) {
    final long MOD = 1_000_000_007L;
    int m = s.length();
    long[] dp = new long[m + 1];
    Arrays.fill(dp, 1);                          // length 1: one arrangement
    for (int i = 1; i <= m; i++) {
        long[] ndp = new long[i + 1];
        if (s.charAt(i-1) == 'I') {              // the new value outranks the last
            long run = 0;
            for (int j = 0; j <= i; j++) {
                ndp[j] = run;                    // ranks strictly below j
                if (j < i) run = (run + dp[j]) % MOD;
            }
        } else {                                 // the new value must rank below
            long run = 0;
            for (int j = i; j >= 0; j--) {
                if (j < i) run = (run + dp[j]) % MOD;
                ndp[j] = run;
            }
        }
        dp = ndp;
    }
    long total = 0;
    for (long v : dp) total = (total + v) % MOD;
    return (int) total;
}   // O(n^2) time · O(n) space""",
            "python": r"""def num_perms_di_sequence(s):
    MOD = 10**9 + 7
    m = len(s)
    dp = [1]                          # one arrangement of length 1

    for i in range(1, m + 1):
        ndp = [0] * (i + 1)
        if s[i-1] == 'I':             # the new value outranks the last one
            run = 0
            for j in range(i + 1):
                ndp[j] = run                  # ranks strictly below j
                if j < i:
                    run = (run + dp[j]) % MOD
        else:                         # 'D': the new value must rank below
            run = 0
            for j in range(i, -1, -1):
                if j < i:
                    run = (run + dp[j]) % MOD     # ranks at least j
                ndp[j] = run
        dp = ndp

    return sum(dp) % MOD""",
        },
    },
    {
        "slug": "find-minimum-time-to-finish-all-jobs",
        "title": "Find Minimum Time to Finish All Jobs",
        "difficulty": "Hard",
        "pattern": "binary search on the answer plus assignment search",
        "statement": "Assign every job to one of k workers; a worker's time is the sum of the jobs assigned to it. Return the smallest possible maximum "
                     "worker time.",
        "examples": [("jobs = [3,2,3], k = 3", "3"), ("jobs = [1,2,4,7,8], k = 2", "11")],
        "constraints": ["1 <= k <= jobs.length <= 12", "1 <= jobs[i] <= 10^7"],
        "approach": "The answer is monotone — if a limit works, every larger limit works — so binary search it, and for a fixed limit run a backtracking "
                     "assignment: place each job on a worker whose load stays inside the limit. Two prunes do the real work: never retry a worker whose "
                     "load equals the load just tried, and stop once an empty worker has failed, because every empty worker is interchangeable.",
        "complexity": ("O(log(sum) · k^n) with pruning", "O(n) stack"),
        "code": {
            "cpp": r"""// Binary search the limit; place each job on a worker that still fits
int minimumTimeRequired(vector<int>& jobs, int k) {
    sort(jobs.rbegin(), jobs.rend());            // big jobs first prune fastest
    int n = jobs.size();
    auto canFinish = [&](long long limit) {
        vector<long long> load(k, 0);
        function<bool(int)> place = [&](int i) -> bool {
            if (i == n) return true;
            unordered_set<long long> tried;      // identical loads are interchangeable
            for (int w = 0; w < k; w++) {
                if (tried.count(load[w])) continue;
                if (load[w] + jobs[i] > limit) continue;
                tried.insert(load[w]);
                load[w] += jobs[i];
                if (place(i + 1)) return true;
                load[w] -= jobs[i];
                if (load[w] == 0) break;         // an empty worker failed: stop
            }
            return false;
        };
        return place(0);
    };
    long long lo = *max_element(jobs.begin(), jobs.end()), hi = accumulate(jobs.begin(), jobs.end(), 0LL);
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (canFinish(mid)) hi = mid; else lo = mid + 1;
    }
    return (int) lo;
}   // O(log(sum) · k^n) with pruning · O(n) stack""",
            "java": r"""// Binary search the limit; place each job on a worker that still fits
int minimumTimeRequired(int[] jobs, int k) {
    Integer[] boxed = Arrays.stream(jobs).boxed().toArray(Integer[]::new);
    Arrays.sort(boxed, Collections.reverseOrder());   // big jobs first
    int n = boxed.length;
    int lo = boxed[0], hi = 0;
    for (int j : jobs) hi += j;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (canFinish(boxed, k, mid)) hi = mid; else lo = mid + 1;
    }
    return lo;
}
boolean canFinish(Integer[] jobs, int k, long limit) {
    return place(jobs, new long[k], 0, limit);
}
boolean place(Integer[] jobs, long[] load, int i, long limit) {
    if (i == jobs.length) return true;
    Set<Long> tried = new HashSet<>();           // identical loads are interchangeable
    for (int w = 0; w < load.length; w++) {
        if (tried.contains(load[w])) continue;
        if (load[w] + jobs[i] > limit) continue;
        tried.add(load[w]);
        load[w] += jobs[i];
        if (place(jobs, load, i + 1, limit)) return true;
        load[w] -= jobs[i];
        if (load[w] == 0) break;                 // an empty worker failed: stop
    }
    return false;
}   // O(log(sum) · k^n) with pruning · O(n) stack""",
            "python": r"""def minimum_time_required(jobs, k):
    jobs.sort(reverse=True)                      # big jobs first prune fastest

    def can_finish(limit):
        load = [0] * k

        def place(i):
            if i == len(jobs):
                return True
            tried = set()
            for w in range(k):
                if load[w] in tried:
                    continue                     # identical loads are interchangeable
                if load[w] + jobs[i] > limit:
                    continue
                tried.add(load[w])
                load[w] += jobs[i]
                if place(i + 1):
                    return True
                load[w] -= jobs[i]
                if load[w] == 0:
                    break                        # an empty worker failed: stop
            return False

        return place(0)

    lo, hi = max(jobs), sum(jobs)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_finish(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo""",
        },
    },
    {
        "slug": "maximum-number-of-achievable-transfer-requests",
        "title": "Maximum Number of Achievable Transfer Requests",
        "difficulty": "Hard",
        "pattern": "include/exclude over requests with a balance check",
        "statement": "Each request moves one employee from building a to building b. Return the largest number of requests that can all be satisfied, "
                     "meaning every building ends with as many employees as it started with.",
        "examples": [("n = 5, requests = [[0,1],[1,0],[0,1],[1,2],[2,0],[3,4]]", "5"),
                     ("n = 3, requests = [[0,0],[1,2],[2,1]]", "3")],
        "constraints": ["1 <= n <= 20", "1 <= requests.length <= 16", "requests[i].length == 2", "0 <= from, to < n"],
        "approach": "Every request is in or out, so walk the include/exclude tree and, at the leaves, accept the selection when the net movement of "
                     "every building is zero — taking a request simply decrements the source and increments the destination. A count bound (selected "
                     "so far plus requests left) prunes branches that can no longer beat the best found.",
        "complexity": ("O(2^requests · n)", "O(n)"),
        "code": {
            "cpp": r"""// Include/exclude each request; a selection counts when nets are zero
int maximumRequests(int n, vector<vector<int>>& requests) {
    int m = requests.size(), best = 0;
    vector<int> net(n, 0);
    function<void(int,int)> dfs = [&](int i, int taken) {
        if (taken + m - i <= best) return;       // cannot beat the best any more
        if (i == m) {
            for (int v : net) if (v != 0) return;    // some building is unbalanced
            best = max(best, taken);
            return;
        }
        int a = requests[i][0], b = requests[i][1];
        net[a]--; net[b]++;                      // take this request
        dfs(i + 1, taken + 1);
        net[a]++; net[b]--;                      // undo it
        dfs(i + 1, taken);                       // skip this request
    };
    dfs(0, 0);
    return best;
}   // O(2^m · n) with pruning · O(n) space""",
            "java": r"""// Include/exclude each request; a selection counts when nets are zero
int maximumRequests(int n, int[][] requests) {
    int[] net = new int[n];
    return dfs(requests, 0, 0, net, requests.length);
}
int dfs(int[][] requests, int i, int taken, int[] net, int m) {
    if (i == m) {
        for (int v : net) if (v != 0) return 0;  // some building is unbalanced
        return taken;
    }
    int a = requests[i][0], b = requests[i][1];
    net[a]--; net[b]++;                          // take this request
    int withIt = dfs(requests, i + 1, taken + 1, net, m);
    net[a]++; net[b]--;                          // undo it
    int without = dfs(requests, i + 1, taken, net, m);
    return Math.max(withIt, without);
}   // O(2^m · n) time · O(n) space""",
            "python": r"""def maximum_requests(n, requests):
    m = len(requests)
    net = [0] * n
    best = 0

    def dfs(i, taken):
        nonlocal best
        if taken + m - i <= best:
            return                           # cannot beat the best any more
        if i == m:
            if all(v == 0 for v in net):     # every building ends balanced
                best = max(best, taken)
            return
        a, b = requests[i]
        net[a] -= 1                          # take this request
        net[b] += 1
        dfs(i + 1, taken + 1)
        net[a] += 1                          # undo it
        net[b] -= 1
        dfs(i + 1, taken)                    # skip this request

    dfs(0, 0)
    return best""",
        },
    },
    {
        "slug": "24-game",
        "title": "24 Game",
        "difficulty": "Hard",
        "pattern": "arithmetic search over a shrinking list",
        "statement": "Using the four cards and the operations +, -, * and / (with parentheses), decide whether 24 can be reached; every card must be "
                     "used exactly once.",
        "examples": [("cards = [4,1,8,7]", "true"), ("cards = [1,2,1,2]", "false")],
        "constraints": ["cards.length == 4", "1 <= cards[i] <= 9", "division by zero is not allowed"],
        "approach": "Pick any two of the remaining numbers, replace them by the result of one operation, and recurse on the shorter list — that models "
                     "every parenthesisation, because a parenthesis is exactly a choice of which two values combine first. Because floating point is "
                     "involved, the final test compares against 24 with a small tolerance.",
        "complexity": ("O(1) in practice: at most 4! · 4³ combinations", "O(1)"),
        "code": {
            "cpp": r"""// Combine any two numbers into one, recursively: that is every parenthesis
bool judgePoint24(vector<int>& cards) {
    vector<double> nums(cards.begin(), cards.end());
    function<bool(vector<double>&)> dfs = [&](vector<double>& a) -> bool {
        if (a.size() == 1) return fabs(a[0] - 24.0) < 1e-6;   // close enough
        for (int i = 0; i < (int)a.size(); i++)
            for (int j = 0; j < (int)a.size(); j++) {
                if (i == j) continue;
                vector<double> rest;
                for (int k = 0; k < (int)a.size(); k++)
                    if (k != i && k != j) rest.push_back(a[k]);
                double x = a[i], y = a[j];
                vector<double> cands = {x + y, x - y, x * y};
                if (fabs(y) > 1e-9) cands.push_back(x / y);   // no division by zero
                for (double v : cands) {
                    rest.push_back(v);
                    if (dfs(rest)) return true;               // recurse on the shorter list
                    rest.pop_back();
                }
            }
        return false;
    };
    return dfs(nums);
}   // O(1) · at most 4! · 4^3 combinations""",
            "java": r"""// Combine any two numbers into one, recursively: that is every parenthesis
boolean judgePoint24(int[] cards) {
    double[] nums = new double[cards.length];
    for (int i = 0; i < cards.length; i++) nums[i] = cards[i];
    return dfs(nums);
}
boolean dfs(double[] a) {
    if (a.length == 1) return Math.abs(a[0] - 24.0) < 1e-6;   // close enough
    for (int i = 0; i < a.length; i++)
        for (int j = 0; j < a.length; j++) {
            if (i == j) continue;
            double[] rest = new double[a.length - 1];
            int at = 0;
            for (int k = 0; k < a.length; k++)
                if (k != i && k != j) rest[at++] = a[k];
            double x = a[i], y = a[j];
            double[] cands = {x + y, x - y, x * y};
            for (double v : cands) {
                rest[at] = v;
                if (dfs(rest)) return true;       // recurse on the shorter list
            }
            if (Math.abs(y) > 1e-9) {             // division by zero is not allowed
                rest[at] = x / y;
                if (dfs(rest)) return true;
            }
        }
    return false;
}   // O(1) · at most 4! · 4^3 combinations""",
            "python": r"""def judge_point24(cards):
    def dfs(nums):
        if len(nums) == 1:
            return abs(nums[0] - 24.0) < 1e-6     # close enough for floats
        for i in range(len(nums)):
            for j in range(len(nums)):
                if i == j:
                    continue
                rest = [nums[t] for t in range(len(nums)) if t != i and t != j]
                x, y = nums[i], nums[j]
                candidates = [x + y, x - y, x * y]
                if abs(y) > 1e-9:
                    candidates.append(x / y)      # division by zero is not allowed
                for v in candidates:
                    if dfs(rest + [v]):           # recurse on the shorter list
                        return True
        return False

    return dfs([float(c) for c in cards])""",
        },
    },
    {
        "slug": "sudoku-solver",
        "title": "Sudoku Solver",
        "difficulty": "Hard",
        "pattern": "constraint backtracking with sets",
        "statement": "Fill the 9 x 9 board so that every row, column and 3 x 3 box contains the digits 1-9 exactly once.",
        "examples": [("board = [[\"5\",\"3\",\".\",\".\",\"7\",\".\",\".\",\".\",\".\"],[\"6\",\".\",\".\",\"1\",\"9\",\"5\",\".\",\".\",\".\"],[\".\",\"9\",\"8\",\".\",\".\",\".\",\".\",\"6\",\".\"],[\"8\",\".\",\".\",\".\",\"6\",\".\",\".\",\".\",\"3\"],[\"4\",\".\",\".\",\"8\",\".\",\"3\",\".\",\".\",\"1\"],[\"7\",\".\",\".\",\".\",\"2\",\".\",\".\",\".\",\"6\"],[\".\",\"6\",\".\",\".\",\".\",\".\",\"2\",\"8\",\".\"],[\".\",\".\",\".\",\"4\",\"1\",\"9\",\".\",\".\",\"5\"],[\".\",\".\",\".\",\".\",\"8\",\".\",\".\",\"7\",\"9\"]]",
                      "the board becomes [[\"5\",\"3\",\"4\",\"6\",\"7\",\"8\",\"9\",\"1\",\"2\"],[\"6\",\"7\",\"2\",\"1\",\"9\",\"5\",\"3\",\"4\",\"8\"],[\"1\",\"9\",\"8\",\"3\",\"4\",\"2\",\"5\",\"6\",\"7\"],[\"8\",\"5\",\"9\",\"7\",\"6\",\"1\",\"4\",\"2\",\"3\"],[\"4\",\"2\",\"6\",\"8\",\"5\",\"3\",\"7\",\"9\",\"1\"],[\"7\",\"1\",\"3\",\"9\",\"2\",\"4\",\"8\",\"5\",\"6\"],[\"9\",\"6\",\"1\",\"5\",\"3\",\"7\",\"2\",\"8\",\"4\"],[\"2\",\"8\",\"7\",\"4\",\"1\",\"9\",\"6\",\"3\",\"5\"],[\"3\",\"4\",\"5\",\"2\",\"8\",\"6\",\"1\",\"7\",\"9\"]]")],
        "constraints": ["board.length == board[i].length == 9", "each cell is a digit or '.'", "the input has exactly one solution"],
        "approach": "Track the digits already present in each row, column and box in three sets, then walk the empty cells one at a time trying only the "
                     "digits that appear in none of the three. A digit that leads to a dead end is removed again — the classic constraint-propagation "
                     "backtracking, and consistent ordering of the empty cells is all the search needs to stay fast.",
        "complexity": ("O(9^(empties)) worst case, far less with propagation", "O(1) for the board"),
        "code": {
            "cpp": r"""// Three sets per cell group; try only digits absent from all three
void solveSudoku(vector<vector<char>>& board) {
    vector<unordered_set<char>> rows(9), cols(9), boxes(9);
    vector<pair<int,int>> empty;
    for (int r = 0; r < 9; r++)
        for (int c = 0; c < 9; c++) {
            int b = (r / 3) * 3 + c / 3;
            if (board[r][c] == '.') empty.push_back({r, c});
            else { rows[r].insert(board[r][c]); cols[c].insert(board[r][c]); boxes[b].insert(board[r][c]); }
        }
    function<bool(int)> place = [&](int i) -> bool {
        if (i == (int)empty.size()) return true;
        auto [r, c] = empty[i];
        int b = (r / 3) * 3 + c / 3;
        for (char d = '1'; d <= '9'; d++) {
            if (rows[r].count(d) || cols[c].count(d) || boxes[b].count(d)) continue;
            board[r][c] = d;                     // place and record
            rows[r].insert(d); cols[c].insert(d); boxes[b].insert(d);
            if (place(i + 1)) return true;
            rows[r].erase(d); cols[c].erase(d); boxes[b].erase(d);
            board[r][c] = '.';                   // undo
        }
        return false;
    };
    place(0);
}   // O(9^empties) worst case · O(1) extra space""",
            "java": r"""// Three sets per cell group; try only digits absent from all three
void solveSudoku(char[][] board) {
    Set<Character>[] rows = new HashSet[9], cols = new HashSet[9], boxes = new HashSet[9];
    for (int i = 0; i < 9; i++) { rows[i] = new HashSet<>(); cols[i] = new HashSet<>(); boxes[i] = new HashSet<>(); }
    List<int[]> empty = new ArrayList<>();
    for (int r = 0; r < 9; r++)
        for (int c = 0; c < 9; c++) {
            int b = (r / 3) * 3 + c / 3;
            if (board[r][c] == '.') empty.add(new int[]{r, c});
            else { rows[r].add(board[r][c]); cols[c].add(board[r][c]); boxes[b].add(board[r][c]); }
        }
    place(board, 0, empty, rows, cols, boxes);
}
boolean place(char[][] board, int i, List<int[]> empty, Set<Character>[] rows, Set<Character>[] cols, Set<Character>[] boxes) {
    if (i == empty.size()) return true;
    int r = empty.get(i)[0], c = empty.get(i)[1];
    int b = (r / 3) * 3 + c / 3;
    for (char d = '1'; d <= '9'; d++) {
        if (rows[r].contains(d) || cols[c].contains(d) || boxes[b].contains(d)) continue;
        board[r][c] = d;                         // place and record
        rows[r].add(d); cols[c].add(d); boxes[b].add(d);
        if (place(board, i + 1, empty, rows, cols, boxes)) return true;
        rows[r].remove(d); cols[c].remove(d); boxes[b].remove(d);
        board[r][c] = '.';                       // undo
    }
    return false;
}   // O(9^empties) worst case · O(1) extra space""",
            "python": r"""def solve_sudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty = []
    for r in range(9):
        for c in range(9):
            b = (r // 3) * 3 + c // 3
            if board[r][c] == '.':
                empty.append((r, c))
            else:
                rows[r].add(board[r][c]); cols[c].add(board[r][c]); boxes[b].add(board[r][c])

    def place(i):
        if i == len(empty):
            return True                      # every cell filled consistently
        r, c = empty[i]
        b = (r // 3) * 3 + c // 3
        for d in '123456789':
            if d in rows[r] or d in cols[c] or d in boxes[b]:
                continue                     # this digit already exists nearby
            board[r][c] = d                  # place and record
            rows[r].add(d); cols[c].add(d); boxes[b].add(d)
            if place(i + 1):
                return True
            rows[r].discard(d); cols[c].discard(d); boxes[b].discard(d)
            board[r][c] = '.'                # undo
        return False

    place(0)""",
        },
    },
]
