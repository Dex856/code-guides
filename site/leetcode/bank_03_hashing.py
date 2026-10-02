# Topic 3 · Hashing & Frequency Maps
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.

TOPIC = {
    "name": "Hashing & Frequency Maps",
    "tagline": "Trade memory for time: one pass, one dictionary, O(1) lookups — the pattern behind a third of all interview questions.",
    "focus": "Choosing the right key (value, value-minus-index, prefix-sum-mod, slope, encoded state), counting with maps instead of "
             "sorting, hashing composite keys, and knowing exactly when a hash map is not allowed (when you need order) or not needed "
             "(when the index itself can store the information).",
    "ordering": "easy 1–6 are single-pass lookups and frequency counts; medium 1–5 are counting maps with a twist (prefix sums, "
                "normalised keys, pair counting), 6–9 are design/encoding problems, 10–12 combine a map with another idea; "
                "hard 1–4 are the classic hard hash problems, 5–8 need a normalised key or an exact-count argument, "
                "9–12 are competition-level variants.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "two-sum-hash",
        "title": "Two Sum (Unsorted)",
        "difficulty": "Easy",
        "pattern": "seen-map of complements",
        "statement": "Given an unsorted array and a target, return the indices of the two numbers that add up to the target. "
                     "Exactly one solution exists and you may not use the same element twice.",
        "examples": [("[2,7,11,15], target = 9", "[0,1]"),
                     ("[3,2,4], target = 6", "[1,2]")],
        "constraints": ["2 <= n <= 10^4", "exactly one valid pair exists", "answers may be returned in any order"],
        "approach": "Walk the array once and remember every value you have already seen together with its index. For the current "
                    "value v you need target - v, so the complement lookup happens *before* storing v — that ordering alone stops "
                    "you from pairing an element with itself.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// One pass, complements in a hash map
vector<int> twoSum(vector<int>& a, int target) {
    unordered_map<int, int> seen;              // value -> index
    for (int i = 0; i < (int)a.size(); i++) {
        auto it = seen.find(target - a[i]);    // look FIRST
        if (it != seen.end()) return {it->second, i};
        seen[a[i]] = i;
    }
    return {};                                 // unreachable for valid input
}   // O(n) time · O(n) space""",
            "java": r"""// One pass, complements in a hash map
int[] twoSum(int[] a, int target) {
    Map<Integer, Integer> seen = new HashMap<>();   // value -> index
    for (int i = 0; i < a.length; i++) {
        Integer j = seen.get(target - a[i]);       // look FIRST
        if (j != null) return new int[]{j, i};
        seen.put(a[i], i);
    }
    return new int[0];                              // unreachable for valid input
}   // O(n) time · O(n) space""",
            "python": r"""def two_sum(a, target):
    seen = {}                       # value -> index
    for i, v in enumerate(a):
        if target - v in seen:      # look FIRST
            return [seen[target - v], i]
        seen[v] = i
    return []                       # unreachable for valid input""",
        },
    },
    {
        "slug": "contains-duplicate",
        "title": "Contains Duplicate",
        "difficulty": "Easy",
        "pattern": "set membership",
        "statement": "Return true if any value appears at least twice in the array, false if every element is distinct.",
        "examples": [("[1,2,3,1]", "true"), ("[1,2,3,4]", "false")],
        "constraints": ["1 <= n <= 10^5", "values fit in a 32-bit integer"],
        "approach": "A set is the minimal structure that answers \"have I seen this?\". Walk once and test membership before "
                    "inserting; the moment the test succeeds you can return true without scanning the rest.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Set membership answers "seen before?" in O(1)
bool containsDuplicate(vector<int>& a) {
    unordered_set<int> seen;
    for (int v : a) {
        if (!seen.insert(v).second) return true;   // insert returns {it, inserted}
    }
    return false;
}   // O(n) time · O(n) space""",
            "java": r"""// Set membership answers "seen before?" in O(1)
boolean containsDuplicate(int[] a) {
    Set<Integer> seen = new HashSet<>();
    for (int v : a) {
        if (!seen.add(v)) return true;   // add returns false if already present
    }
    return false;
}   // O(n) time · O(n) space""",
            "python": r"""def contains_duplicate(a):
    seen = set()
    for v in a:
        if v in seen:
            return True
        seen.add(v)
    return False""",
        },
    },
    {
        "slug": "valid-anagram",
        "title": "Valid Anagram",
        "difficulty": "Easy",
        "pattern": "frequency count 26",
        "statement": "Given two strings s and t, return true if t is an anagram of s — same characters with the same multiplicities.",
        "examples": [("s = \"anagram\", t = \"nagaram\"", "true"), ("s = \"rat\", t = \"car\"", "false")],
        "constraints": ["1 <= len(s), len(t) <= 5 * 10^4", "strings contain lowercase English letters only"],
        "approach": "Count each letter of s up, each letter of t down, and check that every counter returns to zero. Because the "
                    "alphabet is fixed at 26, a small array beats a hash map on both speed and allocation.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Fixed alphabet: a 26-slot array is the fastest "map"
bool isAnagram(string s, string t) {
    if (s.size() != t.size()) return false;
    array<int, 26> cnt{};                       // zero-initialised
    for (char c : s) cnt[c - 'a']++;
    for (char c : t) if (--cnt[c - 'a'] < 0) return false;
    return true;                                // every slot is back to zero
}   // O(n) time · O(1) space""",
            "java": r"""// Fixed alphabet: a 26-slot array is the fastest "map"
boolean isAnagram(String s, String t) {
    if (s.length() != t.length()) return false;
    int[] cnt = new int[26];
    for (char c : s.toCharArray()) cnt[c - 'a']++;
    for (char c : t.toCharArray()) if (--cnt[c - 'a'] < 0) return false;
    return true;                                // every slot is back to zero
}   // O(n) time · O(1) space""",
            "python": r"""def is_anagram(s, t):
    if len(s) != len(t):
        return False
    cnt = [0] * 26
    for c in s:
        cnt[ord(c) - 97] += 1
    for c in t:
        cnt[ord(c) - 97] -= 1
        if cnt[ord(c) - 97] < 0:
            return False
    return True""",
        },
    },
    {
        "slug": "first-unique-character",
        "title": "First Unique Character",
        "difficulty": "Easy",
        "pattern": "count then scan",
        "statement": "Return the index of the first character in the string that does not repeat anywhere else, or -1 if there is none.",
        "examples": [("s = \"leetcode\"", "0"), ("s = \"aabb\"", "-1")],
        "constraints": ["1 <= len(s) <= 10^5", "strings contain lowercase English letters only"],
        "approach": "Two passes: count everything first, then read the counts left to right and stop at the first 1. Trying to "
                    "answer in one pass fails because you cannot know whether a character seen now will repeat later.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Count in pass 1, decide in pass 2
int firstUniqChar(string s) {
    array<int, 26> cnt{};
    for (char c : s) cnt[c - 'a']++;
    for (int i = 0; i < (int)s.size(); i++)
        if (cnt[s[i] - 'a'] == 1) return i;
    return -1;
}   // O(n) time · O(1) space""",
            "java": r"""// Count in pass 1, decide in pass 2
int firstUniqChar(String s) {
    int[] cnt = new int[26];
    for (int i = 0; i < s.length(); i++) cnt[s.charAt(i) - 'a']++;
    for (int i = 0; i < s.length(); i++)
        if (cnt[s.charAt(i) - 'a'] == 1) return i;
    return -1;
}   // O(n) time · O(1) space""",
            "python": r"""def first_uniq_char(s):
    cnt = {}
    for c in s:
        cnt[c] = cnt.get(c, 0) + 1
    for i, c in enumerate(s):        # second pass keeps the left-to-right order
        if cnt[c] == 1:
            return i
    return -1""",
        },
    },
    {
        "slug": "intersection-of-two-arrays",
        "title": "Intersection of Two Arrays",
        "difficulty": "Easy",
        "pattern": "set intersection",
        "statement": "Return the *distinct* values that appear in both arrays; the result may be in any order.",
        "examples": [("[1,2,2,1], [2,2]", "[2]"), ("[4,9,5], [9,4,9,8,4]", "[9,4]")],
        "constraints": ["1 <= n, m <= 1000", "0 <= values <= 1000", "each element of the result must be unique"],
        "approach": "Put one array in a set, then walk the other and keep the values the set contains. Iterate over a snapshot of "
                    "the candidates (or build a separate result set) so you are not mutating the container you are scanning.",
        "complexity": ("O(n + m)", "O(n)"),
        "code": {
            "cpp": r"""// Set of one side, filter the other
vector<int> intersection(vector<int>& a, vector<int>& b) {
    unordered_set<int> have(a.begin(), a.end()), out;
    for (int v : b) if (have.count(v)) out.insert(v);   // dedupes for free
    return vector<int>(out.begin(), out.end());
}   // O(n + m) time · O(n) space""",
            "java": r"""// Set of one side, filter the other
int[] intersection(int[] a, int[] b) {
    Set<Integer> have = new HashSet<>(), out = new HashSet<>();
    for (int v : a) have.add(v);
    for (int v : b) if (have.contains(v)) out.add(v);   // dedupes for free
    int[] res = new int[out.size()]; int i = 0;
    for (int v : out) res[i++] = v;
    return res;
}   // O(n + m) time · O(n) space""",
            "python": r"""def intersection(a, b):
    have = set(a)
    return list({v for v in b if v in have})   # the set dedupes""",
        },
    },
    {
        "slug": "word-pattern",
        "title": "Word Pattern",
        "difficulty": "Easy",
        "pattern": "two-way bijection",
        "statement": "Given a pattern such as \"abba\" and a sentence such as \"dog cat cat dog\", decide whether the sentence follows "
                     "the pattern — a perfect one-to-one correspondence between pattern characters and words, in both directions.",
        "examples": [("pattern = \"abba\", s = \"dog cat cat dog\"", "true"),
                     ("pattern = \"abba\", s = \"dog cat cat fish\"", "false")],
        "constraints": ["1 <= pattern length <= 300", "s contains lowercase words separated by single spaces", "words may repeat"],
        "approach": "One map is not enough: \"ab\" vs \"dog dog\" would pass a char-to-word map alone (both map to dog) yet is not a "
                    "bijection. Keep a map in each direction and reject any clash — this 'two maps' idea reappears in isomorphic "
                    "strings, encoding problems and cipher puzzles.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Both directions, or the mapping is not a bijection
bool wordPattern(string pattern, string s) {
    vector<string> words;
    stringstream ss(s); string w;
    while (ss >> w) words.push_back(w);
    if (words.size() != pattern.size()) return false;
    unordered_map<char, string> c2w;
    unordered_map<string, char> w2c;
    for (int i = 0; i < (int)pattern.size(); i++) {
        char c = pattern[i];
        if (c2w.count(c) && c2w[c] != words[i]) return false;
        if (w2c.count(words[i]) && w2c[words[i]] != c) return false;
        c2w[c] = words[i];
        w2c[words[i]] = c;
    }
    return true;
}   // O(n) time · O(n) space""",
            "java": r"""// Both directions, or the mapping is not a bijection
boolean wordPattern(String pattern, String s) {
    String[] words = s.split(" ");
    if (words.length != pattern.length()) return false;
    Map<Character, String> c2w = new HashMap<>();
    Map<String, Character> w2c = new HashMap<>();
    for (int i = 0; i < words.length; i++) {
        char c = pattern.charAt(i);
        if (c2w.containsKey(c) && !c2w.get(c).equals(words[i])) return false;
        if (w2c.containsKey(words[i]) && w2c.get(words[i]) != c) return false;
        c2w.put(c, words[i]);
        w2c.put(words[i], c);
    }
    return true;
}   // O(n) time · O(n) space""",
            "python": r"""def word_pattern(pattern, s):
    words = s.split()
    if len(words) != len(pattern):
        return False
    c2w, w2c = {}, {}                       # both directions
    for c, w in zip(pattern, words):
        if c2w.setdefault(c, w) != w or w2c.setdefault(w, c) != c:
            return False
    return True""",
        },
    },
    # ---------------------------------------------------------------- MEDIUM
    {
        "slug": "group-anagrams",
        "title": "Group Anagrams",
        "difficulty": "Medium",
        "pattern": "canonical key",
        "statement": "Group the strings that are anagrams of each other and return the groups in any order.",
        "examples": [("[\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]",
                      "[[\"eat\",\"tea\",\"ate\"],[\"tan\",\"nat\"],[\"bat\"]]")],
        "constraints": ["1 <= number of strings <= 10^4", "each string has length 1..100", "lowercase letters only"],
        "approach": "Anagrams share a canonical form. Sorting each word (O(k log k)) is the portable choice; counting letters into a "
                    "26-length signature gives O(k) but needs care to be unambiguous — join the numbers with a separator, otherwise "
                    "[1,11] and [11,1] collide.",
        "complexity": ("O(n · k log k)", "O(n · k)"),
        "code": {
            "cpp": r"""// Sort each word into a canonical key
vector<vector<string>> groupAnagrams(vector<string>& words) {
    unordered_map<string, vector<string>> groups;
    for (const string& w : words) {
        string key = w;
        sort(key.begin(), key.end());          // anagrams share this key
        groups[key].push_back(w);
    }
    vector<vector<string>> out;
    for (auto& kv : groups) out.push_back(move(kv.second));
    return out;
}   // O(n · k log k) time · O(n · k) space""",
            "java": r"""// Sort each word into a canonical key
List<List<String>> groupAnagrams(String[] words) {
    Map<String, List<String>> groups = new HashMap<>();
    for (String w : words) {
        char[] c = w.toCharArray();
        Arrays.sort(c);                        // anagrams share this key
        groups.computeIfAbsent(new String(c), k -> new ArrayList<>()).add(w);
    }
    return new ArrayList<>(groups.values());
}   // O(n · k log k) time · O(n · k) space""",
            "python": r"""def group_anagrams(words):
    groups = {}
    for w in words:
        key = ''.join(sorted(w))            # anagrams share this key
        groups.setdefault(key, []).append(w)
    return list(groups.values())""",
        },
    },
    {
        "slug": "top-k-frequent-elements",
        "title": "Top K Frequent Elements",
        "difficulty": "Medium",
        "pattern": "count + bucket sort",
        "statement": "Return the k values that occur most often in the array; the answer is unique and may be returned in any order.",
        "examples": [("[1,1,1,2,2,3], k = 2", "[1,2]"), ("[1], k = 1", "[1]")],
        "constraints": ["1 <= n <= 10^5", "1 <= k <= number of distinct values", "answer is guaranteed unique"],
        "approach": "Count, then exploit that a frequency is at most n: build an array of buckets indexed by frequency and read "
                    "backwards. That trades the O(n log n) of sorting for O(n). A heap of size k is the alternative when memory is "
                    "tight or frequencies are not bounded by n.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Count, then bucket by frequency (frequencies are <= n)
vector<int> topKFrequent(vector<int>& a, int k) {
    unordered_map<int, int> cnt;
    for (int v : a) cnt[v]++;
    vector<vector<int>> bucket(a.size() + 1);
    for (auto& [v, c] : cnt) bucket[c].push_back(v);
    vector<int> out;
    for (int f = (int)a.size(); f >= 1 && (int)out.size() < k; f--)
        for (int v : bucket[f]) { out.push_back(v); if ((int)out.size() == k) break; }
    return out;
}   // O(n) time · O(n) space""",
            "java": r"""// Count, then bucket by frequency (frequencies are <= n)
int[] topKFrequent(int[] a, int k) {
    Map<Integer, Integer> cnt = new HashMap<>();
    for (int v : a) cnt.merge(v, 1, Integer::sum);
    List<Integer>[] bucket = new List[a.length + 1];
    for (var e : cnt.entrySet()) {
        int f = e.getValue();
        if (bucket[f] == null) bucket[f] = new ArrayList<>();
        bucket[f].add(e.getKey());
    }
    int[] out = new int[k]; int idx = 0;
    for (int f = a.length; f >= 1 && idx < k; f--)
        if (bucket[f] != null) for (int v : bucket[f]) { out[idx++] = v; if (idx == k) break; }
    return out;
}   // O(n) time · O(n) space""",
            "python": r"""def top_k_frequent(a, k):
    cnt = {}
    for v in a:
        cnt[v] = cnt.get(v, 0) + 1
    bucket = [[] for _ in range(len(a) + 1)]      # index = frequency
    for v, f in cnt.items():
        bucket[f].append(v)
    out = []
    for f in range(len(a), 0, -1):
        for v in bucket[f]:
            out.append(v)
            if len(out) == k:
                return out
    return out""",
        },
    },
    {
        "slug": "subarray-sum-equals-k",
        "title": "Subarray Sum Equals K",
        "difficulty": "Medium",
        "pattern": "prefix sum + count map",
        "statement": "Count the contiguous subarrays whose elements sum to exactly k. Values may be negative.",
        "examples": [("[1,1,1], k = 2", "2"), ("[1,2,3], k = 3", "2"), ("[1,-1,0], k = 0", "3")],
        "constraints": ["1 <= n <= 2 * 10^4", "-1000 <= values, k <= 1000", "subarrays must be contiguous and non-empty"],
        "approach": "A subarray sum is prefix[j] - prefix[i]. Fixing j turns the question into 'how many earlier prefixes equal "
                    "prefix[j] - k' — a dictionary lookup. Seed the map with {0: 1} so subarrays that start at index 0 are counted, "
                    "and note that negative values make a sliding window impossible.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// prefix[j] - prefix[i] == k  ->  count earlier prefixes
int subarraySum(vector<int>& a, int k) {
    unordered_map<long long, int> seen{{0, 1}};   // empty prefix
    long long run = 0; int count = 0;
    for (int v : a) {
        run += v;
        auto it = seen.find(run - k);             // how many prefixes end at run-k
        if (it != seen.end()) count += it->second;
        seen[run]++;
    }
    return count;
}   // O(n) time · O(n) space""",
            "java": r"""// prefix[j] - prefix[i] == k  ->  count earlier prefixes
int subarraySum(int[] a, int k) {
    Map<Long, Integer> seen = new HashMap<>();
    seen.put(0L, 1);                          // empty prefix
    long run = 0; int count = 0;
    for (int v : a) {
        run += v;
        count += seen.getOrDefault(run - k, 0);   // prefixes ending at run-k
        seen.merge(run, 1, Integer::sum);
    }
    return count;
}   // O(n) time · O(n) space""",
            "python": r"""def subarray_sum(a, k):
    seen = {0: 1}                 # empty prefix
    run = count = 0
    for v in a:
        run += v
        count += seen.get(run - k, 0)   # prefixes ending at run-k
        seen[run] = seen.get(run, 0) + 1
    return count""",
        },
    },
    {
        "slug": "longest-consecutive-sequence",
        "title": "Longest Consecutive Sequence",
        "difficulty": "Medium",
        "pattern": "hash set + only start at runs",
        "statement": "Given an unsorted array, return the length of the longest run of consecutive integers (for example "
                     "[100,4,200,1,3,2] contains 1,2,3,4). The algorithm must run in O(n).",
        "examples": [("[100,4,200,1,3,2]", "4"), ("[0,3,7,2,5,8,4,6,0,1]", "9")],
        "constraints": ["1 <= n <= 10^5", "-10^9 <= values <= 10^9", "the array is unsorted and may contain duplicates"],
        "approach": "Put every value in a set, then only expand runs whose value has no predecessor in the set. Each value is the "
                    "predecessor test's subject once, so the inner while-loop runs a total of O(n) times across the whole scan — that "
                    "is what makes the approach linear rather than quadratic despite the nested loop.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Only expand a run from its smallest element
int longestConsecutive(vector<int>& a) {
    unordered_set<int> s(a.begin(), a.end());
    int best = 0;
    for (int v : s) {
        if (s.count(v - 1)) continue;            // not the start of a run
        int len = 1;
        while (s.count(v + len)) len++;          // total work over all runs is O(n)
        best = max(best, len);
    }
    return best;
}   // O(n) time · O(n) space""",
            "java": r"""// Only expand a run from its smallest element
int longestConsecutive(int[] a) {
    Set<Integer> s = new HashSet<>();
    for (int v : a) s.add(v);
    int best = 0;
    for (int v : s) {
        if (s.contains(v - 1)) continue;         // not the start of a run
        int len = 1;
        while (s.contains(v + len)) len++;       // total work over all runs is O(n)
        best = Math.max(best, len);
    }
    return best;
}   // O(n) time · O(n) space""",
            "python": r"""def longest_consecutive(a):
    s = set(a)
    best = 0
    for v in s:
        if v - 1 in s:
            continue                # not the start of a run
        length = 1
        while v + length in s:      # total work over all runs is O(n)
            length += 1
        best = max(best, length)
    return best""",
        },
    },
    {
        "slug": "four-sum-count-ii",
        "title": "4Sum II — Counting Tuples",
        "difficulty": "Medium",
        "pattern": "meet in the middle with counts",
        "statement": "Given four arrays of equal length, count the tuples (i,j,k,l) with a[i] + b[j] + c[k] + d[l] = 0.",
        "examples": [("a=[1,2] b=[-2,-1] c=[-1,2] d=[0,2]", "2"), ("a=[0] b=[0] c=[0] d=[0]", "1")],
        "constraints": ["1 <= n <= 200", "-2^28 <= values <= 2^28", "the answer fits in a 32-bit signed integer"],
        "approach": "Splitting the equation into (a+b) and (c+d) is the whole trick: enumerating every pair costs O(n²) and the two "
                    "halves are then matched by lookup. A map from pair-sum to how many times it occurs makes the sweep of the second "
                    "half a plain dictionary read; the same split works for any 4-way counting problem.",
        "complexity": ("O(n²)", "O(n²)"),
        "code": {
            "cpp": r"""// Meet in the middle: hash the sum of every (a,b) pair
int fourSumCount(vector<int>& a, vector<int>& b, vector<int>& c, vector<int>& d) {
    unordered_map<int, int> ab;                  // pair sum -> count
    for (int x : a) for (int y : b) ab[x + y]++;
    int total = 0;
    for (int x : c) for (int y : d) {
        auto it = ab.find(-(x + y));             // need ab sum == -(cd sum)
        if (it != ab.end()) total += it->second;
    }
    return total;
}   // O(n²) time · O(n²) space""",
            "java": r"""// Meet in the middle: hash the sum of every (a,b) pair
int fourSumCount(int[] a, int[] b, int[] c, int[] d) {
    Map<Integer, Integer> ab = new HashMap<>();   // pair sum -> count
    for (int x : a) for (int y : b) ab.merge(x + y, 1, Integer::sum);
    int total = 0;
    for (int x : c) for (int y : d)
        total += ab.getOrDefault(-(x + y), 0);   // need ab sum == -(cd sum)
    return total;
}   // O(n²) time · O(n²) space""",
            "python": r"""def four_sum_count(a, b, c, d):
    ab = {}
    for x in a:
        for y in b:
            ab[x + y] = ab.get(x + y, 0) + 1
    total = 0
    for x in c:
        for y in d:
            total += ab.get(-(x + y), 0)      # need ab sum == -(cd sum)
    return total""",
        },
    },
    {
        "slug": "insert-delete-getrandom-o1",
        "title": "Insert, Delete and GetRandom in O(1)",
        "difficulty": "Medium",
        "pattern": "array + index map",
        "statement": "Design a set supporting insert(value), remove(value) and getRandom() (uniformly at random among the current "
                     "values), each in average O(1). Duplicates are ignored.",
        "examples": [("insert(1), insert(2), remove(1), getRandom()", "returns 2 with probability 1"),
                     ("insert(1), insert(1), getRandom()", "returns 1 (duplicate insert is a no-op)")],
        "constraints": ["up to 2 * 10^5 calls", "-2^31 <= values <= 2^31 - 1", "getRandom is called only when the set is non-empty"],
        "approach": "Random access needs an array; O(1) deletion from an array needs to know positions and to fill gaps. Keep an "
                    "array of values plus a map value → index: deleting means swapping the victim with the last element and popping, "
                    "then repairing the map. The map is what makes both halves O(1).",
        "complexity": ("O(1) average per op", "O(n)"),
        "code": {
            "cpp": r"""// Array for random access + map value->index for O(1) deletes
class RandomizedSet {
    vector<int> vals;
    unordered_map<int, int> idx;                 // value -> position in vals
public:
    bool insert(int v) {
        if (idx.count(v)) return false;
        idx[v] = (int)vals.size();
        vals.push_back(v);
        return true;
    }
    bool remove(int v) {
        auto it = idx.find(v);
        if (it == idx.end()) return false;
        int i = it->second, last = vals.back();
        vals[i] = last; idx[last] = i;           // move the last value into the hole
        vals.pop_back(); idx.erase(v);
        return true;
    }
    int getRandom() { return vals[rand() % vals.size()]; }
};   // O(1) average per op · O(n) space""",
            "java": r"""// Array for random access + map value->index for O(1) deletes
class RandomizedSet {
    private List<Integer> vals = new ArrayList<>();
    private Map<Integer, Integer> idx = new HashMap<>();   // value -> position
    private Random rnd = new Random();

    public boolean insert(int v) {
        if (idx.containsKey(v)) return false;
        idx.put(v, vals.size());
        vals.add(v);
        return true;
    }
    public boolean remove(int v) {
        Integer i = idx.get(v);
        if (i == null) return false;
        int last = vals.get(vals.size() - 1);
        vals.set(i, last); idx.put(last, i);      // move the last value into the hole
        vals.remove(vals.size() - 1); idx.remove(v);
        return true;
    }
    public int getRandom() { return vals.get(rnd.nextInt(vals.size())); }
}   // O(1) average per op · O(n) space""",
            "python": r"""import random

class RandomizedSet:
    def __init__(self):
        self.vals = []            # array gives O(1) random access
        self.idx = {}             # value -> position in vals

    def insert(self, v):
        if v in self.idx:
            return False
        self.idx[v] = len(self.vals)
        self.vals.append(v)
        return True

    def remove(self, v):
        if v not in self.idx:
            return False
        i, last = self.idx[v], self.vals[-1]
        self.vals[i] = last       # move the last value into the hole
        self.idx[last] = i
        self.vals.pop()
        del self.idx[v]
        return True

    def get_random(self):
        return random.choice(self.vals)""",
        },
    },
    {
        "slug": "valid-sudoku",
        "title": "Valid Sudoku",
        "difficulty": "Medium",
        "pattern": "composite keys in sets",
        "statement": "Decide whether a partially filled 9x9 Sudoku board is valid: no digit repeats within any row, any column or "
                     "any of the nine 3x3 boxes. Empty cells are '.' and the board need not be solvable.",
        "examples": [("a board with 8 in the top row twice", "false"), ("a partially filled legal board", "true")],
        "constraints": ["the board is always 9x9", "cells hold '1'-'9' or '.'", "only the already-placed digits are checked"],
        "approach": "One set per row, per column and per box, holding either the digit or a key that includes the digit. The box "
                    "index is (row/3)*3 + col/3 — computing that once and sharing the same 27-set machinery for all three rules keeps "
                    "the code short and hard to get wrong.",
        "complexity": ("O(1)", "O(1)"),
        "code": {
            "cpp": r"""// 27 sets: 9 rows, 9 columns, 9 boxes
bool isValidSudoku(vector<vector<char>>& board) {
    vector<unordered_set<char>> rows(9), cols(9), box(9);
    for (int r = 0; r < 9; r++)
        for (int c = 0; c < 9; c++) {
            char d = board[r][c];
            if (d == '.') continue;
            int b = (r / 3) * 3 + c / 3;          // which 3x3 box
            if (!rows[r].insert(d).second) return false;
            if (!cols[c].insert(d).second) return false;
            if (!box[b].insert(d).second) return false;
        }
    return true;
}   // O(1) time (the board is fixed size) · O(1) space""",
            "java": r"""// 27 sets: 9 rows, 9 columns, 9 boxes
boolean isValidSudoku(char[][] board) {
    Set<Character>[] rows = new HashSet[9], cols = new HashSet[9], box = new HashSet[9];
    for (int i = 0; i < 9; i++) { rows[i] = new HashSet<>(); cols[i] = new HashSet<>(); box[i] = new HashSet<>(); }
    for (int r = 0; r < 9; r++)
        for (int c = 0; c < 9; c++) {
            char d = board[r][c];
            if (d == '.') continue;
            int b = (r / 3) * 3 + c / 3;          // which 3x3 box
            if (!rows[r].add(d)) return false;
            if (!cols[c].add(d)) return false;
            if (!box[b].add(d)) return false;
        }
    return true;
}   // O(1) time (the board is fixed size) · O(1) space""",
            "python": r"""def is_valid_sudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    box = [set() for _ in range(9)]
    for r in range(9):
        for c in range(9):
            d = board[r][c]
            if d == '.':
                continue
            b = (r // 3) * 3 + c // 3          # which 3x3 box
            if d in rows[r] or d in cols[c] or d in box[b]:
                return False
            rows[r].add(d); cols[c].add(d); box[b].add(d)
    return True""",
        },
    },
    {
        "slug": "sort-characters-by-frequency",
        "title": "Sort Characters by Frequency",
        "difficulty": "Medium",
        "pattern": "count + bucket by frequency",
        "statement": "Reorder a string so that characters appear in decreasing order of frequency; characters with equal frequency may "
                     "appear in any relative order.",
        "examples": [("s = \"tree\"", "\"eert\" or \"eetr\""), ("s = \"Aabb\"", "\"bbAa\"")],
        "constraints": ["1 <= len(s) <= 5 * 10^5", "s holds ASCII characters", "any valid ordering is accepted"],
        "approach": "Count first, then either sort the distinct characters by count (O(k log k), simple) or bucket them by count "
                    "(O(n), same trick as Top K Frequent). Either way the output is assembled by repeating each character its own "
                    "number of times — never by sorting all n characters.",
        "complexity": ("O(n + k log k)", "O(n)"),
        "code": {
            "cpp": r"""// Count, sort the distinct characters, then expand
string frequencySort(string s) {
    unordered_map<char, int> cnt;
    for (char c : s) cnt[c]++;
    vector<pair<char, int>> items(cnt.begin(), cnt.end());
    sort(items.begin(), items.end(),
         [](auto& x, auto& y) { return x.second > y.second; });
    string out;
    for (auto& [c, f] : items) out.append(f, c);   // repeat c, f times
    return out;
}   // O(n + k log k) time · O(n) space""",
            "java": r"""// Count, sort the distinct characters, then expand
String frequencySort(String s) {
    Map<Character, Integer> cnt = new HashMap<>();
    for (char c : s.toCharArray()) cnt.merge(c, 1, Integer::sum);
    List<Character> keys = new ArrayList<>(cnt.keySet());
    keys.sort((x, y) -> cnt.get(y) - cnt.get(x));
    StringBuilder out = new StringBuilder();
    for (char c : keys) out.append(String.valueOf(c).repeat(cnt.get(c)));   // repeat
    return out.toString();
}   // O(n + k log k) time · O(n) space""",
            "python": r"""def frequency_sort(s):
    cnt = {}
    for c in s:
        cnt[c] = cnt.get(c, 0) + 1
    items = sorted(cnt.items(), key=lambda kv: -kv[1])
    return ''.join(c * f for c, f in items)   # repeat each character f times""",
        },
    },
    {
        "slug": "find-all-duplicates-in-array",
        "title": "Find All Duplicates in an Array",
        "difficulty": "Medium",
        "pattern": "the array indexes itself",
        "statement": "Given an array where every value is in 1..n (n = length) and each value appears once or twice, return the values "
                     "that appear twice, using no extra memory and O(n) time.",
        "examples": [("[4,3,2,7,8,2,3,1]", "[2,3]"), ("[1,1,2]", "[1]")],
        "constraints": ["1 <= n <= 10^5", "1 <= a[i] <= n", "each value occurs once or twice; extra memory must be O(1)"],
        "approach": "The values 1..n are themselves a perfect hash space: use the sign of a[|v|-1] as the flag for 'value |v| seen'. "
                    "The first visit flips the sign, the second visit finds it already flipped and records a duplicate, and afterwards "
                    "restoring the signs leaves the input unchanged.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Sign of a[|v|-1] is the "seen" flag — no extra memory
vector<int> findDuplicates(vector<int>& a) {
    vector<int> out;
    for (int v : a) {
        int i = abs(v) - 1;
        if (a[i] < 0) out.push_back(abs(v));      // second visit
        else a[i] = -a[i];                        // first visit: mark
    }
    for (int& v : a) v = abs(v);                  // restore the input
    return out;
}   // O(n) time · O(1) space""",
            "java": r"""// Sign of a[|v|-1] is the "seen" flag — no extra memory
List<Integer> findDuplicates(int[] a) {
    List<Integer> out = new ArrayList<>();
    for (int v : a) {
        int i = Math.abs(v) - 1;
        if (a[i] < 0) out.add(Math.abs(v));       // second visit
        else a[i] = -a[i];                        // first visit: mark
    }
    for (int i = 0; i < a.length; i++) a[i] = Math.abs(a[i]);   // restore
    return out;
}   // O(n) time · O(1) space""",
            "python": r"""def find_duplicates(a):
    out = []
    for v in a:
        i = abs(v) - 1
        if a[i] < 0:
            out.append(abs(v))    # second visit
        else:
            a[i] = -a[i]          # first visit: mark
    for i in range(len(a)):
        a[i] = abs(a[i])          # restore the input
    return out""",
        },
    },
    {
        "slug": "encode-and-decode-strings",
        "title": "Encode and Decode Strings",
        "difficulty": "Medium",
        "pattern": "self-describing encoding",
        "statement": "Design encode(list) and decode(string) that round-trip a list of arbitrary strings (which may contain any "
                     "character, including your own separator) through a single string.",
        "examples": [("[\"hello\",\"world\"]", "encode then decode returns [\"hello\",\"world\"]"),
                     ("[\"a\",\"\",\"b\"]", "empty strings must survive too")],
        "constraints": ["up to 200 strings per call", "each string has length 0..200", "the encoded string may use any characters"],
        "approach": "Any fixed delimiter breaks when the payload contains it. Prefix each string with its byte length and a marker, "
                    "then parse by reading the digits and slicing exactly that many characters — the decoder never guesses where a "
                    "string ends, so nothing can be escaped incorrectly.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// "<len>#<bytes>" — the length makes the delimiter unambiguous
string encode(const vector<string>& strs) {
    string out;
    for (const string& s : strs) out += to_string(s.size()) + "#" + s;
    return out;
}
vector<string> decode(const string& s) {
    vector<string> out;
    int i = 0;
    while (i < (int)s.size()) {
        int j = i;
        while (s[j] != '#') j++;                  // read the length digits
        int len = stoi(s.substr(i, j - i));
        out.push_back(s.substr(j + 1, len));      // take exactly len bytes
        i = j + 1 + len;
    }
    return out;
}   // O(n) time · O(n) space""",
            "java": r"""// "<len>#<bytes>" — the length makes the delimiter unambiguous
String encode(List<String> strs) {
    StringBuilder out = new StringBuilder();
    for (String s : strs) out.append(s.length()).append('#').append(s);
    return out.toString();
}
List<String> decode(String s) {
    List<String> out = new ArrayList<>();
    int i = 0;
    while (i < s.length()) {
        int j = i;
        while (s.charAt(j) != '#') j++;           // read the length digits
        int len = Integer.parseInt(s.substring(i, j));
        out.add(s.substring(j + 1, j + 1 + len)); // take exactly len bytes
        i = j + 1 + len;
    }
    return out;
}   // O(n) time · O(n) space""",
            "python": r"""def encode(strs):
    return ''.join(f'{len(s)}#{s}' for s in strs)   # "<len>#<bytes>"

def decode(s):
    out, i = [], 0
    while i < len(s):
        j = s.index('#', i)                # end of the length digits
        length = int(s[i:j])
        out.append(s[j + 1: j + 1 + length])   # take exactly length bytes
        i = j + 1 + length
    return out""",
        },
    },
    {
        "slug": "brick-wall",
        "title": "Brick Wall",
        "difficulty": "Medium",
        "pattern": "count edge positions",
        "statement": "A wall is a list of rows, each row a list of brick widths. Draw a vertical line from top to bottom: return the "
                     "minimum number of bricks that line crosses.",
        "examples": [("wall = [[1,2,2,1],[3,1,2],[1,3,2],[2,4],[3,1,2],[1,3,1,1]]", "2"),
                     ("wall = [[1],[1],[1]]", "3")],
        "constraints": ["1 <= rows <= 10^4", "1 <= total bricks on a row <= 10^4", "all rows are the same total width"],
        "approach": "Crossing fewest bricks means passing through the most gaps, and gaps only exist at the running x-positions of "
                    "row edges. Count how many rows have an edge at each x, take the best count, and the answer is (rows - best). "
                    "Skipping each row's final edge is essential: the right border is not a gap.",
        "complexity": ("O(total bricks)", "O(distinct edges)"),
        "code": {
            "cpp": r"""// Count rows that have a gap at each x
int leastBricks(vector<vector<int>>& wall) {
    unordered_map<int, int> gaps;                 // x -> rows with an edge there
    int best = 0;
    for (const auto& row : wall) {
        int x = 0;
        for (int i = 0; i + 1 < (int)row.size(); i++) {   // skip the last brick
            x += row[i];
            best = max(best, ++gaps[x]);
        }
    }
    return (int)wall.size() - best;
}   // O(total bricks) time · O(edges) space""",
            "java": r"""// Count rows that have a gap at each x
int leastBricks(List<List<Integer>> wall) {
    Map<Integer, Integer> gaps = new HashMap<>();  // x -> rows with an edge there
    int best = 0;
    for (List<Integer> row : wall) {
        int x = 0;
        for (int i = 0; i + 1 < row.size(); i++) { // skip the last brick
            x += row.get(i);
            int c = gaps.merge(x, 1, Integer::sum);
            best = Math.max(best, c);
        }
    }
    return wall.size() - best;
}   // O(total bricks) time · O(edges) space""",
            "python": r"""def least_bricks(wall):
    gaps = {}                      # x -> how many rows have an edge there
    best = 0
    for row in wall:
        x = 0
        for w in row[:-1]:         # skip the last brick of each row
            x += w
            gaps[x] = gaps.get(x, 0) + 1
            best = max(best, gaps[x])
    return len(wall) - best      # every row crossed minus the rows with a gap""",
        },
    },
    {
        "slug": "contiguous-array",
        "title": "Contiguous Array of Equal Zeros and Ones",
        "difficulty": "Medium",
        "pattern": "balance + first index",
        "statement": "Return the length of the longest contiguous subarray containing an equal number of 0s and 1s.",
        "examples": [("[0,1]", "2"), ("[0,1,0]", "2"), ("[0,0,1,1,0]", "4")],
        "constraints": ["1 <= n <= 10^5", "elements are exactly 0 or 1", "subarrays must be contiguous"],
        "approach": "Treat 1 as +1 and 0 as -1: equal counts mean a zero balance. Store the *first* index at which each balance occurs "
                    "and, on seeing a balance again, the distance between the two indices is a valid answer. First-seen, not "
                    "last-seen, is what maximises the length.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// +1 for 1, -1 for 0: equal counts = zero balance
int findMaxLength(vector<int>& a) {
    unordered_map<int, int> first{{0, -1}};       // balance -> earliest index
    int bal = 0, best = 0;
    for (int i = 0; i < (int)a.size(); i++) {
        bal += (a[i] == 1 ? 1 : -1);
        if (first.count(bal)) best = max(best, i - first[bal]);
        else first[bal] = i;                      // remember the earliest only
    }
    return best;
}   // O(n) time · O(n) space""",
            "java": r"""// +1 for 1, -1 for 0: equal counts = zero balance
int findMaxLength(int[] a) {
    Map<Integer, Integer> first = new HashMap<>();
    first.put(0, -1);                            // balance -> earliest index
    int bal = 0, best = 0;
    for (int i = 0; i < a.length; i++) {
        bal += (a[i] == 1 ? 1 : -1);
        Integer j = first.get(bal);
        if (j != null) best = Math.max(best, i - j);
        else first.put(bal, i);                  // remember the earliest only
    }
    return best;
}   // O(n) time · O(n) space""",
            "python": r"""def find_max_length(a):
    first = {0: -1}                # balance -> earliest index
    bal = best = 0
    for i, v in enumerate(a):
        bal += 1 if v == 1 else -1
        if bal in first:
            best = max(best, i - first[bal])
        else:
            first[bal] = i         # remember the earliest only
    return best""",
        },
    },
    # ------------------------------------------------------------------ HARD
    {
        "slug": "max-points-on-a-line",
        "title": "Max Points on a Line",
        "difficulty": "Hard",
        "pattern": "normalised slope keys",
        "statement": "Given n points in the plane, return the maximum number of points that lie on one straight line.",
        "examples": [("[[1,1],[2,2],[3,3]]", "3"), ("[[1,1],[3,2],[5,3],[4,1],[2,3],[1,4]]", "4")],
        "constraints": ["1 <= n <= 300", "-10^4 <= coordinates <= 10^4", "all points are unique"],
        "approach": "Fix one point as the anchor and count how many others share each direction. Storing a reduced fraction (dx/g, dy/g) "
                     "with gcd — plus sign normalisation, since (1,2) and (-1,-2) are the same line — makes slopes exact and immune to "
                     "floating-point error. Identical points are the `(0,0)` key and add to every count.",
        "complexity": ("O(n²)", "O(n)"),
        "code": {
            "cpp": r"""// Fix an anchor, count directions as reduced (dx,dy) keys
int maxPoints(vector<vector<int>>& pts) {
    int n = pts.size();
    if (n <= 2) return n;
    int best = 2;
    for (int i = 0; i < n; i++) {
        unordered_map<long long, int> dir;
        int dup = 0;
        for (int j = i + 1; j < n; j++) {
            long long dx = pts[j][0] - pts[i][0], dy = pts[j][1] - pts[i][1];
            if (dx == 0 && dy == 0) { dup++; continue; }   // same point
            long long g = gcd(abs(dx), abs(dy));
            dx /= g; dy /= g;
            if (dx < 0 || (dx == 0 && dy < 0)) { dx = -dx; dy = -dy; }  // normalise sign
            dir[dx * 100000 + dy]++;                        // exact integer key
        }
        for (auto& [k, c] : dir) best = max(best, c + 1 + dup);
        best = max(best, dup + 1);                          // all points identical
    }
    return best;
}   // O(n²) time · O(n) space""",
            "java": r"""// Fix an anchor, count directions as reduced (dx,dy) keys
int maxPoints(int[][] pts) {
    int n = pts.length;
    if (n <= 2) return n;
    int best = 2;
    for (int i = 0; i < n; i++) {
        Map<String, Integer> dir = new HashMap<>();
        int dup = 0;
        for (int j = i + 1; j < n; j++) {
            long dx = pts[j][0] - pts[i][0], dy = pts[j][1] - pts[i][1];
            if (dx == 0 && dy == 0) { dup++; continue; }    // same point
            long g = gcd(Math.abs(dx), Math.abs(dy));
            dx /= g; dy /= g;
            if (dx < 0 || (dx == 0 && dy < 0)) { dx = -dx; dy = -dy; }   // normalise
            dir.merge(dx + "," + dy, 1, Integer::sum);      // exact integer key
        }
        for (int c : dir.values()) best = Math.max(best, c + 1 + dup);
        best = Math.max(best, dup + 1);                     // all points identical
    }
    return best;
}
static long gcd(long a, long b) { return b == 0 ? a : gcd(b, a % b); }
// O(n²) time · O(n) space""",
            "python": r"""from math import gcd

def max_points(pts):
    n = len(pts)
    if n <= 2:
        return n
    best = 2
    for i in range(n):
        dirs = {}                       # reduced direction -> count
        dup = 0
        for j in range(i + 1, n):
            dx = pts[j][0] - pts[i][0]
            dy = pts[j][1] - pts[i][1]
            if dx == 0 and dy == 0:
                dup += 1                # duplicate point
                continue
            g = gcd(abs(dx), abs(dy))
            dx //= g; dy //= g
            if dx < 0 or (dx == 0 and dy < 0):   # normalise sign
                dx, dy = -dx, -dy
            dirs[(dx, dy)] = dirs.get((dx, dy), 0) + 1
        if dirs:
            best = max(best, max(dirs.values()) + 1 + dup)
        best = max(best, dup + 1)
    return best""",
        },
    },
    {
        "slug": "longest-duplicate-substring",
        "title": "Longest Duplicate Substring",
        "difficulty": "Hard",
        "pattern": "binary search + rolling hash",
        "statement": "Return any substring of length >= 1 that occurs at least twice in the string; if none exists return the empty "
                     "string.",
        "examples": [("s = \"banana\"", "\"ana\""), ("s = \"abcd\"", "\"\"")],
        "constraints": ["2 <= len(s) <= 3 * 10^4", "lowercase English letters", "both occurrences may overlap"],
        "approach": "If a duplicate of length L exists, so does one of every shorter length — the predicate is monotone, so binary "
                     "search L. Each test hashes all windows in O(n) with rolling hashes and looks for a repeat; using two moduli "
                     "makes accidental collisions negligible, which is the practical way to avoid comparing every pair of substrings.",
        "complexity": ("O(n log n)", "O(n)"),
        "code": {
            "cpp": r"""// Monotone in L: binary search the length, test with rolling hashes
string longestDupSubstring(string s) {
    const long long M1 = 1000000007, M2 = 998244353, B = 131;
    int n = s.size();
    vector<long long> p1(n + 1, 1), p2(n + 1, 1);
    for (int i = 1; i <= n; i++) { p1[i] = p1[i-1] * B % M1; p2[i] = p2[i-1] * B % M2; }

    auto findAt = [&](int L) -> int {            // start index of a repeat, or -1
        if (L == 0) return -1;
        unordered_map<long long, int> seen;
        long long h1 = 0, h2 = 0;
        for (int i = 0; i < n; i++) {
            h1 = (h1 * B + (unsigned char)s[i]) % M1;
            h2 = (h2 * B + (unsigned char)s[i]) % M2;
            if (i >= L) {
                h1 = (h1 - (long long)(unsigned char)s[i-L] * p1[L] % M1 + M1) % M1;
                h2 = (h2 - (long long)(unsigned char)s[i-L] * p2[L] % M2 + M2) % M2;
            }
            if (i >= L - 1) {
                long long key = h1 * M2 + h2;
                auto it = seen.find(key);
                if (it != seen.end()) return it->second;   // second occurrence
                seen[key] = i - L + 1;
            }
        }
        return -1;
    };

    int lo = 1, hi = n - 1, bestLen = 0, bestStart = -1;
    while (lo <= hi) {
        int mid = (lo + hi) / 2, start = findAt(mid);
        if (start >= 0) { bestLen = mid; bestStart = start; lo = mid + 1; }
        else hi = mid - 1;
    }
    return bestStart < 0 ? "" : s.substr(bestStart, bestLen);
}   // O(n log n) time · O(n) space""",
            "java": r"""// Monotone in L: binary search the length, test with rolling hashes
String longestDupSubstring(String s) {
    final long M1 = 1000000007L, M2 = 998244353L, B = 131L;
    int n = s.length();
    long[] p1 = new long[n + 1], p2 = new long[n + 1];
    p1[0] = p2[0] = 1;
    for (int i = 1; i <= n; i++) { p1[i] = p1[i-1] * B % M1; p2[i] = p2[i-1] * B % M2; }

    int lo = 1, hi = n - 1, bestLen = 0, bestStart = -1;
    while (lo <= hi) {
        int L = (lo + hi) / 2, start = -1;
        Map<Long, Integer> seen = new HashMap<>();
        long h1 = 0, h2 = 0;
        for (int i = 0; i < n && start < 0; i++) {
            h1 = (h1 * B + s.charAt(i)) % M1;
            h2 = (h2 * B + s.charAt(i)) % M2;
            if (i >= L) {
                h1 = (h1 - s.charAt(i - L) * p1[L] % M1 + M1) % M1;
                h2 = (h2 - s.charAt(i - L) * p2[L] % M2 + M2) % M2;
            }
            if (i >= L - 1) {
                long key = h1 * M2 + h2;
                Integer prev = seen.get(key);
                if (prev != null) start = prev;            // second occurrence
                else seen.put(key, i - L + 1);
            }
        }
        if (start >= 0) { bestLen = L; bestStart = start; lo = L + 1; }
        else hi = L - 1;
    }
    return bestStart < 0 ? "" : s.substring(bestStart, bestStart + bestLen);
}   // O(n log n) time · O(n) space""",
            "python": r"""def longest_dup_substring(s):
    M1, M2, B = 1_000_000_007, 998_244_353, 131
    n = len(s)
    p1 = [1] * (n + 1); p2 = [1] * (n + 1)
    for i in range(1, n + 1):
        p1[i] = p1[i-1] * B % M1
        p2[i] = p2[i-1] * B % M2

    def find_at(L):
        seen, h1, h2 = {}, 0, 0
        for i, ch in enumerate(s):
            c = ord(ch)
            h1 = (h1 * B + c) % M1
            h2 = (h2 * B + c) % M2
            if i >= L:
                h1 = (h1 - ord(s[i - L]) * p1[L]) % M1
                h2 = (h2 - ord(s[i - L]) * p2[L]) % M2
            if i >= L - 1:
                key = (h1, h2)                     # two moduli: collision-proof in practice
                if key in seen:
                    return seen[key]               # second occurrence
                seen[key] = i - L + 1
        return -1

    lo, hi, best_len, best_start = 1, n - 1, 0, -1
    while lo <= hi:                                # monotone predicate: binary search
        mid = (lo + hi) // 2
        start = find_at(mid)
        if start >= 0:
            best_len, best_start, lo = mid, start, mid + 1
        else:
            hi = mid - 1
    return '' if best_start < 0 else s[best_start:best_start + best_len]""",
        },
    },
    {
        "slug": "first-missing-positive",
        "title": "First Missing Positive",
        "difficulty": "Hard",
        "pattern": "index-as-bucket (cyclic placement)",
        "statement": "Given an unsorted integer array, return the smallest positive integer that does not appear in it, using O(1) extra "
                     "memory and O(n) time.",
        "examples": [("[1,2,0]", "3"), ("[3,4,-1,1]", "2"), ("[7,8,9,11,12]", "1")],
        "constraints": ["1 <= n <= 10^5", "-2^31 <= values <= 2^31 - 1", "extra space must be O(1)"],
        "approach": "The answer is always in 1..n+1, so every value in that range has a natural home: value v belongs at index v-1. "
                     "Swap each such value into its home (a while-loop, not an if, because the swapped-in value may also need placing), "
                     "then the first index whose slot does not hold index+1 is the answer.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Value v belongs at index v-1; place, then scan
int firstMissingPositive(vector<int>& a) {
    int n = a.size();
    for (int i = 0; i < n; i++)
        while (a[i] > 0 && a[i] <= n && a[a[i] - 1] != a[i])
            swap(a[i], a[a[i] - 1]);              // send a[i] to its home
    for (int i = 0; i < n; i++)
        if (a[i] != i + 1) return i + 1;          // first broken home
    return n + 1;                                 // 1..n are all present
}   // O(n) time (each swap fixes one value) · O(1) space""",
            "java": r"""// Value v belongs at index v-1; place, then scan
int firstMissingPositive(int[] a) {
    int n = a.length;
    for (int i = 0; i < n; i++)
        while (a[i] > 0 && a[i] <= n && a[a[i] - 1] != a[i]) {
            int t = a[a[i] - 1];                  // send a[i] to its home
            a[a[i] - 1] = a[i];
            a[i] = t;
        }
    for (int i = 0; i < n; i++)
        if (a[i] != i + 1) return i + 1;          // first broken home
    return n + 1;                                 // 1..n are all present
}   // O(n) time (each swap fixes one value) · O(1) space""",
            "python": r"""def first_missing_positive(a):
    n = len(a)
    for i in range(n):
        while 0 < a[i] <= n and a[a[i] - 1] != a[i]:
            home = a[i] - 1
            a[i], a[home] = a[home], a[i]     # send a[i] to its home
    for i in range(n):
        if a[i] != i + 1:
            return i + 1                      # first broken home
    return n + 1                              # 1..n are all present""",
        },
    },
    {
        "slug": "all-oone-data-structure",
        "title": "All O(1) Data Structure",
        "difficulty": "Hard",
        "pattern": "value->count map + count->bucket map",
        "statement": "Design inc(key), dec(key), getMaxKey() and getMinKey() so that all four run in O(1) average time. inc on a missing "
                     "key starts its count at 1; dec removes the key when its count reaches 0.",
        "examples": [("inc(\"a\"), inc(\"a\"), inc(\"b\"), getMaxKey()", "\"a\""),
                     ("after the above, getMinKey()", "\"b\"")],
        "constraints": ["up to 5 * 10^4 calls", "keys are non-empty strings", "every call must be O(1)"],
        "approach": "Two maps: key → count, and count → set of keys with that count. A move touches exactly two buckets, so the cost is "
                     "constant — but only if nothing scans for the minimum or maximum. Use an ordered bucket structure (or cached "
                     "min/max counts) so the extremes are a pointer read rather than a search.",
        "complexity": ("O(1) average per op", "O(n)"),
        "code": {
            "cpp": r"""// key->count plus count->bucket; extremes come from an ordered map
class AllOne {
    unordered_map<string, int> cnt;               // key -> count
    map<int, unordered_set<string>> bucket;       // count -> keys (ordered by count)
public:
    void inc(string key) {
        int c = cnt[key]++;                       // 0 for a new key
        if (c) {
            bucket[c].erase(key);
            if (bucket[c].empty()) bucket.erase(c);
        }
        bucket[c + 1].insert(key);
    }
    void dec(string key) {
        auto it = cnt.find(key);
        if (it == cnt.end()) return;
        int c = it->second;
        bucket[c].erase(key);
        if (bucket[c].empty()) bucket.erase(c);
        if (--it->second == 0) cnt.erase(it);
        else bucket[c - 1].insert(key);
    }
    string getMaxKey() {
        return bucket.empty() ? "" : *bucket.rbegin()->second.begin();
    }
    string getMinKey() {
        return bucket.empty() ? "" : *bucket.begin()->second.begin();
    }
};   // O(1) average per op (map operations on counts are O(log n) keys) · O(n) space""",
            "java": r"""// key->count plus count->bucket; extremes come from a TreeMap
class AllOne {
    private final Map<String, Integer> cnt = new HashMap<>();          // key -> count
    private final TreeMap<Integer, Set<String>> bucket = new TreeMap<>();  // count -> keys

    public void inc(String key) {
        int c = cnt.getOrDefault(key, 0);
        cnt.put(key, c + 1);
        if (c > 0) {
            Set<String> b = bucket.get(c);
            b.remove(key);
            if (b.isEmpty()) bucket.remove(c);
        }
        bucket.computeIfAbsent(c + 1, k -> new LinkedHashSet<>()).add(key);
    }
    public void dec(String key) {
        Integer c = cnt.get(key);
        if (c == null) return;
        Set<String> b = bucket.get(c);
        b.remove(key);
        if (b.isEmpty()) bucket.remove(c);
        if (c == 1) cnt.remove(key);
        else {
            cnt.put(key, c - 1);
            bucket.computeIfAbsent(c - 1, k -> new LinkedHashSet<>()).add(key);
        }
    }
    public String getMaxKey() {
        return bucket.isEmpty() ? "" : bucket.lastEntry().getValue().iterator().next();
    }
    public String getMinKey() {
        return bucket.isEmpty() ? "" : bucket.firstEntry().getValue().iterator().next();
    }
}   // O(log #counts) per op · O(n) space""",
            "python": r"""class AllOne:
    def __init__(self):
        self.cnt = {}                 # key -> count
        self.bucket = {}              # count -> set of keys
        self.min_c = 1                # smallest non-empty count
        self.max_c = 0                # largest non-empty count

    def _add(self, c, key):
        self.bucket.setdefault(c, set()).add(key)
        self.min_c = min(self.min_c, c)     # a fresh bucket may be the new minimum
        self.max_c = max(self.max_c, c)

    def _repair(self):
        # pointers mean nothing while their bucket is empty — drop them lazily
        while self.max_c > 0 and self.max_c not in self.bucket:
            self.max_c -= 1
        while self.min_c <= self.max_c and self.min_c not in self.bucket:
            self.min_c += 1

    def inc(self, key):
        c = self.cnt.get(key, 0)
        if c:
            self.bucket[c].discard(key)
            if not self.bucket[c]:
                del self.bucket[c]
        self.cnt[key] = c + 1
        self._add(c + 1, key)

    def dec(self, key):
        c = self.cnt.get(key)
        if c is None:
            return
        self.bucket[c].discard(key)
        if not self.bucket[c]:
            del self.bucket[c]
        if c == 1:
            del self.cnt[key]
        else:
            self.cnt[key] = c - 1
            self._add(c - 1, key)

    def get_max_key(self):
        self._repair()
        return next(iter(self.bucket[self.max_c])) if self.cnt else ''

    def get_min_key(self):
        self._repair()
        return next(iter(self.bucket[self.min_c])) if self.cnt else ''""",
        },
    },
    {
        "slug": "number-of-submatrices-that-sum-to-target",
        "title": "Submatrices That Sum to Target",
        "difficulty": "Hard",
        "pattern": "2D prefix sums + hash per column band",
        "statement": "Given a matrix and a target, count the non-empty submatrices whose elements sum to the target.",
        "examples": [("matrix = [[0,1,0],[1,1,1],[0,1,0]], target = 0", "4"),
                     ("matrix = [[1,-1],[-1,1]], target = 0", "5")],
        "constraints": ["1 <= rows, cols <= 100", "-1000 <= values, target <= 1000", "submatrices must be non-empty"],
        "approach": "A submatrix is a band of columns crossed with a contiguous run of rows. Fix the column band, collapse it into a "
                     "1-D column vector by adding rows as you widen, and the problem becomes 'subarray sum equals target' in 1-D — the "
                     "same prefix-sum-with-counts map you already know, now applied O(cols²) times.",
        "complexity": ("O(rows · cols²)", "O(rows)"),
        "code": {
            "cpp": r"""// Fix a column band, collapse it to 1-D, then count subarrays
int numSubmatrixSumTarget(vector<vector<int>>& m, int target) {
    int R = m.size(), C = m[0].size(), total = 0;
    for (int c1 = 0; c1 < C; c1++) {
        vector<int> rowSum(R, 0);
        for (int c2 = c1; c2 < C; c2++) {
            for (int r = 0; r < R; r++) rowSum[r] += m[r][c2];   // widen the band
            unordered_map<int, int> seen{{0, 1}};                // prefix -> count
            int run = 0;
            for (int r = 0; r < R; r++) {
                run += rowSum[r];
                auto it = seen.find(run - target);
                if (it != seen.end()) total += it->second;
                seen[run]++;
            }
        }
    }
    return total;
}   // O(rows · cols²) time · O(rows) space""",
            "java": r"""// Fix a column band, collapse it to 1-D, then count subarrays
int numSubmatrixSumTarget(int[][] m, int target) {
    int R = m.length, C = m[0].length, total = 0;
    for (int c1 = 0; c1 < C; c1++) {
        int[] rowSum = new int[R];
        for (int c2 = c1; c2 < C; c2++) {
            for (int r = 0; r < R; r++) rowSum[r] += m[r][c2];    // widen the band
            Map<Integer, Integer> seen = new HashMap<>();
            seen.put(0, 1);                                       // prefix -> count
            int run = 0;
            for (int r = 0; r < R; r++) {
                run += rowSum[r];
                total += seen.getOrDefault(run - target, 0);
                seen.merge(run, 1, Integer::sum);
            }
        }
    }
    return total;
}   // O(rows · cols²) time · O(rows) space""",
            "python": r"""def num_submatrix_sum_target(m, target):
    R, C, total = len(m), len(m[0]), 0
    for c1 in range(C):
        row_sum = [0] * R
        for c2 in range(c1, C):
            for r in range(R):
                row_sum[r] += m[r][c2]            # widen the band
            seen = {0: 1}                         # prefix sum -> count
            run = 0
            for r in range(R):
                run += row_sum[r]
                total += seen.get(run - target, 0)
                seen[run] = seen.get(run, 0) + 1
    return total""",
        },
    },
    {
        "slug": "palindrome-pairs",
        "title": "Palindrome Pairs",
        "difficulty": "Hard",
        "pattern": "split every word + reversed lookup",
        "statement": "Given a list of distinct words, return all index pairs (i, j) such that words[i] + words[j] is a palindrome.",
        "examples": [("[\"abcd\",\"dcba\",\"lls\",\"s\",\"sssll\"]", "[[0,1],[1,0],[3,2],[2,4]]"),
                     ("[\"bat\",\"tab\",\"cat\"]", "[[0,1],[1,0]]")],
        "constraints": ["1 <= number of words <= 5000", "0 <= word length <= 300", "all words are distinct"],
        "approach": "Fix a word and try every split w = left + right. If left is a palindrome then a reversed right placed in front "
                     "completes one pair; if right is a palindrome then a reversed left placed behind completes the other. Both cases "
                     "are dictionary lookups, so the total work is the sum of word lengths. Guard against pairing a word with itself and "
                     "against double-counting the empty suffix case.",
        "complexity": ("O(total characters)", "O(total characters)"),
        "code": {
            "cpp": r"""// Every split of every word is one dictionary lookup
vector<vector<int>> palindromePairs(vector<string>& words) {
    unordered_map<string, int> pos;
    for (int i = 0; i < (int)words.size(); i++) pos[words[i]] = i;
    set<vector<int>> res;
    auto rev = [](const string& s) { return string(s.rbegin(), s.rend()); };
    auto pal = [](const string& s) { return s == string(s.rbegin(), s.rend()); };

    for (int i = 0; i < (int)words.size(); i++) {
        const string& w = words[i];
        for (int cut = 0; cut <= (int)w.size(); cut++) {
            string left = w.substr(0, cut), right = w.substr(cut);
            if (pal(left)) {
                auto it = pos.find(rev(right));               // partner goes in front
                if (it != pos.end() && it->second != i) res.insert({it->second, i});
            }
            if (cut < (int)w.size() && pal(right)) {
                auto it = pos.find(rev(left));                // partner goes behind
                if (it != pos.end() && it->second != i) res.insert({i, it->second});
            }
        }
    }
    return vector<vector<int>>(res.begin(), res.end());
}   // O(total characters) time · O(total characters) space""",
            "java": r"""// Every split of every word is one dictionary lookup
List<List<Integer>> palindromePairs(String[] words) {
    Map<String, Integer> pos = new HashMap<>();
    for (int i = 0; i < words.length; i++) pos.put(words[i], i);
    Set<List<Integer>> res = new HashSet<>();

    for (int i = 0; i < words.length; i++) {
        String w = words[i];
        for (int cut = 0; cut <= w.length(); cut++) {
            String left = w.substring(0, cut), right = w.substring(cut);
            if (isPal(left)) {
                Integer j = pos.get(new StringBuilder(right).reverse().toString());
                if (j != null && j != i) res.add(Arrays.asList(j, i));   // partner in front
            }
            if (cut < w.length() && isPal(right)) {
                Integer j = pos.get(new StringBuilder(left).reverse().toString());
                if (j != null && j != i) res.add(Arrays.asList(i, j));   // partner behind
            }
        }
    }
    return new ArrayList<>(res);
}
static boolean isPal(String s) {
    for (int i = 0, j = s.length() - 1; i < j; i++, j--)
        if (s.charAt(i) != s.charAt(j)) return false;
    return true;
}   // O(total characters) time · O(total characters) space""",
            "python": r"""def palindrome_pairs(words):
    pos = {w: i for i, w in enumerate(words)}
    res = set()
    for i, w in enumerate(words):
        for cut in range(len(w) + 1):
            left, right = w[:cut], w[cut:]
            if left == left[::-1]:
                j = pos.get(right[::-1])        # partner goes in front
                if j is not None and j != i:
                    res.add((j, i))
            if cut < len(w) and right == right[::-1]:
                j = pos.get(left[::-1])         # partner goes behind
                if j is not None and j != i:
                    res.add((i, j))
    return [list(p) for p in res]""",
        },
    },
    {
        "slug": "subarrays-with-k-different-integers",
        "title": "Subarrays with K Different Integers",
        "difficulty": "Hard",
        "pattern": "exactly k = at most k minus at most k-1",
        "statement": "Count the contiguous subarrays that contain exactly k distinct values.",
        "examples": [("[1,2,1,2,3], k = 2", "7"), ("[1,2,1,3,4], k = 3", "3")],
        "constraints": ["1 <= n <= 2 * 10^4", "1 <= values, k <= n", "the answer fits in a 32-bit signed integer"],
        "approach": "The 'exactly k' window cannot be slid directly because both shrinking and growing can violate the rule. Instead "
                     "count windows with *at most* d distinct values — that predicate is monotone in d and window length, so a clever "
                     "two-pointer works — and subtract the answer for d = k-1 from the answer for d = k.",
        "complexity": ("O(n)", "O(k)"),
        "code": {
            "cpp": r"""// Monotone "at most d" windows, evaluated twice
int atMost(vector<int>& a, int d) {
    unordered_map<int, int> cnt;
    int l = 0, total = 0;
    for (int r = 0; r < (int)a.size(); r++) {
        cnt[a[r]]++;
        while ((int)cnt.size() > d) {                  // too many distinct
            if (--cnt[a[l]] == 0) cnt.erase(a[l]);
            l++;
        }
        total += r - l + 1;                            // windows ending at r
    }
    return total;
}
int subarraysWithKDistinct(vector<int>& a, int k) {
    return atMost(a, k) - atMost(a, k - 1);
}   // O(n) time · O(k) space""",
            "java": r"""// Monotone "at most d" windows, evaluated twice
int subarraysWithKDistinct(int[] a, int k) {
    return atMost(a, k) - atMost(a, k - 1);
}
private int atMost(int[] a, int d) {
    Map<Integer, Integer> cnt = new HashMap<>();
    int l = 0, total = 0;
    for (int r = 0; r < a.length; r++) {
        cnt.merge(a[r], 1, Integer::sum);
        while (cnt.size() > d) {                       // too many distinct
            cnt.merge(a[l], -1, Integer::sum);
            if (cnt.get(a[l]) == 0) cnt.remove(a[l]);
            l++;
        }
        total += r - l + 1;                            // windows ending at r
    }
    return total;
}   // O(n) time · O(k) space""",
            "python": r"""def subarrays_with_k_distinct(a, k):
    def at_most(d):
        cnt, l, total = {}, 0, 0
        for r, v in enumerate(a):
            cnt[v] = cnt.get(v, 0) + 1
            while len(cnt) > d:                # too many distinct
                cnt[a[l]] -= 1
                if cnt[a[l]] == 0:
                    del cnt[a[l]]
                l += 1
            total += r - l + 1                 # windows ending at r
        return total
    return at_most(k) - at_most(k - 1)""",
        },
    },
    {
        "slug": "count-array-pairs-divisible-by-k",
        "title": "Count Array Pairs Divisible by K",
        "difficulty": "Hard",
        "pattern": "gcd with k, then count divisors",
        "statement": "Count the index pairs (i, j) with i < j such that a[i] * a[j] is divisible by k.",
        "examples": [("[1,2,3,4,5], k = 2", "7"), ("[1,2,3,4], k = 4", "4")],
        "constraints": ["1 <= n <= 10^5", "1 <= values, k <= 10^5", "the answer fits in a 64-bit signed integer"],
        "approach": "Only gcd(value, k) matters, and it is always a divisor of k. Bucket values by that gcd, list the divisors of k, and "
                     "for each pair of divisors whose product is divisible by k add (count × count) — carefully separating distinct "
                     "divisors from the same-divisor choose-2 case.",
        "complexity": ("O(n + d²)", "O(d)"),
        "code": {
            "cpp": r"""// Bucket by gcd(v, k); combine divisor buckets
long long countPairs(vector<int>& a, int k) {
    unordered_map<int, long long> freq;
    for (int v : a) freq[gcd(v, k)]++;
    vector<int> divs;
    for (int d = 1; (long long)d * d <= k; d++)
        if (k % d == 0) { divs.push_back(d); if (d != k / d) divs.push_back(k / d); }
    long long total = 0;
    for (int i = 0; i < (int)divs.size(); i++)
        for (int j = i; j < (int)divs.size(); j++) {
            int d1 = divs[i], d2 = divs[j];
            if ((long long)d1 * d2 % k) continue;      // product must be divisible
            long long c1 = freq[d1], c2 = freq[d2];
            if (d1 == d2) total += c1 * (c1 - 1) / 2;  // same bucket: choose 2
            else total += c1 * c2;                     // cross buckets
        }
    return total;
}   // O(n + d²) time · O(d) space  (d = number of divisors of k)""",
            "java": r"""// Bucket by gcd(v, k); combine divisor buckets
long countPairs(int[] a, int k) {
    Map<Integer, Long> freq = new HashMap<>();
    for (int v : a) freq.merge(gcd(v, k), 1L, Long::sum);
    List<Integer> divs = new ArrayList<>();
    for (int d = 1; (long) d * d <= k; d++)
        if (k % d == 0) { divs.add(d); if (d != k / d) divs.add(k / d); }
    long total = 0;
    for (int i = 0; i < divs.size(); i++)
        for (int j = i; j < divs.size(); j++) {
            long d1 = divs.get(i), d2 = divs.get(j);
            if (d1 * d2 % k != 0) continue;            // product must be divisible
            long c1 = freq.getOrDefault((int) d1, 0L), c2 = freq.getOrDefault((int) d2, 0L);
            if (d1 == d2) total += c1 * (c1 - 1) / 2;  // same bucket: choose 2
            else total += c1 * c2;                     // cross buckets
        }
    return total;
}
static int gcd(int a, int b) { return b == 0 ? a : gcd(b, a % b); }
// O(n + d²) time · O(d) space  (d = number of divisors of k)""",
            "python": r"""from math import gcd

def count_pairs(a, k):
    freq = {}
    for v in a:
        g = gcd(v, k)
        freq[g] = freq.get(g, 0) + 1
    divs = [d for d in range(1, k + 1) if k % d == 0]   # divisors of k
    total = 0
    for i, d1 in enumerate(divs):
        for d2 in divs[i:]:
            if d1 * d2 % k:                 # product must be divisible by k
                continue
            c1, c2 = freq.get(d1, 0), freq.get(d2, 0)
            if d1 == d2:
                total += c1 * (c1 - 1) // 2  # same bucket: choose 2
            else:
                total += c1 * c2             # cross buckets
    return total""",
        },
    },
    {
        "slug": "maximum-number-of-visible-points",
        "title": "Maximum Number of Visible Points",
        "difficulty": "Hard",
        "pattern": "angles + circular sliding window",
        "statement": "Given your location and a list of points, you see the points whose direction is within angle degrees of some "
                     "half-line from you. Points at your exact location are always visible. Return the maximum you can see at once.",
        "examples": [("points = [[2,1],[2,2],[3,3]], angle = 90, location = [1,1]", "3"),
                     ("points = [[2,1],[2,2],[3,4],[1,1]], angle = 90, location = [1,1]", "4")],
        "constraints": ["1 <= n <= 10^5", "0 <= angle <= 359", "points and location are integer coordinates"],
        "approach": "A point is either at your location (always counted) or at an angle atan2(dy, dx). Sort the angles and duplicate "
                     "them shifted by 360° so a window may wrap around; a two-pointer scan then finds the largest window spanning at "
                     "most `angle` degrees. Compare with a tiny epsilon — floating-point angles that should be equal at the boundary "
                     "otherwise break the count.",
        "complexity": ("O(n log n)", "O(n)"),
        "code": {
            "cpp": r"""// Sort angles, duplicate +360, slide a two-pointer window
int visiblePoints(vector<vector<int>>& points, int angle, vector<int>& loc) {
    vector<double> a;
    int same = 0;
    for (auto& p : points) {
        double dx = p[0] - loc[0], dy = p[1] - loc[1];
        if (dx == 0 && dy == 0) { same++; continue; }   // always visible
        a.push_back(atan2(dy, dx) * 180.0 / M_PI);
    }
    sort(a.begin(), a.end());
    int m = a.size();
    for (int i = 0; i < m; i++) a.push_back(a[i] + 360.0);   // wrap-around
    int best = 0;
    for (int l = 0, r = 0; r < (int)a.size(); r++) {
        while (a[r] - a[l] > angle + 1e-9) l++;             // epsilon for ties
        best = max(best, r - l + 1);
    }
    return best + same;
}   // O(n log n) time · O(n) space""",
            "java": r"""// Sort angles, duplicate +360, slide a two-pointer window
int visiblePoints(List<List<Integer>> points, int angle, List<Integer> loc) {
    List<Double> a = new ArrayList<>();
    int same = 0;
    for (List<Integer> p : points) {
        double dx = p.get(0) - loc.get(0), dy = p.get(1) - loc.get(1);
        if (dx == 0 && dy == 0) { same++; continue; }     // always visible
        a.add(Math.toDegrees(Math.atan2(dy, dx)));
    }
    Collections.sort(a);
    int m = a.size();
    for (int i = 0; i < m; i++) a.add(a.get(i) + 360.0);  // wrap-around
    int best = 0;
    for (int l = 0, r = 0; r < a.size(); r++) {
        while (a.get(r) - a.get(l) > angle + 1e-9) l++;   // epsilon for ties
        best = Math.max(best, r - l + 1);
    }
    return best + same;
}   // O(n log n) time · O(n) space""",
            "python": r"""from math import atan2, degrees

def visible_points(points, angle, loc):
    angles, same = [], 0
    for x, y in points:
        dx, dy = x - loc[0], y - loc[1]
        if dx == 0 and dy == 0:
            same += 1                    # always visible
            continue
        angles.append(degrees(atan2(dy, dx)))
    angles.sort()
    n = len(angles)
    angles += [a + 360.0 for a in angles]     # wrap-around
    best, l = 0, 0
    for r in range(len(angles)):
        while angles[r] - angles[l] > angle + 1e-9:   # epsilon for ties
            l += 1
        best = max(best, r - l + 1)
    return best + same""",
        },
    },
    {
        "slug": "substring-with-largest-variance",
        "title": "Substring With Largest Variance",
        "difficulty": "Hard",
        "pattern": "per-letter-pair Kadane",
        "statement": "The variance of a substring is the largest difference between the number of occurrences of two of its letters. "
                     "Return the largest variance over all substrings of the string.",
        "examples": [("s = \"aababbb\"", "3"), ("s = \"abcde\"", "0")],
        "constraints": ["1 <= len(s) <= 10^4", "lowercase English letters", "a substring must have length at least 1"],
        "approach": "Try every ordered pair of letters (a, b): map a to +1 and b to -1 and find the maximum subarray sum that contains "
                     "at least one b. That extra condition is the whole difficulty — Kadane alone would return a run of pure a's — so "
                     "carry two running values: best sum that has already seen a b, and best sum with none.",
        "complexity": ("O(26² · n)", "O(1)"),
        "code": {
            "cpp": r"""// For each ordered pair (a, b): Kadane that must include a b
int largestVariance(string s) {
    int best = 0;
    for (char a = 'a'; a <= 'z'; a++)
        for (char b = 'a'; b <= 'z'; b++) {
            if (a == b) continue;
            int withB = 0, noB = 0;                 // running sums of each state
            bool seenB = false;
            for (char c : s) {
                if (c == a) { withB++; noB++; }
                else if (c == b) {
                    withB = max(seenB ? withB - 1 : INT_MIN, noB - 1);   // start or extend
                    noB = 0;
                    seenB = true;
                }
                if (seenB) best = max(best, withB);
            }
        }
    return best;
}   // O(26² · n) time · O(1) space""",
            "java": r"""// For each ordered pair (a, b): Kadane that must include a b
int largestVariance(String s) {
    int best = 0;
    for (char a = 'a'; a <= 'z'; a++)
        for (char b = 'a'; b <= 'z'; b++) {
            if (a == b) continue;
            int withB = 0, noB = 0;                 // running sums of each state
            boolean seenB = false;
            for (char c : s.toCharArray()) {
                if (c == a) { withB++; noB++; }
                else if (c == b) {
                    withB = Math.max(seenB ? withB - 1 : Integer.MIN_VALUE, noB - 1);
                    noB = 0;
                    seenB = true;
                }
                if (seenB) best = Math.max(best, withB);
            }
        }
    return best;
}   // O(26² · n) time · O(1) space""",
            "python": r"""def largest_variance(s):
    best = 0
    for a in set(s):                     # only letters that appear matter
        for b in set(s):
            if a == b:
                continue
            with_b = no_b = 0            # running sums of the two states
            seen_b = False
            for c in s:
                if c == a:
                    with_b += 1
                    no_b += 1
                elif c == b:
                    with_b = max(with_b - 1 if seen_b else -10**9, no_b - 1)
                    no_b = 0
                    seen_b = True
                if seen_b:
                    best = max(best, with_b)   # must contain a b
    return best""",
        },
    },
    {
        "slug": "maximum-frequency-stack",
        "title": "Maximum Frequency Stack",
        "difficulty": "Hard",
        "pattern": "value->count map + frequency stacks",
        "statement": "Design push(x) and pop(), where pop removes and returns the value with the highest frequency; ties break by the "
                     "value pushed most recently. pop is only called when the stack is non-empty.",
        "examples": [("push 5, push 7, push 5, push 7, push 4, push 5", "pops: 5, 7, 5, 4")],
        "constraints": ["up to 2 * 10^4 calls", "0 <= values <= 10^9", "pop is never called on an empty structure"],
        "approach": "Keep count[value] plus a list of stacks indexed by frequency: pushing x puts it on stack[count[x]+1], and popping "
                     "takes from the highest non-empty stack. The frequency-indexed stacks give the tie-break rule for free, because a "
                     "value only re-enters a high stack after it is pushed again.",
        "complexity": ("O(1) per op", "O(n)"),
        "code": {
            "cpp": r"""// Stacks indexed by frequency give frequency + recency order at once
class FreqStack {
    unordered_map<int, int> cnt;                       // value -> frequency
    vector<vector<int>> stacks;                        // stacks[f] = values seen f times
public:
    void push(int x) {
        int f = ++cnt[x];
        if (f > (int)stacks.size()) stacks.resize(f);
        stacks[f - 1].push_back(x);                    // index 0 holds frequency 1
    }
    int pop() {
        int x = stacks.back().back();
        stacks.back().pop_back();                      // highest frequency first
        if (stacks.back().empty()) stacks.pop_back();
        if (--cnt[x] == 0) cnt.erase(x);
        return x;
    }
};   // O(1) per op · O(n) space""",
            "java": r"""// Stacks indexed by frequency give frequency + recency order at once
class FreqStack {
    private final Map<Integer, Integer> cnt = new HashMap<>();   // value -> frequency
    private final List<Deque<Integer>> stacks = new ArrayList<>();

    public void push(int x) {
        int f = cnt.merge(x, 1, Integer::sum);
        if (f > stacks.size()) stacks.add(new ArrayDeque<>());
        stacks.get(f - 1).push(x);                                // index 0 = frequency 1
    }
    public int pop() {
        Deque<Integer> top = stacks.get(stacks.size() - 1);
        int x = top.pop();                                        // highest frequency first
        if (top.isEmpty()) stacks.remove(stacks.size() - 1);
        if (cnt.merge(x, -1, Integer::sum) == 0) cnt.remove(x);
        return x;
    }
}   // O(1) per op · O(n) space""",
            "python": r"""class FreqStack:
    def __init__(self):
        self.cnt = {}                 # value -> frequency
        self.stacks = []              # stacks[f] holds values seen f+1 times

    def push(self, x):
        f = self.cnt.get(x, 0) + 1
        self.cnt[x] = f
        if f > len(self.stacks):
            self.stacks.append([])
        self.stacks[f - 1].append(x)   # index 0 holds frequency 1

    def pop(self):
        x = self.stacks[-1].pop()      # highest frequency first
        if not self.stacks[-1]:
            self.stacks.pop()
        self.cnt[x] -= 1
        if self.cnt[x] == 0:
            del self.cnt[x]
        return x""",
        },
    },
    {
        "slug": "count-subarrays-with-median-k",
        "title": "Count Subarrays With Median K",
        "difficulty": "Hard",
        "pattern": "sign transform + balanced prefix pairs",
        "statement": "Given an array containing k exactly once, count how many subarrays have median exactly k (an odd-length "
                     "subarray's median is its middle element after sorting; even lengths use the lower middle).",
        "examples": [("[3,2,1,4,5], k = 4", "3"), ("[2,3,1], k = 3", "1")],
        "constraints": ["1 <= n <= 10^5", "k appears exactly once", "1 <= values <= n"],
        "approach": "Replace every element by +1 if it is > k, -1 if < k and 0 if it equals k. A subarray has median k exactly when it "
                     "contains that single 0 and its signs sum to 0 or 1 (the extra +1 covers even-length windows with the lower "
                     "middle). Counting then means matching prefix sums to the left and right of the 0, restricted to the block between "
                     "its neighbours' occurrences of k — which, since k is unique, is simply the whole array.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// sign(v - k); match prefix sums across the single k
long long countSubarrays(vector<int>& a, int k) {
    int n = a.size(), p = find(a.begin(), a.end(), k) - a.begin();
    vector<int> pre(n + 1, 0);
    for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + (a[i] > k ? 1 : a[i] < k ? -1 : 0);
    unordered_map<int, int> left;
    for (int i = p; i >= 0; i--) left[pre[i]]++;          // left endpoint choices
    long long total = 0;
    for (int j = p + 1; j <= n; j++) {                    // right endpoint choices
        int need1 = left.count(pre[j]);                   // sum == 0
        int need2 = left.count(pre[j] - 1);               // sum == 1 (even length)
        total += (need1 ? left[pre[j]] : 0) + (need2 ? left[pre[j] - 1] : 0);
    }
    return total;
}   // O(n) time · O(n) space""",
            "java": r"""// sign(v - k); match prefix sums across the single k
long countSubarrays(int[] a, int k) {
    int n = a.length, p = 0;
    for (int i = 0; i < n; i++) if (a[i] == k) p = i;
    int[] pre = new int[n + 1];
    for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + (a[i] > k ? 1 : a[i] < k ? -1 : 0);
    Map<Integer, Integer> left = new HashMap<>();
    for (int i = p; i >= 0; i--) left.merge(pre[i], 1, Integer::sum);   // left choices
    long total = 0;
    for (int j = p + 1; j <= n; j++) {                    // right endpoint choices
        total += left.getOrDefault(pre[j], 0);            // sum == 0
        total += left.getOrDefault(pre[j] - 1, 0);        // sum == 1 (even length)
    }
    return total;
}   // O(n) time · O(n) space""",
            "python": r"""def count_subarrays(a, k):
    n = len(a)
    p = a.index(k)
    pre = [0] * (n + 1)
    for i, v in enumerate(a):
        pre[i + 1] = pre[i] + (1 if v > k else -1 if v < k else 0)
    left = {}
    for i in range(p, -1, -1):            # left endpoint choices
        left[pre[i]] = left.get(pre[i], 0) + 1
    total = 0
    for j in range(p + 1, n + 1):         # right endpoint choices
        total += left.get(pre[j], 0)         # sum == 0
        total += left.get(pre[j] - 1, 0)     # sum == 1 (even length)
    return total""",
        },
    },
]
