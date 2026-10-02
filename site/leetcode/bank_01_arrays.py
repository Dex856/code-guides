# Topic 1 · Arrays & Strings — foundations
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.
# Every problem states the task, one or two examples, the constraints, the approach,
# a complete solution in C++ / Java / Python, and the complexity.

TOPIC = {
    "name": "Arrays & Strings — foundations",
    "tagline": "Index arithmetic, in-place editing, and the scans that almost every other topic builds on.",
    "focus": "Reading and rewriting an array or string in one or two passes: prefix state, write pointers, "
             "Kadane-style accumulation, matrix index maths, and the two-pointer family — without extra memory "
             "where the problem forbids it.",
    "ordering": "easy 1–6 introduce one scan each; medium 1–4 are single-pass state, 5–8 are matrix/grid index maths, "
                "9–12 are string scanning; hard 1–4 are in-place/O(1)-space classics, 5–8 are amortised and divide-and-conquer "
                "counts, 9–12 are string algorithms and the two famous 'big' array problems.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "largest-and-second-largest",
        "title": "Largest and Second Largest in One Pass",
        "difficulty": "Easy",
        "pattern": "single-pass state (two variables)",
        "statement": "Given an array of n integers, return the largest value and the second largest **distinct** value. "
                     "If there is no second distinct value, return -1 for it.",
        "examples": [("[3, 1, 9, 4, 9]", "9 4   (second distinct largest)"),
                     ("[5, 5, 5]", "5 -1")],
        "constraints": ["1 <= n <= 10^5", "-10^9 <= a[i] <= 10^9"],
        "approach": "Keep the best and runner-up while scanning once. Update `best` first and push the old `best` down "
                    "to `second` only when the new value is strictly smaller than `best` — that single condition handles "
                    "duplicates for free. Sorting also works but is O(n log n) for no reason.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Largest and second largest distinct value in one pass
pair<int,int> topTwo(const vector<int>& a) {
    long long best = LLONG_MIN, second = LLONG_MIN;
    for (int v : a) {
        if (v > best) { second = best; best = v; }      // new maximum demotes the old one
        else if (v < best && v > second) second = v;    // strict < best removes duplicates
    }
    return {best, second == LLONG_MIN ? -1 : second};
}   // O(n) time · O(1) space""",
            "java": r"""// Largest and second largest distinct value in one pass
long[] topTwo(int[] a) {
    long best = Long.MIN_VALUE, second = Long.MIN_VALUE;
    for (int v : a) {
        if (v > best) { second = best; best = v; }      // new maximum demotes the old one
        else if (v < best && v > second) second = v;    // strict < best removes duplicates
    }
    return new long[]{best, second == Long.MIN_VALUE ? -1 : second};
}   // O(n) time · O(1) space""",
            "python": r"""def top_two(a):
    # returns (largest, second largest distinct); second is -1 when absent
    best = second = float("-inf")
    for v in a:
        if v > best:
            best, second = v, best          # new maximum demotes the old one
        elif best > v > second:             # strict '< best' removes duplicates
            second = v
    return best, (-1 if second == float("-inf") else second)
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "reverse-array-in-place",
        "title": "Reverse an Array In Place",
        "difficulty": "Easy",
        "pattern": "opposite-end swap",
        "statement": "Reverse the given array of n integers in place (no second array), then return it.",
        "examples": [("[1, 2, 3, 4, 5]", "[5, 4, 3, 2, 1]"),
                     ("[7]", "[7]")],
        "constraints": ["1 <= n <= 10^5"],
        "approach": "Two indices walk toward each other and swap until they meet. Each element moves exactly once, so "
                    "the cost is n/2 swaps; the middle element of an odd-length array is never touched.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Reverse in place: swap from both ends inward
void reverseArray(vector<int>& a) {
    for (int i = 0, j = (int)a.size() - 1; i < j; i++, j--) swap(a[i], a[j]);
}   // O(n) time · O(1) space

// The library one-liner (same cost, clearer intent)
// reverse(a.begin(), a.end());""",
            "java": r"""// Reverse in place: swap from both ends inward
void reverseArray(int[] a) {
    for (int i = 0, j = a.length - 1; i < j; i++, j--) { int t = a[i]; a[i] = a[j]; a[j] = t; }
}   // O(n) time · O(1) space""",
            "python": r"""def reverse_array(a):
    i, j = 0, len(a) - 1
    while i < j:
        a[i], a[j] = a[j], a[i]      # Python swaps without a temporary
        i, j = i + 1, j - 1
    return a
# O(n) time · O(1) space (the swaps are in place)""",
        },
    },
    {
        "slug": "count-above-average",
        "title": "Count Elements Greater Than the Average",
        "difficulty": "Easy",
        "pattern": "two passes with an accumulated statistic",
        "statement": "Return how many elements of an integer array are strictly greater than the arithmetic mean of the array.",
        "examples": [("[1, 2, 3, 4]", "2   (average 2.5, so 3 and 4 qualify)"),
                     ("[5, 5, 5]", "0")],
        "constraints": ["1 <= n <= 10^5", "-10^4 <= a[i] <= 10^4"],
        "approach": "First pass sums the values, second pass counts elements above `sum / n`. The trap is overflow: in "
                    "Java and C++ the sum of 10^5 values can exceed a 32-bit int, so accumulate in a 64-bit integer. "
                    "Comparing against `sum > 0` avoids the division entirely when you want to stay exact.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Count values strictly above the mean — accumulate in long long
int countAboveAverage(const vector<int>& a) {
    long long sum = 0;
    for (int v : a) sum += v;
    int cnt = 0;
    for (int v : a) if (v * (long long)a.size() > sum) cnt++;   // compare without floating point
    return cnt;
}   // O(n) time · O(1) space""",
            "java": r"""// Count values strictly above the mean — accumulate in long
int countAboveAverage(int[] a) {
    long sum = 0;
    for (int v : a) sum += v;
    int cnt = 0;
    for (int v : a) if ((long) v * a.length > sum) cnt++;      // exact integer comparison
    return cnt;
}   // O(n) time · O(1) space""",
            "python": r"""def count_above_average(a):
    total = sum(a)                    # Python ints do not overflow
    n = len(a)
    return sum(1 for v in a if v * n > total)   # exact: no float rounding
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "move-zeroes",
        "title": "Move Zeroes to the End (Stable)",
        "difficulty": "Easy",
        "pattern": "write pointer",
        "statement": "Move every zero in the array to the end while keeping the relative order of the non-zero elements, "
                     "using O(1) extra space.",
        "examples": [("[0, 1, 0, 3, 12]", "[1, 3, 12, 0, 0]"),
                     ("[0, 0, 1]", "[1, 0, 0]")],
        "constraints": ["1 <= n <= 10^4"],
        "approach": "One index writes the compacted non-zero prefix while a second index reads. After the read loop, the "
                    "tail from the write index onward is zeroed. This is the model for every \"remove in place\" problem.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Stable partition: non-zero front, zeros back
void moveZeroes(vector<int>& a) {
    int w = 0;                                  // write pointer
    for (int v : a) if (v != 0) a[w++] = v;      // compact the non-zero values
    while (w < (int)a.size()) a[w++] = 0;        // fill the tail
}   // O(n) time · O(1) space""",
            "java": r"""// Stable partition: non-zero front, zeros back
void moveZeroes(int[] a) {
    int w = 0;                                  // write pointer
    for (int v : a) if (v != 0) a[w++] = v;      // compact the non-zero values
    while (w < a.length) a[w++] = 0;             // fill the tail
}   // O(n) time · O(1) space""",
            "python": r"""def move_zeroes(a):
    w = 0                                    # write pointer
    for v in a:
        if v != 0:
            a[w] = v
            w += 1
    for i in range(w, len(a)):               # fill the tail
        a[i] = 0
    return a
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "dedupe-sorted-in-place",
        "title": "Remove Duplicates from a Sorted Array In Place",
        "difficulty": "Easy",
        "pattern": "write pointer with the last written value",
        "statement": "Given a sorted array, remove the duplicates in place so each value appears once, and return the new "
                     "length k. The first k slots of the array must hold the result; anything beyond k is ignored.",
        "examples": [("[1, 1, 2]", "k = 2, array starts [1, 2]"),
                     ("[0, 0, 1, 1, 1, 2, 2]", "k = 3, array starts [0, 1, 2]")],
        "constraints": ["1 <= n <= 3 * 10^4", "the array is sorted in non-decreasing order"],
        "approach": "Compare each value with the last value written: if it differs it is new and gets written at the "
                    "write pointer. Because the array is sorted, all equal values are adjacent, so one comparison "
                    "suffices — no hash set needed.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Sorted input: duplicates are adjacent, so one comparison per element
int removeDuplicates(vector<int>& a) {
    int w = 0;
    for (int v : a)
        if (w == 0 || a[w - 1] != v) a[w++] = v;   // only new values are written
    return w;
}   // O(n) time · O(1) space""",
            "java": r"""// Sorted input: duplicates are adjacent, so one comparison per element
int removeDuplicates(int[] a) {
    int w = 0;
    for (int v : a)
        if (w == 0 || a[w - 1] != v) a[w++] = v;   // only new values are written
    return w;
}   // O(n) time · O(1) space""",
            "python": r"""def remove_duplicates(a):
    w = 0
    for v in a:
        if w == 0 or a[w - 1] != v:
            a[w] = v
            w += 1
    return w                      # a[:w] is the answer
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "rotate-array-by-k",
        "title": "Rotate an Array Right by k Steps",
        "difficulty": "Easy",
        "pattern": "three reversals",
        "statement": "Rotate the array of n integers to the right by k steps, in place, where k can be larger than n.",
        "examples": [("[1, 2, 3, 4, 5, 6, 7], k = 3", "[5, 6, 7, 1, 2, 3, 4]"),
                     ("[1, 2], k = 5", "[2, 1]   (5 mod 2 = 1 step)")],
        "constraints": ["1 <= n <= 10^5", "0 <= k <= 10^9"],
        "approach": "Reduce k modulo n (this is what makes k > n harmless), then reverse the whole array, reverse the "
                    "first k elements, and reverse the rest. Rotating left by k instead means reversing the last n-k "
                    "elements and the first k, in that order.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Rotate right by k using three reversals
void rotateRight(vector<int>& a, long long k) {
    int n = a.size();
    k %= n;                                          // k may exceed n
    reverse(a.begin(), a.end());
    reverse(a.begin(), a.begin() + k);
    reverse(a.begin() + k, a.end());
}   // O(n) time · O(1) space

// Rotate LEFT by k: reverse(a.begin(), a.begin() + n - k); reverse(a.begin() + n - k, a.end()); reverse(all);""",
            "java": r"""// Rotate right by k using three reversals
void rotateRight(int[] a, int k) {
    int n = a.length;
    k %= n;                                          // k may exceed n
    reverse(a, 0, n - 1);
    reverse(a, 0, k - 1);
    reverse(a, k, n - 1);
}
void reverse(int[] a, int i, int j) {                 // inclusive range
    for (; i < j; i++, j--) { int t = a[i]; a[i] = a[j]; a[j] = t; }
}   // O(n) time · O(1) space""",
            "python": r"""def rotate_right(a, k):
    n = len(a)
    k %= n                        # k may exceed n
    def rev(i, j):                # reverse the inclusive range [i, j]
        while i < j:
            a[i], a[j] = a[j], a[i]
            i, j = i + 1, j - 1
    rev(0, n - 1)                 # whole array
    rev(0, k - 1)                 # first k
    rev(k, n - 1)                 # the rest
    return a
# O(n) time · O(1) space""",
        },
    },

    # ---------------------------------------------------------------- MEDIUM
    {
        "slug": "maximum-subarray-sum",
        "title": "Maximum Subarray Sum (Kadane)",
        "difficulty": "Medium",
        "pattern": "DP over ending positions",
        "statement": "Return the largest possible sum of a non-empty contiguous subarray of an integer array.",
        "examples": [("[-2, 1, -3, 4, -1, 2, 1, -5, 4]", "6   (the subarray [4, -1, 2, 1])"),
                     ("[-3, -1, -7]", "-1   (the best single element)")],
        "constraints": ["1 <= n <= 10^5", "-10^4 <= a[i] <= 10^4"],
        "approach": "Let `cur` be the best sum of a subarray that **ends** at the current index: either extend the "
                    "previous run or start fresh at this element. Keep a running maximum of `cur`. The starting rule "
                    "`cur = max(a[i], cur + a[i])` is the entire algorithm.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Kadane: best subarray ending here vs starting fresh
long long maxSubarray(const vector<int>& a) {
    long long best = a[0], cur = a[0];
    for (int i = 1; i < (int)a.size(); i++) {
        cur = max((long long)a[i], cur + a[i]);   // extend or restart
        best = max(best, cur);
    }
    return best;
}   // O(n) time · O(1) space""",
            "java": r"""// Kadane: best subarray ending here vs starting fresh
long maxSubarray(int[] a) {
    long best = a[0], cur = a[0];
    for (int i = 1; i < a.length; i++) {
        cur = Math.max(a[i], cur + a[i]);        // extend or restart
        best = Math.max(best, cur);
    }
    return best;
}   // O(n) time · O(1) space""",
            "python": r"""def max_subarray(a):
    best = cur = a[0]
    for v in a[1:]:
        cur = max(v, cur + v)      # extend the run, or restart at v
        best = max(best, cur)
    return best
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "product-except-self",
        "title": "Product of Array Except Self",
        "difficulty": "Medium",
        "pattern": "two directional prefix passes",
        "statement": "For each index i, return the product of every element except a[i], without using division and in "
                     "O(n) time.",
        "examples": [("[1, 2, 3, 4]", "[24, 12, 8, 6]"),
                     ("[-1, 1, 0, -3, 3]", "[0, 0, 9, 0, 0]")],
        "constraints": ["2 <= n <= 10^5", "-30 <= a[i] <= 30", "the product fits in a 32-bit integer"],
        "approach": "Sweep left to right storing prefix products in the output array, then sweep right to left multiplying "
                    "by a running suffix product. No division is needed, so zeros and negatives are handled automatically "
                    "— which is exactly why the 'product ÷ a[i]' idea fails: it divides by zero and needs two special cases.",
        "complexity": ("O(n)", "O(1) extra (the output array does not count)"),
        "code": {
            "cpp": r"""// Prefix products, then multiply by running suffix products
vector<int> productExceptSelf(const vector<int>& a) {
    int n = a.size();
    vector<int> out(n, 1);
    for (int i = 1; i < n; i++) out[i] = out[i - 1] * a[i - 1];      // out[i] = product of a[0..i-1]
    int suffix = 1;
    for (int i = n - 1; i >= 0; i--) { out[i] *= suffix; suffix *= a[i]; }
    return out;
}   // O(n) time · O(1) extra space""",
            "java": r"""// Prefix products, then multiply by running suffix products
int[] productExceptSelf(int[] a) {
    int n = a.length;
    int[] out = new int[n];
    out[0] = 1;
    for (int i = 1; i < n; i++) out[i] = out[i - 1] * a[i - 1];      // out[i] = product of a[0..i-1]
    int suffix = 1;
    for (int i = n - 1; i >= 0; i--) { out[i] *= suffix; suffix *= a[i]; }
    return out;
}   // O(n) time · O(1) extra space""",
            "python": r"""def product_except_self(a):
    n = len(a)
    out = [1] * n
    for i in range(1, n):
        out[i] = out[i - 1] * a[i - 1]      # prefix products
    suffix = 1
    for i in range(n - 1, -1, -1):
        out[i] *= suffix                    # fold in the suffix
        suffix *= a[i]
    return out
# O(n) time · O(1) extra space""",
        },
    },
    {
        "slug": "sort-colors-three-way",
        "title": "Sort Three Values in One Pass (Dutch Flag)",
        "difficulty": "Medium",
        "pattern": "three-way partition",
        "statement": "An array contains only the values 0, 1 and 2. Sort it in place in a single pass, without counting "
                     "and without a library sort.",
        "examples": [("[2, 0, 2, 1, 1, 0]", "[0, 0, 1, 1, 2, 2]"),
                     ("[2, 0, 1]", "[0, 1, 2]")],
        "constraints": ["1 <= n <= 300", "a[i] is 0, 1 or 2"],
        "approach": "Keep three regions: [0, low) = 0s, [low, mid) = 1s, (high, n-1] = 2s, with mid scanning the unknown "
                    "middle. A 0 swaps to `low`, a 2 swaps to `high` and the element arriving at `mid` must be re-examined "
                    "(so `mid` does not advance in that branch).",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Dutch national flag: three regions in one pass
void sortColors(vector<int>& a) {
    int low = 0, mid = 0, high = (int)a.size() - 1;
    while (mid <= high) {
        if (a[mid] == 0)      swap(a[low++], a[mid++]);
        else if (a[mid] == 1) mid++;
        else                  swap(a[mid], a[high--]);   // do NOT advance mid: a[mid] is new
    }
}   // O(n) time · O(1) space""",
            "java": r"""// Dutch national flag: three regions in one pass
void sortColors(int[] a) {
    int low = 0, mid = 0, high = a.length - 1;
    while (mid <= high) {
        if (a[mid] == 0)      { int t = a[low]; a[low++] = a[mid]; a[mid++] = t; }
        else if (a[mid] == 1) mid++;
        else                  { int t = a[mid]; a[mid] = a[high]; a[high--] = t; }   // re-examine a[mid]
    }
}   // O(n) time · O(1) space""",
            "python": r"""def sort_colors(a):
    low = mid = 0
    high = len(a) - 1
    while mid <= high:
        if a[mid] == 0:
            a[low], a[mid] = a[mid], a[low]
            low += 1; mid += 1
        elif a[mid] == 1:
            mid += 1
        else:
            a[mid], a[high] = a[high], a[mid]   # a[mid] is new: do not advance mid
            high -= 1
    return a
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "majority-element",
        "title": "Majority Element (More Than Half)",
        "difficulty": "Medium",
        "pattern": "Boyer–Moore voting",
        "statement": "Return the element that appears more than floor(n/2) times. The answer is guaranteed to exist.",
        "examples": [("[3, 2, 3]", "3"),
                     ("[2, 2, 1, 1, 1, 2, 2]", "2   (four of the seven elements)")],
        "constraints": ["1 <= n <= 5 * 10^4", "the majority element always exists"],
        "approach": "Throw away pairs of different elements and the majority survives, because it outnumbers everything "
                    "else combined. Boyer–Moore does that in one pass with a candidate and a counter: matching values "
                    "increment, differing values decrement, and hitting zero adopts a new candidate.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Boyer-Moore: cancel pairs of distinct values
int majorityElement(const vector<int>& a) {
    int cand = a[0], count = 0;
    for (int v : a) {
        if (count == 0) cand = v;                 // adopt a new candidate
        count += (v == cand) ? 1 : -1;            // support or cancel
    }
    return cand;                                  // guaranteed to be the majority
}   // O(n) time · O(1) space""",
            "java": r"""// Boyer-Moore: cancel pairs of distinct values
int majorityElement(int[] a) {
    int cand = a[0], count = 0;
    for (int v : a) {
        if (count == 0) cand = v;                 // adopt a new candidate
        count += (v == cand) ? 1 : -1;            // support or cancel
    }
    return cand;                                  // guaranteed to be the majority
}   // O(n) time · O(1) space""",
            "python": r"""def majority_element(a):
    cand = None
    count = 0
    for v in a:
        if count == 0:
            cand = v                  # adopt a new candidate
        count += 1 if v == cand else -1
    return cand
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "best-time-buy-sell-ii",
        "title": "Best Time to Buy and Sell (Unlimited Trades)",
        "difficulty": "Medium",
        "pattern": "greedy over adjacent differences",
        "statement": "Given daily prices, return the maximum profit achievable with any number of trades (buy before "
                     "sell, at most one share held at a time), or 0 if no profit is possible.",
        "examples": [("[7, 1, 5, 3, 6, 4]", "7   (buy 1 sell 5, buy 3 sell 6)"),
                     ("[7, 6, 4, 3, 1]", "0")],
        "constraints": ["1 <= n <= 3 * 10^4", "0 <= price <= 10^4"],
        "approach": "Any multi-day rise decomposes into single-day rises that are each tradable, so summing every "
                    "positive consecutive difference is optimal. With only one trade allowed instead, keep the minimum "
                    "price seen so far and maximise `price - minSoFar` — that variant is one line different.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Unlimited trades: capture every up-day
long long maxProfit(vector<int>& p) {
    long long profit = 0;
    for (int i = 1; i < (int)p.size(); i++)
        if (p[i] > p[i - 1]) profit += p[i] - p[i - 1];   // every rise is tradable
    return profit;
}   // O(n) time · O(1) space

// One trade only:  minSoFar = min(minSoFar, p[i]); best = max(best, p[i] - minSoFar);""",
            "java": r"""// Unlimited trades: capture every up-day
long maxProfit(int[] p) {
    long profit = 0;
    for (int i = 1; i < p.length; i++)
        if (p[i] > p[i - 1]) profit += p[i] - p[i - 1];   // every rise is tradable
    return profit;
}   // O(n) time · O(1) space""",
            "python": r"""def max_profit(p):
    profit = 0
    for i in range(1, len(p)):
        if p[i] > p[i - 1]:
            profit += p[i] - p[i - 1]   # every rise is tradable
    return profit
# O(n) time · O(1) space

# one trade only:
# min_so_far = min(min_so_far, price); best = max(best, price - min_so_far)""",
        },
    },
    {
        "slug": "rotate-matrix-90",
        "title": "Rotate a Matrix 90° Clockwise In Place",
        "difficulty": "Medium",
        "pattern": "transpose + row reversal",
        "statement": "Given an n x n matrix, rotate it 90 degrees clockwise in place.",
        "examples": [("[[1,2,3],[4,5,6],[7,8,9]]", "[[7,4,1],[8,5,2],[9,6,3]]"),
                     ("[[1,2],[3,4]]", "[[3,1],[4,2]]")],
        "constraints": ["1 <= n <= 20"],
        "approach": "A clockwise rotation is the transpose followed by reversing each row. Transposing only needs the "
                    "upper triangle (`j > i`), which halves the work and avoids undoing the swaps. Counter-clockwise is "
                    "the transpose plus reversing each **column** (or reversing the rows first).",
        "complexity": ("O(n²)", "O(1)"),
        "code": {
            "cpp": r"""// Clockwise = transpose, then reverse every row
void rotate(vector<vector<int>>& m) {
    int n = m.size();
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) swap(m[i][j], m[j][i]);   // upper triangle only
    for (int i = 0; i < n; i++) reverse(m[i].begin(), m[i].end());
}   // O(n^2) time · O(1) extra space

// Counter-clockwise = transpose, then reverse the order of the ROWS""",
            "java": r"""// Clockwise = transpose, then reverse every row
void rotate(int[][] m) {
    int n = m.length;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) { int t = m[i][j]; m[i][j] = m[j][i]; m[j][i] = t; }
    for (int[] row : m) for (int l = 0, r = n - 1; l < r; l++, r--) {
        int t = row[l]; row[l] = row[r]; row[r] = t;
    }
}   // O(n^2) time · O(1) extra space""",
            "python": r"""def rotate(m):
    n = len(m)
    for i in range(n):
        for j in range(i + 1, n):          # upper triangle only
            m[i][j], m[j][i] = m[j][i], m[i][j]      # transpose
    for row in m:
        row.reverse()                       # reverse every row
    return m
# O(n^2) time · O(1) extra space""",
        },
    },
    {
        "slug": "spiral-order",
        "title": "Spiral Order of a Matrix",
        "difficulty": "Medium",
        "pattern": "shrinking boundaries",
        "statement": "Return all elements of an m x n matrix in spiral order, starting at the top-left and moving "
                     "right, down, left, up, inward.",
        "examples": [("[[1,2,3],[4,5,6],[7,8,9]]", "[1,2,3,6,9,8,7,4,5]"),
                     ("[[1,2,3,4],[5,6,7,8],[9,10,11,12]]", "[1,2,3,4,8,12,11,10,9,5,6,7]")],
        "constraints": ["1 <= m, n <= 10", "1 <= m*n <= 100"],
        "approach": "Maintain four boundaries (top, bottom, left, right). After walking a side, shrink the corresponding "
                    "boundary. The two `if` guards before the last two sides are essential for non-square matrices — "
                    "without them the middle row or column is emitted twice.",
        "complexity": ("O(m·n)", "O(1) besides the output"),
        "code": {
            "cpp": r"""// Four boundaries, shrunk after each side
vector<int> spiralOrder(vector<vector<int>>& g) {
    vector<int> out;
    int top = 0, bot = g.size() - 1, left = 0, right = g[0].size() - 1;
    while (top <= bot && left <= right) {
        for (int c = left; c <= right; c++) out.push_back(g[top][c]);   top++;
        for (int r = top; r <= bot; r++)  out.push_back(g[r][right]);   right--;
        if (top <= bot) for (int c = right; c >= left; c--) out.push_back(g[bot][c]); bot--;
        if (left <= right) for (int r = bot; r >= top; r--) out.push_back(g[r][left]); left++;
    }
    return out;
}   // O(m*n) time · O(1) extra space""",
            "java": r"""// Four boundaries, shrunk after each side
List<Integer> spiralOrder(int[][] g) {
    List<Integer> out = new ArrayList<>();
    int top = 0, bot = g.length - 1, left = 0, right = g[0].length - 1;
    while (top <= bot && left <= right) {
        for (int c = left; c <= right; c++) out.add(g[top][c]);  top++;
        for (int r = top; r <= bot; r++)  out.add(g[r][right]);  right--;
        if (top <= bot) for (int c = right; c >= left; c--) out.add(g[bot][c]); bot--;
        if (left <= right) for (int r = bot; r >= top; r--) out.add(g[r][left]); left++;
    }
    return out;
}   // O(m*n) time · O(1) extra space""",
            "python": r"""def spiral_order(g):
    out = []
    top, bot, left, right = 0, len(g) - 1, 0, len(g[0]) - 1
    while top <= bot and left <= right:
        out.extend(g[top][left:right + 1]); top += 1
        for r in range(top, bot + 1): out.append(g[r][right])
        right -= 1
        if top <= bot:
            out.extend(g[bot][left:right + 1][::-1])   # right -> left
            bot -= 1
        if left <= right:
            for r in range(bot, top - 1, -1): out.append(g[r][left])
            left += 1
    return out
# O(m*n) time · O(1) extra space""",
        },
    },
    {
        "slug": "set-matrix-zeroes",
        "title": "Set Matrix Zeroes In Place",
        "difficulty": "Medium",
        "pattern": "using the first row/column as flags",
        "statement": "If an element of the matrix is 0, set its entire row and column to 0. Do it in place.",
        "examples": [("[[1,1,1],[1,0,1],[1,1,1]]", "[[1,0,1],[0,0,0],[1,0,1]]"),
                     ("[[0,1,2,0],[3,4,5,2],[1,3,1,5]]", "[[0,0,0,0],[0,4,5,0],[0,3,1,0]]")],
        "constraints": ["1 <= m, n <= 200"],
        "approach": "Record the zeros in the first row and first column themselves (`g[i][0]`, `g[0][j]`) instead of "
                    "allocating two arrays, but remember whether the first row/column originally contained a zero — "
                    "that flag has to be captured before anything is overwritten. Then sweep the interior, and finally "
                    "apply the first row/column flags.",
        "complexity": ("O(m·n)", "O(1)"),
        "code": {
            "cpp": r"""// First row and column double as the flag arrays
void setZeroes(vector<vector<int>>& g) {
    int m = g.size(), n = g[0].size();
    bool firstRowZero = false, firstColZero = false;
    for (int j = 0; j < n; j++) if (g[0][j] == 0) firstRowZero = true;
    for (int i = 0; i < m; i++) if (g[i][0] == 0) firstColZero = true;
    for (int i = 1; i < m; i++)
        for (int j = 1; j < n; j++)
            if (g[i][j] == 0) { g[i][0] = 0; g[0][j] = 0; }        // flag
    for (int i = 1; i < m; i++)
        for (int j = 1; j < n; j++)
            if (g[i][0] == 0 || g[0][j] == 0) g[i][j] = 0;         // apply
    if (firstRowZero) for (int j = 0; j < n; j++) g[0][j] = 0;
    if (firstColZero) for (int i = 0; i < m; i++) g[i][0] = 0;
}   // O(m*n) time · O(1) space""",
            "java": r"""// First row and column double as the flag arrays
void setZeroes(int[][] g) {
    int m = g.length, n = g[0].length;
    boolean firstRowZero = false, firstColZero = false;
    for (int j = 0; j < n; j++) if (g[0][j] == 0) firstRowZero = true;
    for (int i = 0; i < m; i++) if (g[i][0] == 0) firstColZero = true;
    for (int i = 1; i < m; i++)
        for (int j = 1; j < n; j++)
            if (g[i][j] == 0) { g[i][0] = 0; g[0][j] = 0; }        // flag
    for (int i = 1; i < m; i++)
        for (int j = 1; j < n; j++)
            if (g[i][0] == 0 || g[0][j] == 0) g[i][j] = 0;         // apply
    if (firstRowZero) Arrays.fill(g[0], 0);
    if (firstColZero) for (int i = 0; i < m; i++) g[i][0] = 0;
}   // O(m*n) time · O(1) space""",
            "python": r"""def set_zeroes(g):
    m, n = len(g), len(g[0])
    first_row_zero = any(v == 0 for v in g[0])
    first_col_zero = any(g[i][0] == 0 for i in range(m))
    for i in range(1, m):                       # flag inside the matrix
        for j in range(1, n):
            if g[i][j] == 0:
                g[i][0] = 0
                g[0][j] = 0
    for i in range(1, m):                       # apply the flags
        for j in range(1, n):
            if g[i][0] == 0 or g[0][j] == 0:
                g[i][j] = 0
    if first_row_zero:
        for j in range(n): g[0][j] = 0
    if first_col_zero:
        for i in range(m): g[i][0] = 0
    return g
# O(m*n) time · O(1) space""",
        },
    },
    {
        "slug": "longest-common-prefix",
        "title": "Longest Common Prefix of a List of Strings",
        "difficulty": "Medium",
        "pattern": "vertical scan (or sort-then-compare-ends)",
        "statement": "Return the longest prefix shared by every string in a list, or an empty string if there is none.",
        "examples": [("[\"flower\", \"flow\", \"flight\"]", "\"fl\""),
                     ("[\"dog\", \"car\", \"racecar\"]", "\"\"")],
        "constraints": ["1 <= number of strings <= 200", "0 <= length of each string <= 200"],
        "approach": "Vertical scan: compare the character at position i across all strings and stop at the first "
                    "mismatch — this is O(total characters) and stops early. The alternative is to sort the strings and "
                    "compare only the first and last, because those two define the common prefix.",
        "complexity": ("O(total characters)", "O(1)"),
        "code": {
            "cpp": r"""// Vertical scan: compare column by column
string longestCommonPrefix(vector<string>& words) {
    if (words.empty()) return "";
    for (int i = 0; i < (int)words[0].size(); i++) {
        char c = words[0][i];
        for (int k = 1; k < (int)words.size(); k++)
            if (i >= (int)words[k].size() || words[k][i] != c)
                return words[0].substr(0, i);          // mismatch at column i
    }
    return words[0];                                   // first string is the prefix of all
}   // O(total chars) time · O(1) space

// Sort-based alternative: sort(all(words)); compare words.front() with words.back().""",
            "java": r"""// Vertical scan: compare column by column
String longestCommonPrefix(String[] words) {
    if (words.length == 0) return "";
    for (int i = 0; i < words[0].length(); i++) {
        char c = words[0].charAt(i);
        for (int k = 1; k < words.length; k++)
            if (i >= words[k].length() || words[k].charAt(i) != c)
                return words[0].substring(0, i);       // mismatch at column i
    }
    return words[0];
}   // O(total chars) time · O(1) space""",
            "python": r"""def longest_common_prefix(words):
    if not words:
        return ""
    first = words[0]
    for i, c in enumerate(first):
        for w in words[1:]:
            if i >= len(w) or w[i] != c:
                return first[:i]          # mismatch at column i
    return first
# O(total chars) time · O(1) space

# sort-based alternative: s = sorted(words); compare s[0] with s[-1]""",
        },
    },
    {
        "slug": "valid-palindrome-filtered",
        "title": "Valid Palindrome Ignoring Case and Punctuation",
        "difficulty": "Medium",
        "pattern": "two pointers with a skip predicate",
        "statement": "A string is a valid palindrome if, after removing everything that is not a letter or digit and "
                     "lower-casing the rest, it reads the same forwards and backwards. Decide this in place.",
        "examples": [("\"A man, a plan, a canal: Panama\"", "true"),
                     ("\"race a car\"", "false")],
        "constraints": ["0 <= length <= 2 * 10^5", "the string contains printable ASCII characters"],
        "approach": "Two indices walk inward, skipping non-alphanumeric characters, and compare lower-cased characters. "
                    "The skip loops must re-check `i < j` every iteration or they can run past each other on strings "
                    "made only of punctuation.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Two pointers, skipping non-alphanumeric characters
bool isPalindrome(string s) {
    int i = 0, j = (int)s.size() - 1;
    while (i < j) {
        if (!isalnum((unsigned char)s[i])) { i++; continue; }
        if (!isalnum((unsigned char)s[j])) { j--; continue; }
        if (tolower(s[i]) != tolower(s[j])) return false;
        i++; j--;
    }
    return true;
}   // O(n) time · O(1) space""",
            "java": r"""// Two pointers, skipping non-alphanumeric characters
boolean isPalindrome(String s) {
    int i = 0, j = s.length() - 1;
    while (i < j) {
        if (!Character.isLetterOrDigit(s.charAt(i))) { i++; continue; }
        if (!Character.isLetterOrDigit(s.charAt(j))) { j--; continue; }
        if (Character.toLowerCase(s.charAt(i)) != Character.toLowerCase(s.charAt(j))) return false;
        i++; j--;
    }
    return true;
}   // O(n) time · O(1) space""",
            "python": r"""def is_palindrome(s):
    i, j = 0, len(s) - 1
    while i < j:
        if not s[i].isalnum():      # skip punctuation and spaces
            i += 1; continue
        if not s[j].isalnum():
            j -= 1; continue
        if s[i].lower() != s[j].lower():
            return False
        i += 1; j -= 1
    return True
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "first-unique-character",
        "title": "First Non-Repeating Character",
        "difficulty": "Medium",
        "pattern": "counting array with an ordered second pass",
        "statement": "Return the index of the first character in the string that appears exactly once, or -1 if every "
                     "character repeats.",
        "examples": [("\"leetcode\"", "0   ('l' appears once)"),
                     ("\"loveleetcode\"", "2   ('v')"),
                     ("\"aabb\"", "-1")],
        "constraints": ["1 <= length <= 10^5", "the string contains lowercase English letters"],
        "approach": "Count in an array of size 26 in the first pass, then walk the string again and return the first index "
                    "whose count is 1. The second pass **in string order** is what makes this a \"first\" answer — a hash "
                    "map alone loses the order unless you track indices.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Count, then find the first index with count 1
int firstUniqChar(const string& s) {
    int cnt[26] = {0};
    for (char c : s) cnt[c - 'a']++;
    for (int i = 0; i < (int)s.size(); i++) if (cnt[s[i] - 'a'] == 1) return i;
    return -1;
}   // O(n) time · O(1) space""",
            "java": r"""// Count, then find the first index with count 1
int firstUniqChar(String s) {
    int[] cnt = new int[26];
    for (int i = 0; i < s.length(); i++) cnt[s.charAt(i) - 'a']++;
    for (int i = 0; i < s.length(); i++) if (cnt[s.charAt(i) - 'a'] == 1) return i;
    return -1;
}   // O(n) time · O(1) space""",
            "python": r"""from collections import Counter

def first_unique_char(s):
    cnt = Counter(s)
    for i, c in enumerate(s):       # second pass in string order
        if cnt[c] == 1:
            return i
    return -1
# O(n) time · O(1) space (26 counters)""",
        },
    },
    {
        "slug": "reverse-words",
        "title": "Reverse the Order of Words in a Sentence",
        "difficulty": "Medium",
        "pattern": "tokenise then rebuild (in-place variant: reverse twice)",
        "statement": "Given a sentence, reverse the order of its words. Words are separated by one or more spaces, and "
                     "the result must have single spaces with no leading or trailing space.",
        "examples": [("\"the sky is blue\"", "\"blue is sky the\""),
                     ("\"  hello   world  \"", "\"world hello\"")],
        "constraints": ["1 <= length <= 10^4", "the sentence contains letters, digits and spaces"],
        "approach": "For clarity, tokenise on whitespace and rebuild with a `StringBuilder` — O(n) time and space. The "
                    "in-place version (useful for a character array) reverses the whole array first, then reverses each "
                    "word, then compacts the spaces — three passes, O(1) extra space.",
        "complexity": ("O(n)", "O(n) for the rebuild"),
        "code": {
            "cpp": r"""// Tokenise and rebuild in reverse order
string reverseWords(const string& s) {
    vector<string> words;
    string cur;
    for (int i = 0; i <= (int)s.size(); i++) {
        char c = (i == (int)s.size()) ? ' ' : s[i];
        if (c == ' ') { if (!cur.empty()) { words.push_back(cur); cur.clear(); } }
        else cur += c;
    }
    string out;
    for (int k = (int)words.size() - 1; k >= 0; k--) {
        if (!out.empty()) out += ' ';
        out += words[k];
    }
    return out;
}   // O(n) time · O(n) space""",
            "java": r"""// split() handles repeated spaces; "\s+" collapses runs
String reverseWords(String s) {
    String[] w = s.trim().split("\\s+");
    StringBuilder sb = new StringBuilder();
    for (int i = w.length - 1; i >= 0; i--) {
        if (sb.length() > 0) sb.append(' ');
        sb.append(w[i]);
    }
    return sb.toString();
}   // O(n) time · O(n) space""",
            "python": r"""def reverse_words(s):
    # split() with no argument collapses any run of whitespace and trims the ends
    return " ".join(reversed(s.split()))
# O(n) time · O(n) space""",
        },
    },

    # ------------------------------------------------------------------ HARD
    {
        "slug": "first-missing-positive",
        "title": "First Missing Positive Integer",
        "difficulty": "Hard",
        "pattern": "cyclic sort / index-as-hash",
        "statement": "Given an unsorted integer array, return the smallest positive integer (starting from 1) that is not "
                     "present. Required: O(n) time and O(1) extra space.",
        "examples": [("[1, 2, 0]", "3"),
                     ("[3, 4, -1, 1]", "2"),
                     ("[7, 8, 9, 11]", "1")],
        "constraints": ["1 <= n <= 10^5", "-2^31 <= a[i] <= 2^31 - 1"],
        "approach": "The answer lies in 1…n+1, so value v belongs at index v-1. Repeatedly swap each in-range value to its "
                    "home index; afterwards, the first index whose value is not index+1 gives the answer, and if every "
                    "slot is correct the answer is n+1. The `a[a[i]-1] != a[i]` guard prevents an infinite loop on "
                    "duplicates.",
        "complexity": ("O(n) — every value is moved at most once", "O(1)"),
        "code": {
            "cpp": r"""// Cyclic sort: value v belongs at index v - 1
int firstMissingPositive(vector<int>& a) {
    int n = a.size();
    for (int i = 0; i < n; i++)
        while (a[i] > 0 && a[i] <= n && a[a[i] - 1] != a[i])   // in range, not home yet
            swap(a[i], a[a[i] - 1]);
    for (int i = 0; i < n; i++)
        if (a[i] != i + 1) return i + 1;                        // first hole
    return n + 1;                                               // all of 1..n present
}   // O(n) time · O(1) space""",
            "java": r"""// Cyclic sort: value v belongs at index v - 1
int firstMissingPositive(int[] a) {
    int n = a.length;
    for (int i = 0; i < n; i++)
        while (a[i] > 0 && a[i] <= n && a[a[i] - 1] != a[i]) {   // in range, not home yet
            int t = a[i]; a[i] = a[t - 1]; a[t - 1] = t;
        }
    for (int i = 0; i < n; i++)
        if (a[i] != i + 1) return i + 1;                         // first hole
    return n + 1;                                                // all of 1..n present
}   // O(n) time · O(1) space""",
            "python": r"""def first_missing_positive(a):
    n = len(a)
    for i in range(n):
        while 0 < a[i] <= n and a[a[i] - 1] != a[i]:
            j = a[i] - 1                 # value a[i] belongs at index j
            a[i], a[j] = a[j], a[i]
    for i in range(n):
        if a[i] != i + 1:
            return i + 1                 # first hole
    return n + 1                          # 1..n all present
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "container-with-most-water",
        "title": "Container With Most Water",
        "difficulty": "Hard",
        "pattern": "two pointers with a greedy move",
        "statement": "Given n non-negative heights (one line per index), choose two lines that, together with the x-axis, "
                     "hold the most water. Return the maximum area.",
        "examples": [("[1,8,6,2,5,4,8,3,7]", "49   (indices 1 and 8: height 7, width 7)"),
                     ("[1,1]", "1")],
        "constraints": ["2 <= n <= 10^5", "0 <= height <= 10^4"],
        "approach": "Start with the widest pair. The area is width × min(height). Moving the taller side can never help "
                    "(width shrinks and the limit is the shorter side), so always advance the shorter side. Each step "
                    "discards pairs that cannot beat the current best, which is what makes it O(n) instead of O(n²).",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Greedy two pointers: always move the shorter side inward
long long maxArea(const vector<int>& h) {
    int i = 0, j = (int)h.size() - 1;
    long long best = 0;
    while (i < j) {
        best = max(best, (long long)(j - i) * min(h[i], h[j]));
        if (h[i] < h[j]) i++; else j--;      // the shorter side limits the area
    }
    return best;
}   // O(n) time · O(1) space""",
            "java": r"""// Greedy two pointers: always move the shorter side inward
long maxArea(int[] h) {
    int i = 0, j = h.length - 1;
    long best = 0;
    while (i < j) {
        best = Math.max(best, (long) (j - i) * Math.min(h[i], h[j]));
        if (h[i] < h[j]) i++; else j--;      // the shorter side limits the area
    }
    return best;
}   // O(n) time · O(1) space""",
            "python": r"""def max_area(h):
    i, j = 0, len(h) - 1
    best = 0
    while i < j:
        best = max(best, (j - i) * min(h[i], h[j]))
        if h[i] < h[j]:
            i += 1                           # move the shorter side
        else:
            j -= 1
    return best
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "trapping-rain-water",
        "title": "Trapping Rain Water",
        "difficulty": "Hard",
        "pattern": "two pointers with running maxima",
        "statement": "Given an elevation map, compute how many units of water are trapped between the bars after it rains.",
        "examples": [("[0,1,0,2,1,0,1,3,2,1,2,1]", "6"),
                     ("[4,2,0,3,2,5]", "9")],
        "constraints": ["1 <= n <= 2 * 10^4", "0 <= height <= 10^5"],
        "approach": "The water above index i is min(leftMax, rightMax) − height[i]. Instead of precomputing both arrays, "
                    "keep two pointers and two running maxima: when `leftMax <= rightMax`, the left side's water is fully "
                    "determined by `leftMax`, so process that index and advance; otherwise process the right index. Every "
                    "index is decided in O(1) with O(1) memory.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Two pointers: the smaller side's water is determined by its own maximum
long long trap(const vector<int>& h) {
    int i = 0, j = (int)h.size() - 1;
    long long leftMax = 0, rightMax = 0, water = 0;
    while (i < j) {
        if (h[i] <= h[j]) {
            leftMax = max(leftMax, (long long)h[i]);
            water += leftMax - h[i];              // water sitting above column i
            i++;
        } else {
            rightMax = max(rightMax, (long long)h[j]);
            water += rightMax - h[j];
            j--;
        }
    }
    return water;
}   // O(n) time · O(1) space

// Prefix-array alternative: pre = running max from the left, suf = running max from the right,
// then sum min(pre[i], suf[i]) - h[i]. Same answer, O(n) extra space, easier to explain first.""",
            "java": r"""// Two pointers: the smaller side's water is determined by its own maximum
long trap(int[] h) {
    int i = 0, j = h.length - 1;
    long leftMax = 0, rightMax = 0, water = 0;
    while (i < j) {
        if (h[i] <= h[j]) {
            leftMax = Math.max(leftMax, h[i]);
            water += leftMax - h[i];              // water sitting above column i
            i++;
        } else {
            rightMax = Math.max(rightMax, h[j]);
            water += rightMax - h[j];
            j--;
        }
    }
    return water;
}   // O(n) time · O(1) space""",
            "python": r"""def trap(h):
    i, j = 0, len(h) - 1
    left_max = right_max = water = 0
    while i < j:
        if h[i] <= h[j]:                  # the left side is the limiting one
            left_max = max(left_max, h[i])
            water += left_max - h[i]
            i += 1
        else:
            right_max = max(right_max, h[j])
            water += right_max - h[j]
            j -= 1
    return water
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "maximum-product-subarray",
        "title": "Maximum Product Subarray",
        "difficulty": "Hard",
        "pattern": "Kadane with a max and a min state",
        "statement": "Return the largest product obtainable from a contiguous subarray of an integer array.",
        "examples": [("[2,3,-2,4]", "6   ([2,3])"),
                     ("[-2,0,-1]", "0"),
                     ("[-2,3,-4]", "24   (the whole array)")],
        "constraints": ["1 <= n <= 2 * 10^4", "-10 <= a[i] <= 10", "the answer fits in a 32-bit integer"],
        "approach": "A negative number flips a minimum into a maximum, so track **both** the best and the worst product "
                    "ending at the current index. Every step extends one of the previous two states or restarts at the "
                    "current value. Sum-based Kadane does not need this because a negative never becomes positive.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Track best AND worst product ending here (a negative flips them)
long long maxProduct(const vector<int>& a) {
    long long best = a[0], hi = a[0], lo = a[0];
    for (int i = 1; i < (int)a.size(); i++) {
        long long x = a[i];
        long long nHi = max({x, hi * x, lo * x});   // extend the best, the worst, or restart
        long long nLo = min({x, hi * x, lo * x});
        hi = nHi; lo = nLo;
        best = max(best, hi);
    }
    return best;
}   // O(n) time · O(1) space""",
            "java": r"""// Track best AND worst product ending here (a negative flips them)
long maxProduct(int[] a) {
    long best = a[0], hi = a[0], lo = a[0];
    for (int i = 1; i < a.length; i++) {
        long x = a[i];
        long nHi = Math.max(x, Math.max(hi * x, lo * x));   // extend the best, the worst, or restart
        long nLo = Math.min(x, Math.min(hi * x, lo * x));
        hi = nHi; lo = nLo;
        best = Math.max(best, hi);
    }
    return best;
}   // O(n) time · O(1) space""",
            "python": r"""def max_product(a):
    best = hi = lo = a[0]                 # hi/lo: best and worst product ending here
    for x in a[1:]:
        hi, lo = max(x, hi * x, lo * x), min(x, hi * x, lo * x)   # right-hand side uses the old values
        best = max(best, hi)
    return best
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "longest-consecutive-sequence",
        "title": "Longest Consecutive Sequence",
        "difficulty": "Hard",
        "pattern": "hash set with run-start detection",
        "statement": "Return the length of the longest run of consecutive integers present in an unsorted array, in O(n) "
                     "time (so sorting is not allowed).",
        "examples": [("[100,4,200,1,3,2]", "4   (1,2,3,4)"),
                     ("[0,3,7,2,5,8,4,6,0,1]", "9   (0..8)")],
        "constraints": ["0 <= n <= 10^5", "-10^9 <= a[i] <= 10^9"],
        "approach": "Put every value in a hash set. For a value v, expand only when `v-1` is absent — that makes v the "
                    "start of a run, and each element is then visited by exactly one expansion, so the total work is "
                    "O(n) even though there is a nested loop. Duplicates collapse in the set automatically.",
        "complexity": ("O(n) expected", "O(n)"),
        "code": {
            "cpp": r"""// Hash set + run-start detection: each element expanded at most once
int longestConsecutive(const vector<int>& a) {
    unordered_set<int> s(a.begin(), a.end());
    int best = 0;
    for (int v : s) {
        if (s.count(v - 1)) continue;          // not the start of a run
        int len = 1;
        while (s.count(v + len)) len++;        // walk forward
        best = max(best, len);
    }
    return best;
}   // O(n) expected time · O(n) space""",
            "java": r"""// Hash set + run-start detection: each element expanded at most once
int longestConsecutive(int[] a) {
    Set<Integer> s = new HashSet<>();
    for (int v : a) s.add(v);
    int best = 0;
    for (int v : s) {
        if (s.contains(v - 1)) continue;       // not the start of a run
        int len = 1;
        while (s.contains(v + len)) len++;     // walk forward
        best = Math.max(best, len);
    }
    return best;
}   // O(n) expected time · O(n) space""",
            "python": r"""def longest_consecutive(a):
    s = set(a)                       # duplicates and lookups in O(1)
    best = 0
    for v in s:
        if v - 1 in s:
            continue                 # not the start of a run
        length = 1
        while v + length in s:
            length += 1
        best = max(best, length)
    return best
# O(n) expected time · O(n) space""",
        },
    },
    {
        "slug": "count-inversions",
        "title": "Count Inversions (Pairs Out of Order)",
        "difficulty": "Hard",
        "pattern": "divide and conquer (merge sort as a counter)",
        "statement": "An inversion is a pair of indices i < j with a[i] > a[j]. Count all inversions in the array. The "
                     "answer can exceed a 32-bit integer.",
        "examples": [("[2, 4, 1, 3, 5]", "3   ((2,1), (4,1), (4,3))"),
                     ("[5, 4, 3, 2, 1]", "10   (every pair)")],
        "constraints": ["1 <= n <= 10^5", "-10^9 <= a[i] <= 10^9"],
        "approach": "Merge sort, with the counting folded into the merge step: when the element taken comes from the "
                    "right half, every remaining element of the left half forms an inversion with it, so add "
                    "`mid - i + 1`. The recursion keeps the halves sorted, so each pair is counted exactly once at the "
                    "level where the halves meet.",
        "complexity": ("O(n log n)", "O(n) for the temporary buffer"),
        "code": {
            "cpp": r"""// Merge sort that counts inversions while merging
long long mergeCount(vector<int>& a, vector<int>& tmp, int lo, int hi) {
    if (lo >= hi) return 0;
    int mid = lo + (hi - lo) / 2;
    long long inv = mergeCount(a, tmp, lo, mid) + mergeCount(a, tmp, mid + 1, hi);
    int i = lo, j = mid + 1, k = lo;
    while (i <= mid && j <= hi) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];          // stable: equal values are not inversions
        else { inv += mid - i + 1; tmp[k++] = a[j++]; }   // all remaining left elements are bigger
    }
    while (i <= mid) tmp[k++] = a[i++];
    while (j <= hi)  tmp[k++] = a[j++];
    for (int t = lo; t <= hi; t++) a[t] = tmp[t];
    return inv;
}
long long countInversions(vector<int> a) {            // pass by value: we sort a copy
    vector<int> tmp(a.size());
    return mergeCount(a, tmp, 0, (int)a.size() - 1);
}   // O(n log n) time · O(n) space""",
            "java": r"""// Merge sort that counts inversions while merging
long countInversions(int[] a) {
    int[] tmp = new int[a.length];
    return mergeCount(a, tmp, 0, a.length - 1);
}
long mergeCount(int[] a, int[] tmp, int lo, int hi) {
    if (lo >= hi) return 0;
    int mid = lo + (hi - lo) / 2;
    long inv = mergeCount(a, tmp, lo, mid) + mergeCount(a, tmp, mid + 1, hi);
    int i = lo, j = mid + 1, k = lo;
    while (i <= mid && j <= hi) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];                 // stable: equal values are not inversions
        else { inv += mid - i + 1; tmp[k++] = a[j++]; }      // all remaining left elements are bigger
    }
    while (i <= mid) tmp[k++] = a[i++];
    while (j <= hi)  tmp[k++] = a[j++];
    for (int t = lo; t <= hi; t++) a[t] = tmp[t];
    return inv;
}   // O(n log n) time · O(n) space""",
            "python": r"""def count_inversions(a):
    # Returns (sorted_list, inversion_count) — divide and conquer, O(n log n)
    if len(a) <= 1:
        return a, 0
    mid = len(a) // 2
    left, inv_l = count_inversions(a[:mid])
    right, inv_r = count_inversions(a[mid:])
    merged, inv = [], inv_l + inv_r
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            inv += len(left) - i          # every remaining left element is bigger
            merged.append(right[j]); j += 1
    merged += left[i:]
    merged += right[j:]
    return merged, inv
# O(n log n) time · O(n) space""",
        },
    },
    {
        "slug": "majority-element-ii",
        "title": "Elements Appearing More Than n/3 Times",
        "difficulty": "Hard",
        "pattern": "generalised Boyer–Moore (two candidates)",
        "statement": "Return every element that appears more than floor(n/3) times. Return the answer in any order, and "
                     "use O(1) extra space.",
        "examples": [("[3,2,3]", "[3]"),
                     ("[1,1,1,3,3,2,2,2]", "[1,2]")],
        "constraints": ["1 <= n <= 5 * 10^4", "-10^9 <= a[i] <= 10^9"],
        "approach": "At most two values can exceed n/3, so run the voting algorithm with two candidate slots: a new "
                    "value either matches a candidate (its count grows), or fills an empty slot, or cancels both "
                    "candidates' counts. Afterwards verify both candidates by counting — unlike the > n/2 case, existence "
                    "is not guaranteed.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Two-slot voting, then a verification pass
vector<int> majorityElementII(const vector<int>& a) {
    long long c1 = 0, c2 = 0; int v1 = 0, v2 = 0;
    for (int x : a) {
        if (c1 && x == v1) c1++;
        else if (c2 && x == v2) c2++;
        else if (c1 == 0) { v1 = x; c1 = 1; }
        else if (c2 == 0) { v2 = x; c2 = 1; }
        else { c1--; c2--; }                     // cancel one from each slot
    }
    long long need = a.size() / 3;               // "more than n/3"
    vector<int> out;
    for (int cand : {v1, v2}) {
        if (!out.empty() && out[0] == cand) continue;         // both slots may hold the same value
        if (count(a.begin(), a.end(), cand) > need) out.push_back(cand);
    }
    return out;
}   // O(n) time · O(1) space""",
            "java": r"""// Two-slot voting, then a verification pass
List<Integer> majorityElementII(int[] a) {
    long c1 = 0, c2 = 0; int v1 = 0, v2 = 0;
    for (int x : a) {
        if (c1 > 0 && x == v1) c1++;
        else if (c2 > 0 && x == v2) c2++;
        else if (c1 == 0) { v1 = x; c1 = 1; }
        else if (c2 == 0) { v2 = x; c2 = 1; }
        else { c1--; c2--; }                     // cancel one from each slot
    }
    long need = a.length / 3;                    // strictly greater than n/3
    List<Integer> out = new ArrayList<>();
    for (int cand : new int[]{v1, v2}) {
        long cnt = 0;
        for (int x : a) if (x == cand) cnt++;
        if (cnt > need && (out.isEmpty() || out.get(0) != cand)) out.add(cand);   // dedupe the slots
    }
    return out;
}   // O(n) time · O(1) space""",
            "python": r"""def majority_element_ii(a):
    c1 = c2 = 0
    v1 = v2 = None
    for x in a:                       # Boyer-Moore with two slots
        if c1 > 0 and x == v1:
            c1 += 1
        elif c2 > 0 and x == v2:
            c2 += 1
        elif c1 == 0:
            v1, c1 = x, 1
        elif c2 == 0:
            v2, c2 = x, 1
        else:
            c1 -= 1
            c2 -= 1
    need = len(a) // 3
    out = []
    for cand in (v1, v2):             # verify: existence is not guaranteed here
        if cand is not None and a.count(cand) > need and cand not in out:
            out.append(cand)
    return out
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "next-permutation",
        "title": "Next Permutation in Lexicographic Order",
        "difficulty": "Hard",
        "pattern": "pivot, successor swap, suffix reversal",
        "statement": "Rearrange the array into the next lexicographically greater permutation. If no greater permutation "
                     "exists, rearrange it into the smallest possible order, and do everything in place.",
        "examples": [("[1,2,3]", "[1,3,2]"),
                     ("[3,2,1]", "[1,2,3]   (already the largest: wraps to the smallest)"),
                     ("[1,1,5]", "[1,5,1]")],
        "constraints": ["1 <= n <= 100", "0 <= a[i] <= 100"],
        "approach": "Find the rightmost index i with a[i] < a[i+1] — everything right of it is a decreasing suffix. Swap "
                    "a[i] with the rightmost element greater than it, then reverse the suffix to make it increasing, "
                    "which is the smallest arrangement of those values. If no such i exists the array is already the "
                    "largest permutation, so reversing the whole array gives the smallest.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Next permutation by hand (C++ also has std::next_permutation)
void nextPermutation(vector<int>& a) {
    int n = a.size(), i = n - 2;
    while (i >= 0 && a[i] >= a[i + 1]) i--;            // rightmost ascent = the pivot
    if (i >= 0) {
        int j = n - 1;
        while (a[j] <= a[i]) j--;                      // rightmost successor
        swap(a[i], a[j]);
    }
    reverse(a.begin() + i + 1, a.end());               // smallest arrangement of the suffix
}   // O(n) time · O(1) space""",
            "java": r"""// Next permutation by hand
void nextPermutation(int[] a) {
    int n = a.length, i = n - 2;
    while (i >= 0 && a[i] >= a[i + 1]) i--;            // rightmost ascent = the pivot
    if (i >= 0) {
        int j = n - 1;
        while (a[j] <= a[i]) j--;                      // rightmost successor
        int t = a[i]; a[i] = a[j]; a[j] = t;
    }
    for (int l = i + 1, r = n - 1; l < r; l++, r--) {  // reverse the suffix
        int t = a[l]; a[l] = a[r]; a[r] = t;
    }
}   // O(n) time · O(1) space""",
            "python": r"""def next_permutation(a):
    n = len(a)
    i = n - 2
    while i >= 0 and a[i] >= a[i + 1]:
        i -= 1                       # rightmost ascent = the pivot
    if i >= 0:
        j = n - 1
        while a[j] <= a[i]:
            j -= 1                   # rightmost successor
        a[i], a[j] = a[j], a[i]
    a[i + 1:] = reversed(a[i + 1:])  # smallest arrangement of the suffix
    return a
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "string-compression-in-place",
        "title": "Compress a Character Array In Place",
        "difficulty": "Hard",
        "pattern": "write pointer with group counting",
        "statement": "Compress runs of equal characters: a run of length 1 stays as the character, longer runs become the "
                     "character followed by the count in decimal digits. Write the result into the same array and return "
                     "its new length.",
        "examples": [("['a','a','b','b','c','c','c']", "6, array starts ['a','2','b','2','c','3']"),
                     ("['a']", "1, array stays ['a']"),
                     ("['a','b','b','b','b','b','b','b','b','b','b','b','b']", "4, ['a','b','1','2']")],
        "constraints": ["1 <= n <= 2000", "characters are lowercase English letters and digits"],
        "approach": "A read index walks run by run while a write index emits the character and then the digits of the "
                    "run length (note '12' becomes two characters). The write index is always behind the read index, so "
                    "overwriting in place is safe. Returning the new length is what makes the extra tail ignorable.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Runs compressed into the same buffer; returns the new length
int compress(vector<char>& c) {
    int n = c.size(), w = 0, r = 0;
    while (r < n) {
        char ch = c[r];
        int len = 0;
        while (r < n && c[r] == ch) { r++; len++; }        // measure the run
        c[w++] = ch;                                       // emit the character
        if (len > 1) {                                      // emit its digits
            string s = to_string(len);
            for (char d : s) c[w++] = d;
        }
    }
    return w;
}   // O(n) time · O(1) space""",
            "java": r"""// Runs compressed into the same buffer; returns the new length
int compress(char[] c) {
    int n = c.length, w = 0, r = 0;
    while (r < n) {
        char ch = c[r];
        int len = 0;
        while (r < n && c[r] == ch) { r++; len++; }        // measure the run
        c[w++] = ch;                                       // emit the character
        if (len > 1) {                                      // emit its digits
            for (char d : Integer.toString(len).toCharArray()) c[w++] = d;
        }
    }
    return w;
}   // O(n) time · O(1) space""",
            "python": r"""def compress(c):
    n, w, r = len(c), 0, 0
    while r < n:
        ch = c[r]
        length = 0
        while r < n and c[r] == ch:      # measure the run
            r += 1
            length += 1
        c[w] = ch                        # emit the character
        w += 1
        if length > 1:                   # emit its digits
            for d in str(length):
                c[w] = d
                w += 1
    return w
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "longest-palindromic-substring",
        "title": "Longest Palindromic Substring",
        "difficulty": "Hard",
        "pattern": "expand around every centre",
        "statement": "Return the longest contiguous substring of a string that reads the same in both directions. If "
                     "several have the same length, any of them is accepted.",
        "examples": [("\"babad\"", "\"bab\"   (\"aba\" is equally long)"),
                     ("\"cbbd\"", "\"bb\"")],
        "constraints": ["1 <= length <= 1000", "the string contains letters and digits"],
        "approach": "There are 2n−1 centres: each character, and each gap between characters (for even-length "
                    "palindromes). Expand outward from every centre while the characters match, and keep the longest. "
                    "This is O(n²) worst case with O(1) space — the linear-time Manacher algorithm is a separate skill "
                    "and rarely expected in interviews.",
        "complexity": ("O(n²)", "O(1)"),
        "code": {
            "cpp": r"""// Expand around all 2n-1 centres
pair<int,int> expand(const string& s, int l, int r) {      // returns [start, end] inclusive
    while (l >= 0 && r < (int)s.size() && s[l] == s[r]) { l--; r++; }
    return {l + 1, r - 1};
}
string longestPalindrome(const string& s) {
    int bestL = 0, bestR = 0;
    for (int c = 0; c < (int)s.size(); c++) {
        auto [l1, r1] = expand(s, c, c);          // odd length
        auto [l2, r2] = expand(s, c, c + 1);      // even length
        if (r1 - l1 > bestR - bestL) { bestL = l1; bestR = r1; }
        if (r2 - l2 > bestR - bestL) { bestL = l2; bestR = r2; }
    }
    return s.substr(bestL, bestR - bestL + 1);
}   // O(n^2) time · O(1) space""",
            "java": r"""// Expand around all 2n-1 centres
String longestPalindrome(String s) {
    int bestL = 0, bestR = 0;
    for (int c = 0; c < s.length(); c++) {
        int[] odd  = expand(s, c, c);                       // odd length
        int[] even = expand(s, c, c + 1);                   // even length
        if (odd[1] - odd[0] > bestR - bestL)   { bestL = odd[0];  bestR = odd[1]; }
        if (even[1] - even[0] > bestR - bestL) { bestL = even[0]; bestR = even[1]; }
    }
    return s.substring(bestL, bestR + 1);
}
int[] expand(String s, int l, int r) {                      // grows while the characters match
    while (l >= 0 && r < s.length() && s.charAt(l) == s.charAt(r)) { l--; r++; }
    return new int[]{l + 1, r - 1};                         // [start, end] inclusive
}   // O(n^2) time · O(1) space""",
            "python": r"""def longest_palindromic_substring(s):
    best = (0, 0)                          # (start, end) inclusive

    def expand(l, r):                      # grow while the characters match
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return l + 1, r - 1

    for c in range(len(s)):
        for span in (expand(c, c), expand(c, c + 1)):     # odd and even centres
            if span[1] - span[0] > best[1] - best[0]:
                best = span
    return s[best[0]:best[1] + 1]
# O(n^2) time · O(1) space""",
        },
    },
    {
        "slug": "subarray-sums-divisible-by-k",
        "title": "Subarrays With Sum Divisible by k",
        "difficulty": "Hard",
        "pattern": "prefix sums modulo k with a remainder counter",
        "statement": "Count the non-empty contiguous subarrays whose sum is divisible by k (k > 0).",
        "examples": [("[4,5,0,-2,-3,1], k = 5", "7"),
                     ("[5], k = 9", "0")],
        "constraints": ["1 <= n <= 3 * 10^4", "-10^4 <= a[i] <= 10^4", "1 <= k <= 10^4"],
        "approach": "A subarray (i, j] has sum divisible by k exactly when the two prefix sums share the same remainder "
                    "mod k. Keep a count of each remainder seen so far (starting with remainder 0 counted once for the "
                    "empty prefix), and add that count whenever a remainder repeats. Java and C++ give negative results "
                    "for `%` on negative sums, so normalise the remainder.",
        "complexity": ("O(n)", "O(k)"),
        "code": {
            "cpp": r"""// Same prefix remainder -> the difference is divisible by k
long long subarraysDivByK(const vector<int>& a, int k) {
    vector<int> cnt(k, 0);
    cnt[0] = 1;                              // the empty prefix
    long long sum = 0, ans = 0;
    for (int v : a) {
        sum += v;
        int r = ((sum % k) + k) % k;         // normalise negatives
        ans += cnt[r];                       // every earlier equal remainder forms a valid subarray
        cnt[r]++;
    }
    return ans;
}   // O(n) time · O(k) space""",
            "java": r"""// Same prefix remainder -> the difference is divisible by k
long subarraysDivByK(int[] a, int k) {
    int[] cnt = new int[k];
    cnt[0] = 1;                              // the empty prefix
    long sum = 0, ans = 0;
    for (int v : a) {
        sum += v;
        int r = Math.floorMod((int) sum, k);  // normalise negatives
        ans += cnt[r];                       // every earlier equal remainder forms a valid subarray
        cnt[r]++;
    }
    return ans;
}   // O(n) time · O(k) space""",
            "python": r"""def subarrays_div_by_k(a, k):
    cnt = [0] * k
    cnt[0] = 1                    # the empty prefix has remainder 0
    total = ans = 0
    for v in a:
        total += v
        r = total % k             # Python's % is already non-negative for k > 0
        ans += cnt[r]             # earlier prefixes with the same remainder close a valid subarray
        cnt[r] += 1
    return ans
# O(n) time · O(k) space""",
        },
    },
    {
        "slug": "median-of-two-sorted-arrays",
        "title": "Median of Two Sorted Arrays",
        "difficulty": "Hard",
        "pattern": "binary search on a partition of two arrays",
        "statement": "Given two sorted arrays of sizes m and n, return the median of the combined data in O(log(min(m, n))) "
                     "time.",
        "examples": [("[1,3], [2]", "2.0"),
                     ("[1,2], [3,4]", "2.5")],
        "constraints": ["0 <= m, n <= 1000", "0 <= m + n", "at least one array is non-empty"],
        "approach": "Binary search the number of elements taken from the smaller array. A partition is correct when the "
                    "largest element on the left side of both arrays is not greater than the smallest element on the "
                    "right side. Boundary sentinels (±infinity) remove all empty-side special cases, and the median "
                    "follows directly from the four elements around the cut.",
        "complexity": ("O(log(min(m, n)))", "O(1)"),
        "code": {
            "cpp": r"""// Binary search the cut position in the smaller array
double findMedianSortedArrays(vector<int>& A, vector<int>& B) {
    if (A.size() > B.size()) swap(A, B);                  // search the shorter one
    int m = A.size(), n = B.size();
    int lo = 0, hi = m;                                   // take `cut` elements from A
    while (lo <= hi) {
        int cutA = lo + (hi - lo) / 2;
        int cutB = (m + n + 1) / 2 - cutA;                 // keep the left side >= the right side
        double leftA  = (cutA == 0) ? -1e18 : A[cutA - 1];
        double rightA = (cutA == m) ?  1e18 : A[cutA];
        double leftB  = (cutB == 0) ? -1e18 : B[cutB - 1];
        double rightB = (cutB == n) ?  1e18 : B[cutB];
        if (leftA <= rightB && leftB <= rightA) {          // valid partition
            if ((m + n) % 2 == 1) return max(leftA, leftB);
            return (max(leftA, leftB) + min(rightA, rightB)) / 2.0;
        }
        if (leftA > rightB) hi = cutA - 1;                 // taking too many from A
        else lo = cutA + 1;                                // taking too few
    }
    return 0.0;                                            // unreachable for valid input
}   // O(log(min(m,n))) time · O(1) space""",
            "java": r"""// Binary search the cut position in the smaller array
double findMedianSortedArrays(int[] A, int[] B) {
    if (A.length > B.length) { int[] t = A; A = B; B = t; }   // search the shorter one
    int m = A.length, n = B.length;
    int lo = 0, hi = m;                                       // take `cut` elements from A
    while (lo <= hi) {
        int cutA = lo + (hi - lo) / 2;
        int cutB = (m + n + 1) / 2 - cutA;                    // keep the left side >= the right side
        double leftA  = (cutA == 0) ? Double.NEGATIVE_INFINITY : A[cutA - 1];
        double rightA = (cutA == m) ? Double.POSITIVE_INFINITY : A[cutA];
        double leftB  = (cutB == 0) ? Double.NEGATIVE_INFINITY : B[cutB - 1];
        double rightB = (cutB == n) ? Double.POSITIVE_INFINITY : B[cutB];
        if (leftA <= rightB && leftB <= rightA) {              // valid partition
            if ((m + n) % 2 == 1) return Math.max(leftA, leftB);
            return (Math.max(leftA, leftB) + Math.min(rightA, rightB)) / 2.0;
        }
        if (leftA > rightB) hi = cutA - 1;                     // taking too many from A
        else lo = cutA + 1;                                    // taking too few
    }
    return 0.0;                                                // unreachable for valid input
}   // O(log(min(m,n))) time · O(1) space""",
            "python": r"""def find_median_sorted_arrays(a, b):
    if len(a) > len(b):
        a, b = b, a                       # always binary search the shorter array
    m, n = len(a), len(b)
    lo, hi = 0, m                         # cut: how many elements are taken from a
    while lo <= hi:
        cut_a = (lo + hi) // 2
        cut_b = (m + n + 1) // 2 - cut_a  # left half is never smaller than the right half
        left_a  = a[cut_a - 1] if cut_a else float("-inf")
        right_a = a[cut_a] if cut_a < m else float("inf")
        left_b  = b[cut_b - 1] if cut_b else float("-inf")
        right_b = b[cut_b] if cut_b < n else float("inf")
        if left_a <= right_b and left_b <= right_a:       # valid partition
            if (m + n) % 2:
                return float(max(left_a, left_b))
            return (max(left_a, left_b) + min(right_a, right_b)) / 2
        if left_a > right_b:
            hi = cut_a - 1                # too many from a
        else:
            lo = cut_a + 1                # too few from a
    return 0.0                            # unreachable for valid input
# O(log(min(m, n))) time · O(1) space""",
        },
    },
]
