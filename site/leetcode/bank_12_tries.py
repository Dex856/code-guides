# Topic 12 · Tries & String Algorithms
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.

TOPIC = {
    "name": "Tries & String Algorithms",
    "tagline": "A trie turns a dictionary into a walk — one edge per character, and every prefix is a place you can stand.",
    "focus": "Three ideas carry this topic. The trie stores a set of words so that prefixes, wildcards and prefix sums are a walk rather than a scan "
             "through every word. String matching algorithms (the KMP prefix function, rolling hashes, two-pointer chunking) compare two strings in "
             "linear time where the naive version would be quadratic. And the counting problems turn \"how many substrings\" into a contribution "
             "argument: for every position, count the substrings for which that position is the answer, instead of enumerating substrings.",
    "ordering": "easy 1–4 are single-pass scans and word accounting, 5–6 add a small trick (counting arrays, doubled-string containment); medium 1–6 "
                "build tries (plain, prefix-sum, root replacement, buildable words, suggestions, wildcard search), 7–9 are string parsing and windowing, "
                "10–12 are the hashing/index structures that lead into the hard tier; hard 1–5 push tries into streams, filtered suffix queries and board "
                "search, 6–9 are the classic linear-time matching tools (KMP, contribution counting, rolling hash), 10–12 are the largest DP-and-string "
                "combinations.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "length-of-last-word",
        "title": "Length of Last Word",
        "difficulty": "Easy",
        "pattern": "scan from the end",
        "statement": "Given a string s made of words and spaces, return the length of the last word.",
        "examples": [("s = \"Hello World\"", "5"), ("s = \" fly me to the moon \"", "4"), ("s = \"luffy is still joyboy\"", "6")],
        "constraints": ["1 <= s.length <= 10^4", "s contains only letters and spaces", "there is at least one word"],
        "approach": "Walk backwards: skip the trailing spaces first, then count characters until the next space. Scanning from the end means the rest of "
                     "the string is never touched, which is what makes this a one-pass, constant-space answer.",
        "complexity": ("O(n) time", "O(1)"),
        "code": {
            "cpp": r"""// Walk from the end: skip trailing spaces, then count the word
int lengthOfLastWord(string s) {
    int i = (int)s.size() - 1, len = 0;
    while (i >= 0 && s[i] == ' ') i--;           // skip the trailing spaces
    while (i >= 0 && s[i] != ' ') { len++; i--; }  // count until the next space
    return len;
}   // O(n) time · O(1) space""",
            "java": r"""// Walk from the end: skip trailing spaces, then count the word
int lengthOfLastWord(String s) {
    int i = s.length() - 1, len = 0;
    while (i >= 0 && s.charAt(i) == ' ') i--;    // skip the trailing spaces
    while (i >= 0 && s.charAt(i) != ' ') { len++; i--; }  // count the word
    return len;
}   // O(n) time · O(1) space""",
            "python": r"""def length_of_last_word(s):
    i = len(s) - 1
    while i >= 0 and s[i] == ' ':
        i -= 1                      # skip the trailing spaces
    length = 0
    while i >= 0 and s[i] != ' ':
        length += 1                 # count until the next space
        i -= 1
    return length""",
        },
    },
    {
        "slug": "reverse-words-in-a-string-iii",
        "title": "Reverse Words in a String III",
        "difficulty": "Easy",
        "pattern": "word splitting plus per-word reversal",
        "statement": "Reverse the characters of every word in s while keeping the words themselves in their original order and the spaces in place.",
        "examples": [("s = \"Let's take LeetCode contest\"", "\"s'teL ekat edoCteeL tsetnoc\""), ("s = \"Mr Ding\"", "\"rM gniD\"")],
        "constraints": ["1 <= s.length <= 5 · 10^4", "s contains printable ASCII characters", "words are separated by single spaces"],
        "approach": "Find each word's boundary and reverse only that range. The spaces never move, so the word order is preserved automatically and the "
                     "whole job is one pass over the characters.",
        "complexity": ("O(n) time", "O(n) for the mutable copy"),
        "code": {
            "cpp": r"""// Reverse each word in place; the spaces never move
string reverseWords(string s) {
    int n = (int)s.size(), i = 0;
    while (i < n) {
        int j = i;
        while (j < n && s[j] != ' ') j++;        // the current word is [i, j)
        reverse(s.begin() + i, s.begin() + j);
        i = j + 1;                               // skip the space
    }
    return s;
}   // O(n) time · O(n) space (the mutable copy)""",
            "java": r"""// Reverse each word in place; the spaces never move
String reverseWords(String s) {
    char[] a = s.toCharArray();
    int n = a.length, i = 0;
    while (i < n) {
        int j = i;
        while (j < n && a[j] != ' ') j++;        // the current word is [i, j)
        for (int l = i, r = j - 1; l < r; l++, r--) { char t = a[l]; a[l] = a[r]; a[r] = t; }
        i = j + 1;                               // skip the space
    }
    return new String(a);
}   // O(n) time · O(n) space""",
            "python": r"""def reverse_words_iii(s):
    chars = list(s)
    i, n = 0, len(chars)
    while i < n:
        j = i
        while j < n and chars[j] != ' ':
            j += 1                       # the current word is [i, j)
        chars[i:j] = chars[i:j][::-1]    # reverse just that slice
        i = j + 1                        # skip the space
    return ''.join(chars)""",
        },
    },
    {
        "slug": "sorting-the-sentence",
        "title": "Sorting the Sentence",
        "difficulty": "Easy",
        "pattern": "parse a trailing index",
        "statement": "A sentence contains words that each end in the digit giving their position (1-based). Return the sentence with the words in order "
                     "and the digits removed.",
        "examples": [("s = \"is2 sentence4 This1 a3\"", "\"This is a sentence\""), ("s = \"Myself2 Me1 I4 and3\"", "\"Me Myself and I\"")],
        "constraints": ["2 <= s.length <= 200", "words are separated by single spaces and each ends in one digit", "the digits are a permutation of 1..n"],
        "approach": "Split on spaces, then place each word at the index its own last character names. Writing straight into a correctly sized array makes "
                     "the sort unnecessary — the digits *are* the final positions.",
        "complexity": ("O(n) time", "O(n)"),
        "code": {
            "cpp": r"""// Each word's last character is its final position
string sortSentence(string s) {
    vector<string> words;
    stringstream ss(s);
    string w;
    while (ss >> w) words.push_back(w);
    vector<string> out(words.size());
    for (string& x : words) {
        int pos = x.back() - '1';                // 0-based position
        out[pos] = x.substr(0, x.size() - 1);    // drop the digit
    }
    string res;
    for (int i = 0; i < (int)out.size(); i++) {
        if (i) res += ' ';
        res += out[i];
    }
    return res;
}   // O(n) time · O(n) space""",
            "java": r"""// Each word's last character is its final position
String sortSentence(String s) {
    String[] words = s.split(" ");
    String[] out = new String[words.length];
    for (String w : words) {
        int pos = w.charAt(w.length() - 1) - '1';    // 0-based position
        out[pos] = w.substring(0, w.length() - 1);   // drop the digit
    }
    return String.join(" ", out);
}   // O(n) time · O(n) space""",
            "python": r"""def sort_sentence(s):
    words = s.split()
    out = [''] * len(words)
    for w in words:
        pos = int(w[-1]) - 1          # the trailing digit names the position
        out[pos] = w[:-1]             # drop the digit
    return ' '.join(out)""",
        },
    },
    {
        "slug": "uncommon-words-from-two-sentences",
        "title": "Uncommon Words from Two Sentences",
        "difficulty": "Easy",
        "pattern": "word frequency across two strings",
        "statement": "Return the words that appear exactly once across both sentences put together (order does not matter).",
        "examples": [("s1 = \"this apple is sweet\", s2 = \"this apple is sour\"", "[\"sweet\",\"sour\"]"),
                     ("s1 = \"apple apple\", s2 = \"banana\"", "[\"banana\"]")],
        "constraints": ["1 <= s1.length, s2.length <= 200", "sentences contain lowercase letters and single spaces"],
        "approach": "Count every word of both sentences in one table, then keep the entries whose count is exactly one. A word appearing twice inside a "
                     "single sentence is common just like one appearing in both, so the two sentences must be counted together rather than separately.",
        "complexity": ("O(n + m) time", "O(n + m)"),
        "code": {
            "cpp": r"""// One table for both sentences; keep the words seen exactly once
vector<string> uncommonFromSentences(string s1, string s2) {
    unordered_map<string,int> count;
    for (stringstream ss(s1 + " " + s2); ss >> std::ws, !ss.eof(); ) {
        string w;
        if (!(ss >> w)) break;
        count[w]++;
    }
    vector<string> out;
    for (auto& [w, c] : count)
        if (c == 1) out.push_back(w);
    return out;
}   // O(n + m) time · O(n + m) space""",
            "java": r"""// One table for both sentences; keep the words seen exactly once
List<String> uncommonFromSentences(String s1, String s2) {
    Map<String, Integer> count = new HashMap<>();
    for (String w : (s1 + " " + s2).split(" "))
        count.merge(w, 1, Integer::sum);
    List<String> out = new ArrayList<>();
    for (Map.Entry<String, Integer> e : count.entrySet())
        if (e.getValue() == 1) out.add(e.getKey());
    return out;
}   // O(n + m) time · O(n + m) space""",
            "python": r"""from collections import Counter

def uncommon_from_sentences(s1, s2):
    count = Counter(s1.split()) + Counter(s2.split())   # one shared table
    return [w for w, c in count.items() if c == 1]      # seen exactly once""",
        },
    },
    {
        "slug": "find-words-that-can-be-formed-by-characters",
        "title": "Find Words That Can Be Formed by Characters",
        "difficulty": "Easy",
        "pattern": "per-character counting",
        "statement": "Every word may use characters of `chars`, each character at most as many times as it appears there. Return the total length of all "
                     "words that can be formed.",
        "examples": [("words = [\"cat\",\"bt\",\"hat\",\"tree\"], chars = \"atach\"", "6"),
                     ("words = [\"hello\",\"world\",\"leetcode\"], chars = \"welldonehoneyr\"", "10")],
        "constraints": ["1 <= words.length <= 1000", "1 <= words[i].length, chars.length <= 100", "words and chars contain lowercase letters"],
        "approach": "Turn the available characters into 26 counts once, then test each word against a copy of those counts. A word survives exactly when "
                     "no letter needs more copies than the pool has.",
        "complexity": ("O(total characters) time", "O(1)"),
        "code": {
            "cpp": r"""// 26 counts for the pool; a word survives if it never overdraws
int countCharacters(vector<string>& words, string chars) {
    int pool[26] = {0};
    for (char c : chars) pool[c - 'a']++;
    int total = 0;
    for (const string& w : words) {
        int need[26] = {0};
        bool ok = true;
        for (char c : w)
            if (++need[c - 'a'] > pool[c - 'a']) { ok = false; break; }
        if (ok) total += w.size();
    }
    return total;
}   // O(total characters) time · O(1) space""",
            "java": r"""// 26 counts for the pool; a word survives if it never overdraws
int countCharacters(String[] words, String chars) {
    int[] pool = new int[26];
    for (char c : chars.toCharArray()) pool[c - 'a']++;
    int total = 0;
    for (String w : words) {
        int[] need = new int[26];
        boolean ok = true;
        for (char c : w.toCharArray())
            if (++need[c - 'a'] > pool[c - 'a']) { ok = false; break; }
        if (ok) total += w.length();
    }
    return total;
}   // O(total characters) time · O(1) space""",
            "python": r"""from collections import Counter

def count_characters(words, chars):
    pool = Counter(chars)              # how many of each letter are available
    total = 0
    for w in words:
        need = Counter(w)
        if all(need[ch] <= pool[ch] for ch in need):   # never overdraws
            total += len(w)
    return total""",
        },
    },
    {
        "slug": "rotate-string",
        "title": "Rotate String",
        "difficulty": "Easy",
        "pattern": "doubled string containment",
        "statement": "A rotation moves the first character of s to the end any number of times. Return true if goal can be produced this way.",
        "examples": [("s = \"abcde\", goal = \"cdeab\"", "true"), ("s = \"abcde\", goal = \"abced\"", "false")],
        "constraints": ["1 <= s.length, goal.length <= 100", "s and goal contain lowercase letters"],
        "approach": "Every rotation of s appears inside s + s, and every substring of s + s with the length of s is a rotation. So one containment test "
                     "answers the question — after checking the lengths, since containment alone would also accept longer strings.",
        "complexity": ("O(n) time (library search)", "O(n)"),
        "code": {
            "cpp": r"""// Every rotation of s is a length-n window of s + s
bool rotateString(string s, string goal) {
    if (s.size() != goal.size()) return false;
    return (s + s).find(goal) != string::npos;
}   // O(n) time · O(n) space""",
            "java": r"""// Every rotation of s is a length-n window of s + s
boolean rotateString(String s, String goal) {
    if (s.length() != goal.length()) return false;
    return (s + s).contains(goal);
}   // O(n) time · O(n) space""",
            "python": r"""def rotate_string(s, goal):
    if len(s) != len(goal):
        return False                   # different lengths can never match
    return goal in s + s               # every length-n window is a rotation""",
        },
    },
    # ---------------------------------------------------------------- MEDIUM
    {
        "slug": "implement-trie-prefix-tree",
        "title": "Implement Trie (Prefix Tree)",
        "difficulty": "Medium",
        "pattern": "build the trie",
        "statement": "Implement a trie with insert(word), search(word) and startsWith(prefix).",
        "examples": [("[\"Trie\",\"insert\",\"search\",\"search\",\"startsWith\",\"insert\",\"search\"] [[],[\"apple\"],[\"apple\"],[\"app\"],[\"app\"],[\"app\"],[\"app\"]]",
                      "[null, null, true, false, true, null, true]")],
        "constraints": ["1 <= word.length, prefix.length <= 2000", "words and prefixes consist of lowercase English letters", "at most 3 · 10^4 calls"],
        "approach": "Give every node 26 child slots and one flag meaning \"a word ends here\". insert walks the word, creating nodes as needed, and "
                     "search continues past the last character only to read that flag, while startsWith simply stops walking — that one flag is the "
                     "whole difference between the two queries.",
        "complexity": ("O(L) per operation", "O(total characters inserted)"),
        "code": {
            "cpp": r"""// 26 child slots per node plus one "a word ends here" flag
class Trie {
public:
    struct Node {
        Node* kids[26] = {};
        bool ends = false;
    };
    Node* root = new Node();
    void insert(string word) {
        Node* cur = root;
        for (char c : word) {
            int i = c - 'a';
            if (!cur->kids[i]) cur->kids[i] = new Node();
            cur = cur->kids[i];
        }
        cur->ends = true;                        // a word stops here
    }
    bool search(string word) {
        Node* cur = walk(word);
        return cur && cur->ends;                 // ... and only here
    }
    bool startsWith(string prefix) {
        return walk(prefix) != nullptr;          // any node on the path will do
    }
private:
    Node* walk(const string& s) {
        Node* cur = root;
        for (char c : s) {
            cur = cur->kids[c - 'a'];
            if (!cur) return nullptr;
        }
        return cur;
    }
};   // O(L) per operation · O(total characters) space""",
            "java": r"""// 26 child slots per node plus one "a word ends here" flag
class Trie {
    class Node {
        Node[] kids = new Node[26];
        boolean ends;
    }
    private final Node root = new Node();
    public void insert(String word) {
        Node cur = root;
        for (char c : word.toCharArray()) {
            int i = c - 'a';
            if (cur.kids[i] == null) cur.kids[i] = new Node();
            cur = cur.kids[i];
        }
        cur.ends = true;                         // a word stops here
    }
    public boolean search(String word) {
        Node cur = walk(word);
        return cur != null && cur.ends;          // ... and only here
    }
    public boolean startsWith(String prefix) {
        return walk(prefix) != null;             // any node on the path will do
    }
    private Node walk(String s) {
        Node cur = root;
        for (char c : s.toCharArray()) {
            cur = cur.kids[c - 'a'];
            if (cur == null) return null;
        }
        return cur;
    }
}   // O(L) per operation · O(total characters) space""",
            "python": r"""class Trie:
    def __init__(self):
        self.root = {}                     # node: char -> node, '#' marks a word

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node['#'] = True                   # a word stops here

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node:
                return None
            node = node[ch]
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and '#' in node   # ... and only here

    def startsWith(self, prefix):
        return self._walk(prefix) is not None     # any node on the path""",
        },
    },
    {
        "slug": "map-sum-pairs",
        "title": "Map Sum Pairs",
        "difficulty": "Medium",
        "pattern": "trie with prefix sums",
        "statement": "Implement insert(key, val), which overwrites any earlier value for that key, and sum(prefix), which returns the total value of all "
                     "keys that start with prefix.",
        "examples": [("[\"MapSum\",\"insert\",\"sum\",\"insert\",\"sum\"] [[],[\"apple\",3],[\"ap\"],[\"app\",2],[\"ap\"]]",
                      "[null, null, 3, null, 5]")],
        "constraints": ["1 <= key.length, prefix.length <= 50", "keys and prefixes are lowercase letters", "at most 50 calls of each operation"],
        "approach": "Store the total of the subtree at every node, and keep the current value of each key. Overwriting a key then means walking once "
                     "more and adding only the *difference* to the nodes on the path, which keeps insert O(L) instead of rebuilding anything.",
        "complexity": ("O(L) per operation", "O(total characters)"),
        "code": {
            "cpp": r"""// Every node knows the total of the keys passing through it
class MapSum {
public:
    struct Node {
        unordered_map<char, Node*> kids;
        int total = 0;
    };
    Node* root = new Node();
    unordered_map<string,int> value;
    void insert(string key, int val) {
        int delta = val - value[key];            // only the change is pushed down
        value[key] = val;
        Node* cur = root;
        for (char c : key) {
            if (!cur->kids[c]) cur->kids[c] = new Node();
            cur = cur->kids[c];
            cur->total += delta;
        }
    }
    int sum(string prefix) {
        Node* cur = root;
        for (char c : prefix) {
            if (!cur->kids.count(c)) return 0;   // no key has this prefix
            cur = cur->kids[c];
        }
        return cur->total;                       // the whole subtree
    }
};   // O(L) per operation · O(total characters) space""",
            "java": r"""// Every node knows the total of the keys passing through it
class MapSum {
    class Node {
        Map<Character, Node> kids = new HashMap<>();
        int total;
    }
    private final Node root = new Node();
    private final Map<String, Integer> value = new HashMap<>();
    public void insert(String key, int val) {
        int delta = val - value.getOrDefault(key, 0);   // only the change
        value.put(key, val);
        Node cur = root;
        for (char c : key.toCharArray()) {
            cur = cur.kids.computeIfAbsent(c, k -> new Node());
            cur.total += delta;
        }
    }
    public int sum(String prefix) {
        Node cur = root;
        for (char c : prefix.toCharArray()) {
            cur = cur.kids.get(c);
            if (cur == null) return 0;           // no key has this prefix
        }
        return cur.total;                        // the whole subtree
    }
}   // O(L) per operation · O(total characters) space""",
            "python": r"""class MapSum:
    def __init__(self):
        self.root = {}                     # node: char -> node
        self.total = {}                    # node id -> subtree total
        self.value = {}                    # key -> current value

    def insert(self, key, val):
        delta = val - self.value.get(key, 0)     # only the change moves down
        self.value[key] = val
        node = self.root
        for ch in key:
            nxt = node.setdefault(ch, {})
            self.total[id(nxt)] = self.total.get(id(nxt), 0) + delta
            node = nxt

    def sum(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node:
                return 0                     # no key has this prefix
            node = node[ch]
        return self.total.get(id(node), 0)   # the whole subtree""",
        },
    },
    {
        "slug": "replace-words",
        "title": "Replace Words",
        "difficulty": "Medium",
        "pattern": "trie for shortest-prefix lookup",
        "statement": "Given a dictionary of roots and a sentence, replace every word by the shortest root that is one of its prefixes; a word with no "
                     "such root stays as it is.",
        "examples": [("dictionary = [\"cat\",\"bat\",\"rat\"], sentence = \"the cattle was rattled by the battery\"", "\"the cat was rat by the bat\""),
                     ("dictionary = [\"a\",\"b\",\"c\"], sentence = \"aadsfasf absbs bbab cadsfafs\"", "\"a a b c\"")],
        "constraints": ["1 <= dictionary.length <= 1000", "1 <= sentence.length <= 10^6", "dictionary words and sentence words are lowercase"],
        "approach": "Put the roots in a trie and walk each word character by character. The first node marked as a word end gives the shortest root, so "
                     "the walk can stop there even though longer roots also lie down the same path.",
        "complexity": ("O(total characters) time", "O(total root characters)"),
        "code": {
            "cpp": r"""// Walk each word through the root trie and stop at the first root end
string replaceWords(vector<string>& dictionary, string sentence) {
    struct Node { Node* kids[26] = {}; bool ends = false; };
    Node* root = new Node();
    for (const string& r : dictionary) {
        Node* cur = root;
        for (char c : r) {
            if (!cur->kids[c - 'a']) cur->kids[c - 'a'] = new Node();
            cur = cur->kids[c - 'a'];
        }
        cur->ends = true;                        // a root stops here
    }
    string out;
    stringstream ss(sentence);
    string word;
    bool first = true;
    while (ss >> word) {
        if (!first) out += ' ';
        first = false;
        Node* cur = root;
        string replacement = word;               // stays whole if no root fits
        for (int i = 0; i < (int)word.size(); i++) {
            cur = cur->kids[word[i] - 'a'];
            if (!cur) break;
            if (cur->ends) { replacement = word.substr(0, i + 1); break; }
        }
        out += replacement;
    }
    return out;
}   // O(total characters) time · O(total root characters) space""",
            "java": r"""// Walk each word through the root trie and stop at the first root end
String replaceWords(List<String> dictionary, String sentence) {
    Node root = new Node();
    for (String r : dictionary) {                // build the root trie
        Node cur = root;
        for (char c : r.toCharArray()) {
            int i = c - 'a';
            if (cur.kids[i] == null) cur.kids[i] = new Node();
            cur = cur.kids[i];
        }
        cur.ends = true;                         // a root stops here
    }
    String[] words = sentence.split(" ");
    for (int w = 0; w < words.length; w++) {
        Node cur = root;
        for (int i = 0; i < words[w].length(); i++) {
            cur = cur.kids[words[w].charAt(i) - 'a'];
            if (cur == null) break;
            if (cur.ends) { words[w] = words[w].substring(0, i + 1); break; }
        }
    }
    return String.join(" ", words);
}
static class Node { Node[] kids = new Node[26]; boolean ends; }   // O(total chars) time""",
            "python": r"""def replace_words(dictionary, sentence):
    root = {}
    for r in dictionary:                 # build the root trie
        node = root
        for ch in r:
            node = node.setdefault(ch, {})
        node['#'] = True                 # a root stops here

    def shortest(word):
        node = root
        for i, ch in enumerate(word):
            if ch not in node:
                break
            node = node[ch]
            if '#' in node:
                return word[:i+1]        # the shortest root found first
        return word                      # no root fits: keep the word

    return ' '.join(shortest(w) for w in sentence.split())""",
        },
    },
    {
        "slug": "longest-word-in-dictionary",
        "title": "Longest Word in Dictionary",
        "difficulty": "Medium",
        "pattern": "buildable prefixes",
        "statement": "Return the longest word that can be built one character at a time using only words of the list; when several words tie, return the "
                     "lexicographically smallest.",
        "examples": [("words = [\"w\",\"wo\",\"wor\",\"worl\",\"world\"]", "\"world\""),
                     ("words = [\"a\",\"banana\",\"app\",\"appl\",\"ap\",\"apply\",\"apple\"]", "\"apple\"")],
        "constraints": ["1 <= words.length <= 1000", "1 <= words[i].length <= 30", "words contain lowercase letters"],
        "approach": "Sort the words, then sweep once keeping a set of the words already proven buildable. A word is buildable exactly when its prefix "
                     "without the last character is buildable (or it has length one), and sorting makes \"first longest\" also \"lexicographically "
                     "smallest\".",
        "complexity": ("O(n log n + total characters)", "O(n)"),
        "code": {
            "cpp": r"""// Sort, then keep the set of words that can be built up to
string longestWord(vector<string>& words) {
    sort(words.begin(), words.end());
    unordered_set<string> buildable;
    string best;
    for (const string& w : words) {
        if (w.size() == 1 || buildable.count(w.substr(0, w.size() - 1))) {
            buildable.insert(w);
            if (w.size() > best.size()) best = w;   // sorted order breaks ties
        }
    }
    return best;
}   // O(n log n + total characters) time · O(n) space""",
            "java": r"""// Sort, then keep the set of words that can be built up to
String longestWord(String[] words) {
    Arrays.sort(words);
    Set<String> buildable = new HashSet<>();
    String best = "";
    for (String w : words) {
        if (w.length() == 1 || buildable.contains(w.substring(0, w.length() - 1))) {
            buildable.add(w);
            if (w.length() > best.length()) best = w;   // sorted order breaks ties
        }
    }
    return best;
}   // O(n log n + total characters) time · O(n) space""",
            "python": r"""def longest_word(words):
    words.sort()                        # alphabetical order settles the tie
    buildable = set()
    best = ''
    for w in words:
        if len(w) == 1 or w[:-1] in buildable:      # one character at a time
            buildable.add(w)
            if len(w) > len(best):
                best = w                # the first word of this length wins
    return best""",
        },
    },
    {
        "slug": "search-suggestions-system",
        "title": "Search Suggestions System",
        "difficulty": "Medium",
        "pattern": "sorted list plus prefix lookup",
        "statement": "Type the characters of searchWord one at a time and after each keystroke return up to three products having the typed text as a "
                     "prefix, in lexicographic order.",
        "examples": [("products = [\"mobile\",\"mouse\",\"moneypot\",\"monitor\",\"mousepad\"], searchWord = \"mouse\"",
                      "[[\"mobile\",\"moneypot\",\"monitor\"],[\"mobile\",\"moneypot\",\"monitor\"],[\"mouse\",\"mousepad\"],[\"mouse\",\"mousepad\"],[\"mouse\",\"mousepad\"]]"),
                     ("products = [\"havana\"], searchWord = \"havana\"", "[[\"havana\"],[\"havana\"],[\"havana\"],[\"havana\"],[\"havana\"],[\"havana\"]]")],
        "constraints": ["1 <= products.length <= 1000", "1 <= products[i].length <= 3000", "1 <= searchWord.length <= 1000", "all products are distinct"],
        "approach": "Sort the products once. For each prefix, the matching products form one contiguous block starting at the first product that is not "
                     "smaller than the prefix — a binary search finds that start, and the next three entries are the suggestion.",
        "complexity": ("O(n log n + |searchWord| · (log n + 3))", "O(n) for the sorted copy"),
        "code": {
            "cpp": r"""// Sort once; each prefix is a contiguous block after a lower_bound
vector<vector<string>> suggestedProducts(vector<string>& products, string searchWord) {
    sort(products.begin(), products.end());
    vector<vector<string>> out;
    string prefix;
    for (char c : searchWord) {
        prefix += c;
        auto it = lower_bound(products.begin(), products.end(), prefix);   // first >= prefix
        vector<string> picks;
        for (auto j = it; j != products.end() && picks.size() < 3; j++) {
            if (j->compare(0, prefix.size(), prefix) != 0) break;          // block ended
            picks.push_back(*j);
        }
        out.push_back(picks);
    }
    return out;
}   // O(n log n + |searchWord| log n) time · O(n) space (the sorted copy)""",
            "java": r"""// Sort once; each prefix is a contiguous block after a lower bound
List<List<String>> suggestedProducts(String[] products, String searchWord) {
    Arrays.sort(products);
    List<List<String>> out = new ArrayList<>();
    StringBuilder prefix = new StringBuilder();
    for (char c : searchWord.toCharArray()) {
        prefix.append(c);
        String p = prefix.toString();
        int lo = 0, hi = products.length;            // first index with products[i] >= p
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (products[mid].compareTo(p) < 0) lo = mid + 1; else hi = mid;
        }
        List<String> picks = new ArrayList<>();
        for (int i = lo; i < products.length && picks.size() < 3; i++) {
            if (!products[i].startsWith(p)) break;  // the block ended
            picks.add(products[i]);
        }
        out.add(picks);
    }
    return out;
}   // O(n log n + |searchWord| log n) time · O(n) space""",
            "python": r"""from bisect import bisect_left

def suggested_products(products, search_word):
    products.sort()
    out = []
    prefix = ''
    for ch in search_word:
        prefix += ch
        start = bisect_left(products, prefix)      # first product >= prefix
        picks = []
        for i in range(start, min(start + 3, len(products))):
            if not products[i].startswith(prefix):
                break                              # the matching block ended
            picks.append(products[i])
        out.append(picks)
    return out""",
        },
    },
    {
        "slug": "design-add-and-search-words-data-structure",
        "title": "Design Add and Search Words Data Structure",
        "difficulty": "Medium",
        "pattern": "trie with wildcard search",
        "statement": "Implement WordDictionary with addWord(word) and search(word), where a '.' in the query matches any single letter.",
        "examples": [("[\"WordDictionary\",\"addWord\",\"addWord\",\"addWord\",\"search\",\"search\",\"search\",\"search\"] [[],[\"bad\"],[\"dad\"],[\"mad\"],[\"pad\"],[\"bad\"],[\".ad\"],[\"b..\"]]",
                      "[null,null,null,null,false,true,true,true]")],
        "constraints": ["1 <= word.length <= 25", "word and queries contain lowercase letters and '.'", "at most 10^4 calls"],
        "approach": "Keep the usual trie, but make the query a depth-first walk: a normal character follows one edge, while a '.' tries every child of "
                     "the current node at that depth. The search only branches when a wildcard appears, so ordinary lookups stay linear.",
        "complexity": ("O(L) for a plain word, O(26^dots · L) worst case", "O(total characters)"),
        "code": {
            "cpp": r"""// Trie lookups, but a '.' branches into every child at that depth
class WordDictionary {
public:
    struct Node {
        Node* kids[26] = {};
        bool ends = false;
    };
    Node* root = new Node();
    void addWord(string word) {
        Node* cur = root;
        for (char c : word) {
            int i = c - 'a';
            if (!cur->kids[i]) cur->kids[i] = new Node();
            cur = cur->kids[i];
        }
        cur->ends = true;
    }
    bool search(string word) { return dfs(word, 0, root); }
private:
    bool dfs(const string& w, int pos, Node* cur) {
        if (!cur) return false;
        if (pos == (int)w.size()) return cur->ends;
        if (w[pos] == '.') {
            for (int i = 0; i < 26; i++)             // try every child
                if (dfs(w, pos + 1, cur->kids[i])) return true;
            return false;
        }
        return dfs(w, pos + 1, cur->kids[w[pos] - 'a']);
    }
};   // O(L) plain · O(26^dots) worst case · O(total characters) space""",
            "java": r"""// Trie lookups, but a '.' branches into every child at that depth
class WordDictionary {
    class Node {
        Node[] kids = new Node[26];
        boolean ends;
    }
    private final Node root = new Node();
    public void addWord(String word) {
        Node cur = root;
        for (char c : word.toCharArray()) {
            int i = c - 'a';
            if (cur.kids[i] == null) cur.kids[i] = new Node();
            cur = cur.kids[i];
        }
        cur.ends = true;
    }
    public boolean search(String word) { return dfs(word, 0, root); }
    private boolean dfs(String w, int pos, Node cur) {
        if (cur == null) return false;
        if (pos == w.length()) return cur.ends;
        if (w.charAt(pos) == '.') {
            for (int i = 0; i < 26; i++)              // try every child
                if (dfs(w, pos + 1, cur.kids[i])) return true;
            return false;
        }
        return dfs(w, pos + 1, cur.kids[w.charAt(pos) - 'a']);
    }
}   // O(L) plain · O(26^dots) worst case · O(total characters) space""",
            "python": r"""class WordDictionary:
    def __init__(self):
        self.root = {}                     # node: char -> node, '#' marks a word

    def addWord(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node['#'] = True

    def search(self, word):
        def dfs(pos, node):
            if pos == len(word):
                return '#' in node         # the whole query was consumed
            ch = word[pos]
            if ch == '.':
                return any(dfs(pos + 1, kid) for key, kid in node.items() if key != '#')
            return ch in node and dfs(pos + 1, node[ch])
        return dfs(0, self.root)""",
        },
    },
    {
        "slug": "subdomain-visit-count",
        "title": "Subdomain Visit Count",
        "difficulty": "Medium",
        "pattern": "string parsing into a suffix table",
        "statement": "Each entry is \"count domain\". A visit to a domain also counts as a visit to every parent domain, so return every domain with its "
                     "total count (the order of the answer is not important).",
        "examples": [("cpdomains = [\"9001 discuss.leetcode.com\"]", "[\"9001 leetcode.com\",\"9001 discuss.leetcode.com\",\"9001 com\"]"),
                     ("cpdomains = [\"900 google.mail.com\", \"50 yahoo.com\", \"1 intel.mail.com\", \"5 wiki.org\"]",
                      "[\"901 mail.com\",\"50 yahoo.com\",\"900 google.mail.com\",\"5 wiki.org\",\"5 org\",\"1 intel.mail.com\",\"951 com\"]")],
        "constraints": ["1 <= cpdomain.length <= 100", "1 <= count <= 10^4", "domains have 1 to 3 labels of lowercase letters"],
        "approach": "Split the entry into count and domain, then add that count to every suffix of the label list — the full domain, each parent and the "
                     "top-level label. A hash table keyed by the joined suffix keeps the whole pass linear in the number of labels.",
        "complexity": ("O(total labels) time", "O(number of distinct domains)"),
        "code": {
            "cpp": r"""// Add each visit to the domain and to every parent domain
vector<string> subdomainVisits(vector<string>& cpdomains) {
    unordered_map<string,int> total;
    for (const string& entry : cpdomains) {
        int space = entry.find(' ');
        int count = stoi(entry.substr(0, space));
        string domain = entry.substr(space + 1);
        for (size_t i = 0; i <= domain.size(); i++) {
            if (i == 0 || domain[i-1] == '.')          // every suffix start
                total[domain.substr(i)] += count;
        }
    }
    vector<string> out;
    for (auto& [d, c] : total) out.push_back(to_string(c) + " " + d);
    return out;
}   // O(total labels) time · O(distinct domains) space""",
            "java": r"""// Add each visit to the domain and to every parent domain
List<String> subdomainVisits(String[] cpdomains) {
    Map<String, Integer> total = new HashMap<>();
    for (String entry : cpdomains) {
        String[] parts = entry.split(" ");
        int count = Integer.parseInt(parts[0]);
        String domain = parts[1];
        for (int i = 0; i < domain.length(); i++) {
            if (i == 0 || domain.charAt(i - 1) == '.')      // every suffix start
                total.merge(domain.substring(i), count, Integer::sum);
        }
    }
    List<String> out = new ArrayList<>();
    for (Map.Entry<String, Integer> e : total.entrySet())
        out.add(e.getValue() + " " + e.getKey());
    return out;
}   // O(total labels) time · O(distinct domains) space""",
            "python": r"""from collections import defaultdict

def subdomain_visits(cpdomains):
    total = defaultdict(int)
    for entry in cpdomains:
        count, domain = entry.split()
        count = int(count)
        labels = domain.split('.')
        for i in range(len(labels)):
            total['.'.join(labels[i:])] += count   # the domain and every parent
    return [f'{c} {d}' for d, c in total.items()]  # the order is not important""",
        },
    },
    {
        "slug": "string-to-integer-atoi",
        "title": "String to Integer (atoi)",
        "difficulty": "Medium",
        "pattern": "parsing state machine with clamping",
        "statement": "Convert s to a 32-bit signed integer the way the C library does: skip leading spaces, read one optional sign, take the following "
                     "digits, stop at the first non-digit, and clamp to [-2^31, 2^31 - 1] when the value overflows.",
        "examples": [("s = \"42\"", "42"), ("s = \" -042\"", "-42"), ("s = \"1337c0d3\"", "1337"), ("s = \"0-1\"", "0")],
        "constraints": ["0 <= s.length <= 200", "s contains letters, digits, spaces, '+', '-' and '.'"],
        "approach": "Three phases in one pass: skip spaces, consume at most one sign, then read digits into a running value while clamping as soon as it "
                     "passes the 32-bit range. Clamping during the loop (not after) is what keeps a 200-digit input from overflowing the accumulator.",
        "complexity": ("O(n) time", "O(1)"),
        "code": {
            "cpp": r"""// Skip spaces, read one sign, read digits, clamp as soon as possible
int myAtoi(string s) {
    int i = 0, n = s.size();
    while (i < n && s[i] == ' ') i++;
    int sign = 1;
    if (i < n && (s[i] == '+' || s[i] == '-')) {
        if (s[i] == '-') sign = -1;
        i++;
    }
    long long value = 0;
    while (i < n && isdigit((unsigned char)s[i])) {
        value = value * 10 + (s[i] - '0');
        i++;
        if (value > (long long)INT_MAX + 1) break;   // no need to keep reading
    }
    value *= sign;
    if (value > INT_MAX) return INT_MAX;
    if (value < INT_MIN) return INT_MIN;
    return (int)value;
}   // O(n) time · O(1) space""",
            "java": r"""// Skip spaces, read one sign, read digits, clamp as soon as possible
int myAtoi(String s) {
    int i = 0, n = s.length();
    while (i < n && s.charAt(i) == ' ') i++;
    int sign = 1;
    if (i < n && (s.charAt(i) == '+' || s.charAt(i) == '-')) {
        if (s.charAt(i) == '-') sign = -1;
        i++;
    }
    long value = 0;
    while (i < n && Character.isDigit(s.charAt(i))) {
        value = value * 10 + (s.charAt(i) - '0');
        i++;
        if (value > (long) Integer.MAX_VALUE + 1) break;   // no need to read on
    }
    value *= sign;
    if (value > Integer.MAX_VALUE) return Integer.MAX_VALUE;
    if (value < Integer.MIN_VALUE) return Integer.MIN_VALUE;
    return (int) value;
}   // O(n) time · O(1) space""",
            "python": r"""def my_atoi(s):
    i, n = 0, len(s)
    while i < n and s[i] == ' ':
        i += 1                              # phase 1: leading spaces
    sign = 1
    if i < n and s[i] in '+-':
        sign = -1 if s[i] == '-' else 1     # phase 2: at most one sign
        i += 1
    value = 0
    while i < n and '0' <= s[i] <= '9':
        value = value * 10 + (ord(s[i]) - 48)     # phase 3: the digits
        i += 1
        if value > 2**31:                   # already past any legal result
            break
    value *= sign
    return max(-2**31, min(2**31 - 1, value))     # clamp to 32 bits""",
        },
    },
    {
        "slug": "find-all-anagrams-in-a-string",
        "title": "Find All Anagrams in a String",
        "difficulty": "Medium",
        "pattern": "fixed-size window with counting",
        "statement": "Return the starting indices of every substring of s that is an anagram of p.",
        "examples": [("s = \"cbaebabacd\", p = \"abc\"", "[0,6]"), ("s = \"abab\", p = \"ab\"", "[0,1,2]")],
        "constraints": ["1 <= s.length, p.length <= 3 · 10^4", "s and p consist of lowercase letters"],
        "approach": "Every anagram has the same length, so the window is fixed at len(p). Slide it one step at a time, adding the entering character and "
                     "removing the leaving one, and compare 26 counters — equal counters mean an anagram.",
        "complexity": ("O(n) time (O(26) per comparison is constant)", "O(1)"),
        "code": {
            "cpp": r"""// Fixed-size window; equal 26-counter tables mean an anagram
vector<int> findAnagrams(string s, string p) {
    vector<int> out;
    int n = s.size(), m = p.size();
    if (m > n) return out;
    vector<int> need(26, 0), window(26, 0);
    for (char c : p) need[c - 'a']++;
    for (int i = 0; i < m; i++) window[s[i] - 'a']++;
    if (window == need) out.push_back(0);
    for (int i = m; i < n; i++) {
        window[s[i] - 'a']++;                     // the character entering
        window[s[i - m] - 'a']--;                 // the character leaving
        if (window == need) out.push_back(i - m + 1);
    }
    return out;
}   // O(n) time · O(1) space""",
            "java": r"""// Fixed-size window; equal 26-counter tables mean an anagram
List<Integer> findAnagrams(String s, String p) {
    List<Integer> out = new ArrayList<>();
    int n = s.length(), m = p.length();
    if (m > n) return out;
    int[] need = new int[26], window = new int[26];
    for (char c : p.toCharArray()) need[c - 'a']++;
    for (int i = 0; i < m; i++) window[s.charAt(i) - 'a']++;
    if (Arrays.equals(window, need)) out.add(0);
    for (int i = m; i < n; i++) {
        window[s.charAt(i) - 'a']++;              // the character entering
        window[s.charAt(i - m) - 'a']--;          // the character leaving
        if (Arrays.equals(window, need)) out.add(i - m + 1);
    }
    return out;
}   // O(n) time · O(1) space""",
            "python": r"""from collections import Counter

def find_anagrams(s, p):
    n, m = len(s), len(p)
    if m > n:
        return []
    need = Counter(p)
    window = Counter(s[:m])          # the first window
    out = [0] if window == need else []
    for i in range(m, n):
        window[s[i]] += 1            # the character entering
        window[s[i - m]] -= 1        # the character leaving
        if window[s[i - m]] == 0:
            del window[s[i - m]]     # keep the comparison cheap
        if window == need:
            out.append(i - m + 1)
    return out""",
        },
    },
    {
        "slug": "making-file-names-unique",
        "title": "Making File Names Unique",
        "difficulty": "Medium",
        "pattern": "name reservation with a next-suffix table",
        "statement": "Assign folder names in order: if a requested name is free it is used as it is, otherwise the smallest k >= 1 with name(k) unused "
                     "is taken. Return the assigned names.",
        "examples": [("names = [\"pes\",\"fifa\",\"gta\",\"pes(2019)\"]", "[\"pes\",\"fifa\",\"gta\",\"pes(2019)\"]"),
                     ("names = [\"gta\",\"gta(1)\",\"gta\",\"avalon\"]", "[\"gta\",\"gta(1)\",\"gta(2)\",\"avalon\"]"),
                     ("names = [\"onepiece\",\"onepiece(1)\",\"onepiece(2)\",\"onepiece(3)\",\"onepiece\"]",
                      "[\"onepiece\",\"onepiece(1)\",\"onepiece(2)\",\"onepiece(3)\",\"onepiece(4)\"]")],
        "constraints": ["1 <= names.length <= 5 · 10^4", "1 <= names[i].length <= 30", "names consist of lowercase letters, digits and parentheses"],
        "approach": "Keep the set of names already taken, plus a per-name counter remembering the next k worth trying. When a name collides, start from "
                     "that counter and step forward — the counter never rewinds, so repeated collisions cost constant time on average instead of "
                     "restarting at 1 every time.",
        "complexity": ("O(total characters) expected", "O(n)"),
        "code": {
            "cpp": r"""// A taken-set plus a per-name counter: never restart the search at 1
vector<string> getFolderNames(vector<string>& names) {
    unordered_set<string> taken;
    unordered_map<string,int> nextK;             // base name -> next k to try
    vector<string> out;
    for (const string& name : names) {
        if (!taken.count(name)) {
            out.push_back(name);
            taken.insert(name);
            continue;
        }
        int k = nextK.count(name) ? nextK[name] : 1;
        string candidate;
        do {
            candidate = name + "(" + to_string(k) + ")";
            k++;
        } while (taken.count(candidate));
        nextK[name] = k;                         // remember where to resume
        taken.insert(candidate);
        out.push_back(candidate);
    }
    return out;
}   // O(total characters) expected · O(n) space""",
            "java": r"""// A taken-set plus a per-name counter: never restart the search at 1
String[] getFolderNames(String[] names) {
    Set<String> taken = new HashSet<>();
    Map<String, Integer> nextK = new HashMap<>();     // base name -> next k
    String[] out = new String[names.length];
    for (int i = 0; i < names.length; i++) {
        String name = names[i];
        if (!taken.contains(name)) {
            out[i] = name;
            taken.add(name);
            continue;
        }
        int k = nextK.getOrDefault(name, 1);
        String candidate;
        do {
            candidate = name + "(" + k + ")";
            k++;
        } while (taken.contains(candidate));
        nextK.put(name, k);                          // remember where to resume
        taken.add(candidate);
        out[i] = candidate;
    }
    return out;
}   // O(total characters) expected · O(n) space""",
            "python": r"""def get_folder_names(names):
    taken = set()
    next_k = {}                       # base name -> next k worth trying
    out = []
    for name in names:
        if name not in taken:
            out.append(name)
            taken.add(name)
            continue
        k = next_k.get(name, 1)
        while f'{name}({k})' in taken:
            k += 1                    # resume from the remembered counter
        candidate = f'{name}({k})'
        next_k[name] = k + 1          # next time start one further
        taken.add(candidate)
        out.append(candidate)
    return out""",
        },
    },
    {
        "slug": "lexicographical-numbers",
        "title": "Lexicographical Numbers",
        "difficulty": "Medium",
        "pattern": "pre-order walk of a digit tree",
        "statement": "Return the numbers from 1 to n in lexicographical order, in O(n) time.",
        "examples": [("n = 13", "[1,10,11,12,13,2,3,4,5,6,7,8,9]"), ("n = 2", "[1,2]")],
        "constraints": ["1 <= n <= 5 · 10^4", "the answer must be produced in O(n) time and O(1) extra space beyond the output"],
        "approach": "Think of the numbers as a tree where 1..9 are the roots and a node x has children 10x .. 10x+9. Lexicographic order is exactly a "
                     "pre-order walk of that tree, so descend while a child is <= n and jump to the next sibling otherwise — no sorting at all.",
        "complexity": ("O(n) time", "O(1) beyond the output"),
        "code": {
            "cpp": r"""// Pre-order walk of the tree 1..9 with children 10x .. 10x+9
vector<int> lexicalOrder(int n) {
    vector<int> out;
    out.reserve(n);
    int cur = 1;
    for (int i = 0; i < n; i++) {
        out.push_back(cur);
        if (cur * 10 <= n) cur *= 10;            // descend to the first child
        else {
            while (cur % 10 == 9 || cur + 1 > n) cur /= 10;   // climb back
            cur++;
        }
    }
    return out;
}   // O(n) time · O(1) space beyond the output""",
            "java": r"""// Pre-order walk of the tree 1..9 with children 10x .. 10x+9
List<Integer> lexicalOrder(int n) {
    List<Integer> out = new ArrayList<>(n);
    int cur = 1;
    for (int i = 0; i < n; i++) {
        out.add(cur);
        if (cur * 10 <= n) cur *= 10;            // descend to the first child
        else {
            while (cur % 10 == 9 || cur + 1 > n) cur /= 10;   // climb back
            cur++;
        }
    }
    return out;
}   // O(n) time · O(1) space beyond the output""",
            "python": r"""def lexical_order(n):
    out = []
    cur = 1
    for _ in range(n):
        out.append(cur)
        if cur * 10 <= n:
            cur *= 10                  # descend to the first child
        else:
            while cur % 10 == 9 or cur + 1 > n:
                cur //= 10             # climb until a sibling is available
            cur += 1
    return out""",
        },
    },
    {
        "slug": "number-of-matching-subsequences",
        "title": "Number of Matching Subsequences",
        "difficulty": "Medium",
        "pattern": "next-occurrence lists with binary search",
        "statement": "Given s and a list of words, count how many of the words are subsequences of s.",
        "examples": [("s = \"abcde\", words = [\"a\",\"bb\",\"acd\",\"ace\"]", "3"),
                     ("s = \"dsahjpjauf\", words = [\"ahjpjau\",\"ja\",\"ahbwzgqnuk\",\"tnmlanowax\"]", "2")],
        "constraints": ["1 <= s.length <= 5 · 10^4", "1 <= words.length <= 5000", "1 <= words[i].length <= 50", "s and words contain lowercase letters"],
        "approach": "Precompute the sorted positions of each letter in s. Matching a word is then a chain of binary searches: from the current position, "
                     "ask where the needed letter appears next. Each word costs its own length in logarithms instead of a fresh scan of s.",
        "complexity": ("O(|s| + total word length · log |s|)", "O(|s|)"),
        "code": {
            "cpp": r"""// Sorted positions per letter; each word is a chain of binary searches
int numMatchingSubseq(string s, vector<string>& words) {
    vector<vector<int>> pos(26);
    for (int i = 0; i < (int)s.size(); i++) pos[s[i] - 'a'].push_back(i);
    int count = 0;
    for (const string& w : words) {
        int at = -1;
        bool ok = true;
        for (char c : w) {
            const vector<int>& list = pos[c - 'a'];
            auto it = upper_bound(list.begin(), list.end(), at);   // next occurrence
            if (it == list.end()) { ok = false; break; }
            at = *it;
        }
        if (ok) count++;
    }
    return count;
}   // O(|s| + total word length · log |s|) time · O(|s|) space""",
            "java": r"""// Sorted positions per letter; each word is a chain of binary searches
int numMatchingSubseq(String s, String[] words) {
    List<List<Integer>> pos = new ArrayList<>();
    for (int c = 0; c < 26; c++) pos.add(new ArrayList<>());
    for (int i = 0; i < s.length(); i++) pos.get(s.charAt(i) - 'a').add(i);
    int count = 0;
    for (String w : words) {
        int at = -1;
        boolean ok = true;
        for (char c : w.toCharArray()) {
            List<Integer> list = pos.get(c - 'a');
            int lo = 0, hi = list.size();                  // first index above at
            while (lo < hi) {
                int mid = (lo + hi) / 2;
                if (list.get(mid) <= at) lo = mid + 1; else hi = mid;
            }
            if (lo == list.size()) { ok = false; break; }
            at = list.get(lo);
        }
        if (ok) count++;
    }
    return count;
}   // O(|s| + total word length · log |s|) time · O(|s|) space""",
            "python": r"""from bisect import bisect_right

def num_matching_subseq(s, words):
    positions = {}
    for i, ch in enumerate(s):
        positions.setdefault(ch, []).append(i)     # sorted positions per letter
    count = 0
    for w in words:
        at = -1
        ok = True
        for ch in w:
            lst = positions.get(ch)
            if not lst:
                ok = False
                break
            j = bisect_right(lst, at)              # next occurrence after 'at'
            if j == len(lst):
                ok = False
                break
            at = lst[j]
        if ok:
            count += 1
    return count""",
        },
    },
    {
        "slug": "stream-of-characters",
        "title": "Stream of Characters",
        "difficulty": "Hard",
        "pattern": "trie of reversed words over a sliding buffer",
        "statement": "Words are given up front, then characters arrive one at a time. After each character, report whether any word is a suffix of the "
                     "characters seen so far.",
        "examples": [("[\"StreamChecker\",\"query\",\"query\",\"query\",\"query\",\"query\",\"query\",\"query\",\"query\",\"query\",\"query\",\"query\",\"query\"] [[[\"cd\",\"f\",\"kl\"]],[\"a\"],[\"b\"],[\"c\"],[\"d\"],[\"e\"],[\"f\"],[\"g\"],[\"h\"],[\"i\"],[\"j\"],[\"k\"],[\"l\"]]",
                      "[null, false, false, false, true, false, true, false, false, false, false, false, true]")],
        "constraints": ["1 <= words.length <= 2000", "1 <= words[i].length <= 2000", "1 <= query letters <= 4 · 10^4", "words and queries are lowercase letters"],
        "approach": "A suffix question is a prefix question read backwards, so store every word reversed in a trie. Keep a buffer of the last "
                     "longest-word characters and, after each new letter, walk the buffer backwards through the trie: reaching a word end means some "
                     "word ends exactly here. The buffer cap is what keeps the per-query walk bounded.",
        "complexity": ("O(longest word) per query", "O(total word characters + longest word)"),
        "code": {
            "cpp": r"""// Words stored backwards; each query walks the recent buffer backwards
class StreamChecker {
    struct Node {
        unordered_map<char, Node*> kids;
        bool ends = false;
    };
    Node* root = new Node();
    deque<char> buffer;
    int longest = 0;
public:
    StreamChecker(vector<string>& words) {
        for (const string& w : words) {
            longest = max(longest, (int)w.size());
            Node* cur = root;
            for (auto it = w.rbegin(); it != w.rend(); ++it) {   // store reversed
                char c = *it;
                if (!cur->kids[c]) cur->kids[c] = new Node();
                cur = cur->kids[c];
            }
            cur->ends = true;
        }
    }
    bool query(char letter) {
        buffer.push_back(letter);
        if ((int)buffer.size() > longest) buffer.pop_front();    // keep it short
        Node* cur = root;
        for (auto it = buffer.rbegin(); it != buffer.rend(); ++it) {
            auto found = cur->kids.find(*it);
            if (found == cur->kids.end()) return false;
            cur = found->second;
            if (cur->ends) return true;                 // a word ends exactly here
        }
        return false;
    }
};   // O(longest word) per query · O(total word characters) space""",
            "java": r"""// Words stored backwards; each query walks the recent buffer backwards
class StreamChecker {
    class Node {
        Map<Character, Node> kids = new HashMap<>();
        boolean ends;
    }
    private final Node root = new Node();
    private final Deque<Character> buffer = new ArrayDeque<>();
    private int longest = 0;
    public StreamChecker(String[] words) {
        for (String w : words) {
            longest = Math.max(longest, w.length());
            Node cur = root;
            for (int i = w.length() - 1; i >= 0; i--) {     // store reversed
                cur = cur.kids.computeIfAbsent(w.charAt(i), k -> new Node());
            }
            cur.ends = true;
        }
    }
    public boolean query(char letter) {
        buffer.addLast(letter);
        if (buffer.size() > longest) buffer.removeFirst();   // keep it short
        Node cur = root;
        Iterator<Character> it = buffer.descendingIterator();
        while (it.hasNext()) {
            cur = cur.kids.get(it.next());
            if (cur == null) return false;
            if (cur.ends) return true;                  // a word ends exactly here
        }
        return false;
    }
}   // O(longest word) per query · O(total word characters) space""",
            "python": r"""class StreamChecker:
    def __init__(self, words):
        self.root = {}
        for w in words:
            node = self.root
            for ch in reversed(w):             # store every word backwards
                node = node.setdefault(ch, {})
            node['#'] = True                   # a word ends here
        self.buffer = []                       # the recent characters
        self.longest = max(len(w) for w in words)

    def query(self, letter):
        self.buffer.append(letter)
        if len(self.buffer) > self.longest:
            self.buffer.pop(0)                 # nothing older can matter
        node = self.root
        for ch in reversed(self.buffer):       # walk the stream backwards
            if ch not in node:
                return False
            node = node[ch]
            if '#' in node:
                return True                    # a word ends exactly here
        return False""",
        },
    },
    {
        "slug": "prefix-and-suffix-search",
        "title": "Prefix and Suffix Search",
        "difficulty": "Hard",
        "pattern": "trie over (suffix, separator, word) keys",
        "statement": "Build a filter over a list of words whose f(prefix, suffix) returns the largest index of a word starting with prefix and ending "
                     "with suffix, or -1.",
        "examples": [("[\"WordFilter\",\"f\"] [[[\"apple\"]],[\"a\",\"e\"]]", "[null, 0]")],
        "constraints": ["1 <= words.length <= 1.5 · 10^4", "1 <= words[i].length <= 10", "1 <= prefix.length, suffix.length <= 10", "at most 1.5 · 10^4 queries"],
        "approach": "One query mixes a prefix and a suffix, so glue them into a single key. For every word, insert `word[j:] + '{' + word` for all j: a "
                     "query `suffix + '{' + prefix` then finds a key only when the suffix really is one of the word's suffixes and the prefix really "
                     "starts the word. A trie of those keys, each node remembering the largest index below it, answers in one walk.",
        "complexity": ("O(total |word|²) build, O(|prefix| + |suffix|) per query", "O(total |word|²)"),
        "code": {
            "cpp": r"""// Keys word[j:] + '{' + word; query suffix + '{' + prefix, keep max index
class WordFilter {
    struct Node {
        unordered_map<char, Node*> kids;
        int best = -1;                            // largest index in this subtree
    };
    Node* root = new Node();
    void add(const string& key, int idx) {
        Node* cur = root;
        cur->best = max(cur->best, idx);
        for (char c : key) {
            if (!cur->kids[c]) cur->kids[c] = new Node();
            cur = cur->kids[c];
            cur->best = max(cur->best, idx);
        }
    }
public:
    WordFilter(vector<string>& words) {
        for (int i = 0; i < (int)words.size(); i++)
            for (size_t j = 0; j <= words[i].size(); j++)   // every suffix
                add(words[i].substr(j) + "{" + words[i], i);
    }
    int f(string prefix, string suffix) {
        Node* cur = root;
        for (char c : suffix + "{" + prefix) {              // one walk
            auto found = cur->kids.find(c);
            if (found == cur->kids.end()) return -1;
            cur = found->second;
        }
        return cur->best;
    }
};   // O(total |word|^2) build · O(|prefix| + |suffix|) per query""",
            "java": r"""// Keys word[j:] + '{' + word; query suffix + '{' + prefix, keep max index
class WordFilter {
    class Node {
        Map<Character, Node> kids = new HashMap<>();
        int best = -1;                            // largest index in this subtree
    }
    private final Node root = new Node();
    private void add(String key, int idx) {
        Node cur = root;
        cur.best = Math.max(cur.best, idx);
        for (char c : key.toCharArray()) {
            cur = cur.kids.computeIfAbsent(c, k -> new Node());
            cur.best = Math.max(cur.best, idx);
        }
    }
    public WordFilter(String[] words) {
        for (int i = 0; i < words.length; i++)
            for (int j = 0; j <= words[i].length(); j++)     // every suffix
                add(words[i].substring(j) + "{" + words[i], i);
    }
    public int f(String prefix, String suffix) {
        Node cur = root;
        for (char c : (suffix + "{" + prefix).toCharArray()) {   // one walk
            cur = cur.kids.get(c);
            if (cur == null) return -1;
        }
        return cur.best;
    }
}   // O(total |word|^2) build · O(|prefix| + |suffix|) per query""",
            "python": r"""class WordFilter:
    def __init__(self, words):
        self.root = {}
        for idx, w in enumerate(words):
            for j in range(len(w) + 1):            # every suffix of w
                key = w[j:] + '{' + w              # suffix, separator, the word
                node = self.root
                node['#best'] = max(node.get('#best', -1), idx)
                for ch in key:
                    node = node.setdefault(ch, {})
                    node['#best'] = max(node.get('#best', -1), idx)

    def f(self, prefix, suffix):
        node = self.root
        for ch in suffix + '{' + prefix:           # one walk finds the answer
            if ch not in node:
                return -1
            node = node[ch]
        return node.get('#best', -1)""",
        },
    },
    {
        "slug": "word-search-ii",
        "title": "Word Search II",
        "difficulty": "Hard",
        "pattern": "trie plus board DFS",
        "statement": "Given a board of letters and a list of words, return all words that can be traced through horizontally or vertically adjacent cells, "
                     "using each cell at most once per word (the order of the answer does not matter).",
        "examples": [("board = [[\"o\",\"a\",\"a\",\"n\"],[\"e\",\"t\",\"a\",\"e\"],[\"i\",\"h\",\"k\",\"r\"],[\"i\",\"f\",\"l\",\"v\"]], words = [\"oath\",\"pea\",\"eat\",\"rain\"]",
                      "[\"eat\",\"oath\"]"),
                     ("board = [[\"a\",\"b\"],[\"c\",\"d\"]], words = [\"abcb\"]", "[]")],
        "constraints": ["1 <= rows, cols <= 12", "1 <= words.length <= 3 · 10^4", "1 <= word length <= 10", "words are lowercase letters and distinct"],
        "approach": "Put the words in a trie and start a depth-first walk from every cell. The trie prunes as soon as the current path stops being a "
                     "prefix of some word, so the board is never rescanned per word. Clearing a word's end marker when it is found keeps the duplicate "
                     "work away, and temporarily blanking visited cells is the visited set.",
        "complexity": ("O(rows · cols · 4^maxWordLength)", "O(total word characters)"),
        "code": {
            "cpp": r"""// Trie of the words; DFS from every cell, pruned by the trie
vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
    struct TNode { unordered_map<char,int> kids; string word; };
    vector<TNode> trie(1);
    for (const string& w : words) {
        int cur = 0;
        for (char c : w) {
            auto found = trie[cur].kids.find(c);
            if (found == trie[cur].kids.end()) {
                trie.push_back(TNode());
                trie[cur].kids[c] = (int)trie.size() - 1;
                cur = (int)trie.size() - 1;
            } else cur = found->second;
        }
        trie[cur].word = w;                       // the word ends at this node
    }
    int R = board.size(), C = board[0].size();
    vector<string> found;
    function<void(int,int,int)> dfs = [&](int r, int c, int node) {
        auto foundIt = trie[node].kids.find(board[r][c]);
        if (foundIt == trie[node].kids.end()) return;        // not a prefix
        int nxt = foundIt->second;
        if (!trie[nxt].word.empty()) {
            found.push_back(trie[nxt].word);
            trie[nxt].word.clear();                          // report it once
        }
        char saved = board[r][c];
        board[r][c] = '#';                                   // mark visited
        int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr >= 0 && nr < R && nc >= 0 && nc < C && board[nr][nc] != '#')
                dfs(nr, nc, nxt);
        }
        board[r][c] = saved;                                 // restore for other paths
    };
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            dfs(r, c, 0);
    return found;
}   // O(R·C·4^L) time · O(total word characters) space""",
            "java": r"""// Trie of the words; DFS from every cell, pruned by the trie
List<String> findWords(char[][] board, String[] words) {
    List<Map<Character, Integer>> kids = new ArrayList<>();
    List<String> ends = new ArrayList<>();
    kids.add(new HashMap<>());
    ends.add(null);
    for (String w : words) {                       // build the trie
        int cur = 0;
        for (char c : w.toCharArray()) {
            Integer nxt = kids.get(cur).get(c);
            if (nxt == null) {
                kids.add(new HashMap<>());
                ends.add(null);
                nxt = kids.size() - 1;
                kids.get(cur).put(c, nxt);
            }
            cur = nxt;
        }
        ends.set(cur, w);
    }
    List<String> found = new ArrayList<>();
    for (int r = 0; r < board.length; r++)
        for (int c = 0; c < board[0].length; c++)
            dfs(board, r, c, 0, kids, ends, found);
    return found;
}
void dfs(char[][] board, int r, int c, int node,
         List<Map<Character, Integer>> kids, List<String> ends, List<String> found) {
    Integer nxt = kids.get(node).get(board[r][c]);
    if (nxt == null) return;                       // not a prefix of any word
    if (ends.get(nxt) != null) {
        found.add(ends.get(nxt));
        ends.set(nxt, null);                       // report it once
    }
    char saved = board[r][c];
    board[r][c] = '#';
    int[] dr = {1,-1,0,0}, dc = {0,0,1,-1};
    for (int d = 0; d < 4; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr >= 0 && nr < board.length && nc >= 0 && nc < board[0].length && board[nr][nc] != '#')
            dfs(board, nr, nc, nxt, kids, ends, found);
    }
    board[r][c] = saved;                           // restore for other paths
}   // O(R·C·4^L) time · O(total word characters) space""",
            "python": r"""def find_words(board, words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node['#'] = w                     # the word ends at this node

    R, C = len(board), len(board[0])
    found = []

    def dfs(r, c, node):
        ch = board[r][c]
        nxt = node.get(ch)
        if nxt is None:
            return                        # not a prefix of any word
        if '#' in nxt:
            found.append(nxt.pop('#'))    # report it once
        board[r][c] = ''                  # mark visited
        for nr, nc in ((r+1,c), (r-1,c), (r,c+1), (r,c-1)):
            if 0 <= nr < R and 0 <= nc < C and board[nr][nc] in nxt:
                dfs(nr, nc, nxt)
        board[r][c] = ch                  # restore for other paths

    for r in range(R):
        for c in range(C):
            dfs(r, c, root)
    return found""",
        },
    },
    {
        "slug": "concatenated-words",
        "title": "Concatenated Words",
        "difficulty": "Hard",
        "pattern": "per-word segment DP",
        "statement": "Return every word of the list that can be written as the concatenation of at least two *other* words of the list.",
        "examples": [("words = [\"cat\",\"cats\",\"catsdogcats\",\"dog\",\"dogcatsdog\",\"hippopotamuses\",\"rat\",\"ratcatdogcat\"]",
                      "[\"catsdogcats\",\"dogcatsdog\",\"ratcatdogcat\"]"),
                     ("words = [\"cat\",\"dog\",\"catdog\"]", "[\"catdog\"]")],
        "constraints": ["1 <= words.length <= 10^4", "1 <= words[i].length <= 30", "words contain lowercase letters", "words are distinct"],
        "approach": "For each word, run the word-break DP over the set of all words: dp[i] is true when the first i characters can be covered by "
                     "dictionary words. The extra condition — the whole word may not be one single piece — is exactly what forces at least two parts.",
        "complexity": ("O(n · L²) with L <= 30", "O(n · L) plus the word set"),
        "code": {
            "cpp": r"""// Word-break DP per word, with the single-piece split forbidden
vector<string> findAllConcatenatedWordsInADict(vector<string>& words) {
    unordered_set<string> dict(words.begin(), words.end());
    vector<string> out;
    for (const string& w : words) {
        int n = w.size();
        vector<bool> dp(n + 1, false);
        dp[0] = true;
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                if (!dp[j]) continue;
                if (j == 0 && i == n) continue;          // the whole word alone
                if (dict.count(w.substr(j, i - j))) { dp[i] = true; break; }
            }
        }
        if (dp[n]) out.push_back(w);
    }
    return out;
}   // O(n · L^2) time · O(n · L) space""",
            "java": r"""// Word-break DP per word, with the single-piece split forbidden
List<String> findAllConcatenatedWordsInADict(String[] words) {
    Set<String> dict = new HashSet<>(Arrays.asList(words));
    List<String> out = new ArrayList<>();
    for (String w : words) {
        int n = w.length();
        boolean[] dp = new boolean[n + 1];
        dp[0] = true;
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                if (!dp[j]) continue;
                if (j == 0 && i == n) continue;          // the whole word alone
                if (dict.contains(w.substring(j, i))) { dp[i] = true; break; }
            }
        }
        if (dp[n]) out.add(w);
    }
    return out;
}   // O(n · L^2) time · O(n · L) space""",
            "python": r"""def find_all_concatenated_words(words):
    word_set = set(words)
    out = []
    for w in words:
        n = len(w)
        dp = [False] * (n + 1)
        dp[0] = True
        for i in range(1, n + 1):
            for j in range(i):
                if not dp[j]:
                    continue
                if j == 0 and i == n:
                    continue               # the word as one single piece
                if w[j:i] in word_set:
                    dp[i] = True
                    break
        if dp[n]:
            out.append(w)
    return out""",
        },
    },
    {
        "slug": "longest-chunked-palindrome-decomposition",
        "title": "Longest Chunked Palindrome Decomposition",
        "difficulty": "Hard",
        "pattern": "two-pointer chunk matching",
        "statement": "Split text into the largest possible number of parts such that the first part equals the last, the second equals the second last, and "
                     "so on. Return that number of parts.",
        "examples": [("text = \"ghiabcdefhelloadamhelloabcdefghi\"", "7"), ("text = \"merchant\"", "1"),
                     ("text = \"antaprezatepzapreanta\"", "11")],
        "constraints": ["1 <= text.length <= 1000", "text contains lowercase letters"],
        "approach": "Greedily match the shortest possible pieces at both ends: try size 1, then 2, and so on, and take the first size where the left and "
                     "right chunks are equal. Shortest-first is optimal because any coarser split can be refined into it — matching as early as "
                     "possible can never cost a part.",
        "complexity": ("O(n²) time (O(n) chunk comparisons of total length n)", "O(1)"),
        "code": {
            "cpp": r"""// Match the shortest equal chunk at both ends, greedily
int longestDecomposition(string text) {
    int left = 0, right = text.size(), parts = 0;
    while (left < right) {
        int size = 1;
        bool matched = false;
        while (left + size <= right - size) {
            if (text.compare(left, size, text, right - size, size) == 0) {   // equal chunks
                left += size;
                right -= size;
                parts += 2;                      // one part at each end
                matched = true;
                break;
            }
            size++;
        }
        if (!matched) {                          // the middle piece stays whole
            parts += 1;
            break;
        }
    }
    return parts;
}   // O(n^2) time · O(1) space""",
            "java": r"""// Match the shortest equal chunk at both ends, greedily
int longestDecomposition(String text) {
    int left = 0, right = text.length(), parts = 0;
    while (left < right) {
        int size = 1;
        boolean matched = false;
        while (left + size <= right - size) {
            String a = text.substring(left, left + size);
            String b = text.substring(right - size, right);
            if (a.equals(b)) {
                left += size;
                right -= size;
                parts += 2;                      // one part at each end
                matched = true;
                break;
            }
            size++;
        }
        if (!matched) {                          // the middle piece stays whole
            parts += 1;
            break;
        }
    }
    return parts;
}   // O(n^2) time · O(1) space""",
            "python": r"""def longest_decomposition(text):
    left, right = 0, len(text)
    parts = 0
    while left < right:
        size = 1
        matched = False
        while left + size <= right - size:
            if text[left:left+size] == text[right-size:right]:
                left += size
                right -= size
                parts += 2                      # one part at each end
                matched = True
                break
            size += 1                           # try a longer chunk
        if not matched:                         # the middle piece stays whole
            parts += 1
            break
    return parts""",
        },
    },
    {
        "slug": "longest-happy-prefix",
        "title": "Longest Happy Prefix",
        "difficulty": "Hard",
        "pattern": "KMP prefix function",
        "statement": "Return the longest proper prefix of s that is also a suffix of s, or the empty string if there is none.",
        "examples": [("s = \"level\"", "\"l\""), ("s = \"ababab\"", "\"abab\"")],
        "constraints": ["1 <= s.length <= 10^5", "s contains lowercase letters"],
        "approach": "This is exactly what the KMP prefix function computes: pi[i] is the length of the longest proper prefix of s[:i+1] that is also a "
                     "suffix. Carrying the previous value forward and falling back along the border chain gives the answer in one linear pass.",
        "complexity": ("O(n) time", "O(n)"),
        "code": {
            "cpp": r"""// The KMP prefix function's last value is the answer
string longestPrefix(string s) {
    int n = s.size();
    vector<int> pi(n, 0);
    for (int i = 1; i < n; i++) {
        int j = pi[i-1];
        while (j > 0 && s[i] != s[j]) j = pi[j-1];   // fall back along the border
        if (s[i] == s[j]) j++;
        pi[i] = j;
    }
    return s.substr(0, pi[n-1]);
}   // O(n) time · O(n) space""",
            "java": r"""// The KMP prefix function's last value is the answer
String longestPrefix(String s) {
    int n = s.length();
    int[] pi = new int[n];
    for (int i = 1; i < n; i++) {
        int j = pi[i-1];
        while (j > 0 && s.charAt(i) != s.charAt(j)) j = pi[j-1];   // fall back
        if (s.charAt(i) == s.charAt(j)) j++;
        pi[i] = j;
    }
    return s.substring(0, pi[n-1]);
}   // O(n) time · O(n) space""",
            "python": r"""def longest_prefix(s):
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i-1]
        while j > 0 and s[i] != s[j]:
            j = pi[j-1]                 # fall back along the border chain
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return s[:pi[-1]]                   # the longest border of the whole string""",
        },
    },
    {
        "slug": "shortest-palindrome",
        "title": "Shortest Palindrome",
        "difficulty": "Hard",
        "pattern": "KMP over s + '#' + reverse(s)",
        "statement": "Add characters in front of s to make it a palindrome and return the shortest such palindrome.",
        "examples": [("s = \"aacecaaa\"", "\"aaacecaaa\""), ("s = \"abcd\"", "\"dcbabcd\"")],
        "constraints": ["0 <= s.length <= 5 · 10^4", "s contains lowercase letters"],
        "approach": "The characters to prepend are the reverse of the tail that lies *after* the longest palindromic prefix. Finding that prefix is a "
                     "border question on `s + '#' + reverse(s)`: the prefix function's final value is the length of the longest palindromic prefix, and "
                     "everything after it must be mirrored.",
        "complexity": ("O(n) time", "O(n)"),
        "code": {
            "cpp": r"""// Longest palindromic prefix via KMP on s + '#' + reverse(s)
string shortestPalindrome(string s) {
    if (s.empty()) return "";
    string rev(s.rbegin(), s.rend());
    string comb = s + "#" + rev;
    int n = comb.size();
    vector<int> pi(n, 0);
    for (int i = 1; i < n; i++) {
        int j = pi[i-1];
        while (j > 0 && comb[i] != comb[j]) j = pi[j-1];
        if (comb[i] == comb[j]) j++;
        pi[i] = j;
    }
    int palindromePrefix = pi[n-1];              // length of the palindromic prefix
    return rev.substr(0, s.size() - palindromePrefix) + s;
}   // O(n) time · O(n) space""",
            "java": r"""// Longest palindromic prefix via KMP on s + '#' + reverse(s)
String shortestPalindrome(String s) {
    if (s.isEmpty()) return "";
    String rev = new StringBuilder(s).reverse().toString();
    String comb = s + "#" + rev;
    int n = comb.length();
    int[] pi = new int[n];
    for (int i = 1; i < n; i++) {
        int j = pi[i-1];
        while (j > 0 && comb.charAt(i) != comb.charAt(j)) j = pi[j-1];
        if (comb.charAt(i) == comb.charAt(j)) j++;
        pi[i] = j;
    }
    int palindromePrefix = pi[n-1];              // the palindromic prefix length
    return rev.substring(0, s.length() - palindromePrefix) + s;
}   // O(n) time · O(n) space""",
            "python": r"""def shortest_palindrome(s):
    if not s:
        return ''
    rev = s[::-1]
    comb = s + '#' + rev               # a separator no character can match
    pi = [0] * len(comb)
    for i in range(1, len(comb)):
        j = pi[i-1]
        while j > 0 and comb[i] != comb[j]:
            j = pi[j-1]
        if comb[i] == comb[j]:
            j += 1
        pi[i] = j
    good = pi[-1]                      # longest palindromic prefix of s
    return rev[:len(s) - good] + s     # mirror everything after it""",
        },
    },
    {
        "slug": "count-unique-characters-of-all-substrings-of-a-given-string",
        "title": "Count Unique Characters of All Substrings of a Given String",
        "difficulty": "Hard",
        "pattern": "contribution of each character",
        "statement": "For every substring, count the characters that appear exactly once in it. Return the sum of those counts over all substrings, "
                     "modulo 10^9 + 7.",
        "examples": [("s = \"ABC\"", "10"), ("s = \"ABA\"", "8"), ("s = \"LEETCODE\"", "92")],
        "constraints": ["1 <= s.length <= 10^5", "s contains uppercase English letters"],
        "approach": "Stop enumerating substrings and let each character count where it is unique. A character at position i is unique exactly for the "
                     "substrings that start after the previous equal character and end before the next equal one, so it contributes "
                     "(i - prev) · (next - i) directly — one linear pass after computing the next occurrences.",
        "complexity": ("O(n) time", "O(n)"),
        "code": {
            "cpp": r"""// Each character contributes (i - prev) * (next - i) substrings
int uniqueLetterString(string s) {
    const int MOD = 1e9 + 7;
    int n = s.size();
    vector<int> nxt(n, n), lastPos(26, n);
    for (int i = n - 1; i >= 0; i--) {
        nxt[i] = lastPos[s[i] - 'A'];            // next occurrence of the same letter
        lastPos[s[i] - 'A'] = i;
    }
    vector<int> prevPos(26, -1);
    long long total = 0;
    for (int i = 0; i < n; i++) {
        int prev = prevPos[s[i] - 'A'];
        prevPos[s[i] - 'A'] = i;
        total = (total + (long long)(i - prev) * (nxt[i] - i)) % MOD;
    }
    return (int) total;
}   // O(n) time · O(n) space""",
            "java": r"""// Each character contributes (i - prev) * (next - i) substrings
int uniqueLetterString(String s) {
    final int MOD = 1_000_000_007;
    int n = s.length();
    int[] nxt = new int[n], lastPos = new int[26];
    Arrays.fill(lastPos, n);
    for (int i = n - 1; i >= 0; i--) {
        nxt[i] = lastPos[s.charAt(i) - 'A'];      // next occurrence of the letter
        lastPos[s.charAt(i) - 'A'] = i;
    }
    int[] prevPos = new int[26];
    Arrays.fill(prevPos, -1);
    long total = 0;
    for (int i = 0; i < n; i++) {
        int prev = prevPos[s.charAt(i) - 'A'];
        prevPos[s.charAt(i) - 'A'] = i;
        total = (total + (long)(i - prev) * (nxt[i] - i)) % MOD;
    }
    return (int) total;
}   // O(n) time · O(n) space""",
            "python": r"""def unique_letter_string(s):
    MOD = 10**9 + 7
    n = len(s)
    nxt = [n] * n                            # next occurrence of the same letter
    last = {}
    for i in range(n - 1, -1, -1):
        nxt[i] = last.get(s[i], n)
        last[s[i]] = i
    prev = {}
    total = 0
    for i, ch in enumerate(s):
        p = prev.get(ch, -1)
        prev[ch] = i
        total += (i - p) * (nxt[i] - i)       # substrings where this ch is unique
    return total % MOD""",
        },
    },
    {
        "slug": "distinct-echo-substrings",
        "title": "Distinct Echo Substrings",
        "difficulty": "Hard",
        "pattern": "rolling hash over (a, a)",
        "statement": "An echo substring is a substring of the form a + a. Count how many *distinct* echo substrings text contains.",
        "examples": [("text = \"abcabcabc\"", "3"), ("text = \"leetcodeleetcode\"", "2")],
        "constraints": ["1 <= text.length <= 2000", "text contains lowercase letters"],
        "approach": "Every echo is fixed by its start and its half-length, so scan the possible middles and compare the two halves with a rolling hash. "
                     "Storing `(half-length, hash)` in a set counts each distinct echo once even when it occurs many times — hashing the content is what "
                     "turns \"distinct\" from a string comparison into a lookup.",
        "complexity": ("O(n²) time", "O(n²) worst case for the distinct set"),
        "code": {
            "cpp": r"""// Compare the two halves with rolling hashes; a set of hashes counts distinct
int distinctEchoSubstrings(string text) {
    const long long M1 = 1000000007, M2 = 1000000009, B1 = 131, B2 = 137;
    int n = text.size();
    vector<long long> h1(n+1,0), h2(n+1,0), p1(n+1,1), p2(n+1,1);
    for (int i = 0; i < n; i++) {
        long long v = text[i];
        h1[i+1] = (h1[i] * B1 + v) % M1;
        h2[i+1] = (h2[i] * B2 + v) % M2;
        p1[i+1] = p1[i] * B1 % M1;
        p2[i+1] = p2[i] * B2 % M2;
    }
    auto hashOf = [&](int l, int r) {            // hash of text[l, r)
        long long a = ((h1[r] - h1[l] * p1[r-l]) % M1 + M1) % M1;
        long long b = ((h2[r] - h2[l] * p2[r-l]) % M2 + M2) % M2;
        return a * M2 + b;                       // both moduli in one key
    };
    unordered_set<long long> seen;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j + (j - i) <= n; j++) {
            int k = j + (j - i);                 // the end of the second half
            if (hashOf(i, j) == hashOf(j, k))
                seen.insert((long long)(j - i) * (M1 * M2) + hashOf(i, j));
        }
    }
    return seen.size();
}   // O(n^2) time · O(distinct echoes) space""",
            "java": r"""// Compare the two halves with rolling hashes; a set of hashes counts distinct
int distinctEchoSubstrings(String text) {
    final long M1 = 1000000007L, M2 = 1000000009L, B1 = 131, B2 = 137;
    int n = text.length();
    long[] h1 = new long[n+1], h2 = new long[n+1], p1 = new long[n+1], p2 = new long[n+1];
    p1[0] = p2[0] = 1;
    for (int i = 0; i < n; i++) {
        long v = text.charAt(i);
        h1[i+1] = (h1[i] * B1 + v) % M1;
        h2[i+1] = (h2[i] * B2 + v) % M2;
        p1[i+1] = p1[i] * B1 % M1;
        p2[i+1] = p2[i] * B2 % M2;
    }
    Set<Long> seen = new HashSet<>();
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j + (j - i) <= n; j++) {
            int k = j + (j - i);                 // the end of the second half
            long a1 = ((h1[j] - h1[i] * p1[j-i]) % M1 + M1) % M1;
            long b1 = ((h2[j] - h2[i] * p2[j-i]) % M2 + M2) % M2;
            long a2 = ((h1[k] - h1[j] * p1[k-j]) % M1 + M1) % M1;
            long b2 = ((h2[k] - h2[j] * p2[k-j]) % M2 + M2) % M2;
            if (a1 == a2 && b1 == b2)            // the two halves are equal
                seen.add((a1 * M2 + b1) * 2001 + (j - i));
        }
    }
    return seen.size();
}   // O(n^2) time · O(distinct echoes) space""",
            "python": r"""def distinct_echo_substrings(text):
    M1, M2, B1, B2 = 10**9 + 7, 10**9 + 9, 131, 137
    n = len(text)
    h1 = [0] * (n + 1); h2 = [0] * (n + 1)
    p1 = [1] * (n + 1); p2 = [1] * (n + 1)
    for i, ch in enumerate(text):
        v = ord(ch)
        h1[i+1] = (h1[i] * B1 + v) % M1
        h2[i+1] = (h2[i] * B2 + v) % M2
        p1[i+1] = p1[i] * B1 % M1
        p2[i+1] = p2[i] * B2 % M2

    def digest(l, r):                  # hash of text[l:r], both moduli
        a = (h1[r] - h1[l] * p1[r-l]) % M1
        b = (h2[r] - h2[l] * p2[r-l]) % M2
        return (a, b)

    seen = set()
    for i in range(n):
        for j in range(i + 1, n):
            k = j + (j - i)            # end of the second half
            if k > n:
                break
            if digest(i, j) == digest(j, k):
                seen.add((j - i, digest(i, j)))    # distinct by content
    return len(seen)""",
        },
    },
    {
        "slug": "word-break-ii",
        "title": "Word Break II",
        "difficulty": "Hard",
        "pattern": "memoised segmentation",
        "statement": "Given s and a dictionary, return all sentences formed by the dictionary words that together spell s (the order of the answer does "
                     "not matter).",
        "examples": [("s = \"catsanddog\", wordDict = [\"cat\",\"cats\",\"and\",\"sand\",\"dog\"]", "[\"cats and dog\",\"cat sand dog\"]"),
                     ("s = \"pineapplepenapple\", wordDict = [\"apple\",\"pen\",\"applepen\",\"pine\",\"pineapple\"]",
                      "[\"pine apple pen apple\",\"pineapple pen apple\",\"pine applepen apple\"]"),
                     ("s = \"catsandog\", wordDict = [\"cats\",\"dog\",\"sand\",\"and\",\"cat\"]", "[]")],
        "constraints": ["1 <= s.length <= 20", "1 <= wordDict.length <= 1000", "1 <= wordDict[i].length <= 10", "all dictionary words are distinct"],
        "approach": "Recursive segmentation with a memo: solve(i) returns every sentence that spells s[i:], built by taking a dictionary word at i and "
                     "gluing it to each sentence of solve(i + len(word)). The memo turns the exponential repeat work of a naive recursion into a "
                     "single computation per starting index.",
        "complexity": ("O(n · 2^n) worst case (the output itself can be that large)", "O(n · 2^n)"),
        "code": {
            "cpp": r"""// Memoised segmentation: sentences for s[i:] are computed once
vector<string> wordBreak(string s, vector<string>& wordDict) {
    unordered_set<string> dict(wordDict.begin(), wordDict.end());
    int n = s.size();
    vector<vector<string>> memo(n + 1);
    vector<bool> done(n + 1, false);
    function<vector<string>(int)> solve = [&](int i) -> vector<string> {
        if (done[i]) return memo[i];             // already worked out
        done[i] = true;
        if (i == n) return memo[i] = {""};
        vector<string> out;
        for (int j = i + 1; j <= n; j++) {
            string piece = s.substr(i, j - i);
            if (!dict.count(piece)) continue;
            for (const string& rest : solve(j)) {
                if (rest.empty()) out.push_back(piece);
                else out.push_back(piece + " " + rest);
            }
        }
        return memo[i] = out;
    };
    return solve(0);
}   // O(n·2^n) time · O(n·2^n) space""",
            "java": r"""// Memoised segmentation: sentences for s[i:] are computed once
List<String> wordBreak(String s, List<String> wordDict) {
    Set<String> dict = new HashSet<>(wordDict);
    int n = s.length();
    Map<Integer, List<String>> memo = new HashMap<>();
    return solve(s, 0, n, dict, memo);
}
List<String> solve(String s, int i, int n, Set<String> dict, Map<Integer, List<String>> memo) {
    if (memo.containsKey(i)) return memo.get(i);          // computed already
    List<String> out = new ArrayList<>();
    if (i == n) { out.add(""); memo.put(i, out); return out; }
    for (int j = i + 1; j <= n; j++) {
        String piece = s.substring(i, j);
        if (!dict.contains(piece)) continue;
        for (String rest : solve(s, j, n, dict, memo)) {
            out.add(rest.isEmpty() ? piece : piece + " " + rest);
        }
    }
    memo.put(i, out);
    return out;
}   // O(n·2^n) time · O(n·2^n) space""",
            "python": r"""def word_break_ii(s, word_dict):
    words = set(word_dict)
    n = len(s)
    memo = {}

    def solve(i):
        if i in memo:
            return memo[i]                 # computed once per start index
        if i == n:
            return ['']
        out = []
        for j in range(i + 1, n + 1):
            piece = s[i:j]
            if piece in words:
                for rest in solve(j):
                    out.append(piece + (' ' + rest if rest else ''))
        memo[i] = out
        return out

    return solve(0)""",
        },
    },
    {
        "slug": "count-different-palindromic-subsequences",
        "title": "Count Different Palindromic Subsequences",
        "difficulty": "Hard",
        "pattern": "interval DP over palindromic subsequences",
        "statement": "Count the different non-empty palindromic subsequences of s, modulo 10^9 + 7.",
        "examples": [("s = \"bccb\"", "6")],
        "constraints": ["1 <= s.length <= 1000", "s consists of 'a', 'b', 'c' and 'd'"],
        "approach": "Let dp[i][j] count distinct palindromic subsequences inside s[i..j]. When the ends differ, inclusion–exclusion on the two smaller "
                     "intervals is enough; when they are equal, each palindrome inside can be wrapped by both ends, and only the palindromes that "
                     "already start and end with that character (found by scanning inward) must be subtracted so nothing is counted twice.",
        "complexity": ("O(n²) time", "O(n²)"),
        "code": {
            "cpp": r"""// dp[i][j]: distinct palindromic subsequences inside s[i..j]
int countPalindromicSubsequences(string s) {
    const long long MOD = 1e9 + 7;
    int n = s.size();
    vector<vector<long long>> dp(n, vector<long long>(n, 0));
    for (int i = 0; i < n; i++) dp[i][i] = 1;
    for (int len = 2; len <= n; len++) {
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            if (s[i] != s[j]) {
                dp[i][j] = (dp[i+1][j] + dp[i][j-1] - dp[i+1][j-1] + MOD) % MOD;
            } else {
                int lo = i + 1, hi = j - 1;
                while (lo <= hi && s[lo] != s[i]) lo++;      // first same letter inside
                while (lo <= hi && s[hi] != s[i]) hi--;      // last same letter inside
                if (lo > hi) dp[i][j] = (dp[i+1][j-1] * 2 + 2) % MOD;   // none inside
                else if (lo == hi) dp[i][j] = (dp[i+1][j-1] * 2 + 1) % MOD;   // one inside
                else dp[i][j] = (dp[i+1][j-1] * 2 - dp[lo+1][hi-1] + MOD) % MOD;
            }
        }
    }
    return (int) dp[0][n-1];
}   // O(n^2) time · O(n^2) space""",
            "java": r"""// dp[i][j]: distinct palindromic subsequences inside s[i..j]
int countPalindromicSubsequences(String s) {
    final long MOD = 1_000_000_007L;
    int n = s.length();
    long[][] dp = new long[n][n];
    for (int i = 0; i < n; i++) dp[i][i] = 1;
    for (int len = 2; len <= n; len++) {
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            if (s.charAt(i) != s.charAt(j)) {
                dp[i][j] = (dp[i+1][j] + dp[i][j-1] - dp[i+1][j-1] + MOD) % MOD;
            } else {
                int lo = i + 1, hi = j - 1;
                while (lo <= hi && s.charAt(lo) != s.charAt(i)) lo++;   // first inside
                while (lo <= hi && s.charAt(hi) != s.charAt(i)) hi--;   // last inside
                if (lo > hi) dp[i][j] = (dp[i+1][j-1] * 2 + 2) % MOD;
                else if (lo == hi) dp[i][j] = (dp[i+1][j-1] * 2 + 1) % MOD;
                else dp[i][j] = (dp[i+1][j-1] * 2 - dp[lo+1][hi-1] + MOD) % MOD;
            }
        }
    }
    return (int) dp[0][n-1];
}   // O(n^2) time · O(n^2) space""",
            "python": r"""def count_palindromic_subseqs(s):
    MOD = 10**9 + 7
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = 1
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] != s[j]:
                dp[i][j] = (dp[i+1][j] + dp[i][j-1] - dp[i+1][j-1]) % MOD
            else:
                lo, hi = i + 1, j - 1
                while lo <= hi and s[lo] != s[i]:
                    lo += 1                     # first same letter inside
                while lo <= hi and s[hi] != s[i]:
                    hi -= 1                     # last same letter inside
                if lo > hi:                     # no copy of it inside
                    dp[i][j] = dp[i+1][j-1] * 2 + 2
                elif lo == hi:                  # exactly one copy inside
                    dp[i][j] = dp[i+1][j-1] * 2 + 1
                else:                           # subtract the double-counted part
                    dp[i][j] = dp[i+1][j-1] * 2 - dp[lo+1][hi-1]
                dp[i][j] %= MOD
    return dp[0][n-1]""",
        },
    },
    {
        "slug": "find-all-good-strings",
        "title": "Find All Good Strings",
        "difficulty": "Hard",
        "pattern": "KMP automaton inside a digit DP",
        "statement": "Count the strings of length n that are lexicographically between s1 and s2 inclusive and contain no occurrence of evil, modulo "
                     "10^9 + 7.",
        "examples": [("n = 2, s1 = \"aa\", s2 = \"da\", evil = \"b\"", "51"),
                     ("n = 8, s1 = \"leetcode\", s2 = \"leetgoes\", evil = \"leet\"", "0"),
                     ("n = 2, s1 = \"gx\", s2 = \"gz\", evil = \"x\"", "2")],
        "constraints": ["1 <= n <= 500", "1 <= evil.length <= 50", "s1.length == s2.length == n", "all strings are lowercase letters"],
        "approach": "Two ideas stacked. A KMP automaton tracks how much of `evil` is currently matched, so \"no occurrence\" becomes \"never reach the "
                     "final state\". Then a digit DP counts the strings of length n that stay at or below a bound while never hitting that state, with "
                     "one flag remembering whether the prefix is still tight. The answer is below(s2) - below(s1), plus s1 itself if it is good.",
        "complexity": ("O(n · |evil| · 26)", "O(|evil| · 26)"),
        "code": {
            "cpp": r"""// KMP automaton for evil, then a digit DP bounded above by s2 and s1
int findGoodStrings(int n, string s1, string s2, string evil) {
    const long long MOD = 1e9 + 7;
    int m = evil.size();
    vector<int> fail(m, 0);
    for (int i = 1; i < m; i++) {
        int j = fail[i-1];
        while (j > 0 && evil[i] != evil[j]) j = fail[j-1];
        if (evil[i] == evil[j]) j++;
        fail[i] = j;
    }
    vector<array<int,26>> go(m);                  // KMP automaton transitions
    for (int st = 0; st < m; st++) {
        for (int c = 0; c < 26; c++) {
            char ch = 'a' + c;
            int j = st;
            while (j > 0 && ch != evil[j]) j = fail[j-1];
            if (ch == evil[j]) j++;
            go[st][c] = j;                        // m means evil just appeared
        }
    }
    auto countUpTo = [&](const string& bound) {
        vector<vector<long long>> dp(m, vector<long long>(2, 0));
        dp[0][1] = 1;                             // (kmp state, still tight)
        for (int i = 0; i < n; i++) {
            vector<vector<long long>> ndp(m, vector<long long>(2, 0));
            for (int st = 0; st < m; st++)
                for (int tight = 0; tight < 2; tight++) {
                    long long ways = dp[st][tight];
                    if (!ways) continue;
                    int limit = tight ? bound[i] - 'a' : 25;
                    for (int c = 0; c <= limit; c++) {
                        int ns = go[st][c];
                        if (ns == m) continue;    // evil appeared: forbidden
                        int nt = (tight && c == limit) ? 1 : 0;
                        ndp[ns][nt] = (ndp[ns][nt] + ways) % MOD;
                    }
                }
            dp = move(ndp);
        }
        long long total = 0;
        for (int st = 0; st < m; st++)
            total = (total + dp[st][0] + dp[st][1]) % MOD;
        return total;
    };
    long long answer = (countUpTo(s2) - countUpTo(s1) + MOD) % MOD;
    int state = 0;
    bool good = true;
    for (char ch : s1) {
        state = go[state][ch - 'a'];
        if (state == m) { good = false; break; }  // s1 itself contains evil
    }
    if (good) answer = (answer + 1) % MOD;        // s1 counts when it is good
    return (int) answer;
}   // O(n · |evil| · 26) time · O(|evil| · 26) space""",
            "java": r"""// KMP automaton for evil, then a digit DP bounded above by s2 and s1
int findGoodStrings(int n, String s1, String s2, String evil) {
    final long MOD = 1_000_000_007L;
    int m = evil.length();
    int[] fail = new int[m];
    for (int i = 1; i < m; i++) {
        int j = fail[i-1];
        while (j > 0 && evil.charAt(i) != evil.charAt(j)) j = fail[j-1];
        if (evil.charAt(i) == evil.charAt(j)) j++;
        fail[i] = j;
    }
    int[][] go = new int[m][26];                  // KMP automaton transitions
    for (int st = 0; st < m; st++) {
        for (int c = 0; c < 26; c++) {
            char ch = (char) ('a' + c);
            int j = st;
            while (j > 0 && ch != evil.charAt(j)) j = fail[j-1];
            if (ch == evil.charAt(j)) j++;
            go[st][c] = j;                        // m means evil just appeared
        }
    }
    long answer = (countUpTo(n, s2, m, go, MOD) - countUpTo(n, s1, m, go, MOD) + MOD) % MOD;
    int state = 0;
    boolean good = true;
    for (int i = 0; i < n; i++) {
        state = go[state][s1.charAt(i) - 'a'];
        if (state == m) { good = false; break; }  // s1 itself contains evil
    }
    if (good) answer = (answer + 1) % MOD;        // s1 counts when it is good
    return (int) answer;
}
long countUpTo(int n, String bound, int m, int[][] go, long MOD) {
    long[][] dp = new long[m][2];
    dp[0][1] = 1;                                 // (kmp state, still tight)
    for (int i = 0; i < n; i++) {
        long[][] ndp = new long[m][2];
        for (int st = 0; st < m; st++)
            for (int tight = 0; tight < 2; tight++) {
                long ways = dp[st][tight];
                if (ways == 0) continue;
                int limit = tight == 1 ? bound.charAt(i) - 'a' : 25;
                for (int c = 0; c <= limit; c++) {
                    int ns = go[st][c];
                    if (ns == m) continue;        // evil appeared: forbidden
                    int nt = (tight == 1 && c == limit) ? 1 : 0;
                    ndp[ns][nt] = (ndp[ns][nt] + ways) % MOD;
                }
            }
        dp = ndp;
    }
    long total = 0;
    for (int st = 0; st < m; st++) total = (total + dp[st][0] + dp[st][1]) % MOD;
    return total;
}   // O(n · |evil| · 26) time · O(|evil| · 26) space""",
            "python": r"""def find_good_strings(n, s1, s2, evil):
    MOD = 10**9 + 7
    m = len(evil)
    fail = [0] * m
    for i in range(1, m):
        j = fail[i-1]
        while j > 0 and evil[i] != evil[j]:
            j = fail[j-1]
        if evil[i] == evil[j]:
            j += 1
        fail[i] = j

    go = [[0] * 26 for _ in range(m)]        # KMP automaton: state x letter
    for state in range(m):
        for c in range(26):
            ch = chr(97 + c)
            j = state
            while j > 0 and ch != evil[j]:
                j = fail[j-1]
            if ch == evil[j]:
                j += 1
            go[state][c] = j                 # m means evil just appeared

    def count_up_to(bound):
        dp = {(0, True): 1}                  # (kmp state, still tight) -> ways
        for i in range(n):
            ndp = {}
            for (state, tight), ways in dp.items():
                limit = ord(bound[i]) - 97 if tight else 25
                for c in range(limit + 1):
                    ns = go[state][c]
                    if ns == m:
                        continue             # evil appeared: forbidden
                    key = (ns, tight and c == limit)
                    ndp[key] = (ndp.get(key, 0) + ways) % MOD
            dp = ndp
        return sum(dp.values()) % MOD

    answer = (count_up_to(s2) - count_up_to(s1)) % MOD
    state = 0
    good = True
    for ch in s1:
        state = go[state][ord(ch) - 97]
        if state == m:
            good = False                     # s1 itself contains evil
            break
    if good:
        answer = (answer + 1) % MOD          # s1 counts when it is good
    return answer""",
        },
    },
]
