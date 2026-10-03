# Topic 9 · Dynamic Programming — C17 solutions
#
# Rolling arrays replace the 2-D tables wherever the recurrence only looks back one
# row or one step, so most of these are O(1) or O(n) memory.

CODE = {
    "climbing-stairs": r"""
// Fibonacci: two variables are enough because only the last two steps matter.
int climbStairs(int n) {
    long long prev = 1, cur = 1;
    for (int i = 2; i <= n; i++) {
        long long next = prev + cur;
        prev = cur;
        cur = next;
    }
    return (int) cur;
}   // O(n) time · O(1) space
""",
    "n-th-tribonacci-number": r"""
// Same idea with a window of three.
int tribonacci(int n) {
    long long a = 0, b = 1, c = 1;
    for (int i = 0; i < n; i++) { long long next = a + b + c; a = b; b = c; c = next; }
    return (int) a;
}   // O(n) time · O(1) space
""",
    "min-cost-climbing-stairs": r"""
// dp[i] is the cheapest way to stand on step i; the answer is the cheaper of the last two.
int minCostClimbingStairs(int *cost, int n) {
    long long prev2 = 0, prev1 = 0;
    for (int i = 2; i <= n; i++) {
        long long cur = (prev1 + cost[i - 1] < prev2 + cost[i - 2] ? prev1 + cost[i - 1] : prev2 + cost[i - 2]);
        prev2 = prev1;
        prev1 = cur;
    }
    return (int) prev1;
}   // O(n) time · O(1) space
""",
    "best-time-to-buy-and-sell-stock": r"""
// Track the cheapest price seen so far and the best profit so far.
int maxProfit(const int *prices, int n) {
    int best = 0, lowest = INT_MAX;
    for (int i = 0; i < n; i++) {
        if (prices[i] < lowest) lowest = prices[i];
        else if (prices[i] - lowest > best) best = prices[i] - lowest;
    }
    return best;
}   // O(n) time · O(1) space
""",
    "pascals-triangle": r"""
// Each row is built from the previous one; row[i] = prev[i - 1] + prev[i].
int **generate(int numRows, int *returnSize, int **returnColumnSizes) {
    int **rows = malloc(sizeof(int *) * (size_t) numRows);
    *returnColumnSizes = malloc(sizeof(int) * (size_t) numRows);
    for (int r = 0; r < numRows; r++) {
        rows[r] = calloc((size_t) (r + 1), sizeof(int));
        rows[r][0] = rows[r][r] = 1;
        for (int c = 1; c < r; c++) rows[r][c] = rows[r - 1][c - 1] + rows[r - 1][c];
        (*returnColumnSizes)[r] = r + 1;
    }
    *returnSize = numRows;
    return rows;
}   // O(numRows^2) time · O(numRows^2) space
""",
    "divisor-game": r"""
// A number is winning exactly when it is even.
int divisorGame(int n) { return n % 2 == 0; }
// O(1) time · O(1) space
""",
    "maximum-subarray": r"""
// Kadane: extend the run while it helps, otherwise start again here.
int maxSubArray(const int *a, int n) {
    long long best = LLONG_MIN, here = 0;
    for (int i = 0; i < n; i++) {
        here = here > 0 ? here + a[i] : a[i];
        if (here > best) best = here;
    }
    return (int) best;
}   // O(n) time · O(1) space
""",
    "house-robber": r"""
// dp[i] = max(dp[i-1], dp[i-2] + value) — only two values are needed.
int rob(const int *a, int n) {
    long long prev2 = 0, prev1 = 0;
    for (int i = 0; i < n; i++) {
        long long cur = prev2 + a[i] > prev1 ? prev2 + a[i] : prev1;
        prev2 = prev1;
        prev1 = cur;
    }
    return (int) prev1;
}   // O(n) time · O(1) space
""",
    "coin-change": r"""
// Unbounded knapsack: dp[amount] = fewest coins for that amount.
int coinChange(const int *coins, int n, int amount) {
    const int INF = INT_MAX / 4;
    int *dp = malloc(sizeof(int) * (size_t) (amount + 1));
    for (int i = 0; i <= amount; i++) dp[i] = INF;
    dp[0] = 0;
    for (int c = 0; c < n; c++)
        for (int a = coins[c]; a <= amount; a++)
            if (dp[a - coins[c]] + 1 < dp[a]) dp[a] = dp[a - coins[c]] + 1;
    int result = dp[amount] >= INF ? -1 : dp[amount];
    free(dp);
    return result;
}   // O(n * amount) time · O(amount) space
""",
    "coin-change-ii": r"""
// Count combinations: loop coins outside the amount so order does not create duplicates.
int change(int amount, const int *coins, int n) {
    long long *dp = calloc((size_t) amount + 1, sizeof(long long));
    dp[0] = 1;
    for (int c = 0; c < n; c++)
        for (int a = coins[c]; a <= amount; a++)
            dp[a] += dp[a - coins[c]];
    int result = (int) dp[amount];
    free(dp);
    return result;
}   // O(n * amount) time · O(amount) space
""",
    "unique-paths": r"""
// paths on a grid: row[i] += row[i-1] as you move right, row by row.
int uniquePaths(int rows, int cols) {
    long long *dp = malloc(sizeof(long long) * (size_t) cols);
    for (int c = 0; c < cols; c++) dp[c] = 1;             // the first row has exactly one path
    for (int r = 1; r < rows; r++)
        for (int c = 1; c < cols; c++) dp[c] += dp[c - 1];
    int result = (int) dp[cols - 1];
    free(dp);
    return result;
}   // O(rows * cols) time · O(cols) space
""",
    "decode-ways": r"""
// One digit or two digits: dp[i] = dp[i-1] + dp[i-2] when the pair is valid.
int numDecodings(const char *s) {
    int n = (int) strlen(s);
    if (!n || s[0] == '0') return 0;
    long long prev2 = 1, prev1 = 1;
    for (int i = 1; i < n; i++) {
        long long cur = 0;
        if (s[i] != '0') cur += prev1;                    // take one digit
        int pair = (s[i - 1] - '0') * 10 + (s[i] - '0');
        if (pair >= 10 && pair <= 26) cur += prev2;       // take two digits
        prev2 = prev1;
        prev1 = cur;
    }
    return (int) prev1;
}   // O(n) time · O(1) space
""",
    "word-break": r"""
// dp[i] is true when the prefix of length i can be split into dictionary words.
int wordBreak(const char *s, char **dict, int dictCount) {
    int n = (int) strlen(s);
    char *dp = calloc((size_t) n + 1, 1);
    dp[0] = 1;
    for (int i = 1; i <= n; i++)
        for (int j = 0; j < i && !dp[i]; j++) {
            if (!dp[j]) continue;
            int len = i - j;
            for (int w = 0; w < dictCount; w++)
                if ((int) strlen(dict[w]) == len && !strncmp(s + j, dict[w], (size_t) len)) { dp[i] = 1; break; }
        }
    int result = dp[n];
    free(dp);
    return result;
}   // O(n^2 * words) time · O(n) space
""",
    "house-robber-ii": r"""
// The houses form a ring, so the first and last cannot both be taken: solve both halves.
static int robLine(const int *a, int n) {
    long long prev2 = 0, prev1 = 0;
    for (int i = 0; i < n; i++) {
        long long cur = (prev2 + a[i] > prev1) ? prev2 + a[i] : prev1;
        prev2 = prev1;
        prev1 = cur;
    }
    return (int) prev1;
}

int robII(const int *a, int n) {
    if (n == 1) return a[0];
    int skipLast = robLine(a, n - 1);                     // take house 0, leave the last
    int skipFirst = robLine(a + 1, n - 1);                // leave house 0
    return skipLast > skipFirst ? skipLast : skipFirst;
}   // O(n) time · O(1) space
""",
    "target-sum": r"""
// A "+" subset and a "-" subset: finding them is a subset-sum with target (total + target) / 2.
int findTargetSumWays(const int *a, int n, int target) {
    long long total = 0;
    for (int i = 0; i < n; i++) total += a[i];
    if (total < llabs(target) || (total + target) % 2) return 0;
    long long want = (total + target) / 2;
    long long *dp = calloc((size_t) want + 1, sizeof(long long));
    dp[0] = 1;
    for (int i = 0; i < n; i++)
        for (long long s = want; s >= a[i]; s--) dp[s] += dp[s - a[i]];
    int result = (int) dp[want];
    free(dp);
    return result;
}   // O(n * total) time · O(total) space
""",
    "partition-equal-subset-sum": r"""
// Pick a subset with sum total / 2 — the classic 0/1 knapsack seen backwards.
int canPartition(const int *a, int n) {
    long long total = 0;
    for (int i = 0; i < n; i++) total += a[i];
    if (total % 2) return 0;
    long long half = total / 2;
    char *dp = calloc((size_t) half + 1, 1);
    dp[0] = 1;
    for (int i = 0; i < n; i++)
        for (long long s = half; s >= a[i]; s--)
            if (dp[s - a[i]]) dp[s] = 1;
    int result = dp[half];
    free(dp);
    return result;
}   // O(n * total) time · O(total) space
""",
    "longest-common-subsequence": r"""
// dp[i][j] is the LCS of the two prefixes; one row is enough.
int longestCommonSubsequence(const char *a, const char *b) {
    int n = (int) strlen(b);
    int *dp = calloc((size_t) n + 1, sizeof(int));
    for (int i = 1; a[i - 1]; i++) {
        int diagonal = 0;                                 // dp[i-1][j-1] before it is overwritten
        for (int j = 1; j <= n; j++) {
            int saved = dp[j];
            if (a[i - 1] == b[j - 1]) dp[j] = diagonal + 1;
            else dp[j] = dp[j] > dp[j - 1] ? dp[j] : dp[j - 1];
            diagonal = saved;
        }
    }
    int result = dp[n];
    free(dp);
    return result;
}   // O(n * m) time · O(m) space
""",
    "edit-distance": r"""
// Insert, delete or replace: dp[i][j] = 1 + min of the three neighbours.
int minDistance(const char *word1, const char *word2) {
    int n = (int) strlen(word1), m = (int) strlen(word2);
    int *dp = malloc(sizeof(int) * (size_t) (m + 1));
    for (int j = 0; j <= m; j++) dp[j] = j;               // turning "" into a prefix
    for (int i = 1; i <= n; i++) {
        int diagonal = dp[0];
        dp[0] = i;                                        // turning a prefix into ""
        for (int j = 1; j <= m; j++) {
            int saved = dp[j];
            if (word1[i - 1] == word2[j - 1]) dp[j] = diagonal;
            else {
                int best = diagonal < dp[j] ? diagonal : dp[j];
                if (dp[j - 1] < best) best = dp[j - 1];
                dp[j] = best + 1;
            }
            diagonal = saved;
        }
    }
    int result = dp[m];
    free(dp);
    return result;
}   // O(n * m) time · O(m) space
""",
    "longest-increasing-path-in-a-matrix": r"""
// Memoised depth-first search: the best path from a cell is 1 plus the best neighbour.
static int walk(int rows, int cols, int **m, int **memo, int r, int c) {
    if (memo[r][c]) return memo[r][c];
    int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1}, best = 1;
    for (int k = 0; k < 4; k++) {
        int nr = r + dr[k], nc = c + dc[k];
        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
        if (m[nr][nc] <= m[r][c]) continue;                // must be strictly increasing
        int len = 1 + walk(rows, cols, m, memo, nr, nc);
        if (len > best) best = len;
    }
    memo[r][c] = best;
    return best;
}

int longestIncreasingPath(int rows, int cols, int **matrix) {
    int **memo = malloc(sizeof(int *) * (size_t) rows);
    for (int r = 0; r < rows; r++) memo[r] = calloc((size_t) cols, sizeof(int));
    int best = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) {
            int len = walk(rows, cols, matrix, memo, r, c);
            if (len > best) best = len;
        }
    for (int r = 0; r < rows; r++) free(memo[r]);
    free(memo);
    return best;
}   // O(rows * cols) time · O(rows * cols) space
""",
    "number-of-longest-increasing-subsequence": r"""
// Keep both the best length ending at i and how many ways reach it.
int findNumberOfLIS(const int *a, int n) {
    int *len = malloc(sizeof(int) * (size_t) n), *count = malloc(sizeof(int) * (size_t) n);
    int bestLen = 1;
    for (int i = 0; i < n; i++) { len[i] = 1; count[i] = 1; }
    for (int i = 1; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (a[j] >= a[i]) continue;
            if (len[j] + 1 > len[i]) { len[i] = len[j] + 1; count[i] = count[j]; }
            else if (len[j] + 1 == len[i]) count[i] += count[j];   // another way to the same length
        }
        if (len[i] > bestLen) bestLen = len[i];
    }
    long long total = 0;
    for (int i = 0; i < n; i++) if (len[i] == bestLen) total += count[i];
    free(len); free(count);
    return (int) total;
}   // O(n^2) time · O(n) space
""",
    "best-time-to-buy-and-sell-stock-iv": r"""
// dp[k][0] = best with k transactions and no stock held, dp[k][1] = while holding.
int maxProfitIV(int k, const int *prices, int n) {
    if (k > n / 2) {                                      // unlimited transactions
        long long profit = 0;
        for (int i = 1; i < n; i++) if (prices[i] > prices[i - 1]) profit += prices[i] - prices[i - 1];
        return (int) profit;
    }
    long long *hold = malloc(sizeof(long long) * (size_t) (k + 1));
    long long *free_ = calloc((size_t) k + 1, sizeof(long long));
    for (int i = 0; i <= k; i++) hold[i] = LLONG_MIN / 4;
    for (int i = 0; i < n; i++) {
        for (int t = k; t >= 1; t--) {
            if (free_[t - 1] - prices[i] > hold[t]) hold[t] = free_[t - 1] - prices[i];   // buy
            if (hold[t] + prices[i] > free_[t]) free_[t] = hold[t] + prices[i];           // sell
        }
    }
    int result = (int) free_[k];
    free(hold); free(free_);
    return result;
}   // O(n * k) time · O(k) space
""",
    "frog-jump": r"""
// Reachability per stone per jump length, propagated forwards.
int canCross(const int *stones, int n) {
    if (n == 0 || stones[1] != 1) return 0;               // the first jump must be exactly 1
    char **reach = malloc(sizeof(char *) * (size_t) n);
    for (int i = 0; i < n; i++) reach[i] = calloc((size_t) n + 1, 1);
    reach[0][0] = 1;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            long long gap = (long long) stones[j] - stones[i];
            if (gap > n) break;
            for (int step = 0; step <= n; step++) {
                if (!reach[i][step]) continue;
                if (llabs(step - gap) <= 1) reach[j][(int) gap] = 1;   // jump gap from stone i
            }
        }
    }
    int ok = 0;
    for (int step = 0; step <= n && !ok; step++) if (reach[n - 1][step]) ok = 1;
    for (int i = 0; i < n; i++) free(reach[i]);
    free(reach);
    return ok;
}   // O(n^2) time · O(n^2) space
""",
    "distinct-subsequences": r"""
// dp[j] = number of ways to build t's prefix of length j so far.
int numDistinct(const char *s, const char *t) {
    int m = (int) strlen(t);
    unsigned long long *dp = calloc((size_t) m + 1, sizeof(unsigned long long));
    dp[0] = 1;
    for (int i = 0; s[i]; i++)
        for (int j = m; j >= 1; j--)                      // backwards: each s[i] is used once
            if (s[i] == t[j - 1]) dp[j] += dp[j - 1];
    int result = (int) dp[m];
    free(dp);
    return result;
}   // O(n * m) time · O(m) space
""",
    "regular-expression-matching": r"""
// '.' matches any character, '*' repeats the previous token zero or more times.
int isMatch(const char *s, const char *p) {
    int n = (int) strlen(s), m = (int) strlen(p);
    char **dp = malloc(sizeof(char *) * (size_t) (n + 1));
    for (int i = 0; i <= n; i++) dp[i] = calloc((size_t) m + 1, 1);
    dp[0][0] = 1;
    for (int j = 2; j <= m; j++) if (p[j - 1] == '*') dp[0][j] = dp[0][j - 2];   // "a*" matches ""
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++) {
            if (p[j - 1] == '*') {
                char prev = p[j - 2];
                dp[i][j] = dp[i][j - 2];                  // use zero copies
                if (prev == '.' || prev == s[i - 1]) dp[i][j] |= dp[i - 1][j];   // one more copy
            } else if (p[j - 1] == '.' || p[j - 1] == s[i - 1]) {
                dp[i][j] = dp[i - 1][j - 1];
            }
        }
    int result = dp[n][m];
    for (int i = 0; i <= n; i++) free(dp[i]);
    free(dp);
    return result;
}   // O(n * m) time · O(n * m) space
""",
    "wildcard-matching": r"""
// '?' matches one character, '*' matches any run (greedy with backtracking).
int isMatchWild(const char *s, const char *p) {
    int i = 0, j = 0, star = -1, match = 0;
    while (s[i]) {
        if (p[j] == '?' || p[j] == s[i]) { i++; j++; }
        else if (p[j] == '*') { star = j++; match = i; }   // remember where to resume
        else if (star >= 0) { j = star + 1; i = ++match; } // let the star eat one more character
        else return 0;
    }
    while (p[j] == '*') j++;
    return p[j] == '\0';
}   // O(n * m) worst case · O(1) space
""",
    "palindrome-partitioning-ii": r"""
// dp[i] = fewest cuts for the first i characters; every palindromic suffix improves it.
int minCut(const char *s) {
    int n = (int) strlen(s);
    int *dp = malloc(sizeof(int) * (size_t) (n + 1));
    for (int i = 0; i <= n; i++) dp[i] = i - 1;           // one cut per character, at worst
    for (int centre = 0; centre < n; centre++) {
        for (int radius = 0; centre - radius >= 0 && centre + radius < n; radius++) {
            if (s[centre - radius] != s[centre + radius]) break;         // odd palindrome
            int left = centre - radius;
            if (dp[left] + 1 < dp[centre + radius + 1]) dp[centre + radius + 1] = dp[left] + 1;
        }
        for (int radius = 0; centre - radius >= 0 && centre + radius + 1 < n; radius++) {
            if (s[centre - radius] != s[centre + radius + 1]) break;     // even palindrome
            int left = centre - radius;
            if (dp[left] + 1 < dp[centre + radius + 2]) dp[centre + radius + 2] = dp[left] + 1;
        }
    }
    int result = dp[n];
    free(dp);
    return result;
}   // O(n^2) time · O(n) space
""",
    "burst-balloons": r"""
// dp[i][j] = best score for bursting everything strictly between i and j.
int maxCoins(const int *nums, int n) {
    int *a = malloc(sizeof(int) * (size_t) (n + 2));
    a[0] = a[n + 1] = 1;                                  // virtual balloons at both ends
    for (int i = 0; i < n; i++) a[i + 1] = nums[i];
    int size = n + 2;
    int **dp = malloc(sizeof(int *) * (size_t) size);
    for (int i = 0; i < size; i++) dp[i] = calloc((size_t) size, sizeof(int));
    for (int width = 2; width < size; width++)
        for (int left = 0; left + width < size; left++) {
            int right = left + width;
            for (int last = left + 1; last < right; last++) {          // the last one burst here
                int score = dp[left][last] + a[left] * a[last] * a[right] + dp[last][right];
                if (score > dp[left][right]) dp[left][right] = score;
            }
        }
    int result = dp[0][size - 1];
    for (int i = 0; i < size; i++) free(dp[i]);
    free(dp); free(a);
    return result;
}   // O(n^3) time · O(n^2) space
""",
    "minimum-cost-to-cut-a-stick": r"""
// Same interval DP as burst balloons, over the sorted cut positions.
static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}

int minCost(int n, int *cuts, int cutCount) {
    qsort(cuts, (size_t) cutCount, sizeof(int), cmpInt);
    int size = cutCount + 2;
    int *pos = malloc(sizeof(int) * (size_t) size);
    pos[0] = 0;
    pos[size - 1] = n;
    for (int i = 0; i < cutCount; i++) pos[i + 1] = cuts[i];
    int **dp = malloc(sizeof(int *) * (size_t) size);
    for (int i = 0; i < size; i++) dp[i] = calloc((size_t) size, sizeof(int));
    for (int width = 2; width < size; width++)
        for (int left = 0; left + width < size; left++) {
            int right = left + width, best = INT_MAX;
            for (int mid = left + 1; mid < right; mid++) {             // the first cut made here
                int cost = dp[left][mid] + dp[mid][right];
                if (cost < best) best = cost;
            }
            dp[left][right] = best + pos[right] - pos[left];           // paying for this piece
        }
    int result = dp[0][size - 1];
    for (int i = 0; i < size; i++) free(dp[i]);
    free(dp); free(pos);
    return result;
}   // O(cuts^3) time · O(cuts^2) space
""",
    "cherry-pickup": r"""
// Two walkers move down together, so one DP over (row, column of each) covers both.
int cherryPickup(int n, int **grid) {
    const int NEG = -1000000;
    int ***dp = malloc(sizeof(int **) * (size_t) (n + 1));
    for (int r = 0; r <= n; r++) {
        dp[r] = malloc(sizeof(int *) * (size_t) (n + 1));
        for (int c = 0; c <= n; c++) dp[r][c] = calloc((size_t) n + 1, sizeof(int));
    }
    for (int r1 = n; r1 >= 1; r1--)
        for (int c1 = n; c1 >= 1; c1--)
            for (int c2 = n; c2 >= 1; c2--) {
                int r2 = r1 + c1 - c2;                    // both walkers take the same number of steps
                if (r2 < 1 || r2 > n) { dp[r1][c1][c2] = NEG; continue; }
                if (grid[r1 - 1][c1 - 1] == -1 || grid[r2 - 1][c2 - 1] == -1) { dp[r1][c1][c2] = NEG; continue; }
                int cherries = grid[r1 - 1][c1 - 1];
                if (r1 != r2 || c1 != c2) cherries += grid[r2 - 1][c2 - 1];   // shared cells count once
                int best = 0;
                if (r1 + 1 <= n || c1 + 1 <= n) {
                    int candidates[4] = {dp[r1 + 1][c1][c2], dp[r1 + 1][c1][c2 + 1],
                                         dp[r1][c1 + 1][c2], dp[r1][c1 + 1][c2 + 1]};
                    best = NEG;
                    for (int k = 0; k < 4; k++) if (candidates[k] > best) best = candidates[k];
                }
                dp[r1][c1][c2] = cherries + best;
            }
    int result = dp[1][1][1] < 0 ? 0 : dp[1][1][1];
    for (int r = 0; r <= n; r++) {
        for (int c = 0; c <= n; c++) free(dp[r][c]);
        free(dp[r]);
    }
    free(dp);
    return result;
}   // O(n^3) time · O(n^3) space
""",
    "maximum-profit-in-job-scheduling": r"""
// Sort the jobs by end time and binary search the last job that finishes before each starts.
struct Job { int start, end, profit; };

static int cmpJob(const void *x, const void *y) {
    const struct Job *a = x, *b = y;
    return a->end - b->end;
}

int jobScheduling(int *start, int n, int *end, int *profit) {
    struct Job *jobs = malloc(sizeof(struct Job) * (size_t) n);
    for (int i = 0; i < n; i++) { jobs[i].start = start[i]; jobs[i].end = end[i]; jobs[i].profit = profit[i]; }
    qsort(jobs, (size_t) n, sizeof(struct Job), cmpJob);
    int *dp = calloc((size_t) n + 1, sizeof(int));
    for (int i = 1; i <= n; i++) {
        int lo = 0, hi = i - 1, previous = -1;
        while (lo <= hi) {                                // last job that ends before this one starts
            int mid = (lo + hi) / 2;
            if (jobs[mid].end <= jobs[i - 1].start) { previous = mid; lo = mid + 1; }
            else hi = mid - 1;
        }
        int take = jobs[i - 1].profit + (previous >= 0 ? dp[previous + 1] : 0);
        dp[i] = take > dp[i - 1] ? take : dp[i - 1];
    }
    int result = dp[n];
    free(jobs); free(dp);
    return result;
}   // O(n log n) time · O(n) space
""",
}
