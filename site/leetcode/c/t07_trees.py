# Topic 7 · Trees & BSTs — C17 solutions
#
#     struct TreeNode { int val; struct TreeNode *left, *right; };
#
# Recursion is the natural C answer here: the tree is the recursion.

CODE = {
    "max-depth-of-binary-tree": r"""
// One plus the deeper child.
int maxDepth(struct TreeNode *root) {
    if (!root) return 0;
    int left = maxDepth(root->left), right = maxDepth(root->right);
    return 1 + (left > right ? left : right);
}   // O(n) time · O(h) space
""",
    "same-tree": r"""
// Structural equality: same value, and both sides equal recursively.
int isSameTree(struct TreeNode *p, struct TreeNode *q) {
    if (!p || !q) return p == q;                          // both empty, or only one is
    if (p->val != q->val) return 0;
    return isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
}   // O(n) time · O(h) space
""",
    "invert-binary-tree": r"""
// Swap the children, then invert both subtrees.
struct TreeNode *invertTree(struct TreeNode *root) {
    if (!root) return NULL;
    struct TreeNode *tmp = root->left;
    root->left = invertTree(root->right);
    root->right = invertTree(tmp);
    return root;
}   // O(n) time · O(h) space
""",
    "symmetric-tree": r"""
// A tree is symmetric when its two subtrees are mirror images.
static int mirror(struct TreeNode *a, struct TreeNode *b) {
    if (!a || !b) return a == b;
    return a->val == b->val && mirror(a->left, b->right) && mirror(a->right, b->left);
}

int isSymmetric(struct TreeNode *root) {
    return !root || mirror(root->left, root->right);
}   // O(n) time · O(h) space
""",
    "diameter-of-binary-tree": r"""
// The answer through a node is leftDepth + rightDepth; return only one side upwards.
static int depthAndBest(struct TreeNode *root, int *best) {
    if (!root) return 0;
    int left = depthAndBest(root->left, best);
    int right = depthAndBest(root->right, best);
    if (left + right > *best) *best = left + right;        // path bending at this node
    return 1 + (left > right ? left : right);
}

int diameterOfBinaryTree(struct TreeNode *root) {
    int best = 0;
    depthAndBest(root, &best);
    return best;
}   // O(n) time · O(h) space
""",
    "balanced-binary-tree": r"""
// -1 means "already unbalanced"; otherwise the height comes back.
static int heightOrFail(struct TreeNode *root) {
    if (!root) return 0;
    int left = heightOrFail(root->left);
    if (left < 0) return -1;
    int right = heightOrFail(root->right);
    if (right < 0) return -1;
    if (left - right > 1 || right - left > 1) return -1;   // the heights differ too much
    return 1 + (left > right ? left : right);
}

int isBalanced(struct TreeNode *root) { return heightOrFail(root) >= 0; }
// O(n) time · O(h) space
""",
    "binary-tree-level-order-traversal": r"""
// A queue of nodes; the level size tells you where each row ends.
int **levelOrder(struct TreeNode *root, int *returnSize, int **returnColumnSizes) {
    int **levels = malloc(sizeof(int *) * 2048);
    *returnColumnSizes = malloc(sizeof(int) * 2048);
    struct TreeNode **queue = malloc(sizeof(struct TreeNode *) * 4096);
    int head = 0, tail = 0, count = 0;
    if (root) queue[tail++] = root;
    while (head < tail) {
        int size = tail - head;                           // everything currently queued is one row
        levels[count] = malloc(sizeof(int) * (size_t) size);
        for (int i = 0; i < size; i++) {
            struct TreeNode *node = queue[head++];
            levels[count][i] = node->val;
            if (node->left) queue[tail++] = node->left;
            if (node->right) queue[tail++] = node->right;
        }
        (*returnColumnSizes)[count] = size;
        count++;
    }
    free(queue);
    *returnSize = count;
    return levels;
}   // O(n) time · O(n) space
""",
    "path-sum": r"""
// Subtract as you descend; a leaf that reaches zero means success.
int hasPathSum(struct TreeNode *root, int targetSum) {
    if (!root) return 0;
    if (!root->left && !root->right) return root->val == targetSum;
    return hasPathSum(root->left, targetSum - root->val) ||
           hasPathSum(root->right, targetSum - root->val);
}   // O(n) time · O(h) space
""",
    "lowest-common-ancestor-of-a-bst": r"""
// In a BST the split point is the ancestor: go left, right, or stop.
struct TreeNode *lowestCommonAncestorBST(struct TreeNode *root, struct TreeNode *p, struct TreeNode *q) {
    while (root) {
        if (p->val < root->val && q->val < root->val) root = root->left;
        else if (p->val > root->val && q->val > root->val) root = root->right;
        else return root;                                 // the paths part here
    }
    return NULL;
}   // O(h) time · O(1) space
""",
    "validate-binary-search-tree": r"""
// Carry the allowed (low, high) range down the tree.
static int validRange(struct TreeNode *root, long long low, long long high) {
    if (!root) return 1;
    if (root->val <= low || root->val >= high) return 0;
    return validRange(root->left, low, root->val) && validRange(root->right, root->val, high);
}

int isValidBST(struct TreeNode *root) {
    return validRange(root, LLONG_MIN, LLONG_MAX);
}   // O(n) time · O(h) space
""",
    "kth-smallest-element-in-a-bst": r"""
// An in-order walk of a BST yields the values in sorted order.
static void inorder(struct TreeNode *root, int k, int *count, int *answer) {
    if (!root || *count >= k) return;
    inorder(root->left, k, count, answer);
    if (++(*count) == k) { *answer = root->val; return; }
    inorder(root->right, k, count, answer);
}

int kthSmallest(struct TreeNode *root, int k) {
    int count = 0, answer = -1;
    inorder(root, k, &count, &answer);
    return answer;
}   // O(h + k) time · O(h) space
""",
    "binary-tree-right-side-view": r"""
// Level order, but only the last node of each row is recorded.
int *rightSideView(struct TreeNode *root, int *returnSize) {
    int *out = malloc(sizeof(int) * 2048);
    struct TreeNode **queue = malloc(sizeof(struct TreeNode *) * 4096);
    int head = 0, tail = 0, count = 0;
    if (root) queue[tail++] = root;
    while (head < tail) {
        int size = tail - head;
        for (int i = 0; i < size; i++) {
            struct TreeNode *node = queue[head++];
            if (i == size - 1) out[count++] = node->val;   // the rightmost of this level
            if (node->left) queue[tail++] = node->left;
            if (node->right) queue[tail++] = node->right;
        }
    }
    free(queue);
    *returnSize = count;
    return out;
}   // O(n) time · O(n) space
""",
    "zigzag-level-order-traversal": r"""
// Level order with the direction alternating row by row.
int **zigzagLevelOrder(struct TreeNode *root, int *returnSize, int **returnColumnSizes) {
    int **levels = malloc(sizeof(int *) * 2048);
    *returnColumnSizes = malloc(sizeof(int) * 2048);
    struct TreeNode **queue = malloc(sizeof(struct TreeNode *) * 4096);
    int head = 0, tail = 0, count = 0;
    if (root) queue[tail++] = root;
    while (head < tail) {
        int size = tail - head;
        levels[count] = malloc(sizeof(int) * (size_t) size);
        for (int i = 0; i < size; i++) {
            struct TreeNode *node = queue[head++];
            int slot = count % 2 ? size - 1 - i : i;      // every other row is reversed
            levels[count][slot] = node->val;
            if (node->left) queue[tail++] = node->left;
            if (node->right) queue[tail++] = node->right;
        }
        (*returnColumnSizes)[count] = size;
        count++;
    }
    free(queue);
    *returnSize = count;
    return levels;
}   // O(n) time · O(n) space
""",
    "construct-binary-tree-from-preorder-and-inorder": r"""
// The first preorder value is the root; its position in the inorder splits the halves.
static int indexOf(const int *inorder, int n, int value) {
    for (int i = 0; i < n; i++) if (inorder[i] == value) return i;
    return -1;
}

static struct TreeNode *buildFrom(const int *pre, const int *in, int n, int *used) {
    if (n <= 0) return NULL;
    int rootValue = pre[(*used)++];
    int mid = indexOf(in, n, rootValue);
    struct TreeNode *node = malloc(sizeof(struct TreeNode));
    node->val = rootValue;
    node->left = buildFrom(pre, in, mid, used);            // everything left of the root
    node->right = buildFrom(pre + mid + 1, in + mid + 1, n - mid - 1, used);
    return node;
}

struct TreeNode *buildTree(int *preorder, int preorderSize, int *inorder, int inorderSize) {
    int used = 0;
    return buildFrom(preorder, inorder, inorderSize, &used);
}   // O(n^2) time (O(n) with a value→index map) · O(h) space
""",
    "sum-root-to-leaf-numbers": r"""
// Carry the number built so far down each path.
static int walk(struct TreeNode *root, int sofar) {
    if (!root) return 0;
    sofar = sofar * 10 + root->val;
    if (!root->left && !root->right) return sofar;         // a complete number
    return walk(root->left, sofar) + walk(root->right, sofar);
}

int sumNumbers(struct TreeNode *root) { return walk(root, 0); }
// O(n) time · O(h) space
""",
    "delete-node-in-a-bst": r"""
// Find the node, then replace it with its in-order successor when it has two children.
struct TreeNode *deleteNode(struct TreeNode *root, int key) {
    if (!root) return NULL;
    if (key < root->val) root->left = deleteNode(root->left, key);
    else if (key > root->val) root->right = deleteNode(root->right, key);
    else {
        if (!root->left) return root->right;
        if (!root->right) return root->left;
        struct TreeNode *succ = root->right;              // smallest value on the right
        while (succ->left) succ = succ->left;
        root->val = succ->val;
        root->right = deleteNode(root->right, succ->val);
    }
    return root;
}   // O(h) time · O(h) space
""",
    "binary-tree-pruning": r"""
// A node disappears when its whole subtree has no 1.
struct TreeNode *pruneTree(struct TreeNode *root) {
    if (!root) return NULL;
    root->left = pruneTree(root->left);
    root->right = pruneTree(root->right);
    if (!root->left && !root->right && root->val == 0) return NULL;
    return root;
}   // O(n) time · O(h) space
""",
    "count-good-nodes-in-binary-tree": r"""
// A node is good when nothing on the path from the root is larger.
static int walkGood(struct TreeNode *root, int maxSoFar) {
    if (!root) return 0;
    int good = root->val >= maxSoFar ? 1 : 0;
    int next = root->val > maxSoFar ? root->val : maxSoFar;
    return good + walkGood(root->left, next) + walkGood(root->right, next);
}

int goodNodes(struct TreeNode *root) { return walkGood(root, INT_MIN); }
// O(n) time · O(h) space
""",
    "binary-tree-maximum-path-sum": r"""
// A path may bend once at some node: left + right + value. Above, only the better side
// is worth reporting because a path cannot fork.
static int bestDown(struct TreeNode *root, int *best) {
    if (!root) return 0;
    int left = bestDown(root->left, best), right = bestDown(root->right, best);
    if (left < 0) left = 0;                               // a negative branch is simply skipped
    if (right < 0) right = 0;
    if (left + right + root->val > *best) *best = left + right + root->val;
    return root->val + (left > right ? left : right);
}

int maxPathSum(struct TreeNode *root) {
    int best = INT_MIN;
    bestDown(root, &best);
    return best;
}   // O(n) time · O(h) space
""",
    "serialize-and-deserialize-binary-tree": r"""
// Preorder with explicit nulls: "1,2,#,#,3,4,#,#,5,#,#".
void serialize(struct TreeNode *root, char *out) {
    if (!root) { strcat(out, "#,"); return; }
    char buffer[16];
    snprintf(buffer, sizeof buffer, "%d,", root->val);
    strcat(out, buffer);
    serialize(root->left, out);
    serialize(root->right, out);
}

static struct TreeNode *parseNode(char **cursor) {
    if (!*cursor || !**cursor) return NULL;
    char *comma = strchr(*cursor, ',');
    if (!comma) return NULL;
    *comma = '\0';
    struct TreeNode *node;
    if (!strcmp(*cursor, "#")) node = NULL;
    else {
        node = malloc(sizeof(struct TreeNode));
        node->val = atoi(*cursor);
        node->left = parseNode(&(char *){comma + 1});
    }
    if (node) {
        *comma = ',';
        *cursor = comma + 1;
        node->left = parseNode(cursor);
        char *after = strchr(*cursor, ',');
        if (!after) return node;
        *cursor = after + 1;
        node->right = parseNode(cursor);
    }
    return node;
}

struct TreeNode *deserialize(char *data) {
    char *cursor = data;
    return parseNode(&cursor);
}   // O(n) time · O(n) space
""",
    "recover-binary-search-tree": r"""
// In-order finds the two values that are out of order; swap them back.
static void inorderCheck(struct TreeNode *root, struct TreeNode **prev,
                         struct TreeNode **first, struct TreeNode **second) {
    if (!root) return;
    inorderCheck(root->left, prev, first, second);
    if (*prev && (*prev)->val > root->val) {
        if (!*first) *first = *prev;                      // first mistake
        *second = root;                                   // last mistake (handles adjacent swaps)
    }
    *prev = root;
    inorderCheck(root->right, prev, first, second);
}

void recoverTree(struct TreeNode *root) {
    struct TreeNode *prev = NULL, *first = NULL, *second = NULL;
    inorderCheck(root, &prev, &first, &second);
    if (first && second) { int t = first->val; first->val = second->val; second->val = t; }
}   // O(n) time · O(h) space
""",
    "binary-tree-cameras": r"""
// 0 = not covered, 1 = has a camera, 2 = covered. Children are handled bottom-up.
static int place(struct TreeNode *root, int *cameras) {
    if (!root) return 2;
    int left = place(root->left, cameras), right = place(root->right, cameras);
    if (left == 0 || right == 0) { (*cameras)++; return 1; }        // a child needs watching
    if (left == 1 || right == 1) return 2;                          // already covered
    return 0;                                                       // ask the parent to cover it
}

int minCameraCover(struct TreeNode *root) {
    int cameras = 0;
    if (place(root, &cameras) == 0) cameras++;               // the root still needs one
    return cameras;
}   // O(n) time · O(h) space
""",
    "vertical-order-traversal-of-a-binary-tree": r"""
// Collect (column, row, value) for every node, sort by column then row then value.
struct Cell { int col, row, val; };

static int cmpCell(const void *a, const void *b) {
    const struct Cell *x = a, *y = b;
    if (x->col != y->col) return x->col - y->col;
    if (x->row != y->row) return x->row - y->row;
    return x->val - y->val;
}

static void collect(struct TreeNode *root, int col, int row, struct Cell *cells, int *n) {
    if (!root) return;
    cells[*n].col = col;
    cells[*n].row = row;
    cells[*n].val = root->val;
    (*n)++;
    collect(root->left, col - 1, row + 1, cells, n);         // left children are one column left
    collect(root->right, col + 1, row + 1, cells, n);
}

int **verticalTraversal(struct TreeNode *root, int *returnSize, int **returnColumnSizes) {
    struct Cell *cells = malloc(sizeof(struct Cell) * 4096);
    int n = 0;
    collect(root, 0, 0, cells, &n);
    qsort(cells, (size_t) n, sizeof(struct Cell), cmpCell);
    int **out = malloc(sizeof(int *) * 4096);
    *returnColumnSizes = malloc(sizeof(int) * 4096);
    int groups = 0, i = 0;
    while (i < n) {
        int j = i;
        while (j < n && cells[j].col == cells[i].col) j++;    // one column at a time
        out[groups] = malloc(sizeof(int) * (size_t) (j - i));
        for (int k = i; k < j; k++) out[groups][k - i] = cells[k].val;
        (*returnColumnSizes)[groups] = j - i;
        groups++;
        i = j;
    }
    free(cells);
    *returnSize = groups;
    return out;
}   // O(n log n) time · O(n) space
""",
    "path-sum-iii": r"""
// Every node asks "how many paths starting here end at targetSum?" — plus its children's.
static long long pathsFrom(struct TreeNode *root, long long target) {
    if (!root) return 0;
    long long here = root->val == target ? 1 : 0;             // may also continue downwards
    return here + pathsFrom(root->left, target - root->val)
                + pathsFrom(root->right, target - root->val);
}

int pathSumIII(struct TreeNode *root, int targetSum) {
    if (!root) return 0;
    return (int) pathsFrom(root, targetSum)
         + pathSumIII(root->left, targetSum)               // paths that start lower down
         + pathSumIII(root->right, targetSum);
}   // O(n^2) worst case · O(h) space (a prefix-sum map gives O(n))
""",
    "house-robber-iii": r"""
// For each node, return {robbed, skipped}: taking a node skips its children.
typedef struct { int take, skip; } Rob;

static Rob robTree(struct TreeNode *root) {
    Rob result = {0, 0};
    if (!root) return result;
    Rob left = robTree(root->left), right = robTree(root->right);
    result.take = root->val + left.skip + right.skip;
    int bestLeft = left.take > left.skip ? left.take : left.skip;
    int bestRight = right.take > right.skip ? right.take : right.skip;
    result.skip = bestLeft + bestRight;
    return result;
}

int rob(struct TreeNode *root) {
    Rob r = robTree(root);
    return r.take > r.skip ? r.take : r.skip;
}   // O(n) time · O(h) space
""",
    "lowest-common-ancestor-of-a-binary-tree": r"""
// If the two targets are found in different subtrees, this node is the answer.
struct TreeNode *lowestCommonAncestor(struct TreeNode *root, struct TreeNode *p, struct TreeNode *q) {
    if (!root || root == p || root == q) return root;
    struct TreeNode *left = lowestCommonAncestor(root->left, p, q);
    struct TreeNode *right = lowestCommonAncestor(root->right, p, q);
    if (left && right) return root;                           // one on each side
    return left ? left : right;
}   // O(n) time · O(h) space
""",
    "all-nodes-distance-k-in-binary-tree": r"""
// Build a parent map, then a breadth-first search outwards from the target.
int *distanceK(struct TreeNode *root, struct TreeNode *target, int k, int *returnSize) {
    struct TreeNode *parents[8192];
    struct TreeNode *queue[8192];
    int head = 0, tail = 0, count = 0;
    static int out[8192];
    parents[0] = NULL;
    queue[tail++] = root;
    while (head < tail) {                                     // one pass to record parents
        struct TreeNode *node = queue[head++];
        if (node->left) { parents[(int) (size_t) node->left % 8192] = node; queue[tail++] = node->left; }
        if (node->right) { parents[(int) (size_t) node->right % 8192] = node; queue[tail++] = node->right; }
    }
    struct TreeNode *seen[8192];
    int seenCount = 0;
    head = tail = 0;
    queue[tail++] = target;
    seen[seenCount++] = target;
    int distance = 0;
    while (head < tail) {
        int size = tail - head;
        if (distance == k) {
            for (int i = 0; i < size; i++) out[count++] = queue[head + i]->val;
            break;
        }
        for (int i = 0; i < size; i++) {
            struct TreeNode *node = queue[head++];
            struct TreeNode *next[3] = {node->left, node->right, parents[(int) (size_t) node % 8192]};
            for (int n = 0; n < 3; n++) {
                struct TreeNode *candidate = next[n];
                if (!candidate) continue;
                int already = 0;
                for (int s = 0; s < seenCount && !already; s++) if (seen[s] == candidate) already = 1;
                if (!already) { seen[seenCount++] = candidate; queue[tail++] = candidate; }
            }
        }
        distance++;
    }
    *returnSize = count;
    int *result = malloc(sizeof(int) * (size_t) (count ? count : 1));
    memcpy(result, out, sizeof(int) * (size_t) count);
    return result;
}   // O(n) time · O(n) space
""",
    "maximum-sum-bst-in-binary-tree": r"""
// Post-order: every subtree reports whether it is a BST plus its sum and value range.
typedef struct { int isBST, sum, min, max; } Info;

static Info scan(struct TreeNode *root, int *best) {
    Info info = {1, 0, INT_MAX, INT_MIN};
    if (!root) return info;
    Info left = scan(root->left, best), right = scan(root->right, best);
    if (left.isBST && right.isBST && left.max < root->val && root->val < right.min) {
        info.sum = left.sum + right.sum + root->val;
        info.min = left.min == INT_MAX ? root->val : left.min;
        info.max = right.max == INT_MIN ? root->val : right.max;
        if (info.sum > *best) *best = info.sum;
        return info;
    }
    info.isBST = 0;
    return info;
}

int maxSumBST(struct TreeNode *root) {
    int best = 0;
    scan(root, &best);
    return best;
}   // O(n) time · O(h) space
""",
    "bst-iterator": r"""
// The stack holds the path down the left spine; next() pops a node and pushes its right spine.
typedef struct {
    struct TreeNode *stack[4096];
    int top;
} BSTIterator;

BSTIterator *bSTIteratorCreate(struct TreeNode *root) {
    BSTIterator *it = calloc(1, sizeof(BSTIterator));
    struct TreeNode *cur = root;
    while (cur) { it->stack[it->top++] = cur; cur = cur->left; }
    return it;
}

int bSTIteratorNext(BSTIterator *it) {
    struct TreeNode *node = it->stack[--it->top];
    struct TreeNode *cur = node->right;
    while (cur) { it->stack[it->top++] = cur; cur = cur->left; }   // the successor's left spine
    return node->val;
}

int bSTIteratorHasNext(BSTIterator *it) { return it->top > 0; }
// amortised O(1) per call · O(h) space
""",
    "closest-binary-search-tree-value-ii": r"""
// In-order gives sorted values; a sliding window of k keeps the closest ones.
void closestKValues(struct TreeNode *root, double target, int k, int *out, int *outSize) {
    int *sorted = malloc(sizeof(int) * 4096);
    int n = 0;
    struct TreeNode *stack[4096];
    int top = 0;
    struct TreeNode *cur = root;
    while (cur || top) {                                  // iterative in-order walk
        while (cur) { stack[top++] = cur; cur = cur->left; }
        cur = stack[--top];
        sorted[n++] = cur->val;
        cur = cur->right;
    }
    int bestStart = 0;
    for (int i = 0; i + k <= n; i++) {                    // slide the window of length k
        double here = fabs(sorted[i + k - 1] - target), best = fabs(sorted[bestStart + k - 1] - target);
        double hereStart = fabs(sorted[i] - target), bestStartVal = fabs(sorted[bestStart] - target);
        if (here + hereStart < best + bestStartVal) bestStart = i;
    }
    for (int i = 0; i < k && bestStart + i < n; i++) out[i] = sorted[bestStart + i];
    *outSize = k < n ? k : n;
    free(sorted);
}   // O(n) time · O(h) space
""",
}
