# Topic 16 · Prefix Sums & Range Queries — C17 solutions
#
# prefix[i] = sum of the first i elements, so any range sum is prefix[r] - prefix[l].
# The same idea works for XOR, for counts, and (with a Fenwick tree) for values that change.

CODE = {
    "running-sum-of-1d-array": r"""
// Each answer is the running total at that index.
int *runningSum(const int *nums, int n, int *returnSize) {
    int *out = malloc(sizeof(int) * (size_t) n);
    int total = 0;
    for (int i = 0; i < n; i++) { total += nums[i]; out[i] = total; }
    *returnSize = n;
    return out;
}   // O(n) time · O(n) space
""",
    "range-sum-query-immutable": r"""
// Store the prefix sums once, then every query is one subtraction.
typedef struct { int *prefix, size; } NumArray;

NumArray *numArrayCreate(int *nums, int n) {
    NumArray *a = malloc(sizeof(NumArray));
    a->prefix = calloc((size_t) n + 1, sizeof(int));
    for (int i = 0; i < n; i++) a->prefix[i + 1] = a->prefix[i] + nums[i];
    a->size = n;
    return a;
}

int numArraySumRange(NumArray *a, int left, int right) {
    return a->prefix[right + 1] - a->prefix[left];
}   // O(1) per query after O(n) build · O(n) space
""",
    "find-pivot-index": r"""
// Walk once keeping the left sum; the right sum is total - left - value.
int pivotIndex(const int *nums, int n) {
    long long total = 0;
    for (int i = 0; i < n; i++) total += nums[i];
    long long left = 0;
    for (int i = 0; i < n; i++) {
        if (left == total - left - nums[i]) return i;
        left += nums[i];
    }
    return -1;
}   // O(n) time · O(1) space
""",
    "left-and-right-sum-differences": r"""
// The left and right arrays of running sums, then the absolute differences.
int *leftRightDifference(const int *nums, int n, int *returnSize) {
    int *left = calloc((size_t) n, sizeof(int)), *right = calloc((size_t) n, sizeof(int));
    for (int i = 1; i < n; i++) left[i] = left[i - 1] + nums[i - 1];
    for (int i = n - 2; i >= 0; i--) right[i] = right[i + 1] + nums[i + 1];
    int *out = malloc(sizeof(int) * (size_t) n);
    for (int i = 0; i < n; i++) out[i] = abs(left[i] - right[i]);
    free(left); free(right);
    *returnSize = n;
    return out;
}   // O(n) time · O(n) space
""",
    "minimum-value-to-get-positive-step-by-step-sum": r"""
// The smallest answer is 1 minus the lowest prefix sum.
int minStartValue(const int *nums, int n) {
    int prefix = 0, lowest = 0;
    for (int i = 0; i < n; i++) {
        prefix += nums[i];
        if (prefix < lowest) lowest = prefix;
    }
    return 1 - lowest;
}   // O(n) time · O(1) space
""",
    "maximum-score-after-splitting-a-string": r"""
// Count zeros on the left and ones on the right as the split moves.
int maxScore(const char *s) {
    int total = 0, n = (int) strlen(s);
    for (int i = 0; i < n; i++) if (s[i] == '1') total++;
    int best = 0, zeros = 0, onesRight = total;
    for (int i = 0; i < n - 1; i++) {
        if (s[i] == '0') zeros++;
        else onesRight--;
        if (zeros + onesRight > best) best = zeros + onesRight;
    }
    return best;
}   // O(n) time · O(1) space
""",
    "range-sum-query-2d-immutable": r"""
// A 2-D prefix table: sum(rows 0..r, cols 0..c), four lookups per query.
typedef struct { int **prefix; int rows, cols; } NumMatrix;

NumMatrix *numMatrixCreate(int **matrix, int rows, int cols) {
    NumMatrix *m = malloc(sizeof(NumMatrix));
    m->prefix = malloc(sizeof(int *) * (size_t) (rows + 1));
    for (int r = 0; r <= rows; r++) m->prefix[r] = calloc((size_t) cols + 1, sizeof(int));
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            m->prefix[r + 1][c + 1] = matrix[r][c] + m->prefix[r][c + 1] + m->prefix[r + 1][c]
                                                      - m->prefix[r][c];
    m->rows = rows;
    m->cols = cols;
    return m;
}

int numMatrixSumRegion(NumMatrix *m, int row1, int col1, int row2, int col2) {
    return m->prefix[row2 + 1][col2 + 1] - m->prefix[row1][col2 + 1]
         - m->prefix[row2 + 1][col1] + m->prefix[row1][col1];
}   // O(1) per query after O(rows * cols) build · O(rows * cols) space
""",
    "product-of-array-except-self": r"""
// Two sweeps: the product of everything to the left, then of everything to the right.
int *productExceptSelf(const int *nums, int n, int *returnSize) {
    int *out = malloc(sizeof(int) * (size_t) n);
    out[0] = 1;
    for (int i = 1; i < n; i++) out[i] = out[i - 1] * nums[i - 1];     // prefix products
    int suffix = 1;
    for (int i = n - 1; i >= 0; i--) {
        out[i] *= suffix;                                   // suffix product of the right side
        suffix *= nums[i];
    }
    *returnSize = n;
    return out;
}   // O(n) time · O(1) extra space
""",
    "number-of-ways-to-split-array": r"""
// Split after i and i+1: compare the prefix sums directly.
int waysToSplitArray(const int *nums, int n) {
    long long total = 0;
    for (int i = 0; i < n; i++) total += nums[i];
    long long prefix = 0;
    int ways = 0;
    for (int i = 0; i < n - 1; i++) {
        prefix += nums[i];
        if (prefix >= total - prefix) ways++;
    }
    return ways;
}   // O(n) time · O(1) space
""",
    "binary-subarrays-with-sum": r"""
// Counting prefix sums with a small table: count(prefix - goal).
int numSubarraysWithSum(int *nums, int n, int goal) {
    int total = 0;
    for (int i = 0; i < n; i++) total += nums[i];
    int *count = calloc((size_t) total + 2, sizeof(int));    // how often each prefix sum occurred
    count[0] = 1;
    int prefix = 0, ways = 0;
    for (int i = 0; i < n; i++) {
        prefix += nums[i];
        if (prefix - goal >= 0) ways += count[prefix - goal];
        count[prefix]++;
    }
    free(count);
    return ways;
}   // O(n) time · O(n) space
""",
    "xor-queries-of-a-subarray": r"""
// XOR has the same prefix trick as sums, because x ^ x == 0.
int *xorQueries(const int *arr, int n, int **queries, int queryCount, int *returnSize) {
    int *prefix = calloc((size_t) n + 1, sizeof(int));
    for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] ^ arr[i];
    int *out = malloc(sizeof(int) * (size_t) queryCount);
    for (int q = 0; q < queryCount; q++)
        out[q] = prefix[queries[q][1] + 1] ^ prefix[queries[q][0]];
    free(prefix);
    *returnSize = queryCount;
    return out;
}   // O(n + queries) time · O(n) space
""",
    "sum-of-absolute-differences-in-a-sorted-array": r"""
// Sorted, so the absolute value splits at i: (i * a[i] - left) + (right - (n - 1 - i) * a[i]).
long long *getSumAbsoluteDifferences(int *nums, int n, int *returnSize) {
    long long *out = malloc(sizeof(long long) * (size_t) n);
    long long total = 0;
    for (int i = 0; i < n; i++) total += nums[i];
    long long left = 0;
    for (int i = 0; i < n; i++) {
        long long right = total - left - nums[i];
        out[i] = ((long long) i * nums[i] - left) + (right - (long long) (n - 1 - i) * nums[i]);
        left += nums[i];
    }
    *returnSize = n;
    return out;
}   // O(n) time · O(n) space
""",
    "matrix-block-sum": r"""
// The 2-D prefix table answers every block in constant time.
int **matrixBlockSum(int **mat, int rows, int cols, int k, int *returnSize, int **returnColumnSizes) {
    int **prefix = malloc(sizeof(int *) * (size_t) (rows + 1));
    for (int r = 0; r <= rows; r++) prefix[r] = calloc((size_t) cols + 1, sizeof(int));
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            prefix[r + 1][c + 1] = mat[r][c] + prefix[r][c + 1] + prefix[r + 1][c] - prefix[r][c];
    int **out = malloc(sizeof(int *) * (size_t) rows);
    *returnColumnSizes = malloc(sizeof(int) * (size_t) rows);
    for (int r = 0; r < rows; r++) {
        out[r] = malloc(sizeof(int) * (size_t) cols);
        for (int c = 0; c < cols; c++) {
            int top = r - k < 0 ? 0 : r - k, bottom = r + k >= rows ? rows - 1 : r + k;
            int left = c - k < 0 ? 0 : c - k, right = c + k >= cols ? cols - 1 : c + k;
            out[r][c] = prefix[bottom + 1][right + 1] - prefix[top][right + 1]
                      - prefix[bottom + 1][left] + prefix[top][left];
        }
        (*returnColumnSizes)[r] = cols;
    }
    for (int r = 0; r <= rows; r++) free(prefix[r]);
    free(prefix);
    *returnSize = rows;
    return out;
}   // O(rows * cols) time · O(rows * cols) space
""",
    "maximum-sum-of-two-non-overlapping-subarrays": r"""
// best[i] = best single window ending at or before i; then a second window after it.
int maxSumTwoNoOverlap(const int *nums, int n, int firstLen, int secondLen) {
    int *prefix = calloc((size_t) n + 1, sizeof(int));
    for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
    int best = 0;
    for (int order = 0; order < 2; order++) {                // first-then-second, then the reverse
        int a = order ? secondLen : firstLen, b = order ? firstLen : secondLen;
        int bestA = 0;
        for (int end = a; end + b <= n; end++) {             // window A ends at `end`
            int sumA = prefix[end] - prefix[end - a];
            if (sumA > bestA) bestA = sumA;
            int sumB = prefix[end + b] - prefix[end];
            if (bestA + sumB > best) best = bestA + sumB;
        }
    }
    free(prefix);
    return best;
}   // O(n) time · O(n) space
""",
    "range-sum-query-mutable": r"""
// A Fenwick tree (binary indexed tree): add to a point, sum a range in O(log n).
typedef struct { int *tree, *values, size; } NumArrayMutable;

void numArrayMutableUpdate(NumArrayMutable *a, int index, int val);   // used by the constructor

NumArrayMutable *numArrayMutableCreate(int *nums, int n) {
    NumArrayMutable *a = calloc(1, sizeof(NumArrayMutable));
    a->size = n;
    a->tree = calloc((size_t) n + 1, sizeof(int));
    a->values = calloc((size_t) n, sizeof(int));
    for (int i = 0; i < n; i++) numArrayMutableUpdate(a, i, nums[i]);
    return a;
}

void numArrayMutableUpdate(NumArrayMutable *a, int index, int val) {
    int delta = val - a->values[index];
    a->values[index] = val;
    for (int i = index + 1; i <= a->size; i += i & (-i)) a->tree[i] += delta;
}

static int fenwickPrefix(NumArrayMutable *a, int count) {
    int total = 0;
    for (int i = count; i > 0; i -= i & (-i)) total += a->tree[i];
    return total;
}

int numArrayMutableSumRange(NumArrayMutable *a, int left, int right) {
    return fenwickPrefix(a, right + 1) - fenwickPrefix(a, left);
}   // O(log n) per operation · O(n) space
""",
    "range-frequency-queries": r"""
// Remember the positions of each value; a query is a binary search on that list.
typedef struct { int **positions, *counts, *capacity; } RangeFreqQuery;

RangeFreqQuery *rangeFreqQueryCreate(int *arr, int n) {
    RangeFreqQuery *q = calloc(1, sizeof(RangeFreqQuery));
    q->positions = calloc(10001, sizeof(int *));
    q->counts = calloc(10001, sizeof(int));
    q->capacity = calloc(10001, sizeof(int));
    for (int i = 0; i < n; i++) {
        int value = arr[i];
        if (q->counts[value] == q->capacity[value]) {
            q->capacity[value] = q->capacity[value] ? q->capacity[value] * 2 : 4;
            q->positions[value] = realloc(q->positions[value],
                                          sizeof(int) * (size_t) q->capacity[value]);
        }
        q->positions[value][q->counts[value]++] = i;
    }
    return q;
}

static int lowerBoundPositions(int *a, int n, int target) {
    int lo = 0, hi = n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

int rangeFreqQueryQuery(RangeFreqQuery *q, int left, int right, int value) {
    int *list = q->positions[value];
    int n = q->counts[value];
    return lowerBoundPositions(list, n, right + 1) - lowerBoundPositions(list, n, left);
}   // O(log n) per query · O(n) space
""",
    "minimum-absolute-difference-queries": r"""
// A prefix count per value: then scan the 100 possible values for the closest pair.
int *minDifference(int *nums, int n, int **queries, int queryCount, int *returnSize) {
    int **prefix = malloc(sizeof(int *) * (size_t) (n + 1));
    for (int i = 0; i <= n; i++) prefix[i] = calloc(101, sizeof(int));
    for (int i = 0; i < n; i++) {
        memcpy(prefix[i + 1], prefix[i], 101 * sizeof(int));
        prefix[i + 1][nums[i]]++;
    }
    int *out = malloc(sizeof(int) * (size_t) queryCount);
    for (int q = 0; q < queryCount; q++) {
        int left = queries[q][0], right = queries[q][1];
        int previous = -1, best = INT_MAX;
        for (int value = 1; value <= 100; value++) {
            if (prefix[right + 1][value] - prefix[left][value] == 0) continue;
            if (previous >= 0 && value - previous < best) best = value - previous;
            previous = value;
        }
        out[q] = best == INT_MAX ? -1 : best;
    }
    for (int i = 0; i <= n; i++) free(prefix[i]);
    free(prefix);
    *returnSize = queryCount;
    return out;
}   // O((n + queries) * 100) time · O(n * 100) space
""",
    "range-sum-of-sorted-subarray-sums": r"""
// Generate every subarray sum, sort them, then answer the queries.
int rangeSum(int *nums, int n, int left, int right) {
    const long long MOD = 1000000007;
    long long *sums = malloc(sizeof(long long) * (size_t) (n * (n + 1) / 2));
    int count = 0;
    for (int i = 0; i < n; i++) {
        long long sum = 0;
        for (int j = i; j < n; j++) { sum += nums[j]; sums[count++] = sum; }
    }
    for (int i = 1; i < count; i++)                          // insertion sort keeps it simple
        for (int j = i; j > 0 && sums[j] < sums[j - 1]; j--) {
            long long t = sums[j]; sums[j] = sums[j - 1]; sums[j - 1] = t;
        }
    long long total = 0;
    for (int i = left - 1; i < right; i++) total = (total + sums[i]) % MOD;
    free(sums);
    return (int) total;
}   // O(n^2 log n) time · O(n^2) space
""",
    "minimum-number-of-increments-on-subarrays-to-form-a-target-array": r"""
// The answer is the first element plus every rise in the target.
int minNumberOperations(int *target, int n) {
    long long operations = 0;
    int previous = 0;
    for (int i = 0; i < n; i++) {
        if (target[i] > previous) operations += target[i] - previous;
        previous = target[i];
    }
    return (int) operations;
}   // O(n) time · O(1) space
""",
    "smallest-rotation-with-highest-score": r"""
// A rotation's score is the number of elements it leaves in place: sweep with a difference array.
int bestRotation(int *nums, int n) {
    int *delta = calloc((size_t) n + 1, sizeof(int));
    for (int i = 0; i < n; i++) {
        int low = (i - nums[i] + 1 + n) % n;                 // this element counts for these k
        int high = (i + 1) % n;
        delta[low]++;                                        // a range add, done by difference
        delta[high]--;
        if (low > high) delta[0]++;
    }
    int best = -1, bestScore = -1, score = 0;
    for (int k = 0; k < n; k++) {
        score += delta[k];
        if (score > bestScore) { bestScore = score; best = k; }
    }
    free(delta);
    return best;
}   // O(n) time · O(n) space
""",
    "maximum-sum-of-3-non-overlapping-subarrays": r"""
// window[i] = sum of the k elements starting at i; then the best triple by scanning.
int *maxSumOfThreeSubarrays(const int *nums, int n, int k, int *returnSize) {
    int count = n - k + 1;
    long long *window = malloc(sizeof(long long) * (size_t) count);
    long long running = 0;
    for (int i = 0; i < n; i++) {
        running += nums[i];
        if (i >= k) running -= nums[i - k];
        if (i >= k - 1) window[i - k + 1] = running;
    }
    int *bestLeft = malloc(sizeof(int) * (size_t) count);    // best window index up to i
    int *bestRight = malloc(sizeof(int) * (size_t) count);   // best window index from i on
    int index = 0;
    for (int i = 0; i < count; i++) {
        if (window[i] > window[index]) index = i;
        bestLeft[i] = index;
    }
    index = count - 1;
    for (int i = count - 1; i >= 0; i--) {
        if (window[i] >= window[index]) index = i;
        bestRight[i] = index;
    }
    long long best = -1;
    int out[3] = {0, 0, 0};
    for (int mid = k; mid + k < count; mid++) {
        int leftIndex = bestLeft[mid - k], rightIndex = bestRight[mid + k];
        long long total = window[leftIndex] + window[mid] + window[rightIndex];
        if (total > best) {
            best = total;
            out[0] = leftIndex;
            out[1] = mid;
            out[2] = rightIndex;
        }
    }
    int *result = malloc(sizeof(int) * 3);
    memcpy(result, out, sizeof out);
    free(window); free(bestLeft); free(bestRight);
    *returnSize = 3;
    return result;
}   // O(n) time · O(n) space
""",
    "count-of-range-sum": r"""
// Merge sort while counting the pairs whose sums land in [lower, upper].
typedef struct { long long value; int index; } Item;

static Item *buffer;

static int countWhileMerging(Item *a, int lo, int hi, int lower, int upper) {
    if (hi - lo <= 1) return 0;
    int mid = (lo + hi) / 2;
    int count = countWhileMerging(a, lo, mid, lower, upper)
              + countWhileMerging(a, mid, hi, lower, upper);
    int leftStart = mid, rightStart = mid;                  // two-pointer window on the right half
    for (int i = lo; i < mid; i++) {
        while (leftStart < hi && a[leftStart].value - a[i].value < lower) leftStart++;
        while (rightStart < hi && a[rightStart].value - a[i].value <= upper) rightStart++;
        count += rightStart - leftStart;
    }
    int i = lo, j = mid, k = lo;
    while (i < mid && j < hi) buffer[k++] = a[i].value <= a[j].value ? a[i++] : a[j++];
    while (i < mid) buffer[k++] = a[i++];
    while (j < hi) buffer[k++] = a[j++];
    for (int t = lo; t < hi; t++) a[t] = buffer[t];
    return count;
}

int countRangeSum(const int *nums, int n, int lower, int upper) {
    Item *prefix = malloc(sizeof(Item) * (size_t) (n + 1));
    buffer = malloc(sizeof(Item) * (size_t) (n + 1));
    prefix[0].value = 0;
    for (int i = 0; i < n; i++) prefix[i + 1].value = prefix[i].value + nums[i];
    int total = countWhileMerging(prefix, 0, n + 1, lower, upper);
    free(prefix); free(buffer);
    return total;
}   // O(n log n) time · O(n) space
""",
    "maximum-sum-queries": r"""
// Sort the queries by sum and keep only ever-better pairs (sum, length) in a stack.
static int cmpQuery(const void *a, const void *b) {
    const int *x = a, *y = b;
    return x[0] - y[0];
}

int *maximumSumQueries(int *nums1, int n, int *nums2, int **queries, int queryCount, int *returnSize) {
    int *order = malloc(sizeof(int) * (size_t) n);
    for (int i = 0; i < n; i++) order[i] = i;
    for (int i = 1; i < n; i++)                              // sort pairs by nums1 descending
        for (int j = i; j > 0 && nums1[order[j]] > nums1[order[j - 1]]; j--) {
            int t = order[j]; order[j] = order[j - 1]; order[j - 1] = t;
        }
    int *queryOrder = malloc(sizeof(int) * (size_t) queryCount);
    for (int i = 0; i < queryCount; i++) queryOrder[i] = i;
    for (int i = 1; i < queryCount; i++)                     // sort queries by the first bound
        for (int j = i; j > 0 && queries[queryOrder[j]][0] > queries[queryOrder[j - 1]][0]; j--) {
            int t = queryOrder[j]; queryOrder[j] = queryOrder[j - 1]; queryOrder[j - 1] = t;
        }
    int *out = malloc(sizeof(int) * (size_t) queryCount);
    int *stackSum = malloc(sizeof(int) * (size_t) (n + 1));
    int *stackLength = malloc(sizeof(int) * (size_t) (n + 1));
    int top = 0, added = 0;
    for (int q = 0; q < queryCount; q++) {
        int index = queryOrder[q];
        while (added < n && nums1[order[added]] >= queries[index][0]) {
            int second = nums2[order[added]], sum = nums1[order[added]] + second;
            while (top && stackLength[top - 1] <= second) top--;   // dominated: drop it
            if (!top || stackSum[top - 1] < sum) {
                stackLength[top] = second;
                stackSum[top] = sum;
                top++;
            }
            added++;
        }
        int best = -1, lo = 0, hi = top - 1;
        while (lo <= hi) {                                   // the deepest useful entry
            int mid = (lo + hi) / 2;
            if (stackLength[mid] >= queries[index][1]) { best = stackSum[mid]; lo = mid + 1; }
            else hi = mid - 1;
        }
        out[index] = best;
    }
    free(order); free(queryOrder); free(stackSum); free(stackLength);
    *returnSize = queryCount;
    return out;
}   // O((n + queries) log n) time · O(n) space
""",
    "count-of-smaller-numbers-after-self": r"""
// Merge sort counting: count how many later elements are smaller for each index.
typedef struct { int value, index; } Pair;

static Pair *scratch;
static int *answer;

static void mergeCount(Pair *a, int lo, int hi) {
    if (hi - lo <= 1) return;
    int mid = (lo + hi) / 2;
    mergeCount(a, lo, mid);
    mergeCount(a, mid, hi);
    int i = lo, j = mid, k = lo;
    while (i < mid && j < hi) {
        if (a[i].value <= a[j].value) {
            answer[a[i].index] += j - mid;                   // these j values are smaller
            scratch[k++] = a[i++];
        } else {
            scratch[k++] = a[j++];
        }
    }
    while (i < mid) { answer[a[i].index] += j - mid; scratch[k++] = a[i++]; }
    while (j < hi) scratch[k++] = a[j++];
    for (int t = lo; t < hi; t++) a[t] = scratch[t];
}

int *countSmaller(int *nums, int n, int *returnSize) {
    Pair *pairs = malloc(sizeof(Pair) * (size_t) n);
    scratch = malloc(sizeof(Pair) * (size_t) n);
    answer = calloc((size_t) n, sizeof(int));
    for (int i = 0; i < n; i++) {
        pairs[i].value = nums[i];
        pairs[i].index = i;
    }
    mergeCount(pairs, 0, n);
    free(pairs); free(scratch);
    *returnSize = n;
    int *out = answer;
    answer = NULL;
    return out;
}   // O(n log n) time · O(n) space
""",
    "create-sorted-array-through-instructions": r"""
// Fenwick tree over the values: count how many earlier values are smaller or larger.
int createSortedArray(int *instructions, int n) {
    const long long MOD = 1000000007;
    int maximum = 0;
    for (int i = 0; i < n; i++) if (instructions[i] > maximum) maximum = instructions[i];
    int *tree = calloc((size_t) maximum + 2, sizeof(int));
    long long total = 0;
    for (int i = 0; i < n; i++) {
        int value = instructions[i];
        long long smaller = 0, larger = 0;
        for (int j = value - 1; j > 0; j -= j & (-j)) smaller += tree[j];       // values below
        int processed = 0;
        for (int j = maximum; j > 0; j -= j & (-j)) processed += tree[j];
        long long atOrBelow = 0;
        for (int j = value; j > 0; j -= j & (-j)) atOrBelow += tree[j];
        larger = processed - atOrBelow;                          // values above
        total = (total + (smaller < larger ? smaller : larger)) % MOD;
        for (int j = value; j <= maximum; j += j & (-j)) tree[j]++;   // add this value
    }
    free(tree);
    return (int) total;
}   // O(n log max) time · O(max) space
""",
    "count-good-triplets-in-an-array": r"""
// Two Fenwick passes: the count of smaller values on each side, multiplied and summed.
static long long fenwickQuery(long long *tree, int i) {
    long long total = 0;
    for (; i > 0; i -= i & (-i)) total += tree[i];
    return total;
}

static void fenwickAdd(long long *tree, int i, int n) {
    for (; i <= n; i += i & (-i)) tree[i]++;
}

long long goodTriplets(int *nums1, int *nums2, int n) {
    int *position = malloc(sizeof(int) * (size_t) n);        // where each value sits in nums2
    for (int i = 0; i < n; i++) position[nums2[i]] = i;
    long long *tree = calloc((size_t) n + 1, sizeof(long long));
    long long *smallerLeft = malloc(sizeof(long long) * (size_t) n);
    for (int i = 0; i < n; i++) {
        int index = position[nums1[i]];                      // 1-based for the Fenwick tree
        smallerLeft[i] = fenwickQuery(tree, index);
        fenwickAdd(tree, index + 1, n);
    }
    memset(tree, 0, sizeof(long long) * (size_t) (n + 1));
    long long total = 0;
    for (int i = n - 1; i >= 0; i--) {
        int index = position[nums1[i]];
        long long largerRight = fenwickQuery(tree, n) - fenwickQuery(tree, index + 1);
        total += smallerLeft[i] * largerRight;
        fenwickAdd(tree, index + 1, n);
    }
    free(position); free(tree); free(smallerLeft);
    return total;
}   // O(n log n) time · O(n) space
""",
    "reverse-pairs": r"""
// Merge sort counting the pairs where the left value is more than twice the right one.
static int *scratchPairs;

static int countReverse(int *a, int lo, int hi) {
    if (hi - lo <= 1) return 0;
    int mid = (lo + hi) / 2;
    int count = countReverse(a, lo, mid) + countReverse(a, mid, hi);
    int j = mid;
    for (int i = lo; i < mid; i++) {                         // two pointers over the halves
        while (j < hi && (long long) a[i] > 2LL * a[j]) j++;
        count += j - mid;
    }
    int i = lo, k = lo;
    j = mid;
    while (i < mid && j < hi) scratchPairs[k++] = a[i] <= a[j] ? a[i++] : a[j++];
    while (i < mid) scratchPairs[k++] = a[i++];
    while (j < hi) scratchPairs[k++] = a[j++];
    for (int t = lo; t < hi; t++) a[t] = scratchPairs[t];
    return count;
}

int reversePairs(int *nums, int n) {
    scratchPairs = malloc(sizeof(int) * (size_t) n);
    int total = countReverse(nums, 0, n);
    free(scratchPairs);
    return total;
}   // O(n log n) time · O(n) space
""",
    "sum-of-total-strength-of-wizards": r"""
// For each wizard: (sum of subarrays where it is the minimum) * its strength, using
// the previous/next strictly smaller elements for the boundaries.
int totalStrength(int *strength, int n) {
    const long long MOD = 1000000007;
    int *left = malloc(sizeof(int) * (size_t) n), *right = malloc(sizeof(int) * (size_t) n);
    int *stack = malloc(sizeof(int) * (size_t) n);
    int top = 0;
    for (int i = 0; i < n; i++) {                            // previous element that is smaller
        while (top && strength[stack[top - 1]] >= strength[i]) top--;
        left[i] = top ? stack[top - 1] : -1;
        stack[top++] = i;
    }
    top = 0;
    for (int i = n - 1; i >= 0; i--) {                       // next element that is strictly smaller
        while (top && strength[stack[top - 1]] > strength[i]) top--;
        right[i] = top ? stack[top - 1] : n;
        stack[top++] = i;
    }
    long long *prefix = calloc((size_t) n + 2, sizeof(long long));
    for (int i = 1; i <= n; i++) prefix[i] = (prefix[i - 1] + strength[i - 1]) % MOD;
    long long *weighted = calloc((size_t) n + 2, sizeof(long long));
    for (int i = 1; i <= n; i++) weighted[i] = (weighted[i - 1] + prefix[i]) % MOD;
    long long total = 0;
    for (int i = 0; i < n; i++) {
        long long leftCount = i - left[i], rightCount = right[i] - i;
        long long leftSum = (prefix[i + 1] * leftCount % MOD - (weighted[i + 1] - weighted[left[i] + 1] + MOD)) % MOD;
        long long rightSum = ((weighted[right[i]] - weighted[i + 1] + MOD) % MOD
                              - prefix[i + 1] * rightCount % MOD + MOD) % MOD;
        long long contribution = (rightCount % MOD * leftSum % MOD + leftCount % MOD * rightSum % MOD) % MOD;
        total = (total + contribution % MOD * strength[i]) % MOD;
    }
    free(left); free(right); free(stack); free(prefix); free(weighted);
    return (int) ((total % MOD + MOD) % MOD);
}   // O(n) time · O(n) space
""",
    "count-subarrays-with-fixed-bounds": r"""
// A window counts when it contains both bounds and nothing outside the range.
long long countSubarrays(int *nums, int n, int minK, int maxK) {
    long long total = 0;
    int lastBad = -1, lastMin = -1, lastMax = -1;
    for (int i = 0; i < n; i++) {
        if (nums[i] < minK || nums[i] > maxK) lastBad = i;   // this value breaks every window
        if (nums[i] == minK) lastMin = i;
        if (nums[i] == maxK) lastMax = i;
        int earliest = lastMin < lastMax ? lastMin : lastMax;
        if (earliest > lastBad) total += earliest - lastBad;  // windows ending at i
    }
    return total;
}   // O(n) time · O(1) space
""",
    "sum-of-subsequence-widths": r"""
// After sorting, element i is the maximum of 2^i subsequences and the minimum of 2^(n-1-i).
int sumSubseqWidths(int *nums, int n) {
    const long long MOD = 1000000007;
    for (int i = 1; i < n; i++)                              // insertion sort
        for (int j = i; j > 0 && nums[j] < nums[j - 1]; j--) {
            int t = nums[j]; nums[j] = nums[j - 1]; nums[j - 1] = t;
        }
    long long *power = malloc(sizeof(long long) * (size_t) n);
    power[0] = 1;
    for (int i = 1; i < n; i++) power[i] = power[i - 1] * 2 % MOD;
    long long total = 0;
    for (int i = 0; i < n; i++)
        total = (total + (power[i] - power[n - 1 - i] + MOD) % MOD * nums[i]) % MOD;
    free(power);
    return (int) ((total % MOD + MOD) % MOD);
}   // O(n log n) time · O(n) space
""",
}
