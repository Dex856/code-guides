# Topic 5 · Binary Search & Sorted Structures
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.

TOPIC = {
    "name": "Binary Search & Sorted Structures",
    "tagline": "Halving the problem — and its more valuable cousin: binary searching an *answer* instead of an index.",
    "focus": "Three skills. (1) Writing a correct loop and choosing the invariant so the boundary cases never bite. (2) 'Binary search on the "
             "answer': when a monotone feasibility test exists, search the value rather than the position. (3) Searching structures that are "
             "sorted in more than one direction — rotated arrays, matrices, mountains, and pairs whose k-th smallest statistic is wanted.",
    "ordering": "easy 1–6 are plain index searches and integer roots; medium 1–4 are rotated arrays and sorted matrices, 5–7 turn a monotone "
                "predicate into an answer search (Koko, shipping, bouquets), 8–12 are boundaries, peaks, LIS and staircase search; "
                "hard 1–4 are medians, duplicated rotations and answer searches with a sharp edge case, 5–12 are k-th statistics and "
                "partition problems that only look impossible.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "binary-search",
        "title": "Binary Search",
        "difficulty": "Easy",
        "pattern": "the canonical loop",
        "statement": "Given a sorted array of distinct integers, return the index of the target or -1 if it is absent.",
        "examples": [("nums = [-1,0,3,5,9,12], target = 9", "4"), ("nums = [-1,0,3,5,9,12], target = 2", "-1")],
        "constraints": ["1 <= n <= 10^4", "the array is sorted ascending with distinct values", "the algorithm must run in O(log n)"],
        "approach": "Keep an inclusive range [lo, hi] and compare the middle element. Writing `lo + (hi - lo) // 2` rather than `(lo + hi) // 2` "
                     "avoids overflow in fixed-width languages; writing `while lo <= hi` with `hi = mid - 1` guarantees the range shrinks even "
                     "when the target is absent.",
        "complexity": ("O(log n)", "O(1)"),
        "code": {
            "cpp": r"""// Inclusive bounds; every step strictly shrinks the range
int search(vector<int>& a, int target) {
    int lo = 0, hi = a.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;            // no overflow
        if (a[mid] == target) return mid;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}   // O(log n) time · O(1) space""",
            "java": r"""// Inclusive bounds; every step strictly shrinks the range
int search(int[] a, int target) {
    int lo = 0, hi = a.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;            // no overflow
        if (a[mid] == target) return mid;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;
}   // O(log n) time · O(1) space""",
            "python": r"""def search_sorted(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:                 # inclusive bounds
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1""",
        },
    },
    {
        "slug": "search-insert-position",
        "title": "Search Insert Position",
        "difficulty": "Easy",
        "pattern": "lower bound",
        "statement": "In a sorted array of distinct values, return the index of the target, or the index where it should be inserted to keep "
                     "the array sorted.",
        "examples": [("nums = [1,3,5,6], target = 5", "2"), ("nums = [1,3,5,6], target = 2", "1"), ("nums = [1,3,5,6], target = 7", "4")],
        "constraints": ["1 <= n <= 10^4", "the array is sorted ascending with distinct values", "the answer must be found in O(log n)"],
        "approach": "This is the 'first index where the value is >= target' search, also called lower bound. Return `lo` when the loop ends: it "
                     "is simultaneously the insertion point and the answer, which is why lower-bound loops never need post-processing.",
        "complexity": ("O(log n)", "O(1)"),
        "code": {
            "cpp": r"""// First index with a[i] >= target
int searchInsert(vector<int>& a, int target) {
    int lo = 0, hi = a.size();                   // half-open [lo, hi)
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return lo;                                   // insertion point
}   // O(log n) time · O(1) space""",
            "java": r"""// First index with a[i] >= target
int searchInsert(int[] a, int target) {
    int lo = 0, hi = a.length;                   // half-open [lo, hi)
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < target) lo = mid + 1;
        else hi = mid;
    }
    return lo;                                   // insertion point
}   // O(log n) time · O(1) space""",
            "python": r"""def search_insert(a, target):
    lo, hi = 0, len(a)                 # half-open range [lo, hi)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo                          # first index >= target""",
        },
    },
    {
        "slug": "sqrtx",
        "title": "Integer Square Root",
        "difficulty": "Easy",
        "pattern": "search on a monotone predicate",
        "statement": "Given a non-negative integer x, return the integer part of its square root without using any power or square-root function.",
        "examples": [("x = 4", "2"), ("x = 8", "2"), ("x = 0", "0")],
        "constraints": ["0 <= x <= 2^31 - 1", "use only integer arithmetic", "no built-in sqrt is allowed"],
        "approach": "Squares grow monotonically, so 'the largest m with m*m <= x' is a search over a monotone predicate — the first taste of "
                     "binary searching on the answer. Use a 64-bit type for m*m so the test itself cannot overflow.",
        "complexity": ("O(log x)", "O(1)"),
        "code": {
            "cpp": r"""// Largest m with m*m <= x
int mySqrt(int x) {
    long long lo = 0, hi = x;
    while (lo < hi) {
        long long mid = lo + (hi - lo + 1) / 2;  // upper mid: keep lo moving
        if (mid * mid <= x) lo = mid;
        else hi = mid - 1;
    }
    return (int)lo;
}   // O(log x) time · O(1) space""",
            "java": r"""// Largest m with m*m <= x
int mySqrt(int x) {
    long lo = 0, hi = x;
    while (lo < hi) {
        long mid = lo + (hi - lo + 1) / 2;       // upper mid: keep lo moving
        if (mid * mid <= x) lo = mid;
        else hi = mid - 1;
    }
    return (int) lo;
}   // O(log x) time · O(1) space""",
            "python": r"""def my_sqrt(x):
    lo, hi = 0, x
    while lo < hi:
        mid = (lo + hi + 1) // 2        # upper mid so lo always advances
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo""",
        },
    },
    {
        "slug": "first-bad-version",
        "title": "First Bad Version",
        "difficulty": "Easy",
        "pattern": "lower bound on a hidden predicate",
        "statement": "Versions 1..n are ordered so that all versions after the first bad one are also bad. Using only the API "
                     "isBadVersion(v), find the first bad version with as few calls as possible.",
        "examples": [("n = 5, first bad = 4", "4"), ("n = 1, first bad = 1", "1")],
        "constraints": ["1 <= n <= 2^31 - 1", "the predicate is monotone (false...false, true...true)", "the API is the only way to inspect a version"],
        "approach": "The predicate's monotonicity is the entire reason binary search applies: seeing *one* bad version rules out everything "
                     "before it as the answer. This is the template for every 'find the boundary of a hidden property' question.",
        "complexity": ("O(log n)", "O(1)"),
        "code": {
            "cpp": r"""// Lower bound of a monotone hidden predicate
bool isBadVersion(int v);                        // provided by the judge
int firstBadVersion(int n) {
    int lo = 1, hi = n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;            // avoids lo + hi overflow
        if (isBadVersion(mid)) hi = mid;         // mid may be the answer
        else lo = mid + 1;
    }
    return lo;
}   // O(log n) time · O(1) space""",
            "java": r"""// Lower bound of a monotone hidden predicate
static boolean isBadVersion(int v) { return false; }   // stub for the judge API
int firstBadVersion(int n) {
    int lo = 1, hi = n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;            // avoids lo + hi overflow
        if (isBadVersion(mid)) hi = mid;         // mid may be the answer
        else lo = mid + 1;
    }
    return lo;
}   // O(log n) time · O(1) space""",
            "python": r"""def first_bad_version(n, is_bad_version):
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if is_bad_version(mid):
            hi = mid                  # mid may be the answer
        else:
            lo = mid + 1
    return lo""",
        },
    },
    {
        "slug": "valid-perfect-square",
        "title": "Valid Perfect Square",
        "difficulty": "Easy",
        "pattern": "exact-value search",
        "statement": "Return true if the given positive integer is a perfect square, using no built-in square-root function.",
        "examples": [("num = 16", "true"), ("num = 14", "false")],
        "constraints": ["1 <= num <= 2^31 - 1", "integer arithmetic only", "the answer must be exact, not approximate"],
        "approach": "Same search as the integer square root, but the predicate is exact equality: return true only when a mid hit the value "
                     "squarely. Comparing mid*m*m == num inside the loop avoids relying on a floating-point sqrt and a rounding check.",
        "complexity": ("O(log num)", "O(1)"),
        "code": {
            "cpp": r"""// Same search; only an exact hit counts
bool isPerfectSquare(int num) {
    long long lo = 1, hi = num;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2, sq = mid * mid;
        if (sq == num) return true;
        if (sq < num) lo = mid + 1;
        else hi = mid - 1;
    }
    return false;
}   // O(log num) time · O(1) space""",
            "java": r"""// Same search; only an exact hit counts
boolean isPerfectSquare(int num) {
    long lo = 1, hi = num;
    while (lo <= hi) {
        long mid = lo + (hi - lo) / 2, sq = mid * mid;
        if (sq == num) return true;
        if (sq < num) lo = mid + 1;
        else hi = mid - 1;
    }
    return false;
}   // O(log num) time · O(1) space""",
            "python": r"""def is_perfect_square(num):
    lo, hi = 1, num
    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid
        if sq == num:
            return True
        if sq < num:
            lo = mid + 1
        else:
            hi = mid - 1
    return False""",
        },
    },
    {
        "slug": "smallest-letter-greater-than-target",
        "title": "Smallest Letter Greater Than Target",
        "difficulty": "Easy",
        "pattern": "upper bound with wraparound",
        "statement": "Given a sorted circular list of lowercase letters and a target letter, return the smallest letter in the list that is "
                     "strictly greater than the target, wrapping around to the first letter if none is.",
        "examples": [("letters = [\"c\",\"f\",\"j\"], target = \"a\"", "\"c\""), ("letters = [\"c\",\"f\",\"j\"], target = \"j\"", "\"c\"")],
        "constraints": ["2 <= n <= 10^4", "letters are lowercase and sorted, possibly repeating", "the answer is always one of the letters"],
        "approach": "This is the upper bound: the first index whose letter is strictly greater than the target. If that index runs off the end, "
                     "the circular order means the answer is index 0 — a single modulo converts the failure case into the success case.",
        "complexity": ("O(log n)", "O(1)"),
        "code": {
            "cpp": r"""// Upper bound; wrap to the first letter if there is none
char nextGreatestLetter(vector<char>& letters, char target) {
    int lo = 0, hi = letters.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (letters[mid] <= target) lo = mid + 1;   // strictly greater
        else hi = mid;
    }
    return letters[lo % letters.size()];            // wrap around
}   // O(log n) time · O(1) space""",
            "java": r"""// Upper bound; wrap to the first letter if there is none
char nextGreatestLetter(char[] letters, char target) {
    int lo = 0, hi = letters.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (letters[mid] <= target) lo = mid + 1;   // strictly greater
        else hi = mid;
    }
    return letters[lo % letters.length];            // wrap around
}   // O(log n) time · O(1) space""",
            "python": r"""def next_greatest_letter(letters, target):
    lo, hi = 0, len(letters)
    while lo < hi:
        mid = (lo + hi) // 2
        if letters[mid] <= target:
            lo = mid + 1         # strictly greater only
        else:
            hi = mid
    return letters[lo % len(letters)]    # wrap around""",
        },
    },
    # ---------------------------------------------------------------- MEDIUM
    {
        "slug": "search-in-rotated-sorted-array",
        "title": "Search in Rotated Sorted Array",
        "difficulty": "Medium",
        "pattern": "one half is always sorted",
        "statement": "A sorted array of distinct values was rotated at some pivot; find the index of the target or return -1, in O(log n).",
        "examples": [("nums = [4,5,6,7,0,1,2], target = 0", "4"), ("nums = [4,5,6,7,0,1,2], target = 3", "-1")],
        "constraints": ["1 <= n <= 5000", "all values are distinct", "the array is a rotation of a sorted array"],
        "approach": "Even after a rotation, at least one side of the midpoint is properly sorted. Identify that side by comparing a[lo] with "
                     "a[mid], then decide in one comparison whether the target lies inside the sorted half — if it does, search there, otherwise "
                     "search the other half.",
        "complexity": ("O(log n)", "O(1)"),
        "code": {
            "cpp": r"""// Exactly one of the two halves is sorted: use it to decide
int search(vector<int>& a, int target) {
    int lo = 0, hi = a.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        if (a[lo] <= a[mid]) {                       // left half sorted
            if (a[lo] <= target && target < a[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {                                     // right half sorted
            if (a[mid] < target && target <= a[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return -1;
}   // O(log n) time · O(1) space""",
            "java": r"""// Exactly one of the two halves is sorted: use it to decide
int search(int[] a, int target) {
    int lo = 0, hi = a.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        if (a[lo] <= a[mid]) {                       // left half sorted
            if (a[lo] <= target && target < a[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {                                     // right half sorted
            if (a[mid] < target && target <= a[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return -1;
}   // O(log n) time · O(1) space""",
            "python": r"""def search_rotated(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        if a[lo] <= a[mid]:                 # left half is sorted
            if a[lo] <= target < a[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                               # right half is sorted
            if a[mid] < target <= a[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1""",
        },
    },
    {
        "slug": "find-minimum-in-rotated-sorted-array",
        "title": "Find Minimum in Rotated Sorted Array",
        "difficulty": "Medium",
        "pattern": "compare with the right end",
        "statement": "A sorted array of distinct values was rotated; return its minimum element in O(log n).",
        "examples": [("nums = [3,4,5,1,2]", "1"), ("nums = [4,5,6,7,0,1,2]", "0")],
        "constraints": ["1 <= n <= 5000", "all values are distinct", "the array is a rotation of a sorted array"],
        "approach": "Compare the middle value with the rightmost one: if a[mid] is greater, the rotation point (and therefore the minimum) is to "
                     "the right; otherwise it is at mid or to the left. This comparison is the one formulation that needs no special case for an "
                     "array that was not rotated at all.",
        "complexity": ("O(log n)", "O(1)"),
        "code": {
            "cpp": r"""// Compare a[mid] with a[hi]; the minimum follows that sign
int findMin(vector<int>& a) {
    int lo = 0, hi = a.size() - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] > a[hi]) lo = mid + 1;            // rotation point is right
        else hi = mid;                               // mid could be the min
    }
    return a[lo];
}   // O(log n) time · O(1) space""",
            "java": r"""// Compare a[mid] with a[hi]; the minimum follows that sign
int findMin(int[] a) {
    int lo = 0, hi = a.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] > a[hi]) lo = mid + 1;            // rotation point is right
        else hi = mid;                               // mid could be the min
    }
    return a[lo];
}   // O(log n) time · O(1) space""",
            "python": r"""def find_min_rotated(a):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] > a[hi]:
            lo = mid + 1        # the minimum is strictly to the right
        else:
            hi = mid            # mid could be the minimum itself
    return a[lo]""",
        },
    },
    {
        "slug": "search-a-2d-matrix",
        "title": "Search a 2D Matrix",
        "difficulty": "Medium",
        "pattern": "flatten the index",
        "statement": "Rows are sorted left to right and the first value of each row is greater than the last value of the previous row. Decide "
                     "whether a target appears in the matrix, in O(log(rows · cols)).",
        "examples": [("matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3", "true"),
                     ("same matrix, target = 13", "false")],
        "constraints": ["1 <= rows, cols <= 100", "-10^4 <= values, target <= 10^4", "the whole matrix is sorted row-major"],
        "approach": "The row-major layout is itself sorted, so the matrix is a single sorted array stored in two dimensions: map an index k to "
                     "row k/cols and column k%cols and run ordinary binary search. Recognising a layout as one sorted sequence is quicker than "
                     "any two-level search.",
        "complexity": ("O(log(rows · cols))", "O(1)"),
        "code": {
            "cpp": r"""// Row-major layout is one sorted array: map k -> (k / C, k % C)
bool searchMatrix(vector<vector<int>>& m, int target) {
    int R = m.size(), C = m[0].size();
    int lo = 0, hi = R * C - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int v = m[mid / C][mid % C];                 // flatten the index
        if (v == target) return true;
        if (v < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return false;
}   // O(log(R·C)) time · O(1) space""",
            "java": r"""// Row-major layout is one sorted array: map k -> (k / C, k % C)
boolean searchMatrix(int[][] m, int target) {
    int R = m.length, C = m[0].length;
    int lo = 0, hi = R * C - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int v = m[mid / C][mid % C];                 // flatten the index
        if (v == target) return true;
        if (v < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return false;
}   // O(log(R·C)) time · O(1) space""",
            "python": r"""def search_matrix_flat(m, target):
    R, C = len(m), len(m[0])
    lo, hi = 0, R * C - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = m[mid // C][mid % C]        # flatten the index
        if v == target:
            return True
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False""",
        },
    },
    {
        "slug": "koko-eating-bananas",
        "title": "Koko Eating Bananas",
        "difficulty": "Medium",
        "pattern": "binary search on the answer",
        "statement": "There are piles of bananas and h hours. Each hour Koko picks one pile and eats up to k bananas from it (finishing a pile "
                     "before moving on). Return the smallest speed k that clears every pile within h hours.",
        "examples": [("piles = [3,6,7,11], h = 8", "4"), ("piles = [30,11,23,4,20], h = 5", "30")],
        "constraints": ["1 <= number of piles <= 10^4", "h >= number of piles", "1 <= bananas per pile <= 10^9"],
        "approach": "Slow speeds fail and fast speeds succeed — feasibility is monotone, so binary search the speed instead of a position. The "
                     "check sums ceil(pile / k) over all piles; the first speed whose total is at most h is the answer. This 'search the answer "
                     "space with a greedy feasibility test' pattern covers a whole family of problems.",
        "complexity": ("O(n log max)", "O(1)"),
        "code": {
            "cpp": r"""// Monotone in k: binary search the speed, check with ceil division
int minEatingSpeed(vector<int>& piles, int h) {
    auto hoursNeeded = [&](long long k) {
        long long total = 0;
        for (int p : piles) total += (p + k - 1) / k;    // ceil(p / k)
        return total;
    };
    long long lo = 1, hi = *max_element(piles.begin(), piles.end());
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (hoursNeeded(mid) <= h) hi = mid;             // feasible: try slower
        else lo = mid + 1;
    }
    return (int)lo;
}   // O(n log max) time · O(1) space""",
            "java": r"""// Monotone in k: binary search the speed, check with ceil division
int minEatingSpeed(int[] piles, int h) {
    long lo = 1, hi = 0;
    for (int p : piles) hi = Math.max(hi, p);
    while (lo < hi) {
        long mid = lo + (hi - lo) / 2, total = 0;
        for (int p : piles) total += (p + mid - 1) / mid;     // ceil(p / mid)
        if (total <= h) hi = mid;                             // feasible: try slower
        else lo = mid + 1;
    }
    return (int) lo;
}   // O(n log max) time · O(1) space""",
            "python": r"""def min_eating_speed(piles, h):
    def hours_needed(k):
        return sum((p + k - 1) // k for p in piles)   # ceil(p / k)

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours_needed(mid) <= h:
            hi = mid          # feasible: try a slower speed
        else:
            lo = mid + 1
    return lo""",
        },
    },
    {
        "slug": "capacity-to-ship-packages-within-d-days",
        "title": "Ship Packages Within D Days",
        "difficulty": "Medium",
        "pattern": "binary search on capacity",
        "statement": "Packages must be shipped in the given order within d days, loading each day's packages consecutively. Return the smallest "
                     "ship capacity that finishes in time.",
        "examples": [("weights = [1,2,3,4,5,6,7,8,9,10], days = 5", "15"), ("weights = [3,2,2,4,1,4], days = 3", "6")],
        "constraints": ["1 <= n <= 5 * 10^4", "1 <= weights, days <= 5 * 10^4", "the order of the packages may not change"],
        "approach": "Same answer-search shape: capacity is monotone (bigger is never worse), and the feasibility test is one greedy pass that "
                     "fills each day until the next package would exceed the capacity. The lower bound is the heaviest package and the upper "
                     "bound is the total weight — bounding the search tightly is what keeps it fast.",
        "complexity": ("O(n log total)", "O(1)"),
        "code": {
            "cpp": r"""// Greedy feasibility pass, then binary search the capacity
int shipWithinDays(vector<int>& w, int days) {
    auto fits = [&](int cap) {
        int used = 1, load = 0;
        for (int x : w) {
            if (load + x > cap) { used++; load = 0; }   // start a new day
            load += x;
        }
        return used <= days;
    };
    int lo = *max_element(w.begin(), w.end());          // lower bound
    int hi = accumulate(w.begin(), w.end(), 0);         // upper bound
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (fits(mid)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(n log total) time · O(1) space""",
            "java": r"""// Greedy feasibility pass, then binary search the capacity
int shipWithinDays(int[] w, int days) {
    int lo = 0, hi = 0;
    for (int x : w) { lo = Math.max(lo, x); hi += x; }  // tight bounds
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        int used = 1, load = 0;
        for (int x : w) {
            if (load + x > mid) { used++; load = 0; }   // start a new day
            load += x;
        }
        if (used <= days) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(n log total) time · O(1) space""",
            "python": r"""def ship_within_days(w, days):
    def fits(cap):
        used, load = 1, 0
        for x in w:
            if load + x > cap:
                used += 1            # start a new day
                load = 0
            load += x
        return used <= days

    lo, hi = max(w), sum(w)          # tight bounds
    while lo < hi:
        mid = (lo + hi) // 2
        if fits(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo""",
        },
    },
    {
        "slug": "find-peak-element",
        "title": "Find Peak Element",
        "difficulty": "Medium",
        "pattern": "climb the slope",
        "statement": "An element is a peak if it is strictly greater than its neighbours (out-of-range neighbours count as negative infinity). "
                     "Return the index of any peak, in O(log n).",
        "examples": [("nums = [1,2,3,1]", "2"), ("nums = [1,2,1,3,5,6,4]", "5")],
        "constraints": ["1 <= n <= 1000", "adjacent values are never equal", "any valid peak index is accepted"],
        "approach": "If the middle element is smaller than its right neighbour, a peak must exist to the right (the sequence has to come down "
                     "somewhere); otherwise a peak exists at mid or to the left. Following the uphill direction never gets stuck, which is why "
                     "this search needs no sorted input at all.",
        "complexity": ("O(log n)", "O(1)"),
        "code": {
            "cpp": r"""// Always step uphill: a peak is guaranteed in that direction
int findPeakElement(vector<int>& a) {
    int lo = 0, hi = a.size() - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < a[mid + 1]) lo = mid + 1;       // uphill to the right
        else hi = mid;                               // downhill: peak is here or left
    }
    return lo;
}   // O(log n) time · O(1) space""",
            "java": r"""// Always step uphill: a peak is guaranteed in that direction
int findPeakElement(int[] a) {
    int lo = 0, hi = a.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < a[mid + 1]) lo = mid + 1;       // uphill to the right
        else hi = mid;                               // downhill: peak is here or left
    }
    return lo;
}   // O(log n) time · O(1) space""",
            "python": r"""def find_peak_element(a):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < a[mid + 1]:
            lo = mid + 1        # uphill: a peak is guaranteed to the right
        else:
            hi = mid            # downhill: the peak is at mid or to the left
    return lo""",
        },
    },
    {
        "slug": "find-first-and-last-position",
        "title": "First and Last Position of a Target",
        "difficulty": "Medium",
        "pattern": "lower bound + upper bound",
        "statement": "In a sorted array (with duplicates), return the first and last index of the target, or [-1,-1] if it is absent. The "
                     "algorithm must run in O(log n).",
        "examples": [("nums = [5,7,7,8,8,10], target = 8", "[3,4]"), ("nums = [5,7,7,8,8,10], target = 6", "[-1,-1]")],
        "constraints": ["0 <= n <= 10^5", "the array is sorted ascending", "O(log n) is required, so linear scanning is not allowed"],
        "approach": "Two boundary searches on the same array: the first index with value >= target, and the first index with value > target "
                     "(then subtract one). Factoring both into one helper that takes a 'wanted' flag keeps them consistent — most wrong answers "
                     "here come from two hand-edited copies that drifted apart.",
        "complexity": ("O(log n)", "O(1)"),
        "code": {
            "cpp": r"""// One helper for both bounds: first index with a[i] > target - 1 + want
int bound(vector<int>& a, int target, bool wantFirst) {
    int lo = 0, hi = a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        bool moveRight = wantFirst ? a[mid] < target : a[mid] <= target;
        if (moveRight) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
vector<int> searchRange(vector<int>& a, int target) {
    int first = bound(a, target, true);
    if (first == (int)a.size() || a[first] != target) return {-1, -1};
    return {first, bound(a, target, false) - 1};
}   // O(log n) time · O(1) space""",
            "java": r"""// One helper for both bounds: first index with a[i] > target - 1 + want
private int bound(int[] a, int target, boolean wantFirst) {
    int lo = 0, hi = a.length;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        boolean moveRight = wantFirst ? a[mid] < target : a[mid] <= target;
        if (moveRight) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}
int[] searchRange(int[] a, int target) {
    int first = bound(a, target, true);
    if (first == a.length || a[first] != target) return new int[]{-1, -1};
    return new int[]{first, bound(a, target, false) - 1};
}   // O(log n) time · O(1) space""",
            "python": r"""def search_range(a, target):
    def bound(want_first):
        lo, hi = 0, len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            move_right = a[mid] < target if want_first else a[mid] <= target
            if move_right:
                lo = mid + 1
            else:
                hi = mid
        return lo                     # first index where the test stops holding

    first = bound(True)
    if first == len(a) or a[first] != target:
        return [-1, -1]
    return [first, bound(False) - 1]""",
        },
    },
    {
        "slug": "search-in-rotated-sorted-array-ii",
        "title": "Search in Rotated Sorted Array II",
        "difficulty": "Medium",
        "pattern": "rotation with duplicates",
        "statement": "Like the rotated-array search, but values may repeat. Return true if the target appears anywhere in the array.",
        "examples": [("nums = [2,5,6,0,0,1,2], target = 0", "true"), ("nums = [2,5,6,0,0,1,2], target = 3", "false")],
        "constraints": ["1 <= n <= 5000", "the array is a rotation of a sorted array and may contain duplicates", "an answer of O(n) worst case is acceptable"],
        "approach": "Duplicates break the 'which half is sorted' test when a[lo] == a[mid] == a[hi]: nothing can be concluded, so shrink both "
                     "ends by one and continue. That is the only new case, and it is why the worst case degrades to O(n) — worth saying out loud "
                     "in an interview.",
        "complexity": ("O(log n) average, O(n) worst", "O(1)"),
        "code": {
            "cpp": r"""// Same idea; equal ends give no information, so shrink them
bool search(vector<int>& a, int target) {
    int lo = 0, hi = a.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return true;
        if (a[lo] == a[mid] && a[mid] == a[hi]) { lo++; hi--; continue; }   // ambiguous
        if (a[lo] <= a[mid]) {
            if (a[lo] <= target && target < a[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {
            if (a[mid] < target && target <= a[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return false;
}   // O(log n) average, O(n) worst time · O(1) space""",
            "java": r"""// Same idea; equal ends give no information, so shrink them
boolean search(int[] a, int target) {
    int lo = 0, hi = a.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return true;
        if (a[lo] == a[mid] && a[mid] == a[hi]) { lo++; hi--; continue; }   // ambiguous
        if (a[lo] <= a[mid]) {
            if (a[lo] <= target && target < a[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {
            if (a[mid] < target && target <= a[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return false;
}   // O(log n) average, O(n) worst time · O(1) space""",
            "python": r"""def search_rotated_duplicates(a, target):
    lo, hi = 0, len(a) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return True
        if a[lo] == a[mid] == a[hi]:     # no usable information: shrink
            lo += 1
            hi -= 1
            continue
        if a[lo] <= a[mid]:              # left half is sorted
            if a[lo] <= target < a[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                            # right half is sorted
            if a[mid] < target <= a[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False""",
        },
    },
    {
        "slug": "longest-increasing-subsequence",
        "title": "Longest Increasing Subsequence",
        "difficulty": "Medium",
        "pattern": "patience sorting / tails array",
        "statement": "Return the length of the longest strictly increasing subsequence of the array (the elements need not be contiguous).",
        "examples": [("[10,9,2,5,3,7,101,18]", "4"), ("[0,1,0,3,2,3]", "4")],
        "constraints": ["1 <= n <= 2500", "-10^4 <= values <= 10^4", "the subsequence must keep the original order"],
        "approach": "Maintain an array `tails` where tails[k] is the smallest possible tail of an increasing subsequence of length k+1. It stays "
                     "sorted, so each new value replaces the first tail that is >= it — a binary search. The length of `tails` is the answer even "
                     "though `tails` itself is not a valid subsequence; that subtlety is the usual interview follow-up.",
        "complexity": ("O(n log n)", "O(n)"),
        "code": {
            "cpp": r"""// tails[k] = smallest tail of an increasing subsequence of length k+1
int lengthOfLIS(vector<int>& a) {
    vector<int> tails;                            // always sorted
    for (int v : a) {
        auto it = lower_bound(tails.begin(), tails.end(), v);   // first >= v
        if (it == tails.end()) tails.push_back(v);              // extends the LIS
        else *it = v;                                           // smaller tail
    }
    return tails.size();
}   // O(n log n) time · O(n) space""",
            "java": r"""// tails[k] = smallest tail of an increasing subsequence of length k+1
int lengthOfLIS(int[] a) {
    int[] tails = new int[a.length];
    int size = 0;
    for (int v : a) {
        int lo = 0, hi = size;                    // first index with tails[i] >= v
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            if (tails[mid] < v) lo = mid + 1;
            else hi = mid;
        }
        tails[lo] = v;                            // extend or replace a tail
        if (lo == size) size++;
    }
    return size;
}   // O(n log n) time · O(n) space""",
            "python": r"""import bisect

def length_of_lis(a):
    tails = []                      # tails[k] = smallest tail of a length k+1 run
    for v in a:
        i = bisect.bisect_left(tails, v)   # first tail >= v
        if i == len(tails):
            tails.append(v)             # v extends the longest run
        else:
            tails[i] = v                # v is a smaller tail for that length
    return len(tails)""",
        },
    },
    {
        "slug": "search-a-2d-matrix-ii",
        "title": "Search a 2D Matrix II",
        "difficulty": "Medium",
        "pattern": "staircase elimination",
        "statement": "Rows and columns are each sorted ascending. Count or find a target in O(rows + cols).",
        "examples": [("matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5", "true"),
                     ("same matrix, target = 20", "false")],
        "constraints": ["1 <= rows, cols <= 300", "-10^9 <= values <= 10^9", "rows and columns are sorted but the matrix is not row-major sorted"],
        "approach": "Start at the top-right corner: every step discards an entire row or column, because values to the left are smaller and "
                     "values below are larger. That single corner turns the search into at most rows + cols steps — no binary search needed, "
                     "which is the point worth remembering.",
        "complexity": ("O(rows + cols)", "O(1)"),
        "code": {
            "cpp": r"""// Top-right corner: each step deletes a row or a column
bool searchMatrix(vector<vector<int>>& m, int target) {
    int r = 0, c = m[0].size() - 1;
    while (r < (int)m.size() && c >= 0) {
        if (m[r][c] == target) return true;
        if (m[r][c] > target) c--;                // this column is too big
        else r++;                                 // this row is too small
    }
    return false;
}   // O(rows + cols) time · O(1) space""",
            "java": r"""// Top-right corner: each step deletes a row or a column
boolean searchMatrix(int[][] m, int target) {
    int r = 0, c = m[0].length - 1;
    while (r < m.length && c >= 0) {
        if (m[r][c] == target) return true;
        if (m[r][c] > target) c--;                // this column is too big
        else r++;                                 // this row is too small
    }
    return false;
}   // O(rows + cols) time · O(1) space""",
            "python": r"""def search_matrix_staircase(m, target):
    r, c = 0, len(m[0]) - 1            # start at the top-right corner
    while r < len(m) and c >= 0:
        if m[r][c] == target:
            return True
        if m[r][c] > target:
            c -= 1                     # this column is too big
        else:
            r += 1                     # this row is too small
    return False""",
        },
    },
    {
        "slug": "minimum-limit-of-balls-in-a-bag",
        "title": "Minimum Limit of Balls in a Bag",
        "difficulty": "Medium",
        "pattern": "binary search on the maximum size",
        "statement": "Each operation splits one bag into two bags with the same total. With at most maxOperations splits, return the smallest "
                     "possible maximum bag size.",
        "examples": [("nums = [9], maxOperations = 2", "3"), ("nums = [2,4,8,2], maxOperations = 4", "2")],
        "constraints": ["1 <= n <= 10^5", "1 <= values, maxOperations <= 10^9", "the answer is at least 1"],
        "approach": "Test a candidate maximum size m: a bag of size v needs ceil(v/m) - 1 splits to get every piece down to at most m, and the "
                     "test is monotone in m. Summing that over all bags gives feasibility, and the search finds the smallest feasible m.",
        "complexity": ("O(n log max)", "O(1)"),
        "code": {
            "cpp": r"""// Splits needed for limit m: sum(ceil(v / m) - 1)
int minimumSize(vector<int>& nums, int maxOps) {
    auto splitsNeeded = [&](int m) {
        long long ops = 0;
        for (int v : nums) ops += (v + m - 1) / m - 1;
        return ops;
    };
    int lo = 1, hi = *max_element(nums.begin(), nums.end());
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (splitsNeeded(mid) <= maxOps) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(n log max) time · O(1) space""",
            "java": r"""// Splits needed for limit m: sum(ceil(v / m) - 1)
int minimumSize(int[] nums, int maxOps) {
    int lo = 1, hi = 0;
    for (int v : nums) hi = Math.max(hi, v);
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        long ops = 0;
        for (int v : nums) ops += (v + mid - 1) / mid - 1;
        if (ops <= maxOps) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(n log max) time · O(1) space""",
            "python": r"""def minimum_size(nums, max_ops):
    def splits_needed(m):
        return sum((v + m - 1) // m - 1 for v in nums)   # ceil(v/m) - 1 per bag

    lo, hi = 1, max(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if splits_needed(mid) <= max_ops:
            hi = mid
        else:
            lo = mid + 1
    return lo""",
        },
    },
    {
        "slug": "minimum-days-to-make-bouquets",
        "title": "Minimum Days to Make Bouquets",
        "difficulty": "Medium",
        "pattern": "binary search on days",
        "statement": "Flower i blooms on day bloomDay[i]. A bouquet needs m adjacent flowers that have already bloomed. Return the earliest day "
                     "on which m bouquets of k adjacent flowers each can be made, or -1 if impossible.",
        "examples": [("bloomDay = [1,10,3,10,2], m = 3, k = 1", "3"), ("bloomDay = [1,10,3,10,2], m = 3, k = 2", "-1"),
                     ("bloomDay = [7,7,7,7,12,7,7], m = 2, k = 3", "12")],
        "constraints": ["1 <= n <= 10^5", "1 <= bloomDay, m, k <= 10^9", "the flowers used for a bouquet must be adjacent"],
        "approach": "For a candidate day, walk the array and count consecutive bloomed flowers, cutting a bouquet whenever the run reaches k. "
                     "That count is non-decreasing in the day, so binary search it. Check the impossible case up front instead of writing a "
                     "sentinel into the search.",
        "complexity": ("O(n log max)", "O(1)"),
        "code": {
            "cpp": r"""// Feasible(day) is monotone; bouquets = sum of runs / k
int minDays(vector<int>& bloom, int m, int k) {
    if ((long long)m * k > (long long)bloom.size()) return -1;   // impossible
    auto bouquets = [&](int day) {
        int made = 0, run = 0;
        for (int d : bloom) {
            if (d <= day) { if (++run == k) { made++; run = 0; } }
            else run = 0;
        }
        return made;
    };
    int lo = *min_element(bloom.begin(), bloom.end());
    int hi = *max_element(bloom.begin(), bloom.end());
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (bouquets(mid) >= m) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(n log max) time · O(1) space""",
            "java": r"""// Feasible(day) is monotone; bouquets grow with consecutive bloomed runs
int minDays(int[] bloom, int m, int k) {
    if ((long) m * k > bloom.length) return -1;      // impossible
    int lo = Integer.MAX_VALUE, hi = 0;
    for (int d : bloom) { lo = Math.min(lo, d); hi = Math.max(hi, d); }
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2, made = 0, run = 0;
        for (int d : bloom) {
            if (d <= mid) { if (++run == k) { made++; run = 0; } }
            else run = 0;
        }
        if (made >= m) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(n log max) time · O(1) space""",
            "python": r"""def min_days(bloom, m, k):
    if m * k > len(bloom):
        return -1                     # impossible even if all flowers bloom
    def bouquets(day):
        made = run = 0
        for d in bloom:
            if d <= day:
                run += 1
                if run == k:          # k adjacent bloomed flowers
                    made += 1
                    run = 0
            else:
                run = 0
        return made

    lo, hi = min(bloom), max(bloom)
    while lo < hi:
        mid = (lo + hi) // 2
        if bouquets(mid) >= m:
            hi = mid
        else:
            lo = mid + 1
    return lo""",
        },
    },
    # ------------------------------------------------------------------ HARD
    {
        "slug": "median-of-two-sorted-arrays",
        "title": "Median of Two Sorted Arrays",
        "difficulty": "Hard",
        "pattern": "partition the shorter array",
        "statement": "Return the median of two sorted arrays, in O(log(min(n, m))) time.",
        "examples": [("a = [1,3], b = [2]", "2.0"), ("a = [1,2], b = [3,4]", "2.5")],
        "constraints": ["0 <= len(a), len(b) <= 1000", "1 <= len(a) + len(b) <= 2000", "the combined time must be logarithmic, not linear"],
        "approach": "The median splits the merged data into a left half and a right half of fixed sizes. Guess how many elements of the left half "
                     "come from the first array; that choice determines everything else. The guess is right when the biggest left element is not "
                     "bigger than the smallest right element, so binary search that count — on the shorter array, so the search is as short as "
                     "possible.",
        "complexity": ("O(log min(n, m))", "O(1)"),
        "code": {
            "cpp": r"""// Search how many of the left half's elements come from a
double findMedianSortedArrays(vector<int>& a, vector<int>& b) {
    if (a.size() > b.size()) swap(a, b);         // search the shorter array
    int n = a.size(), m = b.size(), half = (n + m + 1) / 2;
    int lo = 0, hi = n;
    while (lo <= hi) {
        int i = (lo + hi) / 2, j = half - i;     // i from a, j from b
        int aL = i ? a[i-1] : INT_MIN, aR = i < n ? a[i] : INT_MAX;
        int bL = j ? b[j-1] : INT_MIN, bR = j < m ? b[j] : INT_MAX;
        if (aL <= bR && bL <= aR) {               // correct split
            if ((n + m) % 2) return max(aL, bL);
            return (max(aL, bL) + min(aR, bR)) / 2.0;
        }
        if (aL > bR) hi = i - 1;                 // took too many from a
        else lo = i + 1;
    }
    return 0.0;
}   // O(log min(n, m)) time · O(1) space""",
            "java": r"""// Search how many of the left half's elements come from a
double findMedianSortedArrays(int[] a, int[] b) {
    if (a.length > b.length) { int[] t = a; a = b; b = t; }   // search the shorter
    int n = a.length, m = b.length, half = (n + m + 1) / 2;
    int lo = 0, hi = n;
    while (lo <= hi) {
        int i = (lo + hi) / 2, j = half - i;     // i from a, j from b
        int aL = i > 0 ? a[i-1] : Integer.MIN_VALUE, aR = i < n ? a[i] : Integer.MAX_VALUE;
        int bL = j > 0 ? b[j-1] : Integer.MIN_VALUE, bR = j < m ? b[j] : Integer.MAX_VALUE;
        if (aL <= bR && bL <= aR) {               // correct split
            if (((n + m) & 1) == 1) return Math.max(aL, bL);
            return (Math.max(aL, bL) + Math.min(aR, bR)) / 2.0;
        }
        if (aL > bR) hi = i - 1;                  // took too many from a
        else lo = i + 1;
    }
    return 0.0;
}   // O(log min(n, m)) time · O(1) space""",
            "python": r"""def find_median_sorted_arrays(a, b):
    if len(a) > len(b):
        a, b = b, a                  # search the shorter array
    n, m = len(a), len(b)
    half = (n + m + 1) // 2
    lo, hi = 0, n
    while lo <= hi:
        i = (lo + hi) // 2           # how many of the left half come from a
        j = half - i
        aL = a[i-1] if i else float('-inf')
        aR = a[i] if i < n else float('inf')
        bL = b[j-1] if j else float('-inf')
        bR = b[j] if j < m else float('inf')
        if aL <= bR and bL <= aR:    # correct split
            if (n + m) % 2:
                return float(max(aL, bL))
            return (max(aL, bL) + min(aR, bR)) / 2.0
        if aL > bR:
            hi = i - 1               # took too many from a
        else:
            lo = i + 1
    return 0.0""",
        },
    },
    {
        "slug": "find-minimum-in-rotated-sorted-array-ii",
        "title": "Find Minimum in Rotated Sorted Array II",
        "difficulty": "Hard",
        "pattern": "rotation + duplicates",
        "statement": "A sorted array that may contain duplicates was rotated; return its minimum element.",
        "examples": [("nums = [1,3,5]", "1"), ("nums = [2,2,2,0,1]", "0")],
        "constraints": ["1 <= n <= 5000", "the array is a rotation of a sorted array with possible duplicates", "an O(n) worst case is acceptable"],
        "approach": "The duplicate-free version compares a[mid] with a[hi]. With duplicates, equality carries no information, so the safe move "
                     "is hi-- and retry. Each shrink either discards a copy of the minimum or keeps one, which is why the worst case is linear "
                     "while the average stays logarithmic.",
        "complexity": ("O(log n) average, O(n) worst", "O(1)"),
        "code": {
            "cpp": r"""// Equality with a[hi] says nothing: shrink hi and retry
int findMin(vector<int>& a) {
    int lo = 0, hi = a.size() - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] > a[hi]) lo = mid + 1;        // minimum is strictly right
        else if (a[mid] < a[hi]) hi = mid;       // minimum is at mid or left
        else hi--;                               // duplicates: discard one copy
    }
    return a[lo];
}   // O(log n) average, O(n) worst time · O(1) space""",
            "java": r"""// Equality with a[hi] says nothing: shrink hi and retry
int findMin(int[] a) {
    int lo = 0, hi = a.length - 1;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] > a[hi]) lo = mid + 1;        // minimum is strictly right
        else if (a[mid] < a[hi]) hi = mid;       // minimum is at mid or left
        else hi--;                               // duplicates: discard one copy
    }
    return a[lo];
}   // O(log n) average, O(n) worst time · O(1) space""",
            "python": r"""def find_min_rotated_duplicates(a):
    lo, hi = 0, len(a) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] > a[hi]:
            lo = mid + 1            # the minimum is strictly to the right
        elif a[mid] < a[hi]:
            hi = mid                # the minimum is at mid or to the left
        else:
            hi -= 1                 # duplicates: discard one copy and retry
    return a[lo]""",
        },
    },
    {
        "slug": "split-array-largest-sum",
        "title": "Split Array Largest Sum",
        "difficulty": "Hard",
        "pattern": "binary search on the largest piece",
        "statement": "Split the array into exactly k non-empty contiguous subarrays so that the largest subarray sum is as small as possible; "
                     "return that smallest largest sum.",
        "examples": [("nums = [7,2,5,10,8], k = 2", "18"), ("nums = [1,2,3,4,5], k = 2", "9")],
        "constraints": ["1 <= n <= 1000", "1 <= k <= n", "0 <= values <= 10^6"],
        "approach": "Same shape as the shipping problem, with a twist: the number of pieces the greedy pass produces *decreases* as the allowed "
                     "sum grows, so feasibility is 'pieces <= k'. The answer must also be at least the largest single element — that lower bound "
                     "is what rules out impossible configurations.",
        "complexity": ("O(n log sum)", "O(1)"),
        "code": {
            "cpp": r"""// Feasible(limit) = greedy pass needs at most k pieces
int splitArray(vector<int>& a, int k) {
    auto fits = [&](long long limit) {
        int pieces = 1; long long cur = 0;
        for (int v : a) {
            if (cur + v > limit) { pieces++; cur = 0; }   // cut here
            cur += v;
        }
        return pieces <= k;
    };
    long long lo = *max_element(a.begin(), a.end());      // must hold the biggest
    long long hi = accumulate(a.begin(), a.end(), 0LL);
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        if (fits(mid)) hi = mid;
        else lo = mid + 1;
    }
    return (int)lo;
}   // O(n log sum) time · O(1) space""",
            "java": r"""// Feasible(limit) = greedy pass needs at most k pieces
int splitArray(int[] a, int k) {
    long lo = 0, hi = 0;
    for (int v : a) { lo = Math.max(lo, v); hi += v; }     // must hold the biggest
    while (lo < hi) {
        long mid = lo + (hi - lo) / 2;
        int pieces = 1; long cur = 0;
        for (int v : a) {
            if (cur + v > mid) { pieces++; cur = 0; }      // cut here
            cur += v;
        }
        if (pieces <= k) hi = mid;
        else lo = mid + 1;
    }
    return (int) lo;
}   // O(n log sum) time · O(1) space""",
            "python": r"""def split_array(a, k):
    def fits(limit):
        pieces, cur = 1, 0
        for v in a:
            if cur + v > limit:
                pieces += 1        # cut here
                cur = 0
            cur += v
        return pieces <= k

    lo, hi = max(a), sum(a)        # the biggest element must fit somewhere
    while lo < hi:
        mid = (lo + hi) // 2
        if fits(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo""",
        },
    },
    {
        "slug": "kth-smallest-number-in-multiplication-table",
        "title": "K-th Smallest Number in a Multiplication Table",
        "difficulty": "Hard",
        "pattern": "count elements <= x",
        "statement": "In the m × n multiplication table (row i holds i, 2i, 3i, ...), return the k-th smallest number.",
        "examples": [("m = 3, n = 3, k = 5", "3"), ("m = 2, n = 3, k = 6", "6")],
        "constraints": ["1 <= m, n <= 3 * 10^4", "1 <= k <= m * n", "values fit in a 32-bit integer"],
        "approach": "Binary search the value, not a position: count how many table entries are <= x with min(n, x / i) summed over rows. That "
                     "count is monotone in x, and the first x whose count reaches k is the answer — even though x itself may not appear in the "
                     "table, which is the subtle part of the argument.",
        "complexity": ("O(m log(m · n))", "O(1)"),
        "code": {
            "cpp": r"""// Binary search the value; count entries <= x with min(n, x / i)
int findKthNumber(int m, int n, int k) {
    int lo = 1, hi = m * n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        int cnt = 0;
        for (int r = 1; r <= m; r++) cnt += min(n, mid / r);   // row r has mid/r hits
        if (cnt >= k) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(m log(m·n)) time · O(1) space""",
            "java": r"""// Binary search the value; count entries <= x with min(n, x / i)
int findKthNumber(int m, int n, int k) {
    int lo = 1, hi = m * n;
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2, cnt = 0;
        for (int r = 1; r <= m; r++) cnt += Math.min(n, mid / r);   // row r hits
        if (cnt >= k) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(m log(m·n)) time · O(1) space""",
            "python": r"""def find_kth_in_table(m, n, k):
    def count_le(x):
        return sum(min(n, x // r) for r in range(1, m + 1))   # row r hits

    lo, hi = 1, m * n
    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid               # the k-th value is at most mid
        else:
            lo = mid + 1
    return lo""",
        },
    },
    {
        "slug": "find-k-th-smallest-pair-distance",
        "title": "K-th Smallest Pair Distance",
        "difficulty": "Hard",
        "pattern": "binary search a distance, count pairs",
        "statement": "Return the k-th smallest distance among all pairs of elements of the array (distances counted with multiplicity).",
        "examples": [("nums = [1,3,1], k = 1", "0"), ("nums = [1,1,1], k = 2", "0"), ("nums = [1,6,1], k = 3", "5")],
        "constraints": ["2 <= n <= 10^4", "0 <= values <= 10^6", "1 <= k <= n · (n - 1) / 2"],
        "approach": "Sorting turns 'how many pairs are within distance d' into a two-pointer count in linear time, and that count is monotone in "
                     "d. So binary search d over [0, max - min]: a distance is a valid answer exactly when at least k pairs are within it, and the "
                     "pairs need never be enumerated.",
        "complexity": ("O(n log n + n log maxDist)", "O(1)"),
        "code": {
            "cpp": r"""// Sort, then binary search d and two-pointer count pairs within d
int smallestDistancePair(vector<int>& a, int k) {
    sort(a.begin(), a.end());
    int n = a.size(), lo = 0, hi = a.back() - a.front();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        long long cnt = 0;
        for (int i = 0, j = 0; i < n; i++) {
            while (a[i] - a[j] > mid) j++;        // shrink the window
            cnt += i - j;                         // pairs ending at i, within mid
        }
        if (cnt >= k) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(n log n + n log maxDist) time · O(1) space""",
            "java": r"""// Sort, then binary search d and two-pointer count pairs within d
int smallestDistancePair(int[] a, int k) {
    Arrays.sort(a);
    int n = a.length, lo = 0, hi = a[n - 1] - a[0];
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        long cnt = 0;
        for (int i = 0, j = 0; i < n; i++) {
            while (a[i] - a[j] > mid) j++;        // shrink the window
            cnt += i - j;                         // pairs ending at i, within mid
        }
        if (cnt >= k) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O(n log n + n log maxDist) time · O(1) space""",
            "python": r"""def smallest_distance_pair(a, k):
    a.sort()
    n = len(a)
    lo, hi = 0, a[-1] - a[0]
    while lo < hi:
        mid = (lo + hi) // 2
        cnt, j = 0, 0
        for i in range(n):
            while a[i] - a[j] > mid:
                j += 1                  # shrink the window
            cnt += i - j                # pairs ending at i within mid
        if cnt >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo""",
        },
    },
    {
        "slug": "preimage-size-of-factorial-zeroes-function",
        "title": "Preimage Size of Factorial Zeroes Function",
        "difficulty": "Hard",
        "pattern": "monotone step function",
        "statement": "Given k, count how many non-negative integers x satisfy: the number of trailing zeros of x! is exactly k.",
        "examples": [("k = 0", "5"), ("k = 5", "0"), ("k = 3", "5")],
        "constraints": ["0 <= k <= 10^9", "trailing zeros of x! = floor(x/5) + floor(x/25) + ...", "the answer is always 0 or 5"],
        "approach": "The trailing-zero count f(x) = Σ floor(x / 5^i) — a monotone step function that never increases by more than 1 per step and "
                     "jumps by exactly 1 at multiples of 5. A value k therefore has either 5 preimages (a full block of consecutive x) or none. "
                     "Binary search the smallest x with f(x) >= k and test whether f(x) equals k.",
        "complexity": ("O(log² k)", "O(1)"),
        "code": {
            "cpp": r"""// f(x) is monotone and never skips 5 in a row; binary search it
long long trailingZeros(long long x) {
    long long c = 0;
    while (x) { x /= 5; c += x; }
    return c;
}
int preimageSizeFZF(int k) {
    long long lo = 0, hi = (long long)k * 5 + 5;
    while (lo < hi) {                             // smallest x with f(x) >= k
        long long mid = lo + (hi - lo) / 2;
        if (trailingZeros(mid) < k) lo = mid + 1;
        else hi = mid;
    }
    return trailingZeros(lo) == k ? 5 : 0;        // a block of 5, or nothing
}   // O(log² k) time · O(1) space""",
            "java": r"""// f(x) is monotone and never skips 5 in a row; binary search it
long trailingZeros(long x) {
    long c = 0;
    while (x > 0) { x /= 5; c += x; }
    return c;
}
int preimageSizeFZF(int k) {
    long lo = 0, hi = (long) k * 5 + 5;
    while (lo < hi) {                             // smallest x with f(x) >= k
        long mid = lo + (hi - lo) / 2;
        if (trailingZeros(mid) < k) lo = mid + 1;
        else hi = mid;
    }
    return trailingZeros(lo) == k ? 5 : 0;        // a block of 5, or nothing
}   // O(log² k) time · O(1) space""",
            "python": r"""def preimage_size_fzf(k):
    def trailing_zeros(x):
        c = 0
        while x:
            x //= 5
            c += x
        return c

    lo, hi = 0, k * 5 + 5
    while lo < hi:                    # smallest x with f(x) >= k
        mid = (lo + hi) // 2
        if trailing_zeros(mid) < k:
            lo = mid + 1
        else:
            hi = mid
    return 5 if trailing_zeros(lo) == k else 0   # a block of 5, or nothing""",
        },
    },
    {
        "slug": "nth-magical-number",
        "title": "N-th Magical Number",
        "difficulty": "Hard",
        "pattern": "count multiples with inclusion-exclusion",
        "statement": "A positive integer is magical if it is divisible by a or by b. Return the n-th magical number, modulo 10^9 + 7.",
        "examples": [("n = 1, a = 2, b = 3", "2"), ("n = 4, a = 2, b = 3", "6")],
        "constraints": ["1 <= n <= 10^9", "2 <= a, b <= 4 * 10^4", "the answer is reported modulo 10^9 + 7"],
        "approach": "Counting multiplies of a or b up to x is inclusion-exclusion: x/a + x/b - x/lcm(a, b). That count is monotone, so binary "
                     "search the smallest x whose count reaches n, with an upper bound of n · min(a, b) — a multiple of min(a, b) supplies n "
                     "magical numbers at most that far out.",
        "complexity": ("O(log(n · min(a, b)))", "O(1)"),
        "code": {
            "cpp": r"""// Inclusion-exclusion count, then binary search the value
int nthMagicalNumber(int n, int a, int b) {
    const long long MOD = 1000000007;
    long long l = (long long)a / __gcd(a, b) * b;          // lcm
    long long lo = 1, hi = (long long)min(a, b) * n;
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;
        long long cnt = mid / a + mid / b - mid / l;       // magical <= mid
        if (cnt >= n) hi = mid;
        else lo = mid + 1;
    }
    return (int)(lo % MOD);
}   // O(log(n · min(a, b))) time · O(1) space""",
            "java": r"""// Inclusion-exclusion count, then binary search the value
int nthMagicalNumber(int n, int a, int b) {
    final long MOD = 1000000007L;
    long l = (long) a / gcd(a, b) * b;                     // lcm
    long lo = 1, hi = (long) Math.min(a, b) * n;
    while (lo < hi) {
        long mid = lo + (hi - lo) / 2;
        long cnt = mid / a + mid / b - mid / l;            // magical <= mid
        if (cnt >= n) hi = mid;
        else lo = mid + 1;
    }
    return (int) (lo % MOD);
}
static int gcd(int x, int y) { return y == 0 ? x : gcd(y, x % y); }
// O(log(n · min(a, b))) time · O(1) space""",
            "python": r"""from math import gcd

def nth_magical_number(n, a, b):
    MOD = 10**9 + 7
    l = a // gcd(a, b) * b              # lcm
    lo, hi = 1, min(a, b) * n
    while lo < hi:
        mid = (lo + hi) // 2
        cnt = mid // a + mid // b - mid // l     # magical numbers <= mid
        if cnt >= n:
            hi = mid
        else:
            lo = mid + 1
    return lo % MOD""",
        },
    },
    {
        "slug": "super-egg-drop",
        "title": "Super Egg Drop",
        "difficulty": "Hard",
        "pattern": "search on moves, not floors",
        "statement": "With k identical eggs and n floors, return the minimum number of moves that guarantees finding the critical floor in the "
                     "worst case.",
        "examples": [("k = 1, n = 2", "2"), ("k = 2, n = 6", "3"), ("k = 3, n = 14", "4")],
        "constraints": ["1 <= k <= 100", "1 <= n <= 10^4", "a broken egg is lost; the worst case is what counts"],
        "approach": "Instead of asking 'how many floors can I solve with m moves', note that dropping an egg splits the remaining floors into "
                     "the ones above (if it survives, with k eggs and m-1 moves) and the ones below (if it breaks, with k-1 eggs and m-1 "
                     "moves). So dp[k][m] = dp[k][m-1] + dp[k-1][m-1] + 1, and the answer is the smallest m with dp[k][m] >= n — an O(k log n) "
                     "loop instead of the naive O(k n²) table.",
        "complexity": ("O(k log n)", "O(k)"),
        "code": {
            "cpp": r"""// dp[e] = floors resolvable with e eggs and the current move count
int superEggDrop(int k, int n) {
    vector<int> dp(k + 1, 0);                    // dp[e] for m moves so far
    int moves = 0;
    while (dp[k] < n) {
        for (int e = k; e >= 1; e--)             // descending: use last move's values
            dp[e] = dp[e] + dp[e - 1] + 1;       // survive + break + this floor
        moves++;
    }
    return moves;
}   // O(k log n) time (at most n moves) · O(k) space""",
            "java": r"""// dp[e] = floors resolvable with e eggs and the current move count
int superEggDrop(int k, int n) {
    int[] dp = new int[k + 1];                   // dp[e] for m moves so far
    int moves = 0;
    while (dp[k] < n) {
        for (int e = k; e >= 1; e--)             // descending: use last move's values
            dp[e] = dp[e] + dp[e - 1] + 1;       // survive + break + this floor
        moves++;
    }
    return moves;
}   // O(k log n) time (at most n moves) · O(k) space""",
            "python": r"""def super_egg_drop(k, n):
    dp = [0] * (k + 1)             # dp[e] = floors resolvable with e eggs, m moves
    moves = 0
    while dp[k] < n:
        for e in range(k, 0, -1):  # descending keeps the previous move's values
            dp[e] = dp[e] + dp[e - 1] + 1   # survive + break + this floor
        moves += 1
    return moves""",
        },
    },
    {
        "slug": "find-in-mountain-array",
        "title": "Find in a Mountain Array",
        "difficulty": "Hard",
        "pattern": "find the peak, then two searches",
        "statement": "The array rises strictly to a peak and then falls strictly. Using only the API arr.get(i) (limited to 100 calls), return "
                     "the smallest index holding the target, or -1.",
        "examples": [("mountain = [1,2,3,4,5,3,1], target = 3", "2"), ("mountain = [0,1,2,4,2,1], target = 3", "-1")],
        "constraints": ["3 <= n <= 10^4", "values are distinct around the peak", "at most 100 calls to get()"],
        "approach": "Three binary searches: one on the slope to find the peak, one ascending search on the left part and one descending search on "
                     "the right part. Because you must return the *smallest* index, search the left part first and only fall through to the right "
                     "if it fails.",
        "complexity": ("O(log n)", "O(1)"),
        "code": {
            "cpp": r"""// Peak, then ascending search left, then descending search right
struct MountainArray {                        // provided by the judge
    int get(int index);
    int length();
};
int findInMountainArray(int target, MountainArray& arr) {
    int n = arr.length(), lo = 0, hi = n - 1;
    while (lo < hi) {                            // 1. find the peak
        int mid = lo + (hi - lo) / 2;
        if (arr.get(mid) < arr.get(mid + 1)) lo = mid + 1;
        else hi = mid;
    }
    int peak = lo;
    lo = 0; hi = peak;
    while (lo <= hi) {                           // 2. ascending half
        int mid = lo + (hi - lo) / 2, v = arr.get(mid);
        if (v == target) return mid;
        if (v < target) lo = mid + 1;
        else hi = mid - 1;
    }
    lo = peak + 1; hi = n - 1;
    while (lo <= hi) {                           // 3. descending half
        int mid = lo + (hi - lo) / 2, v = arr.get(mid);
        if (v == target) return mid;
        if (v > target) lo = mid + 1;            // reversed comparison
        else hi = mid - 1;
    }
    return -1;
}   // O(log n) time · O(1) space""",
            "java": r"""// Peak, then ascending search left, then descending search right
interface MountainArray { int get(int index); int length(); }   // judge API
int findInMountainArray(int target, MountainArray arr) {
    int n = arr.length(), lo = 0, hi = n - 1;
    while (lo < hi) {                            // 1. find the peak
        int mid = lo + (hi - lo) / 2;
        if (arr.get(mid) < arr.get(mid + 1)) lo = mid + 1;
        else hi = mid;
    }
    int peak = lo;
    lo = 0; hi = peak;
    while (lo <= hi) {                           // 2. ascending half
        int mid = lo + (hi - lo) / 2, v = arr.get(mid);
        if (v == target) return mid;
        if (v < target) lo = mid + 1;
        else hi = mid - 1;
    }
    lo = peak + 1; hi = n - 1;
    while (lo <= hi) {                           // 3. descending half
        int mid = lo + (hi - lo) / 2, v = arr.get(mid);
        if (v == target) return mid;
        if (v > target) lo = mid + 1;            // reversed comparison
        else hi = mid - 1;
    }
    return -1;
}   // O(log n) time · O(1) space""",
            "python": r"""def find_in_mountain_array(target, arr):
    n = arr.length()
    lo, hi = 0, n - 1
    while lo < hi:                        # 1. find the peak
        mid = (lo + hi) // 2
        if arr.get(mid) < arr.get(mid + 1):
            lo = mid + 1
        else:
            hi = mid
    peak = lo
    lo, hi = 0, peak
    while lo <= hi:                       # 2. ascending half
        mid = (lo + hi) // 2
        v = arr.get(mid)
        if v == target:
            return mid
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    lo, hi = peak + 1, n - 1
    while lo <= hi:                       # 3. descending half
        mid = (lo + hi) // 2
        v = arr.get(mid)
        if v == target:
            return mid
        if v > target:                    # reversed comparison
            lo = mid + 1
        else:
            hi = mid - 1
    return -1""",
        },
    },
    {
        "slug": "divide-chocolate",
        "title": "Divide Chocolate",
        "difficulty": "Hard",
        "pattern": "binary search + run counting",
        "statement": "Split the chocolate pieces (in order) among k+1 people so that everybody gets one contiguous run, and maximise the minimum "
                     "total sweetness anyone receives.",
        "examples": [("sweetness = [1,2,3,4,5,6,7,8,9], k = 5", "6"), ("sweetness = [5,6,7,8,9,1,2,3,4], k = 8", "1"),
                     ("sweetness = [1,2,2,1,2,2,1,2,2], k = 2", "5")],
        "constraints": ["1 <= n <= 10^4", "0 <= sweetness <= 10^4", "0 <= k < n"],
        "approach": "Maximising the minimum is again monotone: test whether it is possible to hand out at least k+1 pieces each of sum >= m, by "
                     "greedily cutting as soon as a run reaches m. The search then takes the largest feasible m — the classic 'maximise the "
                     "minimum / minimise the maximum' duality with the previous problems.",
        "complexity": ("O(n log sum)", "O(1)"),
        "code": {
            "cpp": r"""// Greedily count pieces with sum >= m; take the largest feasible m
int maximizeSweetness(vector<int>& s, int k) {
    auto piecesAtLeast = [&](int m) {
        int pieces = 0, run = 0;
        for (int v : s) {
            run += v;
            if (run >= m) { pieces++; run = 0; }     // cut as soon as possible
        }
        return pieces;
    };
    int lo = 0, hi = accumulate(s.begin(), s.end(), 0);
    while (lo < hi) {
        int mid = lo + (hi - lo + 1) / 2;            // upper mid: move lo up
        if (piecesAtLeast(mid) >= k + 1) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}   // O(n log sum) time · O(1) space""",
            "java": r"""// Greedily count pieces with sum >= m; take the largest feasible m
int maximizeSweetness(int[] s, int k) {
    int lo = 0, hi = 0;
    for (int v : s) hi += v;
    while (lo < hi) {
        int mid = lo + (hi - lo + 1) / 2;            // upper mid: move lo up
        int pieces = 0, run = 0;
        for (int v : s) {
            run += v;
            if (run >= mid) { pieces++; run = 0; }   // cut as soon as possible
        }
        if (pieces >= k + 1) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}   // O(n log sum) time · O(1) space""",
            "python": r"""def maximize_sweetness(s, k):
    def pieces_at_least(m):
        pieces = run = 0
        for v in s:
            run += v
            if run >= m:              # cut as soon as somebody is satisfied
                pieces += 1
                run = 0
        return pieces

    lo, hi = 0, sum(s)
    while lo < hi:
        mid = (lo + hi + 1) // 2      # upper mid so lo can move up
        if pieces_at_least(mid) >= k + 1:
            lo = mid
        else:
            hi = mid - 1
    return lo""",
        },
    },
    {
        "slug": "k-th-smallest-in-lexicographical-order",
        "title": "K-th Smallest in Lexicographical Order",
        "difficulty": "Hard",
        "pattern": "prefix counting (trie walk)",
        "statement": "Return the k-th smallest integer in the range 1..n when the numbers are ordered lexicographically (as strings).",
        "examples": [("n = 13, k = 2", "10"), ("n = 1, k = 1", "1")],
        "constraints": ["1 <= k <= n <= 10^9", "0-based vs 1-based indexing is the usual trap here", "an O(log n) walk is expected"],
        "approach": "The lexicographic order is a pre-order walk of a ten-ary tree of prefixes. For the current prefix, count how many nodes that "
                     "prefix would contain (all numbers starting with it, level by level); if the count fits inside the remaining k, skip the "
                     "whole subtree, otherwise step down into it by appending a zero.",
        "complexity": ("O(log² n)", "O(1)"),
        "code": {
            "cpp": r"""// Count nodes under a prefix; skip the subtree or descend into it
long long countSteps(long long n, long long first, long long next) {
    long long steps = 0;
    while (first <= n) {
        steps += min(n, next - 1) - first + 1;   // whole level under the prefix
        first *= 10; next *= 10;
    }
    return steps;
}
int findKthNumber(int n, int k) {
    long long cur = 1;
    k--;                                         // 1 is the first number
    while (k > 0) {
        long long steps = countSteps(n, cur, cur + 1);
        if (steps <= k) { k -= steps; cur++; }   // skip this whole subtree
        else { cur *= 10; k--; }                 // descend one level
    }
    return (int)cur;
}   // O(log² n) time · O(1) space""",
            "java": r"""// Count nodes under a prefix; skip the subtree or descend into it
long countSteps(long n, long first, long next) {
    long steps = 0;
    while (first <= n) {
        steps += Math.min(n, next - 1) - first + 1;   // whole level under it
        first *= 10; next *= 10;
    }
    return steps;
}
int findKthNumber(int n, int k) {
    long cur = 1;
    k--;                                          // 1 is the first number
    while (k > 0) {
        long steps = countSteps(n, cur, cur + 1);
        if (steps <= k) { k -= steps; cur++; }    // skip this whole subtree
        else { cur *= 10; k--; }                  // descend one level
    }
    return (int) cur;
}   // O(log² n) time · O(1) space""",
            "python": r"""def find_kth_lexicographic(n, k):
    def count_steps(first, nxt):
        steps = 0
        while first <= n:
            steps += min(n, nxt - 1) - first + 1   # everything on this level
            first *= 10
            nxt *= 10
        return steps

    cur = 1
    k -= 1                       # 1 is the first number in the order
    while k > 0:
        steps = count_steps(cur, cur + 1)
        if steps <= k:
            k -= steps           # skip the whole prefix subtree
            cur += 1
        else:
            cur *= 10            # descend one level
            k -= 1
    return cur""",
        },
    },
    {
        "slug": "maximum-running-time-of-n-computers",
        "title": "Maximum Running Time of N Computers",
        "difficulty": "Hard",
        "pattern": "binary search the runtime with a capped sum",
        "statement": "n computers must run simultaneously, and the i-th battery holds batteries[i] minutes. Batteries can be plugged, unplugged "
                     "and moved between computers at any moment. Return the maximum number of minutes all n computers can run together.",
        "examples": [("n = 2, batteries = [3,3,3]", "4"), ("n = 2, batteries = [1,1,1,1]", "2")],
        "constraints": ["1 <= n <= 10^5", "1 <= batteries[i] <= 10^9", "each computer consumes one unit of battery per minute"],
        "approach": "Test a candidate runtime t: a battery can contribute at most t minutes (it cannot power two computers at once), so the total "
                     "available is Σ min(battery, t), and t is feasible when that is at least n · t. The capped sum is monotone in t, so binary "
                     "search it — a nice reminder that feasibility checks can ignore ordering rules when resources are freely reassignable.",
        "complexity": ("O(len(batteries) · log(sum / n))", "O(1)"),
        "code": {
            "cpp": r"""// Feasible(t): capped sum of batteries >= n * t
long long maxRunTime(int n, vector<int>& batteries) {
    auto feasible = [&](long long t) {
        long long usable = 0;
        for (int b : batteries) usable += min<long long>(b, t);   // cap each battery
        return usable >= t * n;
    };
    long long lo = 0, hi = accumulate(batteries.begin(), batteries.end(), 0LL) / n;
    while (lo < hi) {
        long long mid = lo + (hi - lo + 1) / 2;
        if (feasible(mid)) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}   // O(m log(sum/n)) time · O(1) space""",
            "java": r"""// Feasible(t): capped sum of batteries >= n * t
long maxRunTime(int n, int[] batteries) {
    long lo = 0, total = 0;
    for (int b : batteries) total += b;
    long hi = total / n;
    while (lo < hi) {
        long mid = lo + (hi - lo + 1) / 2, usable = 0;
        for (int b : batteries) usable += Math.min(b, mid);   // cap each battery
        if (usable >= mid * n) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}   // O(m log(sum/n)) time · O(1) space""",
            "python": r"""def max_run_time(n, batteries):
    def feasible(t):
        usable = sum(min(b, t) for b in batteries)   # cap each battery at t
        return usable >= t * n

    lo, hi = 0, sum(batteries) // n
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo""",
        },
    },
]
