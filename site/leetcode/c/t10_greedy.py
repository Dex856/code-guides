# Topic 10 · Greedy & Intervals — C17 solutions
#
# Greedy means one local decision that provably never needs undoing: sort first, then
# take the cheapest, the earliest, or the largest. Interval work is almost always sort.

CODE = {
    "assign-cookies": r"""
// Sort both, then feed each child with the smallest cookie that fits.
static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}

int findContentChildren(int *g, int gn, int *s, int sn) {
    qsort(g, (size_t) gn, sizeof(int), cmpInt);
    qsort(s, (size_t) sn, sizeof(int), cmpInt);
    int child = 0, cookie = 0;
    while (child < gn && cookie < sn) {
        if (s[cookie] >= g[child]) child++;                // this cookie satisfies this child
        cookie++;
    }
    return child;
}   // O(n log n) time · O(1) space
""",
    "lemonade-change": r"""
// Change is paid in 5s and 10s, and big bills are only ever given 10s first.
int lemonadeChange(const int *bills, int n) {
    int fives = 0, tens = 0;
    for (int i = 0; i < n; i++) {
        if (bills[i] == 5) fives++;
        else if (bills[i] == 10) {
            if (!fives) return 0;
            fives--; tens++;
        } else {
            if (tens && fives) { tens--; fives--; }        // prefer giving back a 10
            else if (fives >= 3) fives -= 3;
            else return 0;
        }
    }
    return 1;
}   // O(n) time · O(1) space
""",
    "largest-perimeter-triangle": r"""
// After sorting, the largest side only has to beat the sum of the other two.
static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}

int largestPerimeter(int *nums, int n) {
    qsort(nums, (size_t) n, sizeof(int), cmpInt);
    for (int i = n - 1; i >= 2; i--)
        if (nums[i - 2] + nums[i - 1] > nums[i]) return nums[i - 2] + nums[i - 1] + nums[i];
    return 0;
}   // O(n log n) time · O(1) space
""",
    "can-place-flowers": r"""
// Plant whenever the neighbours are free; planting never hurts later flowers.
int canPlaceFlowers(int *flowerbed, int n, int k) {
    for (int i = 0; i < n && k > 0; i++) {
        if (flowerbed[i]) continue;
        int leftFree = i == 0 || !flowerbed[i - 1];
        int rightFree = i == n - 1 || !flowerbed[i + 1];
        if (leftFree && rightFree) { flowerbed[i] = 1; k--; }
    }
    return k == 0;
}   // O(n) time · O(1) space
""",
    "maximum-units-on-a-truck": r"""
// The most valuable boxes first until the truck is full.
static int cmpBox(const void *a, const void *b) {
    const int *x = *(const int *const *) a, *y = *(const int *const *) b;
    return y[1] - x[1];                                    // descending by units per box
}

int maximumUnits(int **boxTypes, int n, int truckSize) {
    int **boxes = malloc(sizeof(int *) * (size_t) n);
    for (int i = 0; i < n; i++) boxes[i] = boxTypes[i];
    qsort(boxes, (size_t) n, sizeof(int *), cmpBox);
    int units = 0;
    for (int i = 0; i < n && truckSize > 0; i++) {
        int take = boxes[i][0] < truckSize ? boxes[i][0] : truckSize;
        units += take * boxes[i][1];
        truckSize -= take;
    }
    free(boxes);
    return units;
}   // O(n log n) time · O(n) space
""",
    "minimum-number-of-moves-to-seat-everyone": r"""
// Sort both sides and pair them up — the crossing pairs cancel out.
static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}

int minMovesToSeat(int *seats, int n, int *students, int m) {
    (void) m;
    qsort(seats, (size_t) n, sizeof(int), cmpInt);
    qsort(students, (size_t) n, sizeof(int), cmpInt);
    int moves = 0;
    for (int i = 0; i < n; i++) moves += abs(seats[i] - students[i]);
    return moves;
}   // O(n log n) time · O(1) space
""",
    "jump-game": r"""
// Track the farthest index reachable so far; if it falls behind you, you are stuck.
int canJump(const int *nums, int n) {
    int farthest = 0;
    for (int i = 0; i < n; i++) {
        if (i > farthest) return 0;
        if (i + nums[i] > farthest) farthest = i + nums[i];
        if (farthest >= n - 1) return 1;
    }
    return 1;
}   // O(n) time · O(1) space
""",
    "jump-game-ii": r"""
// BFS on ranges: each jump extends the current reach; count the layers.
int jump(const int *nums, int n) {
    int jumps = 0, currentEnd = 0, farthest = 0;
    for (int i = 0; i < n - 1; i++) {
        if (i + nums[i] > farthest) farthest = i + nums[i];
        if (i == currentEnd) {                             // the layer is exhausted: jump
            jumps++;
            currentEnd = farthest;
        }
    }
    return jumps;
}   // O(n) time · O(1) space
""",
    "merge-intervals": r"""
// Sort by start; merge while the next interval starts before the current one ends.
static int cmpInterval(const void *a, const void *b) {
    const int *x = *(const int *const *) a, *y = *(const int *const *) b;
    return x[0] - y[0];
}

int **merge(int **intervals, int n, int *returnSize, int **returnColumnSizes) {
    int **out = malloc(sizeof(int *) * (size_t) n);
    *returnColumnSizes = malloc(sizeof(int) * (size_t) n);
    qsort(intervals, (size_t) n, sizeof(int *), cmpInterval);
    int count = 0;
    for (int i = 0; i < n; i++) {
        if (count && intervals[i][0] <= out[count - 1][1]) {
            if (intervals[i][1] > out[count - 1][1]) out[count - 1][1] = intervals[i][1];
        } else {
            out[count] = malloc(sizeof(int) * 2);
            out[count][0] = intervals[i][0];
            out[count][1] = intervals[i][1];
            (*returnColumnSizes)[count] = 2;
            count++;
        }
    }
    *returnSize = count;
    return out;
}   // O(n log n) time · O(n) space
""",
    "non-overlapping-intervals": r"""
// Keep the interval that ends first; every overlap costs one removal.
static int cmpEnd(const void *a, const void *b) {
    const int *x = *(const int *const *) a, *y = *(const int *const *) b;
    return x[1] - y[1];
}

int eraseOverlapIntervals(int **intervals, int n) {
    if (!n) return 0;
    qsort(intervals, (size_t) n, sizeof(int *), cmpEnd);
    int removed = 0, lastEnd = intervals[0][1];
    for (int i = 1; i < n; i++) {
        if (intervals[i][0] < lastEnd) removed++;          // overlaps: drop it
        else lastEnd = intervals[i][1];
    }
    return removed;
}   // O(n log n) time · O(1) space
""",
    "insert-interval": r"""
// Three phases: intervals entirely before, the merged one, then those after.
int **insert(int **intervals, int n, int *newInterval, int *returnSize, int **returnColumnSizes) {
    int **out = malloc(sizeof(int *) * (size_t) (n + 1));
    *returnColumnSizes = malloc(sizeof(int) * (size_t) (n + 1));
    int count = 0, i = 0;
    while (i < n && intervals[i][1] < newInterval[0]) {    // strictly before
        out[count++] = intervals[i++];
    }
    int start = newInterval[0], end = newInterval[1];
    while (i < n && intervals[i][0] <= end) {              // touching or overlapping: absorb
        if (intervals[i][0] < start) start = intervals[i][0];
        if (intervals[i][1] > end) end = intervals[i][1];
        i++;
    }
    out[count] = malloc(sizeof(int) * 2);
    out[count][0] = start;
    out[count][1] = end;
    count++;
    while (i < n) out[count++] = intervals[i++];
    for (int k = 0; k < count; k++) (*returnColumnSizes)[k] = 2;
    *returnSize = count;
    return out;
}   // O(n) time · O(n) space
""",
    "gas-station": r"""
// If the total cost exceeds the total gas there is no answer; otherwise start right
// after the point where the running shortage went below zero.
int canCompleteCircuit(const int *gas, int n, const int *cost) {
    long long total = 0, tank = 0;
    int start = 0;
    for (int i = 0; i < n; i++) {
        total += gas[i] - cost[i];
        tank += gas[i] - cost[i];
        if (tank < 0) { start = i + 1; tank = 0; }         // this start cannot reach here
    }
    return total >= 0 ? start : -1;
}   // O(n) time · O(1) space
""",
    "partition-labels": r"""
// Record each letter's last position; cut whenever the current part reaches its own end.
int *partitionLabels(char *s, int *returnSize) {
    int last[26] = {0}, n = (int) strlen(s);
    for (int i = 0; i < n; i++) last[s[i] - 'a'] = i;
    int *out = malloc(sizeof(int) * (size_t) n);
    int count = 0, start = 0, end = 0;
    for (int i = 0; i < n; i++) {
        if (last[s[i] - 'a'] > end) end = last[s[i] - 'a'];
        if (i == end) { out[count++] = end - start + 1; start = i + 1; }
    }
    *returnSize = count;
    return out;
}   // O(n) time · O(1) space
""",
    "task-scheduler": r"""
// The hottest task defines the frame: (maxCount - 1) * (n + 1) plus the tasks at that level.
int leastInterval(const char *tasks, int n, int cooldown) {
    int count[26] = {0}, maxCount = 0;
    for (int i = 0; i < n; i++) {
        int c = ++count[tasks[i] - 'A'];
        if (c > maxCount) maxCount = c;
    }
    int hottest = 0;
    for (int c = 0; c < 26; c++) if (count[c] == maxCount) hottest++;
    int slots = (maxCount - 1) * (cooldown + 1) + hottest;
    return slots > n ? slots : n;
}   // O(n) time · O(1) space
""",
    "queue-reconstruction-by-height": r"""
// Tallest first, and among equals the one with fewer people in front first; insert by index.
static int cmpPerson(const void *a, const void *b) {
    const int *x = *(const int *const *) a, *y = *(const int *const *) b;
    if (x[0] != y[0]) return y[0] - x[0];                  // height descending
    return x[1] - y[1];                                    // k ascending
}

int **reconstructQueue(int **people, int n, int *returnSize, int **returnColumnSizes) {
    qsort(people, (size_t) n, sizeof(int *), cmpPerson);
    int **out = malloc(sizeof(int *) * (size_t) n);
    int count = 0;
    for (int i = 0; i < n; i++) {
        int slot = people[i][1] < count ? people[i][1] : count;
        for (int j = count; j > slot; j--) out[j] = out[j - 1];   // shift right to make room
        out[slot] = people[i];
        count++;
    }
    *returnColumnSizes = malloc(sizeof(int) * (size_t) n);
    for (int i = 0; i < n; i++) (*returnColumnSizes)[i] = 2;
    *returnSize = n;
    return out;
}   // O(n^2) time (array inserts) · O(n) space
""",
    "two-city-scheduling": r"""
// Send everyone to A first, then move the n sendings with the best (B - A) to B.
static int cmpDiff(const void *a, const void *b) { return *(const int *) a - *(const int *) b; }

int twoCitySchedCost(int **costs, int n) {
    int *diffs = malloc(sizeof(int) * (size_t) n);
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += costs[i][0];                              // everyone flies to city A
        diffs[i] = costs[i][1] - costs[i][0];
    }
    qsort(diffs, (size_t) n, sizeof(int), cmpDiff);
    for (int i = 0; i < n / 2; i++) total += diffs[i];     // the cheapest switches to B
    free(diffs);
    return total;
}   // O(n log n) time · O(n) space
""",
    "minimum-number-of-arrows-to-burst-balloons": r"""
// Shoot at the earliest end; that arrow bursts every balloon starting before it.
static int cmpEnd(const void *a, const void *b) {
    const int *x = *(const int *const *) a, *y = *(const int *const *) b;
    return x[1] < y[1] ? -1 : x[1] > y[1] ? 1 : 0;
}

int findMinArrowShots(int **points, int n) {
    if (!n) return 0;
    qsort(points, (size_t) n, sizeof(int *), cmpEnd);
    int arrows = 1;
    long long lastArrow = points[0][1];                    // long long: the ends can be huge
    for (int i = 1; i < n; i++) {
        if (points[i][0] > lastArrow) {                    // a gap: a new arrow is needed
            arrows++;
            lastArrow = points[i][1];
        }
    }
    return arrows;
}   // O(n log n) time · O(1) space
""",
    "car-pooling": r"""
// Sweep the road: at every point the load must stay within capacity.
int carPooling(int **trips, int n, int capacity) {
    int delta[1001] = {0};                                 // stops are 0..1000
    for (int i = 0; i < n; i++) {
        delta[trips[i][1]] += trips[i][0];                 // passengers get on
        delta[trips[i][2]] -= trips[i][0];                 // and get off
    }
    int load = 0;
    for (int stop = 0; stop <= 1000; stop++) {
        load += delta[stop];
        if (load > capacity) return 0;
    }
    return 1;
}   // O(n + stops) time · O(stops) space
""",
    "candy": r"""
// Two passes: make the row non-decreasing to the right, then to the left.
int candy(const int *ratings, int n) {
    if (!n) return 0;
    int *candies = malloc(sizeof(int) * (size_t) n);
    for (int i = 0; i < n; i++) candies[i] = 1;
    for (int i = 1; i < n; i++)                            // rising slopes
        if (ratings[i] > ratings[i - 1]) candies[i] = candies[i - 1] + 1;
    for (int i = n - 2; i >= 0; i--)                       // falling slopes
        if (ratings[i] > ratings[i + 1] && candies[i] <= candies[i + 1]) candies[i] = candies[i + 1] + 1;
    int total = 0;
    for (int i = 0; i < n; i++) total += candies[i];
    free(candies);
    return total;
}   // O(n) time · O(n) space
""",
    "course-schedule-iii": r"""
// Take courses by deadline; if time runs out, drop the longest course taken so far.
static int cmpCourse(const void *a, const void *b) {
    const int *x = *(const int *const *) a, *y = *(const int *const *) b;
    return x[1] - y[1];                                    // by deadline
}

int scheduleCourse(int **courses, int n) {
    qsort(courses, (size_t) n, sizeof(int *), cmpCourse);
    int *taken = malloc(sizeof(int) * (size_t) n);          // kept sorted, longest first
    int count = 0;
    long long time = 0;
    for (int i = 0; i < n; i++) {
        int duration = courses[i][0], deadline = courses[i][1];
        if (time + duration <= deadline) {
            int j = count;
            while (j > 0 && taken[j - 1] < duration) { taken[j] = taken[j - 1]; j--; }
            taken[j] = duration;
            count++;
            time += duration;
        } else if (count && duration < taken[0]) {          // swap out the longest course
            time += duration - taken[0];
            int j = 0;
            while (j + 1 < count && taken[j + 1] > duration) { taken[j] = taken[j + 1]; j++; }
            taken[j] = duration;
        }
    }
    free(taken);
    return count;
}   // O(n^2) time (a heap gives O(n log n)) · O(n) space
""",
    "minimum-initial-energy-to-finish-tasks": r"""
// Do the tasks with the biggest (actual - minimum) first, keeping the energy as low as possible.
static int cmpEnergy(const void *a, const void *b) {
    const int *x = *(const int *const *) a, *y = *(const int *const *) b;
    return (y[1] - y[0]) - (x[1] - x[0]);                  // descending by the slack needed
}

int minimumEffort(int **tasks, int n) {
    qsort(tasks, (size_t) n, sizeof(int *), cmpEnergy);
    long long energy = 0, answer = 0;
    for (int i = 0; i < n; i++) {
        long long need = energy + tasks[i][0];
        if (need < tasks[i][1]) need = tasks[i][1];         // top up to the minimum first
        energy = need;
        if (energy > answer) answer = energy;
    }
    return (int) answer;
}   // O(n log n) time · O(1) space
""",
    "minimum-number-of-refueling-stops": r"""
// Drive as far as possible; when stuck, refuel at the station with the most fuel passed.
int minRefuelStops(int target, int startFuel, int **stations, int n) {
    long long *heap = malloc(sizeof(long long) * (size_t) (n + 1));
    int heapSize = 0, stops = 0;
    long long fuel = startFuel, position = 0;
    for (int i = 0; i <= n; i++) {
        long long next = i < n ? stations[i][0] : target;
        while (fuel < next - position) {                    // cannot reach the next point
            if (!heapSize) { free(heap); return -1; }
            int best = 0;                                   // pop the largest fuel seen
            for (int j = 1; j < heapSize; j++) if (heap[j] > heap[best]) best = j;
            fuel += heap[best];
            heap[best] = heap[--heapSize];
            stops++;
        }
        if (i < n) heap[heapSize++] = stations[i][1];       // remember this station's fuel
        position = next;
    }
    free(heap);
    return stops;
}   // O(n^2) time (a real heap gives O(n log n)) · O(n) space
""",
    "maximum-performance-of-a-team": r"""
// Sort by speed descending; the slowest member of the chosen group caps its efficiency.
static int cmpPair(const void *a, const void *b) {
    const int *x = *(const int *const *) a, *y = *(const int *const *) b;
    return y[0] - x[0];
}

int maxPerformance(int n, int **speedAndEfficiency, int k) {
    int **people = malloc(sizeof(int *) * (size_t) n);
    for (int i = 0; i < n; i++) people[i] = speedAndEfficiency[i];
    qsort(people, (size_t) n, sizeof(int *), cmpPair);      // speed descending
    long long *chosen = malloc(sizeof(long long) * (size_t) (k + 1));   // speeds, ascending
    int count = 0;
    long long sum = 0, best = 0;
    for (int i = 0; i < n; i++) {
        long long speed = people[i][0], efficiency = people[i][1];
        int j = count;
        while (j > 0 && chosen[j - 1] > speed) { chosen[j] = chosen[j - 1]; j--; }
        chosen[j] = speed;
        count++;
        sum += speed;
        if (count > k) {                                    // drop the slowest of the group
            count--;
            sum -= chosen[count];
        }
        long long score = sum * efficiency;
        if (score > best) best = score;
    }
    free(people); free(chosen);
    return (int) (best % 1000000007);
}   // O(n * k) time · O(k) space
""",
    "minimum-cost-to-hire-k-workers": r"""
// Sort by pay-per-quality; for each ratio keep the k cheapest qualities seen so far.
static int cmpWorker(const void *a, const void *b) {
    const int *x = *(const int *const *) a, *y = *(const int *const *) b;
    long long left = (long long) x[0] * y[1], right = (long long) y[0] * x[1];
    return left < right ? -1 : left > right ? 1 : 0;
}

double mincostToHireWorkers(int **workers, int n, int k) {
    int **list = malloc(sizeof(int *) * (size_t) n);
    for (int i = 0; i < n; i++) list[i] = workers[i];
    qsort(list, (size_t) n, sizeof(int *), cmpWorker);
    int *quality = malloc(sizeof(int) * (size_t) (k + 1));  // the paid group, quality ascending
    int count = 0;
    long long qualitySum = 0;
    double best = 1e18;
    for (int i = 0; i < n; i++) {
        int q = list[i][0], w = list[i][1];
        int j = count;
        while (j > 0 && quality[j - 1] > q) { quality[j] = quality[j - 1]; j--; }
        quality[j] = q;
        count++;
        qualitySum += q;
        if (count > k) {                                    // drop the most expensive worker
            count--;
            qualitySum -= quality[count];                   // sorted, so it is the last one
        }
        if (count == k) {
            double cost = (double) w / q * qualitySum;      // pay everyone at this ratio
            if (cost < best) best = cost;
        }
    }
    free(list); free(quality);
    return best;
}   // O(n * k) time · O(k) space
""",
    "ipo": r"""
// Take the most profitable affordable project, then spend the capital it returns.
int findMaximizedCapital(int k, int w, int *profits, int n, int *capital) {
    (void) n;
    int *used = calloc((size_t) n, sizeof(int));
    long long capitalNow = w;
    for (int step = 0; step < k; step++) {
        int best = -1;
        for (int i = 0; i < n; i++) {
            if (used[i] || capital[i] > capitalNow) continue;
            if (best < 0 || profits[i] > profits[best]) best = i;
        }
        if (best < 0) break;                               // nothing affordable left
        used[best] = 1;
        capitalNow += profits[best];
    }
    free(used);
    return (int) capitalNow;
}   // O(k * n) time (two heaps give O(n log n)) · O(n) space
""",
    "earliest-possible-day-of-full-bloom": r"""
// Growing takes as long as it takes; sow the slowest growers first.
static int cmpSeed(const void *a, const void *b) {
    const int *x = *(const int *const *) a, *y = *(const int *const *) b;
    return y[0] - x[0];                                    // slower growers first
}

int earliestFullBloom(int *plantTime, int n, int *growTime) {
    int **seeds = malloc(sizeof(int *) * (size_t) n);
    for (int i = 0; i < n; i++) {
        seeds[i] = malloc(sizeof(int) * 2);
        seeds[i][0] = growTime[i];
        seeds[i][1] = plantTime[i];
    }
    qsort(seeds, (size_t) n, sizeof(int *), cmpSeed);
    long long planted = 0, best = 0;
    for (int i = 0; i < n; i++) {
        planted += seeds[i][1];                            // planting days are sequential
        long long bloom = planted + seeds[i][0];
        if (bloom > best) best = bloom;
        free(seeds[i]);
    }
    free(seeds);
    return (int) best;
}   // O(n log n) time · O(n) space
""",
    "minimum-number-of-taps-to-open-to-water-a-garden": r"""
// Each tap covers [i - r, i + r]; always take the tap that reaches farthest.
int minTaps(int n, const int *ranges, int rangeCount) {
    (void) rangeCount;
    int *reach = calloc((size_t) n + 1, sizeof(int));
    for (int i = 0; i <= n; i++) {
        int left = i - ranges[i] < 0 ? 0 : i - ranges[i];
        int right = i + ranges[i] > n ? n : i + ranges[i];
        if (right > reach[left]) reach[left] = right;      // from that start, how far can we get
    }
    int taps = 0, covered = 0, farthest = 0;
    while (covered < n) {
        for (int start = 0; start <= covered; start++)     // any tap starting in the wet part
            if (reach[start] > farthest) farthest = reach[start];
        if (farthest <= covered) { free(reach); return -1; }
        taps++;
        covered = farthest;                                // water now reaches this far
    }
    free(reach);
    return taps;
}   // O(n^2) time · O(n) space
""",
    "maximum-number-of-tasks-you-can-assign": r"""
// Sort tasks and workers, binary search how many tasks can be done, then check the k
// easiest tasks from hardest to easiest: a bare-capable worker if there is one, otherwise
// the weakest worker who needs a pill.
static int cmpInt(const void *a, const void *b) {
    int x = *(const int *) a, y = *(const int *) b;
    return (x > y) - (x < y);
}

static int canDo(int *tasks, int n, int *workers, int m, int pills, int strength, int want) {
    int *pending = malloc(sizeof(int) * (size_t) (m + 1));
    int count = 0, w = m - 1, pillsLeft = pills;
    for (int t = n - 1; t >= n - want; t--) {
        while (w >= 0 && workers[w] + strength >= tasks[t]) {   // can reach it with a pill
            pending[count++] = workers[w];
            w--;
        }
        if (!count) { free(pending); return 0; }                // nobody can take this task
        int strongest = 0;
        for (int i = 1; i < count; i++) if (pending[i] > pending[strongest]) strongest = i;
        if (pending[strongest] >= tasks[t]) {                   // do it bare, keep the pills
            pending[strongest] = pending[--count];
        } else {
            if (pillsLeft <= 0) { free(pending); return 0; }
            pillsLeft--;                                        // spend a pill on the weakest
            int weakest = 0;
            for (int i = 1; i < count; i++) if (pending[i] < pending[weakest]) weakest = i;
            pending[weakest] = pending[--count];
        }
    }
    free(pending);
    return 1;
}

int maxTaskAssign(int *tasks, int n, int *workers, int m, int pills, int strength) {
    qsort(tasks, (size_t) n, sizeof(int), cmpInt);
    qsort(workers, (size_t) m, sizeof(int), cmpInt);
    int lo = 0, hi = n < m ? n : m;
    while (lo < hi) {
        int mid = (lo + hi + 1) / 2;
        if (canDo(tasks, n, workers, m, pills, strength, mid)) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}   // O(log n * n * m) time · O(m) space
""",
    "rearrange-string-k-distance-apart": r"""
// Place the most frequent letters one slot apart, always picking the busiest that is legal.
char *rearrangeString(const char *s, int k) {
    int n = (int) strlen(s);
    int count[26] = {0};
    for (int i = 0; i < n; i++) count[s[i] - 'a']++;
    char *out = malloc((size_t) n + 1);
    int *lastUsed = malloc(sizeof(int) * 26);
    for (int c = 0; c < 26; c++) lastUsed[c] = -k - 1;     // never used
    for (int pos = 0; pos < n; pos++) {
        int pick = -1;
        for (int c = 0; c < 26; c++) {
            if (!count[c] || pos - lastUsed[c] < k) continue;   // too soon to reuse
            if (pick < 0 || count[c] > count[pick]) pick = c;
        }
        if (pick < 0) { free(out); free(lastUsed); return strdup(""); }
        out[pos] = (char) ('a' + pick);
        count[pick]--;
        lastUsed[pick] = pos;
    }
    out[n] = '\0';
    free(lastUsed);
    return out;
}   // O(26 * n) time · O(n) space
""",
    "smallest-range-covering-elements-from-k-lists": r"""
// Keep one pointer per list; always advance the list that currently holds the minimum.
int *smallestRange(int **nums, int k, int *sizes, int *returnSize) {
    int *index = calloc((size_t) k, sizeof(int));
    int bestLow = 0, bestHigh = INT_MAX, exhausted = 0;
    while (!exhausted) {
        int low = INT_MAX, high = INT_MIN, minList = -1;
        for (int i = 0; i < k; i++) {
            if (index[i] >= sizes[i]) { exhausted = 1; break; }   // one list ran out: done
            int v = nums[i][index[i]];
            if (v < low) { low = v; minList = i; }
            if (v > high) high = v;
        }
        if (exhausted) break;
        if (high - low < bestHigh - bestLow) { bestLow = low; bestHigh = high; }
        index[minList]++;                                  // the minimum must move on
    }
    free(index);
    int *out = malloc(sizeof(int) * 2);
    out[0] = bestLow;
    out[1] = bestHigh;
    *returnSize = 2;
    return out;
}   // O(n * k) time · O(k) space
""",
}
