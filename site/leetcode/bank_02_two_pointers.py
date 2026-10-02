# Topic 2 · Two Pointers & Sliding Window
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.

TOPIC = {
    "name": "Two Pointers & Sliding Window",
    "tagline": "One pass with two indices instead of two nested loops — the single highest-yield pattern in interviews.",
    "focus": "Recognising when a window or a pair of pointers can replace an O(n²) search: monotone predicates for "
             "windows, sorted-order arguments for opposite-end pointers, and the counting structures that make a "
             "window's state updatable in O(1) per step.",
    "ordering": "easy 1–6 are fixed windows and opposite-end pointers on sorted data; medium 1–3 are variable windows "
                "with one rule, 4–6 extend opposite-end pointers to k-sum, 7–9 add a counting structure to the window, "
                "10–12 are window counting and greedy two-pointer merge; hard 1–4 are the classic advanced windows, "
                "5–8 need a second structure or a proof, 9–12 are competition-level variants.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "two-sum-sorted",
        "title": "Two Sum in a Sorted Array",
        "difficulty": "Easy",
        "pattern": "opposite-end pointers",
        "statement": "Given a 1-indexed array sorted in non-decreasing order, return the two indices (1-based, smaller "
                     "first) of the values that add up to `target`. Exactly one solution exists and you may not use the "
                     "same element twice.",
        "examples": [("[2,7,11,15], target = 9", "[1,2]"),
                     ("[2,3,4], target = 6", "[1,3]")],
        "constraints": ["2 <= n <= 3 * 10^4", "the array is sorted ascending", "exactly one valid pair exists"],
        "approach": "Start with the smallest and largest values. If their sum is too small, no partner for the smallest "
                    "value can work (every other value is larger), so move the left pointer; if too large, move the "
                    "right. The sorted order is what turns an O(n²) pair search into O(n) — this argument is the heart "
                    "of every two-pointer solution.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Sorted input: the pointer move is justified by the order
vector<int> twoSumSorted(const vector<int>& a, int target) {
    int i = 0, j = (int)a.size() - 1;
    while (i < j) {
        int sum = a[i] + a[j];
        if (sum == target) return {i + 1, j + 1};   // 1-based indices
        if (sum < target) i++;                      // need a bigger value
        else j--;                                   // need a smaller value
    }
    return {};                                      // unreachable for valid input
}   // O(n) time · O(1) space""",
            "java": r"""// Sorted input: the pointer move is justified by the order
int[] twoSumSorted(int[] a, int target) {
    int i = 0, j = a.length - 1;
    while (i < j) {
        int sum = a[i] + a[j];
        if (sum == target) return new int[]{i + 1, j + 1};   // 1-based indices
        if (sum < target) i++;                               // need a bigger value
        else j--;                                            // need a smaller value
    }
    return new int[0];                                       // unreachable for valid input
}   // O(n) time · O(1) space""",
            "python": r"""def two_sum_sorted(a, target):
    i, j = 0, len(a) - 1
    while i < j:
        s = a[i] + a[j]
        if s == target:
            return [i + 1, j + 1]        # 1-based indices
        if s < target:
            i += 1                       # need a bigger value
        else:
            j -= 1                       # need a smaller value
    return []
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "remove-element-in-place",
        "title": "Remove All Occurrences of a Value In Place",
        "difficulty": "Easy",
        "pattern": "write pointer (slow/fast)",
        "statement": "Remove every occurrence of `val` from the array in place and return the new length k. The first k "
                     "elements must be the kept values; the order of the others does not matter.",
        "examples": [("[3,2,2,3], val = 3", "k = 2, array starts [2,2]"),
                     ("[0,1,2,2,3,0,4,2], val = 2", "k = 5, array starts [0,1,3,0,4]")],
        "constraints": ["0 <= n <= 100", "0 <= a[i], val <= 50"],
        "approach": "A slow pointer marks where the next kept value goes while a fast pointer scans. When the fast value "
                    "is not `val`, copy it to the slow slot and advance both; otherwise advance only the fast pointer. "
                    "One pass, no extra memory, and it works for the whole family of \"remove/compact in place\" tasks.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Slow pointer writes, fast pointer reads
int removeElement(vector<int>& a, int val) {
    int w = 0;
    for (int v : a) if (v != val) a[w++] = v;
    return w;                       // a[0..w-1] holds the kept values
}   // O(n) time · O(1) space""",
            "java": r"""// Slow pointer writes, fast pointer reads
int removeElement(int[] a, int val) {
    int w = 0;
    for (int v : a) if (v != val) a[w++] = v;
    return w;                       // a[0..w-1] holds the kept values
}   // O(n) time · O(1) space""",
            "python": r"""def remove_element(a, val):
    w = 0
    for v in a:
        if v != val:
            a[w] = v
            w += 1
    return w                       # a[:w] holds the kept values
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "merge-two-sorted-arrays",
        "title": "Merge Two Sorted Arrays Into a New Array",
        "difficulty": "Easy",
        "pattern": "two read pointers, one write pointer",
        "statement": "Given two sorted arrays, return a single sorted array containing all their elements (duplicates "
                     "included).",
        "examples": [("[1,3,5], [2,4,6]", "[1,2,3,4,5,6]"),
                     ("[], [1,2]", "[1,2]")],
        "constraints": ["0 <= m, n <= 10^4", "both inputs are sorted ascending"],
        "approach": "Advance the pointer of the array holding the smaller current value and append that value. When one "
                    "array is exhausted, append the whole remainder of the other. The two-pointer merge is also the "
                    "engine inside merge sort and inside every \"merge k sorted\" problem.",
        "complexity": ("O(m + n)", "O(m + n) for the output"),
        "code": {
            "cpp": r"""// Merge by always taking the smaller current head
vector<int> mergeSorted(const vector<int>& a, const vector<int>& b) {
    vector<int> out;
    out.reserve(a.size() + b.size());
    int i = 0, j = 0;
    while (i < (int)a.size() && j < (int)b.size())
        out.push_back(a[i] <= b[j] ? a[i++] : b[j++]);   // <= keeps it stable
    while (i < (int)a.size()) out.push_back(a[i++]);
    while (j < (int)b.size()) out.push_back(b[j++]);
    return out;
}   // O(m+n) time · O(m+n) space""",
            "java": r"""// Merge by always taking the smaller current head
int[] mergeSorted(int[] a, int[] b) {
    int[] out = new int[a.length + b.length];
    int i = 0, j = 0, k = 0;
    while (i < a.length && j < b.length) out[k++] = a[i] <= b[j] ? a[i++] : b[j++];
    while (i < a.length) out[k++] = a[i++];
    while (j < b.length) out[k++] = b[j++];
    return out;
}   // O(m+n) time · O(m+n) space""",
            "python": r"""def merge_sorted(a, b):
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:            # '<=' keeps the merge stable
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return out
# O(m + n) time · O(m + n) space""",
        },
    },
    {
        "slug": "is-subsequence",
        "title": "Is One String a Subsequence of Another?",
        "difficulty": "Easy",
        "pattern": "one pointer per string",
        "statement": "Return true if `s` is a subsequence of `t`, meaning every character of `s` appears in `t` in the "
                     "same relative order (not necessarily contiguously).",
        "examples": [("s = \"abc\", t = \"ahbgdc\"", "true"),
                     ("s = \"axc\", t = \"ahbgdc\"", "false")],
        "constraints": ["0 <= length(s) <= 100", "0 <= length(t) <= 10^4"],
        "approach": "Walk `t` with one pointer and `s` with another: every time the characters match, advance the `s` "
                    "pointer. If it reaches the end of `s`, the answer is true. This is the \"greedy matching\" form of "
                    "two pointers and generalises to merging, diffing and edit-distance problems.",
        "complexity": ("O(|t|)", "O(1)"),
        "code": {
            "cpp": r"""// Greedy: match s left to right inside t
bool isSubsequence(const string& s, const string& t) {
    int i = 0;
    for (int j = 0; i < (int)s.size() && j < (int)t.size(); j++)
        if (s[i] == t[j]) i++;              // matched one more character of s
    return i == (int)s.size();
}   // O(|t|) time · O(1) space""",
            "java": r"""// Greedy: match s left to right inside t
boolean isSubsequence(String s, String t) {
    int i = 0;
    for (int j = 0; i < s.length() && j < t.length(); j++)
        if (s.charAt(i) == t.charAt(j)) i++;   // matched one more character of s
    return i == s.length();
}   // O(|t|) time · O(1) space""",
            "python": r"""def is_subsequence(s, t):
    i = 0
    for ch in t:                     # greedy match through t
        if i < len(s) and s[i] == ch:
            i += 1
    return i == len(s)
# O(|t|) time · O(1) space

# one-liner using the iterator protocol:
# it = iter(t); return all(c in it for c in s)""",
        },
    },
    {
        "slug": "max-average-subarray-k",
        "title": "Maximum Average Subarray of Fixed Size k",
        "difficulty": "Easy",
        "pattern": "fixed-size sliding window",
        "statement": "Given an array and an integer k, return the maximum average of any contiguous subarray of length "
                     "exactly k.",
        "examples": [("[1,12,-5,-6,50,3], k = 4", "12.75   (from [12,-5,-6,50])"),
                     ("[5], k = 1", "5.0")],
        "constraints": ["1 <= k <= n <= 10^5", "-10^4 <= a[i] <= 10^4"],
        "approach": "Compute the first window's sum, then slide: add the incoming element and subtract the outgoing one. "
                    "Never recompute the window from scratch. Track the best sum and divide once at the end (dividing "
                    "inside the loop wastes time and adds rounding noise).",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Slide the sum: add the entering element, remove the leaving one
double findMaxAverage(const vector<int>& a, int k) {
    long long sum = 0;
    for (int i = 0; i < k; i++) sum += a[i];
    long long best = sum;
    for (int i = k; i < (int)a.size(); i++) {
        sum += a[i] - a[i - k];          // slide one step
        best = max(best, sum);
    }
    return (double)best / k;             // divide once, at the end
}   // O(n) time · O(1) space""",
            "java": r"""// Slide the sum: add the entering element, remove the leaving one
double findMaxAverage(int[] a, int k) {
    long sum = 0;
    for (int i = 0; i < k; i++) sum += a[i];
    long best = sum;
    for (int i = k; i < a.length; i++) {
        sum += a[i] - a[i - k];          // slide one step
        best = Math.max(best, sum);
    }
    return (double) best / k;            // divide once, at the end
}   // O(n) time · O(1) space""",
            "python": r"""def find_max_average(a, k):
    window = sum(a[:k])                  # first window
    best = window
    for i in range(k, len(a)):
        window += a[i] - a[i - k]        # slide one step
        best = max(best, window)
    return best / k                      # divide once, at the end
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "squares-of-sorted-array",
        "title": "Squares of a Sorted Array, Also Sorted",
        "difficulty": "Easy",
        "pattern": "opposite-end pointers filling from the back",
        "statement": "Given an array sorted in non-decreasing order (possibly containing negatives), return the array of "
                     "squares, sorted in non-decreasing order, in O(n) time.",
        "examples": [("[-4,-1,0,3,10]", "[0,1,9,16,100]"),
                     ("[-7,-3,2,3,11]", "[4,9,9,49,121]")],
        "constraints": ["1 <= n <= 10^4", "-10^4 <= a[i] <= 10^4", "the input is sorted ascending"],
        "approach": "The largest square comes from whichever end has the larger absolute value. Walk two pointers inward "
                    "and fill the output from the back, so each step places the next-largest square. Squaring is not "
                    "monotone across sign changes, which is why a single left-to-right pass fails.",
        "complexity": ("O(n)", "O(n) for the output"),
        "code": {
            "cpp": r"""// Fill from the back: the biggest square is at one of the two ends
vector<int> sortedSquares(const vector<int>& a) {
    int n = a.size();
    vector<int> out(n);
    int i = 0, j = n - 1;
    for (int k = n - 1; k >= 0; k--) {
        long long li = (long long)a[i] * a[i], rj = (long long)a[j] * a[j];
        if (li > rj) { out[k] = (int)li; i++; }
        else         { out[k] = (int)rj; j--; }
    }
    return out;
}   // O(n) time · O(n) space""",
            "java": r"""// Fill from the back: the biggest square is at one of the two ends
int[] sortedSquares(int[] a) {
    int n = a.length;
    int[] out = new int[n];
    int i = 0, j = n - 1;
    for (int k = n - 1; k >= 0; k--) {
        long li = (long) a[i] * a[i], rj = (long) a[j] * a[j];
        if (li > rj) { out[k] = (int) li; i++; }
        else         { out[k] = (int) rj; j--; }
    }
    return out;
}   // O(n) time · O(n) space""",
            "python": r"""def sorted_squares(a):
    n = len(a)
    out = [0] * n
    i, j = 0, n - 1
    for k in range(n - 1, -1, -1):        # fill from the largest square down
        li, rj = a[i] * a[i], a[j] * a[j]
        if li > rj:
            out[k] = li; i += 1
        else:
            out[k] = rj; j -= 1
    return out
# O(n) time · O(n) space""",
        },
    },

    # ---------------------------------------------------------------- MEDIUM
    {
        "slug": "longest-substring-no-repeat",
        "title": "Longest Substring Without Repeating Characters",
        "difficulty": "Medium",
        "pattern": "variable window + last-seen index map",
        "statement": "Return the length of the longest substring of `s` that contains no repeated character.",
        "examples": [("\"abcabcbb\"", "3   (\"abc\")"),
                     ("\"bbbbb\"", "1"),
                     ("\"pwwkew\"", "3   (\"wke\")")],
        "constraints": ["0 <= length <= 5 * 10^4", "the string contains letters, digits, symbols and spaces"],
        "approach": "Grow the window with the right pointer. When the incoming character was last seen inside the current "
                    "window, jump the left pointer just past that occurrence — one move, not a while loop — and update "
                    "the last-seen table. Each index is touched twice, so the cost is linear.",
        "complexity": ("O(n)", "O(min(n, alphabet))"),
        "code": {
            "cpp": r"""// Jump left past the previous occurrence of the entering character
int lengthOfLongestSubstring(const string& s) {
    vector<int> last(256, -1);            // last index of each character
    int left = 0, best = 0;
    for (int right = 0; right < (int)s.size(); right++) {
        unsigned char c = s[right];
        if (last[c] >= left) left = last[c] + 1;   // shrink in one jump
        last[c] = right;
        best = max(best, right - left + 1);
    }
    return best;
}   // O(n) time · O(1) space (fixed alphabet)""",
            "java": r"""// Jump left past the previous occurrence of the entering character
int lengthOfLongestSubstring(String s) {
    int[] last = new int[128];
    Arrays.fill(last, -1);                // last index of each character
    int left = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        if (last[c] >= left) left = last[c] + 1;   // shrink in one jump
        last[c] = right;
        best = Math.max(best, right - left + 1);
    }
    return best;
}   // O(n) time · O(1) space (fixed alphabet)""",
            "python": r"""def length_of_longest_substring(s):
    last = {}                      # character -> last index seen
    left = best = 0
    for right, ch in enumerate(s):
        if last.get(ch, -1) >= left:
            left = last[ch] + 1    # jump past the previous occurrence
        last[ch] = right
        best = max(best, right - left + 1)
    return best
# O(n) time · O(min(n, alphabet)) space""",
        },
    },
    {
        "slug": "min-size-subarray-sum",
        "title": "Minimum Size Subarray With Sum at Least Target",
        "difficulty": "Medium",
        "pattern": "variable window with a while-shrink",
        "statement": "Given an array of positive integers and a target, return the length of the shortest contiguous "
                     "subarray whose sum is at least `target`, or 0 if none exists.",
        "examples": [("target = 7, [2,3,1,2,4,3]", "2   ([4,3])"),
                     ("target = 4, [1,4,4]", "1"),
                     ("target = 11, [1,1,1,1,1,1,1,1]", "0")],
        "constraints": ["1 <= n <= 10^5", "1 <= a[i] <= 10^4", "1 <= target <= 10^9"],
        "approach": "All values are positive, so the window sum is monotone in its width: extending can only help, "
                    "shrinking can only hurt. Expand on the right; while the sum is sufficient, record the length and "
                    "shrink from the left. The positivity assumption is what makes the single pass correct.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Positive values -> the sum is monotone in window width
int minSubArrayLen(int target, const vector<int>& a) {
    long long sum = 0;
    int left = 0, best = INT_MAX;
    for (int right = 0; right < (int)a.size(); right++) {
        sum += a[right];
        while (sum >= target) {                     // the window is valid: try to shrink
            best = min(best, right - left + 1);
            sum -= a[left++];
        }
    }
    return best == INT_MAX ? 0 : best;
}   // O(n) time · O(1) space""",
            "java": r"""// Positive values -> the sum is monotone in window width
int minSubArrayLen(int target, int[] a) {
    long sum = 0;
    int left = 0, best = Integer.MAX_VALUE;
    for (int right = 0; right < a.length; right++) {
        sum += a[right];
        while (sum >= target) {                     // the window is valid: try to shrink
            best = Math.min(best, right - left + 1);
            sum -= a[left++];
        }
    }
    return best == Integer.MAX_VALUE ? 0 : best;
}   // O(n) time · O(1) space""",
            "python": r"""def min_subarray_len(target, a):
    total = 0
    left = 0
    best = float("inf")
    for right, v in enumerate(a):
        total += v
        while total >= target:            # valid window: shrink and record
            best = min(best, right - left + 1)
            total -= a[left]
            left += 1
    return 0 if best == float("inf") else best
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "longest-substring-k-distinct",
        "title": "Longest Substring With At Most k Distinct Characters",
        "difficulty": "Medium",
        "pattern": "variable window + frequency map",
        "statement": "Return the length of the longest substring that contains at most k distinct characters.",
        "examples": [("s = \"eceba\", k = 2", "3   (\"ece\")"),
                     ("s = \"aa\", k = 1", "2"),
                     ("s = \"abcadcacacaca\", k = 3", "8")],
        "constraints": ["0 <= length <= 5 * 10^4", "0 <= k <= 50"],
        "approach": "This is the general template: maintain a frequency map for the window and shrink from the left while "
                    "the window violates the rule (`map.size() > k`). Deleting the entry when its count hits zero is what "
                    "keeps `size()` meaningful — the classic bug is leaving zero-counts in the map.",
        "complexity": ("O(n)", "O(k)"),
        "code": {
            "cpp": r"""// The general variable-window template
int lengthOfLongestSubstringKDistinct(const string& s, int k) {
    if (k == 0) return 0;
    unordered_map<char,int> cnt;
    int left = 0, best = 0;
    for (int right = 0; right < (int)s.size(); right++) {
        cnt[s[right]]++;
        while ((int)cnt.size() > k) {                 // too many distinct characters
            char c = s[left++];
            if (--cnt[c] == 0) cnt.erase(c);          // remove the key, not just the count
        }
        best = max(best, right - left + 1);
    }
    return best;
}   // O(n) time · O(k) space""",
            "java": r"""// The general variable-window template
int lengthOfLongestSubstringKDistinct(String s, int k) {
    if (k == 0) return 0;
    Map<Character,Integer> cnt = new HashMap<>();
    int left = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        char c = s.charAt(right);
        cnt.merge(c, 1, Integer::sum);
        while (cnt.size() > k) {                      // too many distinct characters
            char d = s.charAt(left++);
            if (cnt.merge(d, -1, Integer::sum) == 0) cnt.remove(d);   // drop zero counts
        }
        best = Math.max(best, right - left + 1);
    }
    return best;
}   // O(n) time · O(k) space""",
            "python": r"""from collections import defaultdict

def length_of_longest_k_distinct(s, k):
    if k == 0:
        return 0
    cnt = defaultdict(int)
    left = best = 0
    for right, ch in enumerate(s):
        cnt[ch] += 1
        while len(cnt) > k:                 # violation: shrink
            out = s[left]
            left += 1
            cnt[out] -= 1
            if cnt[out] == 0:
                del cnt[out]                # drop the key, not just the count
        best = max(best, right - left + 1)
    return best
# O(n) time · O(k) space""",
        },
    },
    {
        "slug": "three-sum",
        "title": "3Sum — All Unique Triples Summing to Zero",
        "difficulty": "Medium",
        "pattern": "sort + fix one, two-pointers the rest",
        "statement": "Return all unique triples (a, b, c) from the array with a + b + c = 0. The solution set must not "
                     "contain duplicate triples.",
        "examples": [("[-1,0,1,2,-1,-4]", "[[-1,-1,2],[-1,0,1]]"),
                     ("[0,0,0]", "[[0,0,0]]"),
                     ("[1,2,-2]", "[]")],
        "constraints": ["3 <= n <= 3000", "-10^5 <= a[i] <= 10^5"],
        "approach": "Sort, then fix the smallest element of each triple and solve the remaining two-sum with pointers. "
                    "Two skips keep the output duplicate-free: skip equal first elements, and after finding a pair skip "
                    "equal pointer values. Sorting costs O(n log n) but makes the duplicate handling trivial.",
        "complexity": ("O(n²)", "O(1) besides the output"),
        "code": {
            "cpp": r"""// Sort, fix one element, two-pointer the remaining pair
vector<vector<int>> threeSum(vector<int> a) {
    sort(a.begin(), a.end());
    int n = a.size();
    vector<vector<int>> out;
    for (int i = 0; i + 2 < n; i++) {
        if (i > 0 && a[i] == a[i - 1]) continue;        // skip duplicate first elements
        if ((long long)a[i] + a[i + 1] + a[i + 2] > 0) break;   // smallest possible triple already too big
        int l = i + 1, r = n - 1;
        while (l < r) {
            long long s = (long long)a[i] + a[l] + a[r];
            if (s < 0) l++;
            else if (s > 0) r--;
            else {
                out.push_back({a[i], a[l], a[r]});
                while (l < r && a[l] == a[l + 1]) l++;   // skip duplicates of the second value
                while (l < r && a[r] == a[r - 1]) r--;
                l++; r--;
            }
        }
    }
    return out;
}   // O(n^2) time · O(1) extra space""",
            "java": r"""// Sort, fix one element, two-pointer the remaining pair
List<List<Integer>> threeSum(int[] a) {
    Arrays.sort(a);
    int n = a.length;
    List<List<Integer>> out = new ArrayList<>();
    for (int i = 0; i + 2 < n; i++) {
        if (i > 0 && a[i] == a[i - 1]) continue;                 // skip duplicate first elements
        if ((long) a[i] + a[i + 1] + a[i + 2] > 0) break;        // even the smallest triple is too big
        int l = i + 1, r = n - 1;
        while (l < r) {
            long s = (long) a[i] + a[l] + a[r];
            if (s < 0) l++;
            else if (s > 0) r--;
            else {
                out.add(Arrays.asList(a[i], a[l], a[r]));
                while (l < r && a[l] == a[l + 1]) l++;           // skip duplicates of the second value
                while (l < r && a[r] == a[r - 1]) r--;
                l++; r--;
            }
        }
    }
    return out;
}   // O(n^2) time · O(1) extra space""",
            "python": r"""def three_sum(a):
    a.sort()
    n = len(a)
    out = []
    for i in range(n - 2):
        if i > 0 and a[i] == a[i - 1]:
            continue                          # skip duplicate first elements
        if a[i] + a[i + 1] + a[i + 2] > 0:
            break                             # smallest triple already positive
        l, r = i + 1, n - 1
        while l < r:
            s = a[i] + a[l] + a[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                out.append([a[i], a[l], a[r]])
                while l < r and a[l] == a[l + 1]: l += 1
                while l < r and a[r] == a[r - 1]: r -= 1
                l += 1; r -= 1
    return out
# O(n^2) time · O(1) extra space""",
        },
    },
    {
        "slug": "three-sum-closest",
        "title": "3Sum Closest to a Target",
        "difficulty": "Medium",
        "pattern": "sort + pointers with a running best",
        "statement": "Find the triple whose sum is closest to `target` and return that sum. Exactly one answer is "
                     "guaranteed to be optimal.",
        "examples": [("[-1,2,1,-4], target = 1", "2   (-1 + 2 + 1)"),
                     ("[0,0,0], target = 1", "0")],
        "constraints": ["3 <= n <= 500", "-10^3 <= a[i] <= 10^3", "-10^4 <= target <= 10^4"],
        "approach": "Same skeleton as 3Sum, but there is no equality to stop at — instead keep the sum with the smallest "
                    "absolute distance to the target, and move the pointers according to which side of the target the "
                    "current sum falls on. Early exit is possible when the distance reaches zero.",
        "complexity": ("O(n²)", "O(1)"),
        "code": {
            "cpp": r"""// Track the closest sum instead of an exact match
int threeSumClosest(vector<int> a, int target) {
    sort(a.begin(), a.end());
    int n = a.size();
    long long best = (long long)a[0] + a[1] + a[2];
    for (int i = 0; i + 2 < n; i++) {
        int l = i + 1, r = n - 1;
        while (l < r) {
            long long s = (long long)a[i] + a[l] + a[r];
            if (llabs(s - target) < llabs(best - target)) best = s;
            if (s < target) l++;
            else if (s > target) r--;
            else return (int)s;                     // exact hit: nothing can be closer
        }
    }
    return (int)best;
}   // O(n^2) time · O(1) space""",
            "java": r"""// Track the closest sum instead of an exact match
int threeSumClosest(int[] a, int target) {
    Arrays.sort(a);
    int n = a.length;
    long best = (long) a[0] + a[1] + a[2];
    for (int i = 0; i + 2 < n; i++) {
        int l = i + 1, r = n - 1;
        while (l < r) {
            long s = (long) a[i] + a[l] + a[r];
            if (Math.abs(s - target) < Math.abs(best - target)) best = s;
            if (s < target) l++;
            else if (s > target) r--;
            else return (int) s;                    // exact hit: nothing can be closer
        }
    }
    return (int) best;
}   // O(n^2) time · O(1) space""",
            "python": r"""def three_sum_closest(a, target):
    a.sort()
    n = len(a)
    best = a[0] + a[1] + a[2]
    for i in range(n - 2):
        l, r = i + 1, n - 1
        while l < r:
            s = a[i] + a[l] + a[r]
            if abs(s - target) < abs(best - target):
                best = s
            if s < target:
                l += 1
            elif s > target:
                r -= 1
            else:
                return s            # exact hit
    return best
# O(n^2) time · O(1) space""",
        },
    },
    {
        "slug": "four-sum",
        "title": "4Sum — Unique Quadruples Summing to Target",
        "difficulty": "Medium",
        "pattern": "two fixed loops + two pointers + duplicate skips",
        "statement": "Return all unique quadruples (a, b, c, d) from the array whose sum equals `target`.",
        "examples": [("[1,0,-1,0,-2,2], target = 0", "[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]"),
                     ("[2,2,2,2,2], target = 8", "[[2,2,2,2]]")],
        "constraints": ["1 <= n <= 200", "-10^9 <= a[i] <= 10^9", "-10^9 <= target <= 10^9"],
        "approach": "Extend the 3Sum recipe by one level: sort, fix the first two values with nested loops, then use two "
                    "pointers for the remaining pair. Each loop needs its own duplicate skip, and all arithmetic must be "
                    "done in 64-bit because values reach 10^9.",
        "complexity": ("O(n³)", "O(1) besides the output"),
        "code": {
            "cpp": r"""// Two fixed loops + two pointers; 64-bit sums are mandatory
vector<vector<int>> fourSum(vector<int> a, long long target) {
    sort(a.begin(), a.end());
    int n = a.size();
    vector<vector<int>> out;
    for (int i = 0; i + 3 < n; i++) {
        if (i > 0 && a[i] == a[i - 1]) continue;
        for (int j = i + 1; j + 2 < n; j++) {
            if (j > i + 1 && a[j] == a[j - 1]) continue;
            int l = j + 1, r = n - 1;
            while (l < r) {
                long long s = (long long)a[i] + a[j] + a[l] + a[r];
                if (s < target) l++;
                else if (s > target) r--;
                else {
                    out.push_back({a[i], a[j], a[l], a[r]});
                    while (l < r && a[l] == a[l + 1]) l++;
                    while (l < r && a[r] == a[r - 1]) r--;
                    l++; r--;
                }
            }
        }
    }
    return out;
}   // O(n^3) time · O(1) extra space""",
            "java": r"""// Two fixed loops + two pointers; 64-bit sums are mandatory
List<List<Integer>> fourSum(int[] a, long target) {
    Arrays.sort(a);
    int n = a.length;
    List<List<Integer>> out = new ArrayList<>();
    for (int i = 0; i + 3 < n; i++) {
        if (i > 0 && a[i] == a[i - 1]) continue;
        for (int j = i + 1; j + 2 < n; j++) {
            if (j > i + 1 && a[j] == a[j - 1]) continue;
            int l = j + 1, r = n - 1;
            while (l < r) {
                long s = (long) a[i] + a[j] + a[l] + a[r];
                if (s < target) l++;
                else if (s > target) r--;
                else {
                    out.add(Arrays.asList(a[i], a[j], a[l], a[r]));
                    while (l < r && a[l] == a[l + 1]) l++;
                    while (l < r && a[r] == a[r - 1]) r--;
                    l++; r--;
                }
            }
        }
    }
    return out;
}   // O(n^3) time · O(1) extra space""",
            "python": r"""def four_sum(a, target):
    a.sort()
    n = len(a)
    out = []
    for i in range(n - 3):
        if i > 0 and a[i] == a[i - 1]:
            continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and a[j] == a[j - 1]:
                continue
            l, r = j + 1, n - 1
            while l < r:
                s = a[i] + a[j] + a[l] + a[r]
                if s < target:
                    l += 1
                elif s > target:
                    r -= 1
                else:
                    out.append([a[i], a[j], a[l], a[r]])
                    while l < r and a[l] == a[l + 1]: l += 1
                    while l < r and a[r] == a[r - 1]: r -= 1
                    l += 1; r -= 1
    return out
# O(n^3) time · O(1) extra space (Python ints never overflow)""",
        },
    },
    {
        "slug": "character-replacement",
        "title": "Longest Repeating Character Replacement",
        "difficulty": "Medium",
        "pattern": "window + max-frequency bookkeeping",
        "statement": "You may change at most k characters of a string to any uppercase letter. Return the length of the "
                     "longest substring that can be made of a single repeated letter.",
        "examples": [("s = \"ABAB\", k = 2", "4"),
                     ("s = \"AABABBA\", k = 1", "4")],
        "constraints": ["1 <= length <= 10^5", "s consists of uppercase English letters", "0 <= k <= length"],
        "approach": "A window is feasible when `window length − count of its most frequent character ≤ k`, because only the "
                    "non-majority characters need replacing. Track the maximum frequency seen so far and never let the "
                    "window shrink — the answer only grows, so the left pointer advances at most once per step, keeping "
                    "the pass linear and the code branch-free.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Feasible when  length - maxFrequency  <= k
int characterReplacement(const string& s, int k) {
    int cnt[26] = {0};
    int left = 0, maxFreq = 0, best = 0;
    for (int right = 0; right < (int)s.size(); right++) {
        maxFreq = max(maxFreq, ++cnt[s[right] - 'A']);
        if (right - left + 1 - maxFreq > k) cnt[s[left++] - 'A']--;   // window can never shrink below best
        best = max(best, right - left + 1);
    }
    return best;
}   // O(n) time · O(1) space""",
            "java": r"""// Feasible when  length - maxFrequency  <= k
int characterReplacement(String s, int k) {
    int[] cnt = new int[26];
    int left = 0, maxFreq = 0, best = 0;
    for (int right = 0; right < s.length(); right++) {
        maxFreq = Math.max(maxFreq, ++cnt[s.charAt(right) - 'A']);
        if (right - left + 1 - maxFreq > k) cnt[s.charAt(left++) - 'A']--;   // never shrink below best
        best = Math.max(best, right - left + 1);
    }
    return best;
}   // O(n) time · O(1) space""",
            "python": r"""def character_replacement(s, k):
    cnt = [0] * 26
    left = max_freq = best = 0
    for right, ch in enumerate(s):
        idx = ord(ch) - ord('A')
        cnt[idx] += 1
        max_freq = max(max_freq, cnt[idx])
        if right - left + 1 - max_freq > k:     # infeasible: slide the whole window
            cnt[ord(s[left]) - ord('A')] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "permutation-in-string",
        "title": "Does s2 Contain a Permutation of s1?",
        "difficulty": "Medium",
        "pattern": "fixed window + letter counts",
        "statement": "Return true if some contiguous substring of `s2` is a permutation of `s1` — that is, contains "
                     "exactly the same multiset of characters.",
        "examples": [("s1 = \"ab\", s2 = \"eidbaooo\"", "true   (\"ba\")"),
                     ("s1 = \"ab\", s2 = \"eidboaoo\"", "false")],
        "constraints": ["1 <= |s1|, |s2| <= 10^4", "both strings contain lowercase English letters"],
        "approach": "Slide a window of length |s1| over `s2` and compare character counts. Comparing 26 buckets per step "
                    "is O(26n) — fine — or count how many buckets match and keep that number updated as characters enter "
                    "and leave the window, which makes each step O(1).",
        "complexity": ("O(|s1| + |s2|)", "O(1)"),
        "code": {
            "cpp": r"""// Fixed window the size of s1; track how many buckets agree
bool checkInclusion(const string& s1, const string& s2) {
    int n1 = s1.size(), n2 = s2.size();
    if (n1 > n2) return false;
    vector<int> need(26, 0), win(26, 0);
    for (char c : s1) need[c - 'a']++;
    for (int i = 0; i < n1; i++) win[s2[i] - 'a']++;
    int matches = 0;
    for (int c = 0; c < 26; c++) if (need[c] == win[c]) matches++;
    for (int i = 0; ; i++) {
        if (matches == 26) return true;
        if (i + n1 >= n2) break;
        int in = s2[i + n1] - 'a', out = s2[i] - 'a';      // slide one step
        if (++win[in] == need[in]) matches++;
        else if (win[in] == need[in] + 1) matches--;
        if (--win[out] == need[out]) matches++;
        else if (win[out] == need[out] - 1) matches--;
    }
    return false;
}   // O(|s2|) time · O(1) space""",
            "java": r"""// Fixed window the size of s1; track how many buckets agree
boolean checkInclusion(String s1, String s2) {
    int n1 = s1.length(), n2 = s2.length();
    if (n1 > n2) return false;
    int[] need = new int[26], win = new int[26];
    for (char c : s1.toCharArray()) need[c - 'a']++;
    for (int i = 0; i < n1; i++) win[s2.charAt(i) - 'a']++;
    int matches = 0;
    for (int c = 0; c < 26; c++) if (need[c] == win[c]) matches++;
    for (int i = 0; ; i++) {
        if (matches == 26) return true;
        if (i + n1 >= n2) break;
        int in = s2.charAt(i + n1) - 'a', out = s2.charAt(i) - 'a';   // slide one step
        if (++win[in] == need[in]) matches++;
        else if (win[in] == need[in] + 1) matches--;
        if (--win[out] == need[out]) matches++;
        else if (win[out] == need[out] - 1) matches--;
    }
    return false;
}   // O(|s2|) time · O(1) space""",
            "python": r"""from collections import Counter

def check_inclusion(s1, s2):
    n1, n2 = len(s1), len(s2)
    if n1 > n2:
        return False
    need = Counter(s1)
    win = Counter(s2[:n1])
    if win == need:
        return True
    for i in range(n1, n2):                 # slide the window
        win[s2[i]] += 1
        out = s2[i - n1]
        win[out] -= 1
        if win[out] == 0:
            del win[out]                    # keep counts comparable to `need`
        if win == need:
            return True
    return False
# O(|s2|) time · O(1) space""",
        },
    },
    {
        "slug": "find-all-anagrams",
        "title": "Find All Anagram Start Indices",
        "difficulty": "Medium",
        "pattern": "fixed window + count comparison, collecting all matches",
        "statement": "Return a list of all start indices in `s` where a substring is an anagram of `p`.",
        "examples": [("s = \"cbaebabacd\", p = \"abc\"", "[0,6]"),
                     ("s = \"abab\", p = \"ab\"", "[0,1,2]")],
        "constraints": ["1 <= |s|, |p| <= 3 * 10^4", "both strings contain lowercase English letters"],
        "approach": "Identical to the permutation check, except you must not stop at the first match — collect every "
                    "valid window position. A single differing count is enough to invalidate a window, so the standard "
                    "trick is to track a `diff` counter that reaches zero only for true anagrams.",
        "complexity": ("O(|s|)", "O(1)"),
        "code": {
            "cpp": r"""// Sliding counts; `diff` counts buckets that still disagree
vector<int> findAnagrams(const string& s, const string& p) {
    vector<int> out;
    int n = s.size(), m = p.size();
    if (m > n) return out;
    vector<int> cnt(26, 0);
    for (char c : p) cnt[c - 'a']++;
    int diff = 0;
    for (int c = 0; c < 26; c++) if (cnt[c] != 0) diff++;      // buckets that need fixing
    for (int i = 0; i < n; i++) {
        int in = s[i] - 'a';
        if (cnt[in] == 0) diff++;                              // this bucket becomes wrong
        cnt[in]--;
        if (cnt[in] == 0) diff--;                              // ... and this one becomes right
        if (i >= m) {
            int out = s[i - m] - 'a';
            if (cnt[out] == 0) diff++;
            cnt[out]++;
            if (cnt[out] == 0) diff--;
        }
        if (diff == 0) out.push_back(i - m + 1);
    }
    return out;
}   // O(n) time · O(1) space""",
            "java": r"""// Sliding counts; `diff` counts buckets that still disagree
List<Integer> findAnagrams(String s, String p) {
    List<Integer> out = new ArrayList<>();
    int n = s.length(), m = p.length();
    if (m > n) return out;
    int[] cnt = new int[26];
    for (char c : p.toCharArray()) cnt[c - 'a']++;
    int diff = 0;
    for (int c = 0; c < 26; c++) if (cnt[c] != 0) diff++;      // buckets that need fixing
    for (int i = 0; i < n; i++) {
        int in = s.charAt(i) - 'a';
        if (cnt[in] == 0) diff++;
        cnt[in]--;
        if (cnt[in] == 0) diff--;
        if (i >= m) {
            int outCh = s.charAt(i - m) - 'a';
            if (cnt[outCh] == 0) diff++;
            cnt[outCh]++;
            if (cnt[outCh] == 0) diff--;
        }
        if (diff == 0) out.add(i - m + 1);
    }
    return out;
}   // O(n) time · O(1) space""",
            "python": r"""from collections import Counter

def find_anagrams(s, p):
    m = len(p)
    if m > len(s):
        return []
    need = Counter(p)
    win = Counter(s[:m])
    out = []
    if win == need:
        out.append(0)
    for i in range(m, len(s)):
        win[s[i]] += 1
        left = s[i - m]
        win[left] -= 1
        if win[left] == 0:
            del win[left]
        if win == need:
            out.append(i - m + 1)
    return out
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "subarray-product-less-than-k",
        "title": "Count Subarrays With Product Less Than k",
        "difficulty": "Medium",
        "pattern": "variable window over a product (all values positive)",
        "statement": "Count the contiguous subarrays of a positive-integer array whose product is strictly less than k.",
        "examples": [("[10,5,2,6], k = 100", "8   (the whole array, plus [5,2], [2,6], [5,2,6] excluded variants)"),
                     ("[1,2,3], k = 0", "0")],
        "constraints": ["1 <= n <= 3 * 10^4", "1 <= a[i] <= 1000", "0 <= k <= 10^6"],
        "approach": "Slide a window whose product stays below k. Every time the window is valid, **all subarrays ending at "
                    "`right` and starting anywhere from `left` to `right`** are valid, so add `right - left + 1` in one go "
                    "— counting them one by one would be quadratic. Guard k ≤ 1 up front, since a product of positive "
                    "integers is at least 1.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Every valid window contributes (right - left + 1) subarrays
long long numSubarrayProductLessThanK(const vector<int>& a, int k) {
    if (k <= 1) return 0;
    long long prod = 1, count = 0;
    int left = 0;
    for (int right = 0; right < (int)a.size(); right++) {
        prod *= a[right];
        while (prod >= k) prod /= a[left++];      // shrink until valid
        count += right - left + 1;                // all subarrays ending at `right`
    }
    return count;
}   // O(n) time · O(1) space""",
            "java": r"""// Every valid window contributes (right - left + 1) subarrays
long numSubarrayProductLessThanK(int[] a, int k) {
    if (k <= 1) return 0;
    long prod = 1, count = 0;
    int left = 0;
    for (int right = 0; right < a.length; right++) {
        prod *= a[right];
        while (prod >= k && left <= right) prod /= a[left++];   // shrink until valid
        count += right - left + 1;                              // all subarrays ending at `right`
    }
    return count;
}   // O(n) time · O(1) space""",
            "python": r"""def num_subarray_product_less_than_k(a, k):
    if k <= 1:
        return 0                      # a product of positive ints is at least 1
    prod = 1
    left = count = 0
    for right, v in enumerate(a):
        prod *= v
        while prod >= k:              # shrink until valid
            prod //= a[left]
            left += 1
        count += right - left + 1     # every subarray ending here
    return count
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "boats-to-save-people",
        "title": "Boats to Save People (Greedy Two Pointers)",
        "difficulty": "Medium",
        "pattern": "sort + opposite-end greedy pairing",
        "statement": "Each boat carries at most two people and has a weight limit. Return the minimum number of boats "
                     "needed to carry everyone.",
        "examples": [("people = [1,2], limit = 3", "1"),
                     ("people = [3,2,2,1], limit = 3", "3"),
                     ("people = [3,5,3,4], limit = 5", "4")],
        "constraints": ["1 <= n <= 5 * 10^4", "1 <= people[i] <= limit <= 3 * 10^4"],
        "approach": "Sort, then pair the heaviest remaining person with the lightest if they fit. If they do not fit, the "
                    "heaviest must travel alone — no lighter partner could help. Every step either places two people or "
                    "guarantees one boat, so the greedy is optimal and the loop is linear after sorting.",
        "complexity": ("O(n log n)", "O(1) besides the sort"),
        "code": {
            "cpp": r"""// Greedy: pair the heaviest with the lightest when they fit
int numRescueBoats(vector<int> people, int limit) {
    sort(people.begin(), people.end());
    int i = 0, j = people.size() - 1, boats = 0;
    while (i <= j) {
        if (people[i] + people[j] <= limit) i++;   // they ride together
        j--;                                       // the heaviest always leaves
        boats++;
    }
    return boats;
}   // O(n log n) time · O(1) extra space""",
            "java": r"""// Greedy: pair the heaviest with the lightest when they fit
int numRescueBoats(int[] people, int limit) {
    Arrays.sort(people);
    int i = 0, j = people.length - 1, boats = 0;
    while (i <= j) {
        if (people[i] + people[j] <= limit) i++;   // they ride together
        j--;                                       // the heaviest always leaves
        boats++;
    }
    return boats;
}   // O(n log n) time · O(1) extra space""",
            "python": r"""def num_rescue_boats(people, limit):
    people.sort()
    i, j = 0, len(people) - 1
    boats = 0
    while i <= j:
        if people[i] + people[j] <= limit:
            i += 1                  # the lightest joins the heaviest
        j -= 1                      # the heaviest always leaves
        boats += 1
    return boats
# O(n log n) time · O(1) extra space""",
        },
    },
    {
        "slug": "sorted-array-intersection-two",
        "title": "Intersection of Two Sorted Arrays",
        "difficulty": "Medium",
        "pattern": "two forward pointers with equal-advance on match",
        "statement": "Given two arrays sorted in non-decreasing order, return their intersection (each value once, sorted "
                     "ascending).",
        "examples": [("[1,2,2,1] sorted, [2,2]", "[2]"),
                     ("[4,9,5] sorted, [9,4,9,8,4]", "[4,9]")],
        "constraints": ["1 <= m, n <= 1000", "0 <= a[i], b[i] <= 1000"],
        "approach": "Advance the pointer of the smaller value; on equality emit the value (once, skipping repeats) and "
                    "advance both. This is O(m + n) with no extra memory beyond the output — the set-based solution is "
                    "O(m + n) too but allocates two hash tables, which matters for large inputs.",
        "complexity": ("O(m + n)", "O(1) besides the output"),
        "code": {
            "cpp": r"""// Advance the smaller value; equal values are emitted once
vector<int> intersection(vector<int> a, vector<int> b) {
    sort(a.begin(), a.end());
    sort(b.begin(), b.end());
    vector<int> out;
    int i = 0, j = 0;
    while (i < (int)a.size() && j < (int)b.size()) {
        if (a[i] < b[j]) i++;
        else if (a[i] > b[j]) j++;
        else {
            out.push_back(a[i]);
            while (i < (int)a.size() && a[i] == out.back()) i++;   // skip repeats in a
            while (j < (int)b.size() && b[j] == out.back()) j++;   // and in b
        }
    }
    return out;
}   // O(m + n) after sorting · O(1) extra space""",
            "java": r"""// Advance the smaller value; equal values are emitted once
int[] intersection(int[] a, int[] b) {
    Arrays.sort(a); Arrays.sort(b);
    List<Integer> out = new ArrayList<>();
    int i = 0, j = 0;
    while (i < a.length && j < b.length) {
        if (a[i] < b[j]) i++;
        else if (a[i] > b[j]) j++;
        else {
            int v = a[i];
            out.add(v);
            while (i < a.length && a[i] == v) i++;     // skip repeats in a
            while (j < b.length && b[j] == v) j++;     // and in b
        }
    }
    int[] res = new int[out.size()];
    for (int k = 0; k < res.length; k++) res[k] = out.get(k);
    return res;
}   // O(m + n) after sorting · O(1) extra space""",
            "python": r"""def intersection(a, b):
    a, b = sorted(a), sorted(b)
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            i += 1
        elif a[i] > b[j]:
            j += 1
        else:
            v = a[i]
            out.append(v)
            while i < len(a) and a[i] == v: i += 1   # skip repeats in a
            while j < len(b) and b[j] == v: j += 1   # and in b
    return out
# O(m + n) after sorting · O(1) extra space""",
        },
    },

    # ------------------------------------------------------------------ HARD
    {
        "slug": "minimum-window-substring",
        "title": "Minimum Window Substring",
        "difficulty": "Hard",
        "pattern": "variable window + shortage counter",
        "statement": "Return the shortest substring of `s` that contains every character of `t` including multiplicities, "
                     "or an empty string if no such window exists.",
        "examples": [("s = \"ADOBECODEBANC\", t = \"ABC\"", "\"BANC\""),
                     ("s = \"a\", t = \"a\"", "\"a\""),
                     ("s = \"a\", t = \"aa\"", "\"\"")],
        "constraints": ["1 <= |s|, |t| <= 10^5", "both strings contain upper and lower case letters"],
        "approach": "Keep a `need` array and a `missing` counter of characters still required. The window becomes valid "
                    "when `missing` hits zero; then shrink from the left while recording the best length, restoring the "
                    "counter as characters leave. Decrementing `need` below zero marks a surplus, which is exactly what "
                    "lets the window shrink without losing validity.",
        "complexity": ("O(|s| + |t|)", "O(alphabet)"),
        "code": {
            "cpp": r"""// Expand until valid, then shrink while still valid
string minWindow(const string& s, const string& t) {
    if (t.size() > s.size()) return "";
    int need[128] = {0};
    for (char c : t) need[(unsigned char)c]++;
    int missing = t.size(), left = 0, bestL = 0, bestLen = INT_MAX;
    for (int right = 0; right < (int)s.size(); right++) {
        if (need[(unsigned char)s[right]]-- > 0) missing--;   // consumed a required character
        while (missing == 0) {                                // valid: try to shrink
            if (right - left + 1 < bestLen) { bestLen = right - left + 1; bestL = left; }
            if (need[(unsigned char)s[left++]]++ == 0) missing++;   // giving back a required character
        }
    }
    return bestLen == INT_MAX ? "" : s.substr(bestL, bestLen);
}   // O(|s| + |t|) time · O(1) space""",
            "java": r"""// Expand until valid, then shrink while still valid
String minWindow(String s, String t) {
    if (t.length() > s.length()) return "";
    int[] need = new int[128];
    for (char c : t.toCharArray()) need[c]++;
    int missing = t.length(), left = 0, bestL = 0, bestLen = Integer.MAX_VALUE;
    for (int right = 0; right < s.length(); right++) {
        if (need[s.charAt(right)]-- > 0) missing--;       // consumed a required character
        while (missing == 0) {                            // valid: try to shrink
            if (right - left + 1 < bestLen) { bestLen = right - left + 1; bestL = left; }
            if (need[s.charAt(left++)]++ == 0) missing++; // giving back a required character
        }
    }
    return bestLen == Integer.MAX_VALUE ? "" : s.substring(bestL, bestL + bestLen);
}   // O(|s| + |t|) time · O(1) space""",
            "python": r"""def min_window(s, t):
    if len(t) > len(s):
        return ""
    need = [0] * 128
    for ch in t:
        need[ord(ch)] += 1
    missing = len(t)
    left = best_l = 0
    best_len = float("inf")
    for right, ch in enumerate(s):
        code = ord(ch)
        if need[code] > 0:
            missing -= 1                     # consumed a required character
        need[code] -= 1
        while missing == 0:                  # valid window: shrink
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_l = left
            out = ord(s[left])
            left += 1
            need[out] += 1
            if need[out] > 0:
                missing += 1                 # a required character left the window
    return "" if best_len == float("inf") else s[best_l:best_l + best_len]
# O(|s| + |t|) time · O(1) space""",
        },
    },
    {
        "slug": "substring-concatenation-all-words",
        "title": "Substring With Concatenation of All Words",
        "difficulty": "Hard",
        "pattern": "block-aligned sliding window over word-sized chunks",
        "statement": "Given a string `s` and a list of equal-length words, return every start index of a substring of `s` "
                     "that is exactly a concatenation of all the words, each used once, in any order.",
        "examples": [("s = \"barfoothefoobarman\", words = [\"foo\",\"bar\"]", "[0,9]"),
                     ("s = \"wordgoodgoodgoodbestword\", words = [\"word\",\"good\",\"best\",\"word\"]", "[]")],
        "constraints": ["1 <= |s| <= 10^4", "1 <= number of words <= 5000", "all words have equal length"],
        "approach": "Step through the string in chunks of one word length, but try every offset in `[0, wordLen)` so no "
                    "alignment is missed. Maintain counts of the words inside the current block window; when a word "
                    "exceeds its quota, advance the left end chunk by chunk, and when the window holds exactly all words, "
                    "record the start. Each chunk enters and leaves once per offset, so the total work is linear.",
        "complexity": ("O(|s| · wordLength)", "O(number of distinct words)"),
        "code": {
            "cpp": r"""// Try every alignment; slide in word-sized blocks
vector<int> findSubstring(const string& s, vector<string>& words) {
    vector<int> out;
    if (words.empty()) return out;
    int w = words[0].size(), n = words.size();
    if ((int)s.size() < w * n) return out;
    unordered_map<string,int> need;
    for (const string& x : words) need[x]++;
    for (int start = 0; start < w; start++) {
        unordered_map<string,int> seen;
        int count = 0, left = start;
        for (int i = start; i + w <= (int)s.size(); i += w) {
            string piece = s.substr(i, w);
            if (need.count(piece)) {
                seen[piece]++;
                if (seen[piece] <= need[piece]) count++;
                while (seen[piece] > need[piece]) {          // too many copies: move the left end
                    string old = s.substr(left, w);
                    if (--seen[old] < need[old]) count--;
                    left += w;
                }
                if (count == n) out.push_back(left);
            } else {
                seen.clear(); count = 0; left = i + w;       // unknown word breaks the window
            }
        }
    }
    return out;
}   // O(|s| * wordLen) time · O(distinct words) space""",
            "java": r"""// Try every alignment; slide in word-sized blocks
List<Integer> findSubstring(String s, String[] words) {
    List<Integer> out = new ArrayList<>();
    if (words.length == 0) return out;
    int w = words[0].length(), n = words.length;
    if (s.length() < w * n) return out;
    Map<String,Integer> need = new HashMap<>();
    for (String x : words) need.merge(x, 1, Integer::sum);
    for (int start = 0; start < w; start++) {
        Map<String,Integer> seen = new HashMap<>();
        int count = 0, left = start;
        for (int i = start; i + w <= s.length(); i += w) {
            String piece = s.substring(i, i + w);
            if (need.containsKey(piece)) {
                seen.merge(piece, 1, Integer::sum);
                if (seen.get(piece) <= need.get(piece)) count++;
                while (seen.get(piece) > need.get(piece)) {  // too many copies: move the left end
                    String old = s.substring(left, left + w);
                    if (seen.merge(old, -1, Integer::sum) < need.get(old)) count--;
                    left += w;
                }
                if (count == n) out.add(left);
            } else {
                seen.clear(); count = 0; left = i + w;       // unknown word breaks the window
            }
        }
    }
    return out;
}   // O(|s| * wordLen) time · O(distinct words) space""",
            "python": r"""from collections import Counter, defaultdict

def find_substring(s, words):
    if not words:
        return []
    w = len(words[0])
    n = len(words)
    if len(s) < w * n:
        return []
    need = Counter(words)
    out = []
    for start in range(w):                    # every alignment
        seen = defaultdict(int)
        count = 0
        left = start
        for i in range(start, len(s) - w + 1, w):
            piece = s[i:i + w]
            if piece in need:
                seen[piece] += 1
                if seen[piece] <= need[piece]:
                    count += 1
                while seen[piece] > need[piece]:        # too many copies
                    old = s[left:left + w]
                    seen[old] -= 1
                    if seen[old] < need[old]:
                        count -= 1
                    left += w
                if count == n:
                    out.append(left)
            else:
                seen.clear(); count = 0; left = i + w   # unknown word breaks the window
    return out
# O(|s| * wordLen) time · O(distinct words) space""",
        },
    },
    {
        "slug": "sliding-window-maximum",
        "title": "Sliding Window Maximum",
        "difficulty": "Hard",
        "pattern": "monotonic deque",
        "statement": "Return the maximum of every contiguous window of size k as the window slides from left to right, in "
                     "O(n) total time.",
        "examples": [("[1,3,-1,-3,5,3,6,7], k = 3", "[3,3,5,5,6,7]"),
                     ("[1], k = 1", "[1]")],
        "constraints": ["1 <= n <= 10^5", "1 <= k <= n", "-10^4 <= a[i] <= 10^4"],
        "approach": "Keep a deque of indices whose values decrease from front to back. Before pushing a new index, pop "
                    "from the back every index whose value is not larger — they can never be the maximum again. Drop the "
                    "front index once it leaves the window; the front is then the window maximum. Each index is pushed "
                    "and popped at most once, giving O(n).",
        "complexity": ("O(n)", "O(k)"),
        "code": {
            "cpp": r"""// Deque of indices, values decreasing front -> back
vector<int> maxSlidingWindow(const vector<int>& a, int k) {
    deque<int> dq;
    vector<int> out;
    out.reserve(a.size() - k + 1);
    for (int i = 0; i < (int)a.size(); i++) {
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();   // dominated: never the max again
        dq.push_back(i);
        if (dq.front() <= i - k) dq.pop_front();                     // expired
        if (i >= k - 1) out.push_back(a[dq.front()]);
    }
    return out;
}   // O(n) time · O(k) space""",
            "java": r"""// Deque of indices, values decreasing front -> back
int[] maxSlidingWindow(int[] a, int k) {
    Deque<Integer> dq = new ArrayDeque<>();
    int[] out = new int[a.length - k + 1];
    for (int i = 0; i < a.length; i++) {
        while (!dq.isEmpty() && a[dq.peekLast()] <= a[i]) dq.pollLast();   // dominated
        dq.offerLast(i);
        if (dq.peekFirst() <= i - k) dq.pollFirst();                       // expired
        if (i >= k - 1) out[i - k + 1] = a[dq.peekFirst()];
    }
    return out;
}   // O(n) time · O(k) space""",
            "python": r"""from collections import deque

def max_sliding_window(a, k):
    dq = deque()          # indices, values decreasing from the left
    out = []
    for i, v in enumerate(a):
        while dq and a[dq[-1]] <= v:
            dq.pop()                       # dominated: never the maximum again
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()                   # expired
        if i >= k - 1:
            out.append(a[dq[0]])
    return out
# O(n) time · O(k) space""",
        },
    },
    {
        "slug": "smallest-range-k-lists",
        "title": "Smallest Range Covering Elements From k Lists",
        "difficulty": "Hard",
        "pattern": "k-way merge with a min-heap and a running maximum",
        "statement": "Given k sorted lists of integers, find the smallest range [a, b] that contains at least one number "
                     "from every list. If several are equally small, any of them is accepted.",
        "examples": [("[[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]", "[20,24]   (one value from each list)"),
                     ("[[1,2,3],[1,2,3],[1,2,3]]", "[1,1]")],
        "constraints": ["1 <= k <= 3500", "1 <= total elements <= 10^5", "each list is sorted ascending"],
        "approach": "Merge the lists lazily: keep one pointer per list in a min-heap, plus the maximum of the current "
                    "heads. The current heads span a candidate range. Then advance the list owning the smallest head — "
                    "that is the only move that can improve the range, since the smallest value is what the range must "
                    "cover on the left. Stop when one list is exhausted.",
        "complexity": ("O(N log k) with N the total number of elements", "O(k)"),
        "code": {
            "cpp": r"""// Merge k lists lazily: heap of heads + running maximum
vector<int> smallestRange(vector<vector<int>>& lists) {
    int k = lists.size();
    priority_queue<tuple<int,int,int>, vector<tuple<int,int,int>>, greater<>> pq;  // value, list, index
    int curMax = INT_MIN;
    for (int i = 0; i < k; i++) {
        pq.emplace(lists[i][0], i, 0);
        curMax = max(curMax, lists[i][0]);
    }
    int bestL = -100000, bestR = 100000;
    while ((int)pq.size() == k) {
        auto [v, li, idx] = pq.top(); pq.pop();
        if (curMax - v < bestR - bestL) { bestL = v; bestR = curMax; }   // a tighter span
        if (idx + 1 < (int)lists[li].size()) {
            int nv = lists[li][idx + 1];
            pq.emplace(nv, li, idx + 1);
            curMax = max(curMax, nv);
        }
    }
    return {bestL, bestR};
}   // O(N log k) time · O(k) space""",
            "java": r"""// Merge k lists lazily: heap of heads + running maximum
int[] smallestRange(List<List<Integer>> lists) {
    int k = lists.size();
    PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> Integer.compare(x[0], y[0]));  // {value, list, index}
    int curMax = Integer.MIN_VALUE;
    for (int i = 0; i < k; i++) {
        int v = lists.get(i).get(0);
        pq.offer(new int[]{v, i, 0});
        curMax = Math.max(curMax, v);
    }
    int bestL = -100000, bestR = 100000;
    while (pq.size() == k) {
        int[] cur = pq.poll();
        int v = cur[0], li = cur[1], idx = cur[2];
        if (curMax - v < bestR - bestL) { bestL = v; bestR = curMax; }   // a tighter span
        if (idx + 1 < lists.get(li).size()) {
            int nv = lists.get(li).get(idx + 1);
            pq.offer(new int[]{nv, li, idx + 1});
            curMax = Math.max(curMax, nv);
        }
    }
    return new int[]{bestL, bestR};
}   // O(N log k) time · O(k) space""",
            "python": r"""import heapq

def smallest_range(lists):
    heap = []                                     # (value, list index, position in list)
    cur_max = float("-inf")
    for i, lst in enumerate(lists):
        heap.append((lst[0], i, 0))
        cur_max = max(cur_max, lst[0])
    heapq.heapify(heap)
    best = [heap[0][0], cur_max]
    while True:
        v, li, idx = heapq.heappop(heap)
        if cur_max - v < best[1] - best[0]:        # a tighter span
            best = [v, cur_max]
        if idx + 1 == len(lists[li]):
            break                                  # this list is exhausted: no wider range can beat it
        nv = lists[li][idx + 1]
        heapq.heappush(heap, (nv, li, idx + 1))
        cur_max = max(cur_max, nv)
    return best
# O(N log k) time · O(k) space""",
        },
    },
    {
        "slug": "k-consecutive-bit-flips",
        "title": "Minimum Number of k Consecutive Bit Flips",
        "difficulty": "Hard",
        "pattern": "greedy left-to-right with a sliding flip counter",
        "statement": "In one operation you choose a window of exactly k consecutive bits and flip all of them. Return the "
                     "minimum number of operations to make the array all 1s, or -1 if it is impossible.",
        "examples": [("[0,1,0], k = 1", "2"),
                     ("[1,1,0], k = 2", "-1"),
                     ("[0,0,0,1,0,1,1,0], k = 3", "3")],
        "constraints": ["1 <= n <= 10^5", "1 <= k <= n", "a[i] is 0 or 1"],
        "approach": "Scan left to right: the leftmost bit can only be fixed by a flip starting exactly there. So whenever "
                    "the current bit is 0 after accounting for the flips still in effect, start a flip here, or return -1 "
                    "if the window would run past the end. A deque (or an array of flip-start marks) tracks how many "
                    "flips are still active, which is what makes each step O(1).",
        "complexity": ("O(n)", "O(k)"),
        "code": {
            "cpp": r"""// The leftmost 0 can only be fixed by a flip starting here
int minKBitFlips(vector<int>& a, int k) {
    int n = a.size(), active = 0, ans = 0;
    vector<int> started(n, 0);                       // flip starts a window here
    for (int i = 0; i < n; i++) {
        if (i >= k) active -= started[i - k];        // a flip ended
        if ((a[i] + active) % 2 == 0) {              // still 0: must flip now
            if (i + k > n) return -1;                // would run past the end
            started[i] = 1; active++; ans++;
        }
    }
    return ans;
}   // O(n) time · O(k) space

// O(1) space variant: mark a flip by adding 2 to a[i], then a[i] >= 2 means "flipped".""",
            "java": r"""// The leftmost 0 can only be fixed by a flip starting here
int minKBitFlips(int[] a, int k) {
    int n = a.length, active = 0, ans = 0;
    int[] started = new int[n];                      // flip starts a window here
    for (int i = 0; i < n; i++) {
        if (i >= k) active -= started[i - k];        // a flip ended
        if ((a[i] + active) % 2 == 0) {              // still 0: must flip now
            if (i + k > n) return -1;                // would run past the end
            started[i] = 1; active++; ans++;
        }
    }
    return ans;
}   // O(n) time · O(k) space""",
            "python": r"""from collections import deque

def min_k_bit_flips(a, k):
    a = a[:]                       # work on a copy
    n = len(a)
    flips = deque()                # indices where a flip started
    ans = 0
    for i in range(n):
        if flips and flips[0] <= i - k:
            flips.popleft()        # expired flip
        effective = a[i] ^ (len(flips) % 2)          # current value after active flips
        if effective == 0:
            if i + k > n:
                return -1          # cannot cover the last zero
            flips.append(i)
            ans += 1
    return ans
# O(n) time · O(k) space""",
        },
    },
    {
        "slug": "minimum-window-subsequence",
        "title": "Minimum Window Subsequence",
        "difficulty": "Hard",
        "pattern": "forward match then backward shrink, repeated",
        "statement": "Return the shortest substring of `s1` that contains `s2` as a subsequence. If several are equally "
                     "short, return the one that appears first. Return an empty string if no such window exists.",
        "examples": [("s1 = \"abcdebdde\", s2 = \"bde\"", "\"bcde\""),
                     ("s1 = \"jmeqksfrsdcmsiwvaovztaqenprpvnbstl\", s2 = \"u\"", "\"\"")],
        "constraints": ["1 <= |s1| <= 2 * 10^4", "1 <= |s2| <= 100", "both strings contain lowercase letters"],
        "approach": "Unlike plain substring windows, the window here must obey an order, so start a fresh forward scan "
                    "from the current position until all of `s2` is matched; then walk **backwards** from the last matched "
                    "character to find the tightest start. That start gives one candidate window, and the next search can "
                    "resume just after it, so the total work stays linear in the number of productive scans.",
        "complexity": ("O(|s1| · |s2|) worst case, effectively linear in practice", "O(1)"),
        "code": {
            "cpp": r"""// Forward to match s2, backward to tighten the start
string minWindowSubsequence(const string& s1, const string& s2) {
    int m = s1.size(), n = s2.size();
    int bestLen = INT_MAX, bestStart = -1;
    int i = 0;
    while (i < m) {
        int j = 0, k = i;
        while (k < m && j < n) { if (s1[k] == s2[j]) j++; k++; }   // forward: match s2 in order
        if (j < n) break;                                          // no full match from here on
        int end = k - 1, p = n - 1, q = end;
        while (p >= 0) { if (s1[q] == s2[p]) p--; q--; }            // backward: tighten the start
        int start = q + 1;
        if (end - start + 1 < bestLen) { bestLen = end - start + 1; bestStart = start; }
        i = start + 1;                                              // resume just after this window
    }
    return bestStart == -1 ? "" : s1.substr(bestStart, bestLen);
}   // O(|s1| * |s2|) worst case · O(1) space""",
            "java": r"""// Forward to match s2, backward to tighten the start
String minWindowSubsequence(String s1, String s2) {
    int m = s1.length(), n = s2.length();
    int bestLen = Integer.MAX_VALUE, bestStart = -1;
    int i = 0;
    while (i < m) {
        int j = 0, k = i;
        while (k < m && j < n) { if (s1.charAt(k) == s2.charAt(j)) j++; k++; }   // forward match
        if (j < n) break;                                                        // no match from here
        int end = k - 1, p = n - 1, q = end;
        while (p >= 0) { if (s1.charAt(q) == s2.charAt(p)) p--; q--; }           // backward tighten
        int start = q + 1;
        if (end - start + 1 < bestLen) { bestLen = end - start + 1; bestStart = start; }
        i = start + 1;                                                           // resume after the window
    }
    return bestStart == -1 ? "" : s1.substring(bestStart, bestStart + bestLen);
}   // O(|s1| * |s2|) worst case · O(1) space""",
            "python": r"""def min_window_subsequence(s1, s2):
    m, n = len(s1), len(s2)
    best_len = float("inf")
    best_start = -1
    i = 0
    while i < m:
        j, k = 0, i
        while k < m and j < n:            # forward: match s2 in order
            if s1[k] == s2[j]:
                j += 1
            k += 1
        if j < n:
            break                          # no full match can start from here
        end = k - 1
        p, q = n - 1, end
        while p >= 0:                      # backward: tighten the start
            if s1[q] == s2[p]:
                p -= 1
            q -= 1
        start = q + 1
        if end - start + 1 < best_len:
            best_len = end - start + 1
            best_start = start
        i = start + 1                       # resume just after this window
    return "" if best_start == -1 else s1[best_start:best_start + best_len]
# O(|s1| * |s2|) worst case · O(1) space""",
        },
    },
    {
        "slug": "substrings-containing-three-chars",
        "title": "Number of Substrings Containing All Three Characters",
        "difficulty": "Hard",
        "pattern": "count substrings by their tightest left end",
        "statement": "Given a string of only the characters a, b and c, count how many substrings contain at least one "
                     "of each.",
        "examples": [("\"abcabc\"", "10"),
                     ("\"aaacb\"", "3"),
                     ("\"abc\"", "1")],
        "constraints": ["1 <= length <= 5 * 10^4", "the string contains only a, b and c"],
        "approach": "Track the last position of each of the three characters. When all three have been seen, every "
                    "substring ending at the current index that starts at or before `min(last positions)` contains all "
                    "three; there are `min(last) + 1` such starts, since positions are 0-based. Summing that per index "
                    "gives every substring exactly once, in O(n) with no explicit window management.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// At each index, count starts that cover all three letters
long long numberOfSubstrings(const string& s) {
    long long last[3] = {-1, -1, -1}, count = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        last[s[i] - 'a'] = i;
        count += 1 + min({last[0], last[1], last[2]});   // starts 0..min(last) all work
    }
    return count;
}   // O(n) time · O(1) space""",
            "java": r"""// At each index, count starts that cover all three letters
long numberOfSubstrings(String s) {
    long[] last = {-1, -1, -1};
    long count = 0;
    for (int i = 0; i < s.length(); i++) {
        last[s.charAt(i) - 'a'] = i;
        count += 1 + Math.min(last[0], Math.min(last[1], last[2]));   // starts 0..min(last) all work
    }
    return count;
}   // O(n) time · O(1) space""",
            "python": r"""def number_of_substrings(s):
    last = [-1, -1, -1]
    count = 0
    for i, ch in enumerate(s):
        last[ord(ch) - ord('a')] = i
        count += 1 + min(last)     # this many starts cover all three letters
    return count
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "kth-smallest-prime-fraction",
        "title": "K-th Smallest Prime Fraction",
        "difficulty": "Hard",
        "pattern": "binary search on a value + two-pointer counting",
        "statement": "Given a sorted array of distinct primes, consider every fraction arr[i]/arr[j] with i < j. Return "
                     "the k-th smallest fraction as `[numerator, denominator]`.",
        "examples": [("[1,2,3,5], k = 3", "[2,5]   (the fractions are 1/5, 1/3, 2/5, 1/2, 3/5, 2/3)"),
                     ("[1,7], k = 1", "[1,7]")],
        "constraints": ["2 <= n <= 1000", "1 <= k <= n(n-1)/2", "arr is sorted and its elements are distinct"],
        "approach": "Binary search on the **value** of the answer. For a candidate value, count how many fractions are "
                    "at most it: for each denominator, a single moving pointer over numerators gives the count in O(n) "
                    "because the pointer only moves forward. While counting, also remember the largest fraction that "
                    "does not exceed the candidate — that is the exact answer once the count converges to k.",
        "complexity": ("O(n log(1/eps))", "O(1)"),
        "code": {
            "cpp": r"""// Binary search the value; count fractions <= mid in O(n)
vector<int> kthSmallestPrimeFraction(vector<int>& arr, int k) {
    int n = arr.size();
    double lo = 0.0, hi = 1.0;
    int bestP = 0, bestQ = 1;
    for (int iter = 0; iter < 60; iter++) {                 // 60 halvings is well past double precision
        double mid = (lo + hi) / 2;
        int count = 0, p = 0, q = 1, i = 0;                 // i = first numerator with arr[i]/arr[j] > mid
        for (int j = 1; j < n; j++) {
            while (i < j && (double)arr[i] / arr[j] <= mid) i++;
            count += i;                                     // numerators 0..i-1 qualify
            if (i > 0 && (long long)arr[i - 1] * q > (long long)p * arr[j]) { p = arr[i - 1]; q = arr[j]; }
        }
        if (count < k) lo = mid;                            // too few: the answer is larger
        else { hi = mid; bestP = p; bestQ = q; }            // mid is an upper bound: keep the best seen
    }
    return {bestP, bestQ};
}   // O(n log(1/eps)) time · O(1) space""",
            "java": r"""// Binary search the value; count fractions <= mid in O(n)
int[] kthSmallestPrimeFraction(int[] arr, int k) {
    int n = arr.length;
    double lo = 0.0, hi = 1.0;
    int bestP = 0, bestQ = 1;
    for (int iter = 0; iter < 60; iter++) {                 // 60 halvings is well past double precision
        double mid = (lo + hi) / 2;
        int count = 0, p = 0, q = 1, i = 0;                 // i = first numerator with arr[i]/arr[j] > mid
        for (int j = 1; j < n; j++) {
            while (i < j && (double) arr[i] / arr[j] <= mid) i++;
            count += i;                                     // numerators 0..i-1 qualify
            if (i > 0 && (long) arr[i - 1] * q > (long) p * arr[j]) { p = arr[i - 1]; q = arr[j]; }
        }
        if (count < k) lo = mid;                            // too few: the answer is larger
        else { hi = mid; bestP = p; bestQ = q; }            // keep the best bound seen
    }
    return new int[]{bestP, bestQ};
}   // O(n log(1/eps)) time · O(1) space""",
            "python": r"""def kth_smallest_prime_fraction(arr, k):
    n = len(arr)
    lo, hi = 0.0, 1.0
    best_p, best_q = 0, 1
    for _ in range(60):                 # value binary search
        mid = (lo + hi) / 2
        count = 0
        i = 0                           # first numerator with arr[i]/arr[j] > mid
        p, q = 0, 1
        for j in range(1, n):
            while i < j and arr[i] / arr[j] <= mid:
                i += 1
            count += i                  # numerators 0..i-1 qualify
            if i > 0 and arr[i - 1] * q > p * arr[j]:
                p, q = arr[i - 1], arr[j]
        if count < k:
            lo = mid                    # answer is larger
        else:
            hi = mid
            best_p, best_q = p, q       # keep the largest fraction <= mid
    return [best_p, best_q]
# O(n log(1/eps)) time · O(1) space""",
        },
    },
    {
        "slug": "min-operations-reduce-x",
        "title": "Minimum Operations to Reduce x to Zero",
        "difficulty": "Hard",
        "pattern": "complement of a sliding window",
        "statement": "From either end of the array you may remove one element per operation, subtracting it from a target "
                     "x. Return the minimum number of operations to make x exactly zero, or -1 if impossible.",
        "examples": [("[1,1,4,2,3], x = 5", "2   (remove 2 and 3 from the right)"),
                     ("[5,6,7,8,9], x = 4", "-1")],
        "constraints": ["1 <= n <= 10^5", "1 <= a[i] <= 10^4", "1 <= x <= 10^9"],
        "approach": "Removing prefix and suffix elements leaves a **contiguous middle subarray** untouched, so minimising "
                    "the removed count means maximising the length of the middle whose sum is `total - x`. That is a "
                    "classic positive-values sliding window: the answer is `n - longest such subarray`.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Maximise the untouched middle with sum = total - x
int minOperations(vector<int>& a, int x) {
    long long total = accumulate(a.begin(), a.end(), 0LL);
    long long need = total - x;
    if (need < 0) return -1;                       // must remove more than everything
    if (need == 0) return a.size();                // remove the whole array
    int n = a.size(), left = 0, best = -1;
    long long sum = 0;
    for (int right = 0; right < n; right++) {
        sum += a[right];
        while (sum > need) sum -= a[left++];       // shrink until the sum fits
        if (sum == need) best = max(best, right - left + 1);
    }
    return best == -1 ? -1 : n - best;             // the rest is removed from the ends
}   // O(n) time · O(1) space""",
            "java": r"""// Maximise the untouched middle with sum = total - x
int minOperations(int[] a, int x) {
    long total = 0;
    for (int v : a) total += v;
    long need = total - x;
    if (need < 0) return -1;                       // must remove more than everything
    if (need == 0) return a.length;                // remove the whole array
    int left = 0, best = -1;
    long sum = 0;
    for (int right = 0; right < a.length; right++) {
        sum += a[right];
        while (sum > need) sum -= a[left++];       // shrink until the sum fits
        if (sum == need) best = Math.max(best, right - left + 1);
    }
    return best == -1 ? -1 : a.length - best;      // the rest is removed from the ends
}   // O(n) time · O(1) space""",
            "python": r"""def min_operations(a, x):
    total = sum(a)
    need = total - x
    if need < 0:
        return -1                    # must remove more than everything
    if need == 0:
        return len(a)                # remove the whole array
    left = 0
    window = 0
    best = -1
    for right, v in enumerate(a):    # longest middle with sum == need
        window += v
        while window > need:
            window -= a[left]
            left += 1
        if window == need:
            best = max(best, right - left + 1)
    return -1 if best == -1 else len(a) - best
# O(n) time · O(1) space""",
        },
    },
    {
        "slug": "constrained-subsequence-sum",
        "title": "Constrained Subsequence Sum",
        "difficulty": "Hard",
        "pattern": "DP + monotonic deque",
        "statement": "Choose a subsequence (possibly empty) such that any two chosen indices differ by at most k in "
                     "position, and return the maximum possible sum. The empty subsequence sums to 0.",
        "examples": [("[10,2,-10,5,20], k = 2", "37   (10 + 2 + 5 + 20)"),
                     ("[-1,-2,-3], k = 1", "-1"),
                     ("[10,-2,-10,-5,20], k = 2", "23")],
        "constraints": ["1 <= n <= 10^5", "1 <= k <= n", "-10^4 <= a[i] <= 10^4"],
        "approach": "Let `dp[i]` be the best sum of a valid subsequence ending exactly at i. Then "
                    "`dp[i] = a[i] + max(0, max dp[j] for j in [i-k, i-1])`, and a monotonic deque over the last k dp "
                    "values answers that maximum in O(1) per step. The window of candidate predecessors moves with i, "
                    "which is exactly what a deque is for.",
        "complexity": ("O(n)", "O(k)"),
        "code": {
            "cpp": r"""// dp[i] = a[i] + max(0, best dp in the last k positions)
int constrainedSubsetSum(vector<int>& a, int k) {
    int n = a.size();
    vector<int> dp(n);
    deque<int> dq;                                  // indices with decreasing dp values
    int best = INT_MIN;
    for (int i = 0; i < n; i++) {
        if (!dq.empty() && dq.front() < i - k) dq.pop_front();          // out of range
        int prev = dq.empty() ? 0 : max(0, dp[dq.front()]);             // 0 = start fresh here
        dp[i] = a[i] + prev;
        while (!dq.empty() && dp[dq.back()] <= dp[i]) dq.pop_back();    // dominated
        dq.push_back(i);
        best = max(best, dp[i]);
    }
    return best;
}   // O(n) time · O(k) space""",
            "java": r"""// dp[i] = a[i] + max(0, best dp in the last k positions)
int constrainedSubsetSum(int[] a, int k) {
    int n = a.length;
    int[] dp = new int[n];
    Deque<Integer> dq = new ArrayDeque<>();          // indices with decreasing dp values
    int best = Integer.MIN_VALUE;
    for (int i = 0; i < n; i++) {
        if (!dq.isEmpty() && dq.peekFirst() < i - k) dq.pollFirst();     // out of range
        int prev = dq.isEmpty() ? 0 : Math.max(0, dp[dq.peekFirst()]);   // 0 = start fresh here
        dp[i] = a[i] + prev;
        while (!dq.isEmpty() && dp[dq.peekLast()] <= dp[i]) dq.pollLast();   // dominated
        dq.offerLast(i);
        best = Math.max(best, dp[i]);
    }
    return best;
}   // O(n) time · O(k) space""",
            "python": r"""from collections import deque

def constrained_subset_sum(a, k):
    n = len(a)
    dp = [0] * n
    dq = deque()                       # indices, dp values decreasing from the left
    best = float("-inf")
    for i in range(n):
        if dq and dq[0] < i - k:
            dq.popleft()               # predecessor out of range
        prev = max(0, dp[dq[0]]) if dq else 0    # 0 = start the subsequence here
        dp[i] = a[i] + prev
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()                   # dominated
        dq.append(i)
        best = max(best, dp[i])
    return best
# O(n) time · O(k) space""",
        },
    },
    {
        "slug": "maximum-score-two-arrays",
        "title": "Get the Maximum Score From Two Sorted Arrays",
        "difficulty": "Hard",
        "pattern": "two pointers with segment sums and greedy jumps",
        "statement": "Starting from either array's beginning, walk right through one array or switch arrays only on "
                     "positions holding the same value in both. Return the maximum sum reachable, modulo 10^9 + 7.",
        "examples": [("[2,4,5,8,10], [4,6,8,9]", "30   (2+4+6+8+10)"),
                     ("[1,3,5,7], [2,4,6,8]", "16   (pick the better single array)")],
        "constraints": ["1 <= m, n <= 10^5", "arrays are sorted strictly ascending", "values may be large"],
        "approach": "Walk both arrays with two pointers, accumulating the running sum of the current segment in each. On "
                    "a shared value, the sums so far are two alternative paths to the same junction: keep the larger and "
                    "restart both accumulators. At the end, add the larger of the two remaining tails — a greedy that is "
                    "optimal because each segment between junctions must be taken whole.",
        "complexity": ("O(m + n)", "O(1)"),
        "code": {
            "cpp": r"""// Keep the better path at every shared value
int maxSum(vector<int>& a, vector<int>& b) {
    const long long MOD = 1000000007LL;
    int i = 0, j = 0;
    long long sumA = 0, sumB = 0, total = 0;
    while (i < (int)a.size() && j < (int)b.size()) {
        if (a[i] < b[j]) sumA += a[i++];
        else if (a[i] > b[j]) sumB += b[j++];
        else {                                    // a shared junction: take the better path so far
            total += max(sumA, sumB) + a[i];
            sumA = sumB = 0;
            i++; j++;
        }
    }
    while (i < (int)a.size()) sumA += a[i++];      // remaining tails
    while (j < (int)b.size()) sumB += b[j++];
    total += max(sumA, sumB);
    return (int)(total % MOD);
}   // O(m + n) time · O(1) space""",
            "java": r"""// Keep the better path at every shared value
int maxSum(int[] a, int[] b) {
    final long MOD = 1_000_000_007L;
    int i = 0, j = 0;
    long sumA = 0, sumB = 0, total = 0;
    while (i < a.length && j < b.length) {
        if (a[i] < b[j]) sumA += a[i++];
        else if (a[i] > b[j]) sumB += b[j++];
        else {                                    // a shared junction: take the better path so far
            total += Math.max(sumA, sumB) + a[i];
            sumA = sumB = 0;
            i++; j++;
        }
    }
    while (i < a.length) sumA += a[i++];           // remaining tails
    while (j < b.length) sumB += b[j++];
    total += Math.max(sumA, sumB);
    return (int) (total % MOD);
}   // O(m + n) time · O(1) space""",
            "python": r"""def max_sum(a, b):
    MOD = 10 ** 9 + 7
    i = j = 0
    sum_a = sum_b = total = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            sum_a += a[i]; i += 1
        elif a[i] > b[j]:
            sum_b += b[j]; j += 1
        else:                                  # shared junction: keep the better path
            total += max(sum_a, sum_b) + a[i]
            sum_a = sum_b = 0
            i += 1; j += 1
    sum_a += sum(a[i:])                        # remaining tails
    sum_b += sum(b[j:])
    total += max(sum_a, sum_b)
    return total % MOD
# O(m + n) time · O(1) space""",
        },
    },
    {
        "slug": "count-subarrays-fixed-bounds",
        "title": "Count Subarrays With Fixed Minimum and Maximum",
        "difficulty": "Hard",
        "pattern": "last-position tracking window",
        "statement": "Count the subarrays whose minimum is exactly `minK` and whose maximum is exactly `maxK`.",
        "examples": [("[1,3,5,2,7,5], minK = 1, maxK = 5", "2   ([1,3,5] and [1,3,5,2])"),
                     ("[1,1,1,1], minK = 1, maxK = 1", "10   (every subarray)")],
        "constraints": ["1 <= n <= 10^5", "1 <= a[i], minK, maxK <= 10^9"],
        "approach": "Scan once, remembering the last position of a **bad** value (outside `[minK, maxK]`), the last "
                    "position equal to `minK` and the last equal to `maxK`. A subarray ending at i is valid precisely "
                    "when it starts after the last bad position and at or before the earlier of the two boundary "
                    "positions, giving `min(lastMin, lastMax) - lastBad` valid starts — clamped at zero before both "
                    "boundary values have appeared.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Count valid starts for each ending index
long long countSubarrays(vector<int>& a, int minK, int maxK) {
    long long ans = 0;
    int lastBad = -1, lastMin = -1, lastMax = -1;
    for (int i = 0; i < (int)a.size(); i++) {
        if (a[i] < minK || a[i] > maxK) lastBad = i;     // this value can never be inside a valid subarray
        if (a[i] == minK) lastMin = i;
        if (a[i] == maxK) lastMax = i;
        long long starts = (long long)min(lastMin, lastMax) - lastBad;   // negative before both appear
        if (starts > 0) ans += starts;
    }
    return ans;
}   // O(n) time · O(1) space""",
            "java": r"""// Count valid starts for each ending index
long countSubarrays(int[] a, int minK, int maxK) {
    long ans = 0;
    int lastBad = -1, lastMin = -1, lastMax = -1;
    for (int i = 0; i < a.length; i++) {
        if (a[i] < minK || a[i] > maxK) lastBad = i;     // this value can never be inside a valid subarray
        if (a[i] == minK) lastMin = i;
        if (a[i] == maxK) lastMax = i;
        long starts = (long) Math.min(lastMin, lastMax) - lastBad;   // negative before both appear
        if (starts > 0) ans += starts;
    }
    return ans;
}   // O(n) time · O(1) space""",
            "python": r"""def count_subarrays(a, min_k, max_k):
    ans = 0
    last_bad = last_min = last_max = -1
    for i, v in enumerate(a):
        if v < min_k or v > max_k:
            last_bad = i              # can never be part of a valid subarray
        if v == min_k:
            last_min = i
        if v == max_k:
            last_max = i
        starts = min(last_min, last_max) - last_bad
        if starts > 0:                # both boundaries have appeared after the last bad value
            ans += starts
    return ans
# O(n) time · O(1) space""",
        },
    },
]

