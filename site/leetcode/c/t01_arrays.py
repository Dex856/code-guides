# Topic 1 · Arrays & Strings — C17 solutions
#
# One C function per problem, LeetCode style: the same signature the bank page shows,
# with arrays passed as (pointer, size) and output buffers where the problem needs them.
# CODE maps slug -> source; build.py and build_bank_json.py merge it into the banks.

CODE = {
    # ------------------------------------------------------------------ EASY
    "largest-and-second-largest": r"""
// Largest and second largest distinct value in one pass.
// `out` receives two values: out[0] = largest, out[1] = second (-1 when absent).
void topTwo(const int *a, int n, int *out) {
    long long best = LLONG_MIN, second = LLONG_MIN;
    for (int i = 0; i < n; i++) {
        long long v = a[i];
        if (v > best) { second = best; best = v; }        // new maximum demotes the old one
        else if (v < best && v > second) second = v;      // strict < best removes duplicates
    }
    out[0] = (int) best;
    out[1] = second == LLONG_MIN ? -1 : (int) second;
}   // O(n) time · O(1) space
""",
    "reverse-array-in-place": r"""
// Reverse the array in place with two indices walking towards each other.
void reverseArray(int *a, int n) {
    for (int i = 0, j = n - 1; i < j; i++, j--) {
        int t = a[i]; a[i] = a[j]; a[j] = t;              // swap — no extra array
    }
}   // O(n) time · O(1) space
""",
    "count-above-average": r"""
// Average first, then count — one pass is not enough because the average is not known yet.
int countAboveAverage(const int *a, int n) {
    long long sum = 0;
    for (int i = 0; i < n; i++) sum += a[i];
    int count = 0;
    for (int i = 0; i < n; i++)
        if ((long long) a[i] * n > sum) count++;          // a[i] > sum/n without floating point
    return count;
}   // O(n) time · O(1) space
""",
    "move-zeroes": r"""
// Write pointer: everything before `w` is non-zero, order preserved.
void moveZeroes(int *a, int n) {
    int w = 0;
    for (int i = 0; i < n; i++)
        if (a[i] != 0) a[w++] = a[i];
    while (w < n) a[w++] = 0;                             // the tail becomes zeros
}   // O(n) time · O(1) space
""",
    "dedupe-sorted-in-place": r"""
// Sorted input, so equal values are neighbours; keep the first of each run.
int dedupeSorted(int *a, int n) {
    if (n == 0) return 0;
    int w = 1;
    for (int i = 1; i < n; i++)
        if (a[i] != a[w - 1]) a[w++] = a[i];
    return w;                                             // new length
}   // O(n) time · O(1) space
""",
    "rotate-array-by-k": r"""
// Three reversals instead of k shifts: reverse all, then reverse each part.
static void rev(int *a, int lo, int hi) {
    while (lo < hi) { int t = a[lo]; a[lo++] = a[hi]; a[hi--] = t; }
}

void rotateRight(int *a, int n, int k) {
    if (n == 0) return;
    k %= n;
    if (k < 0) k += n;
    rev(a, 0, n - 1);
    rev(a, 0, k - 1);
    rev(a, k, n - 1);
}   // O(n) time · O(1) space
""",
    # ------------------------------------------------------------------ MEDIUM
    "maximum-subarray-sum": r"""
// Kadane: either extend the run or start again at the current element.
long long maxSubarraySum(const int *a, int n) {
    long long best = LLONG_MIN, here = 0;
    for (int i = 0; i < n; i++) {
        here = here > 0 ? here + a[i] : a[i];
        if (here > best) best = here;
    }
    return best;
}   // O(n) time · O(1) space
""",
    "product-except-self": r"""
// Two passes: out[i] = (product of everything left) * (product of everything right).
void productExceptSelf(const int *a, int n, long long *out) {
    long long run = 1;
    for (int i = 0; i < n; i++) { out[i] = run; run *= a[i]; }      // left products
    run = 1;
    for (int i = n - 1; i >= 0; i--) { out[i] *= run; run *= a[i]; } // times right products
}   // O(n) time · O(1) extra space (the output holds the answer)
""",
    "sort-colors-three-way": r"""
// Dutch national flag: [0, lo) is 0, (hi, n-1] is 2, the middle is unknown.
void sortColors(int *a, int n) {
    int lo = 0, mid = 0, hi = n - 1;
    while (mid <= hi) {
        if (a[mid] == 0) { int t = a[lo]; a[lo++] = a[mid]; a[mid++] = t; }
        else if (a[mid] == 2) { int t = a[mid]; a[mid] = a[hi]; a[hi--] = t; }
        else mid++;                                       // 1s stay where they are
    }
}   // O(n) time · O(1) space
""",
    "majority-element": r"""
// Boyer-Moore: a surviving candidate appears more than half the time, so pairing
// every different pair off leaves it standing.
int majorityElement(const int *a, int n) {
    int cand = a[0], count = 0;
    for (int i = 0; i < n; i++) {
        if (count == 0) cand = a[i];
        count += (a[i] == cand) ? 1 : -1;
    }
    return cand;
}   // O(n) time · O(1) space
""",
    "best-time-buy-sell-ii": r"""
// Sum every upward step: holding across a rise is the same as buying and selling daily.
long long maxProfit(const int *p, int n) {
    long long profit = 0;
    for (int i = 1; i < n; i++)
        if (p[i] > p[i - 1]) profit += p[i] - p[i - 1];
    return profit;
}   // O(n) time · O(1) space
""",
    "rotate-matrix-90": r"""
// Transpose, then reverse every row — both are in-place swaps.
void rotate90(int n, int m[n][n]) {
    for (int i = 0; i < n; i++)                           // transpose across the main diagonal
        for (int j = i + 1; j < n; j++) { int t = m[i][j]; m[i][j] = m[j][i]; m[j][i] = t; }
    for (int i = 0; i < n; i++)                           // reverse each row
        for (int j = 0, k = n - 1; j < k; j++, k--) { int t = m[i][j]; m[i][j] = m[i][k]; m[i][k] = t; }
}   // O(n^2) time · O(1) space
""",
    "spiral-order": r"""
// Shrink a rectangle of four borders after each edge walk.
void spiralOrder(int rows, int cols, const int m[rows][cols], int *out, int *outSize) {
    int top = 0, bottom = rows - 1, left = 0, right = cols - 1, k = 0;
    while (top <= bottom && left <= right) {
        for (int j = left; j <= right; j++) out[k++] = m[top][j];
        top++;
        for (int i = top; i <= bottom; i++) out[k++] = m[i][right];
        right--;
        if (top <= bottom) {
            for (int j = right; j >= left; j--) out[k++] = m[bottom][j];
            bottom--;
        }
        if (left <= right) {
            for (int i = bottom; i >= top; i--) out[k++] = m[i][left];
            left++;
        }
    }
    *outSize = k;
}   // O(rows*cols) time · O(1) space
""",
    "set-matrix-zeroes": r"""
// The first row and column double as the marker storage, so no extra matrix is needed.
void setZeroes(int rows, int cols, int m[rows][cols]) {
    int firstRow = 0, firstCol = 0;
    for (int j = 0; j < cols; j++) if (m[0][j] == 0) firstRow = 1;
    for (int i = 0; i < rows; i++) if (m[i][0] == 0) firstCol = 1;
    for (int i = 1; i < rows; i++)
        for (int j = 1; j < cols; j++)
            if (m[i][j] == 0) { m[i][0] = 0; m[0][j] = 0; }
    for (int i = 1; i < rows; i++)
        for (int j = 1; j < cols; j++)
            if (m[i][0] == 0 || m[0][j] == 0) m[i][j] = 0;
    if (firstRow) for (int j = 0; j < cols; j++) m[0][j] = 0;
    if (firstCol) for (int i = 0; i < rows; i++) m[i][0] = 0;
}   // O(rows*cols) time · O(1) space
""",
    "longest-common-prefix": r"""
// Compare column by column against the first string; stop at the first mismatch.
int longestCommonPrefix(char **words, int n, char *out) {
    int len = 0;
    if (n == 0) { out[0] = '\0'; return 0; }
    for (int i = 0; words[0][i] != '\0'; i++) {
        char c = words[0][i];
        for (int w = 1; w < n; w++)
            if (words[w][i] != c) { out[len] = '\0'; return len; }
        out[len++] = c;                                   // this column matches everywhere
    }
    out[len] = '\0';
    return len;
}   // O(total characters) time · O(1) extra space
""",
    "valid-palindrome-filtered": r"""
// Two indices, skipping characters that are not letters or digits.
int isPalindromeFiltered(const char *s) {
    int i = 0, j = (int) strlen(s) - 1;
    while (i < j) {
        while (i < j && !isalnum((unsigned char) s[i])) i++;
        while (i < j && !isalnum((unsigned char) s[j])) j--;
        if (tolower((unsigned char) s[i]) != tolower((unsigned char) s[j])) return 0;   // false
        i++; j--;
    }
    return 1;                                             // true
}   // O(n) time · O(1) space
""",
    "first-unique-character": r"""
// One counter array for the 26 letters, then the first slot that stayed at 1.
int firstUniqChar(const char *s) {
    int count[26] = {0};
    for (int i = 0; s[i]; i++) count[s[i] - 'a']++;
    for (int i = 0; s[i]; i++)
        if (count[s[i] - 'a'] == 1) return i;
    return -1;
}   // O(n) time · O(1) space
""",
    "reverse-words": r"""
// Reverse the whole sentence, then reverse every word back — the words end up ordered.
static void revRange(char *s, int lo, int hi) {
    while (lo < hi) { char t = s[lo]; s[lo++] = s[hi]; s[hi--] = t; }
}

char *reverseWords(char *s) {
    int n = (int) strlen(s);
    revRange(s, 0, n - 1);
    int i = 0, w = 0;
    while (i < n) {
        while (i < n && s[i] == ' ') i++;                 // skip runs of spaces
        if (i == n) break;
        int start = i;
        while (i < n && s[i] != ' ') i++;
        if (w) s[w++] = ' ';                              // single separator between words
        for (int j = start; j < i; j++) s[w++] = s[j];
        revRange(s, w - (i - start), w - 1);
    }
    s[w] = '\0';
    return s;
}   // O(n) time · O(1) extra space
""",
    # ------------------------------------------------------------------ HARD
    "first-missing-positive": r"""
// Cycle sort into place: value v belongs at index v-1, so a scan finds the first hole.
int firstMissingPositive(int *a, int n) {
    for (int i = 0; i < n; i++)
        while (a[i] > 0 && a[i] <= n && a[a[i] - 1] != a[i]) {
            int t = a[a[i] - 1]; a[a[i] - 1] = a[i]; a[i] = t;
        }
    for (int i = 0; i < n; i++)
        if (a[i] != i + 1) return i + 1;
    return n + 1;
}   // O(n) time · O(1) space
""",
    "container-with-most-water": r"""
// Start wide and always move the shorter wall: the width can only shrink, so the
// short side is the one that can still improve.
long long maxArea(const int *h, int n) {
    int i = 0, j = n - 1;
    long long best = 0;
    while (i < j) {
        long long hh = h[i] < h[j] ? h[i] : h[j];
        long long area = hh * (j - i);
        if (area > best) best = area;
        if (h[i] < h[j]) i++; else j--;
    }
    return best;
}   // O(n) time · O(1) space
""",
    "trapping-rain-water": r"""
// The water above a bar is min(tallest on the left, tallest on the right) - height.
// Walk inwards from the shorter side so the second height is already known.
long long trap(const int *h, int n) {
    int i = 0, j = n - 1, leftMax = 0, rightMax = 0;
    long long water = 0;
    while (i < j) {
        if (h[i] < h[j]) {
            leftMax = h[i] > leftMax ? h[i] : leftMax;
            water += leftMax - h[i];
            i++;
        } else {
            rightMax = h[j] > rightMax ? h[j] : rightMax;
            water += rightMax - h[j];
            j--;
        }
    }
    return water;
}   // O(n) time · O(1) space
""",
    "maximum-product-subarray": r"""
// A negative flips the sign, so track both the maximum and the minimum product ending here.
long long maxProduct(const int *a, int n) {
    long long best = a[0], hi = a[0], lo = a[0];
    for (int i = 1; i < n; i++) {
        long long x = (long long) a[i];
        if (x < 0) { long long t = hi; hi = lo; lo = t; }   // multiplying by x<0 swaps the roles
        hi = hi * x > x ? hi * x : x;
        lo = lo * x < x ? lo * x : x;
        if (hi > best) best = hi;
    }
    return best;
}   // O(n) time · O(1) space
""",
    "longest-consecutive-sequence": r"""
// Put the values in a hash set, then only start counting at values with no left neighbour.
// (A qsort-based version follows: sorting costs O(n log n) but no hash set is needed.)
static int cmpInt(const void *a, const void *b) {
    int x = *(const int *) a, y = *(const int *) b;
    return (x > y) - (x < y);
}

int longestConsecutive(int *a, int n) {
    if (n == 0) return 0;
    qsort(a, n, sizeof(int), cmpInt);
    int best = 1, run = 1;
    for (int i = 1; i < n; i++) {
        if (a[i] == a[i - 1]) continue;                   // duplicates do not extend a run
        run = (a[i] == a[i - 1] + 1) ? run + 1 : 1;
        if (run > best) best = run;
    }
    return best;
}   // O(n log n) time · O(1) space
""",
    "count-inversions": r"""
// Merge sort that counts: while merging, every element taken from the right half is
// smaller than all the elements still waiting in the left half.
static long long countMerge(int *a, int *tmp, int lo, int hi) {
    if (hi - lo < 2) return 0;
    int mid = (lo + hi) / 2;
    long long inv = countMerge(a, tmp, lo, mid) + countMerge(a, tmp, mid, hi);
    int i = lo, j = mid, k = lo;
    while (i < mid && j < hi) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];
        else { inv += mid - i; tmp[k++] = a[j++]; }        // a[j] pairs with i..mid-1
    }
    while (i < mid) tmp[k++] = a[i++];
    while (j < hi) tmp[k++] = a[j++];
    for (int t = lo; t < hi; t++) a[t] = tmp[t];
    return inv;
}

long long countInversions(int *a, int n) {
    int *tmp = malloc(sizeof(int) * (size_t) n);
    long long inv = countMerge(a, tmp, 0, n);
    free(tmp);
    return inv;
}   // O(n log n) time · O(n) space
""",
    "majority-element-ii": r"""
// At most two values can appear more than n/3 times, so verify the two survivors.
int majorityElementII(const int *a, int n, int *out) {
    int c1 = 0, c2 = 0, v1 = 0, v2 = 0, k = 0;
    for (int i = 0; i < n; i++) {
        if (c1 && a[i] == v1) c1++;
        else if (c2 && a[i] == v2) c2++;
        else if (c1 == 0) { v1 = a[i]; c1 = 1; }
        else if (c2 == 0) { v2 = a[i]; c2 = 1; }
        else { c1--; c2--; }                              // three different values cancel
    }
    int t1 = 0, t2 = 0;
    for (int i = 0; i < n; i++) { if (a[i] == v1) t1++; else if (a[i] == v2) t2++; }
    if (c1 && t1 > n / 3) out[k++] = v1;
    if (c2 && t2 > n / 3) out[k++] = v2;
    return k;
}   // O(n) time · O(1) space
""",
    "next-permutation": r"""
// Find the rightmost ascent, swap its left value with the smallest larger one on the
// right, then reverse the descending tail into ascending order.
void nextPermutation(int *a, int n) {
    int i = n - 2;
    while (i >= 0 && a[i] >= a[i + 1]) i--;               // pivot: last index that can grow
    if (i >= 0) {
        int j = n - 1;
        while (a[j] <= a[i]) j--;
        int t = a[i]; a[i] = a[j]; a[j] = t;
    }
    for (int lo = i + 1, hi = n - 1; lo < hi; lo++, hi--) {
        int t = a[lo]; a[lo] = a[hi]; a[hi] = t;          // tail is descending → reverse it
    }
}   // O(n) time · O(1) space
""",
    "string-compression-in-place": r"""
// Read pointer over the characters, write pointer into the same buffer.
int compress(char *s) {
    int n = (int) strlen(s), w = 0, i = 0;
    while (i < n) {
        int j = i;
        while (j < n && s[j] == s[i]) j++;                // the run s[i..j)
        s[w++] = s[i];
        int run = j - i;
        if (run > 1) {                                    // write the count digit by digit
            char digits[12];
            int d = 0;
            while (run) { digits[d++] = (char) ('0' + run % 10); run /= 10; }
            while (d) s[w++] = digits[--d];
        }
        i = j;
    }
    s[w] = '\0';
    return w;
}   // O(n) time · O(1) extra space
""",
    "longest-palindromic-substring": r"""
// Expand around every possible centre (n odd centres, n-1 even centres).
char *longestPalindrome(const char *s) {
    int n = (int) strlen(s), bestStart = 0, bestLen = n ? 1 : 0;
    for (int c = 0; c < n; c++) {
        for (int parity = 0; parity < 2; parity++) {      // 0: odd centre, 1: even centre
            int i = c, j = c + parity;
            while (i >= 0 && j < n && s[i] == s[j]) { i--; j++; }
            int len = j - i - 1;                          // the loop overshoots by one
            if (len > bestLen) { bestLen = len; bestStart = i + 1; }
        }
    }
    char *out = malloc((size_t) bestLen + 1);
    memcpy(out, s + bestStart, (size_t) bestLen);
    out[bestLen] = '\0';
    return out;
}   // O(n^2) time · O(1) space (beyond the answer)
""",
    "subarray-sums-divisible-by-k": r"""
// Two prefixes with the same remainder mod k differ by a multiple of k, so count
// the prefixes per remainder and pair them up.
int subarraysDivByK(const int *a, int n, int k) {
    int *count = calloc((size_t) k, sizeof(int));
    count[0] = 1;                                         // the empty prefix
    int running = 0, total = 0;
    for (int i = 0; i < n; i++) {
        running = ((running + a[i]) % k + k) % k;         // keep the remainder positive
        total += count[running];
        count[running]++;
    }
    free(count);
    return total;
}   // O(n) time · O(k) space
""",
    "median-of-two-sorted-arrays": r"""
// Binary search the split position in the shorter array; the halves must satisfy
// max(left) <= min(right) on both sides.
double findMedianSortedArrays(const int *a, int n, const int *b, int m) {
    if (n > m) { const int *ta = a; a = b; b = ta; int tt = n; n = m; m = tt; }
    int lo = 0, hi = n, half = (n + m + 1) / 2;
    while (lo <= hi) {
        int i = (lo + hi) / 2, j = half - i;
        long long aLeft  = i ? a[i - 1] : LLONG_MIN, aRight = i < n ? a[i] : LLONG_MAX;
        long long bLeft  = j ? b[j - 1] : LLONG_MIN, bRight = j < m ? b[j] : LLONG_MAX;
        if (aLeft <= bRight && bLeft <= aRight) {
            long long leftMax = aLeft > bLeft ? aLeft : bLeft;
            if ((n + m) % 2) return (double) leftMax;
            long long rightMin = aRight < bRight ? aRight : bRight;
            return (leftMax + rightMin) / 2.0;
        }
        if (aLeft > bRight) hi = i - 1;                   // too many elements taken from a
        else lo = i + 1;
    }
    return 0.0;
}   // O(log(min(n, m))) time · O(1) space
""",
}
