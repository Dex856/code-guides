# Topic 15 · Math & Number Theory — C17 solutions
#
# Digit by digit, and long long wherever two ints multiply — that one habit removes most
# overflow bugs. Modular arithmetic appears whenever the answer is "count mod 1e9+7".

CODE = {
    "palindrome-number": r"""
// Reversing the number is the direct test (negative numbers are never palindromes).
int isPalindrome(int x) {
    if (x < 0) return 0;
    long long reversed = 0;
    for (int value = x; value; value /= 10) reversed = reversed * 10 + value % 10;
    return reversed == x;
}   // O(digits) time · O(1) space
""",
    "plus-one": r"""
// Carry from the last digit; if everything carries, the array grows by one.
int *plusOne(int *digits, int n, int *returnSize) {
    for (int i = n - 1; i >= 0; i--) {
        if (digits[i] < 9) { digits[i]++; *returnSize = n; return digits; }
        digits[i] = 0;                                      // this digit carries
    }
    int *out = malloc(sizeof(int) * (size_t) (n + 1));
    out[0] = 1;
    for (int i = 0; i < n; i++) out[i + 1] = 0;
    *returnSize = n + 1;
    return out;
}   // O(n) time · O(1) extra space
""",
    "excel-sheet-column-title": r"""
// A bijective base-26 system: subtract one before taking each digit.
char *convertToTitle(int columnNumber) {
    char *out = malloc(16);
    int length = 0;
    while (columnNumber) {
        columnNumber--;                                     // 1 becomes 'A', 26 becomes 'Z'
        out[length++] = (char) ('A' + columnNumber % 26);
        columnNumber /= 26;
    }
    for (int i = 0; i < length / 2; i++) {
        char t = out[i]; out[i] = out[length - 1 - i]; out[length - 1 - i] = t;
    }
    out[length] = '\0';
    return out;
}   // O(log n) time · O(1) space
""",
    "add-digits": r"""
// The digital root: repeated digit sums land on n % 9, with 9 instead of 0.
int addDigits(int num) {
    if (num == 0) return 0;
    return 1 + (num - 1) % 9;
}   // O(1) time · O(1) space
""",
    "add-binary": r"""
// Add from the least significant bit, carrying as usual.
char *addBinary(const char *a, const char *b) {
    int n = (int) strlen(a), m = (int) strlen(b), size = (n > m ? n : m) + 2;
    char *out = malloc((size_t) size);
    int i = n - 1, j = m - 1, k = size - 1, carry = 0;
    out[k--] = '\0';
    while (i >= 0 || j >= 0 || carry) {
        int sum = carry;
        if (i >= 0) sum += a[i--] - '0';
        if (j >= 0) sum += b[j--] - '0';
        out[k--] = (char) ('0' + sum % 2);
        carry = sum / 2;
    }
    return out + k + 1;                                     // skip the unused front space
}   // O(n + m) time · O(n + m) space
""",
    "happy-number": r"""
// Floyd's cycle detection on the digit-square sum: happy numbers reach 1.
int squareSum(int n) {
    int total = 0;
    while (n) { int d = n % 10; total += d * d; n /= 10; }
    return total;
}

int isHappy(int n) {
    int slow = n, fast = squareSum(n);
    while (fast != 1 && slow != fast) {
        slow = squareSum(slow);
        fast = squareSum(squareSum(fast));                 // twice as fast
    }
    return fast == 1;
}   // O(log n) time · O(1) space
""",
    "reverse-integer": r"""
// Build the reversed number in long long and clamp to the 32-bit range.
int reverse(int x) {
    long long reversed = 0;
    while (x) {
        reversed = reversed * 10 + x % 10;
        x /= 10;
        if (reversed > INT_MAX || reversed < INT_MIN) return 0;
    }
    return (int) reversed;
}   // O(digits) time · O(1) space
""",
    "count-primes": r"""
// Sieve of Eratosthenes: mark the multiples of every prime found.
int countPrimes(int n) {
    if (n < 3) return 0;
    char *composite = calloc((size_t) n, 1);
    int count = 0;
    for (int i = 2; i < n; i++) {
        if (composite[i]) continue;
        count++;
        for (long long j = (long long) i * i; j < n; j += i) composite[j] = 1;
    }
    free(composite);
    return count;
}   // O(n log log n) time · O(n) space
""",
    "factorial-trailing-zeroes": r"""
// Zeros come from factors of 5: n/5 + n/25 + n/125 + …
int trailingZeroes(int n) {
    long long count = 0;
    for (long long power = 5; power <= n; power *= 5) count += n / power;
    return (int) count;
}   // O(log n) time · O(1) space
""",
    "nth-digit": r"""
// Walk the blocks of 1-, 2-, 3-digit numbers, then index into the block.
int findNthDigit(int n) {
    long long digits = 1, count = 9, start = 1;
    while (n > digits * count) {                            // skip a whole block
        n -= (int) (digits * count);
        digits++;
        count *= 10;
        start *= 10;
    }
    long long number = start + (n - 1) / digits;            // which number holds the digit
    int index = (int) ((n - 1) % digits);                   // and which digit of it
    for (int i = 0; i < digits - 1 - index; i++) number /= 10;
    return (int) (number % 10);
}   // O(log n) time · O(1) space
""",
    "powx-n": r"""
// Fast exponentiation by squaring; the exponent is a long long because it can be INT_MIN.
double myPow(double x, long long n) {
    if (n < 0) { x = 1 / x; n = -n; }
    double result = 1;
    while (n) {
        if (n & 1) result *= x;                             // use this power of two
        x *= x;
        n >>= 1;
    }
    return result;
}   // O(log n) time · O(1) space
""",
    "multiply-strings": r"""
// Grade-school multiplication into a digit array, then trim the leading zeros.
char *multiply(const char *num1, const char *num2) {
    int n = (int) strlen(num1), m = (int) strlen(num2);
    int *digits = calloc((size_t) (n + m), sizeof(int));
    for (int i = n - 1; i >= 0; i--)
        for (int j = m - 1; j >= 0; j--) {
            int product = (num1[i] - '0') * (num2[j] - '0') + digits[i + j + 1];
            digits[i + j + 1] = product % 10;               // the digit
            digits[i + j] += product / 10;                  // the carry
        }
    int start = 0;
    while (start < n + m - 1 && !digits[start]) start++;    // skip leading zeros
    char *out = malloc((size_t) (n + m - start) + 1);
    int length = 0;
    for (int i = start; i < n + m; i++) out[length++] = (char) ('0' + digits[i]);
    out[length] = '\0';
    free(digits);
    return out;
}   // O(n * m) time · O(n + m) space
""",
    "integer-break": r"""
// Break into 3s; only the remainder of 1 is special (use 4 = 2 + 2 instead).
int integerBreak(int n) {
    if (n <= 3) return n - 1;
    long long product = 1;
    int remainder = n % 3;
    int threes = n / 3;
    if (remainder == 1) { threes--; product = 4; }          // a 3 + 1 is worse than 2 + 2
    else if (remainder == 2) product = 2;
    while (threes--) product *= 3;
    return (int) product;
}   // O(n) time · O(1) space
""",
    "sum-of-square-numbers": r"""
// Two pointers over the squares below c.
int judgeSquareSum(int c) {
    long long low = 0, high = (long long) sqrt((double) c);
    while (low <= high) {
        long long sum = low * low + high * high;
        if (sum == c) return 1;
        if (sum < c) low++;
        else high--;
    }
    return 0;
}   // O(sqrt(c)) time · O(1) space
""",
    "angle-between-hands-of-a-clock": r"""
// The hour hand moves 0.5 degrees per minute, the minute hand 6.
double angleClock(int hour, int minutes) {
    double hourAngle = (hour % 12) * 30.0 + minutes * 0.5;
    double minuteAngle = minutes * 6.0;
    double difference = fabs(hourAngle - minuteAngle);
    return difference > 180 ? 360 - difference : difference;
}   // O(1) time · O(1) space
""",
    "smallest-integer-divisible-by-k": r"""
// Keep the remainder only: rem = (rem * 10 + 1) % k, and stop when it repeats.
int smallestRepunitDivByK(int k) {
    if (k % 2 == 0 || k % 5 == 0) return -1;                // never divisible by 2 or 5
    int remainder = 0;
    for (int length = 1; length <= k; length++) {
        remainder = (remainder * 10 + 1) % k;               // one more 1 digit
        if (remainder == 0) return length;
    }
    return -1;
}   // O(k) time · O(1) space
""",
    "fraction-to-recurring-decimal": r"""
// Long division with a "seen remainder → position" table to spot the cycle.
char *fractionToDecimal(long long numerator, long long denominator) {
    if (!numerator) return strdup("0");
    char *out = malloc(8192);
    int length = 0;
    if ((numerator < 0) != (denominator < 0)) out[length++] = '-';
    long long a = llabs(numerator), b = llabs(denominator);
    length += snprintf(out + length, 32, "%lld", a / b);
    long long remainder = a % b;
    if (remainder) {
        out[length++] = '.';
        int *seen = malloc(sizeof(int) * 65536);
        for (int i = 0; i < 65536; i++) seen[i] = -1;
        while (remainder && seen[remainder] < 0) {
            seen[remainder] = length;                       // remember where this remainder started
            remainder *= 10;
            out[length++] = (char) ('0' + remainder / b);
            remainder %= b;
        }
        if (remainder) {                                    // the cycle repeats: wrap it in ()
            int startPosition = seen[remainder];
            for (int i = length; i > startPosition; i--) out[i] = out[i - 1];
            out[startPosition] = '(';
            out[++length] = ')';
            length++;
        }
        free(seen);
    }
    out[length] = '\0';
    return out;
}   // O(denominator) time · O(denominator) space
""",
    "super-pow": r"""
// a^b mod 1337: reduce the exponent with Euler's theorem, handling the +1337 case.
int superPow(int a, const int *b, int n) {
    int exponent = 0;
    for (int i = 0; i < n; i++) exponent = (exponent * 10 + b[i]) % 1140;   // phi(1337) = 1140
    if (exponent == 0 && n) exponent = 1140;                // only when b was a multiple of 1140
    long long result = 1, base = a % 1337;
    while (exponent) {
        if (exponent & 1) result = result * base % 1337;
        base = base * base % 1337;
        exponent >>= 1;
    }
    return (int) result;
}   // O(n + log 1140) time · O(1) space
""",
    "number-of-digit-one": r"""
// Count the 1s contributed by each decimal position.
int countDigitOne(int n) {
    long long total = 0;
    for (long long place = 1; place <= n; place *= 10) {
        long long high = n / (place * 10), current = n / place % 10, low = n % place;
        total += high * place;                              // full cycles of the digit
        if (current > 1) total += place;                    // one extra full block
        else if (current == 1) total += low + 1;            // the partial block
    }
    return (int) total;
}   // O(digits) time · O(1) space
""",
    "integer-to-english-words": r"""
// Peel off groups of three digits and name each group.
static const char *ONES[] = {"", "One", "Two", "Three", "Four", "Five", "Six", "Seven",
                             "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen",
                             "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"};
static const char *TENS[] = {"", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty",
                             "Seventy", "Eighty", "Ninety"};
static const char *SCALES[] = {"", " Thousand", " Million", " Billion"};

static void appendGroup(int value, char *out) {
    if (value >= 100) {
        strcat(out, ONES[value / 100]);
        strcat(out, " Hundred");
        value %= 100;
        if (value) strcat(out, " ");
    }
    if (value >= 20) {
        strcat(out, TENS[value / 10]);
        if (value % 10) { strcat(out, " "); strcat(out, ONES[value % 10]); }
    } else if (value) {
        strcat(out, ONES[value]);
    }
}

char *numberToWords(int num) {
    if (!num) return strdup("Zero");
    char *out = calloc(1024, 1);
    int groups[4] = {0}, count = 0;
    for (int value = num; value && count < 4; value /= 1000) groups[count++] = value % 1000;
    for (int i = count - 1; i >= 0; i--) {
        if (!groups[i]) continue;
        if (out[0]) strcat(out, " ");
        appendGroup(groups[i], out);
        strcat(out, SCALES[i]);
    }
    return out;
}   // O(digits) time · O(1) space
""",
    "permutation-sequence": r"""
// Pick each digit by dividing the remaining permutations into blocks of (n-1)!.
char *getPermutation(int n, int k) {
    int factorial[10];
    factorial[0] = 1;
    for (int i = 1; i < 10; i++) factorial[i] = factorial[i - 1] * i;
    int available[9];
    for (int i = 0; i < n; i++) available[i] = i + 1;
    char *out = malloc((size_t) n + 1);
    k--;                                                    // work with a 0-based rank
    int remaining = n;
    for (int i = 0; i < n; i++) {
        int block = factorial[remaining - 1];
        int index = k / block;                              // which digit comes next
        out[i] = (char) ('0' + available[index]);
        for (int j = index; j < remaining - 1; j++) available[j] = available[j + 1];
        k %= block;
        remaining--;
    }
    out[n] = '\0';
    return out;
}   // O(n^2) time · O(n) space
""",
    "numbers-at-most-n-given-digit-set": r"""
// Count numbers of every shorter length, then walk the bound digit by digit.
int atMostNGivenDigitSet(char **digits, int digitCount, int n) {
    char bound[16];
    snprintf(bound, sizeof bound, "%d", n);
    int length = (int) strlen(bound);
    long long total = 0;
    for (int shorter = 1; shorter < length; shorter++) {     // every shorter number counts
        long long count = 1;
        for (int i = 0; i < shorter; i++) count *= digitCount;
        total += count;
    }
    for (int i = 0; i < length; i++) {
        int smaller = 0, equal = 0;
        for (int d = 0; d < digitCount; d++) {
            if (digits[d][0] < bound[i]) smaller++;
            if (digits[d][0] == bound[i]) equal = 1;
        }
        long long count = smaller;
        for (int rest = i + 1; rest < length; rest++) count *= digitCount;   // free choices after
        total += count;
        if (!equal) return (int) total;                      // the prefix diverged: stop here
    }
    return (int) total + 1;                                  // the bound itself is buildable
}   // O(length * digits) time · O(1) space
""",
    "sum-of-floored-pairs": r"""
// Count how many quotients of each value appear, then sum value * count * floor(...).
int sumOfFlooredPairs(int *nums, int n) {
    const long long MOD = 1000000007;
    int maximum = 0;
    for (int i = 0; i < n; i++) if (nums[i] > maximum) maximum = nums[i];
    long long *count = calloc((size_t) maximum + 2, sizeof(long long));
    for (int i = 0; i < n; i++) count[nums[i]]++;
    for (int v = 1; v <= maximum; v++) count[v] += count[v - 1];     // prefix sums of counts
    long long total = 0;
    for (int v = 1; v <= maximum; v++) {
        if (count[v] == count[v - 1]) continue;              // v does not appear
        long long occurrences = count[v] - count[v - 1];
        for (long long multiple = v; multiple <= maximum; multiple += v) {
            long long upper = count[(int) (multiple + v - 1 < maximum ? multiple + v - 1 : maximum)]
                            - count[multiple - 1];
            total = (total + occurrences * (multiple / v) % MOD * upper) % MOD;
        }
    }
    free(count);
    return (int) (total % MOD);
}   // O(maximum log maximum) time · O(maximum) space
""",
    "reaching-points": r"""
// Walk backwards: the larger coordinate must have been the sum of the two.
int reachingPoints(int sx, int sy, int tx, int ty) {
    while (tx >= sx && ty >= sy) {
        if (tx == sx && ty == sy) return 1;
        if (tx > ty) {
            if (!ty) break;
            long long steps = (tx - sx) / ty;                // jump many steps at once
            if (steps == 0) break;
            tx -= (int) (steps * ty);
        } else {
            if (!tx) break;
            long long steps = (ty - sy) / tx;
            if (steps == 0) break;
            ty -= (int) (steps * tx);
        }
    }
    return 0;
}   // O(log max) time · O(1) space
""",
    "count-ways-to-make-array-with-product": r"""
// Factorise k into at most n parts; each factor position can take any prime power.
int *waysToFillArray(int **queries, int queryCount, int *returnSize) {
    const long long MOD = 1000000007;
    /* factorials for the stars-and-bars binomials */
    long long factorial[10001];
    factorial[0] = 1;
    for (int i = 1; i <= 10000; i++) factorial[i] = factorial[i - 1] * i % MOD;
    int *out = malloc(sizeof(int) * (size_t) queryCount);
    for (int q = 0; q < queryCount; q++) {
        int n = queries[q][0], k = queries[q][1];
        long long ways = 1;
        for (int prime = 2; (long long) prime * prime <= k; prime++) {
            if (k % prime) continue;
            int exponent = 0;
            while (k % prime == 0) { k /= prime; exponent++; }
            /* choose where the prime's power goes among n slots: C(exponent + n - 1, exponent) */
            long long binomial = 1;
            for (int i = 1; i <= exponent; i++)
                binomial = binomial * (n - 1 + i) % MOD * factorial[i] % MOD;   // exact enough here
            for (int i = 1; i <= exponent; i++) binomial = binomial * i % MOD;
            ways = ways * binomial % MOD;
        }
        if (k > 1) ways = ways * n % MOD;                    // one leftover prime factor
        out[q] = (int) ways;
    }
    *returnSize = queryCount;
    return out;
}   // O(queries * sqrt(k)) time · O(1) extra space
""",
    "sum-of-k-mirror-numbers": r"""
// Generate palindromes in base 10 and base k, and add those that are mirrors in both.
static long long mirror(long long half, int oddLength) {
    long long value = half, rest = oddLength ? half / 10 : half;   // drop the middle digit
    while (rest) { value = value * 10 + rest % 10; rest /= 10; }
    return value;
}

static int isMirror(long long value, int base) {
    long long reversed = 0, original = value;
    while (value) { reversed = reversed * base + value % base; value /= base; }
    return reversed == original;
}

long long kMirror(int k, int n) {
    long long total = 0;
    int found = 0;
    for (int length = 1; found < n; length++) {
        for (long long half = 1; found < n; half++) {
            long long candidate = mirror(half, length % 2);
            int digits = 0;
            for (long long v = candidate; v; v /= 10) digits++;
            if (digits != length) break;                     // left the block of this length
            if (isMirror(candidate, k)) {
                total += candidate;
                found++;
            }
            if (half > 1000000000) break;                    // far past any needed answer
        }
    }
    return total;
}   // O(n log n) time · O(1) space
""",
    "count-the-number-of-ideal-arrays": r"""
// An ideal array is a chain of divisors: count chains of length n ending at each value.
int idealArrays(int n, int maxValue) {
    const long long MOD = 1000000007;
    long long **ways = malloc(sizeof(long long *) * (size_t) (maxValue + 1));
    for (int v = 0; v <= maxValue; v++) ways[v] = calloc((size_t) n + 1, sizeof(long long));
    for (int v = 1; v <= maxValue; v++) ways[v][1] = 1;      // length 1: the value itself
    for (int length = 2; length <= n; length++)
        for (int v = 1; v <= maxValue; v++)
            for (int multiple = 2 * v; multiple <= maxValue; multiple += v)   // v divides multiple
                ways[multiple][length] = (ways[multiple][length] + ways[v][length - 1]) % MOD;
    long long total = 0;
    for (int v = 1; v <= maxValue; v++)
        for (int length = 1; length <= n; length++) total = (total + ways[v][length]) % MOD;
    for (int v = 0; v <= maxValue; v++) free(ways[v]);
    free(ways);
    return (int) total;
}   // O(n * maxValue log maxValue) time · O(n * maxValue) space
""",
    "number-of-ways-to-reorder-array-to-get-same-bst": r"""
// The first element is the root; the left/right sizes are fixed, so the count is
// C(left + right, left) times the two subtrees' counts.
static long long factorial[1001], inverseFactorial[1001];

static long long power(long long base, long long exponent, long long mod) {
    long long result = 1;
    while (exponent) {
        if (exponent & 1) result = result * base % mod;
        base = base * base % mod;
        exponent >>= 1;
    }
    return result;
}

static long long combinations(int n, int r, long long mod) {
    if (r > n) return 0;
    return factorial[n] * inverseFactorial[r] % mod * inverseFactorial[n - r] % mod;
}

static long long countFrom(int *a, int n, long long mod) {
    if (n <= 2) return 1;
    int *left = malloc(sizeof(int) * (size_t) n), *right = malloc(sizeof(int) * (size_t) n);
    int leftCount = 0, rightCount = 0;
    for (int i = 1; i < n; i++) {
        if (a[i] < a[0]) left[leftCount++] = a[i];
        else right[rightCount++] = a[i];
    }
    long long ways = combinations(n - 1, leftCount, mod);
    ways = ways * countFrom(left, leftCount, mod) % mod;
    ways = ways * countFrom(right, rightCount, mod) % mod;
    free(left); free(right);
    return ways;
}

int numOfWays(int *nums, int n) {
    const long long MOD = 1000000007;
    factorial[0] = 1;
    for (int i = 1; i <= 1000; i++) factorial[i] = factorial[i - 1] * i % MOD;
    inverseFactorial[1000] = power(factorial[1000], MOD - 2, MOD);
    for (int i = 1000; i > 0; i--) inverseFactorial[i - 1] = inverseFactorial[i] * i % MOD;
    return (int) ((countFrom(nums, n, MOD) - 1 + MOD) % MOD);   // minus the original order
}   // O(n^2) time · O(n) recursion
""",
    "count-of-integers": r"""
// Digit DP: count numbers up to a bound whose digit sum is inside [minSum, maxSum],
// then answer = (up to num2) - (up to num1 - 1).
static long long countUpTo(const char *limit, int minSum, int maxSum) {
    const long long MOD = 1000000007;
    int n = (int) strlen(limit);
    long long *less = calloc((size_t) maxSum + 1, sizeof(long long));   // already below the bound
    long long tightCount = 1;                               // equal to the bound so far
    int tightSum = 0;
    less[0] = 1;
    for (int i = 0; i < n; i++) {
        long long *next = calloc((size_t) maxSum + 1, sizeof(long long));
        for (int sum = 0; sum <= maxSum; sum++) {
            if (!less[sum]) continue;
            for (int digit = 0; digit <= 9 && sum + digit <= maxSum; digit++)
                next[sum + digit] = (next[sum + digit] + less[sum]) % MOD;
        }
        if (tightCount) {
            int highest = limit[i] - '0';
            for (int digit = 0; digit < highest && tightSum + digit <= maxSum; digit++)
                next[tightSum + digit] = (next[tightSum + digit] + 1) % MOD;
            if (tightSum + highest <= maxSum) tightSum += highest;
            else tightCount = 0;                            // the sum already overshot
        }
        free(less);
        less = next;
    }
    long long total = 0;
    for (int sum = minSum; sum <= maxSum; sum++) total = (total + less[sum]) % MOD;
    if (tightCount && tightSum >= minSum && tightSum <= maxSum) total = (total + 1) % MOD;
    free(less);
    return (total - 1 + MOD) % MOD;                         // zero is not a positive integer
}

int countOfIntegers(int num1, int num2, int minSum, int maxSum) {
    const long long MOD = 1000000007;
    char lower[16], upper[16];
    snprintf(upper, sizeof upper, "%d", num2);
    int below = num1 - 1;
    long long result = countUpTo(upper, minSum, maxSum);
    if (below >= 0) {
        snprintf(lower, sizeof lower, "%d", below);
        result = (result - countUpTo(lower, minSum, maxSum) + MOD) % MOD;
    }
    return (int) result;
}   // O(digits * maxSum * 10) time \u00b7 O(maxSum) space
""",
    "find-the-closest-palindrome": r"""
// The answer is a palindrome built from the first half (or its neighbours), or a
// 99\u2026/10\u20261 boundary value when the digit count has to change.
static long long mirrorHalf(long long half, int odd) {
    long long value = half, rest = odd ? half / 10 : half;
    while (rest) { value = value * 10 + rest % 10; rest /= 10; }
    return value;
}

static int digitsOf(long long value) {
    int digits = 0;
    for (; value; value /= 10) digits++;
    return digits;
}

static long long powerOfTen[19];

char *nearestPalindromic(const char *n) {
    long long value = strtoll(n, NULL, 10);
    int length = (int) strlen(n);
    int halfLength = (length + 1) / 2;
    long long prefix = value;
    for (int i = halfLength; i < length; i++) prefix /= 10;   // the first half of the digits
    powerOfTen[0] = 1;
    for (int i = 1; i < 19; i++) powerOfTen[i] = powerOfTen[i - 1] * 10;
    long long best = -1;
    for (int delta = -1; delta <= 1; delta++) {
        long long half = prefix + delta;
        if (half <= 0) continue;
        long long candidate = mirrorHalf(half, length % 2);
        if (digitsOf(candidate) != length) continue;          // spilled into the next digit block
        if (candidate == value) continue;
        long long distance = llabs(candidate - value);
        if (best < 0 || distance < llabs(best - value) ||
            (distance == llabs(best - value) && candidate < best)) best = candidate;
    }
    for (int extra = length - 1; extra <= length; extra++) {  // 99\u2026 and 10\u20261
        long long candidates[2] = {powerOfTen[extra] - 1, powerOfTen[extra] + 1};
        for (int k = 0; k < 2; k++) {
            long long candidate = candidates[k];
            if (candidate == value || candidate < 0) continue;
            long long distance = llabs(candidate - value);
            if (best < 0 || distance < llabs(best - value) ||
                (distance == llabs(best - value) && candidate < best)) best = candidate;
        }
    }
    if (best < 0) best = 0;
    char *out = malloc(32);
    snprintf(out, 32, "%lld", best);
    return out;
}   // O(length) time \u00b7 O(1) space
""",
}

