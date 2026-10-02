# Topic 7 · Trees & BSTs
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.

TOPIC = {
    "name": "Trees & BSTs",
    "tagline": "Recursion on a binary tree is three lines: handle null, recurse left, recurse right — the difficulty is deciding what each call returns.",
    "focus": "Two return styles cover almost everything: bottom-up functions that return a summary of the subtree (height, sum, validity) and top-down "
             "functions that pass context down (bounds, target sums, parent links). BST questions add one idea — the in-order sequence is sorted — "
             "and construction questions add index arithmetic on two traversals.",
    "ordering": "easy 1–6 are pure bottom-up recursion; medium 1–4 are traversals and classic BST properties, 5–8 are construction and path sums, "
                "9–12 are deletion, pruning and counting; hard 1–4 are path-based recursion and serialisation, 5–8 mix global state with "
                "bottom-up returns, 9–12 are iterator/ordering designs.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "max-depth-of-binary-tree",
        "title": "Maximum Depth of a Binary Tree",
        "difficulty": "Easy",
        "pattern": "bottom-up recursion",
        "statement": "Return the number of nodes on the longest path from the root down to a leaf.",
        "examples": [("root = [3,9,20,null,null,15,7]", "3"), ("root = []", "0")],
        "constraints": ["0 <= number of nodes <= 10^4", "-100 <= node values <= 100", "the empty tree has depth 0"],
        "approach": "The depth of a tree is one more than the deeper of its two subtrees; the base case is the empty tree, which has depth 0. "
                     "That single recurrence is the template for every bottom-up tree function in this topic.",
        "complexity": ("O(n)", "O(h) recursion depth"),
        "code": {
            "cpp": r"""// depth(v) = 1 + max(depth(left), depth(right))
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
int maxDepth(TreeNode* root) {
    if (!root) return 0;
    return 1 + max(maxDepth(root->left), maxDepth(root->right));
}   // O(n) time · O(h) stack space""",
            "java": r"""// depth(v) = 1 + max(depth(left), depth(right))
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
int maxDepth(TreeNode root) {
    if (root == null) return 0;
    return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}   // O(n) time · O(h) stack space""",
            "python": r"""def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))""",
        },
    },
    {
        "slug": "same-tree",
        "title": "Same Tree",
        "difficulty": "Easy",
        "pattern": "paired recursion",
        "statement": "Return true if two binary trees are structurally identical and hold the same values.",
        "examples": [("p = [1,2,3], q = [1,2,3]", "true"), ("p = [1,2], q = [1,null,2]", "false")],
        "constraints": ["0 <= nodes per tree <= 100", "-10^4 <= node values <= 10^4", "the comparison is exact"],
        "approach": "Recurse on both trees at once: the pair must either be two empties, or two nodes with equal values whose left pairs and right "
                     "pairs also match. Testing the null cases together is what keeps the code to four lines.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// Compare the two trees in lockstep
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
bool isSameTree(TreeNode* p, TreeNode* q) {
    if (!p || !q) return p == q;                 // both null, or exactly one null
    return p->val == q->val && isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
}   // O(n) time · O(h) stack space""",
            "java": r"""// Compare the two trees in lockstep
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
boolean isSameTree(TreeNode p, TreeNode q) {
    if (p == null || q == null) return p == q;   // both null, or exactly one null
    return p.val == q.val && isSameTree(p.left, q.left) && isSameTree(p.right, q.right);
}   // O(n) time · O(h) stack space""",
            "python": r"""def is_same_tree(p, q):
    if not p or not q:
        return p is q          # both None, or exactly one None
    return p.val == q.val and is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)""",
        },
    },
    {
        "slug": "invert-binary-tree",
        "title": "Invert Binary Tree",
        "difficulty": "Easy",
        "pattern": "swap then recurse",
        "statement": "Mirror the tree: every node's left and right subtrees are exchanged, and the root is returned.",
        "examples": [("root = [4,2,7,1,3,6,9]", "[4,7,2,9,6,3,1]"), ("root = []", "[]")],
        "constraints": ["0 <= number of nodes <= 100", "-100 <= node values <= 100", "the mirroring must be in place"],
        "approach": "Swap the two children at the current node, then recurse into both. Order does not matter, and the same shape of loop works "
                     "with an explicit queue if you prefer iterative form.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// Swap the children, then fix both subtrees
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
TreeNode* invertTree(TreeNode* root) {
    if (!root) return nullptr;
    swap(root->left, root->right);               // the local mirror step
    invertTree(root->left);
    invertTree(root->right);
    return root;
}   // O(n) time · O(h) stack space""",
            "java": r"""// Swap the children, then fix both subtrees
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
TreeNode invertTree(TreeNode root) {
    if (root == null) return null;
    TreeNode t = root.left; root.left = root.right; root.right = t;   // local mirror
    invertTree(root.left);
    invertTree(root.right);
    return root;
}   // O(n) time · O(h) stack space""",
            "python": r"""def invert_tree(root):
    if not root:
        return None
    root.left, root.right = root.right, root.left    # local mirror step
    invert_tree(root.left)
    invert_tree(root.right)
    return root""",
        },
    },
    {
        "slug": "symmetric-tree",
        "title": "Symmetric Tree",
        "difficulty": "Easy",
        "pattern": "mirrored paired recursion",
        "statement": "Return true if the tree is a mirror of itself around its centre.",
        "examples": [("root = [1,2,2,3,4,4,3]", "true"), ("root = [1,2,2,null,3,null,3]", "false")],
        "constraints": ["1 <= number of nodes <= 1000", "-100 <= node values <= 100", "the comparison is like for like"],
        "approach": "Same paired recursion as Same Tree, except the calls cross over: the left subtree of one node must match the *right* subtree "
                     "of the other. Writing a helper take (a, b) makes the crossing explicit instead of hiding it in index arithmetic.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// Cross-paired recursion: left of a with right of b
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
bool mirror(TreeNode* a, TreeNode* b) {
    if (!a || !b) return a == b;
    return a->val == b->val && mirror(a->left, b->right) && mirror(a->right, b->left);
}
bool isSymmetric(TreeNode* root) { return !root || mirror(root->left, root->right); }
// O(n) time · O(h) stack space""",
            "java": r"""// Cross-paired recursion: left of a with right of b
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
boolean mirror(TreeNode a, TreeNode b) {
    if (a == null || b == null) return a == b;
    return a.val == b.val && mirror(a.left, b.right) && mirror(a.right, b.left);
}
boolean isSymmetric(TreeNode root) { return root == null || mirror(root.left, root.right); }
// O(n) time · O(h) stack space""",
            "python": r"""def is_symmetric(root):
    def mirror(a, b):
        if not a or not b:
            return a is b
        return a.val == b.val and mirror(a.left, b.right) and mirror(a.right, b.left)

    return not root or mirror(root.left, root.right)""",
        },
    },
    {
        "slug": "diameter-of-binary-tree",
        "title": "Diameter of a Binary Tree",
        "difficulty": "Easy",
        "pattern": "height recursion + running best",
        "statement": "Return the length (number of edges) of the longest path between any two nodes of the tree; the path need not pass through the root.",
        "examples": [("root = [1,2,3,4,5]", "3"), ("root = [1,2]", "1")],
        "constraints": ["1 <= number of nodes <= 10^4", "-100 <= node values <= 100", "the path may bend at any node"],
        "approach": "Each node sees exactly the best path that bends at it: the height of the left subtree plus the height of the right. Return "
                     "heights upward while updating a running maximum — the standard way to combine a bottom-up return with a global answer.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// Return the height, but record the best bend at every node
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
int dfs(TreeNode* node, int& best) {
    if (!node) return 0;
    int l = dfs(node->left, best), r = dfs(node->right, best);
    best = max(best, l + r);                     // path bending at this node
    return 1 + max(l, r);                        // height reported upward
}
int diameterOfBinaryTree(TreeNode* root) { int best = 0; dfs(root, best); return best; }
// O(n) time · O(h) stack space""",
            "java": r"""// Return the height, but record the best bend at every node
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
private int best = 0;
int dfs(TreeNode node) {
    if (node == null) return 0;
    int l = dfs(node.left), r = dfs(node.right);
    best = Math.max(best, l + r);                // path bending at this node
    return 1 + Math.max(l, r);                   // height reported upward
}
int diameterOfBinaryTree(TreeNode root) { best = 0; dfs(root); return best; }
// O(n) time · O(h) stack space""",
            "python": r"""def diameter_of_binary_tree(root):
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0
        l, r = height(node.left), height(node.right)
        best = max(best, l + r)      # path that bends at this node
        return 1 + max(l, r)         # height handed back to the parent

    height(root)
    return best""",
        },
    },
    {
        "slug": "balanced-binary-tree",
        "title": "Balanced Binary Tree",
        "difficulty": "Easy",
        "pattern": "height with an early exit",
        "statement": "Return true if the tree is height-balanced: at every node the two subtree heights differ by at most one.",
        "examples": [("root = [3,9,20,null,null,15,7]", "true"), ("root = [1,2,2,3,3,null,null,4,4]", "false")],
        "constraints": ["0 <= number of nodes <= 5000", "-10^4 <= node values <= 10^4", "the check applies to every node, not just the root"],
        "approach": "Compute heights bottom-up and return -1 as soon as any subtree is unbalanced, so the failure propagates upward and the "
                     "recursion stops early instead of recomputing heights at every node (which would be O(n²)).",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// -1 means "already unbalanced", and it propagates upward
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
int check(TreeNode* node) {
    if (!node) return 0;
    int l = check(node->left);  if (l == -1) return -1;
    int r = check(node->right); if (r == -1) return -1;
    if (abs(l - r) > 1) return -1;               // this node breaks the rule
    return 1 + max(l, r);
}
bool isBalanced(TreeNode* root) { return check(root) != -1; }
// O(n) time · O(h) stack space""",
            "java": r"""// -1 means "already unbalanced", and it propagates upward
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
int check(TreeNode node) {
    if (node == null) return 0;
    int l = check(node.left);  if (l == -1) return -1;
    int r = check(node.right); if (r == -1) return -1;
    if (Math.abs(l - r) > 1) return -1;          // this node breaks the rule
    return 1 + Math.max(l, r);
}
boolean isBalanced(TreeNode root) { return check(root) != -1; }
// O(n) time · O(h) stack space""",
            "python": r"""def is_balanced(root):
    def check(node):
        if not node:
            return 0
        l = check(node.left)
        if l == -1:
            return -1
        r = check(node.right)
        if r == -1:
            return -1
        if abs(l - r) > 1:
            return -1            # unbalanced: stop the work here
        return 1 + max(l, r)

    return check(root) != -1""",
        },
    },
    # ---------------------------------------------------------------- MEDIUM
    {
        "slug": "binary-tree-level-order-traversal",
        "title": "Level Order Traversal",
        "difficulty": "Medium",
        "pattern": "queue + level size",
        "statement": "Return the node values level by level, from left to right, as a list of lists.",
        "examples": [("root = [3,9,20,null,null,15,7]", "[[3],[9,20],[15,7]]"), ("root = []", "[]")],
        "constraints": ["0 <= number of nodes <= 2000", "-1000 <= node values <= 1000", "levels must not be mixed together"],
        "approach": "A queue gives breadth-first order, but the levels only appear if you snapshot the queue's size *before* draining it: that "
                     "count is exactly one level. Forgetting the snapshot is the classic bug that merges levels.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Snapshot the queue size: that count is one level
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
vector<vector<int>> levelOrder(TreeNode* root) {
    vector<vector<int>> out;
    if (!root) return out;
    queue<TreeNode*> q; q.push(root);
    while (!q.empty()) {
        int size = q.size();                     // exactly one level
        vector<int> level;
        while (size--) {
            TreeNode* n = q.front(); q.pop();
            level.push_back(n->val);
            if (n->left) q.push(n->left);
            if (n->right) q.push(n->right);
        }
        out.push_back(level);
    }
    return out;
}   // O(n) time · O(n) space""",
            "java": r"""// Snapshot the queue size: that count is one level
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> out = new ArrayList<>();
    if (root == null) return out;
    Deque<TreeNode> q = new ArrayDeque<>();
    q.add(root);
    while (!q.isEmpty()) {
        int size = q.size();                     // exactly one level
        List<Integer> level = new ArrayList<>();
        while (size-- > 0) {
            TreeNode n = q.poll();
            level.add(n.val);
            if (n.left != null) q.add(n.left);
            if (n.right != null) q.add(n.right);
        }
        out.add(level);
    }
    return out;
}   // O(n) time · O(n) space""",
            "python": r"""from collections import deque

def level_order(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        size = len(q)                 # exactly one level
        level = []
        for _ in range(size):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        out.append(level)
    return out""",
        },
    },
    {
        "slug": "path-sum",
        "title": "Path Sum",
        "difficulty": "Medium",
        "pattern": "top-down target reduction",
        "statement": "Return true if some root-to-leaf path adds up to the target sum.",
        "examples": [("root = [5,4,8,11,null,13,4,7,2], targetSum = 22", "true"), ("root = [1,2,3], targetSum = 5", "false")],
        "constraints": ["0 <= number of nodes <= 5000", "-1000 <= values, targetSum <= 1000", "the path must end at a leaf"],
        "approach": "Carry the *remaining* target downward and subtract as you descend; at a leaf the remainder must be exactly zero. Checking "
                     "`!node->left && !node->right` (rather than `!node`) is what stops a half-finished path from counting as a leaf path.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// Subtract on the way down; a leaf must land exactly on zero
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
bool hasPathSum(TreeNode* node, int target) {
    if (!node) return false;
    if (!node->left && !node->right) return target == node->val;   // real leaf
    return hasPathSum(node->left, target - node->val) ||
           hasPathSum(node->right, target - node->val);
}   // O(n) time · O(h) stack space""",
            "java": r"""// Subtract on the way down; a leaf must land exactly on zero
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
boolean hasPathSum(TreeNode node, int target) {
    if (node == null) return false;
    if (node.left == null && node.right == null) return target == node.val;   // leaf
    return hasPathSum(node.left, target - node.val)
        || hasPathSum(node.right, target - node.val);
}   // O(n) time · O(h) stack space""",
            "python": r"""def has_path_sum(node, target):
    if not node:
        return False
    if not node.left and not node.right:
        return target == node.val        # a leaf must match exactly
    return (has_path_sum(node.left, target - node.val)
            or has_path_sum(node.right, target - node.val))""",
        },
    },
    {
        "slug": "lowest-common-ancestor-of-a-bst",
        "title": "Lowest Common Ancestor in a BST",
        "difficulty": "Medium",
        "pattern": "walk the search path",
        "statement": "Given two nodes in a BST, return their lowest common ancestor.",
        "examples": [("root = [6,2,8,0,4,7,9], p = 2, q = 8", "6"), ("root = [6,2,8,0,4,7,9], p = 2, q = 4", "2")],
        "constraints": ["2 <= number of nodes <= 10^5", "all values are distinct and the BST property holds", "p and q both exist in the tree"],
        "approach": "The BST order turns the problem into a decision at each step: if both targets are smaller, go left; if both are bigger, go "
                     "right; otherwise the current node is the split point and therefore the ancestor. No recursion or parent pointers needed.",
        "complexity": ("O(h)", "O(1)"),
        "code": {
            "cpp": r"""// Follow the search path until the two targets split
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    while (root) {
        if (p->val < root->val && q->val < root->val) root = root->left;
        else if (p->val > root->val && q->val > root->val) root = root->right;
        else return root;                        // the split point
    }
    return nullptr;
}   // O(h) time · O(1) space""",
            "java": r"""// Follow the search path until the two targets split
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    while (root != null) {
        if (p.val < root.val && q.val < root.val) root = root.left;
        else if (p.val > root.val && q.val > root.val) root = root.right;
        else return root;                        // the split point
    }
    return null;
}   // O(h) time · O(1) space""",
            "python": r"""def lowest_common_ancestor_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root              # the split point
    return None""",
        },
    },
    {
        "slug": "validate-binary-search-tree",
        "title": "Validate a Binary Search Tree",
        "difficulty": "Medium",
        "pattern": "top-down bounds",
        "statement": "Return true if the tree is a valid BST: every node is greater than all values in its left subtree and smaller than all values in "
                     "its right subtree.",
        "examples": [("root = [2,1,3]", "true"), ("root = [5,1,4,null,null,3,6]", "false")],
        "constraints": ["1 <= number of nodes <= 10^4", "-2^31 <= node values <= 2^31 - 1", "comparing only with the immediate children is wrong"],
        "approach": "Pass an open interval (lo, hi) down the recursion and tighten it as you descend. Local comparisons are not enough — a node deep "
                     "on the right can still be smaller than an ancestor — and using long bounds avoids trouble at the extremes of the value range.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// Tighten an interval as you descend; local checks are not enough
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
bool valid(TreeNode* node, long lo, long hi) {
    if (!node) return true;
    if (node->val <= lo || node->val >= hi) return false;
    return valid(node->left, lo, node->val) && valid(node->right, node->val, hi);
}
bool isValidBST(TreeNode* root) { return valid(root, LONG_MIN, LONG_MAX); }
// O(n) time · O(h) stack space""",
            "java": r"""// Tighten an interval as you descend; local checks are not enough
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
boolean valid(TreeNode node, long lo, long hi) {
    if (node == null) return true;
    if (node.val <= lo || node.val >= hi) return false;
    return valid(node.left, lo, node.val) && valid(node.right, node.val, hi);
}
boolean isValidBST(TreeNode root) { return valid(root, Long.MIN_VALUE, Long.MAX_VALUE); }
// O(n) time · O(h) stack space""",
            "python": r"""def is_valid_bst(root):
    def valid(node, lo, hi):        # the open interval this node must fall in
        if not node:
            return True
        if not lo < node.val < hi:
            return False
        return valid(node.left, lo, node.val) and valid(node.right, node.val, hi)

    return valid(root, float('-inf'), float('inf'))""",
        },
    },
    {
        "slug": "kth-smallest-element-in-a-bst",
        "title": "K-th Smallest Element in a BST",
        "difficulty": "Medium",
        "pattern": "in-order traversal",
        "statement": "Return the k-th smallest value in a BST (1-indexed).",
        "examples": [("root = [3,1,4,null,2], k = 1", "1"), ("root = [5,3,6,2,4,null,null,1], k = 3", "3")],
        "constraints": ["1 <= k <= number of nodes <= 10^4", "0 <= node values <= 10^4", "an O(h + k) solution is expected"],
        "approach": "An in-order traversal of a BST visits values in sorted order, so counting up to k while walking in-order gives the answer. "
                     "Stopping the recursion as soon as the counter hits k is the difference between O(h + k) and a full O(n) walk.",
        "complexity": ("O(h + k)", "O(h)"),
        "code": {
            "cpp": r"""// In-order visits values in sorted order; stop at the k-th
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
int count_ = 0, answer = 0;
void walk(TreeNode* node, int k) {
    if (!node || count_ >= k) return;
    walk(node->left, k);
    if (++count_ == k) { answer = node->val; return; }   // stop early
    walk(node->right, k);
}
int kthSmallest(TreeNode* root, int k) { count_ = 0; walk(root, k); return answer; }
// O(h + k) time · O(h) stack space""",
            "java": r"""// In-order visits values in sorted order; stop at the k-th
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
private int count_ = 0, answer = 0;
void walk(TreeNode node, int k) {
    if (node == null || count_ >= k) return;
    walk(node.left, k);
    if (++count_ == k) { answer = node.val; return; }    // stop early
    walk(node.right, k);
}
int kthSmallest(TreeNode root, int k) { count_ = 0; walk(root, k); return answer; }
// O(h + k) time · O(h) stack space""",
            "python": r"""def kth_smallest(root, k):
    order = []
    def walk(node):
        if not node or len(order) >= k:
            return
        walk(node.left)
        order.append(node.val)      # in-order: values arrive sorted
        walk(node.right)

    walk(root)
    return order[k - 1]""",
        },
    },
    {
        "slug": "binary-tree-right-side-view",
        "title": "Binary Tree Right Side View",
        "difficulty": "Medium",
        "pattern": "level order, last of each level",
        "statement": "Standing to the right of the tree, return the values of the nodes you can see, ordered from top to bottom.",
        "examples": [("root = [1,2,3,null,5,null,4]", "[1,3,4]"), ("root = [1,null,3]", "[1,3]")],
        "constraints": ["0 <= number of nodes <= 100", "-100 <= node values <= 100", "one value per level is reported"],
        "approach": "Do a normal level-order traversal and keep the last node of each level. Pushing the left child before the right is what makes "
                     "the final node of a level the rightmost one.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Level order; the last node of each level is the visible one
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
vector<int> rightSideView(TreeNode* root) {
    vector<int> out;
    if (!root) return out;
    queue<TreeNode*> q; q.push(root);
    while (!q.empty()) {
        int size = q.size();
        for (int i = 0; i < size; i++) {
            TreeNode* n = q.front(); q.pop();
            if (i == size - 1) out.push_back(n->val);    // rightmost of the level
            if (n->left) q.push(n->left);                // left before right
            if (n->right) q.push(n->right);
        }
    }
    return out;
}   // O(n) time · O(n) space""",
            "java": r"""// Level order; the last node of each level is the visible one
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
List<Integer> rightSideView(TreeNode root) {
    List<Integer> out = new ArrayList<>();
    if (root == null) return out;
    Deque<TreeNode> q = new ArrayDeque<>();
    q.add(root);
    while (!q.isEmpty()) {
        int size = q.size();
        for (int i = 0; i < size; i++) {
            TreeNode n = q.poll();
            if (i == size - 1) out.add(n.val);       // rightmost of the level
            if (n.left != null) q.add(n.left);       // left before right
            if (n.right != null) q.add(n.right);
        }
    }
    return out;
}   // O(n) time · O(n) space""",
            "python": r"""from collections import deque

def right_side_view(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        size = len(q)
        for i in range(size):
            node = q.popleft()
            if i == size - 1:
                out.append(node.val)   # rightmost of this level
            if node.left:
                q.append(node.left)    # left before right
            if node.right:
                q.append(node.right)
    return out""",
        },
    },
    {
        "slug": "zigzag-level-order-traversal",
        "title": "Zigzag Level Order Traversal",
        "difficulty": "Medium",
        "pattern": "level order with a direction flag",
        "statement": "Return the level order traversal but alternate the direction of every level: left to right, then right to left, and so on.",
        "examples": [("root = [3,9,20,null,null,15,7]", "[[3],[20,9],[15,7]]"), ("root = []", "[]")],
        "constraints": ["0 <= number of nodes <= 2000", "-100 <= node values <= 100", "the shape of the output is a list of lists"],
        "approach": "Keep the ordinary level-order traversal and reverse every other level before appending it — reversing a collected level is "
                     "clearer and no slower than juggling the queue. Toggling a boolean at the end of each level does the bookkeeping.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Collect each level, then reverse it on alternate levels
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
vector<vector<int>> zigzagLevelOrder(TreeNode* root) {
    vector<vector<int>> out;
    if (!root) return out;
    queue<TreeNode*> q; q.push(root);
    bool leftToRight = true;
    while (!q.empty()) {
        int size = q.size();
        vector<int> level(size);
        for (int i = 0; i < size; i++) {
            TreeNode* n = q.front(); q.pop();
            int idx = leftToRight ? i : size - 1 - i;    // place it directly
            level[idx] = n->val;
            if (n->left) q.push(n->left);
            if (n->right) q.push(n->right);
        }
        out.push_back(move(level));
        leftToRight = !leftToRight;
    }
    return out;
}   // O(n) time · O(n) space""",
            "java": r"""// Collect each level, then reverse it on alternate levels
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
List<List<Integer>> zigzagLevelOrder(TreeNode root) {
    List<List<Integer>> out = new ArrayList<>();
    if (root == null) return out;
    Deque<TreeNode> q = new ArrayDeque<>();
    q.add(root);
    boolean leftToRight = true;
    while (!q.isEmpty()) {
        int size = q.size();
        List<Integer> level = new ArrayList<>(Collections.nCopies(size, 0));
        for (int i = 0; i < size; i++) {
            TreeNode n = q.poll();
            int idx = leftToRight ? i : size - 1 - i;    // place it directly
            level.set(idx, n.val);
            if (n.left != null) q.add(n.left);
            if (n.right != null) q.add(n.right);
        }
        out.add(level);
        leftToRight = !leftToRight;
    }
    return out;
}   // O(n) time · O(n) space""",
            "python": r"""from collections import deque

def zigzag_level_order(root):
    if not root:
        return []
    out, q, left_to_right = [], deque([root]), True
    while q:
        size = len(q)
        level = [0] * size
        for i in range(size):
            node = q.popleft()
            level[i if left_to_right else size - 1 - i] = node.val   # place directly
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        out.append(level)
        left_to_right = not left_to_right
    return out""",
        },
    },
    {
        "slug": "construct-binary-tree-from-preorder-and-inorder",
        "title": "Construct a Tree From Preorder and Inorder",
        "difficulty": "Medium",
        "pattern": "index split with a hash map",
        "statement": "Rebuild the binary tree from its preorder and inorder traversals. All values are unique.",
        "examples": [("preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]", "the original tree"),
                     ("preorder = [-1], inorder = [-1]", "a single node")],
        "constraints": ["1 <= number of nodes <= 3000", "values are unique", "both traversals describe the same tree"],
        "approach": "Preorder hands you the root first; inorder tells you how many nodes go left and how many go right. A hash map from value to "
                     "its inorder index makes that split O(1), which is what keeps the whole build linear instead of quadratic.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Preorder gives the root, inorder gives the split
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
unordered_map<int, int> pos;
TreeNode* build(vector<int>& pre, int preLo, int inLo, int size) {
    if (size <= 0) return nullptr;
    int rootVal = pre[preLo];
    int leftSize = pos[rootVal] - inLo;          // nodes in the left subtree
    TreeNode* node = new TreeNode(rootVal);
    node->left  = build(pre, preLo + 1, inLo, leftSize);
    node->right = build(pre, preLo + 1 + leftSize, inLo + leftSize + 1, size - 1 - leftSize);
    return node;
}
TreeNode* buildTree(vector<int>& pre, vector<int>& in) {
    pos.clear();
    for (int i = 0; i < (int)in.size(); i++) pos[in[i]] = i;
    return build(pre, 0, 0, pre.size());
}   // O(n) time · O(n) space""",
            "java": r"""// Preorder gives the root, inorder gives the split
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
private final Map<Integer, Integer> pos = new HashMap<>();
TreeNode build(int[] pre, int preLo, int inLo, int size) {
    if (size <= 0) return null;
    int rootVal = pre[preLo];
    int leftSize = pos.get(rootVal) - inLo;      // nodes in the left subtree
    TreeNode node = new TreeNode(rootVal);
    node.left  = build(pre, preLo + 1, inLo, leftSize);
    node.right = build(pre, preLo + 1 + leftSize, inLo + leftSize + 1, size - 1 - leftSize);
    return node;
}
TreeNode buildTree(int[] pre, int[] in) {
    pos.clear();
    for (int i = 0; i < in.length; i++) pos.put(in[i], i);
    return build(pre, 0, 0, pre.length);
}   // O(n) time · O(n) space""",
            "python": r"""def build_tree_pre_in(preorder, inorder):
    pos = {v: i for i, v in enumerate(inorder)}     # value -> inorder index

    def build(pre_lo, in_lo, size):
        if size <= 0:
            return None
        root_val = preorder[pre_lo]
        left_size = pos[root_val] - in_lo           # nodes in the left subtree
        node = TreeNode(root_val)
        node.left = build(pre_lo + 1, in_lo, left_size)
        node.right = build(pre_lo + 1 + left_size, in_lo + left_size + 1, size - 1 - left_size)
        return node

    return build(0, 0, len(preorder))""",
        },
    },
    {
        "slug": "sum-root-to-leaf-numbers",
        "title": "Sum Root-to-Leaf Numbers",
        "difficulty": "Medium",
        "pattern": "top-down accumulation",
        "statement": "Each root-to-leaf path spells a number (digits along the path). Return the sum of all those numbers.",
        "examples": [("root = [1,2,3]", "25  (12 + 13)"), ("root = [4,9,0,5,1]", "1026  (495 + 491 + 40)")],
        "constraints": ["1 <= number of nodes <= 1000", "0 <= node values <= 9", "the answer fits in a 32-bit integer"],
        "approach": "Carry the number built so far downward: entering a node multiplies it by ten and adds the node's digit, and at a leaf the "
                     "accumulated number is added to the total. This is the top-down mirror image of the path-sum style.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// Carry the number down: value * 10 + digit, add it at each leaf
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
int walk(TreeNode* node, int acc) {
    if (!node) return 0;
    acc = acc * 10 + node->val;                  // extend the number
    if (!node->left && !node->right) return acc; // a complete leaf number
    return walk(node->left, acc) + walk(node->right, acc);
}
int sumNumbers(TreeNode* root) { return walk(root, 0); }
// O(n) time · O(h) stack space""",
            "java": r"""// Carry the number down: value * 10 + digit, add it at each leaf
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
int walk(TreeNode node, int acc) {
    if (node == null) return 0;
    acc = acc * 10 + node.val;                   // extend the number
    if (node.left == null && node.right == null) return acc;   // complete number
    return walk(node.left, acc) + walk(node.right, acc);
}
int sumNumbers(TreeNode root) { return walk(root, 0); }
// O(n) time · O(h) stack space""",
            "python": r"""def sum_numbers(root):
    def walk(node, acc):
        if not node:
            return 0
        acc = acc * 10 + node.val      # extend the number
        if not node.left and not node.right:
            return acc                 # a complete leaf number
        return walk(node.left, acc) + walk(node.right, acc)

    return walk(root, 0)""",
        },
    },
    {
        "slug": "delete-node-in-a-bst",
        "title": "Delete a Node in a BST",
        "difficulty": "Medium",
        "pattern": "search, then restructure",
        "statement": "Delete the node with the given key from a BST (if it exists) and return the root, keeping the BST property.",
        "examples": [("root = [5,3,6,2,4,null,7], key = 3", "[5,4,6,2,null,null,7]"),
                     ("root = [5,3,6,2,4,null,7], key = 0", "the tree unchanged")],
        "constraints": ["1 <= number of nodes <= 10^4", "-10^5 <= values, key <= 10^5", "values are unique"],
        "approach": "Search down the BST. When the target is found, there are three cases: no children (return null), one child (return it), two "
                     "children (replace the value with the in-order successor and then delete that successor from the right subtree). Only the "
                     "two-child case needs thought, and using the successor keeps all values to its right larger.",
        "complexity": ("O(h)", "O(h)"),
        "code": {
            "cpp": r"""// Three cases; the two-child case pulls up the in-order successor
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
TreeNode* deleteNode(TreeNode* root, int key) {
    if (!root) return nullptr;
    if (key < root->val) root->left = deleteNode(root->left, key);
    else if (key > root->val) root->right = deleteNode(root->right, key);
    else {
        if (!root->left) return root->right;     // 0 or 1 child
        if (!root->right) return root->left;
        TreeNode* succ = root->right;            // smallest in the right subtree
        while (succ->left) succ = succ->left;
        root->val = succ->val;
        root->right = deleteNode(root->right, succ->val);   // delete the successor
    }
    return root;
}   // O(h) time · O(h) stack space""",
            "java": r"""// Three cases; the two-child case pulls up the in-order successor
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
TreeNode deleteNode(TreeNode root, int key) {
    if (root == null) return null;
    if (key < root.val) root.left = deleteNode(root.left, key);
    else if (key > root.val) root.right = deleteNode(root.right, key);
    else {
        if (root.left == null) return root.right;    // 0 or 1 child
        if (root.right == null) return root.left;
        TreeNode succ = root.right;                  // smallest on the right
        while (succ.left != null) succ = succ.left;
        root.val = succ.val;
        root.right = deleteNode(root.right, succ.val);   // delete the successor
    }
    return root;
}   // O(h) time · O(h) stack space""",
            "python": r"""def delete_node(root, key):
    if not root:
        return None
    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        if not root.left:
            return root.right        # zero or one child
        if not root.right:
            return root.left
        succ = root.right            # smallest value on the right
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = delete_node(root.right, succ.val)   # remove that successor
    return root""",
        },
    },
    {
        "slug": "binary-tree-pruning",
        "title": "Binary Tree Pruning",
        "difficulty": "Medium",
        "pattern": "post-order filtering",
        "statement": "Remove every subtree that contains no 1, and return the root of the pruned tree.",
        "examples": [("root = [1,null,0,0,1]", "[1,null,0,null,1]"), ("root = [1,0,1,0,0,0,1]", "[1,null,1,null,1]")],
        "constraints": ["1 <= number of nodes <= 200", "node values are 0 or 1", "a leaf with value 0 must be removed"],
        "approach": "Prune the children first, then decide about the current node: if both children are gone and this value is 0, return null. "
                     "Post-order is essential here, because you cannot know whether a node should survive until its subtrees are settled.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// Prune the children first, then drop this node if it is a 0 leaf
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
TreeNode* pruneTree(TreeNode* node) {
    if (!node) return nullptr;
    node->left = pruneTree(node->left);          // settle the subtrees first
    node->right = pruneTree(node->right);
    if (node->val == 0 && !node->left && !node->right) return nullptr;   // 0 leaf
    return node;
}   // O(n) time · O(h) stack space""",
            "java": r"""// Prune the children first, then drop this node if it is a 0 leaf
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
TreeNode pruneTree(TreeNode node) {
    if (node == null) return null;
    node.left = pruneTree(node.left);            // settle the subtrees first
    node.right = pruneTree(node.right);
    if (node.val == 0 && node.left == null && node.right == null) return null;
    return node;
}   // O(n) time · O(h) stack space""",
            "python": r"""def prune_tree(node):
    if not node:
        return None
    node.left = prune_tree(node.left)     # settle the subtrees first
    node.right = prune_tree(node.right)
    if node.val == 0 and not node.left and not node.right:
        return None                       # a 0 leaf disappears
    return node""",
        },
    },
    {
        "slug": "count-good-nodes-in-binary-tree",
        "title": "Count Good Nodes",
        "difficulty": "Medium",
        "pattern": "top-down maximum",
        "statement": "A node is good if no node on the path from the root to it has a larger value. Return how many good nodes the tree has.",
        "examples": [("root = [3,1,4,3,null,1,5]", "4"), ("root = [3,3,null,4,2]", "3")],
        "constraints": ["1 <= number of nodes <= 10^5", "-10^4 <= node values <= 10^4", "the root is always good"],
        "approach": "Pass the largest value seen so far downward and count a node when its value is at least that maximum. The comparison must be "
                     "greater-or-equal, so ties along a path all count.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// Carry the path maximum down; a node counts when it is >= that maximum
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
int count(TreeNode* node, int best) {
    if (!node) return 0;
    int good = node->val >= best ? 1 : 0;        // ties also count as good
    int next = max(best, node->val);
    return good + count(node->left, next) + count(node->right, next);
}
int goodNodes(TreeNode* root) { return count(root, INT_MIN); }
// O(n) time · O(h) stack space""",
            "java": r"""// Carry the path maximum down; a node counts when it is >= that maximum
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
int count(TreeNode node, int best) {
    if (node == null) return 0;
    int good = node.val >= best ? 1 : 0;         // ties also count as good
    int next = Math.max(best, node.val);
    return good + count(node.left, next) + count(node.right, next);
}
int goodNodes(TreeNode root) { return count(root, Integer.MIN_VALUE); }
// O(n) time · O(h) stack space""",
            "python": r"""def good_nodes(root):
    def count(node, best):
        if not node:
            return 0
        good = 1 if node.val >= best else 0      # ties count as good
        best = max(best, node.val)
        return good + count(node.left, best) + count(node.right, best)

    return count(root, float('-inf'))""",
        },
    },
    # ------------------------------------------------------------------ HARD
    {
        "slug": "binary-tree-maximum-path-sum",
        "title": "Maximum Path Sum",
        "difficulty": "Hard",
        "pattern": "bottom-up gain with a global best",
        "statement": "A path is any sequence of nodes connected by edges, each used once. Return the largest sum any path can have; negative nodes may be skipped, but a path must contain at least one node.",
        "examples": [("root = [1,2,3]", "6"), ("root = [-10,9,20,null,null,15,7]", "42")],
        "constraints": ["1 <= number of nodes <= 3 * 10^4", "-1000 <= node values <= 1000", "paths may start and end anywhere"],
        "approach": "Each node contributes to its parent at most one side — the better of its two branches, floored at zero so a negative branch is dropped. Separately, the best path *through* the node uses both sides, and that is what updates the global answer.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// Report at most one side upward; record the both-sides path locally
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
int best_;
int gain(TreeNode* node) {
    if (!node) return 0;
    int l = max(0, gain(node->left));            // drop negative branches
    int r = max(0, gain(node->right));
    best_ = max(best_, node->val + l + r);       // path through this node
    return node->val + max(l, r);                // one side to the parent
}
int maxPathSum(TreeNode* root) { best_ = INT_MIN; gain(root); return best_; }
// O(n) time · O(h) stack space""",
            "java": r"""// Report at most one side upward; record the both-sides path locally
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
private int best_;
int gain(TreeNode node) {
    if (node == null) return 0;
    int l = Math.max(0, gain(node.left));        // drop negative branches
    int r = Math.max(0, gain(node.right));
    best_ = Math.max(best_, node.val + l + r);   // path through this node
    return node.val + Math.max(l, r);            // one side to the parent
}
int maxPathSum(TreeNode root) { best_ = Integer.MIN_VALUE; gain(root); return best_; }
// O(n) time · O(h) stack space""",
            "python": r"""def max_path_sum(root):
    best = float('-inf')
    def gain(node):
        nonlocal best
        if not node:
            return 0
        l = max(0, gain(node.left))     # drop negative branches
        r = max(0, gain(node.right))
        best = max(best, node.val + l + r)   # path through this node
        return node.val + max(l, r)          # only one side goes up

    gain(root)
    return best""",
        },
    },
    {
        "slug": "serialize-and-deserialize-binary-tree",
        "title": "Serialize and Deserialize a Binary Tree",
        "difficulty": "Hard",
        "pattern": "preorder with explicit nulls",
        "statement": "Design serialize(root) producing a string and deserialize(data) rebuilding the identical tree.",
        "examples": [("root = [1,2,3,null,null,4,5]", "round-trips to the same tree"),
                     ("root = []", "round-trips to an empty tree")],
        "constraints": ["0 <= number of nodes <= 10^4", "-1000 <= node values <= 1000", "the format is yours to choose"],
        "approach": "Emit a preorder walk in which null children are written explicitly as a marker. That marker is what makes the payload self-describing: rebuilding can then allocate children in order without any length or level bookkeeping, which is why the round trip is exactly one pass each way.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Preorder with explicit nulls: the stream rebuilds itself
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
class Codec {
    void enc(TreeNode* node, string& out) {
        if (!node) { out += "#,"; return; }      // explicit null marker
        out += to_string(node->val) + ",";
        enc(node->left, out);
        enc(node->right, out);
    }
    TreeNode* dec(stringstream& ss) {
        string tok; getline(ss, tok, ',');
        if (tok == "#" || tok.empty()) return nullptr;
        TreeNode* node = new TreeNode(stoi(tok));
        node->left = dec(ss);                    // next token is the left subtree
        node->right = dec(ss);
        return node;
    }
public:
    string serialize(TreeNode* root) { string out; enc(root, out); return out; }
    TreeNode* deserialize(string data) { stringstream ss(data); return dec(ss); }
};   // O(n) time · O(n) space""",
            "java": r"""// Preorder with explicit nulls: the stream rebuilds itself
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
class Codec {
    private void enc(TreeNode node, StringBuilder out) {
        if (node == null) { out.append("#,"); return; }     // explicit null marker
        out.append(node.val).append(',');
        enc(node.left, out);
        enc(node.right, out);
    }
    private int idx;
    private TreeNode dec(String[] tokens) {
        String tok = tokens[idx++];
        if (tok.equals("#")) return null;
        TreeNode node = new TreeNode(Integer.parseInt(tok));
        node.left = dec(tokens);                 // next token is the left subtree
        node.right = dec(tokens);
        return node;
    }
    public String serialize(TreeNode root) {
        StringBuilder out = new StringBuilder();
        enc(root, out);
        return out.toString();
    }
    public TreeNode deserialize(String data) {
        idx = 0;
        return dec(data.split(","));
    }
}   // O(n) time · O(n) space""",
            "python": r"""def serialize(root):
    parts = []
    def enc(node):
        if not node:
            parts.append('#')          # explicit null marker
            return
        parts.append(str(node.val))
        enc(node.left)
        enc(node.right)

    enc(root)
    return ','.join(parts)

def deserialize(data):
    tokens = iter(data.split(','))
    def dec():
        tok = next(tokens)
        if tok == '#':
            return None
        node = TreeNode(int(tok))
        node.left = dec()              # the next token starts the left subtree
        node.right = dec()
        return node

    return dec()""",
        },
    },
    {
        "slug": "recover-binary-search-tree",
        "title": "Recover a Swapped BST",
        "difficulty": "Hard",
        "pattern": "in-order with two violations",
        "statement": "Exactly two nodes of a BST were swapped by mistake. Restore the tree without changing its structure.",
        "examples": [("root = [1,3,null,null,2]", "[3,1,null,null,2]"), ("root = [3,1,4,null,null,2]", "[2,1,4,null,null,3]")],
        "constraints": ["2 <= number of nodes <= 1000", "-2^31 <= node values <= 2^31 - 1", "the fix must swap the values, not relink nodes"],
        "approach": "An in-order walk of a correct BST is increasing, so a swap shows up as one or two descents. Record the previous node only on the first descent and the current node on every descent — for adjacent swaps there is only one descent, and handling that case is where most solutions break.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// In-order: record the first descent's 'prev' and the last descent's 'cur'
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
class Solver {
public:
    TreeNode *prev = nullptr, *first = nullptr, *second = nullptr;
    void walk(TreeNode* node) {                  // Morris would give O(1) space
        if (!node) return;
        walk(node->left);
        if (prev && prev->val > node->val) {
            if (!first) first = prev;            // first descent: keep prev
            second = node;                       // latest descent: keep cur
        }
        prev = node;
        walk(node->right);
    }
    void recoverTree(TreeNode* root) {
        walk(root);
        if (first && second) swap(first->val, second->val);   // values, not links
    }
};   // O(n) time · O(h) stack space""",
            "java": r"""// In-order: record the first descent's 'prev' and the last descent's 'cur'
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
class Solver {
    TreeNode prev, first, second;
    void walk(TreeNode node) {
        if (node == null) return;
        walk(node.left);
        if (prev != null && prev.val > node.val) {
            if (first == null) first = prev;     // first descent: keep prev
            second = node;                       // latest descent: keep cur
        }
        prev = node;
        walk(node.right);
    }
    void recoverTree(TreeNode root) {
        prev = first = second = null;
        walk(root);
        if (first != null && second != null) {   // swap the values, not the links
            int t = first.val; first.val = second.val; second.val = t;
        }
    }
}   // O(n) time · O(h) stack space""",
            "python": r"""def recover_tree(root):
    prev = first = second = None
    def walk(node):
        nonlocal prev, first, second
        if not node:
            return
        walk(node.left)
        if prev and prev.val > node.val:
            if not first:
                first = prev            # first descent: remember prev
            second = node               # latest descent: remember cur
        prev = node
        walk(node.right)

    walk(root)
    first.val, second.val = second.val, first.val   # swap values, not links""",
        },
    },
    {
        "slug": "binary-tree-cameras",
        "title": "Binary Tree Cameras",
        "difficulty": "Hard",
        "pattern": "three-state greedy DP",
        "statement": "A camera on a node covers that node, its parent and its children. Return the minimum number of cameras needed to cover every node.",
        "examples": [("root = [0,0,null,0,0]", "1"), ("root = [0,0,null,0,null,0,null,null,0]", "2")],
        "constraints": ["1 <= number of nodes <= 1000", "each node value is 0", "cameras may be placed on any node"],
        "approach": "Each subtree reports one of three states: it still needs coverage, it is covered by its children, or it has a camera. Placing a camera only when a child reports 'needs coverage' is the greedy choice that makes the count optimal, and the root may need a final camera if it is still uncovered.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// States: 0 = needs cover, 1 = covered, 2 = has a camera
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
int cameras;
int dfs(TreeNode* node) {
    if (!node) return 1;                         // a missing child counts as covered
    int l = dfs(node->left), r = dfs(node->right);
    if (l == 0 || r == 0) { cameras++; return 2; }   // a child demands a camera here
    if (l == 2 || r == 2) return 1;                  // a camera below covers this
    return 0;                                        // needs its parent's camera
}
int minCameraCover(TreeNode* root) {
    cameras = 0;
    return dfs(root) == 0 ? cameras + 1 : cameras;   // the root may still need one
}   // O(n) time · O(h) stack space""",
            "java": r"""// States: 0 = needs cover, 1 = covered, 2 = has a camera
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
private int cameras;
int dfs(TreeNode node) {
    if (node == null) return 1;                  // a missing child counts as covered
    int l = dfs(node.left), r = dfs(node.right);
    if (l == 0 || r == 0) { cameras++; return 2; }    // a child demands a camera here
    if (l == 2 || r == 2) return 1;                   // covered from below
    return 0;                                         // needs its parent's camera
}
int minCameraCover(TreeNode root) {
    cameras = 0;
    return dfs(root) == 0 ? cameras + 1 : cameras;    // the root may need one too
}   // O(n) time · O(h) stack space""",
            "python": r"""def min_camera_cover(root):
    cameras = 0
    def dfs(node):
        nonlocal cameras
        if not node:
            return 1                  # a missing child counts as covered
        l, r = dfs(node.left), dfs(node.right)
        if l == 0 or r == 0:
            cameras += 1              # a child demands a camera here
            return 2
        if l == 2 or r == 2:
            return 1                  # covered from below
        return 0                      # needs its parent's camera

    return cameras + 1 if dfs(root) == 0 else cameras""",
        },
    },
    {
        "slug": "vertical-order-traversal-of-a-binary-tree",
        "title": "Vertical Order Traversal",
        "difficulty": "Hard",
        "pattern": "coordinate sorting",
        "statement": "Report node values column by column from left to right; inside one column, order by row, and for equal row and column, by value.",
        "examples": [("root = [3,9,20,null,null,15,7]", "[[9],[3,15],[20],[7]]"),
                     ("root = [1,2,3,4,5,6,7]", "[[4],[2],[1,5,6],[3],[7]]")],
        "constraints": ["1 <= number of nodes <= 1000", "0 <= node values <= 1000", "the value tie-break inside a cell is part of the answer"],
        "approach": "Give every node a coordinate (column, row, value) during a traversal, then sort that list once. The sorting does all the work: columns first, then rows, then values, so the tie-break rule needs no special code.",
        "complexity": ("O(n log n)", "O(n)"),
        "code": {
            "cpp": r"""// Collect (col, row, val), sort once, then group by column
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
vector<vector<int>> verticalTraversal(TreeNode* root) {
    vector<array<int, 3>> nodes;                 // {col, row, val}
    queue<pair<TreeNode*, pair<int,int>>> q;     // node, {col, row}
    q.push({root, {0, 0}});
    while (!q.empty()) {
        auto [node, cr] = q.front(); q.pop();
        auto [col, row] = cr;
        nodes.push_back({col, row, node->val});
        if (node->left) q.push({node->left, {col - 1, row + 1}});
        if (node->right) q.push({node->right, {col + 1, row + 1}});
    }
    sort(nodes.begin(), nodes.end());             // col, then row, then value
    vector<vector<int>> out;
    int lastCol = INT_MIN;
    for (auto& n : nodes) {
        if (n[0] != lastCol) { out.push_back({}); lastCol = n[0]; }
        out.back().push_back(n[2]);
    }
    return out;
}   // O(n log n) time · O(n) space""",
            "java": r"""// Collect (col, row, val), sort once, then group by column
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
List<List<Integer>> verticalTraversal(TreeNode root) {
    List<int[]> nodes = new ArrayList<>();       // {col, row, val}
    Deque<Object[]> q = new ArrayDeque<>();      // {node, col, row}
    q.add(new Object[]{root, 0, 0});
    while (!q.isEmpty()) {
        Object[] cur = q.poll();
        TreeNode node = (TreeNode) cur[0];
        int col = (Integer) cur[1], row = (Integer) cur[2];
        nodes.add(new int[]{col, row, node.val});
        if (node.left != null) q.add(new Object[]{node.left, col - 1, row + 1});
        if (node.right != null) q.add(new Object[]{node.right, col + 1, row + 1});
    }
    nodes.sort((a, b) -> a[0] != b[0] ? a[0] - b[0]
                       : a[1] != b[1] ? a[1] - b[1] : a[2] - b[2]);
    List<List<Integer>> out = new ArrayList<>();
    int lastCol = Integer.MIN_VALUE;
    for (int[] n : nodes) {
        if (n[0] != lastCol) { out.add(new ArrayList<>()); lastCol = n[0]; }
        out.get(out.size() - 1).add(n[2]);
    }
    return out;
}   // O(n log n) time · O(n) space""",
            "python": r"""from collections import deque

def vertical_traversal(root):
    nodes = []                       # (col, row, val)
    q = deque([(root, 0, 0)])
    while q:
        node, col, row = q.popleft()
        nodes.append((col, row, node.val))
        if node.left:
            q.append((node.left, col - 1, row + 1))
        if node.right:
            q.append((node.right, col + 1, row + 1))
    nodes.sort()                     # column, then row, then value
    out, last_col = [], None
    for col, row, val in nodes:
        if col != last_col:
            out.append([])
            last_col = col
        out[-1].append(val)
    return out""",
        },
    },
    {
        "slug": "path-sum-iii",
        "title": "Path Sum III",
        "difficulty": "Hard",
        "pattern": "prefix sums on a root path",
        "statement": "Count the paths that go downward (parent to child, not necessarily starting at the root or ending at a leaf) whose values sum to the target.",
        "examples": [("root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8", "3"), ("root = [5,4,8,11,null,4,4,7,2,null,null,5,1], targetSum = 22", "3")],
        "constraints": ["1 <= number of nodes <= 1000", "-10^9 <= values, targetSum <= 10^9", "the answer fits in a 32-bit integer"],
        "approach": "Every downward path is the difference of two root-path sums, so keep a map of how many times each running sum has appeared along the current root-to-node path. Insert the current sum in the map *before* recursing and remove it afterwards — that removal is what restricts the counts to genuine downward paths instead of arbitrary ones.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// Prefix sums along the current root path, subtracted from the target
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
unordered_map<long long, int> seen{{0, 1}};      // the empty prefix
int countPaths(TreeNode* node, long long run, int target) {
    if (!node) return 0;
    run += node->val;
    int found = seen.count(run - target) ? seen[run - target] : 0;   // earlier prefixes
    seen[run]++;                                  // add before recursing
    int total = found + countPaths(node->left, run, target)
                      + countPaths(node->right, run, target);
    seen[run]--;                                  // remove on the way back up
    if (seen[run] == 0) seen.erase(run);
    return total;
}
int pathSum(TreeNode* root, int target) {
    seen.clear(); seen[0] = 1;
    return countPaths(root, 0, target);
}   // O(n) time · O(h) space""",
            "java": r"""// Prefix sums along the current root path, subtracted from the target
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
private final Map<Long, Integer> seen = new HashMap<>();
int countPaths(TreeNode node, long run, int target) {
    if (node == null) return 0;
    run += node.val;
    int found = seen.getOrDefault(run - target, 0);      // earlier prefixes
    seen.merge(run, 1, Integer::sum);                    // add before recursing
    int total = found + countPaths(node.left, run, target)
                      + countPaths(node.right, run, target);
    seen.merge(run, -1, Integer::sum);                   // remove on the way up
    if (seen.get(run) == 0) seen.remove(run);
    return total;
}
int pathSum(TreeNode root, int target) {
    seen.clear(); seen.put(0L, 1);
    return countPaths(root, 0L, target);
}   // O(n) time · O(h) space""",
            "python": r"""def path_sum_iii(root, target):
    seen = {0: 1}                    # running sum -> how often it occurred
    def walk(node, run):
        if not node:
            return 0
        run += node.val
        found = seen.get(run - target, 0)   # paths ending here
        seen[run] = seen.get(run, 0) + 1    # add before recursing
        total = found + walk(node.left, run) + walk(node.right, run)
        seen[run] -= 1                      # remove on the way back up
        if seen[run] == 0:
            del seen[run]
        return total

    return walk(root, 0)""",
        },
    },
    {
        "slug": "house-robber-iii",
        "title": "House Robber III",
        "difficulty": "Hard",
        "pattern": "two-value subtree DP",
        "statement": "The houses form a binary tree and adjacent houses (parent and child) cannot both be robbed. Return the maximum amount.",
        "examples": [("root = [3,2,3,null,3,null,1]", "7"), ("root = [3,4,5,1,3,null,1]", "9")],
        "constraints": ["1 <= number of nodes <= 10^4", "0 <= node values <= 10^4", "parent and child may not both be taken"],
        "approach": "Return a pair from every subtree: the best when this node is robbed and the best when it is not. Robbing the node forces the children's 'not robbed' values; skipping it lets each child use its better option. Both numbers travel upward together, so no node is visited twice.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// Each subtree returns {rob this node, skip this node}
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
pair<int, int> dfs(TreeNode* node) {             // {rob, skip}
    if (!node) return {0, 0};
    auto [robL, skipL] = dfs(node->left);
    auto [robR, skipR] = dfs(node->right);
    int rob = node->val + skipL + skipR;         // children must be skipped
    int skip = max(robL, skipL) + max(robR, skipR);
    return {rob, skip};
}
int rob(TreeNode* root) {
    auto [rob, skip] = dfs(root);
    return max(rob, skip);
}   // O(n) time · O(h) stack space""",
            "java": r"""// Each subtree returns {rob this node, skip this node}
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
int[] dfs(TreeNode node) {                       // {rob, skip}
    if (node == null) return new int[]{0, 0};
    int[] l = dfs(node.left), r = dfs(node.right);
    int rob = node.val + l[1] + r[1];            // children must be skipped
    int skip = Math.max(l[0], l[1]) + Math.max(r[0], r[1]);
    return new int[]{rob, skip};
}
int rob(TreeNode root) {
    int[] r = dfs(root);
    return Math.max(r[0], r[1]);
}   // O(n) time · O(h) stack space""",
            "python": r"""def rob_tree(root):
    def dfs(node):                   # returns (rob this node, skip this node)
        if not node:
            return 0, 0
        rob_l, skip_l = dfs(node.left)
        rob_r, skip_r = dfs(node.right)
        rob = node.val + skip_l + skip_r         # children must be skipped
        skip = max(rob_l, skip_l) + max(rob_r, skip_r)
        return rob, skip

    return max(dfs(root))""",
        },
    },
    {
        "slug": "lowest-common-ancestor-of-a-binary-tree",
        "title": "Lowest Common Ancestor of a Binary Tree",
        "difficulty": "Hard",
        "pattern": "post-order signalling",
        "statement": "Given two nodes in an ordinary binary tree, return their lowest common ancestor.",
        "examples": [("root = [3,5,1,6,2,0,8], p = 5, q = 1", "3"), ("root = [3,5,1,6,2,0,8], p = 5, q = 4", "5")],
        "constraints": ["2 <= number of nodes <= 10^5", "values are unique", "p and q both exist and may be the same node"],
        "approach": "Recurse into both subtrees and let each call report whether it found p, q, or neither. The first node that receives a hit from both sides (or is a target itself with a hit from one side) is the answer — returned upward all the way, so no parent pointers are needed.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// A node receiving hits from both sides is the LCA
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
TreeNode* lowestCommonAncestor(TreeNode* node, TreeNode* p, TreeNode* q) {
    if (!node || node == p || node == q) return node;
    TreeNode* l = lowestCommonAncestor(node->left, p, q);
    TreeNode* r = lowestCommonAncestor(node->right, p, q);
    if (l && r) return node;                     // one target on each side
    return l ? l : r;                            // pass the hit upward
}   // O(n) time · O(h) stack space""",
            "java": r"""// A node receiving hits from both sides is the LCA
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
TreeNode lowestCommonAncestor(TreeNode node, TreeNode p, TreeNode q) {
    if (node == null || node == p || node == q) return node;
    TreeNode l = lowestCommonAncestor(node.left, p, q);
    TreeNode r = lowestCommonAncestor(node.right, p, q);
    if (l != null && r != null) return node;     // one target on each side
    return l != null ? l : r;                    // pass the hit upward
}   // O(n) time · O(h) stack space""",
            "python": r"""def lowest_common_ancestor_binary(root, p, q):
    if not root or root is p or root is q:
        return root
    l = lowest_common_ancestor_binary(root.left, p, q)
    r = lowest_common_ancestor_binary(root.right, p, q)
    if l and r:
        return root                  # one target on each side
    return l or r                    # carry the hit upward""",
        },
    },
    {
        "slug": "all-nodes-distance-k-in-binary-tree",
        "title": "All Nodes at Distance K",
        "difficulty": "Hard",
        "pattern": "parent map + BFS",
        "statement": "Given a target node in a binary tree, return the values of all nodes exactly k edges away.",
        "examples": [("root = [3,5,1,6,2,0,8,null,null,7,4], target = 5, k = 2", "[7,4,1]"), ("root = [1], target = 1, k = 3", "[]")],
        "constraints": ["1 <= number of nodes <= 500", "0 <= node values <= 500", "all values are unique"],
        "approach": "Distances in a tree run both down and *up*, and a plain traversal cannot go up. Add a parent pointer per node, then the tree becomes an undirected graph and a breadth-first search from the target finds the k-th layer.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Parent pointers make the tree undirected; BFS k layers out
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
unordered_map<TreeNode*, TreeNode*> parent;
void record(TreeNode* node, TreeNode* par) {
    if (!node) return;
    parent[node] = par;
    record(node->left, node);
    record(node->right, node);
}
vector<int> distanceK(TreeNode* root, TreeNode* target, int k) {
    parent.clear();
    record(root, nullptr);
    unordered_set<TreeNode*> seen{target};
    vector<TreeNode*> frontier{target};
    while (k-- > 0 && !frontier.empty()) {       // walk out one layer at a time
        vector<TreeNode*> next;
        for (TreeNode* node : frontier)
            for (TreeNode* nb : {node->left, node->right, parent[node]})
                if (nb && seen.insert(nb).second) next.push_back(nb);
        frontier = move(next);
    }
    vector<int> out;
    for (TreeNode* node : frontier) out.push_back(node->val);
    return out;
}   // O(n) time · O(n) space""",
            "java": r"""// Parent pointers make the tree undirected; BFS k layers out
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
private final Map<TreeNode, TreeNode> parent = new HashMap<>();
void record(TreeNode node, TreeNode par) {
    if (node == null) return;
    parent.put(node, par);
    record(node.left, node);
    record(node.right, node);
}
List<Integer> distanceK(TreeNode root, TreeNode target, int k) {
    parent.clear();
    record(root, null);
    Set<TreeNode> seen = new HashSet<>();
    seen.add(target);
    List<TreeNode> frontier = new ArrayList<>();
    frontier.add(target);
    while (k-- > 0 && !frontier.isEmpty()) {     // walk out one layer at a time
        List<TreeNode> next = new ArrayList<>();
        for (TreeNode node : frontier) {
            for (TreeNode nb : new TreeNode[]{node.left, node.right, parent.get(node)})
                if (nb != null && seen.add(nb)) next.add(nb);
        }
        frontier = next;
    }
    List<Integer> out = new ArrayList<>();
    for (TreeNode node : frontier) out.add(node.val);
    return out;
}   // O(n) time · O(n) space""",
            "python": r"""def distance_k(root, target, k):
    parent = {}
    def record(node, par):
        if not node:
            return
        parent[node] = par
        record(node.left, node)
        record(node.right, node)

    record(root, None)
    seen = {target}
    frontier = [target]
    while k > 0 and frontier:            # expand one layer at a time
        nxt = []
        for node in frontier:
            for nb in (node.left, node.right, parent[node]):
                if nb and nb not in seen:
                    seen.add(nb)
                    nxt.append(nb)
        frontier = nxt
        k -= 1
    return [node.val for node in frontier]""",
        },
    },
    {
        "slug": "maximum-sum-bst-in-binary-tree",
        "title": "Maximum Sum BST in a Binary Tree",
        "difficulty": "Hard",
        "pattern": "subtree summary (min, max, sum, valid)",
        "statement": "Return the largest sum of node values over all subtrees that are themselves valid BSTs; return 0 if none exists.",
        "examples": [("root = [1,4,3,2,4,2,5,null,null,null,null,null,null,4,6]", "20"),
                     ("root = [4,3,null,1,2]", "2")],
        "constraints": ["1 <= number of nodes <= 4 * 10^4", "-4 * 10^4 <= node values <= 4 * 10^4", "only complete subtrees count"],
        "approach": "Every subtree reports four things: its minimum, its maximum, its sum and whether it is a valid BST. A node is a valid BST exactly when both children are valid and its value sits strictly between the children's extremes — so one bottom-up pass answers everything.",
        "complexity": ("O(n)", "O(h)"),
        "code": {
            "cpp": r"""// Each subtree reports {min, max, sum, isBST}
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
int bestSum;
array<long long, 4> dfs(TreeNode* node) {        // {min, max, sum, valid}
    if (!node) return {LLONG_MAX, LLONG_MIN, 0, 1};
    auto l = dfs(node->left), r = dfs(node->right);
    bool ok = l[3] && r[3] && node->val > l[1] && node->val < r[0];
    if (ok) {
        long long sum = l[2] + r[2] + node->val;
        bestSum = max<long long>(bestSum, sum);
        return {min<long long>(l[0], node->val), max<long long>(r[1], node->val), sum, 1};
    }
    return {LLONG_MIN, LLONG_MAX, 0, 0};         // invalid; parents must not use it
}
int maxSumBST(TreeNode* root) {
    bestSum = 0;
    dfs(root);
    return bestSum;
}   // O(n) time · O(h) stack space""",
            "java": r"""// Each subtree reports {min, max, sum, isBST}
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
private int bestSum;
long[] dfs(TreeNode node) {                      // {min, max, sum, valid}
    if (node == null) return new long[]{Long.MAX_VALUE, Long.MIN_VALUE, 0, 1};
    long[] l = dfs(node.left), r = dfs(node.right);
    boolean ok = l[3] == 1 && r[3] == 1 && node.val > l[1] && node.val < r[0];
    if (ok) {
        long sum = l[2] + r[2] + node.val;
        bestSum = (int) Math.max(bestSum, sum);
        return new long[]{Math.min(l[0], node.val), Math.max(r[1], node.val), sum, 1};
    }
    return new long[]{Long.MIN_VALUE, Long.MAX_VALUE, 0, 0};   // invalid subtree
}
int maxSumBST(TreeNode root) {
    bestSum = 0;
    dfs(root);
    return bestSum;
}   // O(n) time · O(h) stack space""",
            "python": r"""def max_sum_bst(root):
    best = 0
    def dfs(node):                   # returns (min, max, sum, is_bst)
        nonlocal best
        if not node:
            return float('inf'), float('-inf'), 0, True
        lmin, lmax, lsum, lok = dfs(node.left)
        rmin, rmax, rsum, rok = dfs(node.right)
        if lok and rok and lmax < node.val < rmin:
            total = lsum + rsum + node.val
            best = max(best, total)
            return min(lmin, node.val), max(rmax, node.val), total, True
        return float('-inf'), float('inf'), 0, False   # invalid: parents ignore it

    dfs(root)
    return best""",
        },
    },
    {
        "slug": "bst-iterator",
        "title": "BST Iterator",
        "difficulty": "Hard",
        "pattern": "controlled in-order stack",
        "statement": "Design a class over a BST with next() returning the next smallest value and hasNext() reporting whether one exists, both in "
                     "O(1) amortised time and O(h) memory.",
        "examples": [("tree [7,3,15,null,null,9,20], next(), next(), hasNext()", "3, 7, true"),
                     ("continuing: next(), next()", "9, 15")],
        "constraints": ["1 <= number of nodes <= 10^5", "0 <= node values <= 10^6", "the amortised cost must be O(1) per call"],
        "approach": "Do the in-order walk lazily: push the whole left spine at the start, and after each `next()` push the left spine of the popped node's right child. The stack holds exactly the path to the next value, so memory is O(h) rather than O(n).",
        "complexity": ("O(1) amortised per call", "O(h)"),
        "code": {
            "cpp": r"""// Lazy in-order: the stack is the path to the next smallest value
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
class BSTIterator {
    vector<TreeNode*> st;
    void pushLeft(TreeNode* node) {              // the whole left spine
        for (; node; node = node->left) st.push_back(node);
    }
public:
    BSTIterator(TreeNode* root) { pushLeft(root); }
    int next() {
        TreeNode* node = st.back(); st.pop_back();
        pushLeft(node->right);                   // the next values may be to the right
        return node->val;
    }
    bool hasNext() { return !st.empty(); }
};   // O(1) amortised per call · O(h) space""",
            "java": r"""// Lazy in-order: the stack is the path to the next smallest value
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
class BSTIterator {
    private final Deque<TreeNode> st = new ArrayDeque<>();
    private void pushLeft(TreeNode node) {       // the whole left spine
        for (; node != null; node = node.left) st.push(node);
    }
    public BSTIterator(TreeNode root) { pushLeft(root); }
    public int next() {
        TreeNode node = st.pop();
        pushLeft(node.right);                    // next values may be to the right
        return node.val;
    }
    public boolean hasNext() { return !st.isEmpty(); }
}   // O(1) amortised per call · O(h) space""",
            "python": r"""class BSTIterator:
    def __init__(self, root):
        self.st = []
        self._push_left(root)         # the whole left spine

    def _push_left(self, node):
        while node:
            self.st.append(node)
            node = node.left

    def next(self):
        node = self.st.pop()
        self._push_left(node.right)   # the next values may be to the right
        return node.val

    def has_next(self):
        return bool(self.st)""",
        },
    },
    {
        "slug": "closest-binary-search-tree-value-ii",
        "title": "Closest BST Values",
        "difficulty": "Hard",
        "pattern": "in-order with a capped buffer",
        "statement": "Given a BST and a target, return the k values closest to the target, sorted ascending.",
        "examples": [("root = [4,2,5,1,3], target = 3.714286, k = 2", "[4,3]"), ("root = [1], target = 0.5, k = 1", "[1]")],
        "constraints": ["1 <= k <= number of nodes <= 10^4", "0 <= node values <= 10^9", "the output must be sorted ascending"],
        "approach": "An in-order walk produces values in ascending order, so a fixed-size queue that is kept as close as possible to the target collapses the problem to a sliding window of size k. Whenever the queue is full, compare the new value against the front — the front is always the *farthest* of the current candidates, so dropping it is optimal.",
        "complexity": ("O(n log k)", "O(h + k)"),
        "code": {
            "cpp": r"""// In-order + a size-k window: drop the farthest value when full
struct TreeNode { int val; TreeNode *left, *right; TreeNode(int v = 0) : val(v), left(nullptr), right(nullptr) {} };
void walk(TreeNode* node, double target, int k, deque<int>& win) {
    if (!node) return;
    walk(node->left, target, k, win);
    win.push_back(node->val);                    // values arrive ascending
    if ((int)win.size() > k) {
        if (abs(win.front() - target) <= abs(win.back() - target)) win.pop_back();
        else win.pop_front();                    // the front was farther away
    }
    walk(node->right, target, k, win);
}
vector<int> closestKValues(TreeNode* root, double target, int k) {
    deque<int> win;
    walk(root, target, k, win);
    return vector<int>(win.begin(), win.end());
}   // O(n) time · O(h + k) space""",
            "java": r"""// In-order + a size-k window: drop the farthest value when full
class TreeNode { int val; TreeNode left, right; TreeNode(int v) { val = v; } }
void walk(TreeNode node, double target, int k, Deque<Integer> win) {
    if (node == null) return;
    walk(node.left, target, k, win);
    win.addLast(node.val);                       // values arrive ascending
    if (win.size() > k) {
        if (Math.abs(win.peekFirst() - target) <= Math.abs(win.peekLast() - target))
            win.pollLast();
        else win.pollFirst();                    // the front was farther away
    }
    walk(node.right, target, k, win);
}
List<Integer> closestKValues(TreeNode root, double target, int k) {
    Deque<Integer> win = new ArrayDeque<>();
    walk(root, target, k, win);
    return new ArrayList<>(win);
}   // O(n) time · O(h + k) space""",
            "python": r"""from collections import deque

def closest_k_values(root, target, k):
    win = deque()                    # ascending values, size at most k
    def walk(node):
        if not node:
            return
        walk(node.left)
        win.append(node.val)
        if len(win) > k:             # drop the candidate farthest from target
            if abs(win[0] - target) <= abs(win[-1] - target):
                win.pop()
            else:
                win.popleft()
        walk(node.right)

    walk(root)
    return list(win)""",
        },
    },
]
