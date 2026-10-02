# Topic 15 · Math & Number Theory
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.

TOPIC = {
    "name": "Math & Number Theory",
    "tagline": "Most number questions collapse into digits, primes or modular arithmetic — pick the right lens and the loop disappears.",
    "focus": "Four lenses cover this topic. Digit work reads a number place by place: peel with % 10, rebuild with * 10 + d, and remember that the "
             "column you are standing in has a weight (positions, carry, digital root). Prime work replaces trial division with a sieve or a smallest-"
             "prime-factor table, and turns \"how many\" into \"how many multiples of p\". Modular work keeps intermediate values small: subtract a "
             "remainder, exponentiate by squaring, and let a repeating remainder prove a cycle. Counting work asks how many objects satisfy a "
             "property — stars and bars for distributions, binomials for orderings, and digit DP when the bound is a number instead of a count.",
    "ordering": "easy 1–3 are digit reads (palindrome, carry, base-26), 4–6 are digit sums and binary addition; medium 1–4 are reversal, sieving, "
                "trailing zeros and the n-th digit, 5–8 fast power, grade-school multiplication, integer breakage and two squares, 9–12 are angles, "
                "remainder cycles, long division with repeating blocks and modular exponent towers; hard 1–4 count digits, spell numbers, rank "
                "permutations and run digit DP, 5–8 handle harmonic sums, reverse Euclidean geometry, stars-and-bars factorisations and palindrome "
                "enumeration, 9–12 compose prime exponents, count BST orderings, DP over digit sums with huge bounds and construct the nearest "
                "palindrome.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "palindrome-number",
        "title": "Palindrome Number",
        "difficulty": "Easy",
        "pattern": "reverse half of the digits",
        "statement": "Return true if the integer x reads the same forwards and backwards.",
        "examples": [("x = 121", "true"), ("x = -121", "false"), ("x = 10", "false")],
        "constraints": ["-2^31 <= x <= 2^31 - 1"],
        "approach": "Build the reversed number only until it catches up with what is left of x, then compare the two halves — that avoids both string "
                     "conversion and any risk of overflow. Two cases fall out early: negatives are never palindromes, and a positive number ending in 0 "
                     "cannot be one unless it is 0 itself. An odd number of digits leaves a middle digit in the reversed half, which is why the final "
                     "comparison also accepts rev / 10.",
        "complexity": ("O(number of digits) time", "O(1)"),
        "code": {
            "cpp": r"""// Reverse only the back half and compare the two halves
bool isPalindrome(int x) {
    if (x < 0 || (x % 10 == 0 && x != 0)) return false;   // 0 is the exception
    int reversed = 0;
    while (x > reversed) {
        reversed = reversed * 10 + x % 10;   // move one digit to the back half
        x /= 10;
    }
    return x == reversed || x == reversed / 10;   // the extra digit for odd lengths
}   // O(digits) time · O(1) space""",
            "java": r"""// Reverse only the back half and compare the two halves
boolean isPalindrome(int x) {
    if (x < 0 || (x % 10 == 0 && x != 0)) return false;   // 0 is the exception
    int reversed = 0;
    while (x > reversed) {
        reversed = reversed * 10 + x % 10;   // move one digit to the back half
        x /= 10;
    }
    return x == reversed || x == reversed / 10;   // the extra digit for odd lengths
}   // O(digits) time · O(1) space""",
            "python": r"""def is_palindrome(x):
    if x < 0 or (x % 10 == 0 and x != 0):
        return False                       # negatives and trailing zeros never work
    reversed_half = 0
    while x > reversed_half:
        reversed_half = reversed_half * 10 + x % 10
        x //= 10
    return x == reversed_half or x == reversed_half // 10""",
        },
    },
    {
        "slug": "plus-one",
        "title": "Plus One",
        "difficulty": "Easy",
        "pattern": "carry from the last digit",
        "statement": "digits holds the decimal digits of a non-negative integer, most significant first. Return the digits of that integer plus one.",
        "examples": [("digits = [1,2,3]", "[1,2,4]"), ("digits = [4,3,2,1]", "[4,3,2,2]"), ("digits = [9]", "[1,0]")],
        "constraints": ["1 <= digits.length <= 100", "0 <= digits[i] <= 9", "digits has no leading zeros except the number 0 itself"],
        "approach": "Walk from the last digit: anything below 9 can simply be increased, and that ends the carry. A 9 becomes 0 and passes the carry "
                     "left, so the loop either returns early or rewrites a run of nines. If every digit was a 9 the value gained a digit, which is the "
                     "only case needing a 1 pushed onto the front.",
        "complexity": ("O(n) time", "O(1) extra"),
        "code": {
            "cpp": r"""// Walk from the back: a digit below 9 ends the carry
vector<int> plusOne(vector<int>& digits) {
    for (int i = digits.size() - 1; i >= 0; i--) {
        if (digits[i] < 9) { digits[i]++; return digits; }   // no carry left
        digits[i] = 0;                                       // 9 becomes 0, carry on
    }
    digits.insert(digits.begin(), 1);                        // 99…9 became 100…0
    return digits;
}   // O(n) time · O(1) extra space""",
            "java": r"""// Walk from the back: a digit below 9 ends the carry
int[] plusOne(int[] digits) {
    for (int i = digits.length - 1; i >= 0; i--) {
        if (digits[i] < 9) { digits[i]++; return digits; }   // no carry left
        digits[i] = 0;                                       // 9 becomes 0, carry on
    }
    int[] grown = new int[digits.length + 1];                // 99…9 became 100…0
    grown[0] = 1;
    return grown;
}   // O(n) time · O(1) extra space""",
            "python": r"""def plus_one(digits):
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1              # the carry stops here
            return digits
        digits[i] = 0                    # a 9 becomes 0 and carries on
    return [1] + digits                  # 99…9 became 100…0""",
        },
    },
    {
        "slug": "excel-sheet-column-title",
        "title": "Excel Sheet Column Title",
        "difficulty": "Easy",
        "pattern": "bijective base-26",
        "statement": "Return the column title that corresponds to the positive integer columnNumber (1 -> \"A\", 26 -> \"Z\", 27 -> \"AA\").",
        "examples": [("columnNumber = 1", "\"A\""), ("columnNumber = 28", "\"AB\""), ("columnNumber = 701", "\"ZY\"")],
        "constraints": ["1 <= columnNumber <= 2^31 - 1"],
        "approach": "This is base 26 with a twist: there is no digit for zero, so the digits run 1…26 instead of 0…25. Subtracting one before taking the "
                     "remainder shifts the digit into 0…25 and makes ordinary division work — the same trick turns this into a loop as short as the "
                     "title itself.",
        "complexity": ("O(log n) time", "O(log n)"),
        "code": {
            "cpp": r"""// Base 26 without a zero digit: shift by one before dividing
string convertToTitle(int columnNumber) {
    string title;
    while (columnNumber > 0) {
        columnNumber--;                                   // 1…26 becomes 0…25
        title += char('A' + columnNumber % 26);
        columnNumber /= 26;
    }
    reverse(title.begin(), title.end());
    return title;
}   // O(log n) time · O(log n) space""",
            "java": r"""// Base 26 without a zero digit: shift by one before dividing
String convertToTitle(int columnNumber) {
    StringBuilder title = new StringBuilder();
    while (columnNumber > 0) {
        columnNumber--;                                   // 1…26 becomes 0…25
        title.append((char) ('A' + columnNumber % 26));
        columnNumber /= 26;
    }
    return title.reverse().toString();
}   // O(log n) time · O(log n) space""",
            "python": r"""def excel_title(column_number):
    title = []
    while column_number > 0:
        column_number -= 1                    # digits run 1…26, not 0…25
        title.append(chr(ord("A") + column_number % 26))
        column_number //= 26
    return "".join(reversed(title))""",
        },
    },
    {
        "slug": "add-digits",
        "title": "Add Digits",
        "difficulty": "Easy",
        "pattern": "digital root mod 9",
        "statement": "Repeatedly replace num with the sum of its digits until one digit remains, and return that digit. Do it without a loop.",
        "examples": [("num = 38", "2"), ("num = 0", "0")],
        "constraints": ["0 <= num <= 2^31 - 1"],
        "approach": "Summing digits is the same as reducing modulo 9, because 10 ≡ 1 (mod 9) at every place. The only mismatch is that ordinary remainders "
                     "run 0…8 while digital roots run 1…9, so shifting the input by one before the modulo and back again after it gives the answer in "
                     "constant time.",
        "complexity": ("O(1) time", "O(1)"),
        "code": {
            "cpp": r"""// Digit sums reduce mod 9, shifted so 9 stays reachable
int addDigits(int num) {
    if (num == 0) return 0;
    return 1 + (num - 1) % 9;                 // 0 stays 0, otherwise the digital root
}   // O(1) time · O(1) space""",
            "java": r"""// Digit sums reduce mod 9, shifted so 9 stays reachable
int addDigits(int num) {
    if (num == 0) return 0;
    return 1 + (num - 1) % 9;                 // 0 stays 0, otherwise the digital root
}   // O(1) time · O(1) space""",
            "python": r"""def add_digits(num):
    if num == 0:
        return 0
    return 1 + (num - 1) % 9       # the digital root: 10 ≡ 1 (mod 9) at every place""",
        },
    },
    {
        "slug": "add-binary",
        "title": "Add Binary",
        "difficulty": "Easy",
        "pattern": "carry over two strings",
        "statement": "Given two binary strings a and b, return their sum as a binary string.",
        "examples": [("a = \"11\", b = \"1\"", "\"100\""), ("a = \"1010\", b = \"1011\"", "\"10101\"")],
        "constraints": ["1 <= a.length, b.length <= 10^4", "a and b contain only '0' and '1' characters", "neither string has leading zeros except \"0\""],
        "approach": "Do the addition the way you would on paper: read both strings from the back, add the two bits plus the carry, write the sum bit and "
                     "carry the rest. A single loop that keeps going while either string or the carry has something left handles the different lengths "
                     "and the final carry without special cases.",
        "complexity": ("O(max(n, m)) time", "O(max(n, m))"),
        "code": {
            "cpp": r"""// Column-by-column addition with a carry
string addBinary(string a, string b) {
    string result;
    int i = a.size() - 1, j = b.size() - 1, carry = 0;
    while (i >= 0 || j >= 0 || carry) {
        int total = carry;
        if (i >= 0) total += a[i--] - '0';
        if (j >= 0) total += b[j--] - '0';
        result += char('0' + total % 2);      // this column's bit
        carry = total / 2;                    // and what moves left
    }
    reverse(result.begin(), result.end());
    return result;
}   // O(max(n, m)) time · O(max(n, m)) space""",
            "java": r"""// Column-by-column addition with a carry
String addBinary(String a, String b) {
    StringBuilder result = new StringBuilder();
    int i = a.length() - 1, j = b.length() - 1, carry = 0;
    while (i >= 0 || j >= 0 || carry != 0) {
        int total = carry;
        if (i >= 0) total += a.charAt(i--) - '0';
        if (j >= 0) total += b.charAt(j--) - '0';
        result.append((char) ('0' + total % 2));     // this column's bit
        carry = total / 2;                           // and what moves left
    }
    return result.reverse().toString();
}   // O(max(n, m)) time · O(max(n, m)) space""",
            "python": r"""def add_binary(a, b):
    result = []
    i, j, carry = len(a) - 1, len(b) - 1, 0
    while i >= 0 or j >= 0 or carry:
        total = carry
        if i >= 0:
            total += int(a[i])             # this column's bits
            i -= 1
        if j >= 0:
            total += int(b[j])
            j -= 1
        result.append(str(total % 2))      # write the bit
        carry = total // 2                 # carry what is left
    return "".join(reversed(result))""",
        },
    },
    {
        "slug": "happy-number",
        "title": "Happy Number",
        "difficulty": "Easy",
        "pattern": "digit-square map + cycle detection",
        "statement": "Starting from n, repeatedly replace the number with the sum of the squares of its digits. Return true if this reaches 1.",
        "examples": [("n = 19", "true"), ("n = 2", "false")],
        "constraints": ["1 <= n <= 2^31 - 1"],
        "approach": "The sequence is deterministic, so it either reaches 1 or repeats; an unhappy number always falls into the cycle 4 -> 16 -> 37 -> "
                     "58 -> 89 -> 145 -> 42 -> 20 -> 4. Remember the values seen and stop when a value repeats, which keeps the loop short and needs "
                     "no bound on how long the run can be.",
        "complexity": ("O(log n) per step, few steps", "O(1) (the cycle is tiny)"),
        "code": {
            "cpp": r"""// The sequence must fall into the 4-cycle if it is not happy
bool isHappy(int n) {
    unordered_set<int> seen;
    while (n != 1 && !seen.count(n)) {
        seen.insert(n);
        int next = 0;
        while (n > 0) {                       // sum of squared digits
            int digit = n % 10;
            next += digit * digit;
            n /= 10;
        }
        n = next;
    }
    return n == 1;
}   // O(log n) per step · O(1) space (the cycle is tiny)""",
            "java": r"""// The sequence must fall into the 4-cycle if it is not happy
boolean isHappy(int n) {
    Set<Integer> seen = new HashSet<>();
    while (n != 1 && !seen.contains(n)) {
        seen.add(n);
        int next = 0;
        while (n > 0) {                       // sum of squared digits
            int digit = n % 10;
            next += digit * digit;
            n /= 10;
        }
        n = next;
    }
    return n == 1;
}   // O(log n) per step · O(1) space (the cycle is tiny)""",
            "python": r"""def is_happy(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        total = 0
        while n > 0:                       # sum of squared digits
            digit = n % 10
            total += digit * digit
            n //= 10
        n = total
    return n == 1""",
        },
    },
    # ---------------------------------------------------------------- MEDIUM
    {
        "slug": "reverse-integer",
        "title": "Reverse Integer",
        "difficulty": "Medium",
        "pattern": "reverse digits with an overflow test",
        "statement": "Reverse the digits of the 32-bit signed integer x. Return 0 when the reversed value would leave the signed 32-bit range.",
        "examples": [("x = 123", "321"), ("x = -123", "-321"), ("x = 120", "21")],
        "constraints": ["-2^31 <= x <= 2^31 - 1", "the answer must fit in a signed 32-bit integer, otherwise return 0"],
        "approach": "Peel digits off with % 10 and push them onto the result with * 10 + digit. The only trap is overflow, and it can be checked before "
                     "it happens: if the result already exceeds (or undercuts) the last full power of ten, the next multiply is doomed. Testing the "
                     "bound first is what keeps the answer correct without widening the type.",
        "complexity": ("O(log x) time", "O(1)"),
        "code": {
            "cpp": r"""// Push digits onto the result, refusing to overflow
int reverse(int x) {
    int result = 0;
    while (x != 0) {
        int digit = x % 10;
        x /= 10;
        if (result > INT_MAX / 10 || (result == INT_MAX / 10 && digit > 7)) return 0;
        if (result < INT_MIN / 10 || (result == INT_MIN / 10 && digit < -8)) return 0;
        result = result * 10 + digit;
    }
    return result;
}   // O(log x) time · O(1) space""",
            "java": r"""// Push digits onto the result, refusing to overflow
int reverse(int x) {
    int result = 0;
    while (x != 0) {
        int digit = x % 10;
        x /= 10;
        if (result > Integer.MAX_VALUE / 10 || (result == Integer.MAX_VALUE / 10 && digit > 7)) return 0;
        if (result < Integer.MIN_VALUE / 10 || (result == Integer.MIN_VALUE / 10 && digit < -8)) return 0;
        result = result * 10 + digit;
    }
    return result;
}   // O(log x) time · O(1) space""",
            "python": r"""def reverse_integer(x):
    limit = 2**31 - 1
    sign = -1 if x < 0 else 1
    result = 0
    x = abs(x)
    while x:
        result = result * 10 + x % 10
        x //= 10
    result *= sign
    return result if -limit - 1 <= result <= limit else 0   # 32-bit bound""",
        },
    },
    {
        "slug": "count-primes",
        "title": "Count Primes",
        "difficulty": "Medium",
        "pattern": "sieve of Eratosthenes",
        "statement": "Return how many primes are strictly less than n.",
        "examples": [("n = 10", "4"), ("n = 0", "0"), ("n = 1", "0")],
        "constraints": ["0 <= n <= 5 · 10^6"],
        "approach": "Trial division would be far too slow, but a sieve is linear-ish: keep a flag per number, and each time you meet an unflagged value, "
                     "mark its multiples — they cannot be prime. Marking starts at p², since smaller multiples were already crossed off by smaller "
                     "primes, which is what keeps the total work near n log log n.",
        "complexity": ("O(n log log n) time", "O(n)"),
        "code": {
            "cpp": r"""// Sieve: crossing out multiples of each prime found
int countPrimes(int n) {
    if (n < 3) return 0;
    vector<bool> composite(n, false);
    int primes = 0;
    for (int p = 2; p < n; p++) {
        if (composite[p]) continue;
        primes++;
        if ((long long) p * p < n)                       // start at p²
            for (long long m = (long long) p * p; m < n; m += p) composite[m] = true;
    }
    return primes;
}   // O(n log log n) time · O(n) space""",
            "java": r"""// Sieve: crossing out multiples of each prime found
int countPrimes(int n) {
    if (n < 3) return 0;
    boolean[] composite = new boolean[n];
    int primes = 0;
    for (int p = 2; p < n; p++) {
        if (composite[p]) continue;
        primes++;
        if ((long) p * p < n)                            // start at p²
            for (long m = (long) p * p; m < n; m += p) composite[(int) m] = true;
    }
    return primes;
}   // O(n log log n) time · O(n) space""",
            "python": r"""def count_primes(n):
    if n < 3:
        return 0
    composite = [False] * n
    primes = 0
    for p in range(2, n):
        if composite[p]:
            continue
        primes += 1
        for m in range(p * p, n, p):       # smaller multiples were crossed already
            composite[m] = True
    return primes""",
        },
    },
    {
        "slug": "factorial-trailing-zeroes",
        "title": "Factorial Trailing Zeroes",
        "difficulty": "Medium",
        "pattern": "count factors of five",
        "statement": "Return the number of trailing zeroes in n!.",
        "examples": [("n = 3", "0"), ("n = 5", "1"), ("n = 0", "0")],
        "constraints": ["0 <= n <= 10^4"],
        "approach": "A trailing zero is a factor of ten, and tens come from pairing a two with a five; twos are everywhere, so fives are the bottleneck. "
                     "Counting multiples of 5, then of 25, of 125 and so on adds up the exponents of five in n! without ever building the factorial.",
        "complexity": ("O(log n) time", "O(1)"),
        "code": {
            "cpp": r"""// Zeros are limited by the exponent of 5 in n!
int trailingZeroes(int n) {
    int zeroes = 0;
    while (n > 0) {
        n /= 5;                              // 5, 25, 125, … all counted here
        zeroes += n;
    }
    return zeroes;
}   // O(log n) time · O(1) space""",
            "java": r"""// Zeros are limited by the exponent of 5 in n!
int trailingZeroes(int n) {
    int zeroes = 0;
    while (n > 0) {
        n /= 5;                              // 5, 25, 125, … all counted here
        zeroes += n;
    }
    return zeroes;
}   // O(log n) time · O(1) space""",
            "python": r"""def trailing_zeroes(n):
    zeroes = 0
    while n > 0:
        n //= 5                    # 5, 25, 125 … every exponent of five
        zeroes += n
    return zeroes""",
        },
    },
    {
        "slug": "nth-digit",
        "title": "Nth Digit",
        "difficulty": "Medium",
        "pattern": "locate the block of equal-length numbers",
        "statement": "The infinite sequence is 1, 2, 3, … written as digits. Return the n-th digit of that sequence (1-indexed).",
        "examples": [("n = 3", "3"), ("n = 11", "0")],
        "constraints": ["1 <= n <= 2^31 - 1"],
        "approach": "Numbers of a given length occupy a predictable block: 9 one-digit numbers, 90 two-digit numbers, 900 three-digit ones. Skip whole "
                     "blocks while n exceeds their size, then the block you land in tells you the number and the offset inside it. Everything is school "
                     "arithmetic once the block sizes are known — the only thing to watch is using 64-bit values for the totals.",
        "complexity": ("O(log n) time", "O(1)"),
        "code": {
            "cpp": r"""// Skip whole blocks of equal-length numbers, then index inside one
int findNthDigit(int n) {
    long long digits = 1, first = 1, blockSize = 9;      // 9 numbers of 1 digit
    while (n > digits * blockSize) {
        n -= digits * blockSize;                         // skip this whole block
        digits++;
        first *= 10;
        blockSize *= 10;
    }
    long long number = first + (n - 1) / digits;         // which number holds it
    int offset = (n - 1) % digits;                       // and where inside
    string text = to_string(number);
    return text[offset] - '0';
}   // O(log n) time · O(1) space""",
            "java": r"""// Skip whole blocks of equal-length numbers, then index inside one
int findNthDigit(int n) {
    long digits = 1, first = 1, blockSize = 9;           // 9 numbers of 1 digit
    while (n > digits * blockSize) {
        n -= digits * blockSize;                         // skip this whole block
        digits++;
        first *= 10;
        blockSize *= 10;
    }
    long number = first + (n - 1) / digits;               // which number holds it
    int offset = (int) ((n - 1) % digits);                // and where inside
    String text = Long.toString(number);
    return text.charAt(offset) - '0';
}   // O(log n) time · O(1) space""",
            "python": r"""def find_nth_digit(n):
    digits, first, block_size = 1, 1, 9          # 9 numbers of one digit
    while n > digits * block_size:
        n -= digits * block_size                 # skip the whole block
        digits += 1
        first *= 10
        block_size *= 10
    number = first + (n - 1) // digits           # which number holds it
    offset = (n - 1) % digits                    # and where inside that number
    return int(str(number)[offset])""",
        },
    },
    {
        "slug": "powx-n",
        "title": "Pow(x, n)",
        "difficulty": "Medium",
        "pattern": "exponentiation by squaring",
        "statement": "Implement pow(x, n), which computes x raised to the integer power n.",
        "examples": [("x = 2.00000, n = 10", "1024.00000"), ("x = 2.10000, n = 3", "9.26100"), ("x = 2.00000, n = -2", "0.25000")],
        "constraints": ["-100.0 < x < 100.0", "-2^31 <= n <= 2^31 - 1", "either x is not zero or n > 0"],
        "approach": "Multiplying n times is O(n). Instead, square the base and halve the exponent: each bit of n that is set contributes one factor, so "
                     "the loop runs as many times as n has bits. A negative exponent just inverts the base, and the exponent is widened before negating "
                     "so that Integer.MIN_VALUE does not overflow.",
        "complexity": ("O(log |n|) time", "O(1)"),
        "code": {
            "cpp": r"""// Square the base, halve the exponent: one multiply per exponent bit
double myPow(double x, int n) {
    long long exponent = n;
    if (exponent < 0) { x = 1 / x; exponent = -exponent; }
    double result = 1;
    while (exponent) {
        if (exponent & 1) result *= x;       // this bit of the exponent is set
        x *= x;                              // advance to the next power of two
        exponent >>= 1;
    }
    return result;
}   // O(log |n|) time · O(1) space""",
            "java": r"""// Square the base, halve the exponent: one multiply per exponent bit
double myPow(double x, int n) {
    long exponent = n;
    if (exponent < 0) { x = 1 / x; exponent = -exponent; }
    double result = 1;
    while (exponent != 0) {
        if ((exponent & 1) == 1) result *= x;   // this bit of the exponent is set
        x *= x;                                 // advance to the next power of two
        exponent >>= 1;
    }
    return result;
}   // O(log |n|) time · O(1) space""",
            "python": r"""def my_pow(x, n):
    if n < 0:
        x = 1 / x
        n = -n
    result = 1
    while n:
        if n & 1:
            result *= x             # this bit of the exponent is set
        x *= x                      # square up for the next bit
        n >>= 1
    return result""",
        },
    },
    {
        "slug": "multiply-strings",
        "title": "Multiply Strings",
        "difficulty": "Medium",
        "pattern": "grade-school multiplication on digit arrays",
        "statement": "Given two non-negative integers as strings, return their product as a string, without using any built-in big-integer conversion.",
        "examples": [("num1 = \"2\", num2 = \"3\"", "\"6\""), ("num1 = \"123\", num2 = \"456\"", "\"56088\"")],
        "constraints": ["1 <= num1.length, num2.length <= 200", "both strings contain only digits", "neither has leading zeros except \"0\""],
        "approach": "Every pair of digits multiplies into a known pair of output positions: index i from the first number and j from the second land on "
                     "i + j and i + j + 1. Accumulating those products in an array of digits and carrying as you go reproduces long multiplication and "
                     "never needs a number type wider than the answer.",
        "complexity": ("O(n · m) time", "O(n + m)"),
        "code": {
            "cpp": r"""// Digit i times digit j fills positions i+j and i+j+1
string multiply(string num1, string num2) {
    if (num1 == "0" || num2 == "0") return "0";
    vector<int> product(num1.size() + num2.size(), 0);
    for (int i = num1.size() - 1; i >= 0; i--)
        for (int j = num2.size() - 1; j >= 0; j--) {
            int total = (num1[i] - '0') * (num2[j] - '0') + product[i + j + 1];
            product[i + j + 1] = total % 10;         // this column
            product[i + j] += total / 10;            // and the carry left of it
        }
    string result;
    int start = 0;
    while (start + 1 < (int) product.size() && product[start] == 0) start++;   // no leading zeros
    for (int i = start; i < (int) product.size(); i++) result += char('0' + product[i]);
    return result;
}   // O(n · m) time · O(n + m) space""",
            "java": r"""// Digit i times digit j fills positions i+j and i+j+1
String multiply(String num1, String num2) {
    if (num1.equals("0") || num2.equals("0")) return "0";
    int[] product = new int[num1.length() + num2.length()];
    for (int i = num1.length() - 1; i >= 0; i--)
        for (int j = num2.length() - 1; j >= 0; j--) {
            int total = (num1.charAt(i) - '0') * (num2.charAt(j) - '0') + product[i + j + 1];
            product[i + j + 1] = total % 10;         // this column
            product[i + j] += total / 10;            // and the carry left of it
        }
    StringBuilder result = new StringBuilder();
    int start = 0;
    while (start + 1 < product.length && product[start] == 0) start++;   // no leading zeros
    for (int i = start; i < product.length; i++) result.append((char) ('0' + product[i]));
    return result.toString();
}   // O(n · m) time · O(n + m) space""",
            "python": r"""def multiply(num1, num2):
    if num1 == "0" or num2 == "0":
        return "0"
    product = [0] * (len(num1) + len(num2))
    for i in range(len(num1) - 1, -1, -1):
        for j in range(len(num2) - 1, -1, -1):
            total = int(num1[i]) * int(num2[j]) + product[i + j + 1]
            product[i + j + 1] = total % 10        # this column
            product[i + j] += total // 10          # and the carry left of it
    start = 0
    while start + 1 < len(product) and product[start] == 0:
        start += 1                                 # drop leading zeros
    return "".join(map(str, product[start:]))""",
        },
    },
    {
        "slug": "integer-break",
        "title": "Integer Break",
        "difficulty": "Medium",
        "pattern": "prefer 3s, then 2s",
        "statement": "Break n into the sum of at least two positive integers and return the largest possible product of those integers.",
        "examples": [("n = 2", "1"), ("n = 10", "36")],
        "constraints": ["2 <= n <= 58"],
        "approach": "Splitting a number into equal parts is best, and the best part is 3 — a part of 4 is two 2s, a part of 5 is better as 2 + 3, and "
                     "anything above 4 loses by splitting further. So use as many 3s as possible, then repair the remainder: a leftover 1 must become "
                     "2 + 2, and small n has its own trivial answer.",
        "complexity": ("O(n) time (O(log n) with fast power)", "O(1)"),
        "code": {
            "cpp": r"""// Equal parts are best and 3 is the best size
int integerBreak(int n) {
    if (n <= 3) return n - 1;                 // 2 -> 1, 3 -> 2
    int threes = n / 3, rest = n % 3;
    if (rest == 1) { threes--; rest = 4; }    // 3 + 1 is worse than 2 + 2
    long long best = 1;
    for (int i = 0; i < threes; i++) best *= 3;
    if (rest) best *= rest;
    return (int) best;
}   // O(n) time · O(1) space""",
            "java": r"""// Equal parts are best and 3 is the best size
int integerBreak(int n) {
    if (n <= 3) return n - 1;                 // 2 -> 1, 3 -> 2
    int threes = n / 3, rest = n % 3;
    if (rest == 1) { threes--; rest = 4; }    // 3 + 1 is worse than 2 + 2
    long best = 1;
    for (int i = 0; i < threes; i++) best *= 3;
    if (rest != 0) best *= rest;
    return (int) best;
}   // O(n) time · O(1) space""",
            "python": r"""def integer_break(n):
    if n <= 3:
        return n - 1                          # 2 -> 1, 3 -> 2
    threes, rest = divmod(n, 3)
    if rest == 1:
        threes -= 1                           # 3 + 1 is worse than 2 + 2
        rest = 4
    return 3 ** threes * (rest if rest else 1)""",
        },
    },
    {
        "slug": "sum-of-square-numbers",
        "title": "Sum of Square Numbers",
        "difficulty": "Medium",
        "pattern": "two pointers over squares",
        "statement": "Return true if there exist non-negative integers a and b with a² + b² = c.",
        "examples": [("c = 5", "true"), ("c = 3", "false")],
        "constraints": ["0 <= c <= 2^31 - 1"],
        "approach": "Start one pointer at 0 and the other at the integer square root of c. If the squares overshoot, lower the big pointer; if they fall "
                     "short, raise the small one — the sum is monotone in each pointer, so the pair meets the target if it exists. No lookup table and "
                     "no floating-point comparison of the answer, just the sqrt limit for the starting position.",
        "complexity": ("O(sqrt c) time", "O(1)"),
        "code": {
            "cpp": r"""// Two pointers over the squares: nudge whichever side misses
bool judgeSquareSum(int c) {
    long long low = 0, high = (long long) sqrt((double) c);
    while (low <= high) {
        long long sum = low * low + high * high;
        if (sum == c) return true;
        if (sum < c) low++;
        else high--;
    }
    return false;
}   // O(sqrt c) time · O(1) space""",
            "java": r"""// Two pointers over the squares: nudge whichever side misses
boolean judgeSquareSum(int c) {
    long low = 0, high = (long) Math.sqrt(c);
    while (low <= high) {
        long sum = low * low + high * high;
        if (sum == c) return true;
        if (sum < c) low++;
        else high--;
    }
    return false;
}   // O(sqrt c) time · O(1) space""",
            "python": r"""def judge_square_sum(c):
    low, high = 0, int(c ** 0.5)
    while low <= high:
        total = low * low + high * high
        if total == c:
            return True
        if total < c:
            low += 1                 # the small square is not big enough
        else:
            high -= 1                # the big square overshoots
    return False""",
        },
    },
    {
        "slug": "angle-between-hands-of-a-clock",
        "title": "Angle Between Hands of a Clock",
        "difficulty": "Medium",
        "pattern": "two angles, then the smaller one",
        "statement": "Given hour and minutes, return the smaller angle in degrees between the clock's two hands.",
        "examples": [("hour = 12, minutes = 30", "165"), ("hour = 3, minutes = 30", "75"), ("hour = 3, minutes = 15", "7.5")],
        "constraints": ["1 <= hour <= 12", "0 <= minutes <= 59", "answers within 10^-5 of the true value count as correct"],
        "approach": "Each hand has a fixed speed: the minute hand sweeps 6° per minute, the hour hand 30° per hour plus 0.5° for every minute it has "
                     "already travelled — that half-degree is what makes 3:15 give 7.5° instead of 0°. Take the absolute difference and, because the "
                     "two hands are symmetric, report min(difference, 360 - difference).",
        "complexity": ("O(1) time", "O(1)"),
        "code": {
            "cpp": r"""// 6° per minute for one hand, 30° per hour + 0.5° per minute for the other
double angleClock(int hour, int minutes) {
    double minuteAngle = minutes * 6.0;
    double hourAngle = (hour % 12) * 30.0 + minutes * 0.5;   // the hand creeps on
    double difference = fabs(hourAngle - minuteAngle);
    return difference > 180 ? 360 - difference : difference;
}   // O(1) time · O(1) space""",
            "java": r"""// 6° per minute for one hand, 30° per hour + 0.5° per minute for the other
double angleClock(int hour, int minutes) {
    double minuteAngle = minutes * 6.0;
    double hourAngle = (hour % 12) * 30.0 + minutes * 0.5;   // the hand creeps on
    double difference = Math.abs(hourAngle - minuteAngle);
    return difference > 180 ? 360 - difference : difference;
}   // O(1) time · O(1) space""",
            "python": r"""def angle_clock(hour, minutes):
    minute_angle = minutes * 6.0                            # 360 / 60
    hour_angle = (hour % 12) * 30.0 + minutes * 0.5         # 30 per hour, 0.5 per minute
    difference = abs(hour_angle - minute_angle)
    return min(difference, 360 - difference)                # the smaller of the two gaps""",
        },
    },
    {
        "slug": "smallest-integer-divisible-by-k",
        "title": "Smallest Integer Divisible by K",
        "difficulty": "Medium",
        "pattern": "remainders of repunits",
        "statement": "Return the length of the smallest positive integer made only of 1s that is divisible by k, or -1 if no such number exists.",
        "examples": [("k = 1", "1"), ("k = 2", "-1"), ("k = 3", "3")],
        "constraints": ["1 <= k <= 10^5"],
        "approach": "The repunit of length L is the previous one times ten plus one, and only the remainder modulo k matters. If k shares a factor with "
                     "ten, no repunit can ever be divisible by it, so answer -1 immediately; otherwise the remainder sequence must repeat within k steps, "
                     "so trying k lengths is enough and never needs the enormous numbers themselves.",
        "complexity": ("O(k) time", "O(1)"),
        "code": {
            "cpp": r"""// Track only remainders: r = (r * 10 + 1) % k
int smallestRepunitDivByK(int k) {
    if (k % 2 == 0 || k % 5 == 0) return -1;   // shares a factor with 10
    int remainder = 0;
    for (int length = 1; length <= k; length++) {
        remainder = (remainder * 10 + 1) % k;  // append one more 1
        if (remainder == 0) return length;
    }
    return -1;
}   // O(k) time · O(1) space""",
            "java": r"""// Track only remainders: r = (r * 10 + 1) % k
int smallestRepunitDivByK(int k) {
    if (k % 2 == 0 || k % 5 == 0) return -1;   // shares a factor with 10
    int remainder = 0;
    for (int length = 1; length <= k; length++) {
        remainder = (remainder * 10 + 1) % k;  // append one more 1
        if (remainder == 0) return length;
    }
    return -1;
}   // O(k) time · O(1) space""",
            "python": r"""def smallest_repunit_div_by_k(k):
    if k % 2 == 0 or k % 5 == 0:
        return -1                    # no repunit can hold a factor of 2 or 5
    remainder = 0
    for length in range(1, k + 1):
        remainder = (remainder * 10 + 1) % k   # append another 1
        if remainder == 0:
            return length
    return -1""",
        },
    },
    {
        "slug": "fraction-to-recurring-decimal",
        "title": "Fraction to Recurring Decimal",
        "difficulty": "Medium",
        "pattern": "long division + repeated remainder",
        "statement": "Given numerator and denominator, return the fraction as a decimal string, wrapping any repeating part in parentheses.",
        "examples": [("numerator = 1, denominator = 2", "\"0.5\""), ("numerator = 2, denominator = 1", "\"2\""),
                      ("numerator = 4, denominator = 333", "\"0.(012)\"")],
        "constraints": ["-2^31 <= numerator, denominator <= 2^31 - 1", "denominator != 0", "the answer string is shorter than 10^4 characters"],
        "approach": "Handle the sign and the integer part first, then run school long division: multiply the remainder by ten, write a digit, keep the "
                     "remainder. The fraction repeats exactly when a remainder reappears, and remembering where each remainder first appeared tells you "
                     "where to open the parenthesis — no floating point anywhere.",
        "complexity": ("O(denominator) time", "O(denominator)"),
        "code": {
            "cpp": r"""// Long division; a repeated remainder marks the recurring block
string fractionToDecimal(int numerator, int denominator) {
    if (numerator == 0) return "0";
    string result;
    if ((numerator < 0) != (denominator < 0)) result += '-';
    long long top = llabs((long long) numerator), bottom = llabs((long long) denominator);
    result += to_string(top / bottom);                   // integer part
    long long remainder = top % bottom;
    if (remainder == 0) return result;
    result += '.';
    unordered_map<long long, int> seen;                  // remainder -> position
    while (remainder != 0) {
        auto it = seen.find(remainder);
        if (it != seen.end()) {                          // the block repeats from here
            result.insert(it->second, "(");
            result += ')';
            break;
        }
        seen[remainder] = result.size();
        remainder *= 10;
        result += char('0' + remainder / bottom);
        remainder %= bottom;
    }
    return result;
}   // O(denominator) time · O(denominator) space""",
            "java": r"""// Long division; a repeated remainder marks the recurring block
String fractionToDecimal(int numerator, int denominator) {
    if (numerator == 0) return "0";
    StringBuilder result = new StringBuilder();
    if ((numerator < 0) != (denominator < 0)) result.append('-');
    long top = Math.abs((long) numerator), bottom = Math.abs((long) denominator);
    result.append(top / bottom);                         // integer part
    long remainder = top % bottom;
    if (remainder == 0) return result.toString();
    result.append('.');
    Map<Long, Integer> seen = new HashMap<>();           // remainder -> position
    while (remainder != 0) {
        Integer at = seen.get(remainder);
        if (at != null) {                                // the block repeats from here
            result.insert(at, "(");
            result.append(')');
            break;
        }
        seen.put(remainder, result.length());
        remainder *= 10;
        result.append((char) ('0' + remainder / bottom));
        remainder %= bottom;
    }
    return result.toString();
}   // O(denominator) time · O(denominator) space""",
            "python": r"""def fraction_to_decimal(numerator, denominator):
    if numerator == 0:
        return "0"
    sign = "-" if (numerator < 0) != (denominator < 0) else ""
    top, bottom = abs(numerator), abs(denominator)
    result = [sign, str(top // bottom)]        # integer part
    remainder = top % bottom
    if remainder == 0:
        return "".join(result)
    result.append(".")
    seen = {}                                  # remainder -> where its digit was written
    while remainder:
        if remainder in seen:                  # the block repeats from here
            result.insert(seen[remainder], "(")
            result.append(")")
            break
        seen[remainder] = len(result)
        remainder *= 10
        result.append(str(remainder // bottom))
        remainder %= bottom
    return "".join(result)""",
        },
    },
    {
        "slug": "super-pow",
        "title": "Super Pow",
        "difficulty": "Medium",
        "pattern": "modular exponentiation over a digit array",
        "statement": "Compute a^b modulo 1337, where b is given as an array of decimal digits (it may be far too large to build).",
        "examples": [("a = 2, b = [3]", "8"), ("a = 2, b = [1,0]", "1024"), ("a = 1, b = [4,3,3,8,5,2]", "1")],
        "constraints": ["1 <= a <= 2^31 - 1", "1 <= b.length <= 2000", "0 <= b[i] <= 9", "b has no leading zeros"],
        "approach": "Read the exponent one digit at a time and use a^(10d + e) = (a^d)^10 · a^e, all modulo 1337. Sweeping the digits from the front "
                     "keeps one running value: raise it to the tenth power for the next digit and multiply in the new one. Only a small modulus is ever "
                     "squared, so nothing overflows and the exponent array never has to become a number.",
        "complexity": ("O(len(b) · 10 · log 1337) time", "O(1)"),
        "code": {
            "cpp": r"""// a^(10d + e) = (a^d)^10 · a^e, all modulo 1337
long long modPow(long long base, int exponent) {
    long long result = 1;
    base %= 1337;
    while (exponent > 0) {
        if (exponent & 1) result = result * base % 1337;
        base = base * base % 1337;
        exponent >>= 1;
    }
    return result;
}
int superPow(int a, vector<int>& b) {
    long long result = 1;
    for (int digit : b)
        result = modPow(result, 10) * modPow(a, digit) % 1337;   // shift and add
    return (int) result;
}   // O(len(b) · log 1337) time · O(1) space""",
            "java": r"""// a^(10d + e) = (a^d)^10 · a^e, all modulo 1337
long modPow(long base, int exponent) {
    long result = 1;
    base %= 1337;
    while (exponent > 0) {
        if ((exponent & 1) == 1) result = result * base % 1337;
        base = base * base % 1337;
        exponent >>= 1;
    }
    return result;
}
int superPow(int a, int[] b) {
    long result = 1;
    for (int digit : b)
        result = modPow(result, 10) * modPow(a, digit) % 1337;   // shift and add
    return (int) result;
}   // O(len(b) · log 1337) time · O(1) space""",
            "python": r"""def super_pow(a, b):
    mod = 1337

    def power(base, exponent):
        base %= mod
        result = 1
        while exponent:
            if exponent & 1:
                result = result * base % mod
            base = base * base % mod
            exponent >>= 1
        return result

    result = 1
    for digit in b:                          # a^(10d + e) = (a^d)^10 · a^e
        result = power(result, 10) * power(a, digit) % mod
    return result""",
        },
    },
    {
        "slug": "number-of-digit-one",
        "title": "Number of Digit One",
        "difficulty": "Hard",
        "pattern": "count a digit column by column",
        "statement": "Return how many times the digit 1 appears in the decimal representations of every integer from 0 to n.",
        "examples": [("n = 13", "6"), ("n = 0", "0")],
        "constraints": ["0 <= n <= 10^9"],
        "approach": "Do not walk the numbers — walk the positions. At the place worth d, the sequence of digits at that place is a repeating pattern, so the "
                     "number of 1s there is whole blocks times d, plus a partial block decided by the current digit: 0 contributes nothing, 1 contributes "
                     "the number of suffixes seen so far plus one, anything larger contributes a full d.",
        "complexity": ("O(log n) time", "O(1)"),
        "code": {
            "cpp": r"""// Each decimal place contributes whole blocks plus a partial one
int countDigitOne(int n) {
    long long ones = 0;
    for (long long place = 1; place <= n; place *= 10) {
        long long lower = n % place;                        // digits right of this place
        long long current = (n / place) % 10;
        long long higher = n / (place * 10);
        if (current == 0) ones += higher * place;
        else if (current == 1) ones += higher * place + lower + 1;
        else ones += (higher + 1) * place;
    }
    return (int) ones;
}   // O(log n) time · O(1) space""",
            "java": r"""// Each decimal place contributes whole blocks plus a partial one
int countDigitOne(int n) {
    long ones = 0;
    for (long place = 1; place <= n; place *= 10) {
        long lower = n % place;                             // digits right of this place
        long current = (n / place) % 10;
        long higher = n / (place * 10);
        if (current == 0) ones += higher * place;
        else if (current == 1) ones += higher * place + lower + 1;
        else ones += (higher + 1) * place;
    }
    return (int) ones;
}   // O(log n) time · O(1) space""",
            "python": r"""def count_digit_one(n):
    ones = 0
    place = 1
    while place <= n:
        lower = n % place                   # digits right of this place
        current = (n // place) % 10
        higher = n // (place * 10)
        if current == 0:
            ones += higher * place
        elif current == 1:
            ones += higher * place + lower + 1   # the partial block runs to n
        else:
            ones += (higher + 1) * place
        place *= 10
    return ones""",
        },
    },
    {
        "slug": "integer-to-english-words",
        "title": "Integer to English Words",
        "difficulty": "Hard",
        "pattern": "three-digit chunks + scale words",
        "statement": "Convert a non-negative integer into its English words representation.",
        "examples": [("num = 123", "\"One Hundred Twenty Three\""), ("num = 12345", "\"Twelve Thousand Three Hundred Forty Five\""),
                      ("num = 1234567", "\"One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven\"")],
        "constraints": ["0 <= num <= 2^31 - 1", "the output must not contain leading or trailing spaces, or double spaces"],
        "approach": "English groups numbers in threes, and each group is read the same way with a scale word after it. Write one routine for a value below "
                     "1000 — hundreds digit, then the 10…19 words, then tens and units — and call it once per group from the least significant upwards, "
                     "prepending each group's text so the big end lands in front.",
        "complexity": ("O(log n) time", "O(log n)"),
        "code": {
            "cpp": r"""// Read each group of three, then append its scale word
string below1000(int n) {
    static const vector<string> small = {"", "One", "Two", "Three", "Four", "Five", "Six", "Seven",
                                         "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen",
                                         "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"};
    static const vector<string> tens = {"", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"};
    string words;
    if (n >= 100) {
        words += small[n / 100] + " Hundred";
        n %= 100;
        if (n) words += ' ';
    }
    if (n >= 20) {
        words += tens[n / 10];
        n %= 10;
        if (n) words += ' ' + small[n];
    } else if (n > 0) {
        words += small[n];
    }
    return words;
}
string numberToWords(int num) {
    if (num == 0) return "Zero";
    static const vector<string> scales = {"", " Thousand", " Million", " Billion"};
    string result;
    for (int group = 0; num > 0; group++) {
        int chunk = num % 1000;
        if (chunk) {
            string text = below1000(chunk) + scales[group];
            result = result.empty() ? text : text + " " + result;   // bigger groups go first
        }
        num /= 1000;
    }
    return result;
}   // O(log n) time · O(log n) space""",
            "java": r"""// Read each group of three, then append its scale word
String below1000(int n) {
    String[] small = {"", "One", "Two", "Three", "Four", "Five", "Six", "Seven",
                      "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen",
                      "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"};
    String[] tens = {"", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"};
    StringBuilder words = new StringBuilder();
    if (n >= 100) {
        words.append(small[n / 100]).append(" Hundred");
        n %= 100;
        if (n != 0) words.append(' ');
    }
    if (n >= 20) {
        words.append(tens[n / 10]);
        n %= 10;
        if (n != 0) words.append(' ').append(small[n]);
    } else if (n > 0) {
        words.append(small[n]);
    }
    return words.toString();
}
String numberToWords(int num) {
    if (num == 0) return "Zero";
    String[] scales = {"", " Thousand", " Million", " Billion"};
    StringBuilder result = new StringBuilder();
    for (int group = 0; num > 0; group++) {
        int chunk = num % 1000;
        if (chunk != 0) {
            String text = below1000(chunk) + scales[group];
            if (result.length() > 0) result.insert(0, text + " ");
            else result.append(text);            // bigger groups go first
        }
        num /= 1000;
    }
    return result.toString();
}   // O(log n) time · O(log n) space""",
            "python": r"""def number_to_words(num):
    if num == 0:
        return "Zero"
    small = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
             "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
             "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    scales = ["", " Thousand", " Million", " Billion"]

    def below_thousand(n):
        words = []
        if n >= 100:
            words.append(small[n // 100] + " Hundred")
            n %= 100
        if n >= 20:
            words.append(tens[n // 10])
            n %= 10
        if n:
            words.append(small[n])
        return " ".join(words)

    parts = []
    group = 0
    while num > 0:
        chunk = num % 1000
        if chunk:                                   # read every group of three
            parts.insert(0, below_thousand(chunk) + scales[group])
        num //= 1000
        group += 1
    return " ".join(parts)""",
        },
    },
    {
        "slug": "permutation-sequence",
        "title": "Permutation Sequence",
        "difficulty": "Hard",
        "pattern": "factorial number system",
        "statement": "Return the k-th permutation of the numbers 1 to n when all of them are listed in lexicographic order.",
        "examples": [("n = 3, k = 3", "\"213\""), ("n = 4, k = 9", "\"2314\""), ("n = 3, k = 1", "\"123\"")],
        "constraints": ["1 <= n <= 9", "1 <= k <= n!"],
        "approach": "The first position splits the permutations into n equal blocks of (n-1)! each, and which block k falls in names the first digit. Taking "
                     "the remainder and repeating with the remaining digits decodes k the way you decode a number written in the factorial number "
                     "system — no permutation is ever generated.",
        "complexity": ("O(n²) time", "O(n)"),
        "code": {
            "cpp": r"""// k decoded in the factorial number system, digit by digit
string getPermutation(int n, int k) {
    vector<int> factorial(n + 1, 1);
    vector<char> available;
    for (int i = 1; i <= n; i++) {
        factorial[i] = factorial[i - 1] * i;
        available.push_back(char('0' + i));
    }
    k--;                                     // switch to 0-based counting
    string result;
    for (int remaining = n; remaining >= 1; remaining--) {
        int blockSize = factorial[remaining - 1];
        int index = k / blockSize;           // which block of the remains
        k %= blockSize;
        result += available[index];
        available.erase(available.begin() + index);
    }
    return result;
}   // O(n^2) time · O(n) space""",
            "java": r"""// k decoded in the factorial number system, digit by digit
String getPermutation(int n, int k) {
    int[] factorial = new int[n + 1];
    factorial[0] = 1;
    List<Integer> available = new ArrayList<>();
    for (int i = 1; i <= n; i++) {
        factorial[i] = factorial[i - 1] * i;
        available.add(i);
    }
    k--;                                     // switch to 0-based counting
    StringBuilder result = new StringBuilder();
    for (int remaining = n; remaining >= 1; remaining--) {
        int blockSize = factorial[remaining - 1];
        int index = k / blockSize;           // which block of the remains
        k %= blockSize;
        result.append(available.remove(index));
    }
    return result.toString();
}   // O(n^2) time · O(n) space""",
            "python": r"""def get_permutation(n, k):
    factorial = [1] * (n + 1)
    available = [str(i) for i in range(1, n + 1)]
    for i in range(1, n + 1):
        factorial[i] = factorial[i - 1] * i
    k -= 1                                   # 0-based counting
    result = []
    for remaining in range(n, 0, -1):
        block = factorial[remaining - 1]     # permutations sharing this prefix
        index, k = divmod(k, block)
        result.append(available.pop(index))
    return "".join(result)""",
        },
    },
    {
        "slug": "numbers-at-most-n-given-digit-set",
        "title": "Numbers At Most N Given Digit Set",
        "difficulty": "Hard",
        "pattern": "digit DP with a prefix walk",
        "statement": "digits is a sorted list of distinct single-digit strings. Return how many positive integers, using only those digits, are less "
                     "than or equal to n.",
        "examples": [("digits = [\"1\",\"3\",\"5\",\"7\"], n = 100", "20"), ("digits = [\"1\",\"4\",\"9\"], n = 1000000000", "29523"),
                      ("digits = [\"7\"], n = 8", "1")],
        "constraints": ["1 <= digits.length <= 9", "digits[i].length == 1", "digits contains no duplicates", "1 <= n <= 10^9"],
        "approach": "Split the count by length. Every number shorter than n can use any allowed digit in any position — that is base^length. Numbers of "
                     "n's own length are counted by walking n's digits: each allowed digit smaller than the current one frees the remaining positions, "
                     "and the walk continues only while n's own digit is available; if a digit of n is not allowed, the walk stops there.",
        "complexity": ("O(10 · digits of n) time", "O(1)"),
        "code": {
            "cpp": r"""// Count shorter numbers freely, then walk n's own prefix
int atMostNGivenDigitSet(vector<string>& digits, int n) {
    string bound = to_string(n);
    int length = bound.size(), base = digits.size();
    int total = 0;
    for (int len = 1; len < length; len++) {         // every shorter number
        int count = 1;
        for (int i = 0; i < len; i++) count *= base;
        total += count;
    }
    for (int i = 0; i < length; i++) {
        bool sameDigitAllowed = false;
        for (const string& d : digits) {
            if (d[0] < bound[i]) {                   // smaller digit frees the rest
                int free = 1;
                for (int j = i + 1; j < length; j++) free *= base;
                total += free;
            } else if (d[0] == bound[i]) {
                sameDigitAllowed = true;             // keep matching n's prefix
            }
        }
        if (!sameDigitAllowed) return total;         // n's prefix can no longer be matched
    }
    return total + 1;                                // n itself uses allowed digits
}   // O(10 · len(n)) time · O(1) space""",
            "java": r"""// Count shorter numbers freely, then walk n's own prefix
int atMostNGivenDigitSet(String[] digits, int n) {
    String bound = Integer.toString(n);
    int length = bound.length(), base = digits.length;
    int total = 0;
    for (int len = 1; len < length; len++) {         // every shorter number
        int count = 1;
        for (int i = 0; i < len; i++) count *= base;
        total += count;
    }
    for (int i = 0; i < length; i++) {
        boolean sameDigitAllowed = false;
        for (String d : digits) {
            if (d.charAt(0) < bound.charAt(i)) {     // smaller digit frees the rest
                int free = 1;
                for (int j = i + 1; j < length; j++) free *= base;
                total += free;
            } else if (d.charAt(0) == bound.charAt(i)) {
                sameDigitAllowed = true;             // keep matching n's prefix
            }
        }
        if (!sameDigitAllowed) return total;         // n's prefix can no longer be matched
    }
    return total + 1;                                // n itself uses allowed digits
}   // O(10 · len(n)) time · O(1) space""",
            "python": r"""def at_most_n_given_digit_set(digits, n):
    bound = str(n)
    base = len(digits)
    total = 0
    for length in range(1, len(bound)):        # any digit, any position
        total += base ** length
    for i, ch in enumerate(bound):             # numbers of n's own length
        matched = False
        for d in digits:
            if d < ch:
                total += base ** (len(bound) - i - 1)   # smaller digit frees the rest
            elif d == ch:
                matched = True                          # keep following n's prefix
        if not matched:
            return total                       # n's prefix can no longer be matched
    return total + 1                           # n itself qualifies""",
        },
    },
    {
        "slug": "sum-of-floored-pairs",
        "title": "Sum of Floored Pairs",
        "difficulty": "Hard",
        "pattern": "harmonic sweep of quotients",
        "statement": "Return the sum of floor(nums[i] / nums[j]) over all pairs of indices (i, j), modulo 10^9 + 7.",
        "examples": [("nums = [2,5,9]", "10"), ("nums = [7,7,7,7,7,7,7]", "49")],
        "constraints": ["1 <= nums.length <= 10^5", "1 <= nums[i] <= 10^5"],
        "approach": "For a fixed denominator d the quotient is constant on ranges of numerators: [d, 2d-1] gives 1, [2d, 3d-1] gives 2, and so on. Sort "
                     "by counting values into buckets, build a prefix count, then for every denominator sweep its multiples — the total number of steps is "
                     "harmonic, about M log M, instead of quadratic.",
        "complexity": ("O(M log M) time", "O(M)"),
        "code": {
            "cpp": r"""// Denominator fixed: the quotient is constant on ranges [k·d, (k+1)d)
int sumOfFlooredPairs(vector<int>& nums) {
    const int MOD = 1000000007;
    int top = *max_element(nums.begin(), nums.end());
    vector<long long> frequency(top + 2, 0), prefix(top + 2, 0);
    for (int x : nums) frequency[x]++;
    for (int v = 1; v <= top; v++) prefix[v] = prefix[v - 1] + frequency[v];
    long long total = 0;
    for (int d = 1; d <= top; d++) {
        if (frequency[d] == 0) continue;
        for (long long low = d; low <= top; low += d) {
            long long high = min((long long) top, low + d - 1);
            long long numerators = prefix[high] - prefix[low - 1];
            total = (total + (low / d) % MOD * (numerators % MOD) % MOD * frequency[d]) % MOD;
        }
    }
    return (int) total;
}   // O(M log M) time · O(M) space""",
            "java": r"""// Denominator fixed: the quotient is constant on ranges [k·d, (k+1)d)
int sumOfFlooredPairs(int[] nums) {
    final int MOD = 1000000007;
    int top = 0;
    for (int x : nums) top = Math.max(top, x);
    long[] frequency = new long[top + 2], prefix = new long[top + 2];
    for (int x : nums) frequency[x]++;
    for (int v = 1; v <= top; v++) prefix[v] = prefix[v - 1] + frequency[v];
    long total = 0;
    for (int d = 1; d <= top; d++) {
        if (frequency[d] == 0) continue;
        for (long low = d; low <= top; low += d) {
            long high = Math.min((long) top, low + d - 1);
            long numerators = prefix[(int) high] - prefix[(int) low - 1];
            total = (total + (low / d) * (numerators % MOD) % MOD * frequency[d]) % MOD;
        }
    }
    return (int) total;
}   // O(M log M) time · O(M) space""",
            "python": r"""def sum_of_floored_pairs(nums):
    mod = 10**9 + 7
    top = max(nums)
    frequency = [0] * (top + 2)
    for x in nums:
        frequency[x] += 1
    prefix = [0] * (top + 2)              # prefix[v] = how many values are ≤ v
    for v in range(1, top + 1):
        prefix[v] = prefix[v - 1] + frequency[v]
    total = 0
    for d in range(1, top + 1):
        if frequency[d] == 0:
            continue                      # d is never a denominator
        for low in range(d, top + 1, d):  # quotient is low // d on this whole range
            high = min(top, low + d - 1)
            numerators = prefix[high] - prefix[low - 1]
            total = (total + (low // d) * numerators % mod * frequency[d]) % mod
    return total""",
        },
    },
    {
        "slug": "reaching-points",
        "title": "Reaching Points",
        "difficulty": "Hard",
        "pattern": "run the Euclidean step backwards",
        "statement": "Starting from (sx, sy), a move replaces (x, y) with (x + y, y) or (x, y + x). Return true if (tx, ty) is reachable.",
        "examples": [("sx = 1, sy = 1, tx = 3, ty = 5", "true"), ("sx = 1, sy = 1, tx = 2, ty = 2", "false"),
                      ("sx = 1, sy = 1, tx = 1, ty = 1", "true")],
        "constraints": ["1 <= sx, sy, tx, ty <= 10^9"],
        "approach": "Forward moves only grow the coordinates, so run them backwards: the larger coordinate must be the one that was just increased, so "
                     "subtract the smaller from it. Subtracting one step at a time is far too slow for 10^9, but a modulo does many steps at once — with "
                     "the special case that when the other coordinate already equals its target, only exact multiples of the remaining gap will land.",
        "complexity": ("O(log max) time", "O(1)"),
        "code": {
            "cpp": r"""// Undo the last move, many steps at a time
bool reachingPoints(int sx, int sy, int tx, int ty) {
    while (tx >= sx && ty >= sy) {
        if (tx == sx && ty == sy) return true;
        if (tx > ty) {
            if (ty == sy) return (tx - sx) % ty == 0;    // only x can still shrink
            tx %= ty;                                    // as many steps as fit
        } else {
            if (tx == sx) return (ty - sy) % tx == 0;    // only y can still shrink
            ty %= tx;
        }
    }
    return false;
}   // O(log max) time · O(1) space""",
            "java": r"""// Undo the last move, many steps at a time
boolean reachingPoints(int sx, int sy, int tx, int ty) {
    while (tx >= sx && ty >= sy) {
        if (tx == sx && ty == sy) return true;
        if (tx > ty) {
            if (ty == sy) return (tx - sx) % ty == 0;    // only x can still shrink
            tx %= ty;                                    // as many steps as fit
        } else {
            if (tx == sx) return (ty - sy) % tx == 0;    // only y can still shrink
            ty %= tx;
        }
    }
    return false;
}   // O(log max) time · O(1) space""",
            "python": r"""def reaching_points(sx, sy, tx, ty):
    while tx >= sx and ty >= sy:
        if tx == sx and ty == sy:
            return True
        if tx > ty:
            if ty == sy:                      # only x can still shrink
                return (tx - sx) % ty == 0
            tx %= ty                          # undo as many steps as fit
        else:
            if tx == sx:                      # only y can still shrink
                return (ty - sy) % tx == 0
            ty %= tx
    return False""",
        },
    },
    {
        "slug": "count-ways-to-make-array-with-product",
        "title": "Count Ways to Make Array With Product",
        "difficulty": "Hard",
        "pattern": "stars and bars per prime",
        "statement": "For each query [n, k], count the arrays of n positive integers whose product is k, using only primes below 100, modulo 10^9 + 7.",
        "examples": [("queries = [[2,6],[5,1],[73,660]]", "[4,1,50734910]"),
                      ("queries = [[1,1],[2,2],[3,3],[4,4],[5,5]]", "[1,2,3,10,5]")],
        "constraints": ["1 <= queries.length <= 10^4", "1 <= n_i <= 10^4", "0 <= k_i <= 10^5", "each k_i has no prime factor above 100, or is 1"],
        "approach": "Each prime in k is distributed independently across the n slots, and distributing e copies of one prime is a stars-and-bars count: "
                     "C(e + n - 1, e). Factor k with the primes below 100, evaluate that binomial as a short product with modular inverses, and multiply "
                     "the results — a leftover large prime means no array exists at all.",
        "complexity": ("O(25 · max exponent) per query", "O(1)"),
        "code": {
            "cpp": r"""// Each prime's exponent spreads over n slots: C(e + n - 1, e)
long long power(long long base, long long exponent, long long mod) {
    long long result = 1;
    base %= mod;
    while (exponent > 0) {
        if (exponent & 1) result = result * base % mod;
        base = base * base % mod;
        exponent >>= 1;
    }
    return result;
}
vector<int> waysToFillArray(vector<vector<int>>& queries) {
    const long long MOD = 1000000007;
    vector<int> primes;
    for (int p = 2; p < 100; p++) {
        bool prime = true;
        for (int d = 2; d * d <= p; d++) if (p % d == 0) { prime = false; break; }
        if (prime) primes.push_back(p);
    }
    vector<int> answer;
    for (const vector<int>& query : queries) {
        long long n = query[0], k = query[1], ways = 1;
        for (int p : primes) {
            int exponent = 0;
            while (k % p == 0) { k /= p; exponent++; }
            for (int i = 1; i <= exponent; i++)                 // C(e + n - 1, e)
                ways = ways * (n + i - 1) % MOD * power(i, MOD - 2, MOD) % MOD;
        }
        if (k > 1) ways = 0;                                    // a prime above 100 appeared
        answer.push_back((int) ways);
    }
    return answer;
}   // O(queries · exponents) time · O(1) space""",
            "java": r"""// Each prime's exponent spreads over n slots: C(e + n - 1, e)
long power(long base, long exponent, long mod) {
    long result = 1;
    base %= mod;
    while (exponent > 0) {
        if ((exponent & 1) == 1) result = result * base % mod;
        base = base * base % mod;
        exponent >>= 1;
    }
    return result;
}
int[] waysToFillArray(int[][] queries) {
    final long MOD = 1000000007L;
    List<Integer> primes = new ArrayList<>();
    for (int p = 2; p < 100; p++) {
        boolean prime = true;
        for (int d = 2; d * d <= p; d++) if (p % d == 0) { prime = false; break; }
        if (prime) primes.add(p);
    }
    int[] answer = new int[queries.length];
    for (int q = 0; q < queries.length; q++) {
        long n = queries[q][0], k = queries[q][1], ways = 1;
        for (int p : primes) {
            int exponent = 0;
            while (k % p == 0) { k /= p; exponent++; }
            for (int i = 1; i <= exponent; i++)                 // C(e + n - 1, e)
                ways = ways * (n + i - 1) % MOD * power(i, MOD - 2, MOD) % MOD;
        }
        if (k > 1) ways = 0;                                    // a prime above 100 appeared
        answer[q] = (int) ways;
    }
    return answer;
}   // O(queries · exponents) time · O(1) space""",
            "python": r"""def ways_to_fill_array(queries):
    mod = 10**9 + 7
    primes = [p for p in range(2, 100) if all(p % d for d in range(2, int(p ** 0.5) + 1))]
    answer = []
    for n, k in queries:
        ways = 1
        for p in primes:
            exponent = 0
            while k % p == 0:                     # how many copies of this prime
                k //= p
                exponent += 1
            for i in range(1, exponent + 1):      # stars and bars: C(e + n - 1, e)
                ways = ways * (n + i - 1) % mod * pow(i, mod - 2, mod) % mod
        if k > 1:
            ways = 0                              # a prime above 100 can never appear
        answer.append(ways)
    return answer""",
        },
    },
    {
        "slug": "sum-of-k-mirror-numbers",
        "title": "Sum of K-Mirror Numbers",
        "difficulty": "Hard",
        "pattern": "enumerate decimal palindromes",
        "statement": "A k-mirror number reads the same forwards and backwards in base 10 and in base k. Return the sum of the n smallest k-mirror "
                     "numbers.",
        "examples": [("k = 2, n = 5", "25"), ("k = 3, n = 7", "499")],
        "constraints": ["2 <= k <= 9", "1 <= n <= 30"],
        "approach": "Rather than testing every integer, generate the decimal palindromes in increasing order: pick a half, mirror it, and numbers come out "
                     "sorted by construction. Each candidate is then converted to base k and checked — only about two integers in every decade of "
                     "candidates can ever pass, so the search stays small.",
        "complexity": ("O(answer size · log_k answer) time", "O(log answer)"),
        "code": {
            "cpp": r"""// Generate decimal palindromes in order, keep the base-k ones
bool isBaseKPalindrome(long long value, int k) {
    vector<int> digits;
    while (value > 0) { digits.push_back((int) (value % k)); value /= k; }
    for (int i = 0, j = digits.size() - 1; i < j; i++, j--)
        if (digits[i] != digits[j]) return false;
    return true;
}
long long kMirror(int k, int n) {
    long long total = 0;
    int found = 0;
    for (int length = 1; found < n; length++) {
        int halfLength = (length + 1) / 2;
        long long start = 1;
        for (int i = 1; i < halfLength; i++) start *= 10;    // smallest half
        long long end = start * 10;
        for (long long half = start; half < end && found < n; half++) {
            string text = to_string(half), mirror = text;
            if (length % 2 == 1) mirror.pop_back();          // drop the middle digit
            reverse(mirror.begin(), mirror.end());
            long long candidate = stoll(text + mirror);
            if (isBaseKPalindrome(candidate, k)) { total += candidate; found++; }
        }
    }
    return total;
}   // O(candidates · log_k n) time · O(log n) space""",
            "java": r"""// Generate decimal palindromes in order, keep the base-k ones
boolean isBaseKPalindrome(long value, int k) {
    List<Integer> digits = new ArrayList<>();
    while (value > 0) { digits.add((int) (value % k)); value /= k; }
    for (int i = 0, j = digits.size() - 1; i < j; i++, j--)
        if (!digits.get(i).equals(digits.get(j))) return false;
    return true;
}
long kMirror(int k, int n) {
    long total = 0;
    int found = 0;
    for (int length = 1; found < n; length++) {
        int halfLength = (length + 1) / 2;
        long start = 1;
        for (int i = 1; i < halfLength; i++) start *= 10;    // smallest half
        long end = start * 10;
        for (long half = start; half < end && found < n; half++) {
            String text = Long.toString(half), mirror = text;
            if (length % 2 == 1) mirror = mirror.substring(0, mirror.length() - 1);
            mirror = new StringBuilder(mirror).reverse().toString();
            long candidate = Long.parseLong(text + mirror);
            if (isBaseKPalindrome(candidate, k)) { total += candidate; found++; }
        }
    }
    return total;
}   // O(candidates · log_k n) time · O(log n) space""",
            "python": r"""def sum_of_k_mirror_numbers(k, n):
    def base_k_palindrome(value):
        digits = []
        while value:
            digits.append(value % k)
            value //= k
        return digits == digits[::-1]

    total = 0
    found = 0
    length = 1
    while found < n:
        half_length = (length + 1) // 2
        start = 10 ** (half_length - 1)          # smallest half of this length
        for half in range(start, start * 10):
            text = str(half)
            mirror = text[:-1][::-1] if length % 2 else text[::-1]
            candidate = int(text + mirror)       # a decimal palindrome, in order
            if base_k_palindrome(candidate):
                total += candidate
                found += 1
                if found == n:
                    break
        length += 1
    return total""",
        },
    },
    {
        "slug": "count-the-number-of-ideal-arrays",
        "title": "Count the Number of Ideal Arrays",
        "difficulty": "Hard",
        "pattern": "prime exponents + stars and bars",
        "statement": "An array of length n with values in [1, maxValue] is ideal when every element divides the next. Return the number of distinct ideal "
                     "arrays, modulo 10^9 + 7.",
        "examples": [("n = 2, maxValue = 5", "10"), ("n = 5, maxValue = 3", "11")],
        "constraints": ["2 <= n <= 10^4", "1 <= maxValue <= 10^4"],
        "approach": "A chain of divisions is a set of non-decreasing prime exponents, so fix the last value v and look at each prime in it. If v contains p "
                     "exponent e times, the e units of p spread across the n positions as a non-decreasing (equivalently, an ordered) distribution: "
                     "C(e + n - 1, e) ways. Multiplying those binomials over the primes of v and summing over all v counts every ideal array exactly once.",
        "complexity": ("O(maxValue · log maxValue) time", "O(maxValue)"),
        "code": {
            "cpp": r"""// Chains are non-decreasing prime exponents: C(e + n - 1, e) each
int idealArrays(int n, int maxValue) {
    const long long MOD = 1000000007;
    vector<int> smallestPrime(maxValue + 1);
    for (int v = 2; v <= maxValue; v++) smallestPrime[v] = v;
    for (long long p = 2; p * p <= maxValue; p++)
        if (smallestPrime[p] == p)                       // p is prime
            for (long long m = p * p; m <= maxValue; m += p)
                if (smallestPrime[m] == m) smallestPrime[m] = (int) p;
    int maxExponent = 1;
    for (int v = maxValue; v > 1; v >>= 1) maxExponent++;   // log2 of maxValue
    vector<long long> combinations(maxExponent + 1, 1);
    for (int e = 1; e <= maxExponent; e++)                   // C(e + n - 1, e)
        combinations[e] = combinations[e - 1] * (n + e - 1) % MOD * [&] {
            long long base = e, exponent = MOD - 2, result = 1;   // inverse of e
            while (exponent > 0) {
                if (exponent & 1) result = result * base % MOD;
                base = base * base % MOD;
                exponent >>= 1;
            }
            return result;
        }() % MOD;
    long long total = 0;
    for (int value = 1; value <= maxValue; value++) {
        long long ways = 1;
        int rest = value;
        while (rest > 1) {
            int p = smallestPrime[rest], exponent = 0;
            while (rest % p == 0) { rest /= p; exponent++; }
            ways = ways * combinations[exponent] % MOD;
        }
        total = (total + ways) % MOD;
    }
    return (int) total;
}   // O(maxValue log maxValue) time · O(maxValue) space""",
            "java": r"""// Chains are non-decreasing prime exponents: C(e + n - 1, e) each
int idealArrays(int n, int maxValue) {
    final long MOD = 1000000007L;
    int[] smallestPrime = new int[maxValue + 1];
    for (int v = 2; v <= maxValue; v++) smallestPrime[v] = v;
    for (long p = 2; p * p <= maxValue; p++)
        if (smallestPrime[(int) p] == p)                  // p is prime
            for (long m = p * p; m <= maxValue; m += p)
                if (smallestPrime[(int) m] == m) smallestPrime[(int) m] = (int) p;
    int maxExponent = 1;
    for (int v = maxValue; v > 1; v >>= 1) maxExponent++;  // log2 of maxValue
    long[] combinations = new long[maxExponent + 1];
    combinations[0] = 1;
    for (int e = 1; e <= maxExponent; e++)                 // C(e + n - 1, e)
        combinations[e] = combinations[e - 1] * (n + e - 1) % MOD * modInverse(e, MOD) % MOD;
    long total = 0;
    for (int value = 1; value <= maxValue; value++) {
        long ways = 1;
        int rest = value;
        while (rest > 1) {
            int p = smallestPrime[rest], exponent = 0;
            while (rest % p == 0) { rest /= p; exponent++; }
            ways = ways * combinations[exponent] % MOD;
        }
        total = (total + ways) % MOD;
    }
    return (int) total;
}
long modInverse(long value, long mod) {
    long result = 1, base = value, exponent = mod - 2;
    while (exponent > 0) {
        if ((exponent & 1) == 1) result = result * base % mod;
        base = base * base % mod;
        exponent >>= 1;
    }
    return result;
}   // O(maxValue log maxValue) time · O(maxValue) space""",
            "python": r"""def ideal_arrays(n, max_value):
    mod = 10**9 + 7
    smallest_prime = list(range(max_value + 1))
    for p in range(2, int(max_value ** 0.5) + 1):
        if smallest_prime[p] == p:                     # p is prime
            for multiple in range(p * p, max_value + 1, p):
                if smallest_prime[multiple] == multiple:
                    smallest_prime[multiple] = p
    max_exponent = max_value.bit_length()              # log2 of max_value
    combinations = [1] * (max_exponent + 1)
    for e in range(1, max_exponent + 1):               # C(e + n - 1, e)
        combinations[e] = combinations[e - 1] * (n + e - 1) % mod * pow(e, mod - 2, mod) % mod
    total = 0
    for value in range(1, max_value + 1):
        ways = 1
        rest = value
        while rest > 1:                                # factor using the sieve
            p = smallest_prime[rest]
            exponent = 0
            while rest % p == 0:
                rest //= p
                exponent += 1
            ways = ways * combinations[exponent] % mod
        total = (total + ways) % mod
    return total""",
        },
    },
    {
        "slug": "number-of-ways-to-reorder-array-to-get-same-bst",
        "title": "Number of Ways to Reorder Array to Get Same BST",
        "difficulty": "Hard",
        "pattern": "interleave left and right subtrees",
        "statement": "Return, modulo 10^9 + 7, how many permutations of nums build exactly the same binary search tree as the original order, excluding the "
                     "original order itself.",
        "examples": [("nums = [2,1,3]", "1"), ("nums = [3,4,5,1,2]", "5"), ("nums = [1,2,3]", "0")],
        "constraints": ["1 <= nums.length <= 1000", "1 <= nums[i] <= 10^9", "all values are distinct"],
        "approach": "The first element is always the root. Everything smaller than it keeps its relative order within the left subtree and everything "
                     "larger within the right, but the two groups may be interleaved freely: choose which of the remaining positions hold the left "
                     "group — C(n-1, leftSize) ways — and multiply by the counts inside each subtree. Add one at the end because the original order is "
                     "always counted and must be excluded.",
        "complexity": ("O(n²) time", "O(n²)"),
        "code": {
            "cpp": r"""// Interleave the two subtrees: C(n-1, left) per node
long long waysFor(const vector<int>& nums, const vector<vector<long long>>& choose) {
    if (nums.size() <= 1) return 1;
    vector<int> left, right;
    for (int i = 1; i < (int) nums.size(); i++) {
        if (nums[i] < nums[0]) left.push_back(nums[i]);
        else right.push_back(nums[i]);
    }
    long long interleavings = choose[nums.size() - 1][left.size()];
    return interleavings % 1000000007 * waysFor(left, choose) % 1000000007
                               * waysFor(right, choose) % 1000000007;
}
int numOfWays(vector<int>& nums) {
    const long long MOD = 1000000007;
    int n = nums.size();
    vector<vector<long long>> choose(n + 1, vector<long long>(n + 1, 0));
    for (int i = 0; i <= n; i++) {
        choose[i][0] = 1;
        for (int j = 1; j <= i; j++)
            choose[i][j] = (choose[i - 1][j - 1] + choose[i - 1][j]) % MOD;
    }
    return (int) ((waysFor(nums, choose) - 1 + MOD) % MOD);   // drop the original order
}   // O(n^2) time · O(n^2) space""",
            "java": r"""// Interleave the two subtrees: C(n-1, left) per node
long waysFor(List<Integer> nums, long[][] choose) {
    if (nums.size() <= 1) return 1;
    List<Integer> left = new ArrayList<>(), right = new ArrayList<>();
    for (int i = 1; i < nums.size(); i++) {
        if (nums.get(i) < nums.get(0)) left.add(nums.get(i));
        else right.add(nums.get(i));
    }
    long interleavings = choose[nums.size() - 1][left.size()];
    return interleavings % 1000000007 * waysFor(left, choose) % 1000000007
                               * waysFor(right, choose) % 1000000007;
}
int numOfWays(int[] nums) {
    final long MOD = 1000000007L;
    int n = nums.length;
    long[][] choose = new long[n + 1][n + 1];
    for (int i = 0; i <= n; i++) {
        choose[i][0] = 1;
        for (int j = 1; j <= i; j++)
            choose[i][j] = (choose[i - 1][j - 1] + choose[i - 1][j]) % MOD;
    }
    List<Integer> values = new ArrayList<>();
    for (int v : nums) values.add(v);
    return (int) ((waysFor(values, choose) - 1 + MOD) % MOD);   // drop the original order
}   // O(n^2) time · O(n^2) space""",
            "python": r"""def num_of_ways(nums):
    import sys
    sys.setrecursionlimit(10000)          # the tree can be 1000 deep
    mod = 10**9 + 7
    n = len(nums)
    choose = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        choose[i][0] = 1
        for j in range(1, i + 1):
            choose[i][j] = (choose[i - 1][j - 1] + choose[i - 1][j]) % mod

    def count(seq):
        if len(seq) <= 1:
            return 1
        left = [v for v in seq[1:] if v < seq[0]]
        right = [v for v in seq[1:] if v > seq[0]]
        ways = choose[len(seq) - 1][len(left)]     # interleave the two groups
        return ways * count(left) % mod * count(right) % mod

    return (count(nums) - 1) % mod        # the original order does not count""",
        },
    },
    {
        "slug": "count-of-integers",
        "title": "Count of Integers",
        "difficulty": "Hard",
        "pattern": "digit DP over a huge bound",
        "statement": "Count the integers in [num1, num2] whose digit sum lies between min_sum and max_sum, modulo 10^9 + 7. Both bounds are given as "
                     "strings and may be far larger than 64 bits.",
        "examples": [("num1 = \"1\", num2 = \"12\", min_sum = 1, max_sum = 8", "11"), ("num1 = \"1\", num2 = \"5\", min_sum = 1, max_sum = 5", "5")],
        "constraints": ["1 <= num1 <= num2 <= 10^22", "1 <= min_sum <= max_sum <= 400", "num1 and num2 have no leading zeros"],
        "approach": "Work with the decimal string of the bound and count by digit position with three states: where you are, the digit sum so far, and "
                     "whether the prefix still equals the bound. The bound-free part of that state is memoised, so the work is positions × sums rather "
                     "than the size of the numbers. Subtracting the count up to num1 with the count up to num2, then adding back num1's own "
                     "contribution, avoids doing arithmetic on 23-digit values.",
        "complexity": ("O(len(num2) · max_sum · 10) time", "O(len(num2) · max_sum)"),
        "code": {
            "cpp": r"""// Digit DP: position, digit sum so far, and how tight the prefix is
long long countUpTo(const string& bound, int limitSum) {
    // dp over prefixes: loose = prefix already below the bound, tight = still equal
    int length = bound.size();
    if (limitSum < 0) return 0;
    vector<long long> loose(limitSum + 1, 0), tight(limitSum + 1, 0);
    tight[0] = 1;
    for (int pos = 0; pos < length; pos++) {
        vector<long long> nextLoose(limitSum + 1, 0), nextTight(limitSum + 1, 0);
        int boundDigit = bound[pos] - '0';
        for (int sum = 0; sum <= limitSum; sum++) {
            if (tight[sum]) {
                for (int d = 0; d <= boundDigit; d++)
                    if (sum + d <= limitSum) {
                        if (d == boundDigit) nextTight[sum + d]++;
                        else nextLoose[sum + d]++;
                    }
            }
            if (loose[sum]) {
                for (int d = 0; d <= 9; d++)
                    if (sum + d <= limitSum) nextLoose[sum + d] = (nextLoose[sum + d] + loose[sum]) % 1000000007;
            }
        }
        for (int sum = 0; sum <= limitSum; sum++) {
            nextTight[sum] %= 1000000007;
            nextLoose[sum] %= 1000000007;
        }
        loose = nextLoose;
        tight = nextTight;
    }
    long long total = 0;
    for (int sum = 0; sum <= limitSum; sum++) total = (total + loose[sum] + tight[sum]) % 1000000007;
    return total;
}
int count(string num1, string num2, int min_sum, int max_sum) {
    const long long MOD = 1000000007;
    long long upToNum2 = (countUpTo(num2, max_sum) - countUpTo(num2, min_sum - 1) + MOD) % MOD;
    long long upToNum1 = (countUpTo(num1, max_sum) - countUpTo(num1, min_sum - 1) + MOD) % MOD;
    int ownSum = 0;
    for (char ch : num1) ownSum += ch - '0';
    long long total = (upToNum2 - upToNum1 + MOD) % MOD;
    if (min_sum <= ownSum && ownSum <= max_sum) total = (total + 1) % MOD;   // num1 itself
    return (int) total;
}   // O(len · max_sum · 10) time · O(max_sum) space""",
            "java": r"""// Digit DP: position, digit sum so far, and how tight the prefix is
long countUpTo(String bound, int limitSum) {
    // dp over prefixes: loose = prefix already below the bound, tight = still equal
    int length = bound.length();
    if (limitSum < 0) return 0;
    long[] loose = new long[limitSum + 1], tight = new long[limitSum + 1];
    tight[0] = 1;
    for (int pos = 0; pos < length; pos++) {
        long[] nextLoose = new long[limitSum + 1], nextTight = new long[limitSum + 1];
        int boundDigit = bound.charAt(pos) - '0';
        for (int sum = 0; sum <= limitSum; sum++) {
            if (tight[sum] != 0) {
                for (int d = 0; d <= boundDigit && sum + d <= limitSum; d++) {
                    if (d == boundDigit) nextTight[sum + d]++;
                    else nextLoose[sum + d]++;
                }
            }
            if (loose[sum] != 0) {
                for (int d = 0; d <= 9 && sum + d <= limitSum; d++)
                    nextLoose[sum + d] = (nextLoose[sum + d] + loose[sum]) % 1000000007L;
            }
        }
        for (int sum = 0; sum <= limitSum; sum++) {
            nextTight[sum] %= 1000000007L;
            nextLoose[sum] %= 1000000007L;
        }
        loose = nextLoose;
        tight = nextTight;
    }
    long total = 0;
    for (int sum = 0; sum <= limitSum; sum++) total = (total + loose[sum] + tight[sum]) % 1000000007L;
    return total;
}
int count(String num1, String num2, int min_sum, int max_sum) {
    final long MOD = 1000000007L;
    long upToNum2 = (countUpTo(num2, max_sum) - countUpTo(num2, min_sum - 1) + MOD) % MOD;
    long upToNum1 = (countUpTo(num1, max_sum) - countUpTo(num1, min_sum - 1) + MOD) % MOD;
    int ownSum = 0;
    for (char ch : num1.toCharArray()) ownSum += ch - '0';
    long total = (upToNum2 - upToNum1 + MOD) % MOD;
    if (min_sum <= ownSum && ownSum <= max_sum) total = (total + 1) % MOD;   // num1 itself
    return (int) total;
}   // O(len · max_sum · 10) time · O(max_sum) space""",
            "python": r"""def count_of_integers(num1, num2, min_sum, max_sum):
    mod = 10**9 + 7

    def count_up_to(bound, limit):
        if limit < 0:
            return 0
        length = len(bound)
        loose = [0] * (limit + 1)          # prefix already below the bound
        tight = [0] * (limit + 1)          # prefix still equal to the bound
        tight[0] = 1
        for pos in range(length):
            next_loose = [0] * (limit + 1)
            next_tight = [0] * (limit + 1)
            bound_digit = int(bound[pos])
            for total in range(limit + 1):
                if tight[total]:
                    for d in range(min(bound_digit, limit - total) + 1):
                        if d == bound_digit:
                            next_tight[total + d] += 1
                        else:
                            next_loose[total + d] += 1
                if loose[total]:
                    for d in range(min(9, limit - total) + 1):
                        next_loose[total + d] = (next_loose[total + d] + loose[total]) % mod
            loose = [v % mod for v in next_loose]
            tight = [v % mod for v in next_tight]
        return (sum(loose) + sum(tight)) % mod

    counted = (count_up_to(num2, max_sum) - count_up_to(num2, min_sum - 1)
               - count_up_to(num1, max_sum) + count_up_to(num1, min_sum - 1)) % mod
    own_sum = sum(int(ch) for ch in num1)
    if min_sum <= own_sum <= max_sum:
        counted = (counted + 1) % mod      # num1 is counted twice in the subtraction
    return counted""",
        },
    },
    {
        "slug": "find-the-closest-palindrome",
        "title": "Find the Closest Palindrome",
        "difficulty": "Hard",
        "pattern": "mirror the half, check the neighbours",
        "statement": "Given n as a decimal string, return the closest integer (as a string) that is a palindrome and not equal to n. On a tie, return the "
                     "smaller one.",
        "examples": [("n = \"123\"", "\"121\""), ("n = \"1\"", "\"0\"")],
        "constraints": ["1 <= len(n) <= 18", "n has no leading zeros", "the answer must not have leading zeros"],
        "approach": "Any palindrome is decided by its first half, so the answer lies near the palindrome built from n's first half — but the half might "
                     "need to go up or down by one, which is why both neighbours are tried. Two extra candidates cover the length changes: "
                     "9…9 (one digit shorter) and 1 0…0 1, and when nothing else fits these are what carry the answer across a power of ten.",
        "complexity": ("O(len(n)) time", "O(len(n))"),
        "code": {
            "cpp": r"""// Mirror the first half, then also try its two neighbours
string nearestPalindromic(string n) {
    int length = n.size();
    long long value = stoll(n);
    set<long long> candidates;
    candidates.insert(stoll("1" + string(length - 1, '0') + "1"));   // 1 0…0 1
    candidates.insert(length > 1 ? stoll(string(length - 1, '9')) : 0LL);   // 9…9
    long long half = stoll(n.substr(0, (length + 1) / 2));
    for (long long h = half - 1; h <= half + 1; h++) {
        if (h <= 0) continue;
        string left = to_string(h), right = left;
        if (length % 2 == 1) right.pop_back();                       // drop the middle
        reverse(right.begin(), right.end());
        candidates.insert(stoll(left + right));
    }
    long long best = -1;
    for (long long candidate : candidates) {
        if (candidate == value) continue;
        if (best == -1 || llabs(candidate - value) < llabs(best - value) ||
            (llabs(candidate - value) == llabs(best - value) && candidate < best))
            best = candidate;
    }
    return to_string(best);
}   // O(len(n)) time · O(len(n)) space""",
            "java": r"""// Mirror the first half, then also try its two neighbours
String nearestPalindromic(String n) {
    int length = n.length();
    long value = Long.parseLong(n);
    TreeSet<Long> candidates = new TreeSet<>();
    candidates.add(Long.parseLong("1" + "0".repeat(length - 1) + "1"));   // 1 0…0 1
    candidates.add(length > 1 ? Long.parseLong("9".repeat(length - 1)) : 0L);   // 9…9
    long half = Long.parseLong(n.substring(0, (length + 1) / 2));
    for (long h = half - 1; h <= half + 1; h++) {
        if (h <= 0) continue;
        String left = Long.toString(h), right = left;
        if (length % 2 == 1) right = right.substring(0, right.length() - 1);
        right = new StringBuilder(right).reverse().toString();
        candidates.add(Long.parseLong(left + right));
    }
    long best = -1;
    for (long candidate : candidates) {
        if (candidate == value) continue;
        if (best == -1 || Math.abs(candidate - value) < Math.abs(best - value) ||
            (Math.abs(candidate - value) == Math.abs(best - value) && candidate < best))
            best = candidate;
    }
    return Long.toString(best);
}   // O(len(n)) time · O(len(n)) space""",
            "python": r"""def nearest_palindromic(n):
    length = len(n)
    value = int(n)
    candidates = set()
    candidates.add(int("1" + "0" * (length - 1) + "1"))     # 1 0…0 1
    candidates.add(int("9" * (length - 1)) if length > 1 else 0)   # 9…9
    half = int(n[:(length + 1) // 2])
    for h in (half - 1, half, half + 1):
        if h <= 0:
            continue
        left = str(h)
        right = left[:-1] if length % 2 else left           # drop the middle digit
        candidates.add(int(left + right[::-1]))
    best = None
    for candidate in candidates:
        if candidate == value:
            continue
        if (best is None or abs(candidate - value) < abs(best - value)
                or (abs(candidate - value) == abs(best - value) and candidate < best)):
            best = candidate
    return str(best)""",
        },
    },
]
