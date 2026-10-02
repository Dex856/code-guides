# Topic 4 · Stacks, Queues & Monotonic Structures
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.

TOPIC = {
    "name": "Stacks, Queues & Monotonic Structures",
    "tagline": "LIFO and FIFO as tools: undo, matching, parsing — and the monotonic stack, which answers 'next bigger element' for every position in one pass.",
    "focus": "Recognising the three families: plain stacks for nesting and undo, queues/deques for order, and monotonic stacks or deques for "
             "next-greater / previous-smaller / sliding extremes. Includes parsing (expressions, paths, atoms), design questions "
             "(min-stack, circular queue) and the classic hard rectangles.",
    "ordering": "easy 1–6 are direct stack simulation and the gentlest monotonic-stack introduction; medium 1–4 are parsing and simulation, "
                "5–8 are monotonic stacks for next greater/smaller, 9–12 are design, contribution counting and sorting-based stacks; "
                "hard 1–4 are the rectangle/parenthesis/water classics, 5–8 are heavy parsing, 9–12 are monotonic-stack competition variants.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "valid-parentheses",
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "pattern": "stack of open brackets",
        "statement": "Given a string of the characters ()[]{}, decide whether every opening bracket is closed by the matching type in the "
                     "correct order.",
        "examples": [("s = \"()[]{}\"", "true"), ("s = \"(]\"", "false"), ("s = \"([)]\"", "false")],
        "constraints": ["1 <= len(s) <= 10^4", "s contains only bracket characters", "an empty string is considered valid"],
        "approach": "Every closing bracket must match the most recent unmatched opener — exactly LIFO order. Push openers, and on a closer "
                     "either pop a matching opener or fail immediately; at the end the stack must be empty, otherwise brackets were left open.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// A closer must match the most recent unmatched opener
bool isValid(string s) {
    unordered_map<char, char> match{{')', '('}, {']', '['}, {'}', '{'}};
    vector<char> st;
    for (char c : s) {
        if (!match.count(c)) st.push_back(c);            // an opener
        else if (st.empty() || st.back() != match[c]) return false;
        else st.pop_back();
    }
    return st.empty();                                   // nothing left open
}   // O(n) time · O(n) space""",
            "java": r"""// A closer must match the most recent unmatched opener
boolean isValid(String s) {
    Map<Character, Character> match = Map.of(')', '(', ']', '[', '}', '{');
    Deque<Character> st = new ArrayDeque<>();
    for (char c : s.toCharArray()) {
        if (!match.containsKey(c)) st.push(c);           // an opener
        else if (st.isEmpty() || st.peek() != match.get(c)) return false;
        else st.pop();
    }
    return st.isEmpty();                                 // nothing left open
}   // O(n) time · O(n) space""",
            "python": r"""def is_valid(s):
    match = {')': '(', ']': '[', '}': '{'}
    st = []
    for c in s:
        if c not in match:
            st.append(c)                 # an opener
        elif not st or st[-1] != match[c]:
            return False
        else:
            st.pop()
    return not st                        # nothing left open""",
        },
    },
    {
        "slug": "min-stack",
        "title": "Min Stack",
        "difficulty": "Easy",
        "pattern": "two parallel stacks",
        "statement": "Design a stack with push, pop, top and getMin, all in O(1). getMin returns the smallest value currently in the stack.",
        "examples": [("push(-2), push(0), push(-3), getMin()", "-3"),
                     ("pop(), top(), getMin()", "0 then -2")],
        "constraints": ["up to 3 * 10^4 calls", "-2^31 <= values <= 2^31 - 1", "pop/top/getMin are never called on an empty stack"],
        "approach": "Keep a second stack holding, at every depth, the minimum of everything below it. Pushing the minimum of (value, current "
                     "minimum) makes getMin a peek, and popping restores the previous minimum automatically — no recomputation, no scanning.",
        "complexity": ("O(1) per op", "O(n)"),
        "code": {
            "cpp": r"""// Second stack: the running minimum at every depth
class MinStack {
    vector<int> vals, mins;
public:
    void push(int v) {
        vals.push_back(v);
        mins.push_back(mins.empty() ? v : min(v, mins.back()));
    }
    void pop() { vals.pop_back(); mins.pop_back(); }
    int top() { return vals.back(); }
    int getMin() { return mins.back(); }
};   // O(1) per op · O(n) space""",
            "java": r"""// Second stack: the running minimum at every depth
class MinStack {
    private final Deque<Integer> vals = new ArrayDeque<>(), mins = new ArrayDeque<>();

    public void push(int v) {
        vals.push(v);
        mins.push(mins.isEmpty() ? v : Math.min(v, mins.peek()));
    }
    public void pop() { vals.pop(); mins.pop(); }
    public int top() { return vals.peek(); }
    public int getMin() { return mins.peek(); }
}   // O(1) per op · O(n) space""",
            "python": r"""class MinStack:
    def __init__(self):
        self.vals = []
        self.mins = []            # running minimum at every depth

    def push(self, v):
        self.vals.append(v)
        self.mins.append(v if not self.mins else min(v, self.mins[-1]))

    def pop(self):
        self.vals.pop()
        self.mins.pop()           # restores the previous minimum for free

    def top(self):
        return self.vals[-1]

    def get_min(self):
        return self.mins[-1]""",
        },
    },
    {
        "slug": "baseball-game",
        "title": "Baseball Game",
        "difficulty": "Easy",
        "pattern": "stack simulation",
        "statement": "Process a list of operations: an integer scores that many points, \"+\" scores the sum of the last two scores, \"D\" scores "
                     "double the last score, and \"C\" cancels the last score. Return the sum of all scores on the record.",
        "examples": [("[\"5\",\"2\",\"C\",\"D\",\"+\"]", "30"), ("[\"5\",\"-2\",\"4\",\"C\",\"D\",\"9\",\"+\",\"+\"]", "27")],
        "constraints": ["1 <= number of operations <= 1000", "operations are valid as described", "the total fits in a 32-bit integer"],
        "approach": "The record is exactly a stack: every operation reads or removes only the most recent scores. Accumulate the running total as "
                     "you push or cancel, then the answer costs nothing extra.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// The score record is a stack, and "C" is a pop
int calPoints(vector<string>& ops) {
    vector<int> st; int total = 0;
    for (const string& op : ops) {
        if (op == "+") { int v = st[st.size()-1] + st[st.size()-2]; st.push_back(v); total += v; }
        else if (op == "D") { int v = 2 * st.back(); st.push_back(v); total += v; }
        else if (op == "C") { total -= st.back(); st.pop_back(); }
        else { int v = stoi(op); st.push_back(v); total += v; }
    }
    return total;
}   // O(n) time · O(n) space""",
            "java": r"""// The score record is a stack, and "C" is a pop
int calPoints(String[] ops) {
    Deque<Integer> st = new ArrayDeque<>(); int total = 0;
    for (String op : ops) {
        if (op.equals("+")) { int v = st.peek() + st.stream().skip(1).findFirst().orElse(0); st.push(v); total += v; }
        else if (op.equals("D")) { int v = 2 * st.peek(); st.push(v); total += v; }
        else if (op.equals("C")) { total -= st.pop(); }
        else { int v = Integer.parseInt(op); st.push(v); total += v; }
    }
    return total;
}   // O(n) time · O(n) space""",
            "python": r"""def cal_points(ops):
    st, total = [], 0
    for op in ops:
        if op == '+':
            v = st[-1] + st[-2]
            st.append(v); total += v
        elif op == 'D':
            v = 2 * st[-1]
            st.append(v); total += v
        elif op == 'C':
            total -= st.pop()          # cancel the last score
        else:
            v = int(op)
            st.append(v); total += v
    return total""",
        },
    },
    {
        "slug": "queue-using-stacks",
        "title": "Implement Queue Using Stacks",
        "difficulty": "Easy",
        "pattern": "two stacks, amortised",
        "statement": "Implement a first-in-first-out queue using only two stacks, supporting push, pop, peek and empty.",
        "examples": [("push(1), push(2), peek()", "1"), ("pop(), empty()", "1, then false")],
        "constraints": ["up to 100 calls", "1 <= values <= 9", "pop/peek are never called on an empty queue"],
        "approach": "An input stack receives pushes and an output stack serves pops. When the output stack is empty, pour the whole input into it — "
                     "that reverses the order once, and every element is moved at most once, so the expensive step is amortised O(1).",
        "complexity": ("O(1) amortised per op", "O(n)"),
        "code": {
            "cpp": r"""// in for pushes, out for pops; pour only when out is empty
class MyQueue {
    vector<int> in, out;
    void pour() {
        while (!in.empty()) { out.push_back(in.back()); in.pop_back(); }
    }
public:
    void push(int x) { in.push_back(x); }
    int pop() { if (out.empty()) pour(); int v = out.back(); out.pop_back(); return v; }
    int peek() { if (out.empty()) pour(); return out.back(); }
    bool empty() { return in.empty() && out.empty(); }
};   // O(1) amortised per op · O(n) space""",
            "java": r"""// in for pushes, out for pops; pour only when out is empty
class MyQueue {
    private final Deque<Integer> in = new ArrayDeque<>(), out = new ArrayDeque<>();

    private void pour() {
        while (!in.isEmpty()) out.push(in.pop());
    }
    public void push(int x) { in.push(x); }
    public int pop() { if (out.isEmpty()) pour(); return out.pop(); }
    public int peek() { if (out.isEmpty()) pour(); return out.peek(); }
    public boolean empty() { return in.isEmpty() && out.isEmpty(); }
}   // O(1) amortised per op · O(n) space""",
            "python": r"""class MyQueue:
    def __init__(self):
        self.inbox = []            # pushes land here
        self.outbox = []           # pops are served from here

    def _pour(self):
        while self.inbox:
            self.outbox.append(self.inbox.pop())   # reverses the order once

    def push(self, x):
        self.inbox.append(x)

    def pop(self):
        if not self.outbox:
            self._pour()
        return self.outbox.pop()

    def peek(self):
        if not self.outbox:
            self._pour()
        return self.outbox[-1]

    def empty(self):
        return not self.inbox and not self.outbox""",
        },
    },
    {
        "slug": "backspace-string-compare",
        "title": "Backspace String Compare",
        "difficulty": "Easy",
        "pattern": "two pointers from the right",
        "statement": "The character '#' deletes the previous character. Given two strings typed this way, decide whether they are equal, using "
                     "O(1) extra memory.",
        "examples": [("s = \"ab#c\", t = \"ad#c\"", "true"), ("s = \"a#c\", t = \"b\"", "false")],
        "constraints": ["1 <= len(s), len(t) <= 200", "strings contain lowercase letters and '#'", "extra memory must be O(1)"],
        "approach": "Building both strings is easy but uses memory. Walking from the right with a skip counter consumes the backspaces first and "
                     "needs no storage at all: each pointer skips characters that a later '#' already cancelled, then the two visible characters "
                     "are compared directly.",
        "complexity": ("O(n + m)", "O(1)"),
        "code": {
            "cpp": r"""// Walk from the right, consuming '#' with a skip counter
bool backspaceCompare(string s, string t) {
    int i = s.size() - 1, j = t.size() - 1, skipS = 0, skipT = 0;
    while (i >= 0 || j >= 0) {
        while (i >= 0 && (skipS || s[i] == '#')) { s[i] == '#' ? skipS++ : skipS--; i--; }
        while (j >= 0 && (skipT || t[j] == '#')) { t[j] == '#' ? skipT++ : skipT--; j--; }
        char a = i >= 0 ? s[i] : 0, b = j >= 0 ? t[j] : 0;
        if (a != b) return false;
        i--; j--;
    }
    return true;
}   // O(n + m) time · O(1) space""",
            "java": r"""// Walk from the right, consuming '#' with a skip counter
boolean backspaceCompare(String s, String t) {
    int i = s.length() - 1, j = t.length() - 1, skipS = 0, skipT = 0;
    while (i >= 0 || j >= 0) {
        while (i >= 0 && (skipS > 0 || s.charAt(i) == '#')) {
            if (s.charAt(i) == '#') skipS++; else skipS--;
            i--;
        }
        while (j >= 0 && (skipT > 0 || t.charAt(j) == '#')) {
            if (t.charAt(j) == '#') skipT++; else skipT--;
            j--;
        }
        char a = i >= 0 ? s.charAt(i) : 0, b = j >= 0 ? t.charAt(j) : 0;
        if (a != b) return false;
        i--; j--;
    }
    return true;
}   // O(n + m) time · O(1) space""",
            "python": r"""def backspace_compare(s, t):
    i, j = len(s) - 1, len(t) - 1
    skip_s = skip_t = 0
    while i >= 0 or j >= 0:
        while i >= 0 and (skip_s or s[i] == '#'):
            skip_s += 1 if s[i] == '#' else -1   # backspaces cancel earlier chars
            i -= 1
        while j >= 0 and (skip_t or t[j] == '#'):
            skip_t += 1 if t[j] == '#' else -1
            j -= 1
        a = s[i] if i >= 0 else ''
        b = t[j] if j >= 0 else ''
        if a != b:
            return False
        i -= 1
        j -= 1
    return True""",
        },
    },
    {
        "slug": "next-greater-element-i",
        "title": "Next Greater Element I",
        "difficulty": "Easy",
        "pattern": "first monotonic stack",
        "statement": "For each element of nums1 (which is a subset of nums2), find its next greater element to the right inside nums2, or -1 if "
                     "there is none.",
        "examples": [("nums1 = [4,1,2], nums2 = [1,3,4,2]", "[-1,3,-1]"), ("nums1 = [2,4], nums2 = [1,2,3,4]", "[3,-1]")],
        "constraints": ["1 <= len(nums1) <= len(nums2) <= 1000", "all values in nums2 are distinct", "nums1's values all appear in nums2"],
        "approach": "Scan nums2 once with a stack of values that are still waiting for a bigger neighbour. Each new value pops (and answers) every "
                     "smaller value on top — that is the monotonic stack: the stack is always decreasing, and each element is pushed and popped once.",
        "complexity": ("O(n + m)", "O(m)"),
        "code": {
            "cpp": r"""// Decreasing stack answers every element in one pass
vector<int> nextGreaterElement(vector<int>& nums1, vector<int>& nums2) {
    unordered_map<int, int> nge;                 // value -> next greater
    vector<int> st;                              // decreasing stack
    for (int v : nums2) {
        while (!st.empty() && st.back() < v) { nge[st.back()] = v; st.pop_back(); }
        st.push_back(v);
    }
    vector<int> out;
    for (int v : nums1) out.push_back(nge.count(v) ? nge[v] : -1);
    return out;
}   // O(n + m) time · O(m) space""",
            "java": r"""// Decreasing stack answers every element in one pass
int[] nextGreaterElement(int[] nums1, int[] nums2) {
    Map<Integer, Integer> nge = new HashMap<>();   // value -> next greater
    Deque<Integer> st = new ArrayDeque<>();        // decreasing stack
    for (int v : nums2) {
        while (!st.isEmpty() && st.peek() < v) nge.put(st.pop(), v);
        st.push(v);
    }
    int[] out = new int[nums1.length];
    for (int i = 0; i < nums1.length; i++) out[i] = nge.getOrDefault(nums1[i], -1);
    return out;
}   // O(n + m) time · O(m) space""",
            "python": r"""def next_greater_element(nums1, nums2):
    nge = {}                 # value -> next greater value
    st = []                  # decreasing stack of values still waiting
    for v in nums2:
        while st and st[-1] < v:
            nge[st.pop()] = v    # v is the answer for the popped value
        st.append(v)
    return [nge.get(v, -1) for v in nums1]""",
        },
    },
    # ---------------------------------------------------------------- MEDIUM
    {
        "slug": "daily-temperatures",
        "title": "Daily Temperatures",
        "difficulty": "Medium",
        "pattern": "monotonic stack of indices",
        "statement": "For each day, return how many days you must wait for a warmer temperature, or 0 if it never comes.",
        "examples": [("temperatures = [73,74,75,71,69,72,76,73]", "[1,1,4,2,1,1,0,0]"),
                     ("temperatures = [30,40,50,60]", "[1,1,1,0]")],
        "constraints": ["1 <= n <= 10^5", "30 <= temperature <= 100", "answers describe the next strictly warmer day"],
        "approach": "Store indices, not values, so the answer is a subtraction. The stack holds days still waiting for something warmer and is "
                     "decreasing in temperature; a new day settles all cooler waiting days at once, and anything still on the stack at the end "
                     "gets 0.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Indices on a decreasing stack: each pop is one answer
vector<int> dailyTemperatures(vector<int>& t) {
    int n = t.size();
    vector<int> ans(n, 0), st;                   // st holds indices, coolest on top
    for (int i = 0; i < n; i++) {
        while (!st.empty() && t[st.back()] < t[i]) {
            ans[st.back()] = i - st.back();      // wait = index difference
            st.pop_back();
        }
        st.push_back(i);
    }
    return ans;
}   // O(n) time · O(n) space""",
            "java": r"""// Indices on a decreasing stack: each pop is one answer
int[] dailyTemperatures(int[] t) {
    int n = t.length;
    int[] ans = new int[n];
    Deque<Integer> st = new ArrayDeque<>();      // indices, coolest on top
    for (int i = 0; i < n; i++) {
        while (!st.isEmpty() && t[st.peek()] < t[i]) {
            int j = st.pop();
            ans[j] = i - j;                      // wait = index difference
        }
        st.push(i);
    }
    return ans;
}   // O(n) time · O(n) space""",
            "python": r"""def daily_temperatures(t):
    ans = [0] * len(t)
    st = []                              # indices, coolest on top
    for i, v in enumerate(t):
        while st and t[st[-1]] < v:
            j = st.pop()
            ans[j] = i - j               # wait = index difference
        st.append(i)
    return ans""",
        },
    },
    {
        "slug": "evaluate-reverse-polish-notation",
        "title": "Evaluate Reverse Polish Notation",
        "difficulty": "Medium",
        "pattern": "operand stack",
        "statement": "Evaluate an expression in postfix (reverse Polish) notation. Valid operators are + - * /. Division truncates toward zero.",
        "examples": [("tokens = [\"2\",\"1\",\"+\",\"3\",\"*\"]", "9"), ("tokens = [\"4\",\"13\",\"5\",\"/\",\"+\"]", "6")],
        "constraints": ["1 <= number of tokens <= 10^4", "the expression is always valid", "all intermediate values fit in a 32-bit integer"],
        "approach": "Postfix exists precisely because it needs no precedence rules or parentheses: push numbers and, on an operator, pop the two "
                     "most recent operands, compute, and push the result. Note the operand order — the first pop is the right-hand side.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Push numbers; an operator consumes the two most recent
int evalRPN(vector<string>& tokens) {
    vector<int> st;
    for (const string& t : tokens) {
        if (t.size() == 1 && !isdigit(t[0])) {
            int b = st.back(); st.pop_back();        // right operand first
            int a = st.back(); st.pop_back();
            int r = t == "+" ? a + b : t == "-" ? a - b : t == "*" ? a * b : a / b;
            st.push_back(r);
        } else st.push_back(stoi(t));
    }
    return st.back();
}   // O(n) time · O(n) space""",
            "java": r"""// Push numbers; an operator consumes the two most recent
int evalRPN(String[] tokens) {
    Deque<Integer> st = new ArrayDeque<>();
    for (String t : tokens) {
        if (t.length() == 1 && !Character.isDigit(t.charAt(0))) {
            int b = st.pop();                        // right operand first
            int a = st.pop();
            int r = t.equals("+") ? a + b : t.equals("-") ? a - b
                  : t.equals("*") ? a * b : a / b;   // Java / truncates toward zero
            st.push(r);
        } else st.push(Integer.parseInt(t));
    }
    return st.pop();
}   // O(n) time · O(n) space""",
            "python": r"""def eval_rpn(tokens):
    st = []
    ops = {'+': lambda a, b: a + b, '-': lambda a, b: a - b,
           '*': lambda a, b: a * b,
           '/': lambda a, b: int(a / b)}    # truncate toward zero, not floor
    for t in tokens:
        if t in ops:
            b = st.pop()                     # right operand first
            a = st.pop()
            st.append(ops[t](a, b))
        else:
            st.append(int(t))
    return st[-1]""",
        },
    },
    {
        "slug": "decode-string",
        "title": "Decode String",
        "difficulty": "Medium",
        "pattern": "stack of (prefix, repeat)",
        "statement": "Decode a string written as k[encoded] where the bracketed part repeats k times; brackets may nest.",
        "examples": [("s = \"3[a]2[bc]\"", "\"aaabcbc\""), ("s = \"3[a2[c]]\"", "\"accaccacc\""), ("s = \"2[abc]3[cd]ef\"", "\"abcabccdcdcdef\"")],
        "constraints": ["1 <= len(s) <= 30", "k is a positive integer without leading zeros", "the decoded output is at most 10^5 characters"],
        "approach": "When a '[' appears, the work done so far is finished for now: save the current builder and the repeat count on the stack and "
                     "start fresh. On ']', pop and concatenate repeats of the inner result. The stack holds exactly the unfinished outer contexts, "
                     "so nesting is automatic.",
        "complexity": ("O(output length)", "O(depth)"),
        "code": {
            "cpp": r"""// '[' saves the outer context, ']' replays the inner result
string decodeString(string s) {
    vector<pair<string, int>> st;                // (prefix so far, repeat count)
    string cur; int num = 0;
    for (char c : s) {
        if (isdigit(c)) num = num * 10 + (c - '0');
        else if (c == '[') { st.push_back({cur, num}); cur.clear(); num = 0; }
        else if (c == ']') {
            auto [pre, k] = st.back(); st.pop_back();
            string rep; rep.reserve(cur.size() * k);
            for (int i = 0; i < k; i++) rep += cur;
            cur = pre + rep;
        } else cur += c;
    }
    return cur;
}   // O(output) time · O(depth) space""",
            "java": r"""// '[' saves the outer context, ']' replays the inner result
String decodeString(String s) {
    Deque<String> prefix = new ArrayDeque<>();
    Deque<Integer> counts = new ArrayDeque<>();
    StringBuilder cur = new StringBuilder(); int num = 0;
    for (char c : s.toCharArray()) {
        if (Character.isDigit(c)) num = num * 10 + (c - '0');
        else if (c == '[') { prefix.push(cur.toString()); counts.push(num); cur.setLength(0); num = 0; }
        else if (c == ']') {
            int k = counts.pop();
            String inner = cur.toString();
            cur.setLength(0);
            cur.append(prefix.pop());
            for (int i = 0; i < k; i++) cur.append(inner);
        } else cur.append(c);
    }
    return cur.toString();
}   // O(output) time · O(depth) space""",
            "python": r"""def decode_string(s):
    stack = []                   # (prefix built so far, repeat count)
    cur, num = '', 0
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c == '[':
            stack.append((cur, num))   # save the outer context
            cur, num = '', 0
        elif c == ']':
            pre, k = stack.pop()
            cur = pre + cur * k        # replay the inner result k times
        else:
            cur += c
    return cur""",
        },
    },
    {
        "slug": "simplify-path",
        "title": "Simplify Path",
        "difficulty": "Medium",
        "pattern": "stack of path components",
        "statement": "Convert a Unix-style absolute path into its canonical form: collapse repeated slashes, drop '.' components, apply '..' "
                     "by removing the previous component, and never go above the root.",
        "examples": [("path = \"/home//foo/\"", "\"/home/foo\""), ("path = \"/a/./b/../../c/\"", "\"/c\""), ("path = \"/../\"", "\"/\"")],
        "constraints": ["1 <= len(path) <= 3000", "path starts with '/' and holds letters, digits, '.', '_' and '/'", "the result always starts with '/'"],
        "approach": "Splitting on '/' makes each component an instruction: ignore empty and '.', pop for '..' (when non-empty), push otherwise. "
                     "The remaining components joined with '/' are the canonical path — the stack is the set of directories currently open.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Split on '/', then treat each part as an instruction
string simplifyPath(string path) {
    vector<string> st;
    stringstream ss(path); string part;
    while (getline(ss, part, '/')) {
        if (part.empty() || part == ".") continue;
        else if (part == "..") { if (!st.empty()) st.pop_back(); }
        else st.push_back(part);
    }
    string out;
    for (const string& d : st) out += "/" + d;
    return out.empty() ? "/" : out;
}   // O(n) time · O(n) space""",
            "java": r"""// Split on '/', then treat each part as an instruction
String simplifyPath(String path) {
    Deque<String> st = new ArrayDeque<>();
    for (String part : path.split("/")) {
        if (part.isEmpty() || part.equals(".")) continue;
        else if (part.equals("..")) { if (!st.isEmpty()) st.pop(); }
        else st.push(part);
    }
    StringBuilder out = new StringBuilder();
    for (Iterator<String> it = st.descendingIterator(); it.hasNext(); )
        out.append('/').append(it.next());
    return out.length() == 0 ? "/" : out.toString();
}   // O(n) time · O(n) space""",
            "python": r"""def simplify_path(path):
    st = []
    for part in path.split('/'):
        if part in ('', '.'):
            continue
        if part == '..':
            if st:
                st.pop()             # go up one directory, never above root
        else:
            st.append(part)
    return '/' + '/'.join(st)""",
        },
    },
    {
        "slug": "next-greater-element-ii",
        "title": "Next Greater Element II (Circular)",
        "difficulty": "Medium",
        "pattern": "monotonic stack + doubled scan",
        "statement": "Given a circular array, return for each element the next strictly greater value when moving forward (wrapping around), or "
                     "-1 if none exists.",
        "examples": [("[1,2,1]", "[2,-1,2]"), ("[1,2,3,4,3]", "[2,3,4,-1,4]")],
        "constraints": ["1 <= n <= 10^4", "-10^9 <= values <= 10^9", "the search wraps around but visits each element at most once"],
        "approach": "Walking the array twice with index modulo n simulates the wrap. The second pass only resolves leftovers, so no element is "
                     "answered twice as long as you record an answer only when it is still missing.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Two passes with modulo simulate the wrap
vector<int> nextGreaterElements(vector<int>& a) {
    int n = a.size();
    vector<int> ans(n, -1), st;                  // decreasing stack of indices
    for (int i = 0; i < 2 * n; i++) {
        int v = a[i % n];
        while (!st.empty() && a[st.back()] < v) {
            ans[st.back()] = v;                  // first bigger value wins
            st.pop_back();
        }
        if (i < n) st.push_back(i);              // push each index once
    }
    return ans;
}   // O(n) time · O(n) space""",
            "java": r"""// Two passes with modulo simulate the wrap
int[] nextGreaterElements(int[] a) {
    int n = a.length;
    int[] ans = new int[n];
    Arrays.fill(ans, -1);
    Deque<Integer> st = new ArrayDeque<>();      // decreasing stack of indices
    for (int i = 0; i < 2 * n; i++) {
        int v = a[i % n];
        while (!st.isEmpty() && a[st.peek()] < v) ans[st.pop()] = v;
        if (i < n) st.push(i);                   // push each index once
    }
    return ans;
}   // O(n) time · O(n) space""",
            "python": r"""def next_greater_elements(a):
    n = len(a)
    ans = [-1] * n
    st = []                                # decreasing stack of indices
    for i in range(2 * n):                 # second pass simulates the wrap
        v = a[i % n]
        while st and a[st[-1]] < v:
            ans[st.pop()] = v              # first bigger value wins
        if i < n:
            st.append(i)                   # push each index once
    return ans""",
        },
    },
    {
        "slug": "online-stock-span",
        "title": "Online Stock Span",
        "difficulty": "Medium",
        "pattern": "monotonic stack of spans",
        "statement": "Each day a stock price is given. The span of a day is the number of consecutive days ending today with a price less than or "
                     "equal to today's price. Return the span for every day as prices arrive.",
        "examples": [("prices = [100,80,60,70,60,75,85]", "spans = [1,1,1,2,1,4,6]")],
        "constraints": ["1 <= number of calls <= 10^4", "1 <= price <= 10^5", "each call must be efficient — the sequence is online"],
        "approach": "Collapse every run of days into one entry holding (price, span) on a decreasing stack. A new price pops all smaller-or-equal "
                     "entries and absorbs their spans, which is why the total work over n calls stays linear instead of rescanning history.",
        "complexity": ("O(1) amortised per call", "O(n)"),
        "code": {
            "cpp": r"""// Runs collapsed to (price, span) on a decreasing stack
class StockSpanner {
    vector<pair<int, int>> st;                   // (price, span), decreasing price
public:
    int next(int price) {
        int span = 1;
        while (!st.empty() && st.back().first <= price) {   // "less than or equal"
            span += st.back().second;                        // absorb the run
            st.pop_back();
        }
        st.push_back({price, span});
        return span;
    }
};   // O(1) amortised per call · O(n) space""",
            "java": r"""// Runs collapsed to (price, span) on a decreasing stack
class StockSpanner {
    private final Deque<int[]> st = new ArrayDeque<>();   // {price, span}

    public int next(int price) {
        int span = 1;
        while (!st.isEmpty() && st.peek()[0] <= price)       // "less than or equal"
            span += st.pop()[1];                             // absorb the run
        st.push(new int[]{price, span});
        return span;
    }
}   // O(1) amortised per call · O(n) space""",
            "python": r"""class StockSpanner:
    def __init__(self):
        self.st = []                  # (price, span), decreasing by price

    def next(self, price):
        span = 1
        while self.st and self.st[-1][0] <= price:   # "less than or equal"
            span += self.st.pop()[1]                 # absorb the whole run
        self.st.append((price, span))
        return span""",
        },
    },
    {
        "slug": "remove-k-digits",
        "title": "Remove K Digits",
        "difficulty": "Medium",
        "pattern": "greedy monotonic stack",
        "statement": "Remove exactly k digits from a non-negative integer string so that the remaining number is as small as possible. Return it "
                     "without leading zeros, or \"0\" if nothing is left.",
        "examples": [("num = \"1432219\", k = 3", "\"1219\""), ("num = \"10200\", k = 1", "\"200\""), ("num = \"10\", k = 2", "\"0\"")],
        "constraints": ["1 <= len(num) <= 10^5", "0 <= k <= len(num)", "num has no leading zeros unless it is \"0\""],
        "approach": "A digit that is larger than the digit after it should go first — removing it lowers the number at the most significant "
                     "position. Keep a stack of kept digits that is non-decreasing, popping while you still have removals left, then trim any "
                     "leftover k from the tail and strip leading zeros.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Non-decreasing stack; remove from the front first, then the tail
string removeKdigits(string num, int k) {
    string st;
    for (char c : num) {
        while (k > 0 && !st.empty() && st.back() > c) { st.pop_back(); k--; }
        st.push_back(c);
    }
    while (k-- > 0 && !st.empty()) st.pop_back();       // leftover removals
    int i = 0;
    while (i < (int)st.size() && st[i] == '0') i++;     // strip leading zeros
    string out = st.substr(i);
    return out.empty() ? "0" : out;
}   // O(n) time · O(n) space""",
            "java": r"""// Non-decreasing stack; remove from the front first, then the tail
String removeKdigits(String num, int k) {
    Deque<Character> st = new ArrayDeque<>();
    for (char c : num.toCharArray()) {
        while (k > 0 && !st.isEmpty() && st.peek() > c) { st.pop(); k--; }
        st.push(c);
    }
    while (k-- > 0 && !st.isEmpty()) st.pop();          // leftover removals
    StringBuilder sb = new StringBuilder();
    for (Iterator<Character> it = st.descendingIterator(); it.hasNext(); ) sb.append(it.next());
    int i = 0;
    while (i < sb.length() && sb.charAt(i) == '0') i++; // strip leading zeros
    String out = sb.substring(i);
    return out.isEmpty() ? "0" : out;
}   // O(n) time · O(n) space""",
            "python": r"""def remove_k_digits(num, k):
    st = []
    for c in num:
        while k and st and st[-1] > c:
            st.pop()                # dropping a bigger earlier digit helps most
            k -= 1
        st.append(c)
    if k:
        st = st[:-k]               # k still left: cut from the tail
    out = ''.join(st).lstrip('0')  # strip leading zeros
    return out or '0'""",
        },
    },
    {
        "slug": "asteroid-collision",
        "title": "Asteroid Collision",
        "difficulty": "Medium",
        "pattern": "stack simulation with rules",
        "statement": "Asteroids move along a line: a positive value moves right, a negative one moves left, and the absolute value is the size. "
                     "When two meet, the smaller explodes; equal sizes both explode. Return the final state.",
        "examples": [("asteroids = [5,10,-5]", "[5,10]"), ("asteroids = [8,-8]", "[]"), ("asteroids = [10,2,-5]", "[10]")],
        "constraints": ["1 <= n <= 10^4", "-1000 <= values <= 1000", "two asteroids meet only when a right-mover precedes a left-mover"],
        "approach": "Only a right-moving asteroid already on the stack can be hit by a left-moving newcomer; once the newcomer is moving left, "
                     "everything ahead of it is destroyed or it dies. Encode that as a while-loop over the stack top and end with the survivors.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Only a left-mover can be blocked by the stack top
vector<int> asteroidCollision(vector<int>& a) {
    vector<int> st;
    for (int v : a) {
        bool alive = true;
        while (alive && v < 0 && !st.empty() && st.back() > 0) {
            if (st.back() < -v) st.pop_back();       // top explodes, v keeps going
            else if (st.back() == -v) { st.pop_back(); alive = false; }   // both die
            else alive = false;                      // v explodes
        }
        if (alive) st.push_back(v);
    }
    return st;
}   // O(n) time · O(n) space""",
            "java": r"""// Only a left-mover can be blocked by the stack top
int[] asteroidCollision(int[] a) {
    Deque<Integer> st = new ArrayDeque<>();
    for (int v : a) {
        boolean alive = true;
        while (alive && v < 0 && !st.isEmpty() && st.peek() > 0) {
            if (st.peek() < -v) st.pop();            // top explodes, v keeps going
            else if (st.peek() == -v) { st.pop(); alive = false; }   // both die
            else alive = false;                      // v explodes
        }
        if (alive) st.push(v);
    }
    int[] out = new int[st.size()];
    for (int i = out.length - 1; i >= 0; i--) out[i] = st.pop();
    return out;
}   // O(n) time · O(n) space""",
            "python": r"""def asteroid_collision(a):
    st = []
    for v in a:
        alive = True
        while alive and v < 0 and st and st[-1] > 0:
            if st[-1] < -v:
                st.pop()              # the top explodes, v keeps going
            elif st[-1] == -v:
                st.pop(); alive = False   # both explode
            else:
                alive = False         # v explodes
        if alive:
            st.append(v)
    return st""",
        },
    },
    {
        "slug": "design-circular-queue",
        "title": "Design Circular Queue",
        "difficulty": "Medium",
        "pattern": "ring buffer",
        "statement": "Implement a fixed-capacity queue using a circular buffer with enQueue, deQueue, Front, Rear, isEmpty and isFull.",
        "examples": [("capacity 3: enQueue(1), enQueue(2), enQueue(3)", "all succeed, isFull() = true"),
                     ("enQueue(4)", "fails; Rear() = 3")],
        "constraints": ["1 <= capacity <= 1000", "0 <= values <= 1000", "all operations must be O(1)"],
        "approach": "Keep the array, a head index and a size. The rear position is (head + size) % capacity, and every movement is modulo the "
                     "capacity so the buffer wraps. Using an explicit size avoids the classic full-versus-empty ambiguity of head == tail.",
        "complexity": ("O(1) per op", "O(capacity)"),
        "code": {
            "cpp": r"""// Ring buffer: head index + size, rear derived by modulo
class MyCircularQueue {
    vector<int> buf; int head = 0, sz = 0;
public:
    MyCircularQueue(int k) : buf(k) {}
    bool enQueue(int v) {
        if (sz == (int)buf.size()) return false;
        buf[(head + sz) % buf.size()] = v;           // wrap with modulo
        sz++;
        return true;
    }
    bool deQueue() {
        if (sz == 0) return false;
        head = (head + 1) % buf.size(); sz--;
        return true;
    }
    int Front() { return sz ? buf[head] : -1; }
    int Rear() { return sz ? buf[(head + sz - 1) % buf.size()] : -1; }
    bool isEmpty() { return sz == 0; }
    bool isFull() { return sz == (int)buf.size(); }
};   // O(1) per op · O(capacity) space""",
            "java": r"""// Ring buffer: head index + size, rear derived by modulo
class MyCircularQueue {
    private final int[] buf; private int head = 0, sz = 0;

    public MyCircularQueue(int k) { buf = new int[k]; }
    public boolean enQueue(int v) {
        if (sz == buf.length) return false;
        buf[(head + sz) % buf.length] = v;           // wrap with modulo
        sz++;
        return true;
    }
    public boolean deQueue() {
        if (sz == 0) return false;
        head = (head + 1) % buf.length; sz--;
        return true;
    }
    public int Front() { return sz == 0 ? -1 : buf[head]; }
    public int Rear() { return sz == 0 ? -1 : buf[(head + sz - 1) % buf.length]; }
    public boolean isEmpty() { return sz == 0; }
    public boolean isFull() { return sz == buf.length; }
}   // O(1) per op · O(capacity) space""",
            "python": r"""class MyCircularQueue:
    def __init__(self, k):
        self.buf = [0] * k
        self.head = 0
        self.size = 0               # explicit size: no full/empty ambiguity

    def en_queue(self, v):
        if self.size == len(self.buf):
            return False
        self.buf[(self.head + self.size) % len(self.buf)] = v   # wrap with modulo
        self.size += 1
        return True

    def de_queue(self):
        if self.size == 0:
            return False
        self.head = (self.head + 1) % len(self.buf)
        self.size -= 1
        return True

    def front(self):
        return self.buf[self.head] if self.size else -1

    def rear(self):
        return self.buf[(self.head + self.size - 1) % len(self.buf)] if self.size else -1

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == len(self.buf)""",
        },
    },
    {
        "slug": "minimum-remove-to-make-valid",
        "title": "Minimum Remove to Make Valid Parentheses",
        "difficulty": "Medium",
        "pattern": "stack of unmatched indices",
        "statement": "Remove the minimum number of parentheses so the resulting string is valid, and return any valid result.",
        "examples": [("s = \"lee(t(c)o)de)\"", "\"lee(t(c)o)de\""), ("s = \"a)b(c)d\"", "\"ab(c)d\""), ("s = \"))(  (\"", "\"\""),],
        "constraints": ["1 <= len(s) <= 10^5", "s contains lowercase letters and parentheses", "any minimum valid result is accepted"],
        "approach": "Mark, don't rebuild: record the indices of ')' with no earlier '(' and of '(' that are never closed, then drop exactly those "
                     "positions. Remembering indices instead of characters keeps the rest of the string intact, including letters.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Mark the offending indices, then keep everything else
string minRemoveToMakeValid(string s) {
    vector<int> st;                              // indices of unmatched '('
    unordered_set<int> drop;
    for (int i = 0; i < (int)s.size(); i++) {
        if (s[i] == '(') st.push_back(i);
        else if (s[i] == ')') {
            if (st.empty()) drop.insert(i);      // ')' with nothing to close
            else st.pop_back();
        }
    }
    for (int i : st) drop.insert(i);             // '(' that never closed
    string out;
    for (int i = 0; i < (int)s.size(); i++) if (!drop.count(i)) out += s[i];
    return out;
}   // O(n) time · O(n) space""",
            "java": r"""// Mark the offending indices, then keep everything else
String minRemoveToMakeValid(String s) {
    Deque<Integer> st = new ArrayDeque<>();      // indices of unmatched '('
    Set<Integer> drop = new HashSet<>();
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (c == '(') st.push(i);
        else if (c == ')') {
            if (st.isEmpty()) drop.add(i);       // ')' with nothing to close
            else st.pop();
        }
    }
    while (!st.isEmpty()) drop.add(st.pop());    // '(' that never closed
    StringBuilder out = new StringBuilder();
    for (int i = 0; i < s.length(); i++) if (!drop.contains(i)) out.append(s.charAt(i));
    return out.toString();
}   // O(n) time · O(n) space""",
            "python": r"""def min_remove_to_make_valid(s):
    st, drop = [], set()             # stack of indices of unmatched '('
    for i, c in enumerate(s):
        if c == '(':
            st.append(i)
        elif c == ')':
            if st:
                st.pop()
            else:
                drop.add(i)          # ')' with nothing to close
    drop.update(st)                  # '(' that never closed
    return ''.join(c for i, c in enumerate(s) if i not in drop)""",
        },
    },
    {
        "slug": "sum-of-subarray-minimums",
        "title": "Sum of Subarray Minimums",
        "difficulty": "Medium",
        "pattern": "monotonic stack contribution counting",
        "statement": "Return the sum of min(subarray) over every contiguous subarray, modulo 10^9 + 7.",
        "examples": [("[3,1,2,4]", "17"), ("[11,81,94,43,3]", "444")],
        "constraints": ["1 <= n <= 3 * 10^4", "1 <= values <= 3 * 10^4", "the answer is taken modulo 10^9 + 7"],
        "approach": "Instead of enumerating subarrays, ask how many subarrays have each element as their minimum: that is (choices to the left) × "
                     "(choices to the right), found with previous-strictly-smaller and next-smaller-or-equal boundaries. Breaking ties in one "
                     "direction only is what stops equal values from being counted twice.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Each element counts for (left span) * (right span) subarrays
int sumSubarrayMins(vector<int>& a) {
    const long long MOD = 1000000007;
    int n = a.size();
    vector<int> prev(n), next(n);
    vector<int> st;
    for (int i = 0; i < n; i++) {                       // previous strictly smaller
        while (!st.empty() && a[st.back()] >= a[i]) st.pop_back();
        prev[i] = st.empty() ? i + 1 : i - st.back();
        st.push_back(i);
    }
    st.clear();
    for (int i = n - 1; i >= 0; i--) {                  // next smaller or equal
        while (!st.empty() && a[st.back()] > a[i]) st.pop_back();
        next[i] = st.empty() ? n - i : st.back() - i;
        st.push_back(i);
    }
    long long total = 0;
    for (int i = 0; i < n; i++) total = (total + (long long)a[i] * prev[i] % MOD * next[i]) % MOD;
    return (int)total;
}   // O(n) time · O(n) space""",
            "java": r"""// Each element counts for (left span) * (right span) subarrays
int sumSubarrayMins(int[] a) {
    final long MOD = 1000000007L;
    int n = a.length;
    long[] prev = new long[n], next = new long[n];
    Deque<Integer> st = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {                       // previous strictly smaller
        while (!st.isEmpty() && a[st.peek()] >= a[i]) st.pop();
        prev[i] = st.isEmpty() ? i + 1 : i - st.peek();
        st.push(i);
    }
    st.clear();
    for (int i = n - 1; i >= 0; i--) {                  // next smaller or equal
        while (!st.isEmpty() && a[st.peek()] > a[i]) st.pop();
        next[i] = st.isEmpty() ? n - i : st.peek() - i;
        st.push(i);
    }
    long total = 0;
    for (int i = 0; i < n; i++) total = (total + a[i] * prev[i] % MOD * next[i]) % MOD;
    return (int) total;
}   // O(n) time · O(n) space""",
            "python": r"""def sum_subarray_mins(a):
    MOD = 10**9 + 7
    n = len(a)
    prev, nxt = [0] * n, [0] * n
    st = []
    for i in range(n):                          # previous strictly smaller
        while st and a[st[-1]] >= a[i]:
            st.pop()
        prev[i] = i + 1 if not st else i - st[-1]
        st.append(i)
    st = []
    for i in range(n - 1, -1, -1):              # next smaller or equal
        while st and a[st[-1]] > a[i]:
            st.pop()
        nxt[i] = n - i if not st else st[-1] - i
        st.append(i)
    return sum(a[i] * prev[i] * nxt[i] for i in range(n)) % MOD""",
        },
    },
    {
        "slug": "car-fleet",
        "title": "Car Fleet",
        "difficulty": "Medium",
        "pattern": "sort + stack of arrival times",
        "statement": "Cars drive toward a target on a single-lane road and never pass each other; a faster car catching a slower one joins its "
                     "fleet. Given each car's position and speed, return the number of fleets that arrive at the target.",
        "examples": [("target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]", "3"),
                     ("target = 10, position = [3], speed = [3]", "1")],
        "constraints": ["1 <= n <= 10^5", "0 < speed <= 10^6", "positions are distinct"],
        "approach": "Process the cars from the one nearest the target backwards. A car's arrival time is (target - position) / speed; if that "
                     "time is greater than the fleet ahead it forms a new fleet, otherwise it merges. The times are compared by "
                     "cross-multiplying rather than dividing, so two cars that arrive at exactly the same instant never split a fleet just "
                     "because of floating-point rounding.",
        "complexity": ("O(n log n)", "O(n)"),
        "code": {
            "cpp": r"""// Walk cars from the target backwards; a later arrival is a new fleet
int carFleet(int target, vector<int>& pos, vector<int>& spd) {
    vector<pair<int, int>> cars;                 // (position, speed)
    for (int i = 0; i < (int)pos.size(); i++) cars.push_back({pos[i], spd[i]});
    sort(cars.rbegin(), cars.rend());            // closest to the target first
    int fleets = 0;
    long long lastNum = -1, lastDen = 1;         // arrival time of the fleet ahead
    for (auto& [p, s] : cars) {
        long long num = target - p, den = s;
        if (num * lastDen > lastNum * den) {     // exact compare, no division
            fleets++;
            lastNum = num; lastDen = den;
        }
    }
    return fleets;
}   // O(n log n) time · O(n) space""",
            "java": r"""// Walk cars from the target backwards; a later arrival is a new fleet
int carFleet(int target, int[] pos, int[] spd) {
    Integer[] idx = new Integer[pos.length];
    for (int i = 0; i < idx.length; i++) idx[i] = i;
    Arrays.sort(idx, (x, y) -> pos[y] - pos[x]);        // closest to target first
    int fleets = 0;
    long lastNum = -1, lastDen = 1;                     // arrival time of the fleet ahead
    for (int i : idx) {
        long num = target - pos[i], den = spd[i];
        if (num * lastDen > lastNum * den) {            // exact compare, no division
            fleets++;
            lastNum = num; lastDen = den;
        }
    }
    return fleets;
}   // O(n log n) time · O(n) space""",
            "python": r"""def car_fleet(target, position, speed):
    cars = sorted(zip(position, speed), reverse=True)   # closest to target first
    fleets, last = 0, (-1, 1)                # arrival time of the fleet ahead
    for p, s in cars:
        num, den = target - p, s
        if num * last[1] > last[0] * den:    # exact compare, no division
            fleets += 1
            last = (num, den)
    return fleets""",
        },
    },
    # ------------------------------------------------------------------ HARD
    {
        "slug": "largest-rectangle-in-histogram",
        "title": "Largest Rectangle in Histogram",
        "difficulty": "Hard",
        "pattern": "monotonic stack with sentinel",
        "statement": "Given bar heights of a histogram with unit width, return the area of the largest rectangle contained in it.",
        "examples": [("heights = [2,1,5,6,2,3]", "10"), ("heights = [2,4]", "4")],
        "constraints": ["1 <= n <= 10^5", "0 <= height <= 10^4", "rectangles must be aligned to whole bars"],
        "approach": "A bar's maximal rectangle extends left and right until a strictly shorter bar appears, so it is exactly (next smaller index - "
                     "previous smaller index - 1) wide. Keep a stack of increasing heights: a new shorter bar closes off the bars above it, and a "
                     "sentinel 0 at the end flushes the stack without a second pass.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// A shorter bar closes every taller bar above it
int largestRectangleArea(vector<int>& h) {
    vector<int> st;                              // indices, heights increasing
    int best = 0, n = h.size();
    for (int i = 0; i <= n; i++) {
        int cur = (i == n) ? 0 : h[i];            // sentinel 0 flushes the stack
        while (!st.empty() && h[st.back()] >= cur) {
            int height = h[st.back()]; st.pop_back();
            int left = st.empty() ? -1 : st.back();
            best = max(best, height * (i - left - 1));
        }
        st.push_back(i);
    }
    return best;
}   // O(n) time · O(n) space""",
            "java": r"""// A shorter bar closes every taller bar above it
int largestRectangleArea(int[] h) {
    int n = h.length, best = 0;
    Deque<Integer> st = new ArrayDeque<>();      // indices, heights increasing
    for (int i = 0; i <= n; i++) {
        int cur = (i == n) ? 0 : h[i];           // sentinel 0 flushes the stack
        while (!st.isEmpty() && h[st.peek()] >= cur) {
            int height = h[st.pop()];
            int left = st.isEmpty() ? -1 : st.peek();
            best = Math.max(best, height * (i - left - 1));
        }
        st.push(i);
    }
    return best;
}   // O(n) time · O(n) space""",
            "python": r"""def largest_rectangle_area(h):
    st = []                          # indices with increasing heights
    best = 0
    for i in range(len(h) + 1):
        cur = 0 if i == len(h) else h[i]      # sentinel flushes the stack
        while st and h[st[-1]] >= cur:
            height = h[st.pop()]
            left = st[-1] if st else -1
            best = max(best, height * (i - left - 1))
        st.append(i)
    return best""",
        },
    },
    {
        "slug": "maximal-rectangle",
        "title": "Maximal Rectangle",
        "difficulty": "Hard",
        "pattern": "per-row histogram reuse",
        "statement": "Given a binary matrix, return the area of the largest rectangle made only of '1' cells.",
        "examples": [("matrix = [[\"1\",\"0\",\"1\",\"0\",\"0\"],[\"1\",\"0\",\"1\",\"1\",\"1\"],[\"1\",\"1\",\"1\",\"1\",\"1\"],[\"1\",\"0\",\"0\",\"1\",\"0\"]]", "6"),
                     ("matrix = [[\"0\"]]", "0")],
        "constraints": ["1 <= rows, cols <= 200", "cells are the characters '0' and '1'", "the rectangle is aligned to the grid"],
        "approach": "Read the matrix row by row and maintain a running height per column: extend on '1', reset to 0 on '0'. Every rectangle "
                     "ending at the current row is then a rectangle in some histogram, so the previous problem solves each row in O(cols) and "
                     "the whole matrix in O(rows · cols) — a reusable idea you should recognise.",
        "complexity": ("O(rows · cols)", "O(cols)"),
        "code": {
            "cpp": r"""// Each row turns the grid into a histogram
int maximalRectangle(vector<vector<char>>& m) {
    if (m.empty()) return 0;
    int C = m[0].size(), best = 0;
    vector<int> h(C + 1, 0);                     // extra 0 = sentinel column
    for (const auto& row : m) {
        for (int c = 0; c < C; c++) h[c] = row[c] == '1' ? h[c] + 1 : 0;
        vector<int> st;
        for (int c = 0; c <= C; c++) {
            while (!st.empty() && h[st.back()] >= h[c]) {
                int height = h[st.back()]; st.pop_back();
                int left = st.empty() ? -1 : st.back();
                best = max(best, height * (c - left - 1));
            }
            st.push_back(c);
        }
    }
    return best;
}   // O(rows · cols) time · O(cols) space""",
            "java": r"""// Each row turns the grid into a histogram
int maximalRectangle(char[][] m) {
    if (m.length == 0) return 0;
    int C = m[0].length, best = 0;
    int[] h = new int[C + 1];                    // extra 0 = sentinel column
    for (char[] row : m) {
        for (int c = 0; c < C; c++) h[c] = row[c] == '1' ? h[c] + 1 : 0;
        Deque<Integer> st = new ArrayDeque<>();
        for (int c = 0; c <= C; c++) {
            while (!st.isEmpty() && h[st.peek()] >= h[c]) {
                int height = h[st.pop()];
                int left = st.isEmpty() ? -1 : st.peek();
                best = Math.max(best, height * (c - left - 1));
            }
            st.push(c);
        }
    }
    return best;
}   // O(rows · cols) time · O(cols) space""",
            "python": r"""def maximal_rectangle(m):
    if not m:
        return 0
    C = len(m[0])
    h = [0] * (C + 1)                 # extra 0 = sentinel column
    best = 0
    for row in m:
        for c in range(C):
            h[c] = h[c] + 1 if row[c] == '1' else 0
        st = []
        for c in range(C + 1):
            while st and h[st[-1]] >= h[c]:
                height = h[st.pop()]
                left = st[-1] if st else -1
                best = max(best, height * (c - left - 1))
            st.append(c)
    return best""",
        },
    },
    {
        "slug": "longest-valid-parentheses",
        "title": "Longest Valid Parentheses",
        "difficulty": "Hard",
        "pattern": "stack with a base index",
        "statement": "Given a string of '(' and ')', return the length of the longest substring that is a well-formed parentheses sequence.",
        "examples": [("s = \"(()\"", "2"), ("s = \")()())\"", "4"), ("s = \"\"", "0")],
        "constraints": ["0 <= len(s) <= 3 * 10^4", "s contains only '(' and ')'", "the substring must be contiguous"],
        "approach": "Keep a stack of indices of unmatched '(' plus a base marker for the position just before the current valid run. On a ')', "
                     "pop if possible: if the stack becomes empty the run is broken (push the current index as the new base), otherwise the run "
                     "length is the distance to the index now on top.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Stack of indices plus a "base" marker (-1 initially)
int longestValidParentheses(string s) {
    vector<int> st{-1};                          // base index of the current run
    int best = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        if (s[i] == '(') st.push_back(i);
        else {
            st.pop_back();
            if (st.empty()) st.push_back(i);     // run broken here: new base
            else best = max(best, i - st.back());   // distance to the base
        }
    }
    return best;
}   // O(n) time · O(n) space""",
            "java": r"""// Stack of indices plus a "base" marker (-1 initially)
int longestValidParentheses(String s) {
    Deque<Integer> st = new ArrayDeque<>();
    st.push(-1);                                 // base index of the current run
    int best = 0;
    for (int i = 0; i < s.length(); i++) {
        if (s.charAt(i) == '(') st.push(i);
        else {
            st.pop();
            if (st.isEmpty()) st.push(i);        // run broken here: new base
            else best = Math.max(best, i - st.peek());   // distance to the base
        }
    }
    return best;
}   // O(n) time · O(n) space""",
            "python": r"""def longest_valid_parentheses(s):
    st = [-1]                     # base index of the current run
    best = 0
    for i, c in enumerate(s):
        if c == '(':
            st.append(i)
        else:
            st.pop()
            if not st:
                st.append(i)      # the run is broken here: new base
            else:
                best = max(best, i - st[-1])   # distance to the base
    return best""",
        },
    },
    {
        "slug": "trapping-rain-water-stack",
        "title": "Trapping Rain Water (Stack Version)",
        "difficulty": "Hard",
        "pattern": "monotonic stack of walls",
        "statement": "Given an elevation map, compute how much rainwater it can trap after raining.",
        "examples": [("height = [0,1,0,2,1,0,1,3,2,1,2,1]", "6"), ("height = [4,2,0,3,2,5]", "9")],
        "constraints": ["1 <= n <= 2 * 10^4", "0 <= height <= 10^5", "water is trapped between bars, not above them"],
        "approach": "Keep a decreasing stack of walls. When a taller wall arrives, the bars between it and the wall below it form a basin: the "
                     "water depth is (min of the two walls - the basin floor) times the gap width. Popping the basin floor then lets the same "
                     "space be covered again by a wider basin, which is exactly how the layers stack up.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Each pop is one basin floor between two walls
int trap(vector<int>& h) {
    vector<int> st;                              // indices of walls, decreasing
    int water = 0;
    for (int i = 0; i < (int)h.size(); i++) {
        while (!st.empty() && h[st.back()] < h[i]) {
            int floorIdx = st.back(); st.pop_back();
            if (st.empty()) break;               // no left wall: nothing to trap
            int width = i - st.back() - 1;
            int depth = min(h[i], h[st.back()]) - h[floorIdx];
            water += width * depth;              // the layer above the floor
        }
        st.push_back(i);
    }
    return water;
}   // O(n) time · O(n) space""",
            "java": r"""// Each pop is one basin floor between two walls
int trap(int[] h) {
    Deque<Integer> st = new ArrayDeque<>();      // indices of walls, decreasing
    int water = 0;
    for (int i = 0; i < h.length; i++) {
        while (!st.isEmpty() && h[st.peek()] < h[i]) {
            int floorIdx = st.pop();
            if (st.isEmpty()) break;             // no left wall: nothing to trap
            int width = i - st.peek() - 1;
            int depth = Math.min(h[i], h[st.peek()]) - h[floorIdx];
            water += width * depth;              // the layer above the floor
        }
        st.push(i);
    }
    return water;
}   // O(n) time · O(n) space""",
            "python": r"""def trap(h):
    st = []                          # indices of walls, decreasing heights
    water = 0
    for i, v in enumerate(h):
        while st and h[st[-1]] < v:
            floor_idx = st.pop()
            if not st:
                break                # no left wall: nothing to trap
            width = i - st[-1] - 1
            depth = min(v, h[st[-1]]) - h[floor_idx]
            water += width * depth   # one horizontal layer of water
        st.append(i)
    return water""",
        },
    },
    {
        "slug": "basic-calculator",
        "title": "Basic Calculator",
        "difficulty": "Hard",
        "pattern": "stack for signs across parentheses",
        "statement": "Evaluate an expression containing +, -, non-negative integers and parentheses, and return its value.",
        "examples": [("s = \"1 + 1\"", "2"), ("s = \" 2-1 + 2 \"", "3"), ("s = \"(1+(4+5+2)-3)+(6+8)\"", "23")],
        "constraints": ["1 <= len(s) <= 3 * 10^5", "s has digits, '+', '-', '(', ')' and spaces", "there is no unary minus and no '*' or '/'"],
        "approach": "Scan once, accumulating the current number and sign. On '(' push the running result and the sign that applies to the whole "
                     "bracket, then start counting from zero inside; on ')' fold the bracket's value back into the saved result with the saved "
                     "sign. This is the standard single-pass parser for left-to-right expressions.",
        "complexity": ("O(n)", "O(depth)"),
        "code": {
            "cpp": r"""// One pass: keep a result, a sign, and a stack for '('
int calculate(string s) {
    long long res = 0, num = 0; int sign = 1;
    vector<long long> st;                        // saved results, saved signs
    for (char c : s) {
        if (isdigit(c)) num = num * 10 + (c - '0');
        else if (c == '+' || c == '-') { res += sign * num; num = 0; sign = (c == '+') ? 1 : -1; }
        else if (c == '(') { st.push_back(res); st.push_back(sign); res = 0; sign = 1; }
        else if (c == ')') {
            res += sign * num; num = 0;
            int savedSign = st.back(); st.pop_back();
            long long savedRes = st.back(); st.pop_back();
            res = savedRes + savedSign * res;    // apply the bracket's sign
        }
    }
    return (int)(res + sign * num);
}   // O(n) time · O(depth) space""",
            "java": r"""// One pass: keep a result, a sign, and a stack for '('
int calculate(String s) {
    long res = 0, num = 0; int sign = 1;
    Deque<Long> st = new ArrayDeque<>();         // saved results, saved signs
    for (char c : s.toCharArray()) {
        if (Character.isDigit(c)) num = num * 10 + (c - '0');
        else if (c == '+' || c == '-') { res += sign * num; num = 0; sign = (c == '+') ? 1 : -1; }
        else if (c == '(') { st.push(res); st.push((long) sign); res = 0; sign = 1; }
        else if (c == ')') {
            res += sign * num; num = 0;
            int savedSign = st.pop().intValue();
            long savedRes = st.pop();
            res = savedRes + savedSign * res;    // apply the bracket's sign
        }
    }
    return (int) (res + sign * num);
}   // O(n) time · O(depth) space""",
            "python": r"""def calculate(s):
    res = num = 0
    sign = 1
    stack = []                    # saved results and saved signs
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c in '+-':
            res += sign * num
            num = 0
            sign = 1 if c == '+' else -1
        elif c == '(':
            stack.append(res)
            stack.append(sign)
            res, sign = 0, 1
        elif c == ')':
            res += sign * num
            num = 0
            saved_sign = stack.pop()
            saved_res = stack.pop()
            res = saved_res + saved_sign * res   # apply the bracket's sign
    return res + sign * num""",
        },
    },
    {
        "slug": "parsing-a-boolean-expression",
        "title": "Parsing a Boolean Expression",
        "difficulty": "Hard",
        "pattern": "stack of operators and operands",
        "statement": "Evaluate a boolean expression written as 't', 'f', '!(expr)', '&(expr,...)' or '|(expr,...)' and return true or false.",
        "examples": [("expression = \"!(f)\"", "true"), ("expression = \"|(f,t)\"", "true"),
                     ("expression = \"&(t,f)\"", "false"), ("expression = \"|(&(t,f,t),!(t))\"", "false")],
        "constraints": ["1 <= len(expression) <= 2 * 10^4", "the expression is always valid", "operators take one or more operands"],
        "approach": "Push operator characters and values; when a ')' arrives, pop values back to the matching '(' and apply the operator that "
                     "sits just below it, then push the single result. Reading right-to-left out of the stack is the standard trick for "
                     "variadic operators, and '!' is the one-operand special case.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Push tokens; on ')' apply the operator below the matching '('
bool parseBoolExpr(string e) {
    vector<char> st;
    for (char c : e) {
        if (c == ',') continue;
        if (c == ')') {
            vector<char> vals;
            while (st.back() != '(') { vals.push_back(st.back()); st.pop_back(); }
            st.pop_back();                       // the '('
            char op = st.back(); st.pop_back();  // the operator
            bool r;
            if (op == '!') r = vals[0] == 'f';   // exactly one operand
            else if (op == '&') { r = true; for (char v : vals) r = r && (v == 't'); }
            else { r = false; for (char v : vals) r = r || (v == 't'); }
            st.push_back(r ? 't' : 'f');
        } else st.push_back(c);
    }
    return st.back() == 't';
}   // O(n) time · O(n) space""",
            "java": r"""// Push tokens; on ')' apply the operator below the matching '('
boolean parseBoolExpr(String e) {
    Deque<Character> st = new ArrayDeque<>();
    for (char c : e.toCharArray()) {
        if (c == ',') continue;
        if (c == ')') {
            List<Character> vals = new ArrayList<>();
            while (st.peek() != '(') vals.add(st.pop());
            st.pop();                            // the '('
            char op = st.pop();                  // the operator
            boolean r;
            if (op == '!') r = vals.get(0) == 'f';       // exactly one operand
            else if (op == '&') { r = true; for (char v : vals) r &= (v == 't'); }
            else { r = false; for (char v : vals) r |= (v == 't'); }
            st.push(r ? 't' : 'f');
        } else st.push(c);
    }
    return st.peek() == 't';
}   // O(n) time · O(n) space""",
            "python": r"""def parse_bool_expr(e):
    st = []
    for c in e:
        if c == ',':
            continue
        if c == ')':
            vals = []
            while st[-1] != '(':
                vals.append(st.pop())        # operands, right to left
            st.pop()                         # the '('
            op = st.pop()                    # the operator below it
            if op == '!':                    # exactly one operand
                r = vals[0] == 'f'
            elif op == '&':
                r = all(v == 't' for v in vals)
            else:
                r = any(v == 't' for v in vals)
            st.append('t' if r else 'f')
        else:
            st.append(c)
    return st[-1] == 't'""",
        },
    },
    {
        "slug": "number-of-atoms",
        "title": "Number of Atoms",
        "difficulty": "Hard",
        "pattern": "stack of count maps",
        "statement": "Given a chemical formula (elements, digits, parentheses, possibly nested), return the count of each element as a string "
                     "sorted by element name, omitting counts of 1.",
        "examples": [("formula = \"H2O\"", "\"H2O\""), ("formula = \"K4(ON(SO3)2)2\"", "\"K4N2O14S4\"")],
        "constraints": ["1 <= len(formula) <= 1000", "formula is a valid formula of letters, digits and parentheses", "element symbols start with a capital letter"],
        "approach": "Three jobs, each local: read a name (capital plus following lowercase letters), read a number (default 1), and on '(' push a "
                     "fresh count map while on ')' pop it, multiply by the multiplier after the bracket and merge into the outer map. Sorting keys "
                     "at the end gives the required output order.",
        "complexity": ("O(n + k log k)", "O(k)"),
        "code": {
            "cpp": r"""// Stack of {element -> count}; ')' merges a completed map outward
string countOfAtoms(string f) {
    vector<map<string, int>> st{{{}}};
    int n = f.size();
    for (int i = 0; i < n; ) {
        if (f[i] == '(') { st.push_back({}); i++; }
        else if (f[i] == ')') {
            i++;
            int j = i; while (j < n && isdigit(f[j])) j++;
            int mult = (j > i) ? stoi(f.substr(i, j - i)) : 1;
            i = j;
            auto top = st.back(); st.pop_back();
            for (auto& [el, c] : top) st.back()[el] += c * mult;   // merge outward
        } else {
            int j = i + 1;
            while (j < n && islower(f[j])) j++;
            string el = f.substr(i, j - i);
            int k = j; while (k < n && isdigit(f[k])) k++;
            int mult = (k > j) ? stoi(f.substr(j, k - j)) : 1;
            st.back()[el] += mult;
            i = k;
        }
    }
    string out;
    for (auto& [el, c] : st[0]) out += el + (c > 1 ? to_string(c) : "");
    return out;
}   // O(n + k log k) time · O(k) space""",
            "java": r"""// Stack of {element -> count}; ')' merges a completed map outward
String countOfAtoms(String f) {
    Deque<Map<String, Integer>> st = new ArrayDeque<>();
    st.push(new TreeMap<>());
    int n = f.length();
    for (int i = 0; i < n; ) {
        if (f.charAt(i) == '(') { st.push(new TreeMap<>()); i++; }
        else if (f.charAt(i) == ')') {
            i++;
            int j = i; while (j < n && Character.isDigit(f.charAt(j))) j++;
            int mult = (j > i) ? Integer.parseInt(f.substring(i, j)) : 1;
            i = j;
            Map<String, Integer> top = st.pop();
            for (var e : top.entrySet())                 // merge outward
                st.peek().merge(e.getKey(), e.getValue() * mult, Integer::sum);
        } else {
            int j = i + 1;
            while (j < n && Character.isLowerCase(f.charAt(j))) j++;
            String el = f.substring(i, j);
            int k = j; while (k < n && Character.isDigit(f.charAt(k))) k++;
            int mult = (k > j) ? Integer.parseInt(f.substring(j, k)) : 1;
            st.peek().merge(el, mult, Integer::sum);
            i = k;
        }
    }
    StringBuilder out = new StringBuilder();
    for (var e : st.peek().entrySet())                   // TreeMap: sorted keys
        out.append(e.getKey()).append(e.getValue() > 1 ? String.valueOf(e.getValue()) : "");
    return out.toString();
}   // O(n + k log k) time · O(k) space""",
            "python": r"""def count_of_atoms(formula):
    st = [{}]                        # stack of element -> count maps
    i, n = 0, len(formula)
    while i < n:
        c = formula[i]
        if c == '(':
            st.append({})
            i += 1
        elif c == ')':
            i += 1
            j = i
            while j < n and formula[j].isdigit():
                j += 1
            mult = int(formula[i:j]) if j > i else 1
            i = j
            top = st.pop()
            for el, cnt in top.items():       # merge outward
                st[-1][el] = st[-1].get(el, 0) + cnt * mult
        else:
            j = i + 1
            while j < n and formula[j].islower():
                j += 1                        # element names are Ca, Cl, ...
            name = formula[i:j]
            k = j
            while k < n and formula[k].isdigit():
                k += 1
            mult = int(formula[j:k]) if k > j else 1
            st[-1][name] = st[-1].get(name, 0) + mult
            i = k
    return ''.join(el + (str(c) if c > 1 else '') for el, c in sorted(st[0].items()))""",
        },
    },
    {
        "slug": "minimum-increments-to-form-target",
        "title": "Minimum Increments on Subarrays to Form Target",
        "difficulty": "Hard",
        "pattern": "positive rises in the target",
        "statement": "Starting from an array of zeros, each operation increments every element of one contiguous subarray. Return the minimum "
                     "number of operations needed to reach the given target array.",
        "examples": [("target = [1,2,3,2,1]", "3"), ("target = [3,1,1,2]", "4"), ("target = [3,1,2]", "4")],
        "constraints": ["1 <= n <= 10^5", "1 <= target[i] <= 10^5", "each operation must increment a contiguous subarray"],
        "approach": "Think of the target as layers: the number of layers is the sum of the increases from each position to the next, because a "
                     "rise can only be built by starting a new operation, while a fall just lets existing operations end. Formally the answer is "
                     "target[0] + Σ max(0, target[i] - target[i-1]), the same quantity a monotonic stack would accumulate.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Each rise needs a new layer; each fall ends layers for free
int minNumberOperations(vector<int>& target) {
    long long ops = 0;
    int prev = 0;
    for (int v : target) {
        if (v > prev) ops += v - prev;           // start (v - prev) new operations
        prev = v;                                // falls cost nothing
    }
    return (int)ops;
}   // O(n) time · O(1) space""",
            "java": r"""// Each rise needs a new layer; each fall ends layers for free
int minNumberOperations(int[] target) {
    long ops = 0; int prev = 0;
    for (int v : target) {
        if (v > prev) ops += v - prev;           // start (v - prev) new operations
        prev = v;                                // falls cost nothing
    }
    return (int) ops;
}   // O(n) time · O(1) space""",
            "python": r"""def min_number_operations(target):
    ops = prev = 0
    for v in target:
        if v > prev:
            ops += v - prev    # each rise starts that many new layers
        prev = v               # a fall just lets layers end for free
    return ops""",
        },
    },
    {
        "slug": "number-of-visible-people-in-a-queue",
        "title": "Number of Visible People in a Queue",
        "difficulty": "Hard",
        "pattern": "monotonic stack from the right",
        "statement": "People stand in a queue with given heights. Person i can see person j to their right if everyone strictly between them is "
                     "shorter than both. For each person, count how many others they can see.",
        "examples": [("heights = [10,6,8,5,11,9]", "[3,1,2,1,1,0]"), ("heights = [5,1,2,3,10]", "[4,1,1,1,0]")],
        "constraints": ["1 <= n <= 10^5", "1 <= height <= 10^5", "the answer array has one entry per person"],
        "approach": "Walk from the right, keeping a strictly decreasing stack of heights that are still visible. Every shorter person popped is "
                     "visible (they are in front of nobody taller), and the first person at least as tall is also visible but blocks everyone "
                     "beyond. Popping equals keeps the stack strictly decreasing, which is what makes each person pushed and popped once.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Right-to-left: each popped shorter person is visible, plus one blocker
vector<int> canSeePersonsCount(vector<int>& h) {
    int n = h.size();
    vector<int> ans(n, 0), st;                   // strictly decreasing stack
    for (int i = n - 1; i >= 0; i--) {
        int cnt = 0;
        while (!st.empty() && st.back() < h[i]) { st.pop_back(); cnt++; }  // visible
        if (!st.empty()) cnt++;                  // the first >= h[i] blocker
        while (!st.empty() && st.back() == h[i]) st.pop_back();  // keep strict
        st.push_back(h[i]);
        ans[i] = cnt;
    }
    return ans;
}   // O(n) time · O(n) space""",
            "java": r"""// Right-to-left: each popped shorter person is visible, plus one blocker
int[] canSeePersonsCount(int[] h) {
    int n = h.length;
    int[] ans = new int[n];
    Deque<Integer> st = new ArrayDeque<>();      // strictly decreasing stack
    for (int i = n - 1; i >= 0; i--) {
        int cnt = 0;
        while (!st.isEmpty() && st.peek() < h[i]) { st.pop(); cnt++; }    // visible
        if (!st.isEmpty()) cnt++;                // the first >= h[i] blocker
        while (!st.isEmpty() && st.peek() == h[i]) st.pop();   // keep strict
        st.push(h[i]);
        ans[i] = cnt;
    }
    return ans;
}   // O(n) time · O(n) space""",
            "python": r"""def can_see_persons_count(h):
    n = len(h)
    ans = [0] * n
    st = []                              # strictly decreasing stack
    for i in range(n - 1, -1, -1):
        cnt = 0
        while st and st[-1] < h[i]:
            st.pop()                     # every shorter person is visible
            cnt += 1
        if st:
            cnt += 1                     # the first person at least as tall
        while st and st[-1] == h[i]:
            st.pop()                     # keep the stack strictly decreasing
        st.append(h[i])
        ans[i] = cnt
    return ans""",
        },
    },
    {
        "slug": "create-maximum-number",
        "title": "Create Maximum Number",
        "difficulty": "Hard",
        "pattern": "max subsequence + best merge",
        "statement": "Given two arrays of digits, build the maximum number of length k using elements from both while preserving the relative "
                     "order inside each array, and return it as a list of digits.",
        "examples": [("nums1 = [3,4,6,5], nums2 = [9,1,2,5,8,3], k = 5", "[9,8,6,5,3]"),
                     ("nums1 = [6,7], nums2 = [6,0,4], k = 5", "[6,7,6,0,4]")],
        "constraints": ["1 <= len(nums1), len(nums2) <= 500", "k <= len(nums1) + len(nums2)", "0 <= digits <= 9"],
        "approach": "Split k into t digits taken from nums1 and k-t from nums2. Each side is solved by the 'remove digits to maximise' monotonic "
                     "stack, and merging is greedy: always take from whichever remaining tail is lexicographically larger. Trying every valid t "
                     "and keeping the best overall merge covers all splits.",
        "complexity": ("O(k · (n + m))", "O(k)"),
        "code": {
            "cpp": r"""// For every split: best subsequence from each, then lexicographically best merge
vector<int> maxNumber(vector<int>& a, vector<int>& b, int k) {
    auto take = [](const vector<int>& src, int t) {          // max subsequence of length t
        vector<int> st; int drop = src.size() - t;
        for (int v : src) {
            while (drop > 0 && !st.empty() && st.back() < v) { st.pop_back(); drop--; }
            st.push_back(v);
        }
        st.resize(t);
        return st;
    };
    auto better = [](const vector<int>& x, int i, const vector<int>& y, int j) {
        while (i < (int)x.size() && j < (int)y.size() && x[i] == y[j]) { i++; j++; }
        return j == (int)y.size() || (i < (int)x.size() && x[i] > y[j]);
    };
    vector<int> best;
    for (int t = max(0, k - (int)b.size()); t <= min(k, (int)a.size()); t++) {
        vector<int> A = take(a, t), B = take(b, k - t), merged;
        int i = 0, j = 0;
        while (i < (int)A.size() || j < (int)B.size()) {
            if (better(A, i, B, j)) merged.push_back(A[i++]);
            else merged.push_back(B[j++]);
        }
        if (merged > best) best = merged;
    }
    return best;
}   // O(k · (n + m)) time · O(k) space""",
            "java": r"""// For every split: best subsequence from each, then lexicographically best merge
int[] maxNumber(int[] a, int[] b, int k) {
    int[] best = new int[k];
    for (int t = Math.max(0, k - b.length); t <= Math.min(k, a.length); t++) {
        int[] A = take(a, t), B = take(b, k - t), merged = new int[k];
        int i = 0, j = 0, p = 0;
        while (i < A.length || j < B.length)
            merged[p++] = better(A, i, B, j) ? A[i++] : B[j++];
        if (lexGreater(merged, best)) best = merged;
    }
    return best;
}
private int[] take(int[] src, int t) {                 // max subsequence of length t
    int[] st = new int[t]; int top = 0, drop = src.length - t;
    for (int v : src) {
        while (drop > 0 && top > 0 && st[top - 1] < v) { top--; drop--; }
        if (top < t) st[top++] = v;
    }
    return st;
}
private boolean better(int[] x, int i, int[] y, int j) {
    while (i < x.length && j < y.length && x[i] == y[j]) { i++; j++; }
    return j == y.length || (i < x.length && x[i] > y[j]);
}
private boolean lexGreater(int[] x, int[] y) {
    for (int i = 0; i < x.length; i++) if (x[i] != y[i]) return x[i] > y[i];
    return false;
}
// O(k · (n + m)) time · O(k) space""",
            "python": r"""def max_number(a, b, k):
    def take(src, t):                       # max subsequence of length t
        st, drop = [], len(src) - t
        for v in src:
            while drop and st and st[-1] < v:
                st.pop(); drop -= 1
            st.append(v)
        return st[:t]

    def better(x, i, y, j):                 # is x[i:] lexicographically bigger?
        while i < len(x) and j < len(y) and x[i] == y[j]:
            i += 1; j += 1
        return j == len(y) or (i < len(x) and x[i] > y[j])

    best = []
    for t in range(max(0, k - len(b)), min(k, len(a)) + 1):
        A, B = take(a, t), take(b, k - t)
        merged, i, j = [], 0, 0
        while i < len(A) or j < len(B):
            if better(A, i, B, j):
                merged.append(A[i]); i += 1
            else:
                merged.append(B[j]); j += 1
        if merged > best:
            best = merged
    return best""",
        },
    },
    {
        "slug": "shortest-subarray-with-sum-at-least-k",
        "title": "Shortest Subarray With Sum at Least K",
        "difficulty": "Hard",
        "pattern": "prefix sums + monotonic deque",
        "statement": "Return the length of the shortest non-empty contiguous subarray with sum at least k, or -1 if none exists. Values may be "
                     "negative.",
        "examples": [("[1], k = 1", "1"), ("[1,2], k = 4", "-1"), ("[2,-1,2], k = 3", "3")],
        "constraints": ["1 <= n <= 10^5", "-10^5 <= values <= 10^5", "the subarray must be non-empty"],
        "approach": "Negative values break the usual sliding window, because growing the window can lower the sum. Work with prefix sums instead: "
                     "you need the smallest j - i with pre[j] - pre[i] >= k and i < j. A deque of candidates with increasing prefix sums lets both "
                     "ends be pruned — from the front when a pair already qualifies, from the back when a later prefix is smaller and therefore "
                     "dominates an earlier one.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Prefix sums + deque of increasing candidates
int shortestSubarray(vector<int>& a, int k) {
    int n = a.size();
    vector<long long> pre(n + 1, 0);
    for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + a[i];
    deque<int> dq;                                // indices with increasing prefix
    int best = n + 1;
    for (int i = 0; i <= n; i++) {
        while (!dq.empty() && pre[i] - pre[dq.front()] >= k) {
            best = min(best, i - dq.front());     // a shorter window may follow
            dq.pop_front();
        }
        while (!dq.empty() && pre[dq.back()] >= pre[i]) dq.pop_back();  // dominated
        dq.push_back(i);
    }
    return best == n + 1 ? -1 : best;
}   // O(n) time · O(n) space""",
            "java": r"""// Prefix sums + deque of increasing candidates
int shortestSubarray(int[] a, int k) {
    int n = a.length;
    long[] pre = new long[n + 1];
    for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + a[i];
    Deque<Integer> dq = new ArrayDeque<>();      // indices with increasing prefix
    int best = n + 1;
    for (int i = 0; i <= n; i++) {
        while (!dq.isEmpty() && pre[i] - pre[dq.peekFirst()] >= k) {
            best = Math.min(best, i - dq.pollFirst());   // a shorter window may follow
        }
        while (!dq.isEmpty() && pre[dq.peekLast()] >= pre[i]) dq.pollLast();  // dominated
        dq.addLast(i);
    }
    return best == n + 1 ? -1 : best;
}   // O(n) time · O(n) space""",
            "python": r"""from collections import deque

def shortest_subarray(a, k):
    n = len(a)
    pre = [0] * (n + 1)
    for i, v in enumerate(a):
        pre[i + 1] = pre[i] + v
    dq = deque()                     # indices with increasing prefix sums
    best = n + 1
    for i in range(n + 1):
        while dq and pre[i] - pre[dq[0]] >= k:
            best = min(best, i - dq.popleft())     # a shorter window may follow
        while dq and pre[dq[-1]] >= pre[i]:
            dq.pop()                 # dominated: later and no bigger
        dq.append(i)
    return -1 if best == n + 1 else best""",
        },
    },
    {
        "slug": "maximum-score-of-a-good-subarray",
        "title": "Maximum Score of a Good Subarray",
        "difficulty": "Hard",
        "pattern": "expand outward from k",
        "statement": "A subarray is good if it contains index k. Its score is (minimum of the subarray) × (its length). Return the maximum score "
                     "over good subarrays.",
        "examples": [("nums = [1,4,3,7,4,5], k = 3", "15"), ("nums = [5,5,4,5,4,1,1,5], k = 0", "20")],
        "constraints": ["1 <= n <= 10^5", "1 <= values <= 2 * 10^4", "index k is 0-based"],
        "approach": "Start with the single-element window at k and grow it one step at a time toward the larger of the two neighbours. Taking the "
                     "bigger neighbour first is what lets the minimum fall as slowly as possible; the running minimum and the window width give a "
                     "candidate score at every step, and the maximum over those O(n) candidates is the answer.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Grow the window from k, always toward the larger neighbour
int maximumScore(vector<int>& a, int k) {
    int l = k, r = k, n = a.size();
    int curMin = a[k], best = a[k];
    while (l > 0 || r < n - 1) {
        if (r == n - 1 || (l > 0 && a[l - 1] > a[r + 1])) curMin = min(curMin, a[--l]);
        else curMin = min(curMin, a[++r]);           // take the bigger side
        best = max(best, curMin * (r - l + 1));
    }
    return best;
}   // O(n) time · O(1) space""",
            "java": r"""// Grow the window from k, always toward the larger neighbour
int maximumScore(int[] a, int k) {
    int l = k, r = k, n = a.length;
    int curMin = a[k], best = a[k];
    while (l > 0 || r < n - 1) {
        if (r == n - 1 || (l > 0 && a[l - 1] > a[r + 1])) curMin = Math.min(curMin, a[--l]);
        else curMin = Math.min(curMin, a[++r]);      // take the bigger side
        best = Math.max(best, curMin * (r - l + 1));
    }
    return best;
}   // O(n) time · O(1) space""",
            "python": r"""def maximum_score(a, k):
    l = r = k
    cur_min = best = a[k]
    while l > 0 or r < len(a) - 1:
        if r == len(a) - 1 or (l > 0 and a[l - 1] > a[r + 1]):
            l -= 1                   # take the bigger neighbour first
        else:
            r += 1
        cur_min = min(cur_min, a[l], a[r])
        best = max(best, cur_min * (r - l + 1))
    return best""",
        },
    },
]
