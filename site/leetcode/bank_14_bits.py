# Topic 14 · Bit Manipulation
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.

TOPIC = {
    "name": "Bit Manipulation",
    "tagline": "Bits are the cheapest state you can carry: 32 facts for the price of one integer.",
    "focus": "Four moves cover this topic. XOR reveals what is odd: equal values cancel, so one stray value, one differing bit or one unbalanced "
             "prefix all fall out of a running XOR. Counting per bit turns \"how many\" questions into independent columns — and multiplying the ones "
             "by the zeros turns them into pair counts. Masks compress sets: a word becomes one integer, and subset enumeration becomes a loop over "
             "submasks. Finally, tries and digit DP over bit prefixes answer XOR-extremum questions the way ordered structures answer sum questions.",
    "ordering": "easy 1–3 are XOR and popcount basics, 4–6 build or read whole 32-bit patterns; medium 1–2 are the \"every value appears k times\" "
                "XOR family, 3–5 are arithmetic done with bits instead of +, − and /, 6–8 count per bit column, 9–12 are masking tricks over strings "
                "and windows; hard 1–5 search state spaces of bits (flip windows, matrix states, Gray code, puzzle masks), 6–9 count XOR pairs with "
                "tries and combinatorics, 10–12 combine bit masks with meet-in-the-middle and digit DP.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "single-number",
        "title": "Single Number",
        "difficulty": "Easy",
        "pattern": "XOR cancels equal values",
        "statement": "Every value in nums appears twice except one, which appears once. Return that value, in linear time and constant space.",
        "examples": [("nums = [2,2,1]", "1"), ("nums = [4,1,2,1,2]", "4"), ("nums = [1]", "1")],
        "constraints": ["1 <= nums.length <= 3 · 10^4", "-3 · 10^4 <= nums[i] <= 3 · 10^4", "every value appears twice except one"],
        "approach": "XOR of a value with itself is zero, and XOR with zero changes nothing, so the pairs cancel in any order and the single value is "
                     "what remains. Nothing is stored, and one pass suffices — the whole point of the trick is that it needs no bookkeeping.",
        "complexity": ("O(n) time", "O(1)"),
        "code": {
            "cpp": r"""// Pairs cancel under XOR; the leftover is the answer
int singleNumber(vector<int>& nums) {
    int acc = 0;
    for (int x : nums) acc ^= x;             // a ^ a == 0, a ^ 0 == a
    return acc;
}   // O(n) time · O(1) space""",
            "java": r"""// Pairs cancel under XOR; the leftover is the answer
int singleNumber(int[] nums) {
    int acc = 0;
    for (int x : nums) acc ^= x;             // a ^ a == 0, a ^ 0 == a
    return acc;
}   // O(n) time · O(1) space""",
            "python": r"""def single_number(nums):
    acc = 0
    for x in nums:
        acc ^= x                    # a ^ a = 0, so pairs cancel
    return acc""",
        },
    },
    {
        "slug": "number-of-1-bits",
        "title": "Number of 1 Bits",
        "difficulty": "Easy",
        "pattern": "clear the lowest set bit",
        "statement": "Return the number of set bits (the Hamming weight) of a positive integer n.",
        "examples": [("n = 11", "3"), ("n = 128", "1"), ("n = 2147483645", "30")],
        "constraints": ["1 <= n <= 2^31 - 1", "the answer is the count of 1 bits"],
        "approach": "Two standard loops. Either test each of the 32 positions, or use the identity n & (n - 1), which deletes the lowest set bit: the "
                     "number of deletions until zero is exactly the number of ones, so the loop runs popcount times instead of 32 times.",
        "complexity": ("O(number of 1 bits) time", "O(1)"),
        "code": {
            "cpp": r"""// n & (n - 1) deletes the lowest set bit: count the deletions
int hammingWeight(uint32_t n) {
    int count = 0;
    while (n) {
        n &= n - 1;                          // clear the lowest set bit
        count++;
    }
    return count;
}   // O(popcount) time · O(1) space""",
            "java": r"""// n & (n - 1) deletes the lowest set bit: count the deletions
int hammingWeight(int n) {
    int count = 0;
    while (n != 0) {
        n &= n - 1;                          // clear the lowest set bit
        count++;
    }
    return count;
}   // O(popcount) time · O(1) space""",
            "python": r"""def hamming_weight(n):
    count = 0
    while n:
        n &= n - 1                  # delete the lowest set bit
        count += 1
    return count""",
        },
    },
    {
        "slug": "hamming-distance",
        "title": "Hamming Distance",
        "difficulty": "Easy",
        "pattern": "popcount of the XOR",
        "statement": "Return the number of positions at which the bits of x and y differ.",
        "examples": [("x = 1, y = 4", "2"), ("x = 3, y = 1", "1")],
        "constraints": ["0 <= x, y < 2^31"],
        "approach": "A bit differs exactly where the XOR is 1, so the answer is the Hamming weight of x ^ y. That composition — reduce the comparison "
                     "to a value, then ask the previous problem's question — is how most bit-manipulation solutions are assembled.",
        "complexity": ("O(1) (at most 32 positions)", "O(1)"),
        "code": {
            "cpp": r"""// Differing bits are exactly the set bits of x ^ y
int hammingDistance(int x, int y) {
    int diff = x ^ y, count = 0;
    while (diff) { diff &= diff - 1; count++; }   // popcount of the XOR
    return count;
}   // O(1) time · O(1) space""",
            "java": r"""// Differing bits are exactly the set bits of x ^ y
int hammingDistance(int x, int y) {
    int diff = x ^ y, count = 0;
    while (diff != 0) { diff &= diff - 1; count++; }   // popcount of the XOR
    return count;
}   // O(1) time · O(1) space""",
            "python": r"""def hamming_distance(x, y):
    diff = x ^ y                    # set bits mark the positions that differ
    count = 0
    while diff:
        diff &= diff - 1            # popcount of the XOR
        count += 1
    return count""",
        },
    },
    {
        "slug": "reverse-bits",
        "title": "Reverse Bits",
        "difficulty": "Easy",
        "pattern": "collect bits into a new word",
        "statement": "Reverse the 32 bits of n and return the resulting unsigned integer.",
        "examples": [("n = 43261596", "964176192"), ("n = 2147483644", "1073741822")],
        "constraints": ["0 <= n <= 2^31 - 2", "the result is taken as an unsigned 32-bit value"],
        "approach": "Walk the 32 positions of the input and push each bit onto the low end of a result, shifting that result left each time. Reading "
                     "the bits from least significant to most significant while writing them the same way reverses the whole word in one pass.",
        "complexity": ("O(32) time", "O(1)"),
        "code": {
            "cpp": r"""// Read the bits low to high, write them into a shifting result
uint32_t reverseBits(uint32_t n) {
    uint32_t result = 0;
    for (int i = 0; i < 32; i++) {
        result = (result << 1) | (n & 1);    // move the bit into place, then flip
        n >>= 1;
    }
    return result;
}   // O(32) time · O(1) space""",
            "java": r"""// Read the bits low to high, write them into a shifting result
int reverseBits(int n) {
    int result = 0;
    for (int i = 0; i < 32; i++) {
        result = (result << 1) | (n & 1);    // move the bit into place, then flip
        n >>>= 1;                            // unsigned shift: no sign extension
    }
    return result;
}   // O(32) time · O(1) space""",
            "python": r"""def reverse_bits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)   # take the low bit, push it up
        n >>= 1
    return result""",
        },
    },
    {
        "slug": "counting-bits",
        "title": "Counting Bits",
        "difficulty": "Easy",
        "pattern": "reuse the answer for i >> 1",
        "statement": "Return an array where ans[i] is the number of set bits of i, for every i from 0 to n.",
        "examples": [("n = 2", "[0,1,1]"), ("n = 5", "[0,1,1,2,1,2]")],
        "constraints": ["0 <= n <= 10^5", "the whole array must be produced in O(n) time"],
        "approach": "Shifting i right deletes its lowest bit, so i and i >> 1 have the same number of set bits except for that one: "
                     "ans[i] = ans[i >> 1] + (i & 1). Building the table in increasing order means each entry is already known — the same "
                     "\"previous answers are ingredients\" idea as any other DP.",
        "complexity": ("O(n) time", "O(n)"),
        "code": {
            "cpp": r"""// ans[i] = ans[i >> 1] + (i & 1): the low bit is the only difference
vector<int> countBits(int n) {
    vector<int> ans(n + 1, 0);
    for (int i = 1; i <= n; i++)
        ans[i] = ans[i >> 1] + (i & 1);      // drop the lowest bit, add it back
    return ans;
}   // O(n) time · O(n) space""",
            "java": r"""// ans[i] = ans[i >> 1] + (i & 1): the low bit is the only difference
int[] countBits(int n) {
    int[] ans = new int[n + 1];
    for (int i = 1; i <= n; i++)
        ans[i] = ans[i >> 1] + (i & 1);      // drop the lowest bit, add it back
    return ans;
}   // O(n) time · O(n) space""",
            "python": r"""def count_bits(n):
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i >> 1] + (i & 1)   # the low bit is the only difference
    return ans""",
        },
    },
    {
        "slug": "power-of-four",
        "title": "Power of Four",
        "difficulty": "Easy",
        "pattern": "one bit in an even position",
        "statement": "Return true if n is a power of four, false otherwise.",
        "examples": [("n = 16", "true"), ("n = 5", "false"), ("n = 1", "true")],
        "constraints": ["-2^31 <= n <= 2^31 - 1"],
        "approach": "A power of four is a power of two whose single set bit sits in an even position. Two tests capture that: n & (n - 1) must be "
                     "zero (exactly one bit), and that bit must be inside the alternating pattern 0x55555555. Both are constant-time, and no loop or "
                     "division is needed.",
        "complexity": ("O(1) time", "O(1)"),
        "code": {
            "cpp": r"""// Exactly one bit, and it must sit at an even position
bool isPowerOfFour(int n) {
    return n > 0
        && (n & (n - 1)) == 0            // a single set bit → a power of two
        && (n & 0x55555555) != 0;        // ... at an even position → a power of four
}   // O(1) time · O(1) space""",
            "java": r"""// Exactly one bit, and it must sit at an even position
boolean isPowerOfFour(int n) {
    return n > 0
        && (n & (n - 1)) == 0            // a single set bit → a power of two
        && (n & 0x55555555) != 0;        // ... at an even position → a power of four
}   // O(1) time · O(1) space""",
            "python": r"""def is_power_of_four(n):
    if n <= 0:
        return False
    return (n & (n - 1)) == 0 and (n & 0x55555555) != 0
    # one set bit (a power of two) sitting at an even position (a power of four)""",
        },
    },
    # ---------------------------------------------------------------- MEDIUM
    {
        "slug": "single-number-ii",
        "title": "Single Number II",
        "difficulty": "Medium",
        "pattern": "count each bit modulo three",
        "statement": "Every value appears three times except one, which appears once. Return that value in linear time and constant space.",
        "examples": [("nums = [2,2,3,2]", "3"), ("nums = [0,1,0,1,0,1,99]", "99")],
        "constraints": ["1 <= nums.length <= 3 · 10^4", "-2^31 <= nums[i] <= 2^31 - 1", "every value appears three times except one"],
        "approach": "Plain XOR no longer cancels triples, so count the bits: for each of the 32 positions, the number of ones across all values is a "
                     "multiple of three unless the single value has that bit. Counting column by column with a modulo-three accumulator rebuilds the "
                     "answer bit by bit, and the same idea generalises to any odd repeat count.",
        "complexity": ("O(32 · n) time", "O(1)"),
        "code": {
            "cpp": r"""// Each bit position is counted modulo three
int singleNumber(vector<int>& nums) {
    int result = 0;
    for (int i = 0; i < 32; i++) {
        int ones = 0;
        for (int x : nums) ones += (x >> i) & 1;   // how many numbers have bit i
        if (ones % 3) result |= 1 << i;            // only the single value does
    }
    return result;
}   // O(32 · n) time · O(1) space""",
            "java": r"""// Each bit position is counted modulo three
int singleNumber(int[] nums) {
    int result = 0;
    for (int i = 0; i < 32; i++) {
        int ones = 0;
        for (int x : nums) ones += (x >>> i) & 1;  // how many numbers have bit i
        if (ones % 3 != 0) result |= 1 << i;       // only the single value does
    }
    return result;
}   // O(32 · n) time · O(1) space""",
            "python": r"""def single_number_ii(nums):
    result = 0
    for i in range(32):
        ones = sum((x >> i) & 1 for x in nums)   # how many numbers have bit i
        if ones % 3:
            result |= 1 << i                     # only the single value does
    if result >= 1 << 31:                        # a negative answer: fix the sign
        result -= 1 << 32
    return result""",
        },
    },
    {
        "slug": "single-number-iii",
        "title": "Single Number III",
        "difficulty": "Medium",
        "pattern": "XOR then split by a differing bit",
        "statement": "Two values appear exactly once and all others appear twice. Return the two single values (in any order).",
        "examples": [("nums = [1,2,1,3,2,5]", "[3,5]"), ("nums = [-1,0]", "[-1,0]"), ("nums = [0,1]", "[1,0]")],
        "constraints": ["2 <= nums.length <= 3 · 10^4", "-2^31 <= nums[i] <= 2^31 - 1", "exactly two values appear once"],
        "approach": "XOR of everything leaves the two singles XORed together, and any set bit of that residue is a bit where they differ. Partitioning "
                     "the whole array by that one bit puts the two singles in different groups, and each group is then the easy single-number problem.",
        "complexity": ("O(n) time", "O(1)"),
        "code": {
            "cpp": r"""// XOR everything, then split the array by one differing bit
vector<int> singleNumber(vector<int>& nums) {
    int diff = 0;
    for (int x : nums) diff ^= x;                 // = a ^ b
    int bit = diff & (-diff);                     // a bit where a and b differ
    int a = 0;
    for (int x : nums)
        if (x & bit) a ^= x;                      // one group cancels down to a
    return {a, diff ^ a};                         // the other group is diff ^ a
}   // O(n) time · O(1) space""",
            "java": r"""// XOR everything, then split the array by one differing bit
int[] singleNumber(int[] nums) {
    int diff = 0;
    for (int x : nums) diff ^= x;                 // = a ^ b
    int bit = diff & (-diff);                     // a bit where a and b differ
    int a = 0;
    for (int x : nums)
        if ((x & bit) != 0) a ^= x;               // one group cancels down to a
    return new int[]{a, diff ^ a};                // the other group is diff ^ a
}   // O(n) time · O(1) space""",
            "python": r"""def single_number_iii(nums):
    diff = 0
    for x in nums:
        diff ^= x                    # diff = a ^ b
    bit = diff & -diff               # a bit where a and b differ
    a = 0
    for x in nums:
        if x & bit:
            a ^= x                   # one group cancels down to a
    return [a, diff ^ a]             # the other group is diff ^ a""",
        },
    },
    {
        "slug": "bitwise-and-of-numbers-range",
        "title": "Bitwise AND of Numbers Range",
        "difficulty": "Medium",
        "pattern": "common binary prefix",
        "statement": "Return the bitwise AND of every integer in [left, right].",
        "examples": [("left = 5, right = 7", "4"), ("left = 0, right = 0", "0"), ("left = 1, right = 2147483647", "0")],
        "constraints": ["0 <= left <= right <= 2^31 - 1"],
        "approach": "A bit survives the AND only if it is 1 in every number of the range. The interval is too long to walk, but that condition is "
                     "exactly \"the bits above the highest differing bit, which are shared by left and right\" — so shifting both down until they "
                     "meet keeps only the common prefix.",
        "complexity": ("O(32) time", "O(1)"),
        "code": {
            "cpp": r"""// Shift both ends until they agree: what is left is the common prefix
int rangeBitwiseAnd(int left, int right) {
    int shift = 0;
    while (left < right) {
        left >>= 1;
        right >>= 1;
        shift++;                             // one more bit is known to differ
    }
    return left << shift;                    // the shared high bits
}   // O(32) time · O(1) space""",
            "java": r"""// Shift both ends until they agree: what is left is the common prefix
int rangeBitwiseAnd(int left, int right) {
    int shift = 0;
    while (left < right) {
        left >>= 1;
        right >>= 1;
        shift++;                             // one more bit is known to differ
    }
    return left << shift;                    // the shared high bits
}   // O(32) time · O(1) space""",
            "python": r"""def range_bitwise_and(left, right):
    shift = 0
    while left < right:
        left >>= 1
        right >>= 1
        shift += 1                   # one more low bit differs in the range
    return left << shift             # only the shared high bits survive""",
        },
    },
    {
        "slug": "sum-of-two-integers",
        "title": "Sum of Two Integers",
        "difficulty": "Medium",
        "pattern": "adder from XOR and carry",
        "statement": "Return the sum of a and b without using the + or - operators.",
        "examples": [("a = 1, b = 2", "3"), ("a = 2, b = 3", "5")],
        "constraints": ["-1000 <= a, b <= 1000"],
        "approach": "Add without carrying using XOR, then carry with AND shifted left, and repeat with those two values until the carry is empty — "
                     "that is the adder circuit, expressed as a loop. Masking to 32 bits keeps Python's unbounded integers behaving like fixed-width "
                     "ones, and the final step converts a negative two's-complement pattern back to a signed value.",
        "complexity": ("O(1) (at most 32 iterations)", "O(1)"),
        "code": {
            "cpp": r"""// XOR adds without carrying; AND shifted left is the carry
int getSum(int a, int b) {
    while (b != 0) {
        int carry = (unsigned int)(a & b) << 1;   // carry into the next column
        a = a ^ b;                                // sum bits without the carry
        b = carry;                                // repeat with the carry
    }
    return a;
}   // O(32) time · O(1) space""",
            "java": r"""// XOR adds without carrying; AND shifted left is the carry
int getSum(int a, int b) {
    while (b != 0) {
        int carry = (a & b) << 1;                // carry into the next column
        a = a ^ b;                               // sum bits without the carry
        b = carry;                               // repeat with the carry
    }
    return a;
}   // O(32) time · O(1) space""",
            "python": r"""def get_sum(a, b):
    mask = 0xFFFFFFFF                # behave like a 32-bit machine
    while b & mask:
        a, b = (a ^ b) & mask, ((a & b) << 1) & mask
    return a if a < 0x80000000 else ~(a ^ mask)   # back to a signed value""",
        },
    },
    {
        "slug": "total-hamming-distance",
        "title": "Total Hamming Distance",
        "difficulty": "Medium",
        "pattern": "ones x zeros per bit",
        "statement": "Return the sum of the Hamming distances over every unordered pair of values in nums.",
        "examples": [("nums = [4,14,2]", "6"), ("nums = [4,14,4]", "4")],
        "constraints": ["1 <= nums.length <= 10^4", "0 <= nums[i] <= 10^9"],
        "approach": "Instead of comparing pairs, count per column: if a bit is set in c values and clear in the other n - c, that column contributes "
                     "c · (n - c) to the total, because every mixed pair differs there. Summing 30 such columns replaces the quadratic pair loop with "
                     "a linear pass.",
        "complexity": ("O(32 · n) time", "O(1)"),
        "code": {
            "cpp": r"""// Each column contributes ones x zeros to the total
int totalHammingDistance(vector<int>& nums) {
    int total = 0, n = nums.size();
    for (int i = 0; i < 32; i++) {
        int ones = 0;
        for (int x : nums) ones += (x >> i) & 1;
        total += ones * (n - ones);          // mixed pairs differ at this bit
    }
    return total;
}   // O(32 · n) time · O(1) space""",
            "java": r"""// Each column contributes ones x zeros to the total
int totalHammingDistance(int[] nums) {
    int total = 0, n = nums.length;
    for (int i = 0; i < 32; i++) {
        int ones = 0;
        for (int x : nums) ones += (x >>> i) & 1;
        total += ones * (n - ones);          // mixed pairs differ at this bit
    }
    return total;
}   // O(32 · n) time · O(1) space""",
            "python": r"""def total_hamming_distance(nums):
    total = 0
    n = len(nums)
    for i in range(32):
        ones = sum((x >> i) & 1 for x in nums)
        total += ones * (n - ones)   # every mixed pair differs at this bit
    return total""",
        },
    },
    {
        "slug": "divide-two-integers",
        "title": "Divide Two Integers",
        "difficulty": "Medium",
        "pattern": "shift-and-subtract division",
        "statement": "Divide two integers without using multiplication, division or modulo, truncating toward zero and clamping to the 32-bit signed "
                     "range.",
        "examples": [("dividend = 10, divisor = 3", "3"), ("dividend = 7, divisor = -3", "-2")],
        "constraints": ["-2^31 <= dividend, divisor <= 2^31 - 1", "divisor != 0", "the result is clamped to 2^31 - 1"],
        "approach": "Long division in base two: repeatedly find the largest shifted divisor that still fits into what remains, subtract it, and set the "
                     "bit that shift represents in the quotient. Working with negative magnitudes keeps the 32-bit boundary representable, and the "
                     "sign is applied at the very end.",
        "complexity": ("O(32²) time", "O(1)"),
        "code": {
            "cpp": r"""// Long division in base two: subtract shifted divisors bit by bit
int divide(int dividend, int divisor) {
    if (dividend == INT_MIN && divisor == -1) return INT_MAX;   // clamp
    bool negative = (dividend < 0) != (divisor < 0);
    long long a = llabs((long long)dividend), b = llabs((long long)divisor);
    long long quotient = 0;
    for (int shift = 31; shift >= 0; shift--) {
        if ((b << shift) <= a) {              // the shifted divisor still fits
            a -= b << shift;
            quotient |= 1LL << shift;         // this bit of the quotient is 1
        }
    }
    quotient = negative ? -quotient : quotient;
    if (quotient > INT_MAX) return INT_MAX;
    if (quotient < INT_MIN) return INT_MIN;
    return (int) quotient;
}   // O(32^2) time · O(1) space""",
            "java": r"""// Long division in base two: subtract shifted divisors bit by bit
int divide(int dividend, int divisor) {
    if (dividend == Integer.MIN_VALUE && divisor == -1) return Integer.MAX_VALUE;
    boolean negative = (dividend < 0) != (divisor < 0);
    long a = Math.abs((long) dividend), b = Math.abs((long) divisor);
    long quotient = 0;
    for (int shift = 31; shift >= 0; shift--) {
        if ((b << shift) <= a) {              // the shifted divisor still fits
            a -= b << shift;
            quotient |= 1L << shift;          // this bit of the quotient is 1
        }
    }
    quotient = negative ? -quotient : quotient;
    if (quotient > Integer.MAX_VALUE) return Integer.MAX_VALUE;
    if (quotient < Integer.MIN_VALUE) return Integer.MIN_VALUE;
    return (int) quotient;
}   // O(32^2) time · O(1) space""",
            "python": r"""def divide(dividend, divisor):
    if dividend == -2**31 and divisor == -1:
        return 2**31 - 1                          # the only overflow case
    negative = (dividend < 0) != (divisor < 0)
    a, b = abs(dividend), abs(divisor)
    quotient = 0
    for shift in range(31, -1, -1):
        if (b << shift) <= a:                     # the shifted divisor fits
            a -= b << shift
            quotient |= 1 << shift                # this quotient bit is 1
    return -quotient if negative else quotient""",
        },
    },
    {
        "slug": "score-after-flipping-matrix",
        "title": "Score After Flipping Matrix",
        "difficulty": "Medium",
        "pattern": "integer rows + column majorities",
        "statement": "You may flip any rows and then any columns of a 0/1 matrix. Each row is read as a binary number; return the largest sum of those "
                     "numbers that is reachable.",
        "examples": [("grid = [[0,0,1,1],[1,0,1,0],[1,1,0,0]]", "39"), ("grid = [[0]]", "1")],
        "constraints": ["1 <= grid.length, grid[i].length <= 20", "grid[i][j] is 0 or 1"],
        "approach": "The first column dominates everything to its right, so flip any row whose leading bit is 0. Column flips cannot disturb that choice "
                     "independently, so afterwards each remaining column can be flipped wholesale: take whichever of the column or its complement has "
                     "more ones. Reading each row as an integer makes the first step a single comparison.",
        "complexity": ("O(rows · cols) time", "O(rows)"),
        "code": {
            "cpp": r"""// Force the leading bit to 1, then take each column's majority
int matrixScore(vector<vector<int>>& grid) {
    int m = grid.size(), n = grid[0].size(), total = 0;
    vector<int> rows(m, 0);
    for (int r = 0; r < m; r++) {
        for (int c = 0; c < n; c++) rows[r] = rows[r] << 1 | grid[r][c];
        if ((rows[r] >> (n - 1) & 1) == 0)        // leading bit is 0: flip the row
            rows[r] ^= (1 << n) - 1;              // complement all n bits
    }
    for (int c = 0; c < n; c++) {
        int ones = 0;
        for (int r = 0; r < m; r++) ones += (rows[r] >> c) & 1;
        total += max(ones, m - ones) << c;        // the better side of this column
    }
    return total;
}   // O(m·n) time · O(m) space""",
            "java": r"""// Force the leading bit to 1, then take each column's majority
int matrixScore(int[][] grid) {
    int m = grid.length, n = grid[0].length, total = 0;
    int[] rows = new int[m];
    for (int r = 0; r < m; r++) {
        for (int c = 0; c < n; c++) rows[r] = rows[r] << 1 | grid[r][c];
        if (((rows[r] >> (n - 1)) & 1) == 0)      // leading bit is 0: flip the row
            rows[r] ^= (1 << n) - 1;              // complement all n bits
    }
    for (int c = 0; c < n; c++) {
        int ones = 0;
        for (int r = 0; r < m; r++) ones += (rows[r] >> c) & 1;
        total += Math.max(ones, m - ones) << c;   // the better side of this column
    }
    return total;
}   // O(m·n) time · O(m) space""",
            "python": r"""def matrix_score(grid):
    rows, n = [], len(grid[0])
    for row in grid:
        value = 0
        for b in row:
            value = value << 1 | b
        if not value >> (n - 1) & 1:          # leading bit is 0: flip the row
            value ^= (1 << n) - 1
        rows.append(value)
    total = 0
    for c in range(n):
        ones = sum(value >> c & 1 for value in rows)
        total += max(ones, len(rows) - ones) << c   # the better side of the column
    return total""",
        },
    },
    {
        "slug": "minimum-flips-to-make-a-or-b-equal-to-c",
        "title": "Minimum Flips to Make a OR b Equal to c",
        "difficulty": "Medium",
        "pattern": "one decision per bit position",
        "statement": "Return the minimum number of bit flips needed to make a OR b equal to c. A flip changes one bit of either a or b.",
        "examples": [("a = 2, b = 6, c = 5", "3"), ("a = 4, b = 2, c = 7", "1"), ("a = 1, b = 2, c = 3", "0")],
        "constraints": ["1 <= a, b, c <= 10^9"],
        "approach": "The columns never interact, so decide each of them alone. Where c has a 0 both a and b must have 0, costing one flip per set bit "
                     "they currently carry. Where c has a 1 at least one of them must keep a 1, so an empty column costs exactly one flip. Summing the "
                     "per-column costs gives the optimum.",
        "complexity": ("O(32) time", "O(1)"),
        "code": {
            "cpp": r"""// Columns are independent: cost each one, then add up
int minFlips(int a, int b, int c) {
    int flips = 0;
    for (int i = 0; i < 32; i++) {
        int x = (a >> i) & 1, y = (b >> i) & 1, z = (c >> i) & 1;
        if (z == 0) flips += x + y;          // both must be cleared
        else if (x + y == 0) flips += 1;     // at least one must be set
    }
    return flips;
}   // O(32) time · O(1) space""",
            "java": r"""// Columns are independent: cost each one, then add up
int minFlips(int a, int b, int c) {
    int flips = 0;
    for (int i = 0; i < 32; i++) {
        int x = (a >>> i) & 1, y = (b >>> i) & 1, z = (c >>> i) & 1;
        if (z == 0) flips += x + y;          // both must be cleared
        else if (x + y == 0) flips += 1;     // at least one must be set
    }
    return flips;
}   // O(32) time · O(1) space""",
            "python": r"""def min_flips_or(a, b, c):
    flips = 0
    for i in range(32):
        x, y, z = a >> i & 1, b >> i & 1, c >> i & 1
        if z == 0:
            flips += x + y            # both must be cleared
        elif x + y == 0:
            flips += 1                # at least one must be set
    return flips""",
        },
    },
    {
        "slug": "maximum-xor-of-two-numbers-in-an-array",
        "title": "Maximum XOR of Two Numbers in an Array",
        "difficulty": "Medium",
        "pattern": "greedy prefixes in a hash set",
        "statement": "Return the maximum value of nums[i] XOR nums[j] over all pairs, in time better than quadratic.",
        "examples": [("nums = [3,10,5,25,2,8]", "28"), ("nums = [14,70,53,83,49,91,36,80,92,51,66,70]", "127")],
        "constraints": ["1 <= nums.length <= 2 · 10^5", "0 <= nums[i] < 2^31"],
        "approach": "Build the answer one bit at a time from the top. Suppose the best prefix so far is best; ask whether some pair of numbers has the "
                     "candidate prefix best | (1 << i). That is possible exactly when two stored prefixes differ in the candidate — and a prefix set "
                     "answers the question in one pass. Greedy works here because higher bits outweigh all lower ones combined.",
        "complexity": ("O(31 · n) time", "O(n)"),
        "code": {
            "cpp": r"""// Grow the answer one bit at a time; a prefix set tests each candidate
int findMaximumXOR(vector<int>& nums) {
    int best = 0, mask = 0;
    for (int i = 31; i >= 0; i--) {
        mask |= 1 << i;
        unordered_set<int> prefixes;
        for (int x : nums) prefixes.insert(x & mask);
        int candidate = best | (1 << i);
        for (int p : prefixes)
            if (prefixes.count(p ^ candidate)) { best = candidate; break; }
    }
    return best;
}   // O(31 · n) time · O(n) space""",
            "java": r"""// Grow the answer one bit at a time; a prefix set tests each candidate
int findMaximumXOR(int[] nums) {
    int best = 0, mask = 0;
    for (int i = 31; i >= 0; i--) {
        mask |= 1 << i;
        Set<Integer> prefixes = new HashSet<>();
        for (int x : nums) prefixes.add(x & mask);
        int candidate = best | (1 << i);
        for (int p : prefixes)
            if (prefixes.contains(p ^ candidate)) { best = candidate; break; }
    }
    return best;
}   // O(31 · n) time · O(n) space""",
            "python": r"""def find_maximum_xor(nums):
    best, mask = 0, 0
    for i in range(31, -1, -1):
        mask |= 1 << i
        prefixes = {x & mask for x in nums}
        candidate = best | (1 << i)
        for p in prefixes:
            if p ^ candidate in prefixes:      # two prefixes differ in the candidate
                best = candidate
                break
    return best""",
        },
    },
    {
        "slug": "find-kth-bit-in-nth-binary-string",
        "title": "Find Kth Bit in Nth Binary String",
        "difficulty": "Medium",
        "pattern": "halve the index recursively",
        "statement": "S1 is \"0\" and Sn is Sn-1 + \"1\" + reverse(invert(Sn-1)). Return the k-th bit of Sn, where k is 1-indexed.",
        "examples": [("n = 3, k = 1", "\"0\""), ("n = 4, k = 11", "\"1\"")],
        "constraints": ["1 <= n <= 20", "1 <= k <= 2^n - 1"],
        "approach": "Sn is built from Sn-1 symmetrically around its middle 1, so its length is 2^n - 1 and the middle position is a 1. Everything to "
                     "the right of that middle is a mirrored, inverted copy: convert such an index into the mirrored one and flip the bit you find. "
                     "Each step halves n, so the walk is logarithmic.",
        "complexity": ("O(n) time", "O(1)"),
        "code": {
            "cpp": r"""// The middle is '1'; the right half mirrors the left half inverted
char findKthBit(int n, int k) {
    if (n == 1) return '0';
    int mid = (1 << (n - 1));                // middle index of S_n
    if (k == mid) return '1';
    if (k < mid) return findKthBit(n - 1, k);
    return findKthBit(n - 1, 2 * mid - k) == '1' ? '0' : '1';   // mirror + invert
}   // O(n) time · O(1) space""",
            "java": r"""// The middle is '1'; the right half mirrors the left half inverted
char findKthBit(int n, int k) {
    if (n == 1) return '0';
    int mid = 1 << (n - 1);                  // middle index of S_n
    if (k == mid) return '1';
    if (k < mid) return findKthBit(n - 1, k);
    return findKthBit(n - 1, 2 * mid - k) == '1' ? '0' : '1';   // mirror + invert
}   // O(n) time · O(1) space""",
            "python": r"""def find_kth_bit(n, k):
    if n == 1:
        return "0"
    mid = 1 << (n - 1)                # middle index of S_n
    if k == mid:
        return "1"
    if k < mid:
        return find_kth_bit(n - 1, k)
    return "1" if find_kth_bit(n - 1, 2 * mid - k) == "0" else "0"
    # the right half is the left half mirrored and inverted""",
        },
    },
    {
        "slug": "maximum-product-of-word-lengths",
        "title": "Maximum Product of Word Lengths",
        "difficulty": "Medium",
        "pattern": "letter masks + pair scan",
        "statement": "Return the largest product of the lengths of two words that share no common letter, or 0 if no such pair exists.",
        "examples": [("words = [\"abcw\",\"baz\",\"foo\",\"bar\",\"xtfn\",\"abcdef\"]", "16"),
                      ("words = [\"a\",\"ab\",\"abc\",\"d\",\"cd\",\"bcd\",\"abcd\"]", "4"),
                      ("words = [\"a\",\"aa\",\"aaa\",\"aaaa\"]", "0")],
        "constraints": ["2 <= words.length <= 1000", "1 <= words[i].length <= 1000", "words[i] contains only lowercase English letters"],
        "approach": "A word's letter set fits in 26 bits, so \"do these two share a letter?\" becomes a single AND. Build the mask of each word once, "
                     "then test every pair: disjoint masks means the pair is legal, and you keep the largest length product. Longer words can also be "
                     "pruned by length, but the pair scan is already fast enough.",
        "complexity": ("O(n²) mask pairs", "O(n)"),
        "code": {
            "cpp": r"""// Each word becomes a 26-bit letter mask; disjoint masks = a valid pair
int maxProduct(vector<string>& words) {
    int n = words.size();
    vector<int> mask(n, 0), len(n, 0);
    for (int i = 0; i < n; i++) {
        len[i] = words[i].size();
        for (char ch : words[i]) mask[i] |= 1 << (ch - 'a');
    }
    int best = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if ((mask[i] & mask[j]) == 0) best = max(best, len[i] * len[j]);
    return best;
}   // O(n^2) time · O(n) space""",
            "java": r"""// Each word becomes a 26-bit letter mask; disjoint masks = a valid pair
int maxProduct(String[] words) {
    int n = words.length, best = 0;
    int[] mask = new int[n], len = new int[n];
    for (int i = 0; i < n; i++) {
        len[i] = words[i].length();
        for (char ch : words[i].toCharArray()) mask[i] |= 1 << (ch - 'a');
    }
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if ((mask[i] & mask[j]) == 0) best = Math.max(best, len[i] * len[j]);
    return best;
}   // O(n^2) time · O(n) space""",
            "python": r"""def max_product(words):
    masks, lengths = [], []
    for w in words:
        m = 0
        for ch in w:
            m |= 1 << (ord(ch) - 97)     # 26-bit letter set
        masks.append(m)
        lengths.append(len(w))
    best = 0
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if masks[i] & masks[j] == 0:   # no shared letter
                best = max(best, lengths[i] * lengths[j])
    return best""",
        },
    },
    {
        "slug": "check-if-a-string-contains-all-binary-codes-of-size-k",
        "title": "Check If a String Contains All Binary Codes of Size K",
        "difficulty": "Medium",
        "pattern": "rolling window of k bits",
        "statement": "Return true if every binary string of length k appears as a substring of the binary string s.",
        "examples": [("s = \"00110110\", k = 2", "true"), ("s = \"0110\", k = 1", "true"), ("s = \"0110\", k = 2", "false")],
        "constraints": ["1 <= s.length <= 5 · 10^5", "s[i] is '0' or '1'", "1 <= k <= 20"],
        "approach": "The windows are exactly the integers from 0 to 2^k - 1, so the question becomes \"has every integer been seen?\". Slide a window "
                     "that keeps the last k bits as an integer, store each value that appears, and stop as soon as the count reaches 2^k. A k larger "
                     "than the string answers false immediately, since the windows run out before the codes do.",
        "complexity": ("O(n) time", "O(2^k)"),
        "code": {
            "cpp": r"""// Slide a k-bit window and count how many distinct codes appear
bool hasAllCodes(string s, int k) {
    if ((int) s.size() < k) return false;
    int need = 1 << k, mask = need - 1;      // 2^k codes, k bits wide
    unordered_set<int> seen;
    int value = 0;
    for (int i = 0; i < (int) s.size(); i++) {
        value = ((value << 1) | (s[i] - '0')) & mask;   // keep the last k bits
        if (i >= k - 1) seen.insert(value);
    }
    return (int) seen.size() == need;
}   // O(n) time · O(2^k) space""",
            "java": r"""// Slide a k-bit window and count how many distinct codes appear
boolean hasAllCodes(String s, int k) {
    if (s.length() < k) return false;
    int need = 1 << k, mask = need - 1;      // 2^k codes, k bits wide
    Set<Integer> seen = new HashSet<>();
    int value = 0;
    for (int i = 0; i < s.length(); i++) {
        value = ((value << 1) | (s.charAt(i) - '0')) & mask;   // last k bits
        if (i >= k - 1) seen.add(value);
    }
    return seen.size() == need;
}   // O(n) time · O(2^k) space""",
            "python": r"""def has_all_codes(s, k):
    if len(s) < k:
        return False                       # fewer windows than codes
    need, mask, value = 1 << k, (1 << k) - 1, 0
    seen = set()
    for i, ch in enumerate(s):
        value = (value << 1 | int(ch)) & mask   # keep the last k bits
        if i >= k - 1:
            seen.add(value)
    return len(seen) == need""",
        },
    },
    {
        "slug": "minimum-number-of-k-consecutive-bit-flips",
        "title": "Minimum Number of K Consecutive Bit Flips",
        "difficulty": "Hard",
        "pattern": "greedy sweep with a flip window",
        "statement": "A flip of a length-k window turns every 0 in it into 1 and every 1 into 0. Return the minimum number of flips that turn nums into all "
                     "ones, or -1 if that is impossible.",
        "examples": [("nums = [0,1,0], k = 1", "2"), ("nums = [1,1,0], k = 2", "-1"),
                      ("nums = [0,0,0,1,0,1,1,0], k = 3", "3")],
        "constraints": ["1 <= nums.length <= 10^5", "1 <= k <= nums.length", "nums[i] is 0 or 1"],
        "approach": "Scan left to right. The leftmost bit has no choice: if it is still 0, some window must start here, so flip and account for it. What "
                     "makes the sweep cheap is that a window is described by where it ends, so a difference array tracks how many flips are still active "
                     "at each position. Reaching a 0 within the last k - 1 positions means no window can cover it, which is the only failure case.",
        "complexity": ("O(n) time", "O(n)"),
        "code": {
            "cpp": r"""// The leftmost 0 must start a flip; a difference array tracks live flips
int minKBitFlips(vector<int>& nums, int k) {
    int n = nums.size(), flips = 0, flipsUsed = 0;
    vector<int> ends(n + 1, 0);               // flips that stop at position i
    for (int i = 0; i < n; i++) {
        flips += ends[i];                     // how many windows cover i
        if ((nums[i] + flips) % 2 == 0) {      // still 0 → a window must start here
            if (i + k > n) return -1;         // no room left to cover it
            flipsUsed++;
            flips++;
            ends[i + k]--;                    // this flip expires after i + k - 1
        }
    }
    return flipsUsed;
}   // O(n) time · O(n) space""",
            "java": r"""// The leftmost 0 must start a flip; a difference array tracks live flips
int minKBitFlips(int[] nums, int k) {
    int n = nums.length, flips = 0, flipsUsed = 0;
    int[] ends = new int[n + 1];              // flips that stop at position i
    for (int i = 0; i < n; i++) {
        flips += ends[i];                     // how many windows cover i
        if ((nums[i] + flips) % 2 == 0) {      // still 0 → a window must start here
            if (i + k > n) return -1;         // no room left to cover it
            flipsUsed++;
            flips++;
            ends[i + k]--;                    // this flip expires after i + k - 1
        }
    }
    return flipsUsed;
}   // O(n) time · O(n) space""",
            "python": r"""def min_k_bit_flips(nums, k):
    n = len(nums)
    ends = [0] * (n + 1)               # flips that expire at position i
    flips = flips_used = 0
    for i in range(n):
        flips += ends[i]               # how many windows cover i
        if (nums[i] + flips) % 2 == 0:  # still 0 → a window must start here
            if i + k > n:
                return -1              # no room left to cover it
            flips_used += 1
            flips += 1
            ends[i + k] -= 1           # expires after i + k - 1
    return flips_used""",
        },
    },
    {
        "slug": "minimum-number-of-flips-to-convert-binary-matrix-to-zero-matrix",
        "title": "Minimum Number of Flips to Convert Binary Matrix to Zero Matrix",
        "difficulty": "Hard",
        "pattern": "BFS over bitmask states",
        "statement": "A move picks a cell and flips it together with its four edge neighbours. Return the minimum number of moves that turn the whole "
                     "matrix into zeros, or -1 if it is impossible.",
        "examples": [("mat = [[0,0],[0,1]]", "3"), ("mat = [[0]]", "0"), ("mat = [[1,0,0],[1,0,0]]", "-1")],
        "constraints": ["1 <= mat.length, mat[i].length <= 3", "mat[i][j] is 0 or 1"],
        "approach": "The visible state is what matters, not the order of the moves, so pack the matrix into a bitmask and run a shortest-path search "
                     "over masks. Precompute the mask that each cell toggles, then every edge of the search is one XOR. The state space is at most 512, "
                     "so plain BFS is comfortably fast and -1 simply means the search never reached the zero mask.",
        "complexity": ("O(2^(r·c) · r · c) time", "O(2^(r·c))"),
        "code": {
            "cpp": r"""// Pack the board into a bitmask and run BFS over states
int minFlips(vector<vector<int>>& mat) {
    int rows = mat.size(), cols = mat[0].size(), cells = rows * cols;
    vector<int> toggles(cells, 0);
    int dr[5] = {0, -1, 1, 0, 0}, dc[5] = {0, 0, 0, -1, 1};
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            for (int d = 0; d < 5; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols)
                    toggles[r * cols + c] |= 1 << (nr * cols + nc);
            }
    int start = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            if (mat[r][c]) start |= 1 << (r * cols + c);
    vector<int> dist(1 << cells, -1);
    queue<int> q;
    dist[start] = 0;
    q.push(start);
    while (!q.empty()) {
        int cur = q.front(); q.pop();
        if (cur == 0) return dist[cur];       // the all-zero board
        for (int i = 0; i < cells; i++) {
            int nxt = cur ^ toggles[i];       // one move
            if (dist[nxt] == -1) { dist[nxt] = dist[cur] + 1; q.push(nxt); }
        }
    }
    return -1;
}   // O(2^cells · cells) time · O(2^cells) space""",
            "java": r"""// Pack the board into a bitmask and run BFS over states
int minFlips(int[][] mat) {
    int rows = mat.length, cols = mat[0].length, cells = rows * cols;
    int[] toggles = new int[cells];
    int[] dr = {0, -1, 1, 0, 0}, dc = {0, 0, 0, -1, 1};
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            for (int d = 0; d < 5; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols)
                    toggles[r * cols + c] |= 1 << (nr * cols + nc);
            }
    int start = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            if (mat[r][c] == 1) start |= 1 << (r * cols + c);
    int[] dist = new int[1 << cells];
    Arrays.fill(dist, -1);
    ArrayDeque<Integer> q = new ArrayDeque<>();
    dist[start] = 0;
    q.add(start);
    while (!q.isEmpty()) {
        int cur = q.poll();
        if (cur == 0) return dist[cur];       // the all-zero board
        for (int i = 0; i < cells; i++) {
            int nxt = cur ^ toggles[i];       // one move
            if (dist[nxt] == -1) { dist[nxt] = dist[cur] + 1; q.add(nxt); }
        }
    }
    return -1;
}   // O(2^cells · cells) time · O(2^cells) space""",
            "python": r"""def min_flips_matrix(mat):
    rows, cols = len(mat), len(mat[0])
    cells = rows * cols
    toggles = [0] * cells
    for r in range(rows):
        for c in range(cols):
            m = 0
            for dr, dc in ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    m |= 1 << (nr * cols + nc)     # cell plus its neighbours
            toggles[r * cols + c] = m
    start = 0
    for r in range(rows):
        for c in range(cols):
            if mat[r][c]:
                start |= 1 << (r * cols + c)
    dist = {start: 0}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        if cur == 0:
            return dist[cur]                # the all-zero board
        for m in toggles:
            nxt = cur ^ m                   # one move
            if nxt not in dist:
                dist[nxt] = dist[cur] + 1
                queue.append(nxt)
    return -1""",
        },
    },
    {
        "slug": "number-of-valid-words-for-each-puzzle",
        "title": "Number of Valid Words for Each Puzzle",
        "difficulty": "Hard",
        "pattern": "letter masks + submask enumeration",
        "statement": "A word is valid for a puzzle when it contains the puzzle's first letter and every letter of the word appears in the puzzle. Return "
                     "the number of valid words for each puzzle.",
        "examples": [("words = [\"aaaa\",\"asas\",\"able\",\"ability\",\"actt\",\"actor\",\"access\"], puzzles = [\"aboveyz\",\"abrodyz\",\"abslute\",\"absoryz\",\"actresz\",\"gaswxyz\"]",
                      "[1,1,3,2,4,0]"),
                      ("words = [\"apple\",\"pleas\",\"please\"], puzzles = [\"aelwxyz\",\"aelpxyz\",\"aelpsxy\",\"saelpxy\",\"xaelpsy\"]",
                       "[0,1,3,2,0]")],
        "constraints": ["1 <= words.length <= 10^5", "4 <= words[i].length <= 50", "1 <= puzzles.length <= 10^4",
                        "puzzles[i].length == 7", "all puzzles have distinct letters"],
        "approach": "Turn every word into a 26-bit letter mask; words with more than seven distinct letters can never fit a puzzle and are kept out of "
                     "a frequency table keyed by mask. A puzzle has seven letters, so it has only 64 subsets that contain its first letter — enumerate "
                     "those submasks and add the stored frequencies. Big inputs are handled by looking up masks rather than scanning the word list.",
        "complexity": ("O(total word length + 64 · puzzles) time", "O(distinct masks)"),
        "code": {
            "cpp": r"""// Word -> letter mask table, then 64 submask look-ups per puzzle
vector<int> findNumOfValidWords(vector<string>& words, vector<string>& puzzles) {
    unordered_map<int, int> freq;                 // letter mask -> how many words
    for (const string& w : words) {
        int mask = 0;
        for (char ch : w) mask |= 1 << (ch - 'a');
        if (__builtin_popcount(mask) <= 7) freq[mask]++;   // wider than a puzzle
    }
    vector<int> answer;
    for (const string& p : puzzles) {
        int first = 1 << (p[0] - 'a'), mask = 0;
        for (char ch : p) mask |= 1 << (ch - 'a');
        int rest = mask ^ first, total = 0;
        for (int sub = rest; ; sub = (sub - 1) & rest) {    // the 64 submasks
            auto it = freq.find(sub | first);               // must contain p[0]
            if (it != freq.end()) total += it->second;
            if (sub == 0) break;
        }
        answer.push_back(total);
    }
    return answer;
}   // O(words + 64 · puzzles) time · O(distinct masks) space""",
            "java": r"""// Word -> letter mask table, then 64 submask look-ups per puzzle
List<Integer> findNumOfValidWords(String[] words, String[] puzzles) {
    Map<Integer, Integer> freq = new HashMap<>();   // letter mask -> word count
    for (String w : words) {
        int mask = 0;
        for (char ch : w.toCharArray()) mask |= 1 << (ch - 'a');
        if (Integer.bitCount(mask) <= 7)        // wider than any puzzle
            freq.merge(mask, 1, Integer::sum);
    }
    List<Integer> answer = new ArrayList<>();
    for (String p : puzzles) {
        int first = 1 << (p.charAt(0) - 'a'), mask = 0;
        for (char ch : p.toCharArray()) mask |= 1 << (ch - 'a');
        int rest = mask ^ first, total = 0;
        for (int sub = rest; ; sub = (sub - 1) & rest) {   // the 64 submasks
            total += freq.getOrDefault(sub | first, 0);     // must contain p[0]
            if (sub == 0) break;
        }
        answer.add(total);
    }
    return answer;
}   // O(words + 64 · puzzles) time · O(distinct masks) space""",
            "python": r"""def find_num_of_valid_words(words, puzzles):
    freq = {}
    for w in words:
        mask = 0
        for ch in w:
            mask |= 1 << (ord(ch) - 97)
        if bin(mask).count("1") <= 7:          # cannot fit inside a puzzle
            freq[mask] = freq.get(mask, 0) + 1
    answer = []
    for p in puzzles:
        first = 1 << (ord(p[0]) - 97)
        mask = 0
        for ch in p:
            mask |= 1 << (ord(ch) - 97)
        rest, total = mask ^ first, 0
        sub = rest
        while True:                            # the 64 submasks containing p[0]
            total += freq.get(sub | first, 0)
            if sub == 0:
                break
            sub = (sub - 1) & rest
        answer.append(total)
    return answer""",
        },
    },
    {
        "slug": "minimum-one-bit-operations-to-make-integers-zero",
        "title": "Minimum One Bit Operations to Make Integers Zero",
        "difficulty": "Hard",
        "pattern": "Gray-code distance recursion",
        "statement": "An operation either changes bit 0 of n, or changes bit i when bit i - 1 is 1 and bits i - 2 down to 0 are all 0. Return the "
                     "minimum number of operations that turn n into 0.",
        "examples": [("n = 3", "2"), ("n = 6", "4")],
        "constraints": ["0 <= n <= 10^9"],
        "approach": "Each operation is a step between consecutive Gray codes, so the answer is n's position in Gray-code order — the inverse Gray "
                     "value of n. A step at the highest set bit costs 2^(k+1) - 1 operations and lands on n with that bit cleared, and what is left is "
                     "the same question on a smaller number: a recursion that shortens the binary length each time.",
        "complexity": ("O(log n) time", "O(1)"),
        "code": {
            "cpp": r"""// Gray-code distance: clear the top bit, then recurse on the rest
int minimumOneBitOperations(int n) {
    if (n <= 1) return n;
    int k = 31 - __builtin_clz(n);            // index of the highest set bit
    return (1 << (k + 1)) - 1 - minimumOneBitOperations(n ^ (1 << k));
}   // O(log n) time · O(1) space""",
            "java": r"""// Gray-code distance: clear the top bit, then recurse on the rest
int minimumOneBitOperations(int n) {
    if (n <= 1) return n;
    int k = 31 - Integer.numberOfLeadingZeros(n);   // highest set bit
    return (1 << (k + 1)) - 1 - minimumOneBitOperations(n ^ (1 << k));
}   // O(log n) time · O(1) space""",
            "python": r"""def minimum_one_bit_operations(n):
    if n <= 1:
        return n
    k = n.bit_length() - 1                     # index of the highest set bit
    return (1 << (k + 1)) - 1 - minimum_one_bit_operations(n ^ (1 << k))
    # clearing the top bit costs 2^(k+1) - 1 moves and flips the rest""",
        },
    },
    {
        "slug": "find-xor-sum-of-all-pairs-bitwise-and",
        "title": "Find XOR Sum of All Pairs Bitwise AND",
        "difficulty": "Hard",
        "pattern": "per-bit counting of AND results",
        "statement": "Return the XOR of (arr1[i] AND arr2[j]) over every ordered pair (i, j).",
        "examples": [("arr1 = [1,2,3], arr2 = [6,5]", "0"), ("arr1 = [12], arr2 = [4]", "4")],
        "constraints": ["1 <= arr1.length, arr2.length <= 5 · 10^4", "1 <= arr1[i], arr2[i] <= 10^9"],
        "approach": "The XOR of the pair values depends on each bit separately, because XOR keeps the columns independent. A bit of the AND is 1 "
                     "exactly for the pairs where both operands have it, so its contribution appears ones1 · ones2 times; the bit survives the XOR only "
                     "when that count is odd. Each column can therefore be decided with two counters instead of a double loop.",
        "complexity": ("O(32 · (n + m)) time", "O(1)"),
        "code": {
            "cpp": r"""// A bit survives the XOR when ones1 · ones2 is odd
int getXORSum(vector<int>& arr1, vector<int>& arr2) {
    int result = 0;
    for (int b = 0; b < 32; b++) {
        long long ones1 = 0, ones2 = 0;
        for (int x : arr1) ones1 += (x >> b) & 1;
        for (int y : arr2) ones2 += (y >> b) & 1;
        if ((ones1 * ones2) % 2 == 1) result |= 1 << b;   // odd → XOR bit is 1
    }
    return result;
}   // O(32 · (n + m)) time · O(1) space""",
            "java": r"""// A bit survives the XOR when ones1 · ones2 is odd
int getXORSum(int[] arr1, int[] arr2) {
    int result = 0;
    for (int b = 0; b < 32; b++) {
        long ones1 = 0, ones2 = 0;
        for (int x : arr1) ones1 += (x >> b) & 1;
        for (int y : arr2) ones2 += (y >> b) & 1;
        if ((ones1 * ones2) % 2 == 1) result |= 1 << b;   // odd → XOR bit is 1
    }
    return result;
}   // O(32 · (n + m)) time · O(1) space""",
            "python": r"""def get_xor_sum(arr1, arr2):
    result = 0
    for b in range(32):
        ones1 = sum(x >> b & 1 for x in arr1)
        ones2 = sum(y >> b & 1 for y in arr2)
        if ones1 * ones2 % 2:              # an odd number of 1 bits survives
            result |= 1 << b
    return result""",
        },
    },
    {
        "slug": "number-of-excellent-pairs",
        "title": "Number of Excellent Pairs",
        "difficulty": "Hard",
        "pattern": "popcount pairs counted by group",
        "statement": "The pair (a, b) of values from nums is excellent when the total number of set bits of (a AND b) plus (a OR b) is at least k. Return "
                     "the number of excellent ordered pairs, counting duplicates only once.",
        "examples": [("nums = [1,2,3,1], k = 3", "5"), ("nums = [5,1,1], k = 10", "0")],
        "constraints": ["1 <= nums.length <= 10^5", "1 <= nums[i] <= 10^9", "1 <= k <= 60"],
        "approach": "The identity popcount(a AND b) + popcount(a OR b) = popcount(a) + popcount(b) removes the pair itself from the measurement: a "
                     "pair is excellent exactly when the two popcounts sum to at least k. So bucket the distinct values by popcount and count pairs of "
                     "buckets with a small double loop — duplicates collapse because they contribute the same popcount.",
        "complexity": ("O(n + 32²) time", "O(n)"),
        "code": {
            "cpp": r"""// popcount(a AND b) + popcount(a OR b) = popcount(a) + popcount(b)
long long countExcellentPairs(vector<int>& nums, int k) {
    unordered_set<int> distinct(nums.begin(), nums.end());   // duplicates collapse
    long long byCount[32] = {0};
    for (int x : distinct) byCount[__builtin_popcount((unsigned) x)]++;
    long long total = 0;
    for (int p = 0; p < 32; p++)
        for (int q = 0; q < 32; q++)
            if (p + q >= k) total += byCount[p] * byCount[q];
    return total;
}   // O(n + 32^2) time · O(n) space""",
            "java": r"""// popcount(a AND b) + popcount(a OR b) = popcount(a) + popcount(b)
long countExcellentPairs(int[] nums, long k) {
    Set<Integer> distinct = new HashSet<>();
    for (int x : nums) distinct.add(x);          // duplicates collapse
    long[] byCount = new long[32];
    for (int x : distinct) byCount[Integer.bitCount(x)]++;
    long total = 0;
    for (int p = 0; p < 32; p++)
        for (int q = 0; q < 32; q++)
            if (p + q >= k) total += byCount[p] * byCount[q];
    return total;
}   // O(n + 32^2) time · O(n) space""",
            "python": r"""def count_excellent_pairs(nums, k):
    by_count = [0] * 32
    for x in set(nums):                # duplicates collapse
        by_count[bin(x).count("1")] += 1
    total = 0
    for p in range(32):
        for q in range(32):
            if p + q >= k:             # popcount(a) + popcount(b) >= k
                total += by_count[p] * by_count[q]
    return total""",
        },
    },
    {
        "slug": "kth-smallest-instructions",
        "title": "Kth Smallest Instructions",
        "difficulty": "Hard",
        "pattern": "count paths, then take a step",
        "statement": "You start at (0, 0) and want to reach destination = [row, column], writing \"H\" for a step right and \"V\" for a step down. Return "
                     "the k-th smallest instruction string in lexicographic order.",
        "examples": [("destination = [2,3], k = 1", "\"HHHVV\""), ("destination = [2,3], k = 2", "\"HHVHV\""), ("destination = [2,3], k = 3", "\"HHVVH\"")],
        "constraints": ["1 <= row, column <= 15", "1 <= k <= number of ways to reach the destination"],
        "approach": "Lexicographic order means every string that starts with H comes before every string that starts with V, so the paths starting with H "
                     "form a prefix block whose size is a binomial coefficient. Compare k with that block: if it fits, the answer starts with H; "
                     "otherwise skip the whole block (subtract it) and start with V. Repeating this consumes one letter at a time.",
        "complexity": ("O((row + column)²) time", "O(1)"),
        "code": {
            "cpp": r"""// Every H-first path precedes every V-first path: count, then commit
long long choose(int n, int r) {
    long long result = 1;
    for (int i = 1; i <= r; i++) result = result * (n - r + i) / i;
    return result;
}
string kthSmallestPath(vector<int>& destination, int k) {
    int down = destination[0], right = destination[1];   // V steps, H steps
    string result;
    while (down + right > 0) {
        if (right > 0) {
            long long withH = choose(down + right - 1, right - 1);   // H-first block
            if (k <= withH) { result += 'H'; right--; continue; }
            k -= withH;                                  // skip the whole block
        }
        result += 'V';                                   // only V-first paths remain
        down--;
    }
    return result;
}   // O((row+column)^2) time · O(1) space""",
            "java": r"""// Every H-first path precedes every V-first path: count, then commit
long choose(int n, int r) {
    long result = 1;
    for (int i = 1; i <= r; i++) result = result * (n - r + i) / i;
    return result;
}
String kthSmallestPath(int[] destination, int k) {
    int down = destination[0], right = destination[1];   // V steps, H steps
    StringBuilder result = new StringBuilder();
    while (down + right > 0) {
        if (right > 0) {
            long withH = choose(down + right - 1, right - 1);   // H-first block
            if (k <= withH) { result.append('H'); right--; continue; }
            k -= withH;                                  // skip the whole block
        }
        result.append('V');                              // only V-first paths remain
        down--;
    }
    return result.toString();
}   // O((row+column)^2) time · O(1) space""",
            "python": r"""def kth_smallest_path(destination, k):
    down, right = destination[0], destination[1]   # V steps and H steps

    def choose(n, r):
        result = 1
        for i in range(1, r + 1):
            result = result * (n - r + i) // i
        return result

    result = []
    while down + right > 0:
        if right > 0:
            with_h = choose(down + right - 1, right - 1)   # paths starting with H
            if k <= with_h:                        # the answer lies inside the block
                result.append("H")
                right -= 1
                continue
            k -= with_h                            # skip the whole H-first block
        result.append("V")                         # only V-first paths remain
        down -= 1
    return "".join(result)""",
        },
    },
    {
        "slug": "maximum-xor-with-an-element-from-array",
        "title": "Maximum XOR With an Element From Array",
        "difficulty": "Hard",
        "pattern": "offline sort + binary trie",
        "statement": "For each query [xi, mi], return the maximum xi XOR nums[j] over values not exceeding mi, or -1 when no value qualifies.",
        "examples": [("nums = [0,1,2,3,4], queries = [[3,1],[1,3],[5,6]]", "[3,3,7]"),
                      ("nums = [5,2,4,6,6,3], queries = [[12,4],[8,1],[6,3]]", "[15,-1,5]")],
        "constraints": ["1 <= nums.length, queries.length <= 5 · 10^4", "1 <= nums[i], xi, mi <= 10^9"],
        "approach": "The limit is the only thing that makes a query hard, so answer the queries in increasing order of limit and grow one structure as "
                     "you go. Sorting both, inserting every value that now qualifies into a bit trie, and answering each query greedily bit by bit "
                     "keeps the whole thing near-linear; queries whose limit admits nothing yet return -1.",
        "complexity": ("O((n + q) · 31) time", "O(n · 31)"),
        "code": {
            "cpp": r"""// Sort queries by limit, feed values into a binary trie, answer greedily
vector<int> maximizeXor(vector<int>& nums, vector<vector<int>>& queries) {
    sort(nums.begin(), nums.end());
    int q = queries.size();
    vector<int> order(q), answer(q);
    iota(order.begin(), order.end(), 0);
    sort(order.begin(), order.end(),
         [&](int a, int b) { return queries[a][1] < queries[b][1]; });
    vector<array<int, 2>> child(1, {-1, -1});        // binary trie of live values
    int next = 0;                                    // how many values are inserted
    for (int qi : order) {
        int x = queries[qi][0], limit = queries[qi][1];
        while (next < (int) nums.size() && nums[next] <= limit) {
            int node = 0;
            for (int b = 30; b >= 0; b--) {
                int bit = (nums[next] >> b) & 1;
                if (child[node][bit] == -1) { child[node][bit] = child.size(); child.push_back({-1, -1}); }
                node = child[node][bit];
            }
            next++;
        }
        if (next == 0) { answer[qi] = -1; continue; }    // nothing is small enough
        int node = 0, best = 0;
        for (int b = 30; b >= 0; b--) {
            int bit = (x >> b) & 1;
            if (child[node][bit ^ 1] != -1) {            // prefer the opposite bit
                best |= 1 << b;
                node = child[node][bit ^ 1];
            } else {
                node = child[node][bit];
            }
        }
        answer[qi] = best;
    }
    return answer;
}   // O((n + q) · 31) time · O(n · 31) space""",
            "java": r"""// Sort queries by limit, feed values into a binary trie, answer greedily
List<Integer> maximizeXor(int[] nums, int[][] queries) {
    Arrays.sort(nums);
    int q = queries.length;
    Integer[] order = new Integer[q];
    for (int i = 0; i < q; i++) order[i] = i;
    Arrays.sort(order, (a, b) -> Integer.compare(queries[a][1], queries[b][1]));
    List<int[]> child = new ArrayList<>();           // binary trie of live values
    child.add(new int[]{-1, -1});
    int[] answer = new int[q], next = {0};
    for (int qi : order) {
        int x = queries[qi][0], limit = queries[qi][1];
        while (next[0] < nums.length && nums[next[0]] <= limit) insertValue(child, nums[next[0]]++);
        if (next[0] == 0) { answer[qi] = -1; continue; }   // nothing is small enough
        answer[qi] = bestXor(child, x);
    }
    List<Integer> result = new ArrayList<>();
    for (int v : answer) result.add(v);
    return result;
}
void insertValue(List<int[]> child, int value) {
    int node = 0;
    for (int b = 30; b >= 0; b--) {
        int bit = (value >> b) & 1;
        if (child.get(node)[bit] == -1) {
            child.get(node)[bit] = child.size();
            child.add(new int[]{-1, -1});
        }
        node = child.get(node)[bit];
    }
}
int bestXor(List<int[]> child, int value) {
    int node = 0, best = 0;
    for (int b = 30; b >= 0; b--) {
        int bit = (value >> b) & 1;
        if (child.get(node)[bit ^ 1] != -1) {        // prefer the opposite bit
            best |= 1 << b;
            node = child.get(node)[bit ^ 1];
        } else {
            node = child.get(node)[bit];
        }
    }
    return best;
}   // O((n + q) · 31) time · O(n · 31) space""",
            "python": r"""def maximize_xor(nums, queries):
    nums.sort()
    order = sorted(range(len(queries)), key=lambda i: queries[i][1])
    child = [[-1, -1]]                 # binary trie of the values inserted so far
    answer = [0] * len(queries)
    nxt = 0
    for qi in order:
        x, limit = queries[qi]
        while nxt < len(nums) and nums[nxt] <= limit:
            node = 0
            for b in range(30, -1, -1):
                bit = nums[nxt] >> b & 1
                if child[node][bit] == -1:
                    child[node][bit] = len(child)
                    child.append([-1, -1])
                node = child[node][bit]
            nxt += 1
        if nxt == 0:                   # no value is small enough yet
            answer[qi] = -1
            continue
        node = best = 0
        for b in range(30, -1, -1):
            bit = x >> b & 1
            if child[node][bit ^ 1] != -1:      # prefer the opposite bit
                best |= 1 << b
                node = child[node][bit ^ 1]
            else:
                node = child[node][bit]
        answer[qi] = best
    return answer""",
        },
    },
    {
        "slug": "count-pairs-with-xor-in-a-range",
        "title": "Count Pairs With XOR in a Range",
        "difficulty": "Hard",
        "pattern": "trie counting of xors below a bound",
        "statement": "Count the pairs (i, j) with i < j whose nums[i] XOR nums[j] lies between low and high.",
        "examples": [("nums = [1,4,2,7], low = 2, high = 6", "6"), ("nums = [9,8,4,2,1], low = 5, high = 14", "8")],
        "constraints": ["1 <= nums.length <= 5 · 10^4", "1 <= nums[i] <= 2 · 10^4", "0 <= low <= high <= 2 · 10^4"],
        "approach": "Counting below high and below low - 1 and subtracting turns a range into two half-open questions. For a bound, walk a binary trie of "
                     "the numbers seen so far: where the bound's bit is 1, every value matching the current bit already makes the XOR smaller — add "
                     "that whole subtree — and otherwise the only way forward is the matching branch. Each pair is counted once by inserting values as "
                     "you scan.",
        "complexity": ("O(17 · n) time", "O(17 · n)"),
        "code": {
            "cpp": r"""// below(high) - below(low): walk a trie, adding whole subtrees on 1-bits
long long countBelow(const vector<int>& nums, int limit) {
    vector<array<int, 2>> child(1, {-1, -1});
    vector<int> count(1, 0);                 // how many values pass through a node
    long long total = 0;
    for (int value : nums) {
        int node = 0;
        long long below = 0;
        for (int b = 16; b >= 0 && node != -1; b--) {
            int vb = (value >> b) & 1, lb = (limit >> b) & 1;
            if (lb) {                        // xor bit 0 already beats this bound bit
                int same = child[node][vb];
                if (same != -1) below += count[same];
                node = child[node][vb ^ 1];  // keep the xor bit equal to the bound
            } else {
                node = child[node][vb];      // must match the bound bit exactly
            }
        }
        total += below;                      // pairs (value, earlier value)
        node = 0;
        count[0]++;
        for (int b = 16; b >= 0; b--) {
            int bit = (value >> b) & 1;
            if (child[node][bit] == -1) {
                child[node][bit] = child.size();
                child.push_back({-1, -1});
                count.push_back(0);
            }
            node = child[node][bit];
            count[node]++;
        }
    }
    return total;
}
long long countPairs(vector<int>& nums, int low, int high) {
    return countBelow(nums, high + 1) - countBelow(nums, low);
}   // O(17 · n) time · O(17 · n) space""",
            "java": r"""// below(high) - below(low): walk a trie, adding whole subtrees on 1-bits
long countBelow(int[] nums, int limit) {
    List<int[]> child = new ArrayList<>();
    List<Integer> count = new ArrayList<>();
    child.add(new int[]{-1, -1});
    count.add(0);
    long total = 0;
    for (int value : nums) {
        int node = 0;
        long below = 0;
        for (int b = 16; b >= 0 && node != -1; b--) {
            int vb = (value >> b) & 1, lb = (limit >> b) & 1;
            if (lb == 1) {                   // xor bit 0 already beats this bound bit
                int same = child.get(node)[vb];
                if (same != -1) below += count.get(same);
                node = child.get(node)[vb ^ 1];   // keep the xor bit equal
            } else {
                node = child.get(node)[vb];       // must match the bound bit
            }
        }
        total += below;                      // pairs (value, earlier value)
        node = 0;
        count.set(0, count.get(0) + 1);
        for (int b = 16; b >= 0; b--) {
            int bit = (value >> b) & 1;
            if (child.get(node)[bit] == -1) {
                child.get(node)[bit] = child.size();
                child.add(new int[]{-1, -1});
                count.add(0);
            }
            node = child.get(node)[bit];
            count.set(node, count.get(node) + 1);
        }
    }
    return total;
}
long countPairs(int[] nums, int low, int high) {
    return countBelow(nums, high + 1) - countBelow(nums, low);
}   // O(17 · n) time · O(17 · n) space""",
            "python": r"""def count_pairs(nums, low, high):
    def count_below(limit):
        child = [[-1, -1]]             # trie of the values inserted so far
        count = [0]
        total = 0
        for value in nums:
            node, below = 0, 0
            for b in range(16, -1, -1):
                if node == -1:
                    break
                vb, lb = value >> b & 1, limit >> b & 1
                if lb:                 # xor bit 0 already beats this bound bit
                    same = child[node][vb]
                    if same != -1:
                        below += count[same]
                    node = child[node][vb ^ 1]   # keep the xor bit equal
                else:
                    node = child[node][vb]       # must match the bound bit
            total += below             # pairs (value, earlier value)
            node = 0
            count[0] += 1
            for b in range(16, -1, -1):
                bit = value >> b & 1
                if child[node][bit] == -1:
                    child[node][bit] = len(child)
                    child.append([-1, -1])
                    count.append(0)
                node = child[node][bit]
                count[node] += 1
        return total

    return count_below(high + 1) - count_below(low)""",
        },
    },
    {
        "slug": "maximum-strong-pair-xor-ii",
        "title": "Maximum Strong Pair XOR II",
        "difficulty": "Hard",
        "pattern": "sliding window + trie with deletion",
        "statement": "A pair (x, y) is strong when |x - y| <= min(x, y). Return the maximum y XOR x over strong pairs of nums.",
        "examples": [("nums = [1,2,3,4,5]", "7"), ("nums = [10,100]", "0"), ("nums = [500,520,2500,3000]", "1020")],
        "constraints": ["1 <= nums.length <= 5 · 10^4", "1 <= nums[i] <= 10^5"],
        "approach": "After sorting, |x - y| <= min(x, y) is the same as max <= 2 · min, so for a right end the legal partners form a window whose left "
                     "edge only moves forward. Keep a binary trie of the window's values with per-node counts, query the best XOR partner for each "
                     "new element, and delete values as the window slides — a dynamic structure, because the window changes at both ends.",
        "complexity": ("O(n · 17) time", "O(n · 17)"),
        "code": {
            "cpp": r"""// Sorted window (max <= 2 · min) + a trie that supports deletion
void insertValue(vector<array<int, 2>>& child, vector<int>& count, int value) {
    int node = 0;
    count[0]++;
    for (int b = 16; b >= 0; b--) {
        int bit = (value >> b) & 1;
        if (child[node][bit] == -1) { child[node][bit] = child.size(); child.push_back({-1, -1}); count.push_back(0); }
        node = child[node][bit];
        count[node]++;
    }
}
void eraseValue(vector<array<int, 2>>& child, vector<int>& count, int value) {
    int node = 0;
    count[0]--;
    for (int b = 16; b >= 0; b--) {
        node = child[node][(value >> b) & 1];
        count[node]--;
    }
}
int bestXor(const vector<array<int, 2>>& child, const vector<int>& count, int value) {
    int node = 0, best = 0;
    for (int b = 16; b >= 0; b--) {
        int bit = (value >> b) & 1;
        int opposite = child[node][bit ^ 1];
        if (opposite != -1 && count[opposite] > 0) {      // a live value differs here
            best |= 1 << b;
            node = opposite;
        } else {
            node = child[node][bit];
        }
    }
    return best;
}
int maximumStrongPairXor(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    vector<array<int, 2>> child(1, {-1, -1});
    vector<int> count(1, 0);
    int left = 0, best = 0;
    for (int value : nums) {
        while (nums[left] * 2 < value) eraseValue(child, count, nums[left++]);
        best = max(best, bestXor(child, count, value));   // against the live window
        insertValue(child, count, value);
    }
    return best;
}   // O(n · 17) time · O(n · 17) space""",
            "java": r"""// Sorted window (max <= 2 · min) + a trie that supports deletion
void insertValue(List<int[]> child, List<Integer> count, int value) {
    int node = 0;
    count.set(0, count.get(0) + 1);
    for (int b = 16; b >= 0; b--) {
        int bit = (value >> b) & 1;
        if (child.get(node)[bit] == -1) {
            child.get(node)[bit] = child.size();
            child.add(new int[]{-1, -1});
            count.add(0);
        }
        node = child.get(node)[bit];
        count.set(node, count.get(node) + 1);
    }
}
void eraseValue(List<int[]> child, List<Integer> count, int value) {
    int node = 0;
    count.set(0, count.get(0) - 1);
    for (int b = 16; b >= 0; b--) {
        node = child.get(node)[(value >> b) & 1];
        count.set(node, count.get(node) - 1);
    }
}
int bestXor(List<int[]> child, List<Integer> count, int value) {
    int node = 0, best = 0;
    for (int b = 16; b >= 0; b--) {
        int bit = (value >> b) & 1;
        int opposite = child.get(node)[bit ^ 1];
        if (opposite != -1 && count.get(opposite) > 0) {  // a live value differs here
            best |= 1 << b;
            node = opposite;
        } else {
            node = child.get(node)[bit];
        }
    }
    return best;
}
int maximumStrongPairXor(int[] nums) {
    Arrays.sort(nums);
    List<int[]> child = new ArrayList<>();
    List<Integer> count = new ArrayList<>();
    child.add(new int[]{-1, -1});
    count.add(0);
    int left = 0, best = 0;
    for (int value : nums) {
        while (nums[left] * 2L < value) eraseValue(child, count, nums[left++]);
        best = Math.max(best, bestXor(child, count, value));   // live window
        insertValue(child, count, value);
    }
    return best;
}   // O(n · 17) time · O(n · 17) space""",
            "python": r"""def maximum_strong_pair_xor(nums):
    nums.sort()
    child = [[-1, -1]]                 # trie with counts, so values can leave
    count = [0]

    def insert(value):
        node = 0
        count[0] += 1
        for b in range(16, -1, -1):
            bit = value >> b & 1
            if child[node][bit] == -1:
                child[node][bit] = len(child)
                child.append([-1, -1])
                count.append(0)
            node = child[node][bit]
            count[node] += 1

    def erase(value):
        node = 0
        count[0] -= 1
        for b in range(16, -1, -1):
            node = child[node][value >> b & 1]
            count[node] -= 1

    def best_xor(value):
        node = best = 0
        for b in range(16, -1, -1):
            bit = value >> b & 1
            opposite = child[node][bit ^ 1]
            if opposite != -1 and count[opposite] > 0:   # a live value differs here
                best |= 1 << b
                node = opposite
            else:
                node = child[node][bit]
        return best

    left, best = 0, 0
    for value in nums:
        while nums[left] * 2 < value:  # max <= 2 · min is the strong-pair rule
            erase(nums[left])
            left += 1
        best = max(best, best_xor(value))   # against the live window
        insert(value)
    return best""",
        },
    },
    {
        "slug": "smallest-good-base",
        "title": "Smallest Good Base",
        "difficulty": "Hard",
        "pattern": "binary search on the base",
        "statement": "n is given as a string. Return, as a string, the smallest base b >= 2 in which n is written with only 1 digits.",
        "examples": [("n = \"13\"", "\"3\""), ("n = \"4681\"", "\"8\""), ("n = \"1000000000000000000\"", "\"999999999999999999\"")],
        "constraints": ["3 <= n <= 10^18", "n has no leading zeros", "the answer is returned as a string"],
        "approach": "Fix the number of digits d first: then n = 1 + b + … + b^(d-1) increases with b, so a binary search finds the only possible base, and "
                     "the sum is capped early to avoid overflow. Base n - 1 always works because n writes as \"11\" there, and trying every d up to 62 "
                     "covers all remaining cases — the answer is the smallest base found.",
        "complexity": ("O(62 · 62 · log n) time", "O(1)"),
        "code": {
            "cpp": r"""// For each digit count the base is unique: binary search it, keep the smallest
long long allOnes(long long base, int digits, long long cap) {
    long long value = 1, term = 1;
    for (int i = 1; i < digits; i++) {
        if (term > cap / base) return cap + 1;          // already too large
        term *= base;
        value += term;
        if (value > cap) return cap + 1;
    }
    return value;
}
string smallestGoodBase(string n) {
    long long target = stoll(n);
    long long best = target - 1;                        // "11" in base n - 1
    for (int digits = 3; digits <= 62; digits++) {
        long long lo = 2, hi = target - 1;
        while (lo <= hi) {
            long long mid = lo + (hi - lo) / 2;
            long long value = allOnes(mid, digits, target);
            if (value == target) { best = min(best, mid); break; }
            if (value > target) hi = mid - 1;
            else lo = mid + 1;
        }
    }
    return to_string(best);
}   // O(62 · 62 · log n) time · O(1) space""",
            "java": r"""// For each digit count the base is unique: binary search it, keep the smallest
long allOnes(long base, int digits, long cap) {
    long value = 1, term = 1;
    for (int i = 1; i < digits; i++) {
        if (term > cap / base) return cap + 1;          // already too large
        term *= base;
        value += term;
        if (value > cap) return cap + 1;
    }
    return value;
}
String smallestGoodBase(String n) {
    long target = Long.parseLong(n);
    long best = target - 1;                             // "11" in base n - 1
    for (int digits = 3; digits <= 62; digits++) {
        long lo = 2, hi = target - 1;
        while (lo <= hi) {
            long mid = lo + (hi - lo) / 2;
            long value = allOnes(mid, digits, target);
            if (value == target) { best = Math.min(best, mid); break; }
            if (value > target) hi = mid - 1;
            else lo = mid + 1;
        }
    }
    return Long.toString(best);
}   // O(62 · 62 · log n) time · O(1) space""",
            "python": r"""def smallest_good_base(n):
    target = int(n)
    best = target - 1                      # n is "11" in base n - 1

    def all_ones(base, digits):
        value = term = 1
        for _ in range(digits - 1):
            term *= base
            value += term
            if value > target:
                return value                   # already past the target
        return value

    for digits in range(3, 63):            # a longer run of 1s needs a smaller base
        lo, hi = 2, target - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            value = all_ones(mid, digits)
            if value == target:
                best = min(best, mid)
                break
            if value > target:
                hi = mid - 1
            else:
                lo = mid + 1
    return str(best)""",
        },
    },
    {
        "slug": "partition-array-into-two-arrays-to-minimize-sum-difference",
        "title": "Partition Array Into Two Arrays to Minimize Sum Difference",
        "difficulty": "Hard",
        "pattern": "meet in the middle over subsets",
        "statement": "Split nums, which has 2n elements, into two arrays of n elements each so that the absolute difference of their sums is as small "
                     "as possible. Return that minimum difference.",
        "examples": [("nums = [3,9,7,3]", "2"), ("nums = [-36,36]", "72"), ("nums = [2,-1,0,4,-2,-9]", "0")],
        "constraints": ["1 <= nums.length <= 30", "nums.length is even", "-10^7 <= nums[i] <= 10^7"],
        "approach": "Enumerating all assignments is 2^30, so split the array in half: 2^15 subsets per half, each recorded as (count, sum) and grouped "
                     "by count. A choice must take exactly n elements overall, so a left group of size k pairs only with the right group of size n - k. "
                     "Sorting each right group and binary searching for the complement of the target sum makes the join fast.",
        "complexity": ("O(2^(n/2) · n) time", "O(2^(n/2))"),
        "code": {
            "cpp": r"""// Enumerate subsets of each half, then match counts and nearest sums
int minimumDifference(vector<int>& nums) {
    int n = nums.size() / 2;                  // each side of the split takes n
    long long total = 0;
    for (int x : nums) total += x;
    vector<vector<long long>> left(n + 1), right(n + 1);
    for (int mask = 0; mask < (1 << n); mask++) {          // first n elements
        long long sum = 0;
        for (int i = 0; i < n; i++) if ((mask >> i) & 1) sum += nums[i];
        left[__builtin_popcount(mask)].push_back(sum);
    }
    for (int mask = 0; mask < (1 << n); mask++) {          // last n elements
        long long sum = 0;
        for (int i = 0; i < n; i++) if ((mask >> i) & 1) sum += nums[n + i];
        right[__builtin_popcount(mask)].push_back(sum);
    }
    for (auto& group : right) sort(group.begin(), group.end());
    long long best = LLONG_MAX;
    for (int k = 0; k <= n; k++) {
        const vector<long long>& pool = right[n - k];      // counts must add to n
        for (long long s : left[k]) {
            auto it = lower_bound(pool.begin(), pool.end(), total / 2 - s);
            if (it != pool.end()) best = min(best, llabs(total - 2 * (s + *it)));
            if (it != pool.begin()) best = min(best, llabs(total - 2 * (s + *(it - 1))));
        }
    }
    return (int) best;
}   // O(2^(n/2) · n) time · O(2^(n/2)) space""",
            "java": r"""// Enumerate subsets of each half, then match counts and nearest sums
int minimumDifference(int[] nums) {
    int n = nums.length / 2;                  // each side of the split takes n
    long total = 0;
    for (int x : nums) total += x;
    List<List<Long>> left = new ArrayList<>(), right = new ArrayList<>();
    for (int k = 0; k <= n; k++) { left.add(new ArrayList<>()); right.add(new ArrayList<>()); }
    for (int mask = 0; mask < (1 << n); mask++) {          // first n elements
        long sum = 0;
        for (int i = 0; i < n; i++) if (((mask >> i) & 1) == 1) sum += nums[i];
        left.get(Integer.bitCount(mask)).add(sum);
    }
    for (int mask = 0; mask < (1 << n); mask++) {          // last n elements
        long sum = 0;
        for (int i = 0; i < n; i++) if (((mask >> i) & 1) == 1) sum += nums[n + i];
        right.get(Integer.bitCount(mask)).add(sum);
    }
    for (List<Long> group : right) Collections.sort(group);
    long best = Long.MAX_VALUE;
    for (int k = 0; k <= n; k++) {
        List<Long> pool = right.get(n - k);                // counts must add to n
        for (long s : left.get(k)) {
            int pos = Collections.binarySearch(pool, total / 2 - s);
            if (pos < 0) pos = -pos - 1;
            if (pos < pool.size()) best = Math.min(best, Math.abs(total - 2 * (s + pool.get(pos))));
            if (pos > 0) best = Math.min(best, Math.abs(total - 2 * (s + pool.get(pos - 1))));
        }
    }
    return (int) best;
}   // O(2^(n/2) · n) time · O(2^(n/2)) space""",
            "python": r"""def minimum_difference(nums):
    n = len(nums) // 2                       # each side of the split takes n
    total = sum(nums)
    left = [[] for _ in range(n + 1)]
    right = [[] for _ in range(n + 1)]
    for half, groups in ((nums[:n], left), (nums[n:], right)):
        sums = [0] * (1 << n)
        for mask in range(1, 1 << n):
            low = mask & -mask                # add one element to a known subset
            sums[mask] = sums[mask ^ low] + half[low.bit_length() - 1]
            groups[bin(mask).count("1")].append(sums[mask])
        groups[0].append(0)
    for group in right:
        group.sort()
    best = float("inf")
    for k in range(n + 1):
        pool = right[n - k]                   # counts on both sides add up to n
        for s in left[k]:
            pos = bisect_left(pool, total // 2 - s)
            if pos < len(pool):
                best = min(best, abs(total - 2 * (s + pool[pos])))
            if pos > 0:
                best = min(best, abs(total - 2 * (s + pool[pos - 1])))
    return int(best)""",
        },
    },
]
