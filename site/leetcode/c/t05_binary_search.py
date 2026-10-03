# Topic 5 · Binary Search & Sorted Structures — C17 solutions
CODE = {
    "binary-search": r"""
// The classic: halve the range until the target is found or the range is empty.
int search(const int *a, int n, int target) {
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;                     // no overflow: hi + lo may
        if (a[mid] == target) return mid;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}   // O(log n) time · O(1) space
""",
    "search-insert-position": r"""
// Lower bound: the first index whose value is >= target is also the insert position.
int searchInsert(const int *a, int n, int target) {
    int lo = 0, hi = n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}   // O(log n) time · O(1) space
""",
    "sqrtx": r"""
// Binary search the answer in [0, x] using x / mid to avoid overflow.
int mySqrt(int x) {
    if (x < 2) return x;
    long long lo = 1, hi = x / 2, best = 0;
    while (lo <= hi) {
        long long mid = (lo + hi) / 2;
        if (mid <= x / mid) { best = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    return (int) best;
}   // O(log x) time · O(1) space
""",
    "first-bad-version": r"""
// The judge provides isBadVersion through a callback, so it is passed in here.
int firstBadVersion(int n, int (*isBadVersion)(int)) {
    int lo = 1, hi = n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (isBadVersion(mid)) hi = mid;                  // the first bad one is at or before mid
        else lo = mid + 1;
    }
    return lo;
}   // O(log n) time · O(1) space
""",
    "valid-perfect-square": r"""
// Same search as sqrt: a perfect square is exactly mid * mid == num.
int isPerfectSquare(int num) {
    long long lo = 1, hi = num;
    while (lo <= hi) {
        long long mid = (lo + hi) / 2;
        if (mid * mid == num) return 1;
        if (mid * mid < num) lo = mid + 1;
        else hi = mid - 1;
    }
    return 0;
}   // O(log n) time · O(1) space
""",
    "smallest-letter-greater-than-target": r"""
// Upper bound: the first letter strictly greater than the target, wrapping around.
char nextGreatestLetter(const char *letters, char target) {
    int n = (int) strlen(letters), lo = 0, hi = n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (letters[mid] <= target) lo = mid + 1;
        else hi = mid;
    }
    return lo < n ? letters[lo] : letters[0];
}   // O(log n) time · O(1) space
""",
    "search-in-rotated-sorted-array": r"""
// One half is always sorted: decide which, then look inside it.
int searchRotated(const int *a, int n, int target) {
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        if (a[lo] <= a[mid]) {                            // the left half is sorted
            if (a[lo] <= target && target < a[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {                                          // the right half is sorted
            if (a[mid] < target && target <= a[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return -1;
}   // O(log n) time · O(1) space
""",
    "find-minimum-in-rotated-sorted-array": r"""
// The minimum is the only place where the order drops.
int findMin(const int *a, int n) {
    int lo = 0, hi = n - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] > a[hi]) lo = mid + 1;                 // the rotation point is to the right
        else hi = mid;
    }
    return a[lo];
}   // O(log n) time · O(1) space
""",
    "search-a-2d-matrix": r"""
// Treat the matrix as one sorted array of rows * cols values.
int searchMatrix(int rows, int cols, int m[][16], int target) {
    int lo = 0, hi = rows * cols - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int v = m[mid / cols][mid % cols];
        if (v == target) return 1;
        if (v < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return 0;
}   // O(log(rows * cols)) time · O(1) space
""",
    "koko-eating-bananas": r"""
// Binary search the speed: hours(speed) decreases as the speed grows.
static long long hoursFor(const int *piles, int n, int speed) {
    long long hours = 0;
    for (int i = 0; i < n; i++) hours += (piles[i] + speed - 1) / speed;   // ceiling division
    return hours;
}

int minEatingSpeed(const int *piles, int n, int h) {
    int lo = 1, hi = 0;
    for (int i = 0; i < n; i++) if (piles[i] > hi) hi = piles[i];
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (hoursFor(piles, n, mid) <= h) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(n log max(piles)) time · O(1) space
""",
    "capacity-to-ship-packages-within-d-days": r"""
// The capacity must be at least the heaviest package and at most the total weight.
static int daysFor(const int *w, int n, int cap) {
    int days = 1, load = 0;
    for (int i = 0; i < n; i++) {
        if (load + w[i] > cap) { days++; load = 0; }
        load += w[i];
    }
    return days;
}

int shipWithinDays(const int *weights, int n, int days) {
    int lo = 0, hi = 0;
    for (int i = 0; i < n; i++) {
        hi += weights[i];
        if (weights[i] > lo) lo = weights[i];
    }
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (daysFor(weights, n, mid) <= days) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(n log total) time · O(1) space
""",
    "find-peak-element": r"""
// Walk towards the rising side: a peak must exist there.
int findPeakElement(const int *a, int n) {
    int lo = 0, hi = n - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] > a[mid + 1]) hi = mid;                // the peak is at mid or to its left
        else lo = mid + 1;
    }
    return lo;
}   // O(log n) time · O(1) space
""",
    "find-first-and-last-position": r"""
// Two lower-bound searches: the first index >= target, and the first >= target + 1.
static int lowerBound(const int *a, int n, long long target) {
    int lo = 0, hi = n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

void searchRange(const int *a, int n, int target, int *out) {
    int first = lowerBound(a, n, target);
    if (first == n || a[first] != target) { out[0] = out[1] = -1; return; }
    out[0] = first;
    out[1] = lowerBound(a, n, (long long) target + 1) - 1;
}   // O(log n) time · O(1) space
""",
    "search-in-rotated-sorted-array-ii": r"""
// Duplicates mean a[mid] == a[lo] can hide the sorted side: shrink by one then.
int searchRotatedII(const int *a, int n, int target) {
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return 1;
        if (a[lo] == a[mid] && a[mid] == a[hi]) { lo++; hi--; continue; }
        if (a[lo] <= a[mid]) {
            if (a[lo] <= target && target < a[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {
            if (a[mid] < target && target <= a[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return 0;
}   // O(log n) average, O(n) worst case · O(1) space
""",
    "longest-increasing-subsequence": r"""
// tails[i] is the smallest possible tail of an increasing run of length i + 1.
int lengthOfLIS(const int *a, int n) {
    int *tails = malloc(sizeof(int) * (size_t) n);
    int len = 0;
    for (int i = 0; i < n; i++) {
        int lo = 0, hi = len;
        while (lo < hi) {                                 // lower_bound(tails, a[i])
            int mid = lo + (hi - lo) / 2;
            if (tails[mid] < a[i]) lo = mid + 1;
            else hi = mid;
        }
        tails[lo] = a[i];
        if (lo == len) len++;
    }
    free(tails);
    return len;
}   // O(n log n) time · O(n) space
""",
    "search-a-2d-matrix-ii": r"""
// Start at the top-right corner: larger values go down, smaller go left.
int searchMatrixII(int rows, int cols, int m[][16], int target) {
    int r = 0, c = cols - 1;
    while (r < rows && c >= 0) {
        if (m[r][c] == target) return 1;
        if (m[r][c] > target) c--;
        else r++;
    }
    return 0;
}   // O(rows + cols) time · O(1) space
""",
    "minimum-limit-of-balls-in-a-bag": r"""
// Operations needed for a limit L = sum of ceil(v / L) - 1.
static int opsFor(const int *a, int n, int limit) {
    int ops = 0;
    for (int i = 0; i < n; i++) ops += (a[i] - 1) / limit;
    return ops;
}

int minimumSize(const int *nums, int n, int maxOperations) {
    int lo = 1, hi = 0;
    for (int i = 0; i < n; i++) if (nums[i] > hi) hi = nums[i];
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (opsFor(nums, n, mid) <= maxOperations) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(n log max) time · O(1) space
""",
    "minimum-days-to-make-bouquets": r"""
// Feasibility: count the consecutive blooms that are ready on a given day.
static int bouquetsOn(const int *bloom, int n, int day, int k) {
    int bouquets = 0, run = 0;
    for (int i = 0; i < n; i++) {
        run = bloom[i] <= day ? run + 1 : 0;
        if (run == k) { bouquets++; run = 0; }
    }
    return bouquets;
}

int minDays(const int *bloomDay, int n, int m, int k) {
    long long need = (long long) m * k;
    if (need > n) return -1;                              // not enough flowers, ever
    int lo = bloomDay[0], hi = bloomDay[0];
    for (int i = 1; i < n; i++) {
        if (bloomDay[i] < lo) lo = bloomDay[i];
        if (bloomDay[i] > hi) hi = bloomDay[i];
    }
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (bouquetsOn(bloomDay, n, mid, k) >= m) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(n log max) time · O(1) space
""",
    "median-of-two-sorted-arrays": r"""
// Binary search the split of the shorter array; the halves must interleave correctly.
double findMedianSortedArrays(const int *a, int n, const int *b, int m) {
    if (n > m) { const int *ta = a; a = b; b = ta; int tt = n; n = m; m = tt; }
    int lo = 0, hi = n, half = (n + m + 1) / 2;
    while (lo <= hi) {
        int i = (lo + hi) / 2, j = half - i;
        long long aLeft = i ? a[i - 1] : LLONG_MIN, aRight = i < n ? a[i] : LLONG_MAX;
        long long bLeft = j ? b[j - 1] : LLONG_MIN, bRight = j < m ? b[j] : LLONG_MAX;
        if (aLeft <= bRight && bLeft <= aRight) {
            long long leftMax = aLeft > bLeft ? aLeft : bLeft;
            if ((n + m) % 2) return (double) leftMax;
            long long rightMin = aRight < bRight ? aRight : bRight;
            return (leftMax + rightMin) / 2.0;
        }
        if (aLeft > bRight) hi = i - 1;
        else lo = i + 1;
    }
    return 0.0;
}   // O(log min(n, m)) time · O(1) space
""",
    "find-minimum-in-rotated-sorted-array-ii": r"""
// With duplicates, shrink the ends when they equal the middle value.
int findMinII(const int *a, int n) {
    int lo = 0, hi = n - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] > a[hi]) lo = mid + 1;
        else if (a[mid] < a[hi]) hi = mid;
        else hi--;                                        // cannot tell: drop the duplicate end
    }
    return a[lo];
}   // O(log n) average, O(n) worst case · O(1) space
""",
    "split-array-largest-sum": r"""
// Binary search the largest allowed sum; feasibility is a greedy grouping.
static int groupsNeeded(const int *a, int n, long long cap) {
    int groups = 1;
    long long sum = 0;
    for (int i = 0; i < n; i++) {
        if (sum + a[i] > cap) { groups++; sum = 0; }
        sum += a[i];
    }
    return groups;
}

long long splitArray(const int *a, int n, int k) {
    long long lo = 0, hi = 0;
    for (int i = 0; i < n; i++) {
        hi += a[i];
        if (a[i] > lo) lo = a[i];
    }
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (groupsNeeded(a, n, mid) <= k) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(n log sum) time · O(1) space
""",
    "kth-smallest-number-in-multiplication-table": r"""
// Count how many products are <= x, then binary search the smallest x with count >= k.
int findKthNumber(int m, int n, int k) {
    int lo = 1, hi = m * n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2, count = 0;
        for (int i = 1; i <= m; i++) count += mid / i < n ? mid / i : n;
        if (count >= k) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(m log(m * n)) time · O(1) space
""",
    "find-k-th-smallest-pair-distance": r"""
// Binary search the distance and count pairs within it with two pointers.
static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}

int smallestDistancePair(int *a, int n, int k) {
    qsort(a, n, sizeof(int), cmpInt);
    int lo = 0, hi = a[n - 1] - a[0];
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2, count = 0, left = 0;
        for (int right = 0; right < n; right++) {
            while (a[right] - a[left] > mid) left++;
            count += right - left;                        // pairs ending at right within mid
        }
        if (count >= k) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(n log range) time · O(1) space
""",
    "preimage-size-of-factorial-zeroes-function": r"""
// Trailing zeros is monotone in the factorial's n, so binary search how many n give k.
static long long zeroesOf(long long n) {
    long long count = 0;
    for (long long p = 5; p <= n; p *= 5) count += n / p;
    return count;
}

int preimageSizeFZF(int k) {
    long long lo = 0, hi = 5LL * (k + 1);
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (zeroesOf(mid) < k) lo = mid + 1;
        else hi = mid;
    }
    return zeroesOf(lo) == k ? 5 : 0;                     // five consecutive n share a value
}   // O(log k) time · O(1) space
""",
    "nth-magical-number": r"""
// Count values divisible by a or b with inclusion-exclusion, then binary search.
static long long gcdLL(long long a, long long b) {
    while (b) { long long t = a % b; a = b; b = t; }
    return a;
}

int nthMagicalNumber(int n, int a, int b) {
    long long lcm = (long long) a / gcdLL(a, b) * b;
    long long lo = 1, hi = (long long) n * (a < b ? a : b);
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        long long count = mid / a + mid / b - mid / lcm;
        if (count >= n) hi = mid;
        else lo = mid + 1;
    }
    return (int) (lo % 1000000007);
}   // O(log(n * min(a, b))) time · O(1) space
""",
    "super-egg-drop": r"""
// moves(k, m) is the number of floors coverable with k eggs and m moves:
// one move either breaks an egg or does not, so it doubles the covered range.
int superEggDrop(int k, int n) {
    int *dp = calloc((size_t) k + 1, sizeof(int));
    int moves = 0;
    while (dp[k] < n) {
        moves++;
        for (int e = k; e >= 1; e--)
            dp[e] = dp[e] + dp[e - 1] + 1;
    }
    free(dp);
    return moves;
}   // O(k log n) time · O(k) space
""",
    "find-in-mountain-array": r"""
// The peak is found by binary search, then both slopes are searched.
int findInMountainArray(int target, int (*get)(int), int length) {
    int lo = 0, hi = length - 1;
    while (lo < hi) {                                     // locate the peak
        int mid = lo + (hi - lo) / 2;
        if (get(mid) < get(mid + 1)) lo = mid + 1;
        else hi = mid;
    }
    int peak = lo;
    lo = 0; hi = peak;                                    // ascending half
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int v = get(mid);
        if (v == target) return mid;
        if (v < target) lo = mid + 1;
        else hi = mid - 1;
    }
    lo = peak; hi = length - 1;                           // descending half
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int v = get(mid);
        if (v == target) return mid;
        if (v > target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}   // O(log n) time · O(1) space
""",
    "divide-chocolate": r"""
// Maximum chunk sum that still allows k + 1 chunks with at least that sum each.
int maximizeSweetness(const int *sweetness, int n, int k) {
    long long lo = 0, hi = 0;
    for (int i = 0; i < n; i++) hi += sweetness[i];
    while (lo < hi) {
        long long mid = lo + (hi - lo + 1) / 2;           // upper mid: we maximise
        long long sum = 0;
        int chunks = 0;
        for (int i = 0; i < n; i++) {
            sum += sweetness[i];
            if (sum >= mid) { chunks++; sum = 0; }
        }
        if (chunks >= k + 1) lo = mid;
        else hi = mid - 1;
    }
    return (int) lo;
}   // O(n log sum) time · O(1) space
""",
    "k-th-smallest-in-lexicographical-order": r"""
// Count how many numbers start with a given prefix, then walk down the tree.
static long long countWithPrefix(long long prefix, long long n) {
    long long count = 0;
    for (long long first = prefix, last = prefix; first <= n; first *= 10, last = last * 10 + 9) {
        long long hi = last < n ? last : n;
        count += hi - first + 1;
    }
    return count;
}

int findKthNumber(int n, int k) {
    long long cur = 1;
    for (long long remaining = k - 1; remaining > 0; ) {
        long long count = countWithPrefix(cur, n);
        if (count <= remaining) { cur++; remaining -= count; }   // skip this whole subtree
        else { cur *= 10; remaining--; }                         // go one level deeper
    }
    return (int) cur;
}   // O(log n * log n) time · O(1) space
""",
    "maximum-running-time-of-n-computers": r"""
// Feasibility: every computer can run for at most `limit`, batteries can be split.
static int feasible(const int *b, int n, long long limit, int computers) {
    long long total = 0;
    for (int i = 0; i < n; i++) total += b[i] < limit ? b[i] : limit;
    return total >= limit * computers;
}

long long maxRunTime(int n, int *batteries, int batteryCount) {
    long long lo = 0, hi = 0;
    for (int i = 0; i < batteryCount; i++) hi += batteries[i];
    hi /= n;                                              // no computer can run longer than this
    while (lo < hi) {
        long long mid = lo + (hi - lo + 1) / 2;
        if (feasible(batteries, batteryCount, mid, n)) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}   // O(n log sum) time · O(1) space
""",
}
