# Topic 2 · Two Pointers & Sliding Window — C17 solutions
CODE = {
    "two-sum-sorted": r"""
// Sorted input: move the smaller side up, the larger side down — the pair is unique.
// `out` receives the two 0-based indices.
void twoSumSorted(const int *a, int n, int target, int *out) {
    int i = 0, j = n - 1;
    while (i < j) {
        long long sum = (long long) a[i] + a[j];
        if (sum == target) { out[0] = i; out[1] = j; return; }
        if (sum < target) i++;
        else j--;
    }
    out[0] = out[1] = -1;
}   // O(n) time · O(1) space
""",
    "remove-element-in-place": r"""
// Write pointer keeps every value that is not `val`.
int removeElement(int *a, int n, int val) {
    int w = 0;
    for (int i = 0; i < n; i++)
        if (a[i] != val) a[w++] = a[i];
    return w;
}   // O(n) time · O(1) space
""",
    "merge-two-sorted-arrays": r"""
// Merge into a fresh buffer — the two inputs are never written to.
void mergeSorted(const int *a, int n, const int *b, int m, int *out) {
    int i = 0, j = 0, k = 0;
    while (i < n && j < m) out[k++] = a[i] <= b[j] ? a[i++] : b[j++];
    while (i < n) out[k++] = a[i++];
    while (j < m) out[k++] = b[j++];
}   // O(n + m) time · O(1) extra space (the output holds the result)
""",
    "is-subsequence": r"""
// Walk t once, advancing s only when the characters match.
int isSubsequence(const char *s, const char *t) {
    int i = 0, j = 0;
    while (s[i] && t[j]) {
        if (s[i] == t[j]) i++;
        j++;
    }
    return s[i] == '\0';                                  // true when s ran out first
}   // O(n + m) time · O(1) space
""",
    "max-average-subarray-k": r"""
// Fixed-size window: add the entering element, drop the leaving one.
double maxAverage(const int *a, int n, int k) {
    long long sum = 0;
    for (int i = 0; i < k; i++) sum += a[i];
    long long best = sum;
    for (int i = k; i < n; i++) {
        sum += a[i] - a[i - k];
        if (sum > best) best = sum;
    }
    return (double) best / k;
}   // O(n) time · O(1) space
""",
    "squares-of-sorted-array": r"""
// The largest square is at one of the two ends, so fill the output from the back.
void sortedSquares(const int *a, int n, int *out) {
    int i = 0, j = n - 1, w = n - 1;
    while (i <= j) {
        long long lo = (long long) a[i] * a[i], hi = (long long) a[j] * a[j];
        out[w--] = lo > hi ? (int) lo : (int) hi;
        if (lo > hi) i++; else j--;
    }
}   // O(n) time · O(1) extra space
""",
    "longest-substring-no-repeat": r"""
// Sliding window with the last seen position of each character.
int lengthOfLongestSubstring(const char *s) {
    int last[256];
    for (int i = 0; i < 256; i++) last[i] = -1;
    int best = 0, start = 0;
    for (int i = 0; s[i]; i++) {
        unsigned char c = (unsigned char) s[i];
        if (last[c] >= start) start = last[c] + 1;        // jump past the previous copy
        last[c] = i;
        if (i - start + 1 > best) best = i - start + 1;
    }
    return best;
}   // O(n) time · O(1) space
""",
    "min-size-subarray-sum": r"""
// Grow the window to the right, then shrink it from the left while it still works.
int minSubArrayLen(int target, const int *a, int n) {
    int best = n + 1, left = 0;
    long long sum = 0;
    for (int right = 0; right < n; right++) {
        sum += a[right];
        while (sum >= target) {
            if (right - left + 1 < best) best = right - left + 1;
            sum -= a[left++];
        }
    }
    return best <= n ? best : 0;
}   // O(n) time · O(1) space
""",
    "longest-substring-k-distinct": r"""
// Window plus a count per character; shrink while more than k distinct letters are inside.
int lengthOfLongestSubstringKDistinct(const char *s, int k) {
    if (k == 0) return 0;
    int count[256] = {0}, distinct = 0, best = 0, left = 0;
    for (int right = 0; s[right]; right++) {
        unsigned char c = (unsigned char) s[right];
        if (count[c]++ == 0) distinct++;
        while (distinct > k) {
            unsigned char d = (unsigned char) s[left++];
            if (--count[d] == 0) distinct--;
        }
        if (right - left + 1 > best) best = right - left + 1;
    }
    return best;
}   // O(n) time · O(1) space
""",
    "three-sum": r"""
// Sort, then fix one value and solve two-sum with two pointers.
static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}

int threeSum(int *a, int n, int *out, int *outCount) {
    qsort(a, n, sizeof(int), cmpInt);
    int k = 0;
    for (int i = 0; i + 2 < n; i++) {
        if (i && a[i] == a[i - 1]) continue;              // skip duplicate first values
        int lo = i + 1, hi = n - 1;
        while (lo < hi) {
            long long sum = (long long) a[i] + a[lo] + a[hi];
            if (sum == 0) {
                out[k++] = a[i]; out[k++] = a[lo]; out[k++] = a[hi];
                while (lo < hi && a[lo] == a[lo + 1]) lo++;   // skip duplicates on both sides
                while (lo < hi && a[hi] == a[hi - 1]) hi--;
                lo++; hi--;
            } else if (sum < 0) lo++;
            else hi--;
        }
    }
    *outCount = k / 3;
    return k / 3;
}   // O(n^2) time · O(1) extra space (beyond sorting)
""",
    "three-sum-closest": r"""
// Same two-pointer sweep, but keep the sum closest to the target.
static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}

int threeSumClosest(int *a, int n, int target) {
    qsort(a, n, sizeof(int), cmpInt);
    long long best = (long long) a[0] + a[1] + a[2];
    for (int i = 0; i + 2 < n; i++) {
        int lo = i + 1, hi = n - 1;
        while (lo < hi) {
            long long sum = (long long) a[i] + a[lo] + a[hi];
            if (llabs(sum - target) < llabs(best - target)) best = sum;
            if (sum < target) lo++;
            else if (sum > target) hi--;
            else return target;                           // exact hit — cannot do better
        }
    }
    return (int) best;
}   // O(n^2) time · O(1) extra space
""",
    "four-sum": r"""
// Sort, then two nested fixed values and a two-pointer sweep for the rest.
static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}

int fourSum(int *a, int n, int target, int *out, int *outCount) {
    qsort(a, n, sizeof(int), cmpInt);
    int k = 0;
    for (int i = 0; i + 3 < n; i++) {
        if (i && a[i] == a[i - 1]) continue;
        for (int j = i + 1; j + 2 < n; j++) {
            if (j > i + 1 && a[j] == a[j - 1]) continue;
            int lo = j + 1, hi = n - 1;
            while (lo < hi) {
                long long sum = (long long) a[i] + a[j] + a[lo] + a[hi];
                if (sum == target) {
                    out[k++] = a[i]; out[k++] = a[j]; out[k++] = a[lo]; out[k++] = a[hi];
                    while (lo < hi && a[lo] == a[lo + 1]) lo++;
                    while (lo < hi && a[hi] == a[hi - 1]) hi--;
                    lo++; hi--;
                } else if (sum < target) lo++;
                else hi--;
            }
        }
    }
    *outCount = k / 4;
    return k / 4;
}   // O(n^3) time · O(1) extra space
""",
    "character-replacement": r"""
// A window is valid when (window length - most frequent letter) <= k.
int characterReplacement(const char *s, int k) {
    int count[26] = {0}, best = 0, left = 0, maxFreq = 0;
    for (int right = 0; s[right]; right++) {
        int c = s[right] - 'A';
        if (c < 0 || c > 25) continue;
        if (++count[c] > maxFreq) maxFreq = count[c];
        while (right - left + 1 - maxFreq > k) count[s[left++] - 'A']--;
        if (right - left + 1 > best) best = right - left + 1;
    }
    return best;
}   // O(n) time · O(1) space
""",
    "permutation-in-string": r"""
// A fixed window of |s1| characters: the counts must match exactly.
int checkInclusion(const char *s1, const char *s2) {
    int n1 = (int) strlen(s1), n2 = (int) strlen(s2);
    if (n1 > n2) return 0;
    int need[26] = {0}, have[26] = {0};
    for (int i = 0; i < n1; i++) { need[s1[i] - 'a']++; have[s2[i] - 'a']++; }
    for (int i = 0; ; i++) {
        if (!memcmp(need, have, sizeof(int) * 26)) return 1;      // true
        if (i + n1 >= n2) return 0;                              // false
        have[s2[i] - 'a']--;
        have[s2[i + n1] - 'a']++;
    }
}   // O(n) time · O(1) space
""",
    "find-all-anagrams": r"""
// Same sliding counts as permutation-in-string, but every valid start is recorded.
int findAnagrams(const char *s, const char *p, int *out) {
    int n = (int) strlen(s), m = (int) strlen(p), k = 0;
    if (m > n) return 0;
    int need[26] = {0}, have[26] = {0};
    for (int i = 0; i < m; i++) { need[p[i] - 'a']++; have[s[i] - 'a']++; }
    for (int i = 0; ; i++) {
        if (!memcmp(need, have, sizeof(int) * 26)) out[k++] = i;
        if (i + m >= n) break;
        have[s[i] - 'a']--;
        have[s[i + m] - 'a']++;
    }
    return k;
}   // O(n) time · O(1) space
""",
    "subarray-product-less-than-k": r"""
// All positive: a window whose product stays below k; every position adds its width.
int numSubarrayProductLessThanK(const int *a, int n, int k) {
    if (k <= 1) return 0;
    long long prod = 1;
    int left = 0, count = 0;
    for (int right = 0; right < n; right++) {
        prod *= a[right];
        while (prod >= k) prod /= a[left++];
        count += right - left + 1;                        // windows ending at `right`
    }
    return count;
}   // O(n) time · O(1) space
""",
    "boats-to-save-people": r"""
// Sort, then pair the heaviest with the lightest when they fit together.
static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}

int numRescueBoats(int *people, int n, int limit) {
    qsort(people, n, sizeof(int), cmpInt);
    int i = 0, j = n - 1, boats = 0;
    while (i <= j) {
        if ((long long) people[i] + people[j] <= limit) i++;   // the lightest fits too
        j--;
        boats++;
    }
    return boats;
}   // O(n log n) time · O(1) space
""",
    "sorted-array-intersection-two": r"""
// Two indices over sorted arrays: equal → record and advance both, else advance the smaller.
int intersectSorted(const int *a, int n, const int *b, int m, int *out) {
    int i = 0, j = 0, k = 0;
    while (i < n && j < m) {
        if (a[i] == b[j]) { out[k++] = a[i]; i++; j++; }
        else if (a[i] < b[j]) i++;
        else j++;
    }
    return k;
}   // O(n + m) time · O(1) space
""",
    "minimum-window-substring": r"""
// Expand until every needed letter is covered, then shrink from the left.
char *minWindow(const char *s, const char *t) {
    int need[256] = {0};
    int required = 0;
    for (int i = 0; t[i]; i++)
        if (need[(unsigned char) t[i]]++ == 0) required++;
    int have[256] = {0}, formed = 0, left = 0, bestLen = INT_MAX, bestStart = 0;
    for (int right = 0; s[right]; right++) {
        unsigned char c = (unsigned char) s[right];
        if (++have[c] == need[c]) formed++;
        while (formed == required) {                      // shrink while still valid
            if (right - left + 1 < bestLen) { bestLen = right - left + 1; bestStart = left; }
            unsigned char d = (unsigned char) s[left++];
            if (have[d]-- == need[d]) formed--;
        }
    }
    if (bestLen == INT_MAX) bestLen = 0;
    char *out = malloc((size_t) bestLen + 1);
    memcpy(out, s + bestStart, (size_t) bestLen);
    out[bestLen] = '\0';
    return out;
}   // O(n + m) time · O(1) space
""",
    "substring-concatenation-all-words": r"""
// Slide a window of |words| * wordLen over s and compare counts word by word.
static int wordAt(const char *s, char **words, int wordLen, int count) {
    for (int i = 0; i < count; i++)
        if (!strncmp(s, words[i], (size_t) wordLen)) return i;
    return -1;
}

int findSubstring(const char *s, char **words, int wordCount, int *out) {
    int n = (int) strlen(s);
    if (!wordCount) return 0;
    int wordLen = (int) strlen(words[0]), total = wordLen * wordCount, hits = 0;
    for (int start = 0; start + total <= n; start++) {
        int used[64] = {0};
        int ok = 1;
        for (int w = 0; w < wordCount; w++) {
            int id = wordAt(s + start + w * wordLen, words, wordLen, wordCount);
            if (id < 0 || used[id]++ >= 1) { ok = 0; break; }    // unknown or repeated word
        }
        if (ok) out[hits++] = start;
    }
    return hits;
}   // O(n * wordCount) time · O(wordCount) space
""",
    "sliding-window-maximum": r"""
// A deque of indices whose values are decreasing: the front is always the window maximum.
void maxSlidingWindow(const int *a, int n, int k, int *out, int *outSize) {
    int *dq = malloc(sizeof(int) * (size_t) (n + 1));
    int head = 0, tail = 0, w = 0;
    for (int i = 0; i < n; i++) {
        while (tail > head && a[dq[tail - 1]] <= a[i]) tail--;   // drop smaller values
        dq[tail++] = i;
        if (dq[head] <= i - k) head++;                           // drop the element leaving the window
        if (i >= k - 1) out[w++] = a[dq[head]];
    }
    free(dq);
    *outSize = w;
}   // O(n) time · O(k) space
""",
    "smallest-range-k-lists": r"""
// K sorted lists: always advance the list that currently holds the minimum.
void smallestRange(int lists[][6], const int *sizes, int k, int *out) {
    int idx[32];
    for (int i = 0; i < k; i++) idx[i] = 0;
    int bestLo = 0, bestHi = INT_MAX;
    while (1) {
        int lo = INT_MAX, hi = INT_MIN, which = -1;
        for (int i = 0; i < k; i++) {
            int v = lists[i][idx[i]];
            if (v < lo) { lo = v; which = i; }
            if (v > hi) hi = v;
        }
        if (hi - lo < bestHi - bestLo) { bestLo = lo; bestHi = hi; }
        if (++idx[which] >= sizes[which]) break;          // that list ran out
    }
    out[0] = bestLo;
    out[1] = bestHi;
}   // O(n * k) time · O(k) space
""",
    "k-consecutive-bit-flips": r"""
// Greedy left to right: a zero can only be fixed by a flip starting here.
int minKBitFlips(int *a, int n, int k) {
    int *flip = calloc((size_t) n, sizeof(int));
    int flips = 0, active = 0;
    for (int i = 0; i < n; i++) {
        if (i >= k) active ^= flip[i - k];                // the flip that just expired
        if ((a[i] ^ active) == 0) {
            if (i + k > n) { free(flip); return -1; }      // cannot reach the end
            flip[i] = 1;
            active ^= 1;
            flips++;
        }
    }
    free(flip);
    return flips;
}   // O(n) time · O(n) space
""",
    "minimum-window-subsequence": r"""
// dp[j] = best start for matching the first j characters of t, scanned over s.
char *minWindowSubsequence(const char *s, const char *t) {
    int n = (int) strlen(s), m = (int) strlen(t);
    int *start = malloc(sizeof(int) * (size_t) (m + 1));
    for (int j = 0; j <= m; j++) start[j] = -1;
    int best = INT_MAX, bestStart = 0;
    for (int i = 0; i < n; i++) {
        for (int j = m - 1; j >= 0; j--) {                // backwards: use this s[i] once
            if (s[i] == t[j]) start[j + 1] = (j == 0) ? i : start[j];
        }
        if (start[m] >= 0 && i - start[m] + 1 < best) { best = i - start[m] + 1; bestStart = start[m]; }
    }
    free(start);
    if (best == INT_MAX) best = 0;
    char *out = malloc((size_t) best + 1);
    memcpy(out, s + bestStart, (size_t) best);
    out[best] = '\0';
    return out;
}   // O(n * m) time · O(m) space
""",
    "substrings-containing-three-chars": r"""
// Count windows ending at `right` that contain all three letters.
int numberOfSubstrings(const char *s) {
    int last[3] = {-1, -1, -1}, total = 0;
    for (int i = 0; s[i]; i++) {
        last[s[i] - 'a'] = i;
        if (last[0] >= 0 && last[1] >= 0 && last[2] >= 0) {
            int mn = last[0] < last[1] ? last[0] : last[1];
            if (last[2] < mn) mn = last[2];
            total += mn + 1;                              // every start up to the oldest last-seen
        }
    }
    return total;
}   // O(n) time · O(1) space
""",
    "kth-smallest-prime-fraction": r"""
// Fractional binary search on the value, then one exact pass to pick the k-th pair.
void kthSmallestPrimeFraction(const int *a, int n, int k, int *out) {
    double lo = 0.0, hi = 1.0;
    int bestNum = 0, bestDen = 1;
    while (hi - lo > 1e-9) {
        double mid = (lo + hi) / 2;
        int count = 0, j = 1;
        int num = 0, den = 1;
        for (int i = 0; i < n - 1; i++) {
            while (j < n && a[i] > mid * a[j]) j++;
            count += n - j;
            if (j < n && (long long) a[i] * den > (long long) num * a[j]) { num = a[i]; den = a[j]; }
        }
        if (count >= k) { hi = mid; bestNum = num; bestDen = den; }
        else lo = mid;
    }
    out[0] = bestNum;
    out[1] = bestDen;
}   // O(n log(1/eps)) time · O(1) space
""",
    "min-operations-reduce-x": r"""
// Removing a prefix and a suffix is keeping one contiguous middle of sum total - x.
int minOperations(const int *a, int n, int x) {
    long long total = 0;
    for (int i = 0; i < n; i++) total += a[i];
    long long need = total - x;
    if (need < 0) return -1;
    int best = -1, left = 0;
    long long sum = 0;
    for (int right = 0; right < n; right++) {
        sum += a[right];
        while (sum > need && left <= right) sum -= a[left++];
        if (sum == need && right - left + 1 > best) best = right - left + 1;
    }
    return best < 0 ? -1 : n - best;
}   // O(n) time · O(1) space
""",
    "constrained-subsequence-sum": r"""
// Monotonic deque over the last k best subsequence sums.
int constrainedSubsetSum(const int *a, int n, int k) {
    int *dq = malloc(sizeof(int) * (size_t) (n + 1));
    long long *dp = malloc(sizeof(long long) * (size_t) n);
    int head = 0, tail = 0;
    long long best = LLONG_MIN;
    for (int i = 0; i < n; i++) {
        while (tail > head && dq[head] < i - k) head++;         // outside the window
        long long take = a[i];
        if (tail > head) take += dp[dq[head]] > 0 ? dp[dq[head]] : 0;
        dp[i] = take;
        while (tail > head && dp[dq[tail - 1]] <= dp[i]) tail--;
        dq[tail++] = i;
        if (dp[i] > best) best = dp[i];
    }
    free(dq); free(dp);
    return (int) best;
}   // O(n) time · O(n) space
""",
    "maximum-score-two-arrays": r"""
// Two pointers walking the common values, keeping the running sum of each array.
long long maxScore(const int *a, int n, const int *b, int m) {
    long long sumA = 0, sumB = 0;
    int i = 0, j = 0;
    while (i < n && j < m) {
        if (a[i] < b[j]) sumA += a[i++];
        else if (a[i] > b[j]) sumB += b[j++];
        else { sumA = sumB = (sumA > sumB ? sumA : sumB) + a[i]; i++; j++; }
    }
    while (i < n) sumA += a[i++];
    while (j < m) sumB += b[j++];
    return sumA > sumB ? sumA : sumB;
}   // O(n + m) time · O(1) space
""",
    "count-subarrays-fixed-bounds": r"""
// Count subarrays whose min and max are exactly minK and maxK: split at out-of-range
// values and subtract subarrays that miss one of the two bounds.
long long countSubarraysFixedBounds(const int *a, int n, int minK, int maxK) {
    long long total = 0;
    int lastMin = -1, lastMax = -1, bad = -1;
    for (int i = 0; i < n; i++) {
        if (a[i] < minK || a[i] > maxK) bad = i;
        if (a[i] == minK) lastMin = i;
        if (a[i] == maxK) lastMax = i;
        int first = lastMin < lastMax ? lastMin : lastMax;
        if (first > bad) total += first - bad;
    }
    return total;
}   // O(n) time · O(1) space
""",
}
