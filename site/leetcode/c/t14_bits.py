# Topic 14 · Bit Manipulation — C17 solutions
#
# Three identities carry most of these: x ^ x == 0, x & (x - 1) clears the lowest set bit,
# and x ^ (x >> 1) is the Gray code. Unsigned types matter: shifting a signed value is
# undefined behaviour in C, so the solutions below shift `unsigned`.

CODE = {
    "single-number": r"""
// XOR of everything: the pairs cancel, the odd one out survives.
int singleNumber(const int *nums, int n) {
    int result = 0;
    for (int i = 0; i < n; i++) result ^= nums[i];
    return result;
}   // O(n) time · O(1) space
""",
    "number-of-1-bits": r"""
// x & (x - 1) removes the lowest set bit, so the loop runs once per set bit.
int hammingWeight(unsigned n) {
    int count = 0;
    while (n) { n &= n - 1; count++; }
    return count;
}   // O(number of set bits) time · O(1) space
""",
    "hamming-distance": r"""
// XOR marks the differing bits; count them.
int hammingDistance(unsigned x, unsigned y) {
    unsigned diff = x ^ y;
    int count = 0;
    while (diff) { diff &= diff - 1; count++; }
    return count;
}   // O(bits) time · O(1) space
""",
    "reverse-bits": r"""
// Pull bits off the right and push them onto the left.
unsigned reverseBits(unsigned n) {
    unsigned result = 0;
    for (int i = 0; i < 32; i++) {
        result = (result << 1) | (n & 1);
        n >>= 1;
    }
    return result;
}   // O(32) time · O(1) space
""",
    "counting-bits": r"""
// dp[i] = dp[i >> 1] + (i & 1): the answer for half the number, plus its last bit.
int *countBits(int n, int *returnSize) {
    int *out = calloc((size_t) n + 1, sizeof(int));
    for (int i = 1; i <= n; i++) out[i] = out[i >> 1] + (i & 1);
    *returnSize = n + 1;
    return out;
}   // O(n) time · O(n) space
""",
    "power-of-four": r"""
// A power of four is a power of two whose single 1 bit sits at an even position.
int isPowerOfFour(int n) {
    return n > 0 && (n & (n - 1)) == 0 && (n & 0x55555555) != 0;
}   // O(1) time · O(1) space
""",
    "single-number-ii": r"""
// Count each bit modulo 3 with two accumulators — the standard bit-trick circuit.
int singleNumberII(const int *nums, int n) {
    unsigned ones = 0, twos = 0;
    for (int i = 0; i < n; i++) {
        ones = (ones ^ (unsigned) nums[i]) & ~twos;
        twos = (twos ^ (unsigned) nums[i]) & ~ones;
    }
    return (int) ones;
}   // O(n) time · O(1) space
""",
    "single-number-iii": r"""
// XOR everything to get a ^ b, split on any set bit, then XOR each group.
int *singleNumberIII(const int *nums, int n, int *returnSize) {
    unsigned all = 0;
    for (int i = 0; i < n; i++) all ^= (unsigned) nums[i];
    unsigned lowestBit = all & (~all + 1);                   // any bit where the two differ
    int first = 0, second = 0;
    for (int i = 0; i < n; i++) {
        if ((unsigned) nums[i] & lowestBit) first ^= nums[i];
        else second ^= nums[i];
    }
    int *out = malloc(sizeof(int) * 2);
    out[0] = first;
    out[1] = second;
    *returnSize = 2;
    return out;
}   // O(n) time · O(1) space
""",
    "bitwise-and-of-numbers-range": r"""
// The common prefix of left and right: shift both until they meet.
int rangeBitwiseAnd(int left, int right) {
    unsigned shift = 0;
    unsigned a = (unsigned) left, b = (unsigned) right;
    while (a != b) { a >>= 1; b >>= 1; shift++; }
    return (int) (a << shift);
}   // O(bits) time · O(1) space
""",
    "sum-of-two-integers": r"""
// Addition without "+": XOR adds the digits, AND shifted carries them.
int getSum(int a, int b) {
    while (b) {
        unsigned carry = (unsigned) (a & b) << 1;
        a = a ^ b;
        b = (int) carry;
    }
    return a;
}   // O(bits) time · O(1) space
""",
    "total-hamming-distance": r"""
// Each bit contributes ones * zeros pairs across all numbers.
int totalHammingDistance(const int *nums, int n) {
    long long total = 0;
    for (int bit = 0; bit < 32; bit++) {
        int ones = 0;
        for (int i = 0; i < n; i++) if ((unsigned) nums[i] >> bit & 1) ones++;
        total += (long long) ones * (n - ones);
    }
    return (int) total;
}   // O(32 * n) time · O(1) space
""",
    "divide-two-integers": r"""
// Long division in binary: subtract the largest shifted divisor each time.
int divide(int dividend, int divisor) {
    if (dividend == INT_MIN && divisor == -1) return INT_MAX;   // the one overflowing case
    long long a = llabs((long long) dividend), b = llabs((long long) divisor);
    long long quotient = 0;
    while (a >= b) {
        long long shifted = b, multiple = 1;
        while ((shifted << 1) <= a) { shifted <<= 1; multiple <<= 1; }
        a -= shifted;
        quotient += multiple;
    }
    int negative = (dividend < 0) != (divisor < 0);
    long long result = negative ? -quotient : quotient;
    if (result > INT_MAX) return INT_MAX;
    if (result < INT_MIN) return INT_MIN;
    return (int) result;
}   // O(log^2 n) time · O(1) space
""",
    "score-after-flipping-matrix": r"""
// Flip rows so the first column is all 1s, then flip columns with more 0s than 1s.
int matrixScore(int rows, int cols, int **grid) {
    for (int r = 0; r < rows; r++)
        if (!grid[r][0])                                    // top-left bit is the most valuable
            for (int c = 0; c < cols; c++) grid[r][c] ^= 1;
    int total = 0;
    for (int c = 0; c < cols; c++) {
        int ones = 0;
        for (int r = 0; r < rows; r++) ones += grid[r][c];
        int best = ones > rows - ones ? ones : rows - ones;
        total += best << (cols - 1 - c);                    // the column's worth as a number
    }
    return total;
}   // O(rows * cols) time · O(1) space
""",
    "minimum-flips-to-make-a-or-b-equal-to-c": r"""
// Per bit: (a|b) must equal c, and only bits that are 0 in c may be changed at all.
int minFlips(int a, int b, int c) {
    int flips = 0;
    for (int bit = 0; bit < 31; bit++) {
        int abit = (a >> bit) & 1, bbit = (b >> bit) & 1, cbit = (c >> bit) & 1;
        if (cbit == 0) {
            if (abit) flips++;
            if (bbit) flips++;
        } else if (!abit && !bbit) {
            flips++;                                        // one of them must become 1
        }
    }
    return flips;
}   // O(32) time · O(1) space
""",
    "maximum-xor-of-two-numbers-in-an-array": r"""
// Build the answer bit by bit, testing whether some prefix pair reaches the goal.
int findMaximumXOR(const int *nums, int n) {
    int best = 0;
    for (int bit = 30; bit >= 0; bit--) {
        int goal = best | (1 << bit), found = 0;            // try to turn this bit on
        for (int i = 0; i < n && !found; i++)
            for (int j = 0; j < n && !found; j++)
                if (((nums[i] ^ nums[j]) & goal) == goal) found = 1;
        if (found) best = goal;
    }
    return best;
}   // O(31 * n^2) time (a trie gives O(31 * n)) · O(1) space
""",
    "find-kth-bit-in-nth-binary-string": r"""
// S(n) = S(n-1) + '1' + reverse(flip(S(n-1))): walk down to the first half, the middle, or
// the mirrored second half.
int findKthBit(int n, int k) {
    if (n == 1) return 0;
    int length = (1 << (n - 1)) - 1;                        // length of the first half
    if (k == length + 1) return 1;                          // the middle '1'
    if (k <= length) return findKthBit(n - 1, k);
    return 1 - findKthBit(n - 1, 2 * (length + 1) - k);     // mirrored and flipped
}   // O(n) time · O(n) recursion
""",
    "maximum-product-of-word-lengths": r"""
// A 26-bit mask per word: two words are disjoint when the AND is zero.
int maxProduct(char **words, int n) {
    unsigned *masks = malloc(sizeof(unsigned) * (size_t) n);
    int *lengths = malloc(sizeof(int) * (size_t) n);
    for (int i = 0; i < n; i++) {
        unsigned mask = 0;
        for (int j = 0; words[i][j]; j++) mask |= 1u << (words[i][j] - 'a');
        masks[i] = mask;
        lengths[i] = (int) strlen(words[i]);
    }
    int best = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (!(masks[i] & masks[j]) && lengths[i] * lengths[j] > best)
                best = lengths[i] * lengths[j];
    free(masks); free(lengths);
    return best;
}   // O(26 * n + n^2) time · O(n) space
""",
    "check-if-a-string-contains-all-binary-codes-of-size-k": r"""
// Slide a window of k bits and remember which codes have been seen.
int hasAllCodes(const char *s, int k) {
    int n = (int) strlen(s);
    int total = 1 << k;
    char *seen = calloc((size_t) total, 1);
    int distinct = 0;
    for (int i = 0; i + k <= n; i++) {
        int code = 0;
        for (int j = 0; j < k; j++) code = code << 1 | (s[i + j] - '0');
        if (!seen[code]) { seen[code] = 1; distinct++; }
    }
    free(seen);
    return distinct == total;
}   // O(n * k) time · O(2^k) space
""",
    "minimum-number-of-k-consecutive-bit-flips": r"""
// A sliding window of flips: track how many active flips cover the current position.
int minKBitFlips(int *nums, int n, int k) {
    int *flipStart = calloc((size_t) n + 1, sizeof(int));
    int active = 0, flips = 0;
    for (int i = 0; i < n; i++) {
        active ^= flipStart[i];                             // a flip that started earlier ends here
        if ((nums[i] ^ active) == 0) {                      // this bit needs flipping
            if (i + k > n) { free(flipStart); return -1; }  // the window would run off the end
            flips++;
            active ^= 1;
            flipStart[i + k] ^= 1;                          // remember when it stops mattering
        }
    }
    free(flipStart);
    return flips;
}   // O(n) time · O(n) space
""",
    "minimum-number-of-flips-to-convert-binary-matrix-to-zero-matrix": r"""
// BFS over bitmask states: from all-zero, flipping a cell flips its neighbours too.
int minFlips(int rows, int cols, int **mat) {
    int total = rows * cols;
    int start = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            if (mat[r][c]) start |= 1 << (r * cols + c);
    if (!start) return 0;
    int *distance = malloc(sizeof(int) * (size_t) (1 << total));
    for (int i = 0; i < (1 << total); i++) distance[i] = -1;
    int *queue = malloc(sizeof(int) * (size_t) (1 << total));
    int head = 0, tail = 0;
    distance[start] = 0;
    queue[tail++] = start;
    int dr[5] = {0, 1, -1, 0, 0}, dc[5] = {0, 0, 0, 1, -1};
    while (head < tail) {
        int state = queue[head++];
        if (state == 0) {                                   // solved: the state is all zeros
            int answer = distance[state];
            free(distance); free(queue);
            return answer;
        }
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                int next = state;
                for (int k = 0; k < 5; k++) {               // the cell plus its four neighbours
                    int nr = r + dr[k], nc = c + dc[k];
                    if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                    next ^= 1 << (nr * cols + nc);
                }
                if (distance[next] < 0) {
                    distance[next] = distance[state] + 1;
                    queue[tail++] = next;
                }
            }
    }
    free(distance); free(queue);
    return -1;
}   // O(2^(rows * cols) * rows * cols) time · O(2^(rows * cols)) space
""",
    "number-of-valid-words-for-each-puzzle": r"""
// Both words and puzzles become 26-bit masks; a puzzle contains a word when the word's
// mask is a subset and it shares the first letter.
int *findNumOfValidWords(char **words, int wordCount, char **puzzles, int puzzleCount, int *returnSize) {
    unsigned *wordMasks = malloc(sizeof(unsigned) * (size_t) wordCount);
    for (int i = 0; i < wordCount; i++) {
        unsigned mask = 0;
        for (int j = 0; words[i][j]; j++) mask |= 1u << (words[i][j] - 'a');
        wordMasks[i] = mask;
    }
    int *out = malloc(sizeof(int) * (size_t) puzzleCount);
    for (int p = 0; p < puzzleCount; p++) {
        unsigned puzzleMask = 0;
        for (int j = 0; puzzles[p][j]; j++) puzzleMask |= 1u << (puzzles[p][j] - 'a');
        unsigned first = 1u << (puzzles[p][0] - 'a');
        int count = 0;
        for (int i = 0; i < wordCount; i++) {
            unsigned mask = wordMasks[i];
            if ((mask & first) && (mask & puzzleMask) == mask) count++;
        }
        out[p] = count;
    }
    free(wordMasks);
    *returnSize = puzzleCount;
    return out;
}   // O(words * puzzles * length) time · O(words) space
""",
    "minimum-one-bit-operations-to-make-integers-zero": r"""
// Gray-code distance: n -> n - 1 when n is odd, n + 1 when even shrinking is possible.
int minimumOneBitOperations(int n) {
    int answer = 0;
    while (n) {
        answer ^= n;                                        // the inverse Gray code
        n >>= 1;
    }
    return answer;
}   // O(bits) time · O(1) space
""",
    "find-xor-sum-of-all-pairs-bitwise-and": r"""
// AND before XOR: each bit is set in the result when an odd number of ANDs carry it.
int getXORSum(const int *arr1, int n, const int *arr2, int m) {
    long long xorAll = 0;
    for (int i = 0; i < m; i++) xorAll ^= arr2[i];          // XOR of the second array
    int result = 0;
    for (int i = 0; i < n; i++) result ^= (arr1[i] & (int) xorAll);
    return result;
}   // O(n + m) time · O(1) space
""",
    "number-of-excellent-pairs": r"""
// Pairs count by popcount: two numbers pair well when the total popcount is a power of two.
long long countExcellentPairs(int *nums, int n, int k) {
    int seen[32] = {0};
    int *used = calloc(100001, sizeof(int));
    for (int i = 0; i < n; i++) {
        if (used[nums[i]]) continue;                        // distinct values only
        used[nums[i]] = 1;
        int bits = 0, value = nums[i];
        while (value) { value &= value - 1; bits++; }
        seen[bits]++;
    }
    long long total = 0;
    for (int a = 0; a < 32; a++)
        for (int b = 0; b < 32; b++)
            if (a + b >= k && (a + b) & ((a + b) - 1) == 0) total += (long long) seen[a] * seen[b];
    free(used);
    return total;
}   // O(n + 32^2) time · O(n) space
""",
    "kth-smallest-instructions": r"""
// Count the sequences starting with 'H' using binomials, and walk the string from the left.
long long binomial(int n, int r) {
    long long result = 1;
    if (r > n - r) r = n - r;
    for (int i = 1; i <= r; i++) {
        result = result * (n - r + i) / i;                  // exact: no overflow for n <= 30
    }
    return result;
}

char *kthSmallestPath(int *destination, int k) {
    int rows = destination[0], cols = destination[1];
    int total = rows + cols;
    char *out = malloc((size_t) total + 1);
    int h = cols, v = rows;
    for (int i = 0; i < total; i++) {
        if (h == 0) { out[i] = 'V'; v--; continue; }
        long long withH = binomial(h + v - 1, h - 1);       // paths that start with 'H'
        if (k <= withH) { out[i] = 'H'; h--; }
        else { out[i] = 'V'; k -= (int) withH; v--; }
    }
    out[total] = '\0';
    return out;
}   // O(rows + cols) time · O(1) space
""",
    "maximum-xor-with-an-element-from-array": r"""
// Sort the array and the queries by limit, inserting numbers into a trie as they qualify.
typedef struct BitNode { struct BitNode *child[2]; } BitNode;

static void insertBits(BitNode *root, int value) {
    BitNode *node = root;
    for (int bit = 30; bit >= 0; bit--) {
        int b = (value >> bit) & 1;
        if (!node->child[b]) node->child[b] = calloc(1, sizeof(BitNode));
        node = node->child[b];
    }
}

static int bestXor(BitNode *root, int value) {
    BitNode *node = root;
    int result = 0;
    for (int bit = 30; bit >= 0; bit--) {
        int b = (value >> bit) & 1;
        if (node->child[b ^ 1]) {                       // prefer the opposite bit
            result |= 1 << bit;
            node = node->child[b ^ 1];
        } else node = node->child[b];
    }
    return result;
}

int *maximizeXor(int *nums, int n, int **queries, int queryCount, int *returnSize) {
    int *order = malloc(sizeof(int) * (size_t) n);
    for (int i = 0; i < n; i++) order[i] = i;
    for (int i = 1; i < n; i++)                              // insertion sort by value
        for (int j = i; j > 0 && nums[order[j]] < nums[order[j - 1]]; j--) {
            int t = order[j]; order[j] = order[j - 1]; order[j - 1] = t;
        }
    int *queryOrder = malloc(sizeof(int) * (size_t) queryCount);
    for (int i = 0; i < queryCount; i++) queryOrder[i] = i;
    for (int i = 1; i < queryCount; i++)                     // insertion sort by limit
        for (int j = i; j > 0 && queries[queryOrder[j]][1] < queries[queryOrder[j - 1]][1]; j--) {
            int t = queryOrder[j]; queryOrder[j] = queryOrder[j - 1]; queryOrder[j - 1] = t;
        }
    BitNode *root = calloc(1, sizeof(BitNode));
    int *out = malloc(sizeof(int) * (size_t) queryCount);
    int inserted = 0;
    for (int q = 0; q < queryCount; q++) {
        int index = queryOrder[q];
        while (inserted < n && nums[order[inserted]] <= queries[index][1]) {
            insertBits(root, nums[order[inserted]]);
            inserted++;
        }
        out[index] = inserted ? bestXor(root, queries[index][0]) : -1;
    }
    free(order); free(queryOrder);
    *returnSize = queryCount;
    return out;
}   // O((n + queries) * 31) time · O(n * 31) space
""",
    "count-pairs-with-xor-in-a-range": r"""
// Count pairs with XOR <= value by walking a binary trie of the prefix.
typedef struct CountNode { struct CountNode *child[2]; int count; } CountNode;

static void addPath(CountNode *root, int value) {
    CountNode *node = root;
    node->count++;
    for (int bit = 15; bit >= 0; bit--) {
        int b = (value >> bit) & 1;
        if (!node->child[b]) node->child[b] = calloc(1, sizeof(CountNode));
        node = node->child[b];
        node->count++;
    }
}

static int countBelow(CountNode *root, int value, int limit) {
    CountNode *node = root;
    int total = 0;
    for (int bit = 15; bit >= 0 && node; bit--) {
        int v = (value >> bit) & 1, l = (limit >> bit) & 1;
        if (l) {                                            // XOR bit may be 0 here
            if (node->child[v]) total += node->child[v]->count;
            node = node->child[v ^ 1];                      // and continue with XOR bit 1
        } else {
            node = node->child[v];                          // XOR bit must be 0
        }
    }
    return total;
}

int countPairs(int *nums, int n, int low, int high) {
    CountNode *root = calloc(1, sizeof(CountNode));
    long long total = 0;
    for (int i = 0; i < n; i++) {
        total += countBelow(root, nums[i], high + 1) - countBelow(root, nums[i], low);
        addPath(root, nums[i]);
    }
    return (int) total;
}   // O(n * 16) time · O(n * 16) space
""",
    "maximum-strong-pair-xor-ii": r"""
// Two numbers are strongly paired when their highest differing bits are within 2:
// check the three possible windows of the trie.
typedef struct StrongNode { struct StrongNode *child[2]; } StrongNode;

int maximumStrongPairXor(int *nums, int n) {
    int best = 0;
    for (int bit = 19; bit >= 0; bit--) {
        int goal = best | (1 << bit), found = 0;
        for (int i = 0; i < n && !found; i++)
            for (int j = i + 1; j < n && !found; j++) {
                int a = nums[i], b = nums[j];
                if (abs(a - b) > (a < b ? a : b)) continue;  // must be a strong pair
                if (((a ^ b) & goal) == goal) found = 1;
            }
        if (found) best = goal;
    }
    return best;
}   // O(20 * n^2) time (a trie gives O(20 * n)) · O(1) space
""",
    "smallest-good-base": r"""
// Binary search the number of digits, then the base; long doubles stop the overflow.
char *smallestGoodBase(const char *n) {
    long double target = strtold(n, NULL);
    for (int digits = 63; digits >= 2; digits--) {          // more digits means a smaller base
        long double low = 2.0L, high = target;
        while (low <= high) {
            long double base = floorl((low + high) / 2.0L);
            long double sum = 0, term = 1;
            for (int i = 0; i < digits; i++) { sum += term; term *= base; }
            if (sum == target) {                            // all digits are 1 in this base
                char *result = malloc(32);
                snprintf(result, 32, "%lld", (long long) base);
                return result;
            }
            if (sum < target) low = base + 1;
            else high = base - 1;
        }
    }
    char *result = malloc(32);
    snprintf(result, 32, "%lld", (long long) (target - 1));   // always valid: base n - 1
    return result;
}   // O(63 * log n) time · O(1) space
""",
    "partition-array-into-two-arrays-to-minimize-sum-difference": r"""
// Meet in the middle: all subset sums of each half by count, then pair them up.
int minimumDifference(int *nums, int n) {
    int half = n / 2;
    long long total = 0;
    for (int i = 0; i < n; i++) total += nums[i];
    long long best = LLONG_MAX;
    /* all subset sums of the second half, grouped by how many elements they use */
    int **sums = malloc(sizeof(int *) * (size_t) (half + 1));
    int *counts = calloc((size_t) half + 1, sizeof(int));
    int *capacity = calloc((size_t) half + 1, sizeof(int));
    for (int mask = 0; mask < (1 << half); mask++) {
        long long sum = 0;
        int used = 0;
        for (int i = 0; i < half; i++) if (mask >> i & 1) { sum += nums[half + i]; used++; }
        if (counts[used] == capacity[used]) {
            capacity[used] = capacity[used] ? capacity[used] * 2 : 8;
            sums[used] = realloc(sums[used], sizeof(int) * (size_t) capacity[used]);
        }
        sums[used][counts[used]++] = (int) sum;
    }
    for (int used = 0; used <= half; used++)                 // sorted so we can pair with two pointers
        for (int i = 1; i < counts[used]; i++)
            for (int j = i; j > 0 && sums[used][j] < sums[used][j - 1]; j--) {
                int t = sums[used][j]; sums[used][j] = sums[used][j - 1]; sums[used][j - 1] = t;
            }
    int target = (int) (total / 2);
    for (int mask = 0; mask < (1 << half); mask++) {
        long long sum = 0;
        int used = 0;
        for (int i = 0; i < half; i++) if (mask >> i & 1) { sum += nums[i]; used++; }
        int need = half - used, left = 0, right = counts[need] - 1, pick = -1;
        while (left <= right) {                              // binary search the closest partner
            int mid = (left + right) / 2;
            if (sum + sums[need][mid] <= target) { pick = sums[need][mid]; left = mid + 1; }
            else right = mid - 1;
        }
        if (pick >= 0) {
            long long difference = llabs(total - 2 * (sum + pick));
            if (difference < best) best = difference;
        }
    }
    for (int used = 0; used <= half; used++) free(sums[used]);
    free(sums); free(counts); free(capacity);
    return (int) best;
}   // O(2^(n/2) * n) time · O(2^(n/2)) space
""",
}
