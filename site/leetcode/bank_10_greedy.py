# Topic 10 · Greedy & Intervals
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.

TOPIC = {
    "name": "Greedy & Intervals",
    "tagline": "Sort first, then prove one pass is enough — greedy without a proof is just a guess.",
    "focus": "Almost every greedy problem here starts with a sort, and the sort key *is* the insight: by end time for interval scheduling, by "
             "ratio for fractional resources, by deadline for course scheduling. Intervals are their own family (merge, insert, cover, shoot, count "
             "overlaps). The hard tier adds a second structure on top of the greedy sweep — a heap that can undo a choice, or a binary search that "
             "turns a feasibility check into an answer.",
    "ordering": "easy 1–6 are single sorts with one pass; medium 1–2 are the jump-game reach family, 3–5 are interval merging and insertion, 6–7 are "
                "circular sweeps and last-occurrence cuts, 8–10 are schedules and exchange arguments, 11–12 are coverage counting; hard 1–3 are "
                "two-pass and deadline arguments, 4–6 are heaps that undo earlier choices, 7–9 combine greedy with binary search or sorting proofs, "
                "10–12 are the hardest assignment and window problems.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "assign-cookies",
        "title": "Assign Cookies",
        "difficulty": "Easy",
        "pattern": "sort both sides, match the smallest that fits",
        "statement": "Each child i wants a cookie of size at least g[i], and each cookie j has size s[j] and can be given to at most one child. "
                     "Return the maximum number of content children.",
        "examples": [("g = [1,2,3], s = [1,1]", "1"), ("g = [1,2], s = [1,2,3]", "2")],
        "constraints": ["1 <= number of children, cookies <= 3 · 10^4", "1 <= g[i], s[j] <= 2^31 - 1", "a cookie satisfies one child"],
        "approach": "Sort both lists. Offer the smallest unassigned cookie to the least demanding unassigned child: if it fits, both advance; if "
                     "not, the cookie is too small for *everyone* and can be skipped. Never giving a large cookie where a small one works is what "
                     "keeps the matching maximal.",
        "complexity": ("O(n log n + m log m)", "O(1) beyond the sorts"),
        "code": {
            "cpp": r"""// Two pointers on sorted lists: smallest cookie to least demanding child
int findContentChildren(vector<int>& g, vector<int>& s) {
    sort(g.begin(), g.end());
    sort(s.begin(), s.end());
    int child = 0, cookie = 0;
    while (child < (int)g.size() && cookie < (int)s.size()) {
        if (s[cookie] >= g[child]) child++;      // this cookie satisfies the child
        cookie++;                                // either way, the cookie is gone
    }
    return child;
}   // O(n log n + m log m) time · O(1) extra space""",
            "java": r"""// Two pointers on sorted lists: smallest cookie to least demanding child
int findContentChildren(int[] g, int[] s) {
    Arrays.sort(g);
    Arrays.sort(s);
    int child = 0, cookie = 0;
    while (child < g.length && cookie < s.length) {
        if (s[cookie] >= g[child]) child++;      // this cookie satisfies the child
        cookie++;                                // either way, the cookie is gone
    }
    return child;
}   // O(n log n + m log m) time · O(1) extra space""",
            "python": r"""def find_content_children(g, s):
    g.sort()
    s.sort()
    child = cookie = 0
    while child < len(g) and cookie < len(s):
        if s[cookie] >= g[child]:      # this cookie satisfies the child
            child += 1
        cookie += 1                    # either way the cookie is used up
    return child""",
        },
    },
    {
        "slug": "lemonade-change",
        "title": "Lemonade Change",
        "difficulty": "Easy",
        "pattern": "greedy change-making with limited denominations",
        "statement": "Each lemonade costs 5 and customers pay with 5, 10 or 20 in order. Return whether every customer can be given correct change "
                     "from the notes collected so far.",
        "examples": [("bills = [5,5,5,10,20]", "true"), ("bills = [5,5,10,10,20]", "false")],
        "constraints": ["1 <= bills.length <= 10^5", "bills[i] is 5, 10 or 20", "change is given in the order customers arrive"],
        "approach": "Only the counts of 5s and 10s matter, since 20s are never handed back. The one real decision is for a 20: prefer giving a 10 "
                     "plus a 5, because 5s are the more flexible note and using three of them starves later customers.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Track 5s and 10s; for a 20 prefer 10 + 5 over three 5s
bool lemonadeChange(vector<int>& bills) {
    int fives = 0, tens = 0;
    for (int b : bills) {
        if (b == 5) fives++;
        else if (b == 10) { if (!fives) return false; fives--; tens++; }
        else {
            if (tens && fives) { tens--; fives--; }        // best use of a 10
            else if (fives >= 3) fives -= 3;               // only if forced
            else return false;
        }
    }
    return true;
}   // O(n) time · O(1) space""",
            "java": r"""// Track 5s and 10s; for a 20 prefer 10 + 5 over three 5s
boolean lemonadeChange(int[] bills) {
    int fives = 0, tens = 0;
    for (int b : bills) {
        if (b == 5) fives++;
        else if (b == 10) { if (fives == 0) return false; fives--; tens++; }
        else {
            if (tens > 0 && fives > 0) { tens--; fives--; }   // best use of a 10
            else if (fives >= 3) fives -= 3;                  // only if forced
            else return false;
        }
    }
    return true;
}   // O(n) time · O(1) space""",
            "python": r"""def lemonade_change(bills):
    fives = tens = 0
    for b in bills:
        if b == 5:
            fives += 1
        elif b == 10:
            if not fives:
                return False
            fives -= 1
            tens += 1
        else:
            if tens and fives:          # prefer handing back a 10 plus a 5
                tens -= 1
                fives -= 1
            elif fives >= 3:            # only if no 10 is left
                fives -= 3
            else:
                return False
    return True""",
        },
    },
    {
        "slug": "largest-perimeter-triangle",
        "title": "Largest Perimeter Triangle",
        "difficulty": "Easy",
        "pattern": "sort, then test only adjacent triples",
        "statement": "Given side lengths, choose three that form a triangle with the largest perimeter, and return that perimeter or 0 if none exists.",
        "examples": [("nums = [2,1,2]", "5"), ("nums = [1,2,1,10]", "0")],
        "constraints": ["3 <= nums.length <= 10^4", "1 <= nums[i] <= 10^6", "a triangle needs a + b > c"],
        "approach": "Sort the sides. For a fixed largest side c, the best pair of smaller sides is the two just below it, so a single backward scan over "
                     "adjacent triples suffices: the first triple satisfying a + b > c is the answer, because any smaller pair gives a shorter "
                     "perimeter and any larger c was already rejected.",
        "complexity": ("O(n log n)", "O(1)"),
        "code": {
            "cpp": r"""// Sorted, the best triple is always three adjacent sides
int largestPerimeter(vector<int>& nums) {
    sort(nums.begin(), nums.end());
    for (int i = nums.size() - 1; i >= 2; i--)
        if (nums[i-2] + nums[i-1] > nums[i])      // the triangle inequality
            return nums[i-2] + nums[i-1] + nums[i];
    return 0;                                     // no triple works
}   // O(n log n) time · O(1) space""",
            "java": r"""// Sorted, the best triple is always three adjacent sides
int largestPerimeter(int[] nums) {
    Arrays.sort(nums);
    for (int i = nums.length - 1; i >= 2; i--)
        if (nums[i-2] + nums[i-1] > nums[i])      // the triangle inequality
            return nums[i-2] + nums[i-1] + nums[i];
    return 0;                                     // no triple works
}   // O(n log n) time · O(1) space""",
            "python": r"""def largest_perimeter(nums):
    nums.sort()
    for i in range(len(nums) - 1, 1, -1):
        if nums[i-2] + nums[i-1] > nums[i]:      # triangle inequality holds
            return nums[i-2] + nums[i-1] + nums[i]
    return 0                                     # no triple forms a triangle""",
        },
    },
    {
        "slug": "can-place-flowers",
        "title": "Can Place Flowers",
        "difficulty": "Easy",
        "pattern": "greedy planting with a look-ahead rule",
        "statement": "Given a flowerbed where 1 means planted and 0 means empty, and flowers cannot be adjacent, decide whether n new flowers can be "
                     "planted.",
        "examples": [("flowerbed = [1,0,0,0,1], n = 1", "true"), ("flowerbed = [1,0,0,0,1], n = 2", "false")],
        "constraints": ["1 <= flowerbed.length <= 2 · 10^4", "flowerbed[i] is 0 or 1", "no two planted flowers are adjacent initially"],
        "approach": "Scan left to right and plant whenever the current cell and both neighbours are empty, treating the space beyond each end as "
                     "empty. Planting as early as possible never blocks a later slot, because any valid later slot needs its own left neighbour empty "
                     "too.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Plant greedily; the ends count as empty space
bool canPlaceFlowers(vector<int>& bed, int n) {
    int len = bed.size();
    for (int i = 0; i < len && n > 0; i++) {
        if (bed[i]) continue;
        bool leftFree = (i == 0) || bed[i-1] == 0;
        bool rightFree = (i == len - 1) || bed[i+1] == 0;
        if (leftFree && rightFree) { bed[i] = 1; n--; }   // plant here
    }
    return n == 0;
}   // O(n) time · O(1) space""",
            "java": r"""// Plant greedily; the ends count as empty space
boolean canPlaceFlowers(int[] bed, int n) {
    int len = bed.length;
    for (int i = 0; i < len && n > 0; i++) {
        if (bed[i] == 1) continue;
        boolean leftFree = (i == 0) || bed[i-1] == 0;
        boolean rightFree = (i == len - 1) || bed[i+1] == 0;
        if (leftFree && rightFree) { bed[i] = 1; n--; }   // plant here
    }
    return n == 0;
}   // O(n) time · O(1) space""",
            "python": r"""def can_place_flowers(flowerbed, n):
    length = len(flowerbed)
    for i in range(length):
        if n == 0:
            break
        if flowerbed[i] == 1:
            continue
        left_free = i == 0 or flowerbed[i-1] == 0
        right_free = i == length - 1 or flowerbed[i+1] == 0
        if left_free and right_free:
            flowerbed[i] = 1        # plant as early as possible
            n -= 1
    return n == 0""",
        },
    },
    {
        "slug": "maximum-units-on-a-truck",
        "title": "Maximum Units on a Truck",
        "difficulty": "Easy",
        "pattern": "sort by value density, fill the container",
        "statement": "Each box type has a count and a number of units per box. Load at most truckSize boxes, maximising the total units.",
        "examples": [("boxTypes = [[1,3],[2,2],[3,1]], truckSize = 4", "8"),
                     ("boxTypes = [[5,10],[2,5],[4,7],[3,9]], truckSize = 10", "91")],
        "constraints": ["1 <= number of box types <= 1000", "1 <= boxes per type, units per box <= 1000", "the truck holds any mix of types"],
        "approach": "This is the fractional knapsack with all-or-nothing boxes, and the exchange argument is short: if a lower-density box is loaded "
                     "while a higher-density one is left behind, swapping them can only help. Sort by density and take whole types until the truck "
                     "fills.",
        "complexity": ("O(t log t)", "O(1)"),
        "code": {
            "cpp": r"""// Sort by units per box; take whole types until the truck is full
int maximumUnits(vector<vector<int>>& boxTypes, int truckSize) {
    sort(boxTypes.begin(), boxTypes.end(),
         [](const vector<int>& a, const vector<int>& b) { return a[1] > b[1]; });
    int total = 0;
    for (auto& b : boxTypes) {
        if (truckSize == 0) break;
        int take = min(truckSize, b[0]);         // as many as still fit
        total += take * b[1];
        truckSize -= take;
    }
    return total;
}   // O(t log t) time · O(1) space""",
            "java": r"""// Sort by units per box; take whole types until the truck is full
int maximumUnits(int[][] boxTypes, int truckSize) {
    Arrays.sort(boxTypes, (a, b) -> b[1] - a[1]);   // densest first
    int total = 0;
    for (int[] b : boxTypes) {
        if (truckSize == 0) break;
        int take = Math.min(truckSize, b[0]);    // as many as still fit
        total += take * b[1];
        truckSize -= take;
    }
    return total;
}   // O(t log t) time · O(1) space""",
            "python": r"""def maximum_units(box_types, truck_size):
    box_types.sort(key=lambda b: -b[1])         # densest boxes first
    total = 0
    for count, units in box_types:
        if truck_size == 0:
            break
        take = min(truck_size, count)           # as many as still fit
        total += take * units
        truck_size -= take
    return total""",
        },
    },
    {
        "slug": "minimum-number-of-moves-to-seat-everyone",
        "title": "Minimum Number of Moves to Seat Everyone",
        "difficulty": "Easy",
        "pattern": "sort both arrays, pair them up",
        "statement": "There are n seats and n students at given positions. Moving a student one position costs one move. Seat everyone with the "
                     "fewest total moves.",
        "examples": [("seats = [3,1,5], students = [2,7,4]", "4"), ("seats = [4,1,5,9], students = [1,3,2,6]", "7")],
        "constraints": ["n == seats.length == students.length", "1 <= n <= 100", "1 <= positions <= 100"],
        "approach": "Sort both arrays and pair the k-th smallest seat with the k-th smallest student. If two students crossed over in the pairing, "
                     "uncrossing them never increases the total distance on a line — the standard exchange argument for matching on a line.",
        "complexity": ("O(n log n)", "O(1)"),
        "code": {
            "cpp": r"""// Pair sorted seats with sorted students: crossing pairs never help
int minMovesToSeat(vector<int>& seats, vector<int>& students) {
    sort(seats.begin(), seats.end());
    sort(students.begin(), students.end());
    int moves = 0;
    for (int i = 0; i < (int)seats.size(); i++)
        moves += abs(seats[i] - students[i]);
    return moves;
}   // O(n log n) time · O(1) space""",
            "java": r"""// Pair sorted seats with sorted students: crossing pairs never help
int minMovesToSeat(int[] seats, int[] students) {
    Arrays.sort(seats);
    Arrays.sort(students);
    int moves = 0;
    for (int i = 0; i < seats.length; i++)
        moves += Math.abs(seats[i] - students[i]);
    return moves;
}   // O(n log n) time · O(1) space""",
            "python": r"""def min_moves_to_seat(seats, students):
    seats.sort()
    students.sort()
    return sum(abs(a - b) for a, b in zip(seats, students))""",
        },
    },
    # ---------------------------------------------------------------- MEDIUM
    {
        "slug": "jump-game",
        "title": "Jump Game",
        "difficulty": "Medium",
        "pattern": "farthest reach so far",
        "statement": "From position i you may jump up to nums[i] steps forward. Starting at index 0, decide whether the last index is reachable.",
        "examples": [("nums = [2,3,1,1,4]", "true"), ("nums = [3,2,1,0,4]", "false")],
        "constraints": ["1 <= nums.length <= 10^4", "0 <= nums[i] <= 10^5", "the first position is always reachable"],
        "approach": "Track the farthest index reachable so far. Scanning left to right, the moment the current index passes that frontier the game is "
                     "lost — no earlier position can carry you further. Otherwise the answer is simply whether the frontier covers the last index.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Track the farthest reachable index; stop if you fall behind it
bool canJump(vector<int>& nums) {
    int reach = 0;
    for (int i = 0; i < (int)nums.size(); i++) {
        if (i > reach) return false;             // this index is unreachable
        reach = max(reach, i + nums[i]);         // extend the frontier
        if (reach >= (int)nums.size() - 1) return true;
    }
    return true;
}   // O(n) time · O(1) space""",
            "java": r"""// Track the farthest reachable index; stop if you fall behind it
boolean canJump(int[] nums) {
    int reach = 0;
    for (int i = 0; i < nums.length; i++) {
        if (i > reach) return false;             // this index is unreachable
        reach = Math.max(reach, i + nums[i]);    // extend the frontier
        if (reach >= nums.length - 1) return true;
    }
    return true;
}   // O(n) time · O(1) space""",
            "python": r"""def can_jump(nums):
    reach = 0
    for i, step in enumerate(nums):
        if i > reach:
            return False             # this index can never be reached
        reach = max(reach, i + step)  # extend the frontier
        if reach >= len(nums) - 1:
            return True
    return True""",
        },
    },
    {
        "slug": "jump-game-ii",
        "title": "Jump Game II",
        "difficulty": "Medium",
        "pattern": "greedy layers (BFS by reach)",
        "statement": "Return the minimum number of jumps needed to reach the last index, where each jump may cover at most nums[i] positions.",
        "examples": [("nums = [2,3,1,1,4]", "2"), ("nums = [2,3,0,1,4]", "2")],
        "constraints": ["1 <= nums.length <= 10^4", "0 <= nums[i] <= 1000", "the last index is always reachable"],
        "approach": "Instead of a jump-by-jump BFS, sweep the whole band of positions reachable with the current number of jumps and record how far "
                     "that band can extend. The frontier update *is* one level of the BFS, giving the level count in a single pass.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Sweep each BFS layer: current reach, and how far this layer extends
int jump(vector<int>& nums) {
    int jumps = 0, end = 0, farthest = 0;
    for (int i = 0; i < (int)nums.size() - 1; i++) {
        farthest = max(farthest, i + nums[i]);   // the whole layer's reach
        if (i == end) {                          // the layer is exhausted
            jumps++;                             // one more jump is needed
            end = farthest;                      // start the next layer
        }
    }
    return jumps;
}   // O(n) time · O(1) space""",
            "java": r"""// Sweep each BFS layer: current reach, and how far this layer extends
int jump(int[] nums) {
    int jumps = 0, end = 0, farthest = 0;
    for (int i = 0; i < nums.length - 1; i++) {
        farthest = Math.max(farthest, i + nums[i]);   // the whole layer's reach
        if (i == end) {                          // the layer is exhausted
            jumps++;                             // one more jump is needed
            end = farthest;                      // start the next layer
        }
    }
    return jumps;
}   // O(n) time · O(1) space""",
            "python": r"""def jump_game_ii(nums):
    jumps = end = farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])   # reach of the current layer
        if i == end:                            # the layer is exhausted
            jumps += 1                          # one more jump is needed
            end = farthest                      # move to the next layer
    return jumps""",
        },
    },
    {
        "slug": "merge-intervals",
        "title": "Merge Intervals",
        "difficulty": "Medium",
        "pattern": "sort by start, fuse overlapping runs",
        "statement": "Merge all overlapping intervals and return the non-overlapping intervals that cover the same ranges.",
        "examples": [("intervals = [[1,3],[2,6],[8,10],[15,18]]", "[[1,6],[8,10],[15,18]]"),
                     ("intervals = [[1,4],[4,5]]", "[[1,5]]")],
        "constraints": ["1 <= intervals.length <= 10^4", "0 <= start <= end <= 10^4", "touching intervals count as overlapping"],
        "approach": "Sorting by start means overlaps can only happen with the interval currently being built. If the next start falls inside it, "
                     "extend the end; otherwise the current interval is final. One pass after the sort is enough — no comparisons with earlier "
                     "intervals.",
        "complexity": ("O(n log n)", "O(n) for the output"),
        "code": {
            "cpp": r"""// Sort by start; only the interval being built can still overlap
vector<vector<int>> merge(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end());
    vector<vector<int>> out;
    for (auto& cur : intervals) {
        if (!out.empty() && cur[0] <= out.back()[1])
            out.back()[1] = max(out.back()[1], cur[1]);   // extend the run
        else
            out.push_back(cur);                           // start a new run
    }
    return out;
}   // O(n log n) time · O(n) space""",
            "java": r"""// Sort by start; only the interval being built can still overlap
int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
    List<int[]> out = new ArrayList<>();
    for (int[] cur : intervals) {
        if (!out.isEmpty() && cur[0] <= out.get(out.size()-1)[1])
            out.get(out.size()-1)[1] = Math.max(out.get(out.size()-1)[1], cur[1]);
        else
            out.add(new int[]{cur[0], cur[1]});          // start a new run
    }
    return out.toArray(new int[0][]);
}   // O(n log n) time · O(n) space""",
            "python": r"""def merge_intervals(intervals):
    intervals.sort()                     # by start, then by end
    out = []
    for start, end in intervals:
        if out and start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)   # extend the current run
        else:
            out.append([start, end])            # start a new run
    return out""",
        },
    },
    {
        "slug": "non-overlapping-intervals",
        "title": "Non-overlapping Intervals",
        "difficulty": "Medium",
        "pattern": "interval scheduling by earliest end time",
        "statement": "Remove the fewest intervals so the rest do not overlap. Return that minimum number of removals.",
        "examples": [("intervals = [[1,2],[2,3],[3,4],[1,3]]", "1"), ("intervals = [[1,2],[1,2],[1,2]]", "2"),
                     ("intervals = [[1,2],[2,3]]", "0")],
        "constraints": ["1 <= intervals.length <= 10^5", "intervals[i] = [start, end]", "touching intervals do not overlap"],
        "approach": "Equivalent to keeping the largest set of non-overlapping intervals, which the earliest-end-first rule solves: always keep the "
                     "interval that finishes soonest, because it leaves the most room. Between two intervals that end together, take the one that "
                     "starts earlier — it never blocks the other, while the reverse order does. Counting the kept intervals and subtracting gives the "
                     "removals.",
        "complexity": ("O(n log n)", "O(1)"),
        "code": {
            "cpp": r"""// Keep the interval that ends first; it blocks the least
int eraseOverlapIntervals(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end(), [](const vector<int>& a, const vector<int>& b) {
        return a[1] != b[1] ? a[1] < b[1] : a[0] < b[0];   // earliest end, then start
    });
    int kept = 0, lastEnd = INT_MIN;
    for (auto& iv : intervals)
        if (iv[0] >= lastEnd) {                  // no overlap with what we kept
            kept++;
            lastEnd = iv[1];
        }
    return intervals.size() - kept;
}   // O(n log n) time · O(1) space""",
            "java": r"""// Keep the interval that ends first; it blocks the least
int eraseOverlapIntervals(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[1] != b[1] ? a[1] - b[1] : a[0] - b[0]);   // end, start
    int kept = 0, lastEnd = Integer.MIN_VALUE;
    for (int[] iv : intervals)
        if (iv[0] >= lastEnd) {                  // no overlap with what we kept
            kept++;
            lastEnd = iv[1];
        }
    return intervals.length - kept;
}   // O(n log n) time · O(1) space""",
            "python": r"""def erase_overlap_intervals(intervals):
    intervals.sort(key=lambda iv: (iv[1], iv[0]))   # earliest end, then earliest start
    kept = 0
    last_end = float('-inf')
    for start, end in intervals:
        if start >= last_end:                # no overlap with what we kept
            kept += 1
            last_end = end
    return len(intervals) - kept""",
        },
    },
    {
        "slug": "insert-interval",
        "title": "Insert Interval",
        "difficulty": "Medium",
        "pattern": "three-phase linear walk",
        "statement": "Insert a new interval into a sorted list of non-overlapping intervals, merging where needed, and return the result.",
        "examples": [("intervals = [[1,3],[6,9]], newInterval = [2,5]", "[[1,5],[6,9]]"),
                     ("intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]", "[[1,2],[3,10],[12,16]]")],
        "constraints": ["0 <= intervals.length <= 10^4", "intervals are sorted by start and non-overlapping", "the new interval may overlap many"],
        "approach": "Because the list is already sorted, the work splits into three runs: intervals entirely before the new one, a block that "
                     "overlaps it (whose union is found by min of starts and max of ends), and everything after. The merge is done on the fly "
                     "without any search.",
        "complexity": ("O(n)", "O(n) for the output"),
        "code": {
            "cpp": r"""// Three phases: before, overlapping, after — all in one pass
vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& nw) {
    vector<vector<int>> out;
    int i = 0, n = intervals.size();
    while (i < n && intervals[i][1] < nw[0]) out.push_back(intervals[i++]);   // before
    while (i < n && intervals[i][0] <= nw[1]) {          // overlapping block
        nw[0] = min(nw[0], intervals[i][0]);
        nw[1] = max(nw[1], intervals[i][1]);
        i++;
    }
    out.push_back(nw);
    while (i < n) out.push_back(intervals[i++]);         // after
    return out;
}   // O(n) time · O(n) space""",
            "java": r"""// Three phases: before, overlapping, after — all in one pass
int[][] insert(int[][] intervals, int[] nw) {
    List<int[]> out = new ArrayList<>();
    int i = 0, n = intervals.length;
    while (i < n && intervals[i][1] < nw[0]) out.add(intervals[i++]);   // before
    while (i < n && intervals[i][0] <= nw[1]) {          // overlapping block
        nw[0] = Math.min(nw[0], intervals[i][0]);
        nw[1] = Math.max(nw[1], intervals[i][1]);
        i++;
    }
    out.add(new int[]{nw[0], nw[1]});
    while (i < n) out.add(intervals[i++]);               // after
    return out.toArray(new int[0][]);
}   // O(n) time · O(n) space""",
            "python": r"""def insert_interval(intervals, new_interval):
    out = []
    i, n = 0, len(intervals)
    start, end = new_interval
    while i < n and intervals[i][1] < start:      # entirely before
        out.append(intervals[i]); i += 1
    while i < n and intervals[i][0] <= end:       # overlapping block
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    out.append([start, end])
    out.extend(intervals[i:])                     # entirely after
    return out""",
        },
    },
    {
        "slug": "gas-station",
        "title": "Gas Station",
        "difficulty": "Medium",
        "pattern": "single pass with a resetting start",
        "statement": "Station i gives gas[i] fuel and reaching station i+1 costs cost[i]. Starting with an empty tank at some station, return the "
                     "index of a station from which the whole circle can be driven, or -1.",
        "examples": [("gas = [1,2,3,4,5], cost = [3,4,5,1,2]", "3"),
                     ("gas = [2,3,4], cost = [3,4,3]", "-1")],
        "constraints": ["1 <= stations <= 10^5", "gas[i], cost[i] are non-negative", "the answer is unique when it exists"],
        "approach": "Two facts make one pass enough: the trip is possible exactly when total gas covers total cost, and any start that runs dry "
                     "cannot be the answer, nor can any station before it — so the search simply restarts after each failure.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Restart the candidate start whenever the tank runs dry
int canCompleteCircuit(vector<int>& gas, vector<int>& cost) {
    int total = 0, tank = 0, start = 0;
    for (int i = 0; i < (int)gas.size(); i++) {
        int delta = gas[i] - cost[i];
        total += delta;
        tank += delta;
        if (tank < 0) {                          // cannot cross this gap from start
            start = i + 1;                       // move the candidate forward
            tank = 0;
        }
    }
    return total >= 0 ? start : -1;              // feasible only if the sum holds
}   // O(n) time · O(1) space""",
            "java": r"""// Restart the candidate start whenever the tank runs dry
int canCompleteCircuit(int[] gas, int[] cost) {
    int total = 0, tank = 0, start = 0;
    for (int i = 0; i < gas.length; i++) {
        int delta = gas[i] - cost[i];
        total += delta;
        tank += delta;
        if (tank < 0) {                          // cannot cross this gap from start
            start = i + 1;                       // move the candidate forward
            tank = 0;
        }
    }
    return total >= 0 ? start : -1;              // feasible only if the sum holds
}   // O(n) time · O(1) space""",
            "python": r"""def can_complete_circuit(gas, cost):
    total = tank = 0
    start = 0
    for i in range(len(gas)):
        delta = gas[i] - cost[i]
        total += delta
        tank += delta
        if tank < 0:                 # cannot cross this gap from start
            start = i + 1            # so no station up to here is the answer
            tank = 0
    return start if total >= 0 else -1""",
        },
    },
    {
        "slug": "partition-labels",
        "title": "Partition Labels",
        "difficulty": "Medium",
        "pattern": "last occurrence as the cut boundary",
        "statement": "Split the string into as many parts as possible so that each letter appears in at most one part, and return the sizes of those "
                     "parts.",
        "examples": [("s = \"ababcbacadefegdehijhklij\"", "[9,7,8]"), ("s = \"eccbbbbdec\"", "[10]")],
        "constraints": ["1 <= s.length <= 500", "s contains lowercase English letters", "parts are contiguous and cover the whole string"],
        "approach": "The last occurrence of a letter is the earliest position its part can end. Sweep forward keeping the farthest last occurrence "
                     "seen so far; when the current index catches it, the part is complete and cannot affect anything to the right.",
        "complexity": ("O(n)", "O(1) beyond the output"),
        "code": {
            "cpp": r"""// A part must reach the last occurrence of every letter inside it
vector<int> partitionLabels(string s) {
    int last[26];
    for (int i = 0; i < (int)s.size(); i++) last[s[i] - 'a'] = i;
    vector<int> parts;
    int start = 0, end = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        end = max(end, last[s[i] - 'a']);        // the part must stretch this far
        if (i == end) {                          // every letter is contained now
            parts.push_back(end - start + 1);
            start = i + 1;
        }
    }
    return parts;
}   // O(n) time · O(1) extra space""",
            "java": r"""// A part must reach the last occurrence of every letter inside it
List<Integer> partitionLabels(String s) {
    int[] last = new int[26];
    for (int i = 0; i < s.length(); i++) last[s.charAt(i) - 'a'] = i;
    List<Integer> parts = new ArrayList<>();
    int start = 0, end = 0;
    for (int i = 0; i < s.length(); i++) {
        end = Math.max(end, last[s.charAt(i) - 'a']);   // stretch as needed
        if (i == end) {                          // every letter is contained now
            parts.add(end - start + 1);
            start = i + 1;
        }
    }
    return parts;
}   // O(n) time · O(1) extra space""",
            "python": r"""def partition_labels(s):
    last = {ch: i for i, ch in enumerate(s)}    # last position of each letter
    parts = []
    start = end = 0
    for i, ch in enumerate(s):
        end = max(end, last[ch])       # the part must reach this letter's last
        if i == end:                   # every letter is fully contained
            parts.append(end - start + 1)
            start = i + 1
    return parts""",
        },
    },
    {
        "slug": "task-scheduler",
        "title": "Task Scheduler",
        "difficulty": "Medium",
        "pattern": "counting formula around the most frequent task",
        "statement": "The CPU runs one task per interval, and equal tasks must be separated by at least n intervals of cooldown (which may be idle). "
                     "Return the minimum number of intervals to finish all tasks.",
        "examples": [("tasks = [\"A\",\"A\",\"A\",\"B\",\"B\",\"B\"], n = 2", "8"),
                     ("tasks = [\"A\",\"C\",\"A\",\"B\",\"D\",\"B\"], n = 1", "6"),
                     ("tasks = [\"A\",\"A\",\"A\",\"B\",\"B\",\"B\"], n = 3", "10")],
        "constraints": ["1 <= tasks.length <= 10^4", "tasks[i] is an uppercase letter", "0 <= n <= 100"],
        "approach": "Line up the most frequent task with cooldown gaps after each copy: that frame is (maxFreq - 1) * (n + 1) plus however many tasks "
                     "share the maximum frequency. If other tasks are numerous enough to fill every gap, idle time disappears and the answer is "
                     "just the task count.",
        "complexity": ("O(t)", "O(1) — 26 letters"),
        "code": {
            "cpp": r"""// Frame the most frequent task, then check whether the gaps are all filled
int leastInterval(vector<char>& tasks, int n) {
    int counts[26] = {0};
    for (char t : tasks) counts[t - 'A']++;
    int maxFreq = 0, maxCount = 0;
    for (int c : counts) maxFreq = max(maxFreq, c);
    for (int c : counts) if (c == maxFreq) maxCount++;
    int framed = (maxFreq - 1) * (n + 1) + maxCount;
    return max(framed, (int)tasks.size());       // enough tasks ⇒ no idle time
}   // O(t) time · O(1) space""",
            "java": r"""// Frame the most frequent task, then check whether the gaps are all filled
int leastInterval(char[] tasks, int n) {
    int[] counts = new int[26];
    for (char t : tasks) counts[t - 'A']++;
    int maxFreq = 0, maxCount = 0;
    for (int c : counts) maxFreq = Math.max(maxFreq, c);
    for (int c : counts) if (c == maxFreq) maxCount++;
    int framed = (maxFreq - 1) * (n + 1) + maxCount;
    return Math.max(framed, tasks.length);       // enough tasks ⇒ no idle time
}   // O(t) time · O(1) space""",
            "python": r"""from collections import Counter

def least_interval(tasks, n):
    counts = Counter(tasks)
    max_freq = max(counts.values())
    max_count = sum(1 for c in counts.values() if c == max_freq)
    framed = (max_freq - 1) * (n + 1) + max_count   # the most frequent task's frame
    return max(framed, len(tasks))                  # extra tasks fill every gap""",
        },
    },
    {
        "slug": "queue-reconstruction-by-height",
        "title": "Queue Reconstruction by Height",
        "difficulty": "Medium",
        "pattern": "sort by one key, insert by the other",
        "statement": "Each person is [h, k] where k is the number of people at least as tall standing in front. Rebuild one valid queue.",
        "examples": [("people = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]", "[[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]"),
                     ("people = [[6,0],[5,0],[4,0],[3,2],[2,2],[1,4]]", "[[4,0],[5,0],[2,2],[3,2],[1,4],[6,0]]")],
        "constraints": ["1 <= people.length <= 2000", "0 <= h <= 10^5", "0 <= k < people.length"],
        "approach": "Process people from tallest to shortest; ties with the smaller k first. Inserting each person at index k works because everyone "
                     "already placed is at least as tall, so only their count matters — and the shorter people added later are invisible to the "
                     "requirement.",
        "complexity": ("O(n²) with list insertion", "O(n)"),
        "code": {
            "cpp": r"""// Tallest first, insert at index k: later (shorter) people never count
vector<vector<int>> reconstructQueue(vector<vector<int>>& people) {
    sort(people.begin(), people.end(), [](const vector<int>& a, const vector<int>& b) {
        return a[0] == b[0] ? a[1] < b[1] : a[0] > b[0];   // tall first, small k first
    });
    vector<vector<int>> out;
    for (auto& p : people) out.insert(out.begin() + p[1], p);
    return out;
}   // O(n²) time · O(n) space""",
            "java": r"""// Tallest first, insert at index k: later (shorter) people never count
int[][] reconstructQueue(int[][] people) {
    Arrays.sort(people, (a, b) -> a[0] == b[0] ? a[1] - b[1] : b[0] - a[0]);
    List<int[]> out = new ArrayList<>();
    for (int[] p : people) out.add(p[1], p);     // insert where exactly k are taller
    return out.toArray(new int[0][]);
}   // O(n²) time · O(n) space""",
            "python": r"""def reconstruct_queue(people):
    people.sort(key=lambda p: (-p[0], p[1]))     # tall first, small k first
    out = []
    for person in people:
        out.insert(person[1], person)            # exactly k taller people ahead
    return out""",
        },
    },
    {
        "slug": "two-city-scheduling",
        "title": "Two City Scheduling",
        "difficulty": "Medium",
        "pattern": "exchange argument on the cost difference",
        "statement": "Send exactly n people to city A and n to city B, where each person has a different cost for each city. Minimise the total cost.",
        "examples": [("costs = [[10,20],[30,200],[400,50],[30,20]]", "110"),
                     ("costs = [[259,770],[448,54],[926,667],[184,139],[840,118],[577,469]]", "1859"),
                     ("costs = [[515,563],[451,713],[537,709],[343,819],[855,779],[457,60],[650,359],[631,42]]", "3086")],
        "constraints": ["2 <= costs.length <= 100, even", "1 <= costs[i][0], costs[i][1] <= 1000", "exactly half go to each city"],
        "approach": "Start by sending everyone to A. Switching person i to B changes the total by cost[i][1] - cost[i][0], so the best n switches "
                     "are simply the n smallest differences. The exchange argument is one line, and the sort makes it concrete.",
        "complexity": ("O(n log n)", "O(1)"),
        "code": {
            "cpp": r"""// Switching a person from A to B changes the total by diff = b - a
int twoCitySchedCost(vector<vector<int>>& costs) {
    sort(costs.begin(), costs.end(), [](const vector<int>& x, const vector<int>& y) {
        return (x[1] - x[0]) < (y[1] - y[0]);    // biggest savings from switching
    });
    int n = costs.size() / 2, total = 0;
    for (int i = 0; i < n; i++) total += costs[i][1] + costs[i + n][0];   // big savers to B
    return total;
}   // O(n log n) time · O(1) space""",
            "java": r"""// Switching a person from A to B changes the total by diff = b - a
int twoCitySchedCost(int[][] costs) {
    Arrays.sort(costs, (x, y) -> (x[1] - x[0]) - (y[1] - y[0]));
    int n = costs.length / 2, total = 0;
    for (int i = 0; i < n; i++) total += costs[i][1] + costs[i + n][0];   // big savers to B
    return total;
}   // O(n log n) time · O(1) space""",
            "python": r"""def two_city_sched_cost(costs):
    costs.sort(key=lambda c: c[1] - c[0])   # biggest saving from switching to B
    n = len(costs) // 2
    return sum(costs[i][1] for i in range(n)) + \
           sum(costs[n + i][0] for i in range(n))""",
        },
    },
    {
        "slug": "minimum-number-of-arrows-to-burst-balloons",
        "title": "Minimum Number of Arrows to Burst Balloons",
        "difficulty": "Medium",
        "pattern": "interval stabbing by earliest end",
        "statement": "Each balloon spans xstart to xend, and an arrow shot at x bursts every balloon containing x. Return the fewest arrows that burst "
                     "all balloons.",
        "examples": [("points = [[10,16],[2,8],[1,6],[7,12]]", "2"),
                     ("points = [[1,2],[3,4],[5,6],[7,8]]", "4"),
                     ("points = [[1,2],[2,3],[3,4],[4,5]]", "2")],
        "constraints": ["1 <= points.length <= 10^5", "0 <= xstart <= xend <= 10^9", "arrows may be shot at any real position"],
        "approach": "Same earliest-end-first rule as interval scheduling: shoot at the end of the first unfinished balloon, burst everything that "
                     "contains that point, and repeat. Shooting later can only lose balloons, so this is optimal.",
        "complexity": ("O(n log n)", "O(1)"),
        "code": {
            "cpp": r"""// Shoot at the end of the earliest finishing balloon
int findMinArrowShots(vector<vector<int>>& points) {
    sort(points.begin(), points.end(),
         [](const vector<int>& a, const vector<int>& b) { return a[1] < b[1]; });
    int arrows = 0;
    long long shot = LLONG_MIN;
    for (auto& p : points)
        if (p[0] > shot) {                       // this balloon is not yet burst
            arrows++;
            shot = p[1];                         // shoot as far right as allowed
        }
    return arrows;
}   // O(n log n) time · O(1) space""",
            "java": r"""// Shoot at the end of the earliest finishing balloon
int findMinArrowShots(int[][] points) {
    Arrays.sort(points, (a, b) -> Integer.compare(a[1], b[1]));
    int arrows = 0;
    long shot = Long.MIN_VALUE;
    for (int[] p : points)
        if (p[0] > shot) {                       // this balloon is not yet burst
            arrows++;
            shot = p[1];                         // shoot as far right as allowed
        }
    return arrows;
}   // O(n log n) time · O(1) space""",
            "python": r"""def find_min_arrow_shots(points):
    points.sort(key=lambda p: p[1])       # earliest finishing balloon first
    arrows = 0
    shot = float('-inf')
    for start, end in points:
        if start > shot:                  # this balloon is still intact
            arrows += 1
            shot = end                    # shoot at its right edge
    return arrows""",
        },
    },
    {
        "slug": "car-pooling",
        "title": "Car Pooling",
        "difficulty": "Medium",
        "pattern": "sweep line with a running load",
        "statement": "Trips are [numPassengers, from, to] — passengers leave at 'to'. With a fixed car capacity, decide whether every trip can be "
                     "served.",
        "examples": [("trips = [[2,1,5],[3,3,7]], capacity = 4", "false"),
                     ("trips = [[2,1,5],[3,3,7]], capacity = 5", "true")],
        "constraints": ["1 <= trips.length <= 1000", "0 <= from < to <= 1000", "1 <= capacity <= 10^5"],
        "approach": "Turn each trip into two events with a sign: passengers boarding add to the load, passengers alighting subtract. Sorting the "
                     "events by location and keeping a running total is the sweep-line pattern that recurs in every load-over-time problem.",
        "complexity": ("O(n log n)", "O(n)"),
        "code": {
            "cpp": r"""// Turn trips into +/− events and sweep them in location order
bool carPooling(vector<vector<int>>& trips, int capacity) {
    vector<pair<int,int>> events;                // (location, delta)
    for (auto& t : trips) {
        events.push_back({t[1], t[0]});          // passengers board
        events.push_back({t[2], -t[0]});         // passengers alight
    }
    sort(events.begin(), events.end());
    int load = 0;
    for (auto& [pos, delta] : events) {
        load += delta;
        if (load > capacity) return false;       // too heavy on this stretch
    }
    return true;
}   // O(n log n) time · O(n) space""",
            "java": r"""// Turn trips into +/− events and sweep them in location order
boolean carPooling(int[][] trips, int capacity) {
    List<int[]> events = new ArrayList<>();      // (location, delta)
    for (int[] t : trips) {
        events.add(new int[]{t[1], t[0]});       // passengers board
        events.add(new int[]{t[2], -t[0]});      // passengers alight
    }
    events.sort((a, b) -> a[0] - b[0]);
    int load = 0;
    for (int[] e : events) {
        load += e[1];
        if (load > capacity) return false;       // too heavy on this stretch
    }
    return true;
}   // O(n log n) time · O(n) space""",
            "python": r"""def car_pooling(trips, capacity):
    events = []
    for passengers, start, end in trips:
        events.append((start, passengers))       # passengers board here
        events.append((end, -passengers))        # and leave here
    events.sort()
    load = 0
    for _, delta in events:
        load += delta
        if load > capacity:                      # too heavy on this stretch
            return False
    return True""",
        },
    },
    {
        "slug": "candy",
        "title": "Candy",
        "difficulty": "Hard",
        "pattern": "two passes around a peak constraint",
        "statement": "Children stand in a line with ratings. Every child gets at least one candy, and a child with a higher rating than an immediate "
                     "neighbour must get more candy than that neighbour. Return the fewest candies in total.",
        "examples": [("ratings = [1,0,2]", "5"), ("ratings = [1,2,2]", "4")],
        "constraints": ["1 <= ratings.length <= 2 · 10^4", "0 <= ratings[i] <= 2 · 10^4", "both neighbours' constraints must hold at once"],
        "approach": "A single pass can only see one direction. Sweep left to right enforcing the rising condition, then right to left enforcing the "
                     "falling one, taking the larger of the two values per child. Each pass is locally forced, and the maximum of two forced bounds is "
                     "the smallest total that satisfies both.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// One pass for rising slopes, one for falling slopes, take the larger
int candy(vector<int>& ratings) {
    int n = ratings.size();
    vector<int> count(n, 1);                     // everyone gets at least one
    for (int i = 1; i < n; i++)
        if (ratings[i] > ratings[i-1]) count[i] = count[i-1] + 1;   // rising pass
    for (int i = n - 2; i >= 0; i--)
        if (ratings[i] > ratings[i+1]) count[i] = max(count[i], count[i+1] + 1);
    return accumulate(count.begin(), count.end(), 0);
}   // O(n) time · O(n) space""",
            "java": r"""// One pass for rising slopes, one for falling slopes, take the larger
int candy(int[] ratings) {
    int n = ratings.length;
    int[] count = new int[n];
    Arrays.fill(count, 1);                       // everyone gets at least one
    for (int i = 1; i < n; i++)
        if (ratings[i] > ratings[i-1]) count[i] = count[i-1] + 1;   // rising pass
    for (int i = n - 2; i >= 0; i--)
        if (ratings[i] > ratings[i+1]) count[i] = Math.max(count[i], count[i+1] + 1);
    int total = 0;
    for (int c : count) total += c;
    return total;
}   // O(n) time · O(n) space""",
            "python": r"""def candy(ratings):
    n = len(ratings)
    count = [1] * n                      # everyone starts with one candy
    for i in range(1, n):
        if ratings[i] > ratings[i-1]:
            count[i] = count[i-1] + 1    # rising slope
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i+1]:
            count[i] = max(count[i], count[i+1] + 1)   # falling slope
    return sum(count)""",
        },
    },
    {
        "slug": "course-schedule-iii",
        "title": "Course Schedule III",
        "difficulty": "Hard",
        "pattern": "deadline sweep with a heap that undoes choices",
        "statement": "Each course has a duration and a last day by which it must be finished; courses run one at a time. Return the maximum number "
                     "of courses that can be completed.",
        "examples": [("courses = [[100,200],[200,1300],[1000,1250],[2000,3200]]", "3"),
                     ("courses = [[1,2]]", "1"), ("courses = [[3,2],[4,3]]", "0")],
        "constraints": ["1 <= number of courses <= 10^4", "1 <= duration <= lastDay <= 10^4", "courses cannot overlap"],
        "approach": "Sort by deadline and keep adding courses, tracking total time. Whenever the total overshoots the current deadline, drop the "
                     "*longest* course taken so far: the count stays as high as possible and the freed time is the most you can recover. That "
                     "undo step is what separates this from plain interval scheduling.",
        "complexity": ("O(n log n)", "O(n)"),
        "code": {
            "cpp": r"""// Add courses by deadline; when time overruns, drop the longest course
int scheduleCourse(vector<vector<int>>& courses) {
    sort(courses.begin(), courses.end(),
         [](const vector<int>& a, const vector<int>& b) { return a[1] < b[1]; });
    priority_queue<int> taken;                   // durations so far, longest on top
    int time = 0;
    for (auto& c : courses) {
        time += c[0];
        taken.push(c[0]);
        if (time > c[1]) {                       // this deadline is missed
            time -= taken.top();                 // undo the costliest choice
            taken.pop();
        }
    }
    return taken.size();
}   // O(n log n) time · O(n) space""",
            "java": r"""// Add courses by deadline; when time overruns, drop the longest course
int scheduleCourse(int[][] courses) {
    Arrays.sort(courses, (a, b) -> a[1] - b[1]);     // by last day
    PriorityQueue<Integer> taken = new PriorityQueue<>(Collections.reverseOrder());
    int time = 0;
    for (int[] c : courses) {
        time += c[0];
        taken.add(c[0]);
        if (time > c[1]) {                       // this deadline is missed
            time -= taken.poll();                // undo the costliest choice
        }
    }
    return taken.size();
}   // O(n log n) time · O(n) space""",
            "python": r"""import heapq

def schedule_course(courses):
    courses.sort(key=lambda c: c[1])         # by last day
    taken = []                               # max-heap of durations (negated)
    time = 0
    for duration, last_day in courses:
        time += duration
        heapq.heappush(taken, -duration)
        if time > last_day:                  # this deadline is missed
            time -= -heapq.heappop(taken)    # drop the longest course so far
    return len(taken)""",
        },
    },
    {
        "slug": "minimum-initial-energy-to-finish-tasks",
        "title": "Minimum Initial Energy to Finish Tasks",
        "difficulty": "Hard",
        "pattern": "exchange-argument sort by energy gap",
        "statement": "Task i needs at least minimum[i] energy to start and consumes actual[i] while running. Return the smallest starting energy that "
                     "finishes every task in some order.",
        "examples": [("tasks = [[1,2],[2,4],[4,8]]", "8"), ("tasks = [[1,3],[2,4],[10,11],[10,12],[8,9]]", "32")],
        "constraints": ["1 <= number of tasks <= 10^5", "1 <= actual[i] <= minimum[i] <= 10^4", "energy only ever decreases"],
        "approach": "For two adjacent tasks i then j you need max(min[i], min[j] + actual[i]); swapping gives the mirror image, and comparing them "
                     "shows the larger (minimum - actual) must come first. That single comparison sorts the whole schedule, after which one running "
                     "sum gives the answer.",
        "complexity": ("O(n log n)", "O(1)"),
        "code": {
            "cpp": r"""// Big energy gap first: sort by (minimum - actual) descending
int minimumEffort(vector<vector<int>>& tasks) {
    sort(tasks.begin(), tasks.end(), [](const vector<int>& a, const vector<int>& b) {
        return (a[1] - a[0]) > (b[1] - b[0]);    // largest headroom first
    });
    int spent = 0, need = 0;
    for (auto& t : tasks) {
        spent += t[0];                           // energy used before this task
        need = max(need, spent + t[1] - t[0]);   // enough to start it
    }
    return need;
}   // O(n log n) time · O(1) space""",
            "java": r"""// Big energy gap first: sort by (minimum - actual) descending
int minimumEffort(int[][] tasks) {
    Arrays.sort(tasks, (a, b) -> (b[1] - b[0]) - (a[1] - a[0]));
    int spent = 0, need = 0;
    for (int[] t : tasks) {
        spent += t[0];                           // energy used before this task
        need = Math.max(need, spent + t[1] - t[0]);   // enough to start it
    }
    return need;
}   // O(n log n) time · O(1) space""",
            "python": r"""def minimum_effort(tasks):
    tasks.sort(key=lambda t: t[1] - t[0], reverse=True)   # largest headroom first
    spent = need = 0
    for actual, minimum in tasks:
        spent += actual                     # energy used before this task
        need = max(need, spent + minimum - actual)        # enough to start it
    return need""",
        },
    },
    {
        "slug": "minimum-number-of-refueling-stops",
        "title": "Minimum Number of Refueling Stops",
        "difficulty": "Hard",
        "pattern": "lazy refuelling with a max-heap",
        "statement": "A car starts with startFuel and must reach a target, with fuel stations at given positions and amounts. Return the fewest "
                     "refuelling stops, or -1 if the target is unreachable.",
        "examples": [("target = 1, startFuel = 1, stations = []", "0"),
                     ("target = 100, startFuel = 1, stations = [[10,100]]", "-1"),
                     ("target = 100, startFuel = 10, stations = [[10,60],[20,30],[30,30],[60,40]]", "2")],
        "constraints": ["1 <= target, startFuel <= 10^9", "0 <= stations.length <= 500", "stations are sorted by position"],
        "approach": "Pass every station reachable on the current fuel and remember it in a max-heap without deciding yet. When the fuel runs out, "
                     "refuel from the *largest* remembered station — the decision that maximises range per stop. Deferring the choice is what makes "
                     "the greedy correct rather than merely plausible.",
        "complexity": ("O(n log n)", "O(n)"),
        "code": {
            "cpp": r"""// Remember every reachable station; refuel from the largest when stuck
int minRefuelStops(int target, int startFuel, vector<vector<int>>& stations) {
    priority_queue<int> reachable;               // fuel amounts passed so far
    int stops = 0, i = 0, n = stations.size();
    long long fuel = startFuel;
    while (fuel < target) {
        while (i < n && stations[i][0] <= fuel)  // can reach these without a stop
            reachable.push(stations[i++][1]);
        if (reachable.empty()) return -1;        // nothing left to burn
        fuel += reachable.top();                 // refuel at the best station so far
        reachable.pop();
        stops++;
    }
    return stops;
}   // O(n log n) time · O(n) space""",
            "java": r"""// Remember every reachable station; refuel from the largest when stuck
int minRefuelStops(int target, int startFuel, int[][] stations) {
    PriorityQueue<Integer> reachable = new PriorityQueue<>(Collections.reverseOrder());
    int stops = 0, i = 0, n = stations.length;
    long fuel = startFuel;
    while (fuel < target) {
        while (i < n && stations[i][0] <= fuel)  // reachable without a stop
            reachable.add(stations[i++][1]);
        if (reachable.isEmpty()) return -1;      // nothing left to burn
        fuel += reachable.poll();                // refuel at the best station so far
        stops++;
    }
    return stops;
}   // O(n log n) time · O(n) space""",
            "python": r"""import heapq

def min_refuel_stops(target, start_fuel, stations):
    reachable = []                   # fuel amounts of stations already passed
    stops = 0
    fuel = start_fuel
    i = 0
    while fuel < target:
        while i < len(stations) and stations[i][0] <= fuel:
            heapq.heappush(reachable, -stations[i][1])   # can reach it, decide later
            i += 1
        if not reachable:
            return -1                # nothing left to burn
        fuel += -heapq.heappop(reachable)   # refuel at the best station so far
        stops += 1
    return stops""",
        },
    },
    {
        "slug": "maximum-performance-of-a-team",
        "title": "Maximum Performance of a Team",
        "difficulty": "Hard",
        "pattern": "sort by one factor, heap over the other",
        "statement": "Choose at most k engineers. The team's performance is the sum of their speeds multiplied by the smallest efficiency in the "
                     "team. Return the maximum performance modulo 10^9 + 7.",
        "examples": [("n = 6, speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 2", "60"),
                     ("n = 6, speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 3", "68"),
                     ("n = 6, speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 4", "72")],
        "constraints": ["1 <= n <= 10^5", "1 <= speed[i], efficiency[i] <= 10^8", "at most k engineers may be chosen"],
        "approach": "Sort by efficiency descending so that, as you sweep, the current engineer is always the least efficient one in any team that "
                     "includes them — which fixes the multiplier. The question becomes the best speed sum for at most k engineers, kept by a "
                     "min-heap that discards the slowest whenever it overflows.",
        "complexity": ("O(n log n)", "O(k)"),
        "code": {
            "cpp": r"""// Efficiency descending fixes the multiplier; the heap maximises the speed sum
int maxPerformance(int n, vector<int>& speed, vector<int>& efficiency, int k) {
    vector<pair<int,int>> eng(n);                // (efficiency, speed)
    for (int i = 0; i < n; i++) eng[i] = {efficiency[i], speed[i]};
    sort(eng.rbegin(), eng.rend());
    priority_queue<int, vector<int>, greater<int>> chosen;   // slowest on top
    long long sum = 0, best = 0;
    for (auto& [eff, sp] : eng) {
        sum += sp;
        chosen.push(sp);
        if ((int)chosen.size() > k) { sum -= chosen.top(); chosen.pop(); }
        best = max(best, sum * eff);             // eff is the team minimum here
    }
    return (int)(best % 1000000007LL);
}   // O(n log n) time · O(k) space""",
            "java": r"""// Efficiency descending fixes the multiplier; the heap maximises the speed sum
int maxPerformance(int n, int[] speed, int[] efficiency, int k) {
    int[][] eng = new int[n][2];
    for (int i = 0; i < n; i++) eng[i] = new int[]{efficiency[i], speed[i]};
    Arrays.sort(eng, (a, b) -> b[0] - a[0]);     // efficiency descending
    PriorityQueue<Integer> chosen = new PriorityQueue<>();   // slowest on top
    long sum = 0, best = 0;
    for (int[] e : eng) {
        sum += e[1];
        chosen.add(e[1]);
        if (chosen.size() > k) sum -= chosen.poll();
        best = Math.max(best, sum * e[0]);       // e[0] is the team minimum here
    }
    return (int) (best % 1_000_000_007L);
}   // O(n log n) time · O(k) space""",
            "python": r"""import heapq

def max_performance(n, speed, efficiency, k):
    engineers = sorted(zip(efficiency, speed), reverse=True)   # efficiency desc
    chosen = []                       # min-heap of speeds
    total = best = 0
    for eff, sp in engineers:
        total += sp
        heapq.heappush(chosen, sp)
        if len(chosen) > k:           # keep only the k fastest so far
            total -= heapq.heappop(chosen)
        best = max(best, total * eff)  # eff is the team minimum at this point
    return best % (10 ** 9 + 7)""",
        },
    },
    {
        "slug": "minimum-cost-to-hire-k-workers",
        "title": "Minimum Cost to Hire K Workers",
        "difficulty": "Hard",
        "pattern": "pay ratio sweep with a quality heap",
        "statement": "Each worker has a quality and a minimum expected wage. Hired workers must be paid in proportion to their quality, at least their "
                     "minimum. Return the cheapest total cost of hiring exactly k workers.",
        "examples": [("quality = [10,20,5], wage = [70,50,30], k = 2", "105.00000"),
                     ("quality = [3,1,10,10,1], wage = [4,8,2,2,7], k = 3", "30.66667")],
        "constraints": ["1 <= k <= n <= 10^4", "1 <= quality[i] <= 10^4", "1 <= wage[i] <= 10^4"],
        "approach": "The pay rate is set by the strictest worker in the group, so sort by the required rate wage/quality. Sweeping in that order "
                     "fixes the rate; the cheapest group at that rate uses the k smallest qualities, which a max-heap maintains as the sweep advances.",
        "complexity": ("O(n log n)", "O(k)"),
        "code": {
            "cpp": r"""// Sweep the required rate; keep the k smallest qualities in a max-heap
double mincostToHireWorkers(vector<int>& quality, vector<int>& wage, int k) {
    int n = quality.size();
    vector<int> idx(n);
    iota(idx.begin(), idx.end(), 0);
    sort(idx.begin(), idx.end(), [&](int a, int b) {          // by wage/quality
        return (long long)wage[a] * quality[b] < (long long)wage[b] * quality[a];
    });
    priority_queue<int> biggest;                 // largest quality on top
    long long sum = 0;
    double best = 1e18;
    for (int i : idx) {
        biggest.push(quality[i]);
        sum += quality[i];
        if ((int)biggest.size() > k) { sum -= biggest.top(); biggest.pop(); }
        if ((int)biggest.size() == k)
            best = min(best, (double)wage[i] / quality[i] * sum);   // this rate
    }
    return best;
}   // O(n log n) time · O(k) space""",
            "java": r"""// Sweep the required rate; keep the k smallest qualities in a max-heap
double mincostToHireWorkers(int[] quality, int[] wage, int k) {
    int n = quality.length;
    Integer[] idx = new Integer[n];
    for (int i = 0; i < n; i++) idx[i] = i;
    Arrays.sort(idx, (a, b) ->                       // by wage/quality
        Long.compare((long) wage[a] * quality[b], (long) wage[b] * quality[a]));
    PriorityQueue<Integer> biggest = new PriorityQueue<>(Collections.reverseOrder());
    long sum = 0;
    double best = Double.MAX_VALUE;
    for (int i : idx) {
        biggest.add(quality[i]);
        sum += quality[i];
        if (biggest.size() > k) sum -= biggest.poll();
        if (biggest.size() == k)
            best = Math.min(best, (double) wage[i] / quality[i] * sum);   // this rate
    }
    return best;
}   // O(n log n) time · O(k) space""",
            "python": r"""import heapq

def mincost_to_hire_workers(quality, wage, k):
    workers = sorted(zip(quality, wage), key=lambda qw: qw[1] / qw[0])   # by rate
    biggest = []                      # max-heap of qualities (negated)
    total = 0
    best = float('inf')
    for q, w in workers:
        heapq.heappush(biggest, -q)
        total += q
        if len(biggest) > k:          # keep the k smallest qualities
            total -= -heapq.heappop(biggest)
        if len(biggest) == k:
            best = min(best, w / q * total)   # pay everyone at this worker's rate
    return best""",
        },
    },
    {
        "slug": "ipo",
        "title": "IPO",
        "difficulty": "Hard",
        "pattern": "two heaps on capital and profit",
        "statement": "With start capital w you may take up to k projects; project i needs capital[i] to start and gives profit[i]. Return the final "
                     "capital when you always pick optimally.",
        "examples": [("k = 2, w = 0, profits = [1,2,3], capital = [0,1,1]", "4"),
                     ("k = 3, w = 0, profits = [1,2,3], capital = [0,1,2]", "6")],
        "constraints": ["1 <= k <= 10^5", "0 <= w, capital[i] <= 10^9", "1 <= profits[i] <= 10^4"],
        "approach": "Capital only grows, so a project that is affordable stays affordable. That means the affordable set can be maintained "
                     "incrementally: a min-heap over capital releases projects as the bankroll rises, and a max-heap over profit picks the best of "
                     "them each round.",
        "complexity": ("O(n log n)", "O(n)"),
        "code": {
            "cpp": r"""// Unlock projects by capital, then take the most profitable of those
int findMaximizedCapital(int k, int w, vector<int>& profits, vector<int>& capital) {
    int n = profits.size();
    vector<int> idx(n);
    iota(idx.begin(), idx.end(), 0);
    sort(idx.begin(), idx.end(), [&](int a, int b) { return capital[a] < capital[b]; });
    priority_queue<int> affordable;              // profits of projects we can start
    int i = 0;
    for (int step = 0; step < k; step++) {
        while (i < n && capital[idx[i]] <= w)    // newly affordable projects
            affordable.push(profits[idx[i++]]);
        if (affordable.empty()) break;           // nothing left to invest in
        w += affordable.top();                   // take the most profitable one
        affordable.pop();
    }
    return w;
}   // O(n log n) time · O(n) space""",
            "java": r"""// Unlock projects by capital, then take the most profitable of those
int findMaximizedCapital(int k, int w, int[] profits, int[] capital) {
    int n = profits.length;
    Integer[] idx = new Integer[n];
    for (int i = 0; i < n; i++) idx[i] = i;
    Arrays.sort(idx, (a, b) -> capital[a] - capital[b]);      // cheapest capital first
    PriorityQueue<Integer> affordable = new PriorityQueue<>(Collections.reverseOrder());
    int i = 0;
    for (int step = 0; step < k; step++) {
        while (i < n && capital[idx[i]] <= w)    // newly affordable projects
            affordable.add(profits[idx[i++]]);
        if (affordable.isEmpty()) break;         // nothing left to invest in
        w += affordable.poll();                  // take the most profitable one
    }
    return w;
}   // O(n log n) time · O(n) space""",
            "python": r"""import heapq

def find_maximized_capital(k, w, profits, capital):
    projects = sorted(zip(capital, profits))     # cheapest capital first
    affordable = []                              # max-heap of profits (negated)
    i = 0
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(affordable, -projects[i][1])   # now within reach
            i += 1
        if not affordable:
            break                                # nothing left to invest in
        w += -heapq.heappop(affordable)          # do the most profitable project
    return w""",
        },
    },
    {
        "slug": "earliest-possible-day-of-full-bloom",
        "title": "Earliest Possible Day of Full Bloom",
        "difficulty": "Hard",
        "pattern": "sort by grow time, plant back to back",
        "statement": "Flower i needs plantTime[i] consecutive days of planting and then growTime[i] days to bloom. Only one flower can be planted per "
                     "day. Return the earliest day all flowers are blooming.",
        "examples": [("plantTime = [1,4,3], growTime = [2,3,1]", "9"),
                     ("plantTime = [1,2,3,2], growTime = [2,1,2,1]", "9")],
        "constraints": ["1 <= number of flowers <= 10^5", "1 <= plantTime[i], growTime[i] <= 10^4", "planting is sequential, growing is parallel"],
        "approach": "Planting is the only serial resource, so the schedule should never idle: keep planting in some order. The exchange argument "
                     "says the flower with the longest growth must be planted first, because a long growth period can overlap with later planting "
                     "only if it starts early.",
        "complexity": ("O(n log n)", "O(1)"),
        "code": {
            "cpp": r"""// Longest growing flower first: growth overlaps the planting that follows
int earliestFullBloom(vector<int>& plantTime, vector<int>& growTime) {
    int n = plantTime.size();
    vector<int> idx(n);
    iota(idx.begin(), idx.end(), 0);
    sort(idx.begin(), idx.end(), [&](int a, int b) { return growTime[a] > growTime[b]; });
    int day = 0, answer = 0;
    for (int i : idx) {
        day += plantTime[i];                     // planted immediately after the last
        answer = max(answer, day + growTime[i]);
    }
    return answer;
}   // O(n log n) time · O(1) space""",
            "java": r"""// Longest growing flower first: growth overlaps the planting that follows
int earliestFullBloom(int[] plantTime, int[] growTime) {
    int n = plantTime.length;
    Integer[] idx = new Integer[n];
    for (int i = 0; i < n; i++) idx[i] = i;
    Arrays.sort(idx, (a, b) -> growTime[b] - growTime[a]);    // longest growth first
    int day = 0, answer = 0;
    for (int i : idx) {
        day += plantTime[i];                     // planted right after the last one
        answer = Math.max(answer, day + growTime[i]);
    }
    return answer;
}   // O(n log n) time · O(1) space""",
            "python": r"""def earliest_full_bloom(plant_time, grow_time):
    order = sorted(range(len(plant_time)), key=lambda i: -grow_time[i])
    day = answer = 0
    for i in order:
        day += plant_time[i]            # planted right after the previous flower
        answer = max(answer, day + grow_time[i])
    return answer""",
        },
    },
    {
        "slug": "minimum-number-of-taps-to-open-to-water-a-garden",
        "title": "Minimum Number of Taps to Open to Water a Garden",
        "difficulty": "Hard",
        "pattern": "taps become intervals, then greedy coverage",
        "statement": "A garden spans [0, n], and the tap at position i waters [i - taps[i], i + taps[i]]. Return the fewest taps that water the whole "
                     "garden, or -1.",
        "examples": [("n = 5, ranges = [3,4,1,1,0,0]", "1"), ("n = 3, ranges = [0,0,0,0]", "-1")],
        "constraints": ["1 <= n <= 10^4", "0 <= taps[i] <= 100", "coverage outside [0, n] is clipped"],
        "approach": "Each tap is an interval, so the question becomes covering [0, n] with the fewest intervals — the jump-game greedy. Sweep the "
                     "intervals in order of left end, always extending the covered frontier as far right as possible with intervals that start inside "
                     "it; if nothing extends it, coverage is impossible.",
        "complexity": ("O(n log n)", "O(n)"),
        "code": {
            "cpp": r"""// Taps are intervals; cover [0, n] with the fewest of them
int minTaps(int n, vector<int>& taps) {
    vector<pair<int,int>> iv;                    // (left, right) coverage
    for (int i = 0; i <= n; i++) {
        if (taps[i] == 0) continue;
        iv.push_back({max(0, i - taps[i]), min(n, i + taps[i])});
    }
    sort(iv.begin(), iv.end());
    int count = 0, covered = 0, i = 0, m = iv.size();
    while (covered < n) {
        int farthest = covered;
        while (i < m && iv[i].first <= covered)  // any interval starting inside
            farthest = max(farthest, iv[i++].second);
        if (farthest == covered) return -1;      // nothing extends the frontier
        count++;
        covered = farthest;
    }
    return count;
}   // O(n log n) time · O(n) space""",
            "java": r"""// Taps are intervals; cover [0, n] with the fewest of them
int minTaps(int n, int[] taps) {
    List<int[]> iv = new ArrayList<>();          // (left, right) coverage
    for (int i = 0; i <= n; i++) {
        if (taps[i] == 0) continue;
        iv.add(new int[]{Math.max(0, i - taps[i]), Math.min(n, i + taps[i])});
    }
    iv.sort((a, b) -> a[0] - b[0]);
    int count = 0, covered = 0, i = 0, m = iv.size();
    while (covered < n) {
        int farthest = covered;
        while (i < m && iv.get(i)[0] <= covered)  // any interval starting inside
            farthest = Math.max(farthest, iv.get(i++)[1]);
        if (farthest == covered) return -1;      // nothing extends the frontier
        count++;
        covered = farthest;
    }
    return count;
}   // O(n log n) time · O(n) space""",
            "python": r"""def min_taps(n, taps):
    intervals = []
    for i, t in enumerate(taps):
        if t:
            intervals.append((max(0, i - t), min(n, i + t)))   # clipped coverage
    intervals.sort()
    count = covered = i = 0
    while covered < n:
        farthest = covered
        while i < len(intervals) and intervals[i][0] <= covered:
            farthest = max(farthest, intervals[i][1])   # any interval inside
            i += 1
        if farthest == covered:
            return -1                     # the frontier cannot advance
        count += 1
        covered = farthest
    return count""",
        },
    },
    {
        "slug": "maximum-number-of-tasks-you-can-assign",
        "title": "Maximum Number of Tasks You Can Assign",
        "difficulty": "Hard",
        "pattern": "binary search the count, then match k easiest tasks to k strongest workers",
        "statement": "Task i needs tasks[i] strength. Each worker has a strength and does at most one task, and at most 'pills' workers may be given a "
                     "boost of 'strength' before starting. Return the maximum number of tasks that can be completed.",
        "examples": [("tasks = [3,2,1], workers = [0,3,3], pills = 1, strength = 1", "3"),
                     ("tasks = [5,4], workers = [0,0,0], pills = 1, strength = 5", "1"),
                     ("tasks = [10,15,30], workers = [0,10,10,10,10], pills = 3, strength = 10", "2")],
        "constraints": ["1 <= tasks.length, workers.length <= 5 · 10^4", "1 <= pills <= tasks.length", "1 <= strength <= 10^9"],
        "approach": "If k tasks can be done at all, then the k *easiest* tasks can be done by the k *strongest* workers, so binary search k. The check "
                     "walks the k chosen tasks from hardest to easiest and hands each one the *weakest* worker still able to do it: that keeps the "
                     "strong workers free for the tasks below. A pill is spent only when no worker can manage the task unaided, and only on the "
                     "weakest worker it can lift.",
        "complexity": ("O((t + w) log w + log(min(t, w)) · k log k)", "O(k)"),
        "code": {
            "cpp": r"""// Binary search k; the check matches k easiest tasks to k strongest workers
int maxTaskAssign(vector<int>& tasks, vector<int>& workers, int pills, int strength) {
    sort(tasks.begin(), tasks.end());
    sort(workers.begin(), workers.end());
    int n = tasks.size(), m = workers.size();
    auto feasible = [&](int k) {
        multiset<int> pool(workers.end() - k, workers.end());   // k strongest workers
        int pillsLeft = pills;
        for (int i = k - 1; i >= 0; i--) {                      // hardest task first
            auto fit = pool.lower_bound(tasks[i]);              // weakest that fits
            if (fit != pool.end()) { pool.erase(fit); continue; }
            if (pillsLeft) {
                auto boosted = pool.lower_bound(tasks[i] - strength);
                if (boosted != pool.end()) {                    // a pill lifts this one
                    pool.erase(boosted);
                    pillsLeft--;
                    continue;
                }
            }
            return false;                                       // nobody could manage it
        }
        return true;
    };
    int lo = 0, hi = min(n, m);
    while (lo < hi) {                                           // feasible(k) is monotone
        int mid = (lo + hi + 1) / 2;
        if (feasible(mid)) lo = mid; else hi = mid - 1;
    }
    return lo;
}   // O((t + w) log w + log(min) · k log k) time · O(k) space""",
            "java": r"""// Binary search k; the check matches k easiest tasks to k strongest workers
int maxTaskAssign(int[] tasks, int[] workers, int pills, int strength) {
    Arrays.sort(tasks);
    Arrays.sort(workers);
    int n = tasks.length, m = workers.length;
    int lo = 0, hi = Math.min(n, m);
    while (lo < hi) {                                // feasible(k) is monotone in k
        int mid = (lo + hi + 1) / 2;
        if (feasible(tasks, workers, pills, strength, mid)) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}
boolean feasible(int[] tasks, int[] workers, int pills, int strength, int k) {
    TreeMap<Integer, Integer> pool = new TreeMap<>();
    for (int i = workers.length - k; i < workers.length; i++)   // k strongest workers
        pool.merge(workers[i], 1, Integer::sum);
    int pillsLeft = pills;
    for (int i = k - 1; i >= 0; i--) {               // hardest task first
        Integer fit = pool.ceilingKey(tasks[i]);     // weakest worker that fits
        if (fit != null) { take(pool, fit); continue; }
        if (pillsLeft > 0) {
            Integer boosted = pool.ceilingKey(tasks[i] - strength);
            if (boosted != null) {                   // a pill lifts this worker
                take(pool, boosted);
                pillsLeft--;
                continue;
            }
        }
        return false;                                // nobody could manage it
    }
    return true;
}
void take(TreeMap<Integer, Integer> pool, int w) {
    int left = pool.get(w);
    if (left == 1) pool.remove(w); else pool.put(w, left - 1);
}   // O((t + w) log w + log(min) · k log k) time · O(k) space""",
            "python": r"""from bisect import bisect_left

def max_task_assign(tasks, workers, pills, strength):
    tasks.sort()
    workers.sort()
    n, m = len(tasks), len(workers)

    def feasible(k):
        pool = workers[m - k:]           # the k strongest workers, ascending
        # next_free[i] = smallest unused index >= i (a successor structure, so
        # removing a worker is O(alpha) instead of shifting the list)
        next_free = list(range(k + 1))

        def find(i):
            while next_free[i] != i:
                next_free[i] = next_free[next_free[i]]
                i = next_free[i]
            return i

        pills_left = pills
        for i in range(k - 1, -1, -1):   # hardest chosen task first
            t = tasks[i]
            j = find(bisect_left(pool, t))          # weakest unused worker that fits
            if j < k:
                next_free[j] = j + 1                # mark the worker as used
                continue
            if pills_left:
                j = find(bisect_left(pool, t - strength))
                if j < k:                           # a pill lifts this worker
                    next_free[j] = j + 1
                    pills_left -= 1
                    continue
            return False                            # nobody could manage it
        return True

    lo, hi = 0, min(n, m)
    while lo < hi:                       # feasible(k) is monotone in k
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo""",
        },
    },
    {
        "slug": "rearrange-string-k-distance-apart",
        "title": "Rearrange String k Distance Apart",
        "difficulty": "Hard",
        "pattern": "most frequent first with a cooldown queue",
        "statement": "Rearrange the string so that equal characters are at least k positions apart. Return any valid arrangement, or the empty string "
                     "if none exists.",
        "examples": [("s = \"aabbcc\", k = 3", "abcabc"), ("s = \"aaabc\", k = 3", ""), ("s = \"aaadbbcc\", k = 2", "abacbdca")],
        "constraints": ["1 <= s.length <= 3 · 10^4", "1 <= k <= s.length", "s contains lowercase English letters"],
        "approach": "Place the most frequent remaining character at each position — it is the one that runs out of room first. A character just used "
                     "must sit out the next k-1 positions, which a small queue models exactly: hold the last k placed characters and release the "
                     "oldest one back into the heap before choosing again.",
        "complexity": ("O(n log 26)", "O(k + 26)"),
        "code": {
            "cpp": r"""// Most frequent first, with the last k characters held in a queue
string rearrangeString(string s, int k) {
    if (k <= 1) return s;
    int counts[26] = {0};
    for (char c : s) counts[c - 'a']++;
    priority_queue<pair<int,char>> pq;            // (remaining count, character)
    for (int c = 0; c < 26; c++) if (counts[c]) pq.push({counts[c], (char)('a' + c)});
    queue<pair<int,char>> cooldown;               // placed within the last k steps
    string out;
    for (int step = 0; step < (int)s.size(); step++) {
        if ((int)cooldown.size() == k) {          // the character k steps back returns
            auto back = cooldown.front(); cooldown.pop();
            if (back.first > 0) pq.push(back);
        }
        if (pq.empty()) return "";                // no character is far enough away
        auto [cnt, ch] = pq.top(); pq.pop();
        out += ch;
        cooldown.push({cnt - 1, ch});             // sits out the next k-1 positions
    }
    return out;
}   // O(n log 26) time · O(k + 26) space""",
            "java": r"""// Most frequent first, with the last k characters held in a queue
String rearrangeString(String s, int k) {
    if (k <= 1) return s;
    int[] counts = new int[26];
    for (int i = 0; i < s.length(); i++) counts[s.charAt(i) - 'a']++;
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> b[0] - a[0]);
    for (int c = 0; c < 26; c++) if (counts[c] > 0) pq.add(new int[]{counts[c], c});
    Deque<int[]> cooldown = new ArrayDeque<>();   // placed within the last k steps
    StringBuilder out = new StringBuilder();
    for (int step = 0; step < s.length(); step++) {
        if (cooldown.size() == k) {               // the character k steps back returns
            int[] back = cooldown.poll();
            if (back[0] > 0) pq.add(back);
        }
        if (pq.isEmpty()) return "";              // no character is far enough away
        int[] cur = pq.poll();
        out.append((char) ('a' + cur[1]));
        cooldown.add(new int[]{cur[0] - 1, cur[1]});   // sits out k-1 positions
    }
    return out.toString();
}   // O(n log 26) time · O(k + 26) space""",
            "python": r"""import heapq
from collections import Counter, deque

def rearrange_string(s, k):
    if k <= 1:
        return s
    heap = [(-c, ch) for ch, c in Counter(s).items()]
    heapq.heapify(heap)
    cooldown = deque()                 # characters placed in the last k steps
    out = []
    for _ in range(len(s)):
        if len(cooldown) == k:         # the character k steps back returns
            rem, ch = cooldown.popleft()
            if rem < 0:
                heapq.heappush(heap, (rem, ch))
        if not heap:
            return ''                  # no character is far enough away
        cnt, ch = heapq.heappop(heap)
        out.append(ch)
        cooldown.append((cnt + 1, ch))   # one fewer copy, then cooldown
    return ''.join(out)""",
        },
    },
    {
        "slug": "smallest-range-covering-elements-from-k-lists",
        "title": "Smallest Range Covering Elements from K Lists",
        "difficulty": "Hard",
        "pattern": "merge the lists, then slide a window",
        "statement": "Each of the k sorted lists must contribute at least one element to the chosen range [a, b]. Return the smallest such range, "
                     "breaking ties by the smallest a.",
        "examples": [("nums = [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]", "[20,24]"),
                     ("nums = [[1,2,3],[1,2,3],[1,2,3]]", "[1,1]")],
        "constraints": ["1 <= k <= 3500", "1 <= total elements <= 5 · 10^4", "each list is sorted ascending"],
        "approach": "Merge everything into one sorted list while remembering which list each value came from. A window covering all k lists has its "
                     "range fixed by its two ends, so a sliding window that shrinks from the left whenever all lists are covered finds the minimum — "
                     "the same pattern as the smallest substring problems.",
        "complexity": ("O(N log N)", "O(N + k)"),
        "code": {
            "cpp": r"""// Merge with list tags, then shrink a window until some list is uncovered
vector<int> smallestRange(vector<vector<int>>& nums) {
    vector<pair<int,int>> all;                   // (value, list index)
    for (int i = 0; i < (int)nums.size(); i++)
        for (int v : nums[i]) all.push_back({v, i});
    sort(all.begin(), all.end());
    int k = nums.size();
    vector<int> cnt(k, 0);
    int covered = 0, left = 0;
    int bestL = all.front().first, bestR = all.back().first;
    for (int right = 0; right < (int)all.size(); right++) {
        if (cnt[all[right].second]++ == 0) covered++;       // new list represented
        while (covered == k) {                   // every list is inside: try shrinking
            if (all[right].first - all[left].first < bestR - bestL) {
                bestL = all[left].first;
                bestR = all[right].first;
            }
            if (--cnt[all[left].second] == 0) covered--;
            left++;
        }
    }
    return {bestL, bestR};
}   // O(N log N) time · O(N + k) space""",
            "java": r"""// Merge with list tags, then shrink a window until some list is uncovered
int[] smallestRange(List<List<Integer>> nums) {
    int k = nums.size(), n = 0;
    for (List<Integer> l : nums) n += l.size();
    int[][] all = new int[n][2];                 // {value, list index}
    int p = 0;
    for (int i = 0; i < k; i++)
        for (int v : nums.get(i)) all[p++] = new int[]{v, i};
    Arrays.sort(all, (a, b) -> a[0] - b[0]);
    int[] cnt = new int[k];
    int covered = 0, left = 0, bestL = all[0][0], bestR = all[n-1][0];
    for (int right = 0; right < n; right++) {
        if (cnt[all[right][1]]++ == 0) covered++;   // new list represented
        while (covered == k) {                   // try shrinking from the left
            if (all[right][0] - all[left][0] < bestR - bestL) {
                bestL = all[left][0];
                bestR = all[right][0];
            }
            if (--cnt[all[left][1]] == 0) covered--;
            left++;
        }
    }
    return new int[]{bestL, bestR};
}   // O(N log N) time · O(N + k) space""",
            "python": r"""def smallest_range(nums):
    tagged = sorted((v, i) for i, lst in enumerate(nums) for v in lst)
    k = len(nums)
    counts = [0] * k
    covered = 0
    left = 0
    best = [tagged[0][0], tagged[-1][0]]        # widest possible start
    for right, (value, idx) in enumerate(tagged):
        if counts[idx] == 0:
            covered += 1                        # this list is now represented
        counts[idx] += 1
        while covered == k:                     # window spans every list
            if value - tagged[left][0] < best[1] - best[0]:
                best = [tagged[left][0], value]  # a tighter range
            j = tagged[left][1]
            counts[j] -= 1
            if counts[j] == 0:
                covered -= 1
            left += 1
    return best""",
        },
    },
]
