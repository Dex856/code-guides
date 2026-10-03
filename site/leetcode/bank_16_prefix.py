# Topic 16 · Prefix Sums & Range Queries
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.

TOPIC = {
    "name": "Prefix Sums & Range Queries",
    "tagline": "Precompute once, answer forever: a running total turns any range into a subtraction.",
    "focus": "The whole topic rests on one identity: sum(l..r) = prefix[r + 1] - prefix[l]. Everything else is a variation on what the prefix carries — "
             "sums for range weight, remainders for divisibility, XOR for parity, counts per value for frequency questions, and per-row prefixes for 2D "
             "blocks. When the array keeps changing, a Fenwick tree stores the same information in a form that survives updates; when the question is "
             "\"how many subarrays sum to k\", the prefixes themselves become a hash map or a sorted list, and counting pairs replaces scanning. "
             "Difference arrays are the inverse view: they record where a value starts and stops mattering instead of what it is.",
    "ordering": "easy 1–2 build and use a prefix array, 3–4 match left and right sums, 5–6 track a running total while scanning; medium 1–3 cover 2D "
                "prefixes, prefix/suffix products and split sums, 4–5 turn prefixes into hash maps and XOR states, 6–7 pair prefixes with a sorted "
                "array and a squared block, 8 moves to sliding windows over prefixes, 9–12 add updates (Fenwick), per-value frequencies, per-value "
                "counts and sorted subarray sums; hard 1–2 read arrays as difference arrays, 3–5 combine prefix tables with window and index "
                "structures, 6–9 count pairs and triplets with Fenwick and merge sorting, 10–12 push prefixes through monotonic stacks, two-pointer "
                "windows and sorted contributions.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "running-sum-of-1d-array",
        "title": "Running Sum of 1d Array",
        "difficulty": "Easy",
        "pattern": "accumulate in place",
        "statement": "Return the running sum of nums: the i-th entry is the sum of nums[0..i].",
        "examples": [("nums = [1,2,3,4]", "[1,3,6,10]"), ("nums = [1,1,1,1,1]", "[1,2,3,4,5]"), ("nums = [3,1,2,10,1]", "[3,4,6,16,17]")],
        "constraints": ["1 <= nums.length <= 1000", "-10^6 <= nums[i] <= 10^6"],
        "approach": "A running sum is the prefix array itself, so one pass suffices: each entry is the previous running total plus the current value. "
                     "Writing the result back into the array avoids a second buffer, and there is no reason to ever recompute a partial sum.",
        "complexity": ("O(n) time", "O(1) extra"),
        "code": {
            "cpp": r"""// One pass: each entry is the previous total plus the value
vector<int> runningSum(vector<int>& nums) {
    for (int i = 1; i < (int) nums.size(); i++)
        nums[i] += nums[i - 1];              // nums[i] now holds prefix[i]
    return nums;
}   // O(n) time · O(1) extra space""",
            "java": r"""// One pass: each entry is the previous total plus the value
int[] runningSum(int[] nums) {
    for (int i = 1; i < nums.length; i++)
        nums[i] += nums[i - 1];              // nums[i] now holds prefix[i]
    return nums;
}   // O(n) time · O(1) extra space""",
            "python": r"""def running_sum(nums):
    for i in range(1, len(nums)):
        nums[i] += nums[i - 1]          # nums[i] now holds the prefix sum
    return nums""",
        },
    },
    {
        "slug": "range-sum-query-immutable",
        "title": "Range Sum Query - Immutable",
        "difficulty": "Easy",
        "pattern": "prefix array, O(1) queries",
        "statement": "Design a structure over a fixed array that answers sumRange(left, right) — the sum of nums[left..right] — quickly.",
        "examples": [("[\"NumArray\",\"sumRange\",\"sumRange\",\"sumRange\"] [[[-2,0,3,-5,2,-1]],[0,2],[2,5],[0,5]]", "[null, 1, -1, -3]")],
        "constraints": ["1 <= nums.length <= 10^4", "-10^5 <= nums[i] <= 10^5", "0 <= left <= right < nums.length", "at most 10^4 calls to sumRange"],
        "approach": "Build the prefix array once in the constructor, offset by one so that prefix[i] is the sum of the first i values. Any range then "
                     "costs one subtraction: prefix[right + 1] - prefix[left]. Paying O(n) up front is what makes every later query constant time.",
        "complexity": ("O(n) build, O(1) per query", "O(n)"),
        "code": {
            "cpp": r"""// Prefix with a leading zero: each query is one subtraction
class NumArray {
    vector<int> prefix;
public:
    NumArray(vector<int>& nums) {
        prefix.assign(nums.size() + 1, 0);
        for (int i = 0; i < (int) nums.size(); i++)
            prefix[i + 1] = prefix[i] + nums[i];   // prefix[i] = sum of first i
    }
    int sumRange(int left, int right) {
        return prefix[right + 1] - prefix[left];   // sum(left..right)
    }
};   // O(n) build · O(1) per query · O(n) space""",
            "java": r"""// Prefix with a leading zero: each query is one subtraction
class NumArray {
    private int[] prefix;
    NumArray(int[] nums) {
        prefix = new int[nums.length + 1];
        for (int i = 0; i < nums.length; i++)
            prefix[i + 1] = prefix[i] + nums[i];   // prefix[i] = sum of first i
    }
    int sumRange(int left, int right) {
        return prefix[right + 1] - prefix[left];   // sum(left..right)
    }
}   // O(n) build · O(1) per query · O(n) space""",
            "python": r"""class NumArray:
    def __init__(self, nums):
        self.prefix = [0]
        for value in nums:
            self.prefix.append(self.prefix[-1] + value)   # prefix[i] = first i values

    def sum_range(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]""",
        },
    },
    {
        "slug": "find-pivot-index",
        "title": "Find Pivot Index",
        "difficulty": "Easy",
        "pattern": "left sum against total minus left",
        "statement": "Return the leftmost index where the sum of everything to its left equals the sum of everything to its right, or -1 if none exists.",
        "examples": [("nums = [1,7,3,6,5,6]", "3"), ("nums = [1,2,3]", "-1"), ("nums = [2,1,-1]", "0")],
        "constraints": ["1 <= nums.length <= 10^4", "-1000 <= nums[i] <= 1000"],
        "approach": "Take the total once, then sweep while keeping the sum of what you have passed. The right-hand sum is the total minus the left sum and "
                     "the current value, so a single comparison per index decides the answer — no second sweep and no prefix array needed.",
        "complexity": ("O(n) time", "O(1)"),
        "code": {
            "cpp": r"""// right = total - left - nums[i], so one sweep decides it
int pivotIndex(vector<int>& nums) {
    long long total = 0;
    for (int x : nums) total += x;
    long long left = 0;
    for (int i = 0; i < (int) nums.size(); i++) {
        if (left == total - left - nums[i]) return i;   // balanced here
        left += nums[i];                                // move the pivot right
    }
    return -1;
}   // O(n) time · O(1) space""",
            "java": r"""// right = total - left - nums[i], so one sweep decides it
int pivotIndex(int[] nums) {
    long total = 0;
    for (int x : nums) total += x;
    long left = 0;
    for (int i = 0; i < nums.length; i++) {
        if (left == total - left - nums[i]) return i;   // balanced here
        left += nums[i];                                // move the pivot right
    }
    return -1;
}   // O(n) time · O(1) space""",
            "python": r"""def pivot_index(nums):
    total = sum(nums)
    left = 0
    for i, value in enumerate(nums):
        if left == total - left - value:    # the right side is what is left over
            return i
        left += value
    return -1""",
        },
    },
    {
        "slug": "left-and-right-sum-differences",
        "title": "Left and Right Sum Differences",
        "difficulty": "Easy",
        "pattern": "two running totals",
        "statement": "For every index i return |sum(nums[0..i-1]) - sum(nums[i+1..n-1])|.",
        "examples": [("nums = [10,4,8,3]", "[15,1,11,22]"), ("nums = [1]", "[0]")],
        "constraints": ["1 <= nums.length <= 1000", "-10^5 <= nums[i] <= 10^5"],
        "approach": "Sweep once with the left sum in hand; the right sum is the total minus the left sum minus the current value. Subtracting and taking "
                     "the absolute value gives each answer in O(1), so the whole array is built in one pass over the input.",
        "complexity": ("O(n) time", "O(n)"),
        "code": {
            "cpp": r"""// Keep the left total; the right total is what remains
vector<int> leftRightDifference(vector<int>& nums) {
    long long total = 0;
    for (int x : nums) total += x;
    vector<int> answer(nums.size());
    long long left = 0;
    for (int i = 0; i < (int) nums.size(); i++) {
        long long right = total - left - nums[i];
        answer[i] = (int) llabs(left - right);
        left += nums[i];
    }
    return answer;
}   // O(n) time · O(n) space""",
            "java": r"""// Keep the left total; the right total is what remains
int[] leftRightDifference(int[] nums) {
    long total = 0;
    for (int x : nums) total += x;
    int[] answer = new int[nums.length];
    long left = 0;
    for (int i = 0; i < nums.length; i++) {
        long right = total - left - nums[i];
        answer[i] = (int) Math.abs(left - right);
        left += nums[i];
    }
    return answer;
}   // O(n) time · O(n) space""",
            "python": r"""def left_right_difference(nums):
    total = sum(nums)
    left, answer = 0, []
    for value in nums:
        right = total - left - value
        answer.append(abs(left - right))
        left += value
    return answer""",
        },
    },
    {
        "slug": "minimum-value-to-get-positive-step-by-step-sum",
        "title": "Minimum Value to Get Positive Step by Step Sum",
        "difficulty": "Easy",
        "pattern": "lowest prefix decides the start",
        "statement": "Pick a startValue so that every step-by-step sum (startValue plus the first i values) is at least 1. Return the smallest such "
                     "startValue.",
        "examples": [("nums = [-3,2,-3,4,2]", "5"), ("nums = [1,2]", "1"), ("nums = [1,-2,-3]", "5")],
        "constraints": ["1 <= nums.length <= 100", "-100 <= nums[i] <= 100"],
        "approach": "The step-by-step sums are startValue plus the prefix sums, so the tightest constraint comes from the smallest prefix. Choose "
                     "startValue = 1 - minPrefix, which is exactly positive enough at the worst moment and no larger.",
        "complexity": ("O(n) time", "O(1)"),
        "code": {
            "cpp": r"""// The worst moment is the smallest prefix sum
int minStartValue(vector<int>& nums) {
    int prefix = 0, lowest = 0;
    for (int x : nums) {
        prefix += x;
        lowest = min(lowest, prefix);        // the deepest dip
    }
    return 1 - lowest;                       // lift that dip up to 1
}   // O(n) time · O(1) space""",
            "java": r"""// The worst moment is the smallest prefix sum
int minStartValue(int[] nums) {
    int prefix = 0, lowest = 0;
    for (int x : nums) {
        prefix += x;
        lowest = Math.min(lowest, prefix);   // the deepest dip
    }
    return 1 - lowest;                       // lift that dip up to 1
}   // O(n) time · O(1) space""",
            "python": r"""def min_start_value(nums):
    prefix = lowest = 0
    for value in nums:
        prefix += value
        lowest = min(lowest, prefix)     # the deepest dip in the running sum
    return 1 - lowest                    # start high enough to survive it""",
        },
    },
    {
        "slug": "maximum-score-after-splitting-a-string",
        "title": "Maximum Score After Splitting a String",
        "difficulty": "Easy",
        "pattern": "prefix zeros + suffix ones",
        "statement": "Split the binary string s into two non-empty parts. The score is the number of zeros on the left plus the number of ones on the "
                     "right. Return the maximum score.",
        "examples": [("s = \"011101\"", "5"), ("s = \"00111\"", "5"), ("s = \"1111\"", "3")],
        "constraints": ["2 <= s.length <= 500", "s consists of '0' and '1' characters"],
        "approach": "Count the ones in the whole string first, then walk the split point: as the left part grows it gains a zero or loses a one from the "
                     "right part, so each candidate score is available in O(1) and the best one is found in a single sweep.",
        "complexity": ("O(n) time", "O(1)"),
        "code": {
            "cpp": r"""// Walk the split point: zeros left plus ones right
int maxScore(string s) {
    int ones = 0;
    for (char ch : s) ones += ch == '1';
    int zeros = 0, best = 0;
    for (int i = 0; i + 1 < (int) s.size(); i++) {
        if (s[i] == '0') zeros++;            // the left part gained a zero
        else ones--;                         // the right part lost a one
        best = max(best, zeros + ones);
    }
    return best;
}   // O(n) time · O(1) space""",
            "java": r"""// Walk the split point: zeros left plus ones right
int maxScore(String s) {
    int ones = 0;
    for (char ch : s.toCharArray()) if (ch == '1') ones++;
    int zeros = 0, best = 0;
    for (int i = 0; i + 1 < s.length(); i++) {
        if (s.charAt(i) == '0') zeros++;     // the left part gained a zero
        else ones--;                         // the right part lost a one
        best = Math.max(best, zeros + ones);
    }
    return best;
}   // O(n) time · O(1) space""",
            "python": r"""def max_score(s):
    ones = s.count("1")               # everything on the right at the start
    zeros, best = 0, 0
    for ch in s[:-1]:                 # both parts must be non-empty
        if ch == "0":
            zeros += 1                # the left part gained a zero
        else:
            ones -= 1                 # the right part lost a one
        best = max(best, zeros + ones)
    return best""",
        },
    },
    # ---------------------------------------------------------------- MEDIUM
    {
        "slug": "range-sum-query-2d-immutable",
        "title": "Range Sum Query 2D - Immutable",
        "difficulty": "Medium",
        "pattern": "2D prefix sums with inclusion-exclusion",
        "statement": "Design a structure over a fixed matrix that returns the sum of the submatrix with corners (row1, col1) and (row2, col2).",
        "examples": [("[\"NumMatrix\",\"sumRegion\",\"sumRegion\",\"sumRegion\"] [[[[3,0,1,4,2],[5,6,3,2,1],[1,2,0,1,5],[4,1,0,1,7],[1,0,3,0,5]]],[2,1,4,3],[1,1,2,2],[1,2,2,4]]", "[null, 8, 11, 12]")],
        "constraints": ["1 <= rows, cols <= 200", "-10^4 <= matrix[i][j] <= 10^4", "at most 10^4 calls to sumRegion"],
        "approach": "Extend the prefix idea to two dimensions: prefix[i][j] is the sum of the block from the origin to (i-1, j-1), built with one "
                     "recurrence. A rectangle is then the big block minus the two strips above and to the left, with the doubly-subtracted corner added "
                     "back — the inclusion-exclusion rule, four look-ups per query.",
        "complexity": ("O(rows · cols) build, O(1) per query", "O(rows · cols)"),
        "code": {
            "cpp": r"""// prefix[i][j] sums the block above and left of (i-1, j-1)
class NumMatrix {
    vector<vector<long long>> prefix;
public:
    NumMatrix(vector<vector<int>>& matrix) {
        int rows = matrix.size(), cols = matrix[0].size();
        prefix.assign(rows + 1, vector<long long>(cols + 1, 0));
        for (int i = 0; i < rows; i++)
            for (int j = 0; j < cols; j++)
                prefix[i + 1][j + 1] = prefix[i][j + 1] + prefix[i + 1][j]
                                     - prefix[i][j] + matrix[i][j];   // add the corner back
    }
    int sumRegion(int row1, int col1, int row2, int col2) {
        return (int) (prefix[row2 + 1][col2 + 1] - prefix[row1][col2 + 1]
                    - prefix[row2 + 1][col1] + prefix[row1][col1]);
    }
};   // O(rows·cols) build · O(1) per query""",
            "java": r"""// prefix[i][j] sums the block above and left of (i-1, j-1)
class NumMatrix {
    private long[][] prefix;
    NumMatrix(int[][] matrix) {
        int rows = matrix.length, cols = matrix[0].length;
        prefix = new long[rows + 1][cols + 1];
        for (int i = 0; i < rows; i++)
            for (int j = 0; j < cols; j++)
                prefix[i + 1][j + 1] = prefix[i][j + 1] + prefix[i + 1][j]
                                     - prefix[i][j] + matrix[i][j];   // add the corner back
    }
    int sumRegion(int row1, int col1, int row2, int col2) {
        return (int) (prefix[row2 + 1][col2 + 1] - prefix[row1][col2 + 1]
                    - prefix[row2 + 1][col1] + prefix[row1][col1]);
    }
}   // O(rows·cols) build · O(1) per query""",
            "python": r"""class NumMatrix:
    def __init__(self, matrix):
        rows, cols = len(matrix), len(matrix[0])
        self.prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
        for i in range(rows):
            for j in range(cols):
                self.prefix[i + 1][j + 1] = (self.prefix[i][j + 1] + self.prefix[i + 1][j]
                                             - self.prefix[i][j] + matrix[i][j])

    def sum_region(self, row1, col1, row2, col2):
        p = self.prefix                                  # inclusion-exclusion
        return p[row2 + 1][col2 + 1] - p[row1][col2 + 1] - p[row2 + 1][col1] + p[row1][col1]""",
        },
    },
    {
        "slug": "product-of-array-except-self",
        "title": "Product of Array Except Self",
        "difficulty": "Medium",
        "pattern": "prefix and suffix products in place",
        "statement": "Return an array where answer[i] is the product of every element of nums except nums[i], without using division.",
        "examples": [("nums = [1,2,3,4]", "[24,12,8,6]"), ("nums = [-1,1,0,-3,3]", "[0,0,9,0,0]")],
        "constraints": ["2 <= nums.length <= 10^5", "-30 <= nums[i] <= 30", "the product of any prefix or suffix fits in a 32-bit integer"],
        "approach": "answer[i] is the product of everything left of i times the product of everything right of i. Fill the result with prefix products "
                     "on a first pass, then walk backwards with a running suffix product multiplied in — two passes, no division and no second array.",
        "complexity": ("O(n) time", "O(1) extra"),
        "code": {
            "cpp": r"""// ans[i] = (product left of i) · (product right of i)
vector<int> productExceptSelf(vector<int>& nums) {
    int n = nums.size();
    vector<int> answer(n, 1);
    int running = 1;
    for (int i = 0; i < n; i++) {
        answer[i] = running;                 // prefix product, excluding nums[i]
        running *= nums[i];
    }
    running = 1;
    for (int i = n - 1; i >= 0; i--) {
        answer[i] *= running;                // ... times the suffix product
        running *= nums[i];
    }
    return answer;
}   // O(n) time · O(1) extra space""",
            "java": r"""// ans[i] = (product left of i) · (product right of i)
int[] productExceptSelf(int[] nums) {
    int n = nums.length;
    int[] answer = new int[n];
    Arrays.fill(answer, 1);
    int running = 1;
    for (int i = 0; i < n; i++) {
        answer[i] = running;                 // prefix product, excluding nums[i]
        running *= nums[i];
    }
    running = 1;
    for (int i = n - 1; i >= 0; i--) {
        answer[i] *= running;                // ... times the suffix product
        running *= nums[i];
    }
    return answer;
}   // O(n) time · O(1) extra space""",
            "python": r"""def product_except_self(nums):
    n = len(nums)
    answer = [1] * n
    running = 1
    for i in range(n):
        answer[i] = running            # prefix product, excluding nums[i]
        running *= nums[i]
    running = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= running           # ... times the suffix product
        running *= nums[i]
    return answer""",
        },
    },
    {
        "slug": "number-of-ways-to-split-array",
        "title": "Number of Ways to Split Array",
        "difficulty": "Medium",
        "pattern": "prefix versus the remaining total",
        "statement": "Count the indices i with 0 <= i < n - 1 where the sum of the first i + 1 elements is at least the sum of the rest.",
        "examples": [("nums = [10,4,-8,7]", "2"), ("nums = [2,3,1,0]", "2")],
        "constraints": ["2 <= nums.length <= 10^5", "-10^5 <= nums[i] <= 10^5"],
        "approach": "Total the array once, then sweep keeping a running left sum. The split at i is valid when left >= total - left, and a single "
                     "comparison per index is enough — the prefix is built as you go, so no extra array is needed.",
        "complexity": ("O(n) time", "O(1)"),
        "code": {
            "cpp": r"""// A split is valid when the left prefix reaches half the total
int waysToSplitArray(vector<int>& nums) {
    long long total = 0;
    for (int x : nums) total += x;
    long long left = 0;
    int ways = 0;
    for (int i = 0; i + 1 < (int) nums.size(); i++) {
        left += nums[i];                     // prefix ending at i
        if (left >= total - left) ways++;    // both sides non-empty
    }
    return ways;
}   // O(n) time · O(1) space""",
            "java": r"""// A split is valid when the left prefix reaches half the total
int waysToSplitArray(int[] nums) {
    long total = 0;
    for (int x : nums) total += x;
    long left = 0;
    int ways = 0;
    for (int i = 0; i + 1 < nums.length; i++) {
        left += nums[i];                     // prefix ending at i
        if (left >= total - left) ways++;    // both sides non-empty
    }
    return ways;
}   // O(n) time · O(1) space""",
            "python": r"""def ways_to_split_array(nums):
    total = sum(nums)
    left, ways = 0, 0
    for value in nums[:-1]:                  # the right part must stay non-empty
        left += value
        if left >= total - left:
            ways += 1
    return ways""",
        },
    },
    {
        "slug": "binary-subarrays-with-sum",
        "title": "Binary Subarrays With Sum",
        "difficulty": "Medium",
        "pattern": "prefix counts in a hash map",
        "statement": "Count the non-empty subarrays of the 0/1 array nums whose sum is exactly goal.",
        "examples": [("nums = [1,0,1,0,1], goal = 2", "4"), ("nums = [0,0,0,0,0], goal = 0", "15")],
        "constraints": ["1 <= nums.length <= 3 · 10^4", "nums[i] is 0 or 1", "0 <= goal <= nums.length"],
        "approach": "A subarray sums to goal exactly when two prefixes differ by goal, so count how many earlier prefixes hold each value. Walking left "
                     "to right and asking for prefix - goal counts every subarray ending here in O(1); zeros are handled naturally because repeated "
                     "prefix values accumulate in the map.",
        "complexity": ("O(n) time", "O(n)"),
        "code": {
            "cpp": r"""// Subarrays ending here = prefixes equal to prefix - goal
int numSubarraysWithSum(vector<int>& nums, int goal) {
    unordered_map<int, int> seen;             // prefix value -> how often seen
    seen[0] = 1;                              // the empty prefix
    int prefix = 0, count = 0;
    for (int x : nums) {
        prefix += x;
        count += seen[prefix - goal];          // each one ends a valid subarray
        seen[prefix]++;
    }
    return count;
}   // O(n) time · O(n) space""",
            "java": r"""// Subarrays ending here = prefixes equal to prefix - goal
int numSubarraysWithSum(int[] nums, int goal) {
    Map<Integer, Integer> seen = new HashMap<>();   // prefix value -> frequency
    seen.put(0, 1);                                 // the empty prefix
    int prefix = 0, count = 0;
    for (int x : nums) {
        prefix += x;
        count += seen.getOrDefault(prefix - goal, 0);   // ends a valid subarray
        seen.merge(prefix, 1, Integer::sum);
    }
    return count;
}   // O(n) time · O(n) space""",
            "python": r"""def num_subarrays_with_sum(nums, goal):
    seen = {0: 1}                    # prefix value -> how often it occurred
    prefix = count = 0
    for value in nums:
        prefix += value
        count += seen.get(prefix - goal, 0)   # prefix - goal ends a valid subarray
        seen[prefix] = seen.get(prefix, 0) + 1
    return count""",
        },
    },
    {
        "slug": "xor-queries-of-a-subarray",
        "title": "XOR Queries of a Subarray",
        "difficulty": "Medium",
        "pattern": "prefix XOR",
        "statement": "Answer each query [left, right] with the XOR of arr[left..right].",
        "examples": [("arr = [1,3,4,8], queries = [[0,1],[1,2],[0,3],[3,3]]", "[2,7,14,8]"),
                      ("arr = [4,8,2,10], queries = [[2,3],[1,3],[0,0],[0,3]]", "[8,0,4,4]")],
        "constraints": ["1 <= arr.length, queries.length <= 3 · 10^4", "0 <= arr[i] <= 10^9", "queries[i].length == 2", "0 <= left <= right < arr.length"],
        "approach": "XOR is its own inverse, so prefixes work exactly as they do for sums: prefix[i + 1] = prefix[i] ^ arr[i], and a range is "
                     "prefix[right + 1] ^ prefix[left]. Anything appearing in both prefixes cancels, leaving precisely the query's range.",
        "complexity": ("O(n + q) time", "O(n)"),
        "code": {
            "cpp": r"""// XOR of a range: prefixes that cancel everything outside it
vector<int> xorQueries(vector<int>& arr, vector<vector<int>>& queries) {
    vector<int> prefix(arr.size() + 1, 0);
    for (int i = 0; i < (int) arr.size(); i++)
        prefix[i + 1] = prefix[i] ^ arr[i];      // running XOR
    vector<int> answer;
    for (const vector<int>& q : queries)
        answer.push_back(prefix[q[1] + 1] ^ prefix[q[0]]);
    return answer;
}   // O(n + q) time · O(n) space""",
            "java": r"""// XOR of a range: prefixes that cancel everything outside it
int[] xorQueries(int[] arr, int[][] queries) {
    int[] prefix = new int[arr.length + 1];
    for (int i = 0; i < arr.length; i++)
        prefix[i + 1] = prefix[i] ^ arr[i];      // running XOR
    int[] answer = new int[queries.length];
    for (int i = 0; i < queries.length; i++)
        answer[i] = prefix[queries[i][1] + 1] ^ prefix[queries[i][0]];
    return answer;
}   // O(n + q) time · O(n) space""",
            "python": r"""def xor_queries(arr, queries):
    prefix = [0]
    for value in arr:
        prefix.append(prefix[-1] ^ value)        # running XOR
    return [prefix[right + 1] ^ prefix[left] for left, right in queries]""",
        },
    },
    {
        "slug": "sum-of-absolute-differences-in-a-sorted-array",
        "title": "Sum of Absolute Differences in a Sorted Array",
        "difficulty": "Medium",
        "pattern": "prefix sums split the absolute value",
        "statement": "For each index i of the sorted array nums, return the sum of |nums[i] - nums[j]| over all j.",
        "examples": [("nums = [2,3,5]", "[4,3,5]"), ("nums = [1,4,6,8,10]", "[24,15,13,15,21]")],
        "constraints": ["2 <= nums.length <= 10^5", "0 <= nums[i] <= 10^4", "nums is sorted in non-decreasing order"],
        "approach": "Sorted order removes the absolute value: everything to the left is smaller and everything to the right is larger, so the total is "
                     "(i · nums[i] - sum of the left part) + (sum of the right part - (n - 1 - i) · nums[i]). Prefix sums give both parts instantly, "
                     "turning an O(n²) sum into a single pass.",
        "complexity": ("O(n) time", "O(n)"),
        "code": {
            "cpp": r"""// Sorted: left side below, right side above — prefix sums do the rest
vector<int> getSumAbsoluteDifferences(vector<int>& nums) {
    int n = nums.size();
    vector<long long> prefix(n + 1, 0);
    for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
    vector<int> answer(n);
    for (int i = 0; i < n; i++) {
        long long left = (long long) i * nums[i] - prefix[i];                    // smaller side
        long long right = (prefix[n] - prefix[i + 1]) - (long long) (n - 1 - i) * nums[i];
        answer[i] = (int) (left + right);
    }
    return answer;
}   // O(n) time · O(n) space""",
            "java": r"""// Sorted: left side below, right side above — prefix sums do the rest
int[] getSumAbsoluteDifferences(int[] nums) {
    int n = nums.length;
    long[] prefix = new long[n + 1];
    for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
    int[] answer = new int[n];
    for (int i = 0; i < n; i++) {
        long left = (long) i * nums[i] - prefix[i];                              // smaller side
        long right = (prefix[n] - prefix[i + 1]) - (long) (n - 1 - i) * nums[i];
        answer[i] = (int) (left + right);
    }
    return answer;
}   // O(n) time · O(n) space""",
            "python": r"""def sum_absolute_differences(nums):
    n = len(nums)
    prefix = [0] * (n + 1)
    for i, value in enumerate(nums):
        prefix[i + 1] = prefix[i] + value
    answer = []
    for i, value in enumerate(nums):
        left = i * value - prefix[i]                                  # smaller side
        right = (prefix[n] - prefix[i + 1]) - (n - 1 - i) * value     # larger side
        answer.append(left + right)
    return answer""",
        },
    },
    {
        "slug": "matrix-block-sum",
        "title": "Matrix Block Sum",
        "difficulty": "Medium",
        "pattern": "2D prefix with clamped corners",
        "statement": "Return a matrix where answer[i][j] is the sum of all mat[r][c] with |r - i| <= k and |c - j| <= k.",
        "examples": [("mat = [[1,2,3],[4,5,6],[7,8,9]], k = 1", "[[12,21,16],[27,45,33],[24,39,28]]"),
                      ("mat = [[1,2,3],[4,5,6],[7,8,9]], k = 2", "[[45,45,45],[45,45,45],[45,45,45]]")],
        "constraints": ["1 <= rows, cols <= 100", "1 <= mat[i][j] <= 100", "0 <= k <= 100"],
        "approach": "The 2D prefix from the previous problem turns each block into four look-ups. The only new idea is clamping the rectangle to the "
                     "matrix borders, which is exactly why the prefix carries a leading row and column of zeros — no bounds checks are needed inside "
                     "the sum itself.",
        "complexity": ("O(rows · cols) time", "O(rows · cols)"),
        "code": {
            "cpp": r"""// Same 2D prefix; clamp each block to the matrix borders
vector<vector<int>> matrixBlockSum(vector<vector<int>>& mat, int k) {
    int rows = mat.size(), cols = mat[0].size();
    vector<vector<long long>> prefix(rows + 1, vector<long long>(cols + 1, 0));
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < cols; j++)
            prefix[i + 1][j + 1] = prefix[i][j + 1] + prefix[i + 1][j] - prefix[i][j] + mat[i][j];
    vector<vector<int>> answer(rows, vector<int>(cols));
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < cols; j++) {
            int r1 = max(0, i - k), c1 = max(0, j - k);
            int r2 = min(rows - 1, i + k), c2 = min(cols - 1, j + k);
            answer[i][j] = (int) (prefix[r2 + 1][c2 + 1] - prefix[r1][c2 + 1]
                                - prefix[r2 + 1][c1] + prefix[r1][c1]);
        }
    return answer;
}   // O(rows·cols) time · O(rows·cols) space""",
            "java": r"""// Same 2D prefix; clamp each block to the matrix borders
int[][] matrixBlockSum(int[][] mat, int k) {
    int rows = mat.length, cols = mat[0].length;
    long[][] prefix = new long[rows + 1][cols + 1];
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < cols; j++)
            prefix[i + 1][j + 1] = prefix[i][j + 1] + prefix[i + 1][j] - prefix[i][j] + mat[i][j];
    int[][] answer = new int[rows][cols];
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < cols; j++) {
            int r1 = Math.max(0, i - k), c1 = Math.max(0, j - k);
            int r2 = Math.min(rows - 1, i + k), c2 = Math.min(cols - 1, j + k);
            answer[i][j] = (int) (prefix[r2 + 1][c2 + 1] - prefix[r1][c2 + 1]
                                - prefix[r2 + 1][c1] + prefix[r1][c1]);
        }
    return answer;
}   // O(rows·cols) time · O(rows·cols) space""",
            "python": r"""def matrix_block_sum(mat, k):
    rows, cols = len(mat), len(mat[0])
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
    for i in range(rows):
        for j in range(cols):
            prefix[i + 1][j + 1] = (prefix[i][j + 1] + prefix[i + 1][j]
                                    - prefix[i][j] + mat[i][j])
    answer = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            r1, c1 = max(0, i - k), max(0, j - k)
            r2, c2 = min(rows - 1, i + k), min(cols - 1, j + k)
            answer[i][j] = (prefix[r2 + 1][c2 + 1] - prefix[r1][c2 + 1]
                            - prefix[r2 + 1][c1] + prefix[r1][c1])
    return answer""",
        },
    },
    {
        "slug": "maximum-sum-of-two-non-overlapping-subarrays",
        "title": "Maximum Sum of Two Non-Overlapping Subarrays",
        "difficulty": "Medium",
        "pattern": "sliding window + best-so-far prefix",
        "statement": "Given nums and two lengths, return the largest sum of two non-overlapping subarrays of those lengths (in either order).",
        "examples": [("nums = [0,6,5,2,2,5,1,9,4], firstLen = 1, secondLen = 2", "20"),
                      ("nums = [3,8,1,3,2,1,8,9,0], firstLen = 3, secondLen = 2", "29"),
                      ("nums = [2,1,5,6,0,9,5,0,3,8], firstLen = 4, secondLen = 3", "31")],
        "constraints": ["1 <= firstLen, secondLen <= 1000", "2 <= nums.length <= 1000", "0 <= nums[i] <= 1000"],
        "approach": "Fix the order: one window of the first length on the left, one of the second length on the right. Sweep the left window once "
                     "recording the best sum seen so far, then slide the right window and combine it with that record — each pairing is considered "
                     "exactly once. Running the same routine with the lengths swapped covers the other order.",
        "complexity": ("O(n) time", "O(n)"),
        "code": {
            "cpp": r"""// Best left window so far + each right window, then swap the lengths
int bestOrder(vector<int>& nums, int first, int second) {
    int n = nums.size();
    vector<int> best(n, 0);                  // best `first`-window ending at or before i
    int window = 0;
    for (int i = 0; i < first; i++) window += nums[i];
    best[first - 1] = window;
    for (int i = first; i < n; i++) {
        window += nums[i] - nums[i - first]; // slide by one
        best[i] = max(best[i - 1], window);
    }
    window = 0;
    for (int i = first; i < first + second; i++) window += nums[i];
    int answer = best[first - 1] + window;   // second window starts at `first`
    for (int i = first + second; i < n; i++) {
        window += nums[i] - nums[i - second]; // slide the right window
        answer = max(answer, best[i - second] + window);
    }
    return answer;
}
int maxSumTwoNoOverlap(vector<int>& nums, int firstLen, int secondLen) {
    return max(bestOrder(nums, firstLen, secondLen), bestOrder(nums, secondLen, firstLen));
}   // O(n) time · O(n) space""",
            "java": r"""// Best left window so far + each right window, then swap the lengths
int bestOrder(int[] nums, int first, int second) {
    int n = nums.length;
    int[] best = new int[n];                 // best `first`-window ending at or before i
    int window = 0;
    for (int i = 0; i < first; i++) window += nums[i];
    best[first - 1] = window;
    for (int i = first; i < n; i++) {
        window += nums[i] - nums[i - first]; // slide by one
        best[i] = Math.max(best[i - 1], window);
    }
    window = 0;
    for (int i = first; i < first + second; i++) window += nums[i];
    int answer = best[first - 1] + window;   // second window starts at `first`
    for (int i = first + second; i < n; i++) {
        window += nums[i] - nums[i - second]; // slide the right window
        answer = Math.max(answer, best[i - second] + window);
    }
    return answer;
}
int maxSumTwoNoOverlap(int[] nums, int firstLen, int secondLen) {
    return Math.max(bestOrder(nums, firstLen, secondLen), bestOrder(nums, secondLen, firstLen));
}   // O(n) time · O(n) space""",
            "python": r"""def max_sum_two_no_overlap(nums, first_len, second_len):
    def best_order(first, second):
        n = len(nums)
        best = [0] * n                       # best `first`-window ending at or before i
        window = sum(nums[:first])
        best[first - 1] = window
        for i in range(first, n):
            window += nums[i] - nums[i - first]      # slide by one
            best[i] = max(best[i - 1], window)
        window = sum(nums[first:first + second])
        answer = best[first - 1] + window
        for i in range(first + second, n):
            window += nums[i] - nums[i - second]     # slide the right window
            answer = max(answer, best[i - second] + window)
        return answer

    return max(best_order(first_len, second_len), best_order(second_len, first_len))""",
        },
    },
    {
        "slug": "range-sum-query-mutable",
        "title": "Range Sum Query - Mutable",
        "difficulty": "Medium",
        "pattern": "Fenwick tree (binary indexed tree)",
        "statement": "Design a structure over a mutable array that supports update(index, value) and sumRange(left, right).",
        "examples": [("[\"NumArray\",\"sumRange\",\"update\",\"sumRange\"] [[[1,3,5]],[0,2],[1,2],[0,2]]", "[null, 9, null, 8]")],
        "constraints": ["1 <= nums.length <= 3 · 10^4", "-100 <= nums[i] <= 100", "0 <= index < nums.length", "-100 <= value <= 100",
                        "at most 3 · 10^4 calls in total"],
        "approach": "A prefix array breaks under updates, so keep a Fenwick tree instead: entry i stores the sum of a range of length lowbit(i) ending at "
                     "i. Adding to a prefix walks upward by lowbit, reading a prefix walks downward, and both touch only O(log n) entries — so updates "
                     "and queries are both fast.",
        "complexity": ("O(log n) per update and per query", "O(n)"),
        "code": {
            "cpp": r"""// Fenwick tree: each entry owns a lowbit-sized block
class NumArray {
    vector<int> tree, values;
    int n;
    void add(int index, int delta) {
        for (int i = index + 1; i <= n; i += i & (-i)) tree[i] += delta;   // walk up
    }
    int prefixSum(int index) {                   // sum of values[0..index - 1]
        int total = 0;
        for (int i = index; i > 0; i -= i & (-i)) total += tree[i];        // walk down
        return total;
    }
public:
    NumArray(vector<int>& nums) : tree(nums.size() + 1, 0), values(nums), n(nums.size()) {
        for (int i = 0; i < n; i++) add(i, nums[i]);   // build by inserting
    }
    void update(int index, int value) {
        add(index, value - values[index]);       // store only the change
        values[index] = value;
    }
    int sumRange(int left, int right) {
        return prefixSum(right + 1) - prefixSum(left);
    }
};   // O(log n) per operation · O(n) space""",
            "java": r"""// Fenwick tree: each entry owns a lowbit-sized block
class NumArray {
    private int[] tree, values;
    private int n;
    NumArray(int[] nums) {
        n = nums.length;
        tree = new int[n + 1];
        values = nums.clone();
        for (int i = 0; i < n; i++) add(i, nums[i]);   // build by inserting
    }
    private void add(int index, int delta) {
        for (int i = index + 1; i <= n; i += i & (-i)) tree[i] += delta;   // walk up
    }
    private int prefixSum(int index) {               // sum of values[0..index - 1]
        int total = 0;
        for (int i = index; i > 0; i -= i & (-i)) total += tree[i];        // walk down
        return total;
    }
    void update(int index, int value) {
        add(index, value - values[index]);            // store only the change
        values[index] = value;
    }
    int sumRange(int left, int right) {
        return prefixSum(right + 1) - prefixSum(left);
    }
}   // O(log n) per operation · O(n) space""",
            "python": r"""class NumArray:
    def __init__(self, nums):
        self.values = list(nums)
        self.size = len(nums)
        self.tree = [0] * (self.size + 1)          # Fenwick tree
        for i, value in enumerate(nums):
            self._add(i, value)

    def _add(self, index, delta):
        i = index + 1
        while i <= self.size:
            self.tree[i] += delta                  # walk up by lowbit
            i += i & -i

    def _prefix(self, index):                      # sum of values[0..index - 1]
        total, i = 0, index
        while i > 0:
            total += self.tree[i]                  # walk down by lowbit
            i -= i & -i
        return total

    def update(self, index, value):
        self._add(index, value - self.values[index])   # store only the change
        self.values[index] = value

    def sum_range(self, left, right):
        return self._prefix(right + 1) - self._prefix(left)""",
        },
    },
    {
        "slug": "range-frequency-queries",
        "title": "Range Frequency Queries",
        "difficulty": "Medium",
        "pattern": "positions per value + binary search",
        "statement": "Design a structure that answers query(left, right, value): how many times value occurs in arr[left..right].",
        "examples": [("[\"RangeFreqQuery\",\"query\",\"query\"] [[[12,33,4,56,22,2,34,33,22,12,34,56]],[1,2,4],[0,11,33]]", "[null, 1, 2]")],
        "constraints": ["1 <= arr.length <= 10^5", "1 <= arr[i], value <= 10^4", "0 <= left <= right < arr.length", "at most 10^5 calls to query"],
        "approach": "Scanning the range per query is too slow, but the occurrences of one value are naturally sorted. Store the index list of every "
                     "value, then count how many of those indices fall inside [left, right] with two binary searches — the answer is the distance "
                     "between the two insertion points.",
        "complexity": ("O(n) build, O(log n) per query", "O(n)"),
        "code": {
            "cpp": r"""// Sorted index lists: count them between left and right
class RangeFreqQuery {
    unordered_map<int, vector<int>> positions;
public:
    RangeFreqQuery(vector<int>& arr) {
        for (int i = 0; i < (int) arr.size(); i++) positions[arr[i]].push_back(i);
    }
    int query(int left, int right, int value) {
        auto it = positions.find(value);
        if (it == positions.end()) return 0;
        const vector<int>& list = it->second;
        auto from = lower_bound(list.begin(), list.end(), left);
        auto to = upper_bound(list.begin(), list.end(), right);
        return (int) (to - from);
    }
};   // O(n) build · O(log n) per query""",
            "java": r"""// Sorted index lists: count them between left and right
class RangeFreqQuery {
    private Map<Integer, List<Integer>> positions = new HashMap<>();
    RangeFreqQuery(int[] arr) {
        for (int i = 0; i < arr.length; i++)
            positions.computeIfAbsent(arr[i], key -> new ArrayList<>()).add(i);
    }
    int query(int left, int right, int value) {
        List<Integer> list = positions.get(value);
        if (list == null) return 0;
        return upperBound(list, right) - lowerBound(list, left);
    }
    private int lowerBound(List<Integer> list, int target) {
        int low = 0, high = list.size();
        while (low < high) {
            int mid = (low + high) / 2;
            if (list.get(mid) < target) low = mid + 1;
            else high = mid;
        }
        return low;
    }
    private int upperBound(List<Integer> list, int target) {
        int low = 0, high = list.size();
        while (low < high) {
            int mid = (low + high) / 2;
            if (list.get(mid) <= target) low = mid + 1;
            else high = mid;
        }
        return low;
    }
}   // O(n) build · O(log n) per query""",
            "python": r"""class RangeFreqQuery:
    def __init__(self, arr):
        self.positions = {}
        for i, value in enumerate(arr):
            self.positions.setdefault(value, []).append(i)   # indices of each value

    def query(self, left, right, value):
        indices = self.positions.get(value, [])
        return bisect_right(indices, right) - bisect_left(indices, left)""",
        },
    },
    {
        "slug": "minimum-absolute-difference-queries",
        "title": "Minimum Absolute Difference Queries",
        "difficulty": "Medium",
        "pattern": "occurrence lists + a bounded value range",
        "statement": "For each query [left, right], return the minimum |nums[i] - nums[j]| over distinct values inside the subarray, or -1 if the subarray "
                     "holds fewer than two distinct values.",
        "examples": [("nums = [1,3,4,8], queries = [[0,1],[1,2],[2,3],[0,3]]", "[2,1,4,1]"),
                      ("nums = [4,5,2,2,7,10], queries = [[2,3],[0,2],[0,5],[3,5]]", "[-1,1,1,3]")],
        "constraints": ["1 <= nums.length, queries.length <= 10^5", "1 <= nums[i] <= 100", "0 <= left <= right < nums.length"],
        "approach": "The values live in a small fixed range, so a query only needs to know which of the 100 values appear inside it. Scanning those 100 "
                     "candidates in order and keeping the gap between consecutive present values finds the minimum in constant-ish time — a presence "
                     "test per value comes from its sorted index list.",
        "complexity": ("O(100 · log n) per query", "O(n)"),
        "code": {
            "cpp": r"""// Only 100 possible values: check which appear, then take gaps
vector<int> minDifference(vector<int>& nums, vector<vector<int>>& queries) {
    unordered_map<int, vector<int>> positions;
    for (int i = 0; i < (int) nums.size(); i++) positions[nums[i]].push_back(i);
    vector<int> answer;
    for (const vector<int>& q : queries) {
        int previous = -1, best = INT_MAX;
        for (int value = 1; value <= 100; value++) {
            auto it = positions.find(value);
            if (it == positions.end()) continue;
            const vector<int>& list = it->second;
            auto at = lower_bound(list.begin(), list.end(), q[0]);
            if (at == list.end() || *at > q[1]) continue;      // not inside the range
            if (previous != -1) best = min(best, value - previous);
            previous = value;
        }
        answer.push_back(best == INT_MAX ? -1 : best);
    }
    return answer;
}   // O(100 log n) per query · O(n) space""",
            "java": r"""// Only 100 possible values: check which appear, then take gaps
int[] minDifference(int[] nums, int[][] queries) {
    Map<Integer, List<Integer>> positions = new HashMap<>();
    for (int i = 0; i < nums.length; i++)
        positions.computeIfAbsent(nums[i], key -> new ArrayList<>()).add(i);
    int[] answer = new int[queries.length];
    for (int q = 0; q < queries.length; q++) {
        int left = queries[q][0], right = queries[q][1], previous = -1, best = Integer.MAX_VALUE;
        for (int value = 1; value <= 100; value++) {
            List<Integer> list = positions.get(value);
            if (list == null) continue;
            int at = lowerBound(list, left);
            if (at == list.size() || list.get(at) > right) continue;   // not inside
            if (previous != -1) best = Math.min(best, value - previous);
            previous = value;
        }
        answer[q] = best == Integer.MAX_VALUE ? -1 : best;
    }
    return answer;
}
int lowerBound(List<Integer> list, int target) {
    int low = 0, high = list.size();
    while (low < high) {
        int mid = (low + high) / 2;
        if (list.get(mid) < target) low = mid + 1;
        else high = mid;
    }
    return low;
}   // O(100 log n) per query · O(n) space""",
            "python": r"""def min_difference_queries(nums, queries):
    positions = {}
    for i, value in enumerate(nums):
        positions.setdefault(value, []).append(i)
    answer = []
    for left, right in queries:
        previous, best = -1, None
        for value in sorted(positions):          # values in increasing order
            indices = positions[value]
            at = bisect_left(indices, left)
            if at == len(indices) or indices[at] > right:
                continue                         # this value is not in the range
            if previous != -1:
                gap = value - previous
                best = gap if best is None else min(best, gap)
            previous = value
        answer.append(-1 if best is None else best)
    return answer""",
        },
    },
    {
        "slug": "range-sum-of-sorted-subarray-sums",
        "title": "Range Sum of Sorted Subarray Sums",
        "difficulty": "Medium",
        "pattern": "prefix sums for every subarray, then sort",
        "statement": "Take every non-empty subarray sum of nums, sort them, and return the sum of the entries from position left to position right "
                     "(1-indexed) modulo 10^9 + 7.",
        "examples": [("nums = [1,2,3,4], n = 4, left = 1, right = 5", "13"), ("nums = [1,2,3,4], n = 4, left = 3, right = 4", "6"),
                      ("nums = [1,2,3,4], n = 4, left = 1, right = 10", "50")],
        "constraints": ["1 <= nums.length <= 1000", "1 <= nums[i] <= 100", "1 <= left <= right <= n · (n + 1) / 2"],
        "approach": "With a small array, the direct reading of the statement is fast enough: build every subarray sum by extending a running total from "
                     "each starting point, sort the n(n+1)/2 values, and add the requested slice. Prefix-style running totals are what make the "
                     "collection step quadratic rather than cubic.",
        "complexity": ("O(n² log n) time", "O(n²)"),
        "code": {
            "cpp": r"""// Collect every subarray sum with running totals, sort, slice
int rangeSum(vector<int>& nums, int n, int left, int right) {
    const long long MOD = 1000000007;
    vector<long long> sums;
    for (int i = 0; i < n; i++) {
        long long running = 0;
        for (int j = i; j < n; j++) {
            running += nums[j];               // sum of nums[i..j]
            sums.push_back(running);
        }
    }
    sort(sums.begin(), sums.end());
    long long total = 0;
    for (int i = left - 1; i <= right - 1; i++) total = (total + sums[i]) % MOD;
    return (int) total;
}   // O(n^2 log n) time · O(n^2) space""",
            "java": r"""// Collect every subarray sum with running totals, sort, slice
int rangeSum(int[] nums, int n, int left, int right) {
    final long MOD = 1000000007L;
    long[] sums = new long[n * (n + 1) / 2];
    int at = 0;
    for (int i = 0; i < n; i++) {
        long running = 0;
        for (int j = i; j < n; j++) {
            running += nums[j];               // sum of nums[i..j]
            sums[at++] = running;
        }
    }
    Arrays.sort(sums);
    long total = 0;
    for (int i = left - 1; i <= right - 1; i++) total = (total + sums[i]) % MOD;
    return (int) total;
}   // O(n^2 log n) time · O(n^2) space""",
            "python": r"""def range_sum_sorted_subarray_sums(nums, n, left, right):
    sums = []
    for start in range(n):
        running = 0
        for end in range(start, n):
            running += nums[end]             # sum of nums[start..end]
            sums.append(running)
    sums.sort()
    return sum(sums[left - 1:right]) % (10**9 + 7)""",
        },
    },
    {
        "slug": "minimum-number-of-increments-on-subarrays-to-form-a-target-array",
        "title": "Minimum Number of Increments on Subarrays to Form a Target Array",
        "difficulty": "Hard",
        "pattern": "difference array: charge every rise",
        "statement": "Starting from all zeros, each operation adds 1 to every element of a contiguous subarray. Return the minimum number of operations "
                     "that build target.",
        "examples": [("target = [1,2,3,2,1]", "3"), ("target = [3,1,1,2]", "4"), ("target = [3,1,5,4,2]", "7")],
        "constraints": ["1 <= target.length <= 10^5", "1 <= target[i] <= 10^5"],
        "approach": "Read the array as differences: every increase from target[i-1] to target[i] costs exactly that many new increments, because the "
                     "extra height cannot be produced by any operation that already covers the left part. Drops are free — those layers were paid for "
                     "earlier — so the answer is the sum of the positive rises, with the first element compared against zero.",
        "complexity": ("O(n) time", "O(1)"),
        "code": {
            "cpp": r"""// Sum of the positive rises: a drop is already paid for
int minNumberOperations(vector<int>& target) {
    long long operations = 0;
    int previous = 0;
    for (int value : target) {
        if (value > previous) operations += value - previous;   // new layers needed
        previous = value;
    }
    return (int) operations;
}   // O(n) time · O(1) space""",
            "java": r"""// Sum of the positive rises: a drop is already paid for
int minNumberOperations(int[] target) {
    long operations = 0;
    int previous = 0;
    for (int value : target) {
        if (value > previous) operations += value - previous;   // new layers needed
        previous = value;
    }
    return (int) operations;
}   // O(n) time · O(1) space""",
            "python": r"""def min_number_operations(target):
    operations, previous = 0, 0
    for value in target:
        if value > previous:
            operations += value - previous   # each rise costs new layers
        previous = value                     # drops are already paid for
    return operations""",
        },
    },
    {
        "slug": "smallest-rotation-with-highest-score",
        "title": "Smallest Rotation with Highest Score",
        "difficulty": "Hard",
        "pattern": "difference array over rotations",
        "statement": "Rotating nums by k moves each element k places left; a rotation scores one point per index i with nums[i] <= i afterwards. Return the "
                     "smallest k with the highest score.",
        "examples": [("nums = [2,3,1,4,0]", "3"), ("nums = [1,3,0,2,4]", "0")],
        "constraints": ["1 <= nums.length <= 10^5", "0 <= nums[i] < nums.length"],
        "approach": "Instead of scoring every rotation, work out for each element which rotations make it score — a contiguous block of k values on a "
                     "circle — and mark those blocks with a difference array. Prefix-summing that array gives all n scores in one pass, and the first "
                     "maximum is the answer.",
        "complexity": ("O(n) time", "O(n)"),
        "code": {
            "cpp": r"""// Each element fails to score on one circular block of rotations
int bestRotation(vector<int>& nums) {
    int n = nums.size();
    vector<int> penalty(n + 1, 0);
    for (int i = 0; i < n; i++) {
        int length = min(nums[i], n);                // rotations where i < nums[i]
        if (length == 0) continue;
        int start = (i - length + 1 + n) % n;        // first bad rotation
        if (start <= i) {                            // one straight block
            penalty[start]++;
            penalty[i + 1]--;
        } else {                                     // wraps past the end
            penalty[start]++;
            penalty[n]--;
            penalty[0]++;
            penalty[i + 1]--;
        }
    }
    int best = -1, score = 0, answer = 0;
    for (int k = 0; k < n; k++) {
        score += penalty[k];
        if (n - score > best) { best = n - score; answer = k; }   // first maximum wins
    }
    return answer;
}   // O(n) time · O(n) space""",
            "java": r"""// Each element fails to score on one circular block of rotations
int bestRotation(int[] nums) {
    int n = nums.length;
    int[] penalty = new int[n + 1];
    for (int i = 0; i < n; i++) {
        int length = Math.min(nums[i], n);            // rotations where i < nums[i]
        if (length == 0) continue;
        int start = (i - length + 1 + n) % n;         // first bad rotation
        if (start <= i) {                             // one straight block
            penalty[start]++;
            penalty[i + 1]--;
        } else {                                      // wraps past the end
            penalty[start]++;
            penalty[n]--;
            penalty[0]++;
            penalty[i + 1]--;
        }
    }
    int best = -1, score = 0, answer = 0;
    for (int k = 0; k < n; k++) {
        score += penalty[k];
        if (n - score > best) { best = n - score; answer = k; }   // first maximum wins
    }
    return answer;
}   // O(n) time · O(n) space""",
            "python": r"""def best_rotation(nums):
    n = len(nums)
    penalty = [0] * (n + 1)              # penalty[k] = how many indices lose their point
    for i, value in enumerate(nums):
        length = min(value, n)           # rotations where this index fails
        if length == 0:
            continue
        start = (i - length + 1 + n) % n
        if start <= i:                   # one straight block
            penalty[start] += 1
            penalty[i + 1] -= 1
        else:                            # the block wraps past the end
            penalty[start] += 1
            penalty[n] -= 1
            penalty[0] += 1
            penalty[i + 1] -= 1
    best, score, answer = -1, 0, 0
    for k in range(n):
        score += penalty[k]
        if n - score > best:             # take the first maximum
            best, answer = n - score, k
    return answer""",
        },
    },
    {
        "slug": "maximum-sum-of-3-non-overlapping-subarrays",
        "title": "Maximum Sum of 3 Non-Overlapping Subarrays",
        "difficulty": "Hard",
        "pattern": "window sums + best prefix and suffix",
        "statement": "Choose three non-overlapping subarrays of length k with the largest total sum. Return their starting indices, taking the "
                     "lexicographically smallest answer on a tie.",
        "examples": [("nums = [1,2,1,2,6,7,5,1], k = 2", "[0,3,5]"), ("nums = [1,2,1,2,1,2,1,2,1], k = 2", "[0,2,4]")],
        "constraints": ["1 <= nums.length <= 2 · 10^4", "1 <= nums[i] < 10^5", "1 <= k <= nums.length / 3"],
        "approach": "Compute every k-length window sum once. Then for the middle window, the best left window is the best one that ends before it and the "
                     "best right window starts after it — precompute those two arrays, keeping the earliest index on ties so the answer stays "
                     "lexicographically smallest.",
        "complexity": ("O(n) time", "O(n)"),
        "code": {
            "cpp": r"""// For each middle window: best window on its left plus best on its right
vector<int> maxSumOfThreeSubarrays(vector<int>& nums, int k) {
    int n = nums.size(), m = n - k + 1;
    vector<long long> window(m, 0);
    long long running = 0;
    for (int i = 0; i < n; i++) {
        running += nums[i];
        if (i >= k) running -= nums[i - k];
        if (i >= k - 1) window[i - k + 1] = running;
    }
    vector<int> bestLeft(m), bestRight(m);
    bestLeft[0] = 0;
    for (int i = 1; i < m; i++)                       // earliest index wins ties
        bestLeft[i] = window[i] > window[bestLeft[i - 1]] ? i : bestLeft[i - 1];
    bestRight[m - 1] = m - 1;
    for (int i = m - 2; i >= 0; i--)
        bestRight[i] = window[i] >= window[bestRight[i + 1]] ? i : bestRight[i + 1];
    long long best = LLONG_MIN;               // handles negative windows too
    vector<int> answer(3, 0);
    for (int mid = k; mid + 2 * k <= n; mid++) {
        int left = bestLeft[mid - k], right = bestRight[mid + k];
        long long total = window[left] + window[mid] + window[right];
        if (total > best) { best = total; answer = {left, mid, right}; }
        else if (total == best && vector<int>{left, mid, right} < answer)
            answer = {left, mid, right};              // lexicographically smaller
    }
    return answer;
}   // O(n) time · O(n) space""",
            "java": r"""// For each middle window: best window on its left plus best on its right
int[] maxSumOfThreeSubarrays(int[] nums, int k) {
    int n = nums.length, m = n - k + 1;
    long[] window = new long[m];
    long running = 0;
    for (int i = 0; i < n; i++) {
        running += nums[i];
        if (i >= k) running -= nums[i - k];
        if (i >= k - 1) window[i - k + 1] = running;
    }
    int[] bestLeft = new int[m], bestRight = new int[m];
    bestLeft[0] = 0;
    for (int i = 1; i < m; i++)                       // earliest index wins ties
        bestLeft[i] = window[i] > window[bestLeft[i - 1]] ? i : bestLeft[i - 1];
    bestRight[m - 1] = m - 1;
    for (int i = m - 2; i >= 0; i--)
        bestRight[i] = window[i] >= window[bestRight[i + 1]] ? i : bestRight[i + 1];
    long best = Long.MIN_VALUE;               // handles negative windows too
    int[] answer = new int[3];
    for (int mid = k; mid + 2 * k <= n; mid++) {
        int left = bestLeft[mid - k], right = bestRight[mid + k];
        long total = window[left] + window[mid] + window[right];
        if (total > best) { best = total; answer = new int[]{left, mid, right}; }
        else if (total == best && lexLess(new int[]{left, mid, right}, answer))
            answer = new int[]{left, mid, right};     // lexicographically smaller
    }
    return answer;
}
boolean lexLess(int[] a, int[] b) {
    for (int i = 0; i < a.length; i++) {
        if (a[i] != b[i]) return a[i] < b[i];
    }
    return false;
}   // O(n) time · O(n) space""",
            "python": r"""def max_sum_of_three_subarrays(nums, k):
    n = len(nums)
    m = n - k + 1
    window = [0] * m
    running = 0
    for i, value in enumerate(nums):
        running += value
        if i >= k:
            running -= nums[i - k]
        if i >= k - 1:
            window[i - k + 1] = running           # sum of nums[start..start+k-1]
    best_left = [0] * m
    for i in range(1, m):                         # best window ending at or before i
        best_left[i] = i if window[i] > window[best_left[i - 1]] else best_left[i - 1]
    best_right = [0] * m
    best_right[m - 1] = m - 1
    for i in range(m - 2, -1, -1):                # best window starting at or after i
        best_right[i] = i if window[i] >= window[best_right[i + 1]] else best_right[i + 1]
    best, answer = None, None
    for mid in range(k, n - 2 * k + 1):
        left, right = best_left[mid - k], best_right[mid + k]
        total = window[left] + window[mid] + window[right]
        candidate = [left, mid, right]
        if best is None or total > best or (total == best and candidate < answer):
            best, answer = total, candidate       # ties go to the smaller indices
    return answer""",
        },
    },
    {
        "slug": "count-of-range-sum",
        "title": "Count of Range Sum",
        "difficulty": "Hard",
        "pattern": "prefix pairs counted with a Fenwick tree",
        "statement": "Count the subarrays whose sum lies in [lower, upper].",
        "examples": [("nums = [-2,5,-1], lower = -2, upper = 2", "3"), ("nums = [0], lower = 0, upper = 0", "1")],
        "constraints": ["1 <= nums.length <= 10^5", "-2^31 <= nums[i] <= 2^31 - 1", "-10^5 <= lower <= upper <= 10^5"],
        "approach": "A subarray sum is a difference of two prefixes, so the question becomes: how many earlier prefixes p satisfy prefix[j] - upper <= p <= prefix[j] - lower? Sorting the prefixes and storing them in a "
                     "Fenwick tree over their compressed ranks answers each of those range counts in logarithmic time.",
        "complexity": ("O(n log n) time", "O(n)"),
        "code": {
            "cpp": r"""// Count earlier prefixes inside a moving range of values
int countRangeSum(vector<int>& nums, int lower, int upper) {
    int n = nums.size();
    vector<long long> prefix(n + 1, 0);
    for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
    vector<long long> sorted = prefix;
    sort(sorted.begin(), sorted.end());
    sorted.erase(unique(sorted.begin(), sorted.end()), sorted.end());
    int m = sorted.size();
    vector<int> tree(m + 1, 0);
    auto add = [&](int pos) { for (int i = pos; i <= m; i += i & (-i)) tree[i]++; };
    auto countUpTo = [&](int pos) {
        int total = 0;
        for (int i = pos; i > 0; i -= i & (-i)) total += tree[i];
        return total;
    };
    auto rank = [&](long long value) {
        return (int) (lower_bound(sorted.begin(), sorted.end(), value) - sorted.begin()) + 1;
    };
    long long answer = 0;
    for (int j = 0; j <= n; j++) {
        if (j > 0) {
            int low = rank(prefix[j] - upper);        // smallest value allowed
            int high = (int) (upper_bound(sorted.begin(), sorted.end(), prefix[j] - lower) - sorted.begin());
            if (high >= low) answer += countUpTo(high) - countUpTo(low - 1);
        }
        add(rank(prefix[j]));
    }
    return (int) answer;
}   // O(n log n) time · O(n) space""",
            "java": r"""// Count earlier prefixes inside a moving range of values
int countRangeSum(int[] nums, int lower, int upper) {
    int n = nums.length;
    long[] prefix = new long[n + 1];
    for (int i = 0; i < n; i++) prefix[i + 1] = prefix[i] + nums[i];
    long[] sorted = prefix.clone();
    Arrays.sort(sorted);
    int m = 1;
    for (int i = 1; i < sorted.length; i++)          // drop duplicates
        if (sorted[i] != sorted[m - 1]) sorted[m++] = sorted[i];
    int[] tree = new int[m + 1];
    long answer = 0;
    for (int j = 0; j <= n; j++) {
        if (j > 0) {
            int low = lowerBound(sorted, m, prefix[j] - upper);
            int high = upperBound(sorted, m, prefix[j] - lower);
            // count the inserted ranks in [low, high - 1]; prefixCount(x) counts ranks < x
            if (high > low) answer += prefixCount(tree, high) - prefixCount(tree, low);
        }
        add(tree, m, lowerBound(sorted, m, prefix[j]));
    }
    return (int) answer;
}
int lowerBound(long[] values, int size, long target) {
    int low = 0, high = size;
    while (low < high) {
        int mid = (low + high) / 2;
        if (values[mid] < target) low = mid + 1;
        else high = mid;
    }
    return low;                                      // 0-based insertion point
}
int upperBound(long[] values, int size, long target) {
    int low = 0, high = size;
    while (low < high) {
        int mid = (low + high) / 2;
        if (values[mid] <= target) low = mid + 1;
        else high = mid;
    }
    return low;
}
void add(int[] tree, int size, int zeroBased) {
    for (int i = zeroBased + 1; i <= size; i += i & (-i)) tree[i]++;
}
int prefixCount(int[] tree, int oneBased) {
    int total = 0;
    for (int i = oneBased; i > 0; i -= i & (-i)) total += tree[i];
    return total;
}   // O(n log n) time · O(n) space""",
            "python": r"""def count_range_sum(nums, lower, upper):
    prefix = [0]
    for value in nums:
        prefix.append(prefix[-1] + value)
    ordered = sorted(set(prefix))
    size = len(ordered)
    tree = [0] * (size + 1)

    def add(zero_based):                          # Fenwick: mark this prefix as seen
        i = zero_based + 1
        while i <= size:
            tree[i] += 1
            i += i & -i

    def count_up_to(one_based):                   # how many seen prefixes are ≤ index
        total, i = 0, one_based
        while i > 0:
            total += tree[i]
            i -= i & -i
        return total

    answer = 0
    for j, current in enumerate(prefix):
        if j > 0:
            low = bisect_left(ordered, current - upper)        # first allowed value
            high = bisect_right(ordered, current - lower)      # one past the last
            if high > low:
                answer += count_up_to(high) - count_up_to(low)
        add(bisect_left(ordered, current))
    return answer""",
        },
    },
    {
        "slug": "maximum-sum-queries",
        "title": "Maximum Sum Queries",
        "difficulty": "Hard",
        "pattern": "offline sort + Fenwick maximum",
        "statement": "For each query [x, y], return the largest nums1[j] + nums2[j] over indices with nums1[j] >= x and nums2[j] >= y, or -1 if there is "
                     "none.",
        "examples": [("nums1 = [4,3,1,2], nums2 = [2,4,9,5], queries = [[4,1],[1,3],[2,5]]", "[6,10,7]"),
                      ("nums1 = [3,2,5], nums2 = [2,3,4], queries = [[4,4],[3,2],[1,1]]", "[9,9,9]")],
        "constraints": ["1 <= nums1.length, nums2.length, queries.length <= 10^5", "1 <= nums1[i], nums2[i] <= 10^9",
                        "queries[i] = [xi, yi] with 1 <= xi, yi <= 10^9"],
        "approach": "Sort the queries by x and the indices by nums1 descending, so that answering a query only means inserting a few more indices. What "
                     "is left is \"the largest value among inserted indices with nums2 >= y\", which a Fenwick tree answers as a prefix maximum once "
                     "nums2 values are compressed and the order is reversed.",
        "complexity": ("O((n + q) log n) time", "O(n)"),
        "code": {
            "cpp": r"""// Queries sorted by x; Fenwick maximum over compressed nums2
vector<int> maximumSumQueries(vector<int>& nums1, vector<int>& nums2, vector<vector<int>>& queries) {
    int n = nums1.size();
    vector<int> order(n), values = nums2, qorder(queries.size());
    iota(order.begin(), order.end(), 0);
    iota(qorder.begin(), qorder.end(), 0);
    sort(order.begin(), order.end(), [&](int a, int b) { return nums1[a] > nums1[b]; });
    sort(qorder.begin(), qorder.end(), [&](int a, int b) { return queries[a][0] > queries[b][0]; });
    sort(values.begin(), values.end());
    values.erase(unique(values.begin(), values.end()), values.end());
    int m = values.size();
    vector<int> tree(m + 1, -1);
    auto update = [&](int pos, int value) {
        for (int i = pos; i <= m; i += i & (-i)) tree[i] = max(tree[i], value);
    };
    auto best = [&](int pos) {                       // maximum over the first pos slots
        int result = -1;
        for (int i = pos; i > 0; i -= i & (-i)) result = max(result, tree[i]);
        return result;
    };
    vector<int> answer(queries.size(), -1);
    int next = 0;
    for (int qi : qorder) {
        int x = queries[qi][0], y = queries[qi][1];
        while (next < n && nums1[order[next]] >= x) {          // this index now qualifies
            int j = order[next++];
            int rank = lower_bound(values.begin(), values.end(), nums2[j]) - values.begin();
            update(m - rank, nums1[j] + nums2[j]);             // reversed order
        }
        int first = lower_bound(values.begin(), values.end(), y) - values.begin();
        answer[qi] = best(m - first);                          // nums2 ≥ y becomes a prefix
    }
    return answer;
}   // O((n + q) log n) time · O(n) space""",
            "java": r"""// Queries sorted by x; Fenwick maximum over compressed nums2
int[] maximumSumQueries(int[] nums1, int[] nums2, int[][] queries) {
    int n = nums1.length;
    Integer[] order = new Integer[n], qorder = new Integer[queries.length];
    for (int i = 0; i < n; i++) order[i] = i;
    for (int i = 0; i < queries.length; i++) qorder[i] = i;
    Arrays.sort(order, (a, b) -> Integer.compare(nums1[b], nums1[a]));
    Arrays.sort(qorder, (a, b) -> Integer.compare(queries[b][0], queries[a][0]));
    int[] values = nums2.clone();
    Arrays.sort(values);
    int m = 1;
    for (int i = 1; i < values.length; i++)
        if (values[i] != values[m - 1]) values[m++] = values[i];
    int[] tree = new int[m + 1];
    Arrays.fill(tree, -1);
    int[] answer = new int[queries.length];
    Arrays.fill(answer, -1);
    int next = 0;
    for (int qi : qorder) {
        int x = queries[qi][0], y = queries[qi][1];
        while (next < n && nums1[order[next]] >= x) {          // this index now qualifies
            int j = order[next++];
            int rank = lowerBound(values, m, nums2[j]);
            int value = nums1[j] + nums2[j];
            for (int i = m - rank; i <= m; i += i & (-i))      // reversed order
                tree[i] = Math.max(tree[i], value);
        }
        int first = lowerBound(values, m, y);
        int best = -1;
        for (int i = m - first; i > 0; i -= i & (-i)) best = Math.max(best, tree[i]);
        answer[qi] = best;
    }
    return answer;
}
int lowerBound(int[] values, int size, int target) {
    int low = 0, high = size;
    while (low < high) {
        int mid = (low + high) / 2;
        if (values[mid] < target) low = mid + 1;
        else high = mid;
    }
    return low;
}   // O((n + q) log n) time · O(n) space""",
            "python": r"""def maximum_sum_queries(nums1, nums2, queries):
    n = len(nums1)
    order = sorted(range(n), key=lambda i: -nums1[i])
    qorder = sorted(range(len(queries)), key=lambda i: -queries[i][0])
    values = sorted(set(nums2))
    m = len(values)
    tree = [-1] * (m + 1)

    def update(pos, value):                    # Fenwick maximum, 1-based
        while pos <= m:
            tree[pos] = max(tree[pos], value)
            pos += pos & -pos

    def best(pos):                             # maximum over the first pos slots
        result = -1
        while pos > 0:
            result = max(result, tree[pos])
            pos -= pos & -pos
        return result

    answer = [-1] * len(queries)
    nxt = 0
    for qi in qorder:
        x, y = queries[qi]
        while nxt < n and nums1[order[nxt]] >= x:      # index now qualifies on nums1
            j = order[nxt]
            nxt += 1
            rank = bisect_left(values, nums2[j])
            update(m - rank, nums1[j] + nums2[j])      # reversed order
        first = bisect_left(values, y)
        answer[qi] = best(m - first)                   # nums2 ≥ y is now a prefix
    return answer""",
        },
    },
    {
        "slug": "count-of-smaller-numbers-after-self",
        "title": "Count of Smaller Numbers After Self",
        "difficulty": "Hard",
        "pattern": "Fenwick counts from the right",
        "statement": "Return an array counts where counts[i] is the number of indices j > i with nums[j] < nums[i].",
        "examples": [("nums = [5,2,6,1]", "[2,1,1,0]"), ("nums = [-1]", "[0]"), ("nums = [-1,-1]", "[0,0]")],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "approach": "Sweep from the right and keep the values already seen in a Fenwick tree indexed by compressed rank. The answer for the current "
                     "element is the count of stored values with a smaller rank, which is one prefix query — the array is then built back to front in "
                     "logarithmic time per element.",
        "complexity": ("O(n log n) time", "O(n)"),
        "code": {
            "cpp": r"""// Sweep right to left, counting what is already stored
vector<int> countSmaller(vector<int>& nums) {
    vector<int> values = nums, answer(nums.size(), 0);
    sort(values.begin(), values.end());
    values.erase(unique(values.begin(), values.end()), values.end());
    int m = values.size();
    vector<int> tree(m + 1, 0);
    auto add = [&](int pos) { for (int i = pos; i <= m; i += i & (-i)) tree[i]++; };
    auto countUpTo = [&](int pos) {
        int total = 0;
        for (int i = pos; i > 0; i -= i & (-i)) total += tree[i];
        return total;
    };
    for (int i = nums.size() - 1; i >= 0; i--) {
        int rank = lower_bound(values.begin(), values.end(), nums[i]) - values.begin() + 1;
        answer[i] = countUpTo(rank - 1);         // strictly smaller, already seen
        add(rank);
    }
    return answer;
}   // O(n log n) time · O(n) space""",
            "java": r"""// Sweep right to left, counting what is already stored
List<Integer> countSmaller(int[] nums) {
    int[] values = nums.clone();
    Arrays.sort(values);
    int m = 1;
    for (int i = 1; i < values.length; i++)
        if (values[i] != values[m - 1]) values[m++] = values[i];
    int[] tree = new int[m + 1], answer = new int[nums.length];
    for (int i = nums.length - 1; i >= 0; i--) {
        int rank = lowerBound(values, m, nums[i]) + 1;
        for (int p = rank - 1; p > 0; p -= p & (-p)) answer[i] += tree[p];   // smaller, seen
        for (int p = rank; p <= m; p += p & (-p)) tree[p]++;
    }
    List<Integer> result = new ArrayList<>();
    for (int value : answer) result.add(value);
    return result;
}
int lowerBound(int[] values, int size, int target) {
    int low = 0, high = size;
    while (low < high) {
        int mid = (low + high) / 2;
        if (values[mid] < target) low = mid + 1;
        else high = mid;
    }
    return low;
}   // O(n log n) time · O(n) space""",
            "python": r"""def count_smaller(nums):
    values = sorted(set(nums))
    size = len(values)
    tree = [0] * (size + 1)
    answer = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):
        rank = bisect_left(values, nums[i]) + 1     # 1-based rank
        pos = rank - 1
        while pos > 0:                              # count strictly smaller, seen
            answer[i] += tree[pos]
            pos -= pos & -pos
        pos = rank
        while pos <= size:                          # remember this value
            tree[pos] += 1
            pos += pos & -pos
    return answer""",
        },
    },
    {
        "slug": "create-sorted-array-through-instructions",
        "title": "Create Sorted Array through Instructions",
        "difficulty": "Hard",
        "pattern": "Fenwick over values while inserting",
        "statement": "Insert the values of instructions one by one into a sorted array. Each insertion costs the smaller of (strictly smaller values "
                     "already present) and (strictly larger values already present). Return the total cost modulo 10^9 + 7.",
        "examples": [("instructions = [1,5,6,2]", "1"), ("instructions = [1,2,3,6,5,4]", "3")],
        "constraints": ["1 <= instructions.length <= 10^5", "1 <= instructions[i] <= 10^5"],
        "approach": "Both costs are counts over values already inserted, and the value range is small and known. A Fenwick tree indexed by value gives "
                     "the number of smaller and of equal values in two prefix queries, so the larger count follows by subtraction and every insertion is "
                     "handled in logarithmic time.",
        "complexity": ("O(n log V) time", "O(V)"),
        "code": {
            "cpp": r"""// Counts of smaller and larger values already inserted
int createSortedArray(vector<int>& instructions) {
    const long long MOD = 1000000007;
    int top = *max_element(instructions.begin(), instructions.end());
    vector<long long> tree(top + 1, 0);
    auto add = [&](int pos) { for (int i = pos; i <= top; i += i & (-i)) tree[i]++; };
    auto countUpTo = [&](int pos) {
        long long total = 0;
        for (int i = pos; i > 0; i -= i & (-i)) total += tree[i];
        return total;
    };
    long long cost = 0, inserted = 0;
    for (int value : instructions) {
        long long smaller = countUpTo(value - 1);
        long long notLarger = countUpTo(value);           // smaller plus equal
        long long larger = inserted - notLarger;
        cost = (cost + min(smaller, larger)) % MOD;       // cheaper side wins
        add(value);
        inserted++;
    }
    return (int) cost;
}   // O(n log V) time · O(V) space""",
            "java": r"""// Counts of smaller and larger values already inserted
int createSortedArray(int[] instructions) {
    final long MOD = 1000000007L;
    int top = 0;
    for (int value : instructions) top = Math.max(top, value);
    int[] tree = new int[top + 1];
    long cost = 0;
    for (int index = 0; index < instructions.length; index++) {
        int value = instructions[index];
        long smaller = 0;
        for (int p = value - 1; p > 0; p -= p & (-p)) smaller += tree[p];
        long notLarger = 0;
        for (int p = value; p > 0; p -= p & (-p)) notLarger += tree[p];
        long larger = index - notLarger;                  // inserted count is `index`
        cost = (cost + Math.min(smaller, larger)) % MOD;   // cheaper side wins
        for (int p = value; p <= top; p += p & (-p)) tree[p]++;
    }
    return (int) cost;
}   // O(n log V) time · O(V) space""",
            "python": r"""def create_sorted_array(instructions):
    mod = 10**9 + 7
    top = max(instructions)
    tree = [0] * (top + 1)

    def add(pos):
        while pos <= top:
            tree[pos] += 1
            pos += pos & -pos

    def count_up_to(pos):
        total = 0
        while pos > 0:
            total += tree[pos]
            pos -= pos & -pos
        return total

    cost = 0
    for inserted, value in enumerate(instructions):
        smaller = count_up_to(value - 1)
        not_larger = count_up_to(value)          # smaller plus equal
        larger = inserted - not_larger
        cost = (cost + min(smaller, larger)) % mod   # the cheaper side decides
        add(value)
    return cost""",
        },
    },
    {
        "slug": "count-good-triplets-in-an-array",
        "title": "Count Good Triplets in an Array",
        "difficulty": "Hard",
        "pattern": "prefix counts of relative positions",
        "statement": "nums1 and nums2 are permutations. A triplet (x, y, z) is good when their positions increase in both arrays. Count the good "
                     "triplets.",
        "examples": [("nums1 = [2,0,1,3], nums2 = [0,1,2,3]", "1"), ("nums1 = [4,0,1,3,2], nums2 = [4,1,0,2,3]", "4")],
        "constraints": ["1 <= nums1.length == nums2.length <= 10^5", "nums1 and nums2 are permutations of 0..n-1"],
        "approach": "Fix the middle value y and count the choices on each side. Sweep nums1 in order keeping a Fenwick tree of the positions that value "
                     "has in nums2: the number of already-seen values with a smaller position gives one factor, and a subtraction gives the other — so "
                     "every triplet is counted exactly once, by its middle element.",
        "complexity": ("O(n log n) time", "O(n)"),
        "code": {
            "cpp": r"""// Fix the middle value; count smaller positions before and larger after
long long goodTriplets(vector<int>& nums1, vector<int>& nums2) {
    int n = nums1.size();
    vector<int> positionIn2(n, 0);
    for (int i = 0; i < n; i++) positionIn2[nums2[i]] = i;
    vector<int> tree(n + 1, 0);
    auto add = [&](int pos) { for (int i = pos; i <= n; i += i & (-i)) tree[i]++; };
    auto countUpTo = [&](int pos) {
        long long total = 0;
        for (int i = pos; i > 0; i -= i & (-i)) total += tree[i];
        return total;
    };
    long long total = 0;
    for (int i = 0; i < n; i++) {
        int pos = positionIn2[nums1[i]];
        long long smallerBefore = countUpTo(pos);        // pos is 0-based → pos values are below
        long long biggerBefore = i - smallerBefore;
        long long biggerAfter = (n - 1 - pos) - biggerBefore;
        total += smallerBefore * biggerAfter;            // pair a left choice with a right one
        add(pos + 1);
    }
    return total;
}   // O(n log n) time · O(n) space""",
            "java": r"""// Fix the middle value; count smaller positions before and larger after
long goodTriplets(int[] nums1, int[] nums2) {
    int n = nums1.length;
    int[] positionIn2 = new int[n];
    for (int i = 0; i < n; i++) positionIn2[nums2[i]] = i;
    int[] tree = new int[n + 1];
    long total = 0;
    for (int i = 0; i < n; i++) {
        int pos = positionIn2[nums1[i]];
        long smallerBefore = 0;
        for (int p = pos; p > 0; p -= p & (-p)) smallerBefore += tree[p];
        long biggerBefore = i - smallerBefore;
        long biggerAfter = (n - 1 - pos) - biggerBefore;   // positions still unseen
        total += smallerBefore * biggerAfter;              // left choice × right choice
        for (int p = pos + 1; p <= n; p += p & (-p)) tree[p]++;
    }
    return total;
}   // O(n log n) time · O(n) space""",
            "python": r"""def good_triplets(nums1, nums2):
    n = len(nums1)
    position_in_2 = [0] * n
    for i, value in enumerate(nums2):
        position_in_2[value] = i
    tree = [0] * (n + 1)
    total = 0
    for i, value in enumerate(nums1):
        pos = position_in_2[value]                 # where this value sits in nums2
        smaller_before = 0
        p = pos
        while p > 0:                               # seen values with a smaller position
            smaller_before += tree[p]
            p -= p & -p
        bigger_before = i - smaller_before
        bigger_after = (n - 1 - pos) - bigger_before   # still unseen, position larger
        total += smaller_before * bigger_after          # a left choice × a right choice
        p = pos + 1
        while p <= n:
            tree[p] += 1
            p += p & -p
    return total""",
        },
    },
    {
        "slug": "reverse-pairs",
        "title": "Reverse Pairs",
        "difficulty": "Hard",
        "pattern": "merge sort counting",
        "statement": "Count the pairs (i, j) with i < j and nums[i] > 2 · nums[j].",
        "examples": [("nums = [1,3,2,3,1]", "2"), ("nums = [2,4,3,5,1]", "3")],
        "constraints": ["1 <= nums.length <= 5 · 10^4", "-2^31 <= nums[i] <= 2^31 - 1"],
        "approach": "Merge sort already splits the array in half and keeps each half sorted, which is exactly what the count needs: while merging, two "
                     "pointers sweep the halves and count how many right-half values are less than half of each left-half value. Values are widened to "
                     "64 bits first so 2 · nums[j] cannot overflow.",
        "complexity": ("O(n log n) time", "O(n)"),
        "code": {
            "cpp": r"""// Merge sort: count while the two sorted halves are joined
void sortAndCount(vector<long long>& nums, vector<long long>& buffer, int left, int right, long long& count) {
    if (right - left <= 1) return;
    int mid = (left + right) / 2;
    sortAndCount(nums, buffer, left, mid, count);
    sortAndCount(nums, buffer, mid, right, count);
    int j = mid;
    for (int i = left; i < mid; i++) {
        while (j < right && nums[i] > 2 * nums[j]) j++;      // each j matches many i
        count += j - mid;
    }
    int a = left, b = mid, out = left;
    while (a < mid && b < right) buffer[out++] = nums[a] <= nums[b] ? nums[a++] : nums[b++];
    while (a < mid) buffer[out++] = nums[a++];
    while (b < right) buffer[out++] = nums[b++];
    for (int i = left; i < right; i++) nums[i] = buffer[i];
}
int reversePairs(vector<int>& nums) {
    vector<long long> values(nums.begin(), nums.end()), buffer(nums.size());
    long long count = 0;
    sortAndCount(values, buffer, 0, values.size(), count);
    return (int) count;
}   // O(n log n) time · O(n) space""",
            "java": r"""// Merge sort: count while the two sorted halves are joined
void sortAndCount(long[] nums, long[] buffer, int left, int right, long[] count) {
    if (right - left <= 1) return;
    int mid = (left + right) / 2;
    sortAndCount(nums, buffer, left, mid, count);
    sortAndCount(nums, buffer, mid, right, count);
    int j = mid;
    for (int i = left; i < mid; i++) {
        while (j < right && nums[i] > 2 * nums[j]) j++;      // each j matches many i
        count[0] += j - mid;
    }
    int a = left, b = mid, out = left;
    while (a < mid && b < right) buffer[out++] = nums[a] <= nums[b] ? nums[a++] : nums[b++];
    while (a < mid) buffer[out++] = nums[a++];
    while (b < right) buffer[out++] = nums[b++];
    for (int i = left; i < right; i++) nums[i] = buffer[i];
}
int reversePairs(int[] nums) {
    long[] values = new long[nums.length], buffer = new long[nums.length], count = new long[1];
    for (int i = 0; i < nums.length; i++) values[i] = nums[i];
    sortAndCount(values, buffer, 0, values.length, count);
    return (int) count[0];
}   // O(n log n) time · O(n) space""",
            "python": r"""def reverse_pairs(nums):
    values = [float(v) for v in nums]              # 64-bit-safe arithmetic
    buffer = [0.0] * len(values)
    count = 0

    def sort_and_count(left, right):
        nonlocal count
        if right - left <= 1:
            return
        mid = (left + right) // 2
        sort_and_count(left, mid)
        sort_and_count(mid, right)
        j = mid
        for i in range(left, mid):                 # count while both halves are sorted
            while j < right and values[i] > 2 * values[j]:
                j += 1
            count += j - mid
        a, b, out = left, mid, left
        while a < mid and b < right:
            if values[a] <= values[b]:
                buffer[out] = values[a]
                a += 1
            else:
                buffer[out] = values[b]
                b += 1
            out += 1
        while a < mid:
            buffer[out] = values[a]
            a += 1
            out += 1
        while b < right:
            buffer[out] = values[b]
            b += 1
            out += 1
        values[left:right] = buffer[left:right]

    sort_and_count(0, len(values))
    return count""",
        },
    },
    {
        "slug": "sum-of-total-strength-of-wizards",
        "title": "Sum of Total Strength of Wizards",
        "difficulty": "Hard",
        "pattern": "monotonic boundaries + prefix of prefixes",
        "statement": "The total strength of a subarray is its minimum times its sum. Return the sum of total strengths over every subarray, modulo "
                     "10^9 + 7.",
        "examples": [("strength = [1,3,1,2]", "44"), ("strength = [5,4,6]", "213")],
        "constraints": ["1 <= strength.length <= 10^5", "1 <= strength[i] <= 10^9"],
        "approach": "Each subarray is charged to its minimum, so find for every index how far it stays the minimum — the nearest strictly smaller value "
                     "on the left and the nearest smaller-or-equal value on the right, which the monotonic stack gives in linear time. Within that "
                     "window all subarrays containing the index are counted at once, and a prefix-of-prefix array sums their sums in O(1).",
        "complexity": ("O(n) time", "O(n)"),
        "code": {
            "cpp": r"""// Monotonic boundaries, then prefix-of-prefix sums for the window
int totalStrength(vector<int>& strength) {
    const long long MOD = 1000000007;
    int n = strength.size();
    vector<int> previousSmaller(n, -1), nextSmallerOrEqual(n, n);
    vector<int> stack;
    for (int i = 0; i < n; i++) {
        while (!stack.empty() && strength[stack.back()] >= strength[i]) stack.pop_back();
        previousSmaller[i] = stack.empty() ? -1 : stack.back();
        stack.push_back(i);
    }
    stack.clear();
    for (int i = n - 1; i >= 0; i--) {
        while (!stack.empty() && strength[stack.back()] > strength[i]) stack.pop_back();
        nextSmallerOrEqual[i] = stack.empty() ? n : stack.back();
        stack.push_back(i);
    }
    vector<long long> prefix(n + 1, 0), doublePrefix(n + 2, 0);
    for (int i = 0; i < n; i++)
        prefix[i + 1] = (prefix[i] + strength[i]) % MOD;          // sums of strength
    for (int i = 0; i <= n; i++)
        doublePrefix[i + 1] = (doublePrefix[i] + prefix[i]) % MOD; // sums of prefix sums
    long long total = 0;
    for (int i = 0; i < n; i++) {
        long long left = i - previousSmaller[i];                   // choices of start
        long long right = nextSmallerOrEqual[i] - i;               // choices of end
        long long rightSums = (doublePrefix[i + right + 1] - doublePrefix[i + 1] + MOD) % MOD;
        long long leftSums = (doublePrefix[i + 1] - doublePrefix[i - left + 1] + MOD) % MOD;
        long long contribution = (left * rightSums - right * leftSums) % MOD;
        total = (total + strength[i] % MOD * contribution) % MOD;
    }
    return (int) ((total + MOD) % MOD);
}   // O(n) time · O(n) space""",
            "java": r"""// Monotonic boundaries, then prefix-of-prefix sums for the window
int totalStrength(int[] strength) {
    final long MOD = 1000000007L;
    int n = strength.length;
    int[] previousSmaller = new int[n], nextSmallerOrEqual = new int[n];
    int[] stack = new int[n];
    int top = 0;
    for (int i = 0; i < n; i++) {
        while (top > 0 && strength[stack[top - 1]] >= strength[i]) top--;
        previousSmaller[i] = top == 0 ? -1 : stack[top - 1];
        stack[top++] = i;
    }
    top = 0;
    for (int i = n - 1; i >= 0; i--) {
        while (top > 0 && strength[stack[top - 1]] > strength[i]) top--;
        nextSmallerOrEqual[i] = top == 0 ? n : stack[top - 1];
        stack[top++] = i;
    }
    long[] prefix = new long[n + 1], doublePrefix = new long[n + 2];
    for (int i = 0; i < n; i++) prefix[i + 1] = (prefix[i] + strength[i]) % MOD;
    for (int i = 0; i <= n; i++) doublePrefix[i + 1] = (doublePrefix[i] + prefix[i]) % MOD;
    long total = 0;
    for (int i = 0; i < n; i++) {
        long left = i - previousSmaller[i];                        // choices of start
        long right = nextSmallerOrEqual[i] - i;                    // choices of end
        long rightSums = (doublePrefix[i + (int) right + 1] - doublePrefix[i + 1] + MOD) % MOD;
        long leftSums = (doublePrefix[i + 1] - doublePrefix[i - (int) left + 1] + MOD) % MOD;
        long contribution = (left * rightSums - right * leftSums) % MOD;
        total = (total + strength[i] % MOD * contribution) % MOD;
    }
    return (int) ((total + MOD) % MOD);
}   // O(n) time · O(n) space""",
            "python": r"""def total_strength(strength):
    mod = 10**9 + 7
    n = len(strength)
    previous_smaller = [-1] * n
    next_smaller_or_equal = [n] * n
    stack = []
    for i, value in enumerate(strength):          # nearest strictly smaller on the left
        while stack and strength[stack[-1]] >= value:
            stack.pop()
        previous_smaller[i] = stack[-1] if stack else -1
        stack.append(i)
    stack.clear()
    for i in range(n - 1, -1, -1):                # nearest smaller-or-equal on the right
        while stack and strength[stack[-1]] > strength[i]:
            stack.pop()
        next_smaller_or_equal[i] = stack[-1] if stack else n
        stack.append(i)
    prefix = [0] * (n + 1)
    for i, value in enumerate(strength):
        prefix[i + 1] = (prefix[i] + value) % mod
    double_prefix = [0] * (n + 2)                 # sums of the prefix sums
    for i in range(n + 1):
        double_prefix[i + 1] = (double_prefix[i] + prefix[i]) % mod
    total = 0
    for i, value in enumerate(strength):
        left = i - previous_smaller[i]            # how many starts keep it the minimum
        right = next_smaller_or_equal[i] - i      # how many ends keep it the minimum
        right_sums = (double_prefix[i + right + 1] - double_prefix[i + 1]) % mod
        left_sums = (double_prefix[i + 1] - double_prefix[i - left + 1]) % mod
        contribution = (left * right_sums - right * left_sums) % mod
        total = (total + value % mod * contribution) % mod
    return total""",
        },
    },
    {
        "slug": "count-subarrays-with-fixed-bounds",
        "title": "Count Subarrays With Fixed Bounds",
        "difficulty": "Hard",
        "pattern": "two pointers with the last bad index",
        "statement": "Count the subarrays in which the minimum is exactly minK and the maximum is exactly maxK.",
        "examples": [("nums = [1,3,5,2,7,5], minK = 1, maxK = 5", "2"), ("nums = [1,1,1,1], minK = 1, maxK = 1", "10")],
        "constraints": ["2 <= nums.length <= 10^5", "1 <= nums[i], minK, maxK <= 10^6"],
        "approach": "Sweep the right end and remember three positions: the last element outside [minK, maxK], the last minK and the last maxK. A subarray "
                     "ending here is valid exactly when it starts after the bad position and at or before the earlier of the two boundary positions, "
                     "which turns into one subtraction per index.",
        "complexity": ("O(n) time", "O(1)"),
        "code": {
            "cpp": r"""// Windows ending at i: start after the last bad index, before both bounds
long long countSubarrays(vector<int>& nums, int minK, int maxK) {
    long long count = 0;
    int lastBad = -1, lastMin = -1, lastMax = -1;
    for (int i = 0; i < (int) nums.size(); i++) {
        if (nums[i] < minK || nums[i] > maxK) lastBad = i;   // breaks every window
        if (nums[i] == minK) lastMin = i;
        if (nums[i] == maxK) lastMax = i;
        int earliest = min(lastMin, lastMax);
        if (earliest > lastBad) count += earliest - lastBad;  // starts that work
    }
    return count;
}   // O(n) time · O(1) space""",
            "java": r"""// Windows ending at i: start after the last bad index, before both bounds
long countSubarrays(int[] nums, int minK, int maxK) {
    long count = 0;
    int lastBad = -1, lastMin = -1, lastMax = -1;
    for (int i = 0; i < nums.length; i++) {
        if (nums[i] < minK || nums[i] > maxK) lastBad = i;   // breaks every window
        if (nums[i] == minK) lastMin = i;
        if (nums[i] == maxK) lastMax = i;
        int earliest = Math.min(lastMin, lastMax);
        if (earliest > lastBad) count += earliest - lastBad;  // starts that work
    }
    return count;
}   // O(n) time · O(1) space""",
            "python": r"""def count_subarrays_with_fixed_bounds(nums, min_k, max_k):
    count = 0
    last_bad = last_min = last_max = -1
    for i, value in enumerate(nums):
        if value < min_k or value > max_k:
            last_bad = i                  # every window through here is invalid
        if value == min_k:
            last_min = i
        if value == max_k:
            last_max = i
        earliest = min(last_min, last_max)
        if earliest > last_bad:
            count += earliest - last_bad  # valid starts for a window ending here
    return count""",
        },
    },
    {
        "slug": "sum-of-subsequence-widths",
        "title": "Sum of Subsequence Widths",
        "difficulty": "Hard",
        "pattern": "sorted contributions with powers of two",
        "statement": "The width of a sequence is its largest element minus its smallest. Return the sum of widths over all non-empty subsequences of "
                     "nums, modulo 10^9 + 7.",
        "examples": [("nums = [2,1,3]", "6"), ("nums = [2]", "0")],
        "constraints": ["1 <= nums.length <= 10^5", "1 <= nums[i] <= 10^5"],
        "approach": "Sort the array: then every subsequence contributes its last element as the maximum and its first as the minimum, and each element "
                     "can be chosen freely in the middle. The value at sorted position i is the maximum of 2^i subsequences and the minimum of "
                     "2^(n-1-i), so the whole sum collapses into one pass with precomputed powers of two.",
        "complexity": ("O(n log n) time", "O(n)"),
        "code": {
            "cpp": r"""// Element i is the max of 2^i and the min of 2^(n-1-i) subsequences
int sumSubseqWidths(vector<int>& nums) {
    const long long MOD = 1000000007;
    sort(nums.begin(), nums.end());
    int n = nums.size();
    vector<long long> power(n, 1);
    for (int i = 1; i < n; i++) power[i] = power[i - 1] * 2 % MOD;
    long long total = 0;
    for (int i = 0; i < n; i++)
        total = (total + nums[i] % MOD * (power[i] - power[n - 1 - i])) % MOD;
    return (int) ((total % MOD + MOD) % MOD);
}   // O(n log n) time · O(n) space""",
            "java": r"""// Element i is the max of 2^i and the min of 2^(n-1-i) subsequences
int sumSubseqWidths(int[] nums) {
    final long MOD = 1000000007L;
    Arrays.sort(nums);
    int n = nums.length;
    long[] power = new long[n];
    power[0] = 1;
    for (int i = 1; i < n; i++) power[i] = power[i - 1] * 2 % MOD;
    long total = 0;
    for (int i = 0; i < n; i++)
        total = (total + nums[i] % MOD * (power[i] - power[n - 1 - i])) % MOD;
    return (int) ((total % MOD + MOD) % MOD);
}   // O(n log n) time · O(n) space""",
            "python": r"""def sum_subsequence_widths(nums):
    mod = 10**9 + 7
    nums.sort()
    n = len(nums)
    powers = [1] * n
    for i in range(1, n):
        powers[i] = powers[i - 1] * 2 % mod
    total = 0
    for i, value in enumerate(nums):
        total = (total + value * (powers[i] - powers[n - 1 - i])) % mod
    return total % mod""",
        },
    },
]
