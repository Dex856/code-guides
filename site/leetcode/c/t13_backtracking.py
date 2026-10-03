# Topic 13 · Backtracking & Recursion — C17 solutions
#
# The C pattern is always the same:
#     void go(state, ...)   — check the goal, loop over the choices,
#                             take one, recurse, undo it.
# The `undo` line is what makes it backtracking rather than brute force.

CODE = {
    "power-of-two": r"""
// A power of two has exactly one 1 bit — and is positive.
int isPowerOfTwo(int n) { return n > 0 && (n & (n - 1)) == 0; }
// O(1) time · O(1) space
""",
    "power-of-three": r"""
// 3^19 is the largest power of three that fits in an int, so 3^19 % n == 0 is the test.
int isPowerOfThree(int n) { return n > 0 && 1162261467 % n == 0; }
// O(1) time · O(1) space
""",
    "fibonacci-number": r"""
// Rolling two variables: the whole table is unnecessary.
int fib(int n) {
    long long prev = 0, cur = 1;
    for (int i = 0; i < n; i++) { long long next = prev + cur; prev = cur; cur = next; }
    return (int) prev;
}   // O(n) time · O(1) space
""",
    "binary-tree-paths": r"""
// Depth-first search that carries the path as text and prints it at every leaf.
static void walk(struct TreeNode *root, char *path, int length, char **out, int *count) {
    if (!root) return;
    int written = snprintf(path + length, 128, "%s%d", length ? "->" : "", root->val);
    length += written;
    if (!root->left && !root->right) {
        out[*count] = strdup(path);
        (*count)++;
        return;
    }
    walk(root->left, path, length, out, count);
    walk(root->right, path, length, out, count);
    path[length - written] = '\0';                          // undo the text we added
}

char **binaryTreePaths(struct TreeNode *root, int *returnSize) {
    char **out = malloc(sizeof(char *) * 512);
    char path[1024] = "";
    int count = 0;
    walk(root, path, 0, out, &count);
    *returnSize = count;
    return out;
}   // O(n * h) time · O(h) recursion
""",
    "sum-of-left-leaves": r"""
// The flag "am I the left child?" is the whole trick.
static int walk(struct TreeNode *node, int isLeft) {
    if (!node) return 0;
    if (isLeft && !node->left && !node->right) return node->val;
    return walk(node->left, 1) + walk(node->right, 0);
}

int sumOfLeftLeaves(struct TreeNode *root) { return walk(root, 0); }
// O(n) time · O(h) space
""",
    "reverse-string": r"""
// Two pointers walking towards each other.
void reverseString(char *s, int n) {
    for (int left = 0, right = n - 1; left < right; left++, right--) {
        char t = s[left]; s[left] = s[right]; s[right] = t;
    }
}   // O(n) time · O(1) space
""",
    "letter-case-permutation": r"""
// Each letter doubles the answer: branch on lowercase and uppercase.
static void go(const char *s, int index, char *current, char **out, int *count) {
    if (!s[index]) {
        out[*count] = strdup(current);
        (*count)++;
        return;
    }
    char c = s[index];
    if (c >= 'a' && c <= 'z') {
        current[index] = c;
        go(s, index + 1, current, out, count);
        current[index] = (char) (c - 'a' + 'A');            // the other case
        go(s, index + 1, current, out, count);
    } else if (c >= 'A' && c <= 'Z') {
        current[index] = c;
        go(s, index + 1, current, out, count);
        current[index] = (char) (c - 'A' + 'a');
        go(s, index + 1, current, out, count);
    } else {
        current[index] = c;                                 // digits: one branch only
        go(s, index + 1, current, out, count);
    }
    current[index] = c;                                     // backtrack
}

char **letterCasePermutation(const char *s, int *returnSize) {
    char **out = malloc(sizeof(char *) * 4096);
    char *current = calloc(strlen(s) + 1, 1);               // zeroed: it ends up NUL terminated
    int count = 0;
    go(s, 0, current, out, &count);
    free(current);
    *returnSize = count;
    return out;
}   // O(2^letters * n) time · O(n) recursion
""",
    "subsets": r"""
// At every index decide: take this number or skip it.
static void go(const int *a, int n, int index, int *current, int depth,
               int **out, int *sizes, int *count) {
    if (index == n) {
        out[*count] = malloc(sizeof(int) * (size_t) (depth ? depth : 1));
        memcpy(out[*count], current, sizeof(int) * (size_t) depth);
        sizes[*count] = depth;
        (*count)++;
        return;
    }
    go(a, n, index + 1, current, depth, out, sizes, count);              // skip
    current[depth] = a[index];
    go(a, n, index + 1, current, depth + 1, out, sizes, count);          // take
}

int **subsets(const int *nums, int n, int *returnSize, int **returnColumnSizes) {
    int **out = malloc(sizeof(int *) * 4096);
    *returnColumnSizes = malloc(sizeof(int) * 4096);
    int *current = malloc(sizeof(int) * (size_t) (n ? n : 1));
    int count = 0;
    go(nums, n, 0, current, 0, out, *returnColumnSizes, &count);
    free(current);
    *returnSize = count;
    return out;
}   // O(2^n * n) time · O(n) recursion
""",
    "combinations": r"""
// Pick k of n in increasing order so no permutation is repeated.
static void go(int n, int k, int start, int *current, int depth, int **out, int *count) {
    if (depth == k) {
        out[*count] = malloc(sizeof(int) * (size_t) k);
        memcpy(out[*count], current, sizeof(int) * (size_t) k);
        (*count)++;
        return;
    }
    for (int v = start; v <= n - (k - depth) + 1; v++) {    // leave enough numbers behind
        current[depth] = v;
        go(n, k, v + 1, current, depth + 1, out, count);
    }
}

int **combine(int n, int k, int *returnSize, int **returnColumnSizes) {
    int **out = malloc(sizeof(int *) * 65536);
    *returnColumnSizes = malloc(sizeof(int) * 65536);
    int *current = malloc(sizeof(int) * (size_t) (k ? k : 1));
    int count = 0;
    if (k >= 0 && k <= n) go(n, k, 1, current, 0, out, &count);
    for (int i = 0; i < count; i++) (*returnColumnSizes)[i] = k;
    free(current);
    *returnSize = count;
    return out;
}   // O(C(n, k) * k) time · O(k) recursion
""",
    "permutations": r"""
// Swap the current position with each later one — no `used` array needed.
static void swapInt(int *a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }

static void go(int *a, int n, int start, int **out, int *count) {
    if (start == n) {
        out[*count] = malloc(sizeof(int) * (size_t) n);
        memcpy(out[*count], a, sizeof(int) * (size_t) n);
        (*count)++;
        return;
    }
    for (int i = start; i < n; i++) {
        swapInt(a, start, i);
        go(a, n, start + 1, out, count);
        swapInt(a, start, i);                               // undo the swap
    }
}

int **permute(int *nums, int n, int *returnSize, int **returnColumnSizes) {
    int **out = malloc(sizeof(int *) * 65536);
    *returnColumnSizes = malloc(sizeof(int) * 65536);
    int count = 0;
    go(nums, n, 0, out, &count);
    for (int i = 0; i < count; i++) (*returnColumnSizes)[i] = n;
    *returnSize = count;
    return out;
}   // O(n! * n) time · O(n) recursion
""",
    "gray-code": r"""
// The i-th Gray code is i ^ (i >> 1) — one bit changes between neighbours.
int *grayCode(int n, int *returnSize) {
    int size = 1 << n;
    int *out = malloc(sizeof(int) * (size_t) size);
    for (int i = 0; i < size; i++) out[i] = i ^ (i >> 1);
    *returnSize = size;
    return out;
}   // O(2^n) time · O(2^n) space
""",
    "palindrome-partitioning": r"""
// Try every palindromic prefix, then recurse on the rest.
static int isPalindrome(const char *s, int start, int end) {
    while (start < end) if (s[start++] != s[end--]) return 0;
    return 1;
}

static void go(const char *s, int n, int start, char ***out, int *sizes, int *count,
               char **current, int depth) {
    if (start == n) {
        out[*count] = malloc(sizeof(char *) * (size_t) depth);
        for (int i = 0; i < depth; i++) out[*count][i] = strdup(current[i]);
        sizes[*count] = depth;
        (*count)++;
        return;
    }
    for (int end = start; end < n; end++) {
        if (!isPalindrome(s, start, end)) continue;
        int length = end - start + 1;
        current[depth] = malloc((size_t) length + 1);
        memcpy(current[depth], s + start, (size_t) length);
        current[depth][length] = '\0';
        go(s, n, end + 1, out, sizes, count, current, depth + 1);
        free(current[depth]);                               // undo
    }
}

char ***partition(const char *s, int *returnSize, int **returnColumnSizes) {
    int n = (int) strlen(s);
    char ***out = malloc(sizeof(char **) * 65536);
    *returnColumnSizes = malloc(sizeof(int) * 65536);
    char **current = malloc(sizeof(char *) * (size_t) (n ? n : 1));
    int count = 0;
    go(s, n, 0, out, *returnColumnSizes, &count, current, 0);
    free(current);
    *returnSize = count;
    return out;
}   // O(n * 2^n) time · O(n) recursion
""",
    "restore-ip-addresses": r"""
// Four groups, each 1-3 digits, each at most 255 and without a leading zero.
static void go(const char *s, int n, int start, int group, char *current, char **out, int *count) {
    if (group == 4) {
        if (start == n) {
            out[*count] = strdup(current);
            (*count)++;
        }
        return;
    }
    int length = (int) strlen(current);
    for (int take = 1; take <= 3 && start + take <= n; take++) {
        if (take > 1 && s[start] == '0') break;             // no leading zeros
        int value = 0;
        for (int i = 0; i < take; i++) value = value * 10 + (s[start + i] - '0');
        if (value > 255) break;
        if (group) current[length] = '.';                   // dot between the groups
        memcpy(current + length + (group ? 1 : 0), s + start, (size_t) take);
        int newLength = length + (group ? 1 : 0) + take;
        current[newLength] = '\0';
        go(s, n, start + take, group + 1, current, out, count);
        current[length] = '\0';                             // backtrack
    }
}

char **restoreIpAddresses(const char *s, int *returnSize) {
    char **out = malloc(sizeof(char *) * 4096);
    char current[64] = "";
    int count = 0, n = (int) strlen(s);
    if (n >= 4 && n <= 12) go(s, n, 0, 0, current, out, &count);
    *returnSize = count;
    return out;
}   // O(3^4) time · O(1) recursion
""",
    "generate-parentheses": r"""
// Add '(' while any remain, add ')' only when it keeps the string valid.
static void go(int n, int open, int close, char *current, int depth, char **out, int *count) {
    if (depth == 2 * n) {
        current[depth] = '\0';
        out[*count] = strdup(current);
        (*count)++;
        return;
    }
    if (open < n) {
        current[depth] = '(';
        go(n, open + 1, close, current, depth + 1, out, count);
    }
    if (close < open) {
        current[depth] = ')';
        go(n, open, close + 1, current, depth + 1, out, count);
    }
}

char **generateParenthesis(int n, int *returnSize) {
    char **out = malloc(sizeof(char *) * 65536);
    char *current = malloc((size_t) 2 * n + 1);
    int count = 0;
    go(n, 0, 0, current, 0, out, &count);
    free(current);
    *returnSize = count;
    return out;
}   // O(4^n / sqrt(n)) time · O(n) recursion
""",
    "combination-sum": r"""
// Unbounded picks: stay at the same index to reuse a number, move on to stop using it.
static void go(const int *a, int n, int index, int remaining, int *current, int depth,
               int **out, int *sizes, int *count) {
    if (remaining == 0) {
        out[*count] = malloc(sizeof(int) * (size_t) depth);
        memcpy(out[*count], current, sizeof(int) * (size_t) depth);
        sizes[*count] = depth;
        (*count)++;
        return;
    }
    for (int i = index; i < n; i++) {
        if (a[i] > remaining) continue;                     // would overshoot
        current[depth] = a[i];
        go(a, n, i, remaining - a[i], current, depth + 1, out, sizes, count);
    }
}

int **combinationSum(const int *candidates, int n, int target, int *returnSize, int **returnColumnSizes) {
    int **out = malloc(sizeof(int *) * 16384);
    *returnColumnSizes = malloc(sizeof(int) * 16384);
    int *current = malloc(sizeof(int) * (size_t) (target + 1));
    int count = 0;
    go(candidates, n, 0, target, current, 0, out, *returnColumnSizes, &count);
    free(current);
    *returnSize = count;
    return out;
}   // O(target^2) exploration · O(target) recursion
""",
    "subsets-ii": r"""
// Sort first, then skip duplicates at the same depth level.
static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}

static void go(const int *a, int n, int index, int *current, int depth,
               int **out, int *sizes, int *count) {
    out[*count] = malloc(sizeof(int) * (size_t) (depth ? depth : 1));
    memcpy(out[*count], current, sizeof(int) * (size_t) depth);
    sizes[*count] = depth;
    (*count)++;
    for (int i = index; i < n; i++) {
        if (i > index && a[i] == a[i - 1]) continue;        // same value: one branch only
        current[depth] = a[i];
        go(a, n, i + 1, current, depth + 1, out, sizes, count);
    }
}

int **subsetsWithDup(int *nums, int n, int *returnSize, int **returnColumnSizes) {
    qsort(nums, (size_t) n, sizeof(int), cmpInt);
    int **out = malloc(sizeof(int *) * 4096);
    *returnColumnSizes = malloc(sizeof(int) * 4096);
    int *current = malloc(sizeof(int) * (size_t) (n ? n : 1));
    int count = 0;
    go(nums, n, 0, current, 0, out, *returnColumnSizes, &count);
    free(current);
    *returnSize = count;
    return out;
}   // O(2^n * n) time · O(n) recursion
""",
    "letter-tile-possibilities": r"""
// Count every distinct arrangement: pick a tile, recurse, put it back.
static int go(int *counts, int remaining) {
    if (!remaining) return 1;                               // one arrangement reached
    int total = 1;                                          // the empty continuation counts
    for (int c = 0; c < 26; c++) {
        if (!counts[c]) continue;
        counts[c]--;                                        // use this tile
        total += go(counts, remaining - 1);
        counts[c]++;                                        // and give it back
    }
    return total;
}

int numTilePossibilities(const char *tiles) {
    int counts[26] = {0}, n = (int) strlen(tiles);
    for (int i = 0; i < n; i++) counts[tiles[i] - 'A']++;
    return go(counts, n) - 1;                               // minus the empty sequence
}   // O(n!) exploration · O(n) recursion
""",
    "unique-binary-search-trees-ii": r"""
// Build every BST on the range [lo, hi] recursively.
static struct TreeNode **build(int lo, int hi, int *count) {
    struct TreeNode **out = malloc(sizeof(struct TreeNode *) * 4096);
    int n = 0;
    if (lo > hi) {
        out[n++] = NULL;                                    // the empty tree is a valid subtree
        *count = n;
        return out;
    }
    for (int root = lo; root <= hi; root++) {
        int leftCount = 0, rightCount = 0;
        struct TreeNode **left = build(lo, root - 1, &leftCount);
        struct TreeNode **right = build(root + 1, hi, &rightCount);
        for (int l = 0; l < leftCount; l++)
            for (int r = 0; r < rightCount; r++) {
                struct TreeNode *node = malloc(sizeof(struct TreeNode));
                node->val = root;
                node->left = left[l];
                node->right = right[r];
                out[n++] = node;
            }
        free(left); free(right);
    }
    *count = n;
    return out;
}

struct TreeNode **generateTrees(int n, int *returnSize) {
    int count = 0;
    struct TreeNode **forest = build(1, n, &count);
    *returnSize = count;
    return forest;
}   // O(Catalan(n) * n) time · O(n) recursion
""",
    "n-queens-ii": r"""
// Columns and both diagonals are bitmasks: a queen is placeable when all three are free.
static int go(int n, int row, int columns, int downDiagonal, int upDiagonal) {
    if (row == n) return 1;
    int total = 0;
    for (int col = 0; col < n; col++) {
        int down = row - col + n, up = row + col;           // diagonal indexes, made positive
        if (columns & (1 << col)) continue;
        if (downDiagonal & (1 << down)) continue;
        if (upDiagonal & (1 << up)) continue;
        total += go(n, row + 1, columns | (1 << col),
                    downDiagonal | (1 << down), upDiagonal | (1 << up));
    }
    return total;
}

int totalNQueens(int n) { return go(n, 0, 0, 0, 0); }
// O(n!) exploration · O(n) recursion
""",
    "n-queens": r"""
// Same search as n-queens-ii, but each complete board is written out.
static void go(int n, int row, int *placement, char ***out, int *count) {
    if (row == n) {
        out[*count] = malloc(sizeof(char *) * (size_t) n);
        for (int r = 0; r < n; r++) {
            out[*count][r] = malloc((size_t) n + 1);
            for (int c = 0; c < n; c++) out[*count][r][c] = placement[r] == c ? 'Q' : '.';
            out[*count][r][n] = '\0';
        }
        (*count)++;
        return;
    }
    for (int col = 0; col < n; col++) {
        int safe = 1;
        for (int r = 0; r < row && safe; r++) {
            if (placement[r] == col) safe = 0;                       // same column
            if (abs(placement[r] - col) == row - r) safe = 0;        // same diagonal
        }
        if (!safe) continue;
        placement[row] = col;
        go(n, row + 1, placement, out, count);
    }
}

char ***solveNQueens(int n, int *returnSize, int **returnColumnSizes) {
    char ***out = malloc(sizeof(char **) * 4096);
    *returnColumnSizes = malloc(sizeof(int) * 4096);
    int *placement = malloc(sizeof(int) * (size_t) (n ? n : 1));
    int count = 0;
    go(n, 0, placement, out, &count);
    free(placement);
    for (int i = 0; i < count; i++) (*returnColumnSizes)[i] = n;
    *returnSize = count;
    return out;
}   // O(n!) exploration · O(n) recursion
""",
    "number-of-squareful-arrays": r"""
// Build the sequence position by position, using each number once.
static int isSquare(int v) {
    int root = (int) (sqrt((double) v) + 0.5);
    return root * root == v;
}

static int go(int *a, int n, int *used, int depth, int previous) {
    if (depth == n) return 1;
    int total = 0;
    for (int i = 0; i < n; i++) {
        if (used[i]) continue;
        if (i > 0 && a[i] == a[i - 1] && !used[i - 1]) continue;   // a duplicate must be used first
        if (depth && !isSquare(previous + a[i])) continue;
        used[i] = 1;
        total += go(a, n, used, depth + 1, a[i]);
        used[i] = 0;
    }
    return total;
}

static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}

int numSquarefulPerms(int *nums, int n) {
    qsort(nums, (size_t) n, sizeof(int), cmpInt);
    int *used = calloc((size_t) n, sizeof(int));
    int total = go(nums, n, used, 0, 0);
    free(used);
    return total;
}   // O(n!) exploration · O(n) recursion
""",
    "unique-paths-iii": r"""
// Walk every non-obstacle square exactly once and count the walks that end on the goal.
static int go(int **grid, int rows, int cols, int r, int c, int emptyLeft) {
    if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] == -1) return 0;
    if (grid[r][c] == 2) return emptyLeft == 0;             // reached the end with all squares used
    grid[r][c] = -1;                                        // mark visited
    int total = go(grid, rows, cols, r + 1, c, emptyLeft - 1)
              + go(grid, rows, cols, r - 1, c, emptyLeft - 1)
              + go(grid, rows, cols, r, c + 1, emptyLeft - 1)
              + go(grid, rows, cols, r, c - 1, emptyLeft - 1);
    grid[r][c] = 0;                                         // undo the mark
    return total;
}

int uniquePathsIII(int rows, int cols, int **grid) {
    int startRow = 0, startCol = 0, empty = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) {
            if (grid[r][c] == 1) { startRow = r; startCol = c; }
            else if (!grid[r][c]) empty++;
        }
    return go(grid, rows, cols, startRow, startCol, empty + 1);
}   // O(4^(rows * cols)) exploration · O(rows * cols) recursion depth
""",
    "maximum-score-words-formed-by-letters": r"""
// Take the word if its letters are available, or skip it — the classic subset search.
static int go(char **words, int *scores, int n, int index, int *available) {
    if (index == n) return 0;
    int best = go(words, scores, n, index + 1, available);  // skip this word
    int letters[26] = {0}, score = 0, usable = 1;
    for (int i = 0; words[index][i]; i++) {
        int c = words[index][i] - 'a';
        letters[c]++;
        score += scores[c];
        if (letters[c] > available[c]) usable = 0;          // not enough of this letter
    }
    if (usable) {
        for (int c = 0; c < 26; c++) available[c] -= letters[c];
        int taken = score + go(words, scores, n, index + 1, available);
        if (taken > best) best = taken;
        for (int c = 0; c < 26; c++) available[c] += letters[c];   // give the letters back
    }
    return best;
}

int maxScoreWords(char **words, int wordCount, char *letters, int letterCount, int *score) {
    (void) letterCount;
    int available[26] = {0};
    for (int i = 0; letters[i]; i++) available[letters[i] - 'a']++;
    return go(words, score, wordCount, 0, available);
}   // O(2^words * length) time · O(26) space
""",
    "remove-invalid-parentheses": r"""
// Find the minimum removals by counting, then generate every string with that many.
static int isValid(const char *s) {
    int balance = 0;
    for (int i = 0; s[i]; i++) {
        if (s[i] == '(') balance++;
        else if (s[i] == ')') { if (--balance < 0) return 0; }
    }
    return balance == 0;
}

static void go(const char *s, int index, int leftRemove, int rightRemove, int open,
               char *current, int depth, char **out, int *count) {
    if (index == (int) strlen(s)) {
        if (leftRemove == 0 && rightRemove == 0 && open == 0) {
            current[depth] = '\0';
            out[*count] = strdup(current);
            (*count)++;
        }
        return;
    }
    char c = s[index];
    if (c == '(' && leftRemove > 0) go(s, index + 1, leftRemove - 1, rightRemove, open, current, depth, out, count);
    if (c == ')' && rightRemove > 0) go(s, index + 1, leftRemove, rightRemove - 1, open, current, depth, out, count);
    current[depth] = c;
    if (c != '(' && c != ')') go(s, index + 1, leftRemove, rightRemove, open, current, depth + 1, out, count);
    else if (c == '(') go(s, index + 1, leftRemove, rightRemove, open + 1, current, depth + 1, out, count);
    else if (open > 0) go(s, index + 1, leftRemove, rightRemove, open - 1, current, depth + 1, out, count);
    current[depth] = '\0';
}

char **removeInvalidParentheses(const char *s, int *returnSize) {
    int leftRemove = 0, rightRemove = 0;
    for (int i = 0; s[i]; i++) {                            // how many of each must go
        if (s[i] == '(') leftRemove++;
        else if (s[i] == ')') { if (leftRemove) leftRemove--; else rightRemove++; }
    }
    char **out = malloc(sizeof(char *) * 16384);
    char *current = malloc(strlen(s) + 1);
    int count = 0;
    go(s, 0, leftRemove, rightRemove, 0, current, 0, out, &count);
    free(current);
    /* de-duplicate the results */
    int unique = 0;
    for (int i = 0; i < count; i++) {
        int duplicate = 0;
        for (int j = 0; j < unique && !duplicate; j++) if (!strcmp(out[j], out[i])) duplicate = 1;
        if (duplicate) free(out[i]);
        else out[unique++] = out[i];
    }
    *returnSize = unique ? unique : 1;
    if (!unique) out[0] = strdup("");                       // the answer is never empty
    return out;
}   // O(2^n * n) time · O(n) recursion
""",
    "expression-add-operators": r"""
// Track the running value and the last operand so "*" can be applied correctly.
static void go(const char *num, int n, int index, long long target,
               long long value, long long previous, char *current, int length,
               char **out, int *count) {
    if (index == n) {
        if (value == target) {
            current[length] = '\0';
            out[*count] = strdup(current);
            (*count)++;
        }
        return;
    }
    long long operand = 0;
    int startLength = length;
    for (int i = index; i < n; i++) {
        if (i > index && num[index] == '0') break;          // no numbers with leading zeros
        operand = operand * 10 + (num[i] - '0');
        length = startLength;
        if (index == 0) {                                   // the first number has no sign
            length += snprintf(current + length, 32, "%lld", operand);
            go(num, n, i + 1, target, operand, operand, current, length, out, count);
            continue;
        }
        length += snprintf(current + length, 32, "+%lld", operand);
        go(num, n, i + 1, target, value + operand, operand, current, length, out, count);
        length = startLength + snprintf(current + startLength, 32, "-%lld", operand);
        go(num, n, i + 1, target, value - operand, -operand, current, length, out, count);
        length = startLength + snprintf(current + startLength, 32, "*%lld", operand);
        go(num, n, i + 1, target, value - previous + previous * operand, previous * operand,
           current, length, out, count);
    }
}

char **addOperators(const char *num, int target, int *returnSize) {
    int n = (int) strlen(num);
    char **out = malloc(sizeof(char *) * 16384);
    char *current = malloc((size_t) 2 * n + 64);
    int count = 0;
    go(num, n, 0, target, 0, 0, current, 0, out, &count);
    free(current);
    *returnSize = count;
    return out;
}   // O(3^n) exploration · O(n) recursion
""",
    "valid-permutations-for-di-sequence": r"""
// dp[i] = number of valid sequences using the first i + 1 numbers; update by direction.
int numPermsDISequence(const char *s) {
    const long long MOD = 1000000007;
    int n = (int) strlen(s);
    long long *dp = calloc((size_t) n + 1, sizeof(long long));
    for (int i = 0; i <= n; i++) dp[i] = 1;                 // sequences of one number
    for (int length = 2; length <= n + 1; length++) {       // grow the sequences one step
        long long *next = calloc((size_t) n + 1, sizeof(long long));
        if (s[length - 2] == 'D') {                         // a descent: next[j] = sum dp[j+1..]
            long long running = 0;
            for (int k = length - 1; k >= 1; k--) {
                running = (running + dp[k]) % MOD;
                next[k - 1] = running;
            }
        } else {                                            // an ascent: next[j] = sum dp[..j-1]
            long long running = 0;
            for (int k = 0; k <= length - 2; k++) {
                running = (running + dp[k]) % MOD;
                next[k + 1] = running;
            }
        }
        free(dp);
        dp = next;
    }
    long long total = 0;
    for (int i = 0; i <= n; i++) total = (total + dp[i]) % MOD;
    free(dp);
    return (int) total;
}   // O(n^2) time · O(n) space
""",
    "find-minimum-time-to-finish-all-jobs": r"""
// Binary search the makespan and test it by assigning each job to a worker in turn.
static int canFinish(int *jobs, int n, int *load, int workers, int limit, int index) {
    if (index == n) return 1;
    for (int w = 0; w < workers; w++) {
        if (load[w] + jobs[index] > limit) continue;
        load[w] += jobs[index];
        if (canFinish(jobs, n, load, workers, limit, index + 1)) return 1;
        load[w] -= jobs[index];
        if (!load[w]) break;                                // a worker with no load is equivalent
    }
    return 0;
}

int minimumTimeRequired(int *jobs, int n, int k) {
    int lo = 0, hi = 0;
    for (int i = 0; i < n; i++) {
        hi += jobs[i];
        if (jobs[i] > lo) lo = jobs[i];
    }
    int *load = calloc((size_t) k, sizeof(int));
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (canFinish(jobs, n, load, k, mid, 0)) hi = mid;
        else lo = mid + 1;
    }
    free(load);
    return lo;
}   // O(log sum * k^n) exploration · O(k) space
""",
    "maximum-number-of-achievable-transfer-requests": r"""
// Each request is either taken or not; a set is achievable when every building's net is zero.
static int go(int **requests, int n, int index, int *net, int taken) {
    if (index == n) {
        for (int b = 0; b < 32; b++) if (net[b]) return -1;   // unbalanced: unusable
        return taken;
    }
    int best = go(requests, n, index + 1, net, taken);        // skip this request
    net[requests[index][0]]--;
    net[requests[index][1]]++;
    int withRequest = go(requests, n, index + 1, net, taken + 1);
    net[requests[index][0]]++;
    net[requests[index][1]]--;                                // undo
    return withRequest > best ? withRequest : best;
}

int maximumRequests(int n, int **requests, int requestCount) {
    (void) n;
    int net[32] = {0};
    return go(requests, requestCount, 0, net, 0);
}   // O(2^n * buildings) time · O(n) recursion
""",
    "24-game": r"""
// Pick two numbers, apply one of six operations, and put the result back.
static int canReach(double *values, int n) {
    if (n == 1) return fabs(values[0] - 24.0) < 1e-6;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            if (i == j) continue;
            double a = values[i], b = values[j], results[6];
            int count = 0;
            results[count++] = a + b;
            results[count++] = a - b;
            results[count++] = a * b;
            if (fabs(b) > 1e-9) results[count++] = a / b;
            for (int k = 0; k < count; k++) {
                double remaining[4];
                int m = 0;
                remaining[m++] = results[k];                // the combined value
                for (int t = 0; t < n; t++) if (t != i && t != j) remaining[m++] = values[t];
                if (canReach(remaining, m)) return 1;
            }
        }
    return 0;
}

int judgePoint24(int *cards, int n) {
    double values[4];
    for (int i = 0; i < n; i++) values[i] = cards[i];
    return canReach(values, n);
}   // O(6^n) exploration · O(n) recursion
""",
    "sudoku-solver": r"""
// Place a digit, recurse, and undo when the placement makes the board unsolvable.
static int safe(char **board, int r, int c, char digit) {
    for (int i = 0; i < 9; i++) {
        if (board[r][i] == digit) return 0;                 // row
        if (board[i][c] == digit) return 0;                 // column
    }
    int boxRow = r / 3 * 3, boxCol = c / 3 * 3;
    for (int i = boxRow; i < boxRow + 3; i++)
        for (int j = boxCol; j < boxCol + 3; j++)
            if (board[i][j] == digit) return 0;             // 3x3 box
    return 1;
}

static int solve(char **board) {
    for (int r = 0; r < 9; r++)
        for (int c = 0; c < 9; c++) {
            if (board[r][c] != '.') continue;
            for (char d = '1'; d <= '9'; d++) {
                if (!safe(board, r, c, d)) continue;
                board[r][c] = d;
                if (solve(board)) return 1;
                board[r][c] = '.';                          // undo and try the next digit
            }
            return 0;                                       // no digit fits: backtrack
        }
    return 1;                                               // nothing empty: solved
}

void solveSudoku(char **board) { solve(board); }
// O(9^(empty cells)) worst case · O(1) extra space
""",
}
