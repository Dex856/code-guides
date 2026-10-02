# Topic 11 · Heaps, Top-K & Design
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.

TOPIC = {
    "name": "Heaps, Top-K & Design",
    "tagline": "A heap is a promise about one end of a collection — pay log n to keep the extreme element cheap.",
    "focus": "Three shapes cover the topic. Top-K keeps a heap of exactly k elements and discards the weakest, so the extra cost stays logarithmic "
             "in k rather than in n. Merge/sweep keeps one heap per source and always pops the global extreme. Design problems keep two heaps or a "
             "heap plus an index, which is how a stream answers median and ranking questions. The hard tier adds laziness — deleted entries stay in "
             "the heap and are skipped when they surface.",
    "ordering": "easy 1–4 are single-heap simulations and top-K shepherds, 5–6 add a second structure (sorting, two stacks); medium 1–5 are the "
                "Top-K family and the heap-greedy strings, 6–9 are scheduling sweeps with deadlines, 10–12 are heap-backed designs; hard 1–3 are "
                "two-heap median structures, 4–6 are sweep-line and k-way merge problems, 7–9 combine heaps with windows or prefix sums, 10–12 are "
                "the largest designs, where the data structure itself is the answer.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "last-stone-weight",
        "title": "Last Stone Weight",
        "difficulty": "Easy",
        "pattern": "max-heap simulation",
        "statement": "Repeatedly take the two heaviest stones; if they differ, the difference goes back into the pile. Return the weight of the last "
                     "stone, or 0 if none is left.",
        "examples": [("stones = [2,7,4,1,8,1]", "1"), ("stones = [1]", "1")],
        "constraints": ["1 <= stones.length <= 30", "1 <= stones[i] <= 1000", "at most one new stone appears per smash"],
        "approach": "The rule always asks for the two heaviest, which is exactly what a max-heap gives cheaply: pop twice, push the difference if it "
                     "is positive, and repeat until at most one stone remains. A sorted list would re-sort on every insertion.",
        "complexity": ("O(n log n)", "O(n)"),
        "code": {
            "cpp": r"""// Always smash the two heaviest: a max-heap supplies them
int lastStoneWeight(vector<int>& stones) {
    priority_queue<int> pq(stones.begin(), stones.end());
    while (pq.size() > 1) {
        int a = pq.top(); pq.pop();              // heaviest
        int b = pq.top(); pq.pop();              // second heaviest
        if (a != b) pq.push(a - b);              // the difference survives
    }
    return pq.empty() ? 0 : pq.top();
}   // O(n log n) time · O(n) space""",
            "java": r"""// Always smash the two heaviest: a max-heap supplies them
int lastStoneWeight(int[] stones) {
    PriorityQueue<Integer> pq = new PriorityQueue<>(Collections.reverseOrder());
    for (int s : stones) pq.add(s);
    while (pq.size() > 1) {
        int a = pq.poll();                       // heaviest
        int b = pq.poll();                       // second heaviest
        if (a != b) pq.add(a - b);               // the difference survives
    }
    return pq.isEmpty() ? 0 : pq.peek();
}   // O(n log n) time · O(n) space""",
            "python": r"""import heapq

def last_stone_weight(stones):
    heap = [-s for s in stones]        # negate for a max-heap
    heapq.heapify(heap)
    while len(heap) > 1:
        a = -heapq.heappop(heap)       # heaviest
        b = -heapq.heappop(heap)       # second heaviest
        if a != b:
            heapq.heappush(heap, -(a - b))   # the difference survives
    return -heap[0] if heap else 0""",
        },
    },
    {
        "slug": "kth-largest-element-in-a-stream",
        "title": "Kth Largest Element in a Stream",
        "difficulty": "Easy",
        "pattern": "bounded min-heap (design)",
        "statement": "Design a class that is initialised with a list and a number k, and answers, after each added value, the k-th largest value "
                     "seen so far.",
        "examples": [("k = 3, nums = [4,5,8,2]: [\"KthLargest\",\"add\",\"add\",\"add\",\"add\",\"add\"] [[3,[4,5,8,2]],[3],[5],[10],[9],[4]]",
                      "[null, 4, 5, 5, 8, 8]"),
                     ("k = 4, nums = [7,7,7,7,8,3]: [\"KthLargest\",\"add\",\"add\",\"add\",\"add\"] [[4,[7,7,7,7,8,3]],[2],[10],[9],[9]]",
                      "[null, 7, 7, 7, 8]")],
        "constraints": ["1 <= k <= 10^4", "0 <= nums.length <= 10^4", "-10^4 <= values <= 10^4"],
        "approach": "Keep only the k largest values seen so far in a min-heap. Its root is then the smallest of them — which is exactly the k-th "
                     "largest overall — and an incoming value either replaces the root or is discarded immediately.",
        "complexity": ("O(log k) per add", "O(k)"),
        "code": {
            "cpp": r"""// A min-heap of the k largest values: its root is the answer
class KthLargest {
public:
    priority_queue<int, vector<int>, greater<int>> small;   // smallest on top
    int k;
    KthLargest(int k, vector<int>& nums) : k(k) {
        for (int x : nums) add(x);
    }
    int add(int val) {
        small.push(val);
        if ((int)small.size() > k) small.pop();   // drop the least useful value
        return small.top();                       // the k-th largest
    }
};   // O(log k) per add · O(k) space""",
            "java": r"""// A min-heap of the k largest values: its root is the answer
class KthLargest {
    PriorityQueue<Integer> small = new PriorityQueue<>();    // smallest on top
    int k;
    KthLargest(int k, int[] nums) {
        this.k = k;
        for (int x : nums) add(x);
    }
    int add(int val) {
        small.add(val);
        if (small.size() > k) small.poll();       // drop the least useful value
        return small.peek();                      // the k-th largest
    }
}   // O(log k) per add · O(k) space""",
            "python": r"""import heapq

class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.small = []                # min-heap of the k largest values so far
        for x in nums:
            self.add(x)

    def add(self, val):
        heapq.heappush(self.small, val)
        if len(self.small) > self.k:
            heapq.heappop(self.small)  # drop the least useful value
        return self.small[0]           # the k-th largest seen so far""",
        },
    },
    {
        "slug": "take-gifts-from-the-richest-pile",
        "title": "Take Gifts From the Richest Pile",
        "difficulty": "Easy",
        "pattern": "max-heap with a shrinking value",
        "statement": "For k seconds, replace the largest pile by the integer square root of its size. Return the total left afterwards.",
        "examples": [("gifts = [25,64,9,4,100], k = 4", "29"), ("gifts = [1,1,1,1], k = 4", "4")],
        "constraints": ["1 <= gifts.length <= 10^3", "1 <= gifts[i] <= 10^9", "1 <= k <= 10^3"],
        "approach": "Each second acts on the current maximum, so a max-heap keeps that lookup to O(log n). Pop the largest, push back its square root, "
                     "and repeat k times; the remaining sum is the answer.",
        "complexity": ("O((n + k) log n)", "O(n)"),
        "code": {
            "cpp": r"""// Pop the largest, push back its square root, k times
long long pickGifts(vector<int>& gifts, int k) {
    priority_queue<int> pq(gifts.begin(), gifts.end());
    while (k-- > 0) {
        int biggest = pq.top(); pq.pop();
        pq.push((int) sqrt(biggest));            // integer square root
    }
    long long total = 0;
    while (!pq.empty()) { total += pq.top(); pq.pop(); }
    return total;
}   // O((n + k) log n) time · O(n) space""",
            "java": r"""// Pop the largest, push back its square root, k times
long pickGifts(int[] gifts, int k) {
    PriorityQueue<Integer> pq = new PriorityQueue<>(Collections.reverseOrder());
    for (int g : gifts) pq.add(g);
    while (k-- > 0) {
        int biggest = pq.poll();
        pq.add((int) Math.sqrt(biggest));        // integer square root
    }
    long total = 0;
    while (!pq.isEmpty()) total += pq.poll();
    return total;
}   // O((n + k) log n) time · O(n) space""",
            "python": r"""import heapq
import math

def pick_gifts(gifts, k):
    heap = [-g for g in gifts]
    heapq.heapify(heap)
    for _ in range(k):
        biggest = -heapq.heappop(heap)
        heapq.heappush(heap, -math.isqrt(biggest))   # integer square root
    return -sum(heap)""",
        },
    },
    {
        "slug": "maximum-product-of-two-elements-in-an-array",
        "title": "Maximum Product of Two Elements",
        "difficulty": "Easy",
        "pattern": "top-two selection",
        "statement": "Pick two different indices and return (nums[i] - 1) * (nums[j] - 1) as large as possible.",
        "examples": [("nums = [3,4,5,2]", "12"), ("nums = [1,5,4,5]", "16"), ("nums = [3,7]", "12")],
        "constraints": ["2 <= nums.length <= 500", "1 <= nums[i] <= 10^3", "the two indices must differ"],
        "approach": "Only the two largest values matter, since subtracting 1 preserves order. This is the smallest version of the top-K pattern: a "
                     "single heap of size two, or just two running maxima, makes the scan linear.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Only the two largest values matter; keep them as running maxima
int maxProduct(vector<int>& nums) {
    int first = 0, second = 0;                   // the two best values so far
    for (int x : nums) {
        if (x > first) { second = first; first = x; }
        else if (x > second) second = x;
    }
    return (first - 1) * (second - 1);
}   // O(n) time · O(1) space""",
            "java": r"""// Only the two largest values matter; keep them as running maxima
int maxProduct(int[] nums) {
    int first = 0, second = 0;                   // the two best values so far
    for (int x : nums) {
        if (x > first) { second = first; first = x; }
        else if (x > second) second = x;
    }
    return (first - 1) * (second - 1);
}   // O(n) time · O(1) space""",
            "python": r"""def max_product_two(nums):
    first = second = 0               # the two largest values so far
    for x in nums:
        if x > first:
            first, second = x, first
        elif x > second:
            second = x
    return (first - 1) * (second - 1)""",
        },
    },
    {
        "slug": "the-k-weakest-rows-in-a-matrix",
        "title": "The K Weakest Rows in a Matrix",
        "difficulty": "Easy",
        "pattern": "rank rows by a pair key",
        "statement": "Each row of 0s and 1s has its 1s first. Return the indices of the k weakest rows, where weaker means fewer 1s, ties broken by "
                     "the smaller row index.",
        "examples": [("mat = [[1,1,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,1,0,0,0],[1,1,1,1,1]], k = 3", "[2,0,3]"),
                     ("mat = [[1,0,0,0],[1,1,1,1],[1,0,0,0],[1,0,0,0]], k = 2", "[0,2]")],
        "constraints": ["2 <= rows, cols <= 100", "matrix entries are 0 or 1, sorted in each row", "1 <= k <= number of rows"],
        "approach": "The strength of a row is just its count of ones, and because each row is sorted that count is a binary search. Ranking by the "
                     "pair (strength, index) gives the required tie-break; a heap of size k or a full sort both work at these sizes.",
        "complexity": ("O(rows log cols + rows log k)", "O(k)"),
        "code": {
            "cpp": r"""// Strength is the number of ones; rank by (strength, row index)
vector<int> kWeakestRows(vector<vector<int>>& mat, int k) {
    vector<pair<int,int>> rows;                  // (soldiers, row index)
    for (int i = 0; i < (int)mat.size(); i++) {
        // rows are sorted, so count by binary search: first 0 minus first 1
        int lo = 0, hi = mat[i].size();
        while (lo < hi) { int mid = (lo + hi) / 2; if (mat[i][mid]) lo = mid + 1; else hi = mid; }
        rows.push_back({lo, i});
    }
    sort(rows.begin(), rows.end());              // ties broken by the index
    vector<int> out;
    for (int i = 0; i < k; i++) out.push_back(rows[i].second);
    return out;
}   // O(rows log cols + rows log rows) time · O(rows) space""",
            "java": r"""// Strength is the number of ones; rank by (strength, row index)
int[] kWeakestRows(int[][] mat, int k) {
    int[][] rows = new int[mat.length][2];       // {soldiers, row index}
    for (int i = 0; i < mat.length; i++) {
        int lo = 0, hi = mat[i].length;
        while (lo < hi) { int mid = (lo + hi) / 2; if (mat[i][mid] == 1) lo = mid + 1; else hi = mid; }
        rows[i] = new int[]{lo, i};
    }
    Arrays.sort(rows, (a, b) -> a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]);
    int[] out = new int[k];
    for (int i = 0; i < k; i++) out[i] = rows[i][1];
    return out;
}   // O(rows log cols + rows log rows) time · O(rows) space""",
            "python": r"""def k_weakest_rows(mat, k):
    rows = []
    for i, row in enumerate(mat):
        lo, hi = 0, len(row)              # find the first 0 (rows are 1s then 0s)
        while lo < hi:
            mid = (lo + hi) // 2
            if row[mid] == 1:
                lo = mid + 1
            else:
                hi = mid
        rows.append((lo, i))              # soldiers, then index for the tie-break
    rows.sort()
    return [i for _, i in rows[:k]]""",
        },
    },
    {
        "slug": "implement-queue-using-stacks",
        "title": "Implement Queue using Stacks",
        "difficulty": "Easy",
        "pattern": "two stacks with a lazy transfer",
        "statement": "Implement a queue with only stack operations: push, peek, pop and empty.",
        "examples": [("[\"MyQueue\",\"push\",\"push\",\"peek\",\"pop\",\"empty\"] [[],[1],[2],[],[],[]]", "[null, null, null, 1, 1, false]")],
        "constraints": ["1 <= number of calls <= 100", "1 <= values <= 9", "only standard stack operations may be used"],
        "approach": "One stack receives pushes, the other serves pops. Moving elements across only when the serving stack is empty reverses them twice "
                     "in total, which gives each element an amortised constant cost even though a single transfer looks linear.",
        "complexity": ("O(1) amortised per operation", "O(n)"),
        "code": {
            "cpp": r"""// in receives pushes; out serves pops, refilled only when empty
class MyQueue {
public:
    stack<int> in, out;
    void push(int x) { in.push(x); }
    void transfer() {
        if (out.empty()) while (!in.empty()) { out.push(in.top()); in.pop(); }
    }
    int pop() { transfer(); int x = out.top(); out.pop(); return x; }
    int peek() { transfer(); return out.top(); }
    bool empty() { return in.empty() && out.empty(); }
};   // O(1) amortised per operation · O(n) space""",
            "java": r"""// in receives pushes; out serves pops, refilled only when empty
class MyQueue {
    Deque<Integer> in = new ArrayDeque<>(), out = new ArrayDeque<>();
    void push(int x) { in.push(x); }
    void transfer() {
        if (out.isEmpty()) while (!in.isEmpty()) out.push(in.pop());
    }
    int pop() { transfer(); return out.pop(); }
    int peek() { transfer(); return out.peek(); }
    boolean empty() { return in.isEmpty() && out.isEmpty(); }
}   // O(1) amortised per operation · O(n) space""",
            "python": r"""class MyQueue:
    def __init__(self):
        self.inbox = []            # receives pushes
        self.outbox = []           # serves pops, refilled only when empty

    def push(self, x):
        self.inbox.append(x)

    def _transfer(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())   # reversed once

    def pop(self):
        self._transfer()
        return self.outbox.pop()

    def peek(self):
        self._transfer()
        return self.outbox[-1]

    def empty(self):
        return not self.inbox and not self.outbox""",
        },
    },
    # ---------------------------------------------------------------- MEDIUM
    {
        "slug": "kth-largest-element-in-an-array",
        "title": "Kth Largest Element in an Array",
        "difficulty": "Medium",
        "pattern": "bounded min-heap or quickselect",
        "statement": "Return the k-th largest element of an unsorted array.",
        "examples": [("nums = [3,2,1,5,6,4], k = 2", "5"), ("nums = [3,2,3,1,2,4,5,5,6], k = 4", "4")],
        "constraints": ["1 <= k <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4", "counting-sort sizes are allowed"],
        "approach": "The heap route keeps at most k values, so the cost depends on k rather than n; quickselect partitions instead and skips the half "
                     "that cannot contain the answer, averaging linear time. Both are standard answers and the choice is a trade of worst-case safety "
                     "against average speed.",
        "complexity": ("O(n log k) heap, O(n) average quickselect", "O(k) or O(1)"),
        "code": {
            "cpp": r"""// Keep the k largest in a min-heap; its root is the answer
int findKthLargest(vector<int>& nums, int k) {
    priority_queue<int, vector<int>, greater<int>> heap;   // smallest on top
    for (int x : nums) {
        heap.push(x);
        if ((int)heap.size() > k) heap.pop();    // discard the weakest
    }
    return heap.top();
}   // O(n log k) time · O(k) space""",
            "java": r"""// Keep the k largest in a min-heap; its root is the answer
int findKthLargest(int[] nums, int k) {
    PriorityQueue<Integer> heap = new PriorityQueue<>();   // smallest on top
    for (int x : nums) {
        heap.add(x);
        if (heap.size() > k) heap.poll();        // discard the weakest
    }
    return heap.peek();
}   // O(n log k) time · O(k) space""",
            "python": r"""import heapq

def find_kth_largest(nums, k):
    heap = []                        # min-heap holding the k largest values
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)      # discard the weakest
    return heap[0]""",
        },
    },
    {
        "slug": "k-closest-points-to-origin",
        "title": "K Closest Points to Origin",
        "difficulty": "Medium",
        "pattern": "bounded max-heap on a distance key",
        "statement": "Return the k points closest to (0, 0), in any order.",
        "examples": [("points = [[1,3],[-2,2]], k = 1", "[[-2,2]]"), ("points = [[3,3],[5,-1],[-2,4]], k = 2", "[[3,3],[-2,4]]")],
        "constraints": ["1 <= k <= points.length <= 10^4", "-10^4 <= coordinates <= 10^4", "no square roots are needed"],
        "approach": "Distance comparisons only need squared distances, which avoids floating point entirely. Mirroring the k-th largest pattern, keep "
                     "a max-heap of the k nearest candidates and evict the farthest whenever it overflows.",
        "complexity": ("O(n log k)", "O(k)"),
        "code": {
            "cpp": r"""// Squared distances avoid floating point; evict the farthest
vector<vector<int>> kClosest(vector<vector<int>>& points, int k) {
    priority_queue<pair<int,int>> heap;          // (sq distance, index), farthest on top
    for (int i = 0; i < (int)points.size(); i++) {
        int d = points[i][0] * points[i][0] + points[i][1] * points[i][1];
        heap.push({d, i});
        if ((int)heap.size() > k) heap.pop();    // drop the farthest candidate
    }
    vector<vector<int>> out;
    while (!heap.empty()) { out.push_back(points[heap.top().second]); heap.pop(); }
    return out;
}   // O(n log k) time · O(k) space""",
            "java": r"""// Squared distances avoid floating point; evict the farthest
int[][] kClosest(int[][] points, int k) {
    PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> b[0] - a[0]);   // farthest first
    for (int i = 0; i < points.length; i++) {
        int d = points[i][0] * points[i][0] + points[i][1] * points[i][1];
        heap.add(new int[]{d, i});
        if (heap.size() > k) heap.poll();        // drop the farthest candidate
    }
    int[][] out = new int[k][];
    for (int i = 0; i < k; i++) out[i] = points[heap.poll()[1]];
    return out;
}   // O(n log k) time · O(k) space""",
            "python": r"""import heapq

def k_closest(points, k):
    heap = []                        # max-heap of (-squared distance, point)
    for x, y in points:
        d = x * x + y * y            # squared distance: no square roots
        heapq.heappush(heap, (-d, x, y))
        if len(heap) > k:
            heapq.heappop(heap)      # drop the farthest candidate
    return [[x, y] for _, x, y in heap]""",
        },
    },
    {
        "slug": "reorganize-string",
        "title": "Reorganize String",
        "difficulty": "Medium",
        "pattern": "most frequent first with a hold-back slot",
        "statement": "Rearrange the characters so that no two adjacent characters are equal. Return any valid arrangement, or the empty string if none "
                     "exists.",
        "examples": [("s = \"aab\"", "\"aba\""), ("s = \"aaab\"", "\"\"")],
        "constraints": ["1 <= s.length <= 500", "s contains lowercase letters", "adjacent characters must differ"],
        "approach": "Placing the most frequent remaining character first is safe as long as it is not the one just used. Holding the previous "
                     "character out of the heap for one step is exactly the constraint, and if the heap is empty while characters remain, the answer "
                     "is impossible.",
        "complexity": ("O(n log 26)", "O(26)"),
        "code": {
            "cpp": r"""// Most frequent first; hold the previous character out for one step
string reorganizeString(string s) {
    int counts[26] = {0};
    for (char c : s) counts[c - 'a']++;
    priority_queue<pair<int,char>> pq;           // (remaining, character)
    for (int c = 0; c < 26; c++) if (counts[c]) pq.push({counts[c], (char)('a' + c)});
    string out;
    int heldCount = 0; char heldChar = 0;        // the character used last
    while (!pq.empty()) {
        auto [cnt, ch] = pq.top(); pq.pop();     // never the character just used
        out += ch;
        if (heldCount > 0) pq.push({heldCount, heldChar});   // it may come back now
        heldCount = cnt - 1;                     // and it must wait one step
        heldChar = ch;
    }
    return (int)out.size() == (int)s.size() ? out : "";
}   // O(n log 26) time · O(26) space""",
            "java": r"""// Most frequent first; hold the previous character out for one step
String reorganizeString(String s) {
    int[] counts = new int[26];
    for (int i = 0; i < s.length(); i++) counts[s.charAt(i) - 'a']++;
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> b[0] - a[0]);
    for (int c = 0; c < 26; c++) if (counts[c] > 0) pq.add(new int[]{counts[c], c});
    StringBuilder out = new StringBuilder();
    int heldCount = 0, heldChar = 0;             // the character used last
    while (!pq.isEmpty()) {
        int[] cur = pq.poll();                   // never the character just used
        out.append((char) ('a' + cur[1]));
        if (heldCount > 0) pq.add(new int[]{heldCount, heldChar});   // may come back now
        heldCount = cur[0] - 1;                  // and it must wait one step
        heldChar = cur[1];
    }
    return out.length() == s.length() ? out.toString() : "";
}   // O(n log 26) time · O(26) space""",
            "python": r"""import heapq
from collections import Counter

def reorganize_string(s):
    heap = [(-c, ch) for ch, c in Counter(s).items()]
    heapq.heapify(heap)
    out = []
    held_count, held_char = 0, ''           # the character used last
    while heap:
        neg, ch = heapq.heappop(heap)       # never the character just used
        out.append(ch)
        if held_count > 0:
            heapq.heappush(heap, (-held_count, held_char))   # it may come back now
        held_count, held_char = -neg - 1, ch    # and it must wait one step
    return ''.join(out) if len(out) == len(s) else ''""",
        },
    },
    {
        "slug": "longest-happy-string",
        "title": "Longest Happy String",
        "difficulty": "Medium",
        "pattern": "greedy with two-character hold-back",
        "statement": "Build the longest string of a, b and c that uses the given counts, contains no 'aaa', 'bbb' or 'ccc', and uses at most the given "
                     "number of each letter.",
        "examples": [("a = 1, b = 1, c = 7", "ccaccbcc"), ("a = 7, b = 1, c = 0", "aabaa")],
        "constraints": ["0 <= a, b, c <= 100", "at least one count is positive", "no letter may appear three times in a row"],
        "approach": "Always append the most plentiful letter that does not create a triple. If the top of the heap would form a triple, take the "
                     "second instead — that swap is the whole algorithm, and it fails only when no letter is left to break the run.",
        "complexity": ("O((a + b + c) log 3)", "O(1)"),
        "code": {
            "cpp": r"""// Append the most plentiful letter that does not make a triple
string longestDiverseString(int a, int b, int c) {
    priority_queue<pair<int,char>> pq;
    if (a) pq.push({a, 'a'});
    if (b) pq.push({b, 'b'});
    if (c) pq.push({c, 'c'});
    string out;
    while (!pq.empty()) {
        auto [cnt, ch] = pq.top(); pq.pop();
        int n = out.size();
        if (n >= 2 && out[n-1] == ch && out[n-2] == ch) {   // this would make a triple
            if (pq.empty()) break;                          // nothing else to use
            auto [cnt2, ch2] = pq.top(); pq.pop();          // take the runner-up
            out += ch2;
            if (--cnt2 > 0) pq.push({cnt2, ch2});
            pq.push({cnt, ch});                             // the leader stays
        } else {
            out += ch;
            if (--cnt > 0) pq.push({cnt, ch});
        }
    }
    return out;
}   // O((a + b + c) log 3) time · O(1) space""",
            "java": r"""// Append the most plentiful letter that does not make a triple
String longestDiverseString(int a, int b, int c) {
    PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> y[0] - x[0]);   // {count, letter}
    if (a > 0) pq.add(new int[]{a, 'a'});
    if (b > 0) pq.add(new int[]{b, 'b'});
    if (c > 0) pq.add(new int[]{c, 'c'});
    StringBuilder out = new StringBuilder();
    while (!pq.isEmpty()) {
        int[] top = pq.poll();
        int n = out.length();
        if (n >= 2 && out.charAt(n-1) == top[1] && out.charAt(n-2) == top[1]) {
            if (pq.isEmpty()) break;             // nothing else can break the run
            int[] second = pq.poll();            // take the runner-up instead
            out.append((char) second[1]);
            if (--second[0] > 0) pq.add(second);
            pq.add(top);                         // the leader stays available
        } else {
            out.append((char) top[1]);
            if (--top[0] > 0) pq.add(top);
        }
    }
    return out.toString();
}   // O((a + b + c) log 3) time · O(1) space""",
            "python": r"""import heapq

def longest_diverse_string(a, b, c):
    heap = [(-n, ch) for n, ch in ((a, 'a'), (b, 'b'), (c, 'c')) if n > 0]
    heapq.heapify(heap)
    out = []
    while heap:
        cnt, ch = heapq.heappop(heap)
        cnt = -cnt
        if len(out) >= 2 and out[-1] == ch and out[-2] == ch:
            if not heap:
                break                      # nothing else can break the run
            cnt2, ch2 = heapq.heappop(heap)
            cnt2 = -cnt2
            out.append(ch2)
            if cnt2 - 1 > 0:
                heapq.heappush(heap, (-(cnt2 - 1), ch2))
            heapq.heappush(heap, (-cnt, ch))       # the leader stays available
        else:
            out.append(ch)
            if cnt - 1 > 0:
                heapq.heappush(heap, (-(cnt - 1), ch))
    return ''.join(out)""",
        },
    },
    {
        "slug": "furthest-building-you-can-reach",
        "title": "Furthest Building You Can Reach",
        "difficulty": "Medium",
        "pattern": "ladder/brick trade with a heap",
        "statement": "Move between buildings in order: a rise costs either one ladder or that many bricks, while a fall is free. With a fixed number of "
                     "ladders and bricks, return the furthest index reachable.",
        "examples": [("heights = [4,2,7,6,9,14,12], bricks = 5, ladders = 1", "4"),
                     ("heights = [4,12,2,7,3,18,20,3,19], bricks = 10, ladders = 2", "7"),
                     ("heights = [14,3,19,3], bricks = 17, ladders = 0", "3")],
        "constraints": ["1 <= heights.length <= 10^5", "0 <= bricks <= 10^9", "0 <= ladders <= heights.length"],
        "approach": "Ladders should be spent on the *largest* climbs, so collect every positive climb in a min-heap and let it hold the climbs "
                     "currently assigned to ladders. When a new climb arrives, the smaller of the pair takes bricks and the larger takes a ladder, "
                     "which keeps the ladder assignment optimal as you advance.",
        "complexity": ("O(n log ladders)", "O(ladders)"),
        "code": {
            "cpp": r"""// Ladders pay for the biggest climbs: keep those in a min-heap
int furthestBuilding(vector<int>& heights, int bricks, int ladders) {
    priority_queue<int, vector<int>, greater<int>> laddered;   // climbs on ladders
    for (int i = 0; i + 1 < (int)heights.size(); i++) {
        int climb = heights[i+1] - heights[i];
        if (climb <= 0) continue;                // going down is free
        laddered.push(climb);
        if ((int)laddered.size() > ladders) {    // too many ladder climbs
            bricks -= laddered.top();            // the smallest one takes bricks
            laddered.pop();
            if (bricks < 0) return i;            // out of bricks: stop here
        }
    }
    return heights.size() - 1;
}   // O(n log ladders) time · O(ladders) space""",
            "java": r"""// Ladders pay for the biggest climbs: keep those in a min-heap
int furthestBuilding(int[] heights, int bricks, int ladders) {
    PriorityQueue<Integer> laddered = new PriorityQueue<>();   // climbs on ladders
    for (int i = 0; i + 1 < heights.length; i++) {
        int climb = heights[i+1] - heights[i];
        if (climb <= 0) continue;                // going down is free
        laddered.add(climb);
        if (laddered.size() > ladders) {         // too many ladder climbs
            bricks -= laddered.poll();           // the smallest one takes bricks
            if (bricks < 0) return i;            // out of bricks: stop here
        }
    }
    return heights.length - 1;
}   // O(n log ladders) time · O(ladders) space""",
            "python": r"""import heapq

def furthest_building(heights, bricks, ladders):
    laddered = []                    # climbs currently paid for by ladders
    for i in range(len(heights) - 1):
        climb = heights[i+1] - heights[i]
        if climb <= 0:
            continue                 # going down is free
        heapq.heappush(laddered, climb)
        if len(laddered) > ladders:  # too many climbs claim a ladder
            bricks -= heapq.heappop(laddered)   # the smallest falls to bricks
            if bricks < 0:
                return i             # out of bricks: this is the last reachable
    return len(heights) - 1""",
        },
    },
    {
        "slug": "design-twitter",
        "title": "Design Twitter",
        "difficulty": "Medium",
        "pattern": "heap merge across followees",
        "statement": "Design a small Twitter with postTweet, getNewsFeed (the ten most recent tweets from the user and their followees), follow and "
                     "unfollow.",
        "examples": [("[\"Twitter\",\"postTweet\",\"getNewsFeed\",\"follow\",\"postTweet\",\"getNewsFeed\",\"unfollow\",\"getNewsFeed\"] [[],[1,5],[1],[1,2],[2,6],[1],[1,2],[1]]",
                      "[null, null, [5], null, null, [6,5], null, [5]]")],
        "constraints": ["1 <= number of calls <= 3 · 10^4", "0 <= userId, followerId <= 500", "the feed holds at most ten tweets"],
        "approach": "Keep each user's tweets in a running list with a global counter as the timestamp, and merge the followees' most recent tweets "
                     "with a max-heap. Because only ten results are needed, each list contributes at most ten candidates — a bounded k-way merge.",
        "complexity": ("O(f log f) per feed with f followees", "O(tweets)"),
        "code": {
            "cpp": r"""// Timestamped lists per user, merged with a heap for the feed
class Twitter {
public:
    int time = 0;
    unordered_map<int, vector<pair<int,int>>> tweets;   // user -> [(time, tweetId)]
    unordered_map<int, unordered_set<int>> follows;     // user -> followees
    void postTweet(int userId, int tweetId) {
        tweets[userId].push_back({time++, tweetId});
    }
    vector<int> getNewsFeed(int userId) {
        priority_queue<array<int,3>> pq;                 // (time, user, position)
        auto add = [&](int u) {
            if (!tweets[u].empty())
                pq.push({tweets[u].back().first, u, (int)tweets[u].size() - 1});
        };
        add(userId);
        for (int u : follows[userId]) add(u);
        vector<int> feed;
        while (!pq.empty() && (int)feed.size() < 10) {
            auto [t, u, pos] = pq.top(); pq.pop();
            feed.push_back(tweets[u][pos].second);
            if (pos > 0) pq.push({tweets[u][pos-1].first, u, pos - 1});
        }
        return feed;
    }
    void follow(int followerId, int followeeId) {
        if (followerId != followeeId) follows[followerId].insert(followeeId);
    }
    void unfollow(int followerId, int followeeId) {
        follows[followerId].erase(followeeId);
    }
};   // O(f log f) per feed · O(tweets + f) space""",
            "java": r"""// Timestamped lists per user, merged with a heap for the feed
class Twitter {
    int time = 0;
    Map<Integer, List<int[]>> tweets = new HashMap<>();   // user -> [(time, id)]
    Map<Integer, Set<Integer>> follows = new HashMap<>();
    void postTweet(int userId, int tweetId) {
        tweets.computeIfAbsent(userId, k -> new ArrayList<>()).add(new int[]{time++, tweetId});
    }
    List<Integer> getNewsFeed(int userId) {
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> b[0] - a[0]);   // by time
        add(pq, userId);
        for (int u : follows.getOrDefault(userId, Set.of())) add(pq, u);
        List<Integer> feed = new ArrayList<>();
        while (!pq.isEmpty() && feed.size() < 10) {
            int[] top = pq.poll();
            List<int[]> list = tweets.get(top[1]);
            feed.add(list.get(top[2])[1]);
            if (top[2] > 0) pq.add(new int[]{list.get(top[2]-1)[0], top[1], top[2] - 1});
        }
        return feed;
    }
    void add(PriorityQueue<int[]> pq, int u) {
        List<int[]> list = tweets.getOrDefault(u, List.of());
        if (!list.isEmpty())
            pq.add(new int[]{list.get(list.size()-1)[0], u, list.size() - 1});
    }
    void follow(int followerId, int followeeId) {
        if (followerId != followeeId)
            follows.computeIfAbsent(followerId, k -> new HashSet<>()).add(followeeId);
    }
    void unfollow(int followerId, int followeeId) {
        follows.getOrDefault(followerId, new HashSet<>()).remove(followeeId);
    }
}   // O(f log f) per feed · O(tweets + f) space""",
            "python": r"""import heapq

class Twitter:
    def __init__(self):
        self.time = 0
        self.tweets = {}             # user -> [(time, tweetId)]
        self.follows = {}            # user -> set of followees

    def postTweet(self, userId, tweetId):
        self.time += 1
        self.tweets.setdefault(userId, []).append((self.time, tweetId))

    def getNewsFeed(self, userId):
        heap = []                    # (time, user, position), newest first
        def push(u):
            lst = self.tweets.get(u)
            if lst:
                heapq.heappush(heap, (-lst[-1][0], u, len(lst) - 1))
        push(userId)
        for u in self.follows.get(userId, ()):
            push(u)
        feed = []
        while heap and len(feed) < 10:
            neg, u, pos = heapq.heappop(heap)
            feed.append(self.tweets[u][pos][1])
            if pos > 0:
                lst = self.tweets[u]
                heapq.heappush(heap, (-lst[pos-1][0], u, pos - 1))
        return feed

    def follow(self, followerId, followeeId):
        if followerId != followeeId:
            self.follows.setdefault(followerId, set()).add(followeeId)

    def unfollow(self, followerId, followeeId):
        self.follows.get(followerId, set()).discard(followeeId)""",
        },
    },
    {
        "slug": "find-k-pairs-with-smallest-sums",
        "title": "Find K Pairs with Smallest Sums",
        "difficulty": "Medium",
        "pattern": "k-way merge over two sorted arrays",
        "statement": "Given two ascending arrays, return the k pairs (one element from each) with the smallest sums.",
        "examples": [("nums1 = [1,7,11], nums2 = [2,4,6], k = 3", "[[1,2],[1,4],[1,6]]"),
                     ("nums1 = [1,1,2], nums2 = [1,2,3], k = 2", "[[1,1],[1,1]]")],
        "constraints": ["1 <= lengths <= 10^5", "-10^9 <= values <= 10^9", "pairs may repeat"],
        "approach": "The simplest pair for each index of the first array is (i, 0). Seed a min-heap with those, then repeatedly pop the smallest pair "
                     "and push its successor (i, j+1). The heap is doing a k-way merge over the rows of the implicit matrix of sums, so only k rows "
                     "are ever touched.",
        "complexity": ("O(k log min(k, n))", "O(min(k, n))"),
        "code": {
            "cpp": r"""// Seed with (i, 0); each pop pushes the pair one column further
vector<vector<int>> kSmallestPairs(vector<int>& a, vector<int>& b, int k) {
    vector<vector<int>> out;
    if (a.empty() || b.empty()) return out;
    priority_queue<array<long long,3>, vector<array<long long,3>>, greater<>> pq;  // (sum, i, j)
    for (int i = 0; i < (int)a.size() && i < k; i++) pq.push({(long long)a[i] + b[0], i, 0});
    while (!pq.empty() && (int)out.size() < k) {
        auto [sum, i, j] = pq.top(); pq.pop();
        out.push_back({a[i], b[j]});
        if (j + 1 < (int)b.size())                   // the successor in this row
            pq.push({(long long)a[i] + b[j+1], i, j + 1});
    }
    return out;
}   // O(k log min(k, n)) time · O(min(k, n)) space""",
            "java": r"""// Seed with (i, 0); each pop pushes the pair one column further
List<List<Integer>> kSmallestPairs(int[] a, int[] b, int k) {
    List<List<Integer>> out = new ArrayList<>();
    if (a.length == 0 || b.length == 0) return out;
    PriorityQueue<long[]> pq = new PriorityQueue<>((x, y) -> Long.compare(x[0], y[0]));
    for (int i = 0; i < a.length && i < k; i++) pq.add(new long[]{(long) a[i] + b[0], i, 0});
    while (!pq.isEmpty() && out.size() < k) {
        long[] top = pq.poll();
        int i = (int) top[1], j = (int) top[2];
        out.add(Arrays.asList(a[i], b[j]));
        if (j + 1 < b.length)                        // the successor in this row
            pq.add(new long[]{(long) a[i] + b[j+1], i, j + 1});
    }
    return out;
}   // O(k log min(k, n)) time · O(min(k, n)) space""",
            "python": r"""import heapq

def k_smallest_pairs(a, b, k):
    if not a or not b:
        return []
    heap = [(a[i] + b[0], i, 0) for i in range(min(len(a), k))]   # one row each
    heapq.heapify(heap)
    out = []
    while heap and len(out) < k:
        _, i, j = heapq.heappop(heap)
        out.append([a[i], b[j]])
        if j + 1 < len(b):                    # the successor in this row
            heapq.heappush(heap, (a[i] + b[j+1], i, j + 1))
    return out""",
        },
    },
    {
        "slug": "kth-smallest-element-in-a-sorted-matrix",
        "title": "Kth Smallest Element in a Sorted Matrix",
        "difficulty": "Medium",
        "pattern": "k-way merge on a matrix",
        "statement": "Rows and columns of a matrix are each sorted ascending. Return the k-th smallest element.",
        "examples": [("matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8", "13"),
                     ("matrix = [[-5]], k = 1", "-5")],
        "constraints": ["1 <= n <= 300", "-10^9 <= values <= 10^9", "rows and columns are sorted"],
        "approach": "Treat the first column as the heads of n sorted lists and merge them with a heap exactly as in the k-way merge. After popping a "
                     "value its row advances one cell, so the k-th pop is the answer with only O(k) heap work.",
        "complexity": ("O(k log n)", "O(n)"),
        "code": {
            "cpp": r"""// Merge the rows with a heap; the k-th pop is the answer
int kthSmallest(vector<vector<int>>& mat, int k) {
    int n = mat.size();
    priority_queue<array<int,3>, vector<array<int,3>>, greater<>> pq;   // (value, row, col)
    for (int i = 0; i < n; i++) pq.push({mat[i][0], i, 0});
    int answer = mat[0][0];
    while (k-- > 0) {
        auto [v, r, c] = pq.top(); pq.pop();
        answer = v;
        if (c + 1 < n) pq.push({mat[r][c+1], r, c + 1});   // advance that row
    }
    return answer;
}   // O(k log n) time · O(n) space""",
            "java": r"""// Merge the rows with a heap; the k-th pop is the answer
int kthSmallest(int[][] mat, int k) {
    int n = mat.length;
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
    for (int i = 0; i < n; i++) pq.add(new int[]{mat[i][0], i, 0});
    int answer = mat[0][0];
    while (k-- > 0) {
        int[] top = pq.poll();
        answer = top[0];
        if (top[2] + 1 < n) pq.add(new int[]{mat[top[1]][top[2]+1], top[1], top[2] + 1});
    }
    return answer;
}   // O(k log n) time · O(n) space""",
            "python": r"""import heapq

def kth_smallest_matrix(matrix, k):
    n = len(matrix)
    heap = [(matrix[i][0], i, 0) for i in range(n)]   # heads of the n rows
    heapq.heapify(heap)
    answer = matrix[0][0]
    for _ in range(k):
        answer, r, c = heapq.heappop(heap)
        if c + 1 < n:
            heapq.heappush(heap, (matrix[r][c+1], r, c + 1))   # advance that row
    return answer""",
        },
    },
    {
        "slug": "seat-reservation-manager",
        "title": "Seat Reservation Manager",
        "difficulty": "Medium",
        "pattern": "min-heap of free seats (design)",
        "statement": "Design a booking system for n seats numbered 1 to n: reserve() returns the smallest unreserved number, and unreserve(seat) returns "
                     "that seat to the pool.",
        "examples": [("[\"SeatManager\",\"reserve\",\"reserve\",\"unreserve\",\"reserve\",\"reserve\",\"reserve\",\"reserve\",\"unreserve\"] [[5],[],[],[2],[],[],[],[],[5]]",
                      "[null, 1, 2, null, 2, 3, 4, 5, null]")],
        "constraints": ["1 <= n <= 10^5", "0 <= number of calls <= 2 · 10^5", "reserve always has a free seat available"],
        "approach": "A min-heap of free seat numbers gives the smallest available seat in logarithmic time, and returned seats are simply pushed back. "
                     "There is no need to sort anything after construction.",
        "complexity": ("O(log n) per operation", "O(n)"),
        "code": {
            "cpp": r"""// A min-heap of free seats answers reserve() and absorbs unreserve()
class SeatManager {
public:
    priority_queue<int, vector<int>, greater<int>> freeSeats;
    SeatManager(int n) {
        for (int s = 1; s <= n; s++) freeSeats.push(s);
    }
    int reserve() {
        int s = freeSeats.top(); freeSeats.pop();
        return s;
    }
    void unreserve(int seatNumber) {
        freeSeats.push(seatNumber);              // returned to the pool
    }
};   // O(log n) per operation · O(n) space""",
            "java": r"""// A min-heap of free seats answers reserve() and absorbs unreserve()
class SeatManager {
    PriorityQueue<Integer> freeSeats = new PriorityQueue<>();
    SeatManager(int n) {
        for (int s = 1; s <= n; s++) freeSeats.add(s);
    }
    int reserve() {
        return freeSeats.poll();
    }
    void unreserve(int seatNumber) {
        freeSeats.add(seatNumber);               // returned to the pool
    }
}   // O(log n) per operation · O(n) space""",
            "python": r"""import heapq

class SeatManager:
    def __init__(self, n):
        self.free = list(range(1, n + 1))    # every seat starts free
        heapq.heapify(self.free)

    def reserve(self):
        return heapq.heappop(self.free)      # the smallest free number

    def unreserve(self, seatNumber):
        heapq.heappush(self.free, seatNumber)   # returned to the pool""",
        },
    },
    {
        "slug": "maximum-number-of-events-that-can-be-attended",
        "title": "Maximum Number of Events That Can Be Attended",
        "difficulty": "Medium",
        "pattern": "sweep days with a deadline heap",
        "statement": "Each event is [startDay, endDay] and attending one takes that whole day, at most one event per day. Return the maximum number of "
                     "events attendable.",
        "examples": [("events = [[1,2],[2,3],[3,4]]", "3"), ("events = [[1,2],[2,3],[3,4],[1,2]]", "4")],
        "constraints": ["1 <= events.length <= 10^5", "1 <= startDay <= endDay <= 10^5", "one event per day"],
        "approach": "Sweep day by day, adding every event that has started into a min-heap keyed by end day, and attend the one that expires soonest. "
                     "That earliest-deadline-first choice is the same exchange argument as interval scheduling, applied one day at a time; the day "
                     "counter can jump straight to the next start when the heap is empty.",
        "complexity": ("O(n log n + days)", "O(n)"),
        "code": {
            "cpp": r"""// Sweep days, always attend the event expiring soonest
int maxEvents(vector<vector<int>>& events) {
    sort(events.begin(), events.end());          // by start day
    priority_queue<int, vector<int>, greater<int>> ending;   // end days
    int i = 0, n = events.size(), day = 0, attended = 0;
    while (i < n || !ending.empty()) {
        if (ending.empty()) day = max(day, events[i][0]);    // jump forward
        while (i < n && events[i][0] <= day) ending.push(events[i++][1]);
        ending.pop();                            // attend the earliest deadline
        attended++;
        day++;
        while (!ending.empty() && ending.top() < day) ending.pop();   // expired
    }
    return attended;
}   // O(n log n) time · O(n) space""",
            "java": r"""// Sweep days, always attend the event expiring soonest
int maxEvents(int[][] events) {
    Arrays.sort(events, (a, b) -> a[0] - b[0]);  // by start day
    PriorityQueue<Integer> ending = new PriorityQueue<>();   // end days
    int i = 0, n = events.length, day = 0, attended = 0;
    while (i < n || !ending.isEmpty()) {
        if (ending.isEmpty()) day = Math.max(day, events[i][0]);   // jump forward
        while (i < n && events[i][0] <= day) ending.add(events[i++][1]);
        ending.poll();                           // attend the earliest deadline
        attended++;
        day++;
        while (!ending.isEmpty() && ending.peek() < day) ending.poll();   // expired
    }
    return attended;
}   // O(n log n) time · O(n) space""",
            "python": r"""import heapq

def max_events(events):
    events.sort()                    # by start day
    ending = []                      # min-heap of end days
    i = 0
    day = 0
    attended = 0
    while i < len(events) or ending:
        if not ending:
            day = max(day, events[i][0])     # jump to the next start day
        while i < len(events) and events[i][0] <= day:
            heapq.heappush(ending, events[i][1])
            i += 1
        heapq.heappop(ending)        # attend the event expiring soonest
        attended += 1
        day += 1
        while ending and ending[0] < day:
            heapq.heappop(ending)    # these deadlines have passed
    return attended""",
        },
    },
    {
        "slug": "process-tasks-using-servers",
        "title": "Process Tasks Using Servers",
        "difficulty": "Medium",
        "pattern": "two heaps: free pool and busy queue",
        "statement": "Servers have weights; each task arrives at a given second. Assign each task to the free server with the smallest weight (ties by "
                     "index); if none is free, wait for the earliest one to finish, again preferring the smallest weight. Return the server indices "
                     "used.",
        "examples": [("servers = [3,3,2], tasks = [1,2,3,2,1,2]", "[2,2,0,2,1,2]"),
                     ("servers = [5,1,4,3,2], tasks = [2,1,2,4,5,2,1]", "[1,4,1,4,1,3,2]")],
        "constraints": ["1 <= servers, tasks <= 2 · 10^5", "1 <= weights, task times <= 2 · 10^5", "the next task starts only when this one is done"],
        "approach": "Keep free servers in a heap ordered by (weight, index) and busy ones in a heap ordered by (free time, weight, index). Before "
                     "each task, release everything that has finished and pick the best free server; the doubly-keyed ordering handles both tie-breaks "
                     "without a single sort.",
        "complexity": ("O((s + t) log s)", "O(s)"),
        "code": {
            "cpp": r"""// Free pool by (weight, index); busy queue by (free time, weight, index)
vector<int> assignTasks(vector<int>& servers, vector<int>& tasks) {
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> freePool;   // (weight, index)
    priority_queue<array<long long,3>, vector<array<long long,3>>, greater<>> busy;  // (time, weight, index)
    for (int i = 0; i < (int)servers.size(); i++) freePool.push({servers[i], i});
    vector<int> out;
    long long second = 0;
    for (int t = 0; t < (int)tasks.size(); t++) {
        second = max(second, (long long)t);       // the task arrives no earlier
        if (freePool.empty()) second = max(second, busy.top()[0]);   // wait for one
        while (!busy.empty() && busy.top()[0] <= second) {           // release
            auto [finish, w, idx] = busy.top(); busy.pop();
            freePool.push({(int)w, (int)idx});
        }
        auto [w, idx] = freePool.top(); freePool.pop();
        out.push_back(idx);
        busy.push({second + tasks[t], w, idx});   // busy until this task finishes
    }
    return out;
}   // O((s + t) log s) time · O(s) space""",
            "java": r"""// Free pool by (weight, index); busy queue by (free time, weight, index)
int[] assignTasks(int[] servers, int[] tasks) {
    PriorityQueue<int[]> freePool = new PriorityQueue<>((a, b) -> a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]);
    PriorityQueue<long[]> busy = new PriorityQueue<>((a, b) -> a[0] != b[0] ? Long.compare(a[0], b[0])
                                                     : (a[1] != b[1] ? Long.compare(a[1], b[1]) : Long.compare(a[2], b[2])));
    for (int i = 0; i < servers.length; i++) freePool.add(new int[]{servers[i], i});
    int[] out = new int[tasks.length];
    long second = 0;
    for (int t = 0; t < tasks.length; t++) {
        second = Math.max(second, t);             // the task arrives no earlier
        if (freePool.isEmpty()) second = Math.max(second, busy.peek()[0]);   // wait
        while (!busy.isEmpty() && busy.peek()[0] <= second) {                // release
            long[] b = busy.poll();
            freePool.add(new int[]{(int) b[1], (int) b[2]});
        }
        int[] chosen = freePool.poll();
        out[t] = chosen[1];
        busy.add(new long[]{second + tasks[t], chosen[0], chosen[1]});       // busy now
    }
    return out;
}   // O((s + t) log s) time · O(s) space""",
            "python": r"""import heapq

def assign_tasks(servers, tasks):
    free_pool = [(w, i) for i, w in enumerate(servers)]   # by (weight, index)
    heapq.heapify(free_pool)
    busy = []                          # (free time, weight, index)
    out = []
    second = 0
    for t, duration in enumerate(tasks):
        second = max(second, t)        # the task arrives no earlier than now
        if not free_pool:
            second = max(second, busy[0][0])     # wait for the first to finish
        while busy and busy[0][0] <= second:     # release finished servers
            _, w, idx = heapq.heappop(busy)
            heapq.heappush(free_pool, (w, idx))
        w, idx = heapq.heappop(free_pool)        # lightest, then smallest index
        out.append(idx)
        heapq.heappush(busy, (second + duration, w, idx))
    return out""",
        },
    },
    {
        "slug": "time-based-key-value-store",
        "title": "Time Based Key-Value Store",
        "difficulty": "Medium",
        "pattern": "append-only log with binary search (design)",
        "statement": "Design a store whose set(key, value, timestamp) records values in increasing timestamp order per key, and whose get(key, timestamp) "
                     "returns the value with the largest timestamp at most the given one, or \"\" if there is none.",
        "examples": [("[\"TimeMap\",\"set\",\"get\",\"get\",\"set\",\"get\",\"get\"] [[],[\"foo\",\"bar\",1],[\"foo\",1],[\"foo\",3],[\"foo\",\"bar2\",4],[\"foo\",4],[\"foo\",5]]",
                      "[null, null, \"bar\", \"bar\", null, \"bar2\", \"bar2\"]")],
        "constraints": ["1 <= number of calls <= 2 · 10^5", "timestamps strictly increase per key", "keys and values are short lowercase strings"],
        "approach": "A per-key list of (timestamp, value) pairs is already sorted, because timestamps only grow per key. Binary search finds the last "
                     "entry at or before the query timestamp, which turns a potentially linear scan into a logarithmic one.",
        "complexity": ("O(log n) per get", "O(total entries)"),
        "code": {
            "cpp": r"""// Each key keeps a growing list; get() binary searches it
class TimeMap {
public:
    unordered_map<string, vector<pair<int,string>>> store;   // key -> [(time, value)]
    void set(string key, string value, int timestamp) {
        store[key].push_back({timestamp, value});            // times only grow
    }
    string get(string key, int timestamp) {
        auto it = store.find(key);
        if (it == store.end()) return "";
        auto& list = it->second;
        // last entry whose time is <= timestamp
        int lo = 0, hi = list.size();
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            if (list[mid].first <= timestamp) lo = mid + 1; else hi = mid;
        }
        return lo == 0 ? "" : list[lo-1].second;
    }
};   // O(log n) per get · O(total entries) space""",
            "java": r"""// Each key keeps a growing list; get() binary searches it
class TimeMap {
    Map<String, List<Object[]>> store = new HashMap<>();   // key -> [(time, value)]
    void set(String key, String value, int timestamp) {
        store.computeIfAbsent(key, k -> new ArrayList<>()).add(new Object[]{timestamp, value});
    }
    String get(String key, int timestamp) {
        List<Object[]> list = store.get(key);
        if (list == null) return "";
        int lo = 0, hi = list.size();
        while (lo < hi) {                        // last entry with time <= timestamp
            int mid = (lo + hi) / 2;
            if ((Integer) list.get(mid)[0] <= timestamp) lo = mid + 1; else hi = mid;
        }
        return lo == 0 ? "" : (String) list.get(lo - 1)[1];
    }
}   // O(log n) per get · O(total entries) space""",
            "python": r"""from bisect import bisect_right

class TimeMap:
    def __init__(self):
        self.times = {}                # key -> [timestamps], ascending
        self.values = {}               # key -> [values]

    def set(self, key, value, timestamp):
        self.times.setdefault(key, []).append(timestamp)   # times only grow
        self.values.setdefault(key, []).append(value)

    def get(self, key, timestamp):
        if key not in self.times:
            return ''
        i = bisect_right(self.times[key], timestamp)       # last time <= timestamp
        return '' if i == 0 else self.values[key][i-1]""",
        },
    },
    {
        "slug": "find-median-from-data-stream",
        "title": "Find Median from Data Stream",
        "difficulty": "Hard",
        "pattern": "two heaps around the median",
        "statement": "Design a structure with addNum(int) and findMedian() that reports the median of everything added so far.",
        "examples": [("[\"MedianFinder\",\"addNum\",\"addNum\",\"findMedian\",\"addNum\",\"findMedian\"] [[],[1],[2],[],[3],[]]",
                      "[null, null, null, 1.5, null, 2.0]")],
        "constraints": ["-10^5 <= num <= 10^5", "at most 5 · 10^4 calls", "findMedian is only called when a number exists"],
        "approach": "Keep the smaller half in a max-heap and the larger half in a min-heap, sized so they differ by at most one. The median is then "
                     "either the top of the bigger heap or the average of the two tops, and each insertion costs two logarithmic moves.",
        "complexity": ("O(log n) per add, O(1) per median", "O(n)"),
        "code": {
            "cpp": r"""// Smaller half in a max-heap, larger half in a min-heap
class MedianFinder {
public:
    priority_queue<int> low;                                 // max-heap
    priority_queue<int, vector<int>, greater<int>> high;     // min-heap
    void addNum(int num) {
        low.push(num);
        high.push(low.top()); low.pop();                     // hand the largest low over
        if (high.size() > low.size()) { low.push(high.top()); high.pop(); }
    }
    double findMedian() {
        return low.size() > high.size()
             ? low.top()                                     // odd count: the middle
             : (low.top() + high.top()) / 2.0;               // even count: the average
    }
};   // O(log n) per add · O(n) space""",
            "java": r"""// Smaller half in a max-heap, larger half in a min-heap
class MedianFinder {
    PriorityQueue<Integer> low = new PriorityQueue<>(Collections.reverseOrder());
    PriorityQueue<Integer> high = new PriorityQueue<>();
    void addNum(int num) {
        low.add(num);
        high.add(low.poll());                    // hand the largest low over
        if (high.size() > low.size()) low.add(high.poll());
    }
    double findMedian() {
        return low.size() > high.size()
             ? low.peek()                        // odd count: the middle
             : (low.peek() + high.peek()) / 2.0; // even count: the average
    }
}   // O(log n) per add · O(n) space""",
            "python": r"""import heapq

class MedianFinder:
    def __init__(self):
        self.low = []                  # max-heap (negated): the smaller half
        self.high = []                 # min-heap: the larger half

    def addNum(self, num):
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))   # largest low moves up
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def findMedian(self):
        if len(self.low) > len(self.high):
            return float(-self.low[0])             # odd count: the middle
        return (-self.low[0] + self.high[0]) / 2   # even count: the average""",
        },
    },
    {
        "slug": "sliding-window-median",
        "title": "Sliding Window Median",
        "difficulty": "Hard",
        "pattern": "two heaps with lazy deletion",
        "statement": "Return the median of every window of size k as it slides across the array from left to right.",
        "examples": [("nums = [1,3,-1,-3,5,3,6,7], k = 3", "[1.00000,-1.00000,-1.00000,3.00000,5.00000,6.00000]"),
                     ("nums = [1,2,3,4,2,3,1,4,2], k = 3", "[2.00000,3.00000,3.00000,3.00000,2.00000,3.00000,2.00000]")],
        "constraints": ["1 <= k <= nums.length <= 10^5", "-2^31 <= nums[i] <= 2^31 - 1", "the median of an even window is the mean of the middle two"],
        "approach": "The two-heap median structure cannot delete arbitrary elements cheaply, so deletions are *deferred*: record the leaving value in a "
                     "pending map, shrink the logical size of the half it belonged to, and let each heap discard such entries when they reach its top. "
                     "The result is two heaps that stay the right shape while ignoring the values that have left the window.",
        "complexity": ("O(n log k)", "O(k)"),
        "code": {
            "cpp": r"""// Two heaps plus a pending-deletion map: stale entries leave at the top
vector<double> medianSlidingWindow(vector<int>& nums, int k) {
    priority_queue<int> low;                                 // max-heap (smaller half)
    priority_queue<int, vector<int>, greater<int>> high;     // min-heap (larger half)
    unordered_map<int,int> pending;                          // value -> deletions owed
    int lowSize = 0, highSize = 0;
    auto clean = [&]() {
        while (!low.empty() && pending[low.top()]) { pending[low.top()]--; low.pop(); }
        while (!high.empty() && pending[high.top()]) { pending[high.top()]--; high.pop(); }
    };
    auto rebalance = [&]() {
        if (lowSize > highSize + 1) {
            high.push(low.top()); low.pop(); lowSize--; highSize++;
        } else if (highSize > lowSize) {
            low.push(high.top()); high.pop(); highSize--; lowSize++;
        }
    };
    vector<double> out;
    for (int i = 0; i < (int)nums.size(); i++) {
        clean();
        if (!low.empty() && nums[i] <= low.top()) { low.push(nums[i]); lowSize++; }
        else { high.push(nums[i]); highSize++; }
        rebalance();
        clean();
        if (i >= k - 1) {
            out.push_back(k % 2 ? (double) low.top()
                                : (low.top() + (double) high.top()) / 2.0);
            int gone = nums[i - k + 1];
            clean();
            if (!low.empty() && gone <= low.top()) lowSize--; else highSize--;
            pending[gone]++;
            clean();
            rebalance();
            clean();
        }
    }
    return out;
}   // O(n log k) time · O(k) space""",
            "java": r"""// Two heaps plus a pending-deletion map: stale entries leave at the top
double[] medianSlidingWindow(int[] nums, int k) {
    PriorityQueue<Integer> low = new PriorityQueue<>(Collections.reverseOrder());
    PriorityQueue<Integer> high = new PriorityQueue<>();
    Map<Integer, Integer> pending = new HashMap<>();          // deletions owed
    int[] sizes = new int[]{0, 0};                            // [lowSize, highSize]
    double[] out = new double[nums.length - k + 1];
    for (int i = 0; i < nums.length; i++) {
        clean(low, high, pending);
        if (!low.isEmpty() && nums[i] <= low.peek()) { low.add(nums[i]); sizes[0]++; }
        else { high.add(nums[i]); sizes[1]++; }
        rebalance(low, high, sizes);
        clean(low, high, pending);
        if (i >= k - 1) {
            out[i - k + 1] = (k % 2 == 1) ? (double) low.peek()
                          : ((double) low.peek() + high.peek()) / 2.0;
            int gone = nums[i - k + 1];
            clean(low, high, pending);
            if (!low.isEmpty() && gone <= low.peek()) sizes[0]--; else sizes[1]--;
            pending.merge(gone, 1, Integer::sum);
            clean(low, high, pending);
            rebalance(low, high, sizes);
            clean(low, high, pending);
        }
    }
    return out;
}
void clean(PriorityQueue<Integer> low, PriorityQueue<Integer> high, Map<Integer, Integer> pending) {
    while (!low.isEmpty() && pending.getOrDefault(low.peek(), 0) > 0) {
        pending.merge(low.peek(), -1, Integer::sum); low.poll();
    }
    while (!high.isEmpty() && pending.getOrDefault(high.peek(), 0) > 0) {
        pending.merge(high.peek(), -1, Integer::sum); high.poll();
    }
}
void rebalance(PriorityQueue<Integer> low, PriorityQueue<Integer> high, int[] sizes) {
    if (sizes[0] > sizes[1] + 1) { high.add(low.poll()); sizes[0]--; sizes[1]++; }
    else if (sizes[1] > sizes[0]) { low.add(high.poll()); sizes[1]--; sizes[0]++; }
}   // O(n log k) time · O(k) space""",
            "python": r"""import heapq

def median_sliding_window(nums, k):
    low, high = [], []                 # low: max-heap (negated), high: min-heap
    pending = {}                       # value -> deletions still owed
    sizes = [0, 0]                     # logical sizes, ignoring stale entries

    def clean():
        while low and pending.get(-low[0], 0) > 0:
            pending[-low[0]] -= 1
            heapq.heappop(low)
        while high and pending.get(high[0], 0) > 0:
            pending[high[0]] -= 1
            heapq.heappop(high)

    def rebalance():
        if sizes[0] > sizes[1] + 1:
            heapq.heappush(high, -heapq.heappop(low))
            sizes[0] -= 1; sizes[1] += 1
        elif sizes[1] > sizes[0]:
            heapq.heappush(low, -heapq.heappop(high))
            sizes[1] -= 1; sizes[0] += 1

    out = []
    for i, x in enumerate(nums):
        clean()
        if low and x <= -low[0]:
            heapq.heappush(low, -x); sizes[0] += 1
        else:
            heapq.heappush(high, x); sizes[1] += 1
        rebalance()
        clean()
        if i >= k - 1:
            out.append(float(-low[0]) if k % 2 else (-low[0] + high[0]) / 2)
            gone = nums[i - k + 1]
            clean()
            if low and gone <= -low[0]:
                sizes[0] -= 1
            else:
                sizes[1] -= 1
            pending[gone] = pending.get(gone, 0) + 1   # defer the removal
            clean()
            rebalance()
            clean()
    return out""",
        },
    },
    {
        "slug": "find-the-kth-smallest-sum-of-a-matrix-with-sorted-rows",
        "title": "Kth Smallest Sum of a Matrix With Sorted Rows",
        "difficulty": "Hard",
        "pattern": "repeated k-way merge across rows",
        "statement": "The rows of the matrix are sorted. A sum picks exactly one element from each row. Return the k-th smallest such sum.",
        "examples": [("mat = [[1,3,11],[2,4,6]], k = 5", "7"),
                     ("mat = [[1,3,11],[2,4,6]], k = 9", "17"), ("mat = [[1,10,10],[1,4,5],[2,3,6]], k = 7", "9")],
        "constraints": ["1 <= rows, cols <= 40", "1 <= mat[i][j] <= 5000", "1 <= k <= min(200, cols^rows)"],
        "approach": "Fold the rows one at a time. Keeping only the k smallest partial sums is safe, because any larger partial sum can only produce "
                     "larger totals. Combining a k-element list with the next row is exactly the k-smallest-pairs problem, solved by a heap walk that "
                     "never materialises the full product.",
        "complexity": ("O(rows · k log min(k, cols))", "O(k)"),
        "code": {
            "cpp": r"""// Fold rows in: each step keeps only the k smallest partial sums
int kthSmallest(vector<vector<int>>& mat, int k) {
    vector<int> sums = mat[0];
    sort(sums.begin(), sums.end());
    if ((int)sums.size() > k) sums.resize(k);
    for (size_t r = 1; r < mat.size(); r++) {
        vector<int> row = mat[r];
        sort(row.begin(), row.end());
        priority_queue<array<long long,3>, vector<array<long long,3>>, greater<>> pq;   // (sum, i, j)
        for (int i = 0; i < (int)sums.size() && i < k; i++)
            pq.push({(long long)sums[i] + row[0], i, 0});
        vector<int> next;
        while (!pq.empty() && (int)next.size() < k) {
            auto [s, i, j] = pq.top(); pq.pop();
            next.push_back((int) s);
            if (j + 1 < (int)row.size())             // the successor in this row
                pq.push({(long long)sums[i] + row[j+1], i, j + 1});
        }
        sums = move(next);
    }
    return sums[k - 1];
}   // O(rows · k log min(k, cols)) time · O(k) space""",
            "java": r"""// Fold rows in: each step keeps only the k smallest partial sums
int kthSmallest(int[][] mat, int k) {
    int[] sums = mat[0].clone();
    Arrays.sort(sums);
    if (sums.length > k) sums = Arrays.copyOf(sums, k);
    for (int r = 1; r < mat.length; r++) {
        int[] row = mat[r].clone();
        Arrays.sort(row);
        PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
        for (int i = 0; i < sums.length && i < k; i++)
            pq.add(new long[]{(long) sums[i] + row[0], i, 0});
        int[] next = new int[Math.min(k, sums.length * row.length)];
        int count = 0;
        while (!pq.isEmpty() && count < next.length) {
            long[] top = pq.poll();
            int i = (int) top[1], j = (int) top[2];
            next[count++] = (int) top[0];
            if (j + 1 < row.length)                  // the successor in this row
                pq.add(new long[]{(long) sums[i] + row[j+1], i, j + 1});
        }
        sums = next;
    }
    return sums[k - 1];
}   // O(rows · k log min(k, cols)) time · O(k) space""",
            "python": r"""import heapq

def kth_smallest_sum(mat, k):
    sums = sorted(mat[0])[:k]                  # the k smallest of the first row
    for row in mat[1:]:
        row = sorted(row)
        heap = [(sums[i] + row[0], i, 0) for i in range(min(len(sums), k))]
        heapq.heapify(heap)
        nxt = []
        while heap and len(nxt) < k:
            total, i, j = heapq.heappop(heap)
            nxt.append(total)
            if j + 1 < len(row):               # the successor in this row
                heapq.heappush(heap, (sums[i] + row[j+1], i, j + 1))
        sums = nxt
    return sums[k - 1]""",
        },
    },
    {
        "slug": "the-skyline-problem",
        "title": "The Skyline Problem",
        "difficulty": "Hard",
        "pattern": "sweep line with a height heap",
        "statement": "Each building is [left, right, height]. Return the skyline as the list of critical points where the silhouette's height changes.",
        "examples": [("buildings = [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]",
                      "[[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]"),
                     ("buildings = [[0,2,3],[2,5,3]]", "[[0,3],[5,0]]")],
        "constraints": ["1 <= buildings.length <= 10^4", "0 <= left < right <= 2^31 - 1", "1 <= height <= 2^31 - 1"],
        "approach": "Turn each building into a start event and an end event, sort by x, and keep the active heights in a max-heap. Endings cannot be "
                     "removed from a heap directly, so they are counted in a pending map and discarded when they surface at the top — the same lazy "
                     "deletion trick as the sliding median, here doing all the work.",
        "complexity": ("O(n log n)", "O(n)"),
        "code": {
            "cpp": r"""// Sweep the x-axis; the heap top is the current skyline height
vector<vector<int>> getSkyline(vector<vector<int>>& buildings) {
    vector<pair<int,int>> events;                // (x, signed height): -h starts, +h ends
    for (auto& b : buildings) {
        events.push_back({b[0], -b[2]});
        events.push_back({b[1], b[2]});
    }
    sort(events.begin(), events.end());          // starts sort before ends at the same x
    priority_queue<int> heights;                 // active heights, max on top
    unordered_map<int,int> pending;              // endings waiting to be discarded
    heights.push(0);                             // the ground
    vector<vector<int>> out;
    int prev = 0;
    for (auto& [x, h] : events) {
        if (h < 0) heights.push(-h);             // a building starts
        else pending[h]++;                       // a building ends
        while (pending[heights.top()] > 0) {     // drop heights that already ended
            pending[heights.top()]--;
            heights.pop();
        }
        int cur = heights.top();
        if (cur != prev) {                       // the silhouette changed here
            out.push_back({x, cur});
            prev = cur;
        }
    }
    return out;
}   // O(n log n) time · O(n) space""",
            "java": r"""// Sweep the x-axis; the heap top is the current skyline height
List<List<Integer>> getSkyline(int[][] buildings) {
    List<int[]> events = new ArrayList<>();      // (x, signed height): -h starts, +h ends
    for (int[] b : buildings) {
        events.add(new int[]{b[0], -b[2]});
        events.add(new int[]{b[1], b[2]});
    }
    events.sort((a, b) -> a[0] != b[0] ? a[0] - b[0] : a[1] - b[1]);
    PriorityQueue<Integer> heights = new PriorityQueue<>(Collections.reverseOrder());
    Map<Integer, Integer> pending = new HashMap<>();   // endings waiting to be discarded
    heights.add(0);                              // the ground
    List<List<Integer>> out = new ArrayList<>();
    int prev = 0;
    for (int[] e : events) {
        if (e[1] < 0) heights.add(-e[1]);        // a building starts
        else pending.merge(e[1], 1, Integer::sum);   // a building ends
        while (pending.getOrDefault(heights.peek(), 0) > 0) {   // drop ended heights
            pending.merge(heights.peek(), -1, Integer::sum);
            heights.poll();
        }
        int cur = heights.peek();
        if (cur != prev) {                       // the silhouette changed here
            out.add(Arrays.asList(e[0], cur));
            prev = cur;
        }
    }
    return out;
}   // O(n log n) time · O(n) space""",
            "python": r"""import heapq

def get_skyline(buildings):
    events = []                          # (x, signed height): -h starts, +h ends
    for left, right, height in buildings:
        events.append((left, -height))
        events.append((right, height))
    events.sort()                        # starts sort before ends at the same x
    heights = [0]                        # max-heap (negated) of active heights
    pending = {}                         # endings waiting to be discarded
    out = []
    prev = 0
    for x, h in events:
        if h < 0:
            heapq.heappush(heights, h)   # a building starts
        else:
            pending[h] = pending.get(h, 0) + 1   # a building ends
        while pending.get(-heights[0], 0) > 0:   # discard heights that ended
            pending[-heights[0]] -= 1
            heapq.heappop(heights)
        cur = -heights[0]
        if cur != prev:                  # the silhouette changed here
            out.append([x, cur])
            prev = cur
    return out""",
        },
    },
    {
        "slug": "trapping-rain-water-ii",
        "title": "Trapping Rain Water II",
        "difficulty": "Hard",
        "pattern": "min-heap flooding from the border",
        "statement": "Given the heights of a 2D cell grid, return how much water is trapped after raining.",
        "examples": [("heightMap = [[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]", "4"),
                     ("heightMap = [[3,3,3,3,3],[3,2,2,2,3],[3,2,1,2,3],[3,2,2,2,3],[3,3,3,3,3]]", "10")],
        "constraints": ["1 <= rows, cols <= 200", "0 <= height <= 2 · 10^4", "water cannot flow off the border cells"],
        "approach": "Water escapes along the lowest path to the border, so flood inward from the border with a min-heap: always process the lowest "
                     "boundary cell, raise the water level to it, and let its neighbours join the boundary. A cell's trapped water is the level when "
                     "it is reached minus its own height.",
        "complexity": ("O(rows · cols · log(rows · cols))", "O(rows · cols)"),
        "code": {
            "cpp": r"""// Flood inward from the border; the heap keeps the lowest boundary cell
int trapRainWater(vector<vector<int>>& h) {
    int R = h.size(), C = h[0].size();
    if (R < 3 || C < 3) return 0;                // no room to trap anything
    priority_queue<array<int,3>, vector<array<int,3>>, greater<>> pq;   // (height, r, c)
    vector<vector<bool>> seen(R, vector<bool>(C, false));
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            if (r == 0 || c == 0 || r == R-1 || c == C-1) {
                pq.push({h[r][c], r, c});
                seen[r][c] = true;
            }
    int water = 0, level = 0;
    int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    while (!pq.empty()) {
        auto [height, r, c] = pq.top(); pq.pop();
        level = max(level, height);              // the water level never falls
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= R || nc < 0 || nc >= C || seen[nr][nc]) continue;
            seen[nr][nc] = true;
            water += max(0, level - h[nr][nc]);  // anything below the level holds water
            pq.push({h[nr][nc], nr, nc});
        }
    }
    return water;
}   // O(R·C log(R·C)) time · O(R·C) space""",
            "java": r"""// Flood inward from the border; the heap keeps the lowest boundary cell
int trapRainWater(int[][] h) {
    int R = h.length, C = h[0].length;
    if (R < 3 || C < 3) return 0;                // no room to trap anything
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
    boolean[][] seen = new boolean[R][C];
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            if (r == 0 || c == 0 || r == R-1 || c == C-1) {
                pq.add(new int[]{h[r][c], r, c});
                seen[r][c] = true;
            }
    int water = 0, level = 0;
    int[] dr = {1,-1,0,0}, dc = {0,0,1,-1};
    while (!pq.isEmpty()) {
        int[] cur = pq.poll();
        int height = cur[0], r = cur[1], c = cur[2];
        level = Math.max(level, height);         // the water level never falls
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= R || nc < 0 || nc >= C || seen[nr][nc]) continue;
            seen[nr][nc] = true;
            water += Math.max(0, level - h[nr][nc]);   // held below the level
            pq.add(new int[]{h[nr][nc], nr, nc});
        }
    }
    return water;
}   // O(R·C log(R·C)) time · O(R·C) space""",
            "python": r"""import heapq

def trap_rain_water(height_map):
    R, C = len(height_map), len(height_map[0])
    if R < 3 or C < 3:
        return 0                     # a 1- or 2-wide strip traps nothing
    heap = []
    seen = [[False] * C for _ in range(R)]
    for r in range(R):
        for c in range(C):
            if r in (0, R - 1) or c in (0, C - 1):
                heapq.heappush(heap, (height_map[r][c], r, c))
                seen[r][c] = True
    water = 0
    level = 0
    while heap:
        height, r, c = heapq.heappop(heap)
        level = max(level, height)   # the water level never falls
        for nr, nc in ((r+1,c), (r-1,c), (r,c+1), (r,c-1)):
            if 0 <= nr < R and 0 <= nc < C and not seen[nr][nc]:
                seen[nr][nc] = True
                water += max(0, level - height_map[nr][nc])   # held water
                heapq.heappush(heap, (height_map[nr][nc], nr, nc))
    return water""",
        },
    },
    {
        "slug": "max-value-of-equation",
        "title": "Max Value of Equation",
        "difficulty": "Hard",
        "pattern": "sliding window maximum with a deque",
        "statement": "Given points [xi, yi] with xi strictly increasing, and a limit k, maximise yi + yj + |xi - xj| over pairs with |xi - xj| <= k.",
        "examples": [("points = [[1,3],[2,0],[5,10],[6,-10]], k = 1", "4"),
                     ("points = [[0,0],[3,0],[9,2]], k = 3", "3")],
        "constraints": ["2 <= points.length <= 10^5", "-10^8 <= xi, yi <= 10^8", "points are sorted by xi"],
        "approach": "Because the x values increase, the absolute value disappears: for i before j the expression is (yj + xj) + (yi - xi). That makes "
                     "it a sliding-window maximum of yi - xi over the previous positions within distance k, which a monotonic deque maintains in "
                     "constant amortised time.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// For i < j the expression is (yj + xj) + (yi - xi): windowed max of y - x
int findMaxValueOfEquation(vector<vector<int>>& points, int k) {
    deque<int> dq;                               // indices with decreasing y - x
    int best = INT_MIN;
    for (int j = 0; j < (int)points.size(); j++) {
        int xj = points[j][0], yj = points[j][1];
        while (!dq.empty() && xj - points[dq.front()][0] > k) dq.pop_front();   // out of reach
        if (!dq.empty()) {
            int i = dq.front();
            best = max(best, yj + xj + points[i][1] - points[i][0]);
        }
        int key = yj - xj;
        while (!dq.empty() && points[dq.back()][1] - points[dq.back()][0] <= key)
            dq.pop_back();                       // this candidate is superseded
        dq.push_back(j);
    }
    return best;
}   // O(n) time · O(n) space""",
            "java": r"""// For i < j the expression is (yj + xj) + (yi - xi): windowed max of y - x
int findMaxValueOfEquation(int[][] points, int k) {
    Deque<Integer> dq = new ArrayDeque<>();      // indices with decreasing y - x
    int best = Integer.MIN_VALUE;
    for (int j = 0; j < points.length; j++) {
        int xj = points[j][0], yj = points[j][1];
        while (!dq.isEmpty() && xj - points[dq.peekFirst()][0] > k) dq.pollFirst();   // too far
        if (!dq.isEmpty()) {
            int i = dq.peekFirst();
            best = Math.max(best, yj + xj + points[i][1] - points[i][0]);
        }
        int key = yj - xj;
        while (!dq.isEmpty() && points[dq.peekLast()][1] - points[dq.peekLast()][0] <= key)
            dq.pollLast();                       // this candidate is superseded
        dq.addLast(j);
    }
    return best;
}   // O(n) time · O(n) space""",
            "python": r"""from collections import deque

def find_max_value_of_equation(points, k):
    dq = deque()                     # indices with decreasing y - x
    best = float('-inf')
    for j, (xj, yj) in enumerate(points):
        while dq and xj - points[dq[0]][0] > k:
            dq.popleft()             # this partner is out of reach
        if dq:
            i = dq[0]
            best = max(best, yj + xj + points[i][1] - points[i][0])
        key = yj - xj
        while dq and points[dq[-1]][1] - points[dq[-1]][0] <= key:
            dq.pop()                 # a better candidate supersedes it
        dq.append(j)
    return best""",
        },
    },
    {
        "slug": "construct-target-array-with-multiple-sums",
        "title": "Construct Target Array With Multiple Sums",
        "difficulty": "Hard",
        "pattern": "reverse simulation with a max-heap",
        "statement": "Starting from an array of all ones, each step replaces one element by the sum of the whole array. Given a target array, decide "
                     "whether it can be produced.",
        "examples": [("target = [9,3,5]", "true"), ("target = [1,1,1,2]", "false"), ("target = [8,5]", "true")],
        "constraints": ["1 <= target.length <= 5 · 10^4", "1 <= target[i] <= 10^9", "the forward step raises one element at a time"],
        "approach": "Run the process backwards: the largest element must have been the sum of everything else plus its own previous value, so it "
                     "reduces to (largest mod rest). Taking the modulo skips thousands of identical reverse steps at once, which is what keeps the "
                     "loop logarithmic instead of linear in the values.",
        "complexity": ("O(n log n log(max value))", "O(n)"),
        "code": {
            "cpp": r"""// Reverse the process: the max shrinks to (max mod rest)
bool isPossible(vector<int>& target) {
    priority_queue<int> pq(target.begin(), target.end());
    long long total = accumulate(target.begin(), target.end(), 0LL);
    while (pq.top() > 1) {
        long long mx = pq.top(); pq.pop();
        long long rest = total - mx;
        if (rest == 0 || rest >= mx) return false;       // impossible predecessor
        long long prev = mx % rest;                      // skip repeated steps
        if (prev == 0) prev = rest;                      // exact multiple of rest
        if (prev >= mx) return false;                    // must have come from below
        total = rest + prev;
        pq.push((int) prev);
    }
    return true;
}   // O(n log n log(max value)) time · O(n) space""",
            "java": r"""// Reverse the process: the max shrinks to (max mod rest)
boolean isPossible(int[] target) {
    PriorityQueue<Long> pq = new PriorityQueue<>(Collections.reverseOrder());
    long total = 0;
    for (int t : target) { pq.add((long) t); total += t; }
    while (pq.peek() > 1) {
        long mx = pq.poll();
        long rest = total - mx;
        if (rest == 0 || rest >= mx) return false;       // impossible predecessor
        long prev = mx % rest;                           // skip repeated steps
        if (prev == 0) prev = rest;                      // exact multiple of rest
        if (prev >= mx) return false;                    // must have come from below
        total = rest + prev;
        pq.add(prev);
    }
    return true;
}   // O(n log n log(max value)) time · O(n) space""",
            "python": r"""import heapq

def is_possible(target):
    heap = [-t for t in target]          # max-heap (negated)
    heapq.heapify(heap)
    total = sum(target)
    while -heap[0] > 1:
        mx = -heapq.heappop(heap)
        rest = total - mx
        if rest == 0 or rest >= mx:
            return False                 # the largest must exceed the rest
        prev = mx % rest                 # skip thousands of identical steps
        if prev == 0:
            prev = rest                  # the max was an exact multiple of rest
        if prev >= mx:
            return False                 # the predecessor must be smaller
        total = rest + prev
        heapq.heappush(heap, -prev)
    return True                          # reduced all the way to ones""",
        },
    },
    {
        "slug": "minimum-difference-in-sums-after-removal-of-elements",
        "title": "Minimum Difference in Sums After Removal of Elements",
        "difficulty": "Hard",
        "pattern": "prefix and suffix selection with heaps",
        "statement": "The array has 3n elements. Remove exactly n of them, then split the remaining 2n, in order, into a first and a second half of n "
                     "elements each; return the smallest possible value of (sum of the first half) - (sum of the second half).",
        "examples": [("nums = [3,1,2]", "-1"), ("nums = [7,9,5,8,1,3]", "1")],
        "constraints": ["1 <= n <= 10^5", "nums.length == 3n", "1 <= nums[i] <= 10^5"],
        "approach": "Scan once from the left keeping the n smallest values in a max-heap to get the cheapest prefix sum at every split, then scan from "
                     "the right keeping the n largest in a min-heap for the best suffix sum. The answer is the smallest gap between the two arrays at "
                     "any valid cut.",
        "complexity": ("O(n log n)", "O(n)"),
        "code": {
            "cpp": r"""// Cheapest prefix selection and richest suffix selection, then compare
long long minimumDifference(vector<int>& nums) {
    int m = nums.size(), n = m / 3;
    vector<long long> left(m, 0), right(m, 0);
    priority_queue<int> keepLow;                 // largest of the n smallest on top
    long long sum = 0;
    for (int i = 0; i < m; i++) {
        keepLow.push(nums[i]);
        sum += nums[i];
        if ((int)keepLow.size() > n) { sum -= keepLow.top(); keepLow.pop(); }
        if ((int)keepLow.size() == n) left[i] = sum;
    }
    priority_queue<int, vector<int>, greater<int>> keepHigh;   // smallest of the n largest
    sum = 0;
    for (int i = m - 1; i >= 0; i--) {
        keepHigh.push(nums[i]);
        sum += nums[i];
        if ((int)keepHigh.size() > n) { sum -= keepHigh.top(); keepHigh.pop(); }
        if ((int)keepHigh.size() == n) right[i] = sum;
    }
    long long best = LLONG_MAX;
    for (int i = n - 1; i < 2 * n; i++) best = min(best, left[i] - right[i+1]);
    return best;
}   // O(n log n) time · O(n) space""",
            "java": r"""// Cheapest prefix selection and richest suffix selection, then compare
long minimumDifference(int[] nums) {
    int m = nums.length, n = m / 3;
    long[] left = new long[m], right = new long[m];
    PriorityQueue<Integer> keepLow = new PriorityQueue<>(Collections.reverseOrder());
    long sum = 0;
    for (int i = 0; i < m; i++) {
        keepLow.add(nums[i]);
        sum += nums[i];
        if (keepLow.size() > n) sum -= keepLow.poll();
        if (keepLow.size() == n) left[i] = sum;
    }
    PriorityQueue<Integer> keepHigh = new PriorityQueue<>();
    sum = 0;
    for (int i = m - 1; i >= 0; i--) {
        keepHigh.add(nums[i]);
        sum += nums[i];
        if (keepHigh.size() > n) sum -= keepHigh.poll();
        if (keepHigh.size() == n) right[i] = sum;
    }
    long best = Long.MAX_VALUE;
    for (int i = n - 1; i < 2 * n; i++) best = Math.min(best, left[i] - right[i+1]);
    return best;
}   // O(n log n) time · O(n) space""",
            "python": r"""import heapq

def minimum_difference(nums):
    m = len(nums)
    n = m // 3
    left = [0] * m                    # cheapest sum of n picked from nums[:i+1]
    keep = []                         # max-heap of the n smallest values so far
    total = 0
    for i, x in enumerate(nums):
        heapq.heappush(keep, -x)
        total += x
        if len(keep) > n:
            total += heapq.heappop(keep)      # drop the largest (negated)
        if len(keep) == n:
            left[i] = total
    right = [0] * m                   # richest sum of n picked from nums[i:]
    keep = []                         # min-heap of the n largest values so far
    total = 0
    for i in range(m - 1, -1, -1):
        x = nums[i]
        heapq.heappush(keep, x)
        total += x
        if len(keep) > n:
            total -= heapq.heappop(keep)      # drop the smallest
        if len(keep) == n:
            right[i] = total
    return min(left[i] - right[i+1] for i in range(n - 1, 2 * n))""",
        },
    },
    {
        "slug": "insert-delete-getrandom-o1-duplicates-allowed",
        "title": "Insert Delete GetRandom O(1) — Duplicates Allowed",
        "difficulty": "Hard",
        "pattern": "array plus index map (design)",
        "statement": "Design a multiset with insert(val), which returns true only when val was absent; remove(val), which returns true only when val "
                     "was present; and getRandom(), which returns a uniformly random element. Duplicates are allowed and every operation must "
                     "average constant time.",
        "examples": [("[\"RandomizedCollection\",\"insert\",\"insert\",\"insert\",\"getRandom\",\"remove\",\"getRandom\"] [[],[1],[1],[2],[],[1],[]]",
                      "[null, true, false, true, 2, true, 1]")],
        "constraints": ["-2^31 <= val <= 2^31 - 1", "at most 2 · 10^5 calls", "getRandom is called only when the structure is non-empty"],
        "approach": "Keep the values in a plain array and a map from value to the set of its array positions. Deletion swaps the victim with the last "
                     "array element and rewrites only those two positions, so no shifting ever happens and every operation stays constant on average.",
        "complexity": ("O(1) average per operation", "O(n)"),
        "code": {
            "cpp": r"""// Array plus value -> positions; deletion swaps with the last slot
class RandomizedCollection {
public:
    vector<int> items;
    unordered_map<int, unordered_set<int>> where;    // value -> array indices
    bool insert(int val) {
        bool fresh = where[val].empty();
        where[val].insert(items.size());
        items.push_back(val);
        return fresh;
    }
    bool remove(int val) {
        auto it = where.find(val);
        if (it == where.end() || it->second.empty()) return false;
        int victim = *it->second.begin();            // any copy will do
        it->second.erase(victim);
        int last = items.size() - 1;
        if (victim != last) {
            int moved = items[last];                 // the last slot fills the hole
            items[victim] = moved;
            where[moved].erase(last);
            where[moved].insert(victim);
        }
        items.pop_back();
        return true;
    }
    int getRandom() {
        return items[rand() % items.size()];
    }
};   // O(1) average per operation · O(n) space""",
            "java": r"""// Array plus value -> positions; deletion swaps with the last slot
class RandomizedCollection {
    List<Integer> items = new ArrayList<>();
    Map<Integer, Set<Integer>> where = new HashMap<>();   // value -> indices
    boolean insert(int val) {
        boolean fresh = !where.containsKey(val) || where.get(val).isEmpty();
        where.computeIfAbsent(val, k -> new HashSet<>()).add(items.size());
        items.add(val);
        return fresh;
    }
    boolean remove(int val) {
        Set<Integer> spots = where.get(val);
        if (spots == null || spots.isEmpty()) return false;
        int victim = spots.iterator().next();        // any copy will do
        spots.remove(victim);
        int last = items.size() - 1;
        if (victim != last) {
            int moved = items.get(last);             // the last slot fills the hole
            items.set(victim, moved);
            where.get(moved).remove(last);
            where.get(moved).add(victim);
        }
        items.remove(last);
        return true;
    }
    int getRandom() {
        return items.get((int) (Math.random() * items.size()));
    }
}   // O(1) average per operation · O(n) space""",
            "python": r"""import random

class RandomizedCollection:
    def __init__(self):
        self.items = []                    # the values, in arbitrary order
        self.where = {}                    # value -> set of array indices

    def insert(self, val):
        fresh = not self.where.get(val)    # true only if it was absent
        self.where.setdefault(val, set()).add(len(self.items))
        self.items.append(val)
        return fresh

    def remove(self, val):
        spots = self.where.get(val)
        if not spots:
            return False
        victim = next(iter(spots))         # any copy of the value
        spots.discard(victim)
        last = self.items[-1]
        if victim != len(self.items) - 1:
            self.items[victim] = last      # the last slot fills the hole
            self.where[last].discard(len(self.items) - 1)
            self.where[last].add(victim)
        self.items.pop()
        return True

    def getRandom(self):
        return random.choice(self.items)   # uniform, constant time""",
        },
    },
    {
        "slug": "minimum-cost-to-reach-destination-in-time",
        "title": "Minimum Cost to Reach Destination in Time",
        "difficulty": "Hard",
        "pattern": "Dijkstra over (node, time) states",
        "statement": "The country has n cities joined by bidirectional roads, where edges[i] = [x, y, time] says travelling that road takes time "
                     "minutes. You pay passingFees[i] every time you pass through city i. Return the cheapest way from city 0 to city n-1 that "
                     "finishes within maxTime minutes, or -1.",
        "examples": [("maxTime = 30, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3]", "11"),
                     ("maxTime = 29, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3]", "48"),
                     ("maxTime = 25, edges = [[0,1,10],[1,2,10],[2,5,10],[0,3,1],[3,4,10],[4,5,15]], passingFees = [5,1,2,20,20,3]", "-1")],
        "constraints": ["1 <= n <= 1000", "1 <= edges.length <= 1000", "2 <= time_i <= 1000", "1 <= passingFees[i] <= 1000",
                        "1 <= maxTime <= 1000", "passingFees.length == n and each road is [x, y, time]"],
        "approach": "Time is a resource, not just a weight, so cost alone cannot be the state: arriving later can be cheaper, and arriving cheaper "
                     "can be too late. The Dijkstra state is therefore the pair (city, minutes spent) and the distance is the fee paid — starting at "
                     "city 0 costs its own fee and every step adds the fee of the city you enter. The heap settles states in order of cost, so the "
                     "first settled state that reaches the destination within maxTime is the answer.",
        "complexity": ("O(maxTime · n log(maxTime · n)) in the worst case", "O(maxTime · n)"),
        "code": {
            "cpp": r"""// Dijkstra over (city, minutes spent); the distance is the fee paid
int minCost(int maxTime, vector<vector<int>>& edges, vector<int>& fees) {
    int n = fees.size();
    vector<vector<pair<int,int>>> adj(n);                    // city -> (neighbour, time)
    for (auto& e : edges) {
        adj[e[0]].push_back({e[1], e[2]});
        adj[e[1]].push_back({e[0], e[2]});
    }
    const int INF = 1e9;
    vector<vector<int>> best(n, vector<int>(maxTime + 1, INF));   // fee per state
    vector<vector<bool>> done(n, vector<bool>(maxTime + 1, false));
    priority_queue<array<int,3>, vector<array<int,3>>, greater<>> pq;   // (fee, city, time)
    best[0][0] = fees[0];                            // entering city 0 costs its own fee
    pq.push({fees[0], 0, 0});
    int answer = INF;
    while (!pq.empty()) {
        auto [cost, u, t] = pq.top(); pq.pop();
        if (done[u][t]) continue;                    // a cheaper state is already settled
        done[u][t] = true;
        if (u == n - 1) { answer = min(answer, cost); continue; }
        for (auto [v, dt] : adj[u]) {
            int nt = t + dt;
            if (nt > maxTime) continue;              // the ride would run out of time
            int nc = cost + fees[v];
            if (nc < best[v][nt]) { best[v][nt] = nc; pq.push({nc, v, nt}); }
        }
    }
    return answer == INF ? -1 : answer;
}   // O(maxTime · n log(maxTime · n)) time · O(maxTime · n) space""",
            "java": r"""// Dijkstra over (city, minutes spent); the distance is the fee paid
int minCost(int maxTime, int[][] edges, int[] fees) {
    int n = fees.length;
    List<List<int[]>> adj = new ArrayList<>();       // city -> {neighbour, time}
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) {
        adj.get(e[0]).add(new int[]{e[1], e[2]});
        adj.get(e[1]).add(new int[]{e[0], e[2]});
    }
    final int INF = 1_000_000_000;
    int[][] best = new int[n][maxTime + 1];          // fee per (city, time) state
    for (int[] row : best) Arrays.fill(row, INF);
    boolean[][] done = new boolean[n][maxTime + 1];
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);   // (fee, city, time)
    best[0][0] = fees[0];                            // entering city 0 costs its own fee
    pq.add(new int[]{fees[0], 0, 0});
    int answer = INF;
    while (!pq.isEmpty()) {
        int[] cur = pq.poll();
        int cost = cur[0], u = cur[1], t = cur[2];
        if (done[u][t]) continue;                    // a cheaper state is already settled
        done[u][t] = true;
        if (u == n - 1) { answer = Math.min(answer, cost); continue; }
        for (int[] e : adj.get(u)) {
            int nt = t + e[1];
            if (nt > maxTime) continue;              // the ride would run out of time
            int nc = cost + fees[e[0]];
            if (nc < best[e[0]][nt]) { best[e[0]][nt] = nc; pq.add(new int[]{nc, e[0], nt}); }
        }
    }
    return answer == INF ? -1 : answer;
}   // O(maxTime · n log(maxTime · n)) time · O(maxTime · n) space""",
            "python": r"""import heapq

def min_cost(max_time, edges, passing_fees):
    n = len(passing_fees)
    adj = [[] for _ in range(n)]                 # city -> [(neighbour, time)]
    for u, v, t in edges:
        adj[u].append((v, t))
        adj[v].append((u, t))
    INF = float('inf')
    best = [[INF] * (max_time + 1) for _ in range(n)]   # fee per state
    best[0][0] = passing_fees[0]                 # entering city 0 costs its own fee
    pq = [(passing_fees[0], 0, 0)]               # (fee, city, minutes spent)
    answer = INF
    while pq:
        cost, u, t = heapq.heappop(pq)
        if cost > best[u][t]:
            continue                             # a cheaper state is already known
        if u == n - 1:
            answer = min(answer, cost)
            continue
        for v, dt in adj[u]:
            nt = t + dt
            if nt > max_time:
                continue                         # the ride would run out of time
            nc = cost + passing_fees[v]
            if nc < best[v][nt]:
                best[v][nt] = nc
                heapq.heappush(pq, (nc, v, nt))
    return -1 if answer == INF else answer""",
        },
    },
    {
        "slug": "minimize-deviation-in-array",
        "title": "Minimize Deviation in Array",
        "difficulty": "Hard",
        "pattern": "raise the odd values, then halve the maximum",
        "statement": "You may double odd numbers and halve even numbers any number of times. Return the smallest possible (maximum - minimum) of the "
                     "resulting array.",
        "examples": [("nums = [1,2,3,4]", "1"), ("nums = [4,1,5,20,3]", "3"), ("nums = [2,10,8]", "3")],
        "constraints": ["1 <= nums.length <= 5 · 10^4", "1 <= nums[i] <= 10^9", "halving applies only to even numbers"],
        "approach": "Doubling odd values first is free and makes every number reachable by halving alone, so the minimum can only ever be a value that "
                     "was on the board at some point. Repeatedly halve the current maximum and keep the running minimum; every such step is the only "
                     "move that can shrink the gap.",
        "complexity": ("O(n log n log(max value))", "O(n)"),
        "code": {
            "cpp": r"""// Double the odds, then repeatedly halve the current maximum
int minimumDeviation(vector<int>& nums) {
    priority_queue<int> pq;
    int smallest = INT_MAX;
    for (int x : nums) {
        if (x % 2) x *= 2;                       // odds can only be doubled first
        pq.push(x);
        smallest = min(smallest, x);
    }
    int best = pq.top() - smallest;
    while (pq.top() % 2 == 0) {                  // only evens can shrink
        int top = pq.top(); pq.pop();
        int halved = top / 2;
        pq.push(halved);
        smallest = min(smallest, halved);        // the minimum may fall
        best = min(best, pq.top() - smallest);
    }
    return best;
}   // O(n log n log(max value)) time · O(n) space""",
            "java": r"""// Double the odds, then repeatedly halve the current maximum
int minimumDeviation(int[] nums) {
    PriorityQueue<Integer> pq = new PriorityQueue<>(Collections.reverseOrder());
    int smallest = Integer.MAX_VALUE;
    for (int x : nums) {
        if (x % 2 == 1) x *= 2;                  // odds can only be doubled first
        pq.add(x);
        smallest = Math.min(smallest, x);
    }
    int best = pq.peek() - smallest;
    while (pq.peek() % 2 == 0) {                 // only evens can shrink
        int halved = pq.poll() / 2;
        pq.add(halved);
        smallest = Math.min(smallest, halved);   // the minimum may fall
        best = Math.min(best, pq.peek() - smallest);
    }
    return best;
}   // O(n log n log(max value)) time · O(n) space""",
            "python": r"""import heapq

def minimum_deviation(nums):
    heap = []
    smallest = float('inf')
    for x in nums:
        if x % 2:                    # an odd value can only be doubled first
            x *= 2
        heapq.heappush(heap, -x)
        smallest = min(smallest, x)
    best = -heap[0] - smallest
    while -heap[0] % 2 == 0:         # halving is allowed only for even values
        top = -heapq.heappop(heap)
        halved = top // 2
        heapq.heappush(heap, -halved)
        smallest = min(smallest, halved)          # the minimum may drop
        best = min(best, -heap[0] - smallest)
    return best""",
        },
    },
    {
        "slug": "maximum-number-of-robots-within-budget",
        "title": "Maximum Number of Robots Within Budget",
        "difficulty": "Hard",
        "pattern": "sliding window maximum with running costs",
        "statement": "Choosing robots i..j costs max(chargeTimes in the window) + k * sum(runningCosts in the window). Return the largest window "
                     "whose cost fits the budget.",
        "examples": [("chargeTimes = [3,6,1,3,4], runningCosts = [2,1,3,4,5], budget = 25", "3"),
                     ("chargeTimes = [11,12,19], runningCosts = [10,8,7], budget = 19", "0")],
        "constraints": ["1 <= robots <= 5 · 10^4", "1 <= chargeTimes[i], runningCosts[i] <= 10^5", "0 <= budget <= 10^15"],
        "approach": "For a window, the charge term is its maximum and the cost term is its sum, so a monotonic deque supplies the maximum in "
                     "constant amortised time while a running sum tracks the costs. Whenever the window is too expensive, drop the left end — the "
                     "cost is monotone in the window, so that is the only repair needed.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Grow a window; track its max with a deque and its cost with a running sum
int maximumRobots(vector<int>& chargeTimes, vector<int>& runningCosts, long long budget) {
    deque<int> dq;                               // indices with decreasing charge time
    long long costSum = 0, best = 0;
    int left = 0;
    for (int right = 0; right < (int)chargeTimes.size(); right++) {
        while (!dq.empty() && chargeTimes[dq.back()] <= chargeTimes[right])
            dq.pop_back();                       // this robot dominates them
        dq.push_back(right);
        costSum += runningCosts[right];
        while (left <= right &&
               (long long)chargeTimes[dq.front()] + (right - left + 1) * costSum > budget) {
            costSum -= runningCosts[left];       // shrink from the left
            if (dq.front() == left) dq.pop_front();
            left++;
        }
        best = max(best, (long long)(right - left + 1));
    }
    return (int) best;
}   // O(n) time · O(n) space""",
            "java": r"""// Grow a window; track its max with a deque and its cost with a running sum
int maximumRobots(int[] chargeTimes, int[] runningCosts, long budget) {
    Deque<Integer> dq = new ArrayDeque<>();      // indices with decreasing charge
    long costSum = 0, best = 0;
    int left = 0;
    for (int right = 0; right < chargeTimes.length; right++) {
        while (!dq.isEmpty() && chargeTimes[dq.peekLast()] <= chargeTimes[right])
            dq.pollLast();                       // this robot dominates them
        dq.addLast(right);
        costSum += runningCosts[right];
        while (left <= right &&
               chargeTimes[dq.peekFirst()] + (long)(right - left + 1) * costSum > budget) {
            costSum -= runningCosts[left];       // shrink from the left
            if (dq.peekFirst() == left) dq.pollFirst();
            left++;
        }
        best = Math.max(best, right - left + 1);
    }
    return (int) best;
}   // O(n) time · O(n) space""",
            "python": r"""from collections import deque

def maximum_robots(charge_times, running_costs, budget):
    dq = deque()                     # indices with decreasing charge time
    cost_sum = 0
    best = 0
    left = 0
    for right in range(len(charge_times)):
        while dq and charge_times[dq[-1]] <= charge_times[right]:
            dq.pop()                 # this robot dominates the ones behind
        dq.append(right)
        cost_sum += running_costs[right]
        while left <= right and charge_times[dq[0]] + (right - left + 1) * cost_sum > budget:
            cost_sum -= running_costs[left]      # shrink from the left
            if dq[0] == left:
                dq.popleft()
            left += 1
        best = max(best, right - left + 1)
    return best""",
        },
    },
]
