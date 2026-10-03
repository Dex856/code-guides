# Topic 11 · Heaps, Top-K & Design — C17 solutions
#
# C has no priority queue in the standard library, so each answer that needs one carries a
# tiny binary heap (an array plus sift-up / sift-down). That is the whole trick: `heap[0]`
# is always the answer's next element.

CODE = {
    "last-stone-weight": r"""
// A max-heap: smash the two heaviest, push the difference back.
static void siftDown(int *h, int n, int i) {
    while (1) {
        int l = 2 * i + 1, r = l + 1, big = i;
        if (l < n && h[l] > h[big]) big = l;
        if (r < n && h[r] > h[big]) big = r;
        if (big == i) return;
        int t = h[i]; h[i] = h[big]; h[big] = t;
        i = big;
    }
}

int lastStoneWeight(int *stones, int n) {
    for (int i = n / 2 - 1; i >= 0; i--) siftDown(stones, n, i);   // heapify in place
    int size = n;
    while (size > 1) {
        int a = stones[0];                                         // heaviest
        stones[0] = stones[--size];
        siftDown(stones, size, 0);
        int b = stones[0];                                         // second heaviest
        stones[0] = stones[--size];
        siftDown(stones, size, 0);
        if (a != b) {                                              // leftovers go back in
            stones[size++] = a - b;
            int i = size - 1;
            while (i > 0 && stones[(i - 1) / 2] < stones[i]) {     // sift up
                int t = stones[i]; stones[i] = stones[(i - 1) / 2]; stones[(i - 1) / 2] = t;
                i = (i - 1) / 2;
            }
        }
    }
    return size ? stones[0] : 0;
}   // O(n log n) time · O(1) extra space
""",
    "kth-largest-element-in-a-stream": r"""
// Keep a min-heap of exactly k values: its root is the k-th largest.
typedef struct { int *heap, size, k; } KthLargest;

int kthLargestAdd(KthLargest *obj, int val);              // used by the constructor below

static void up(int *h, int i) {
    while (i > 0 && h[(i - 1) / 2] > h[i]) {
        int t = h[i]; h[i] = h[(i - 1) / 2]; h[(i - 1) / 2] = t;
        i = (i - 1) / 2;
    }
}

static void down(int *h, int n, int i) {
    while (1) {
        int l = 2 * i + 1, r = l + 1, small = i;
        if (l < n && h[l] < h[small]) small = l;
        if (r < n && h[r] < h[small]) small = r;
        if (small == i) return;
        int t = h[i]; h[i] = h[small]; h[small] = t;
        i = small;
    }
}

KthLargest *kthLargestCreate(int k, int *nums, int n) {
    KthLargest *obj = malloc(sizeof(KthLargest));
    obj->heap = malloc(sizeof(int) * (size_t) k);
    obj->size = 0;
    obj->k = k;
    for (int i = 0; i < n; i++) kthLargestAdd(obj, nums[i]);
    return obj;
}

int kthLargestAdd(KthLargest *obj, int val) {
    if (obj->size < obj->k) {                              // still filling up
        obj->heap[obj->size++] = val;
        up(obj->heap, obj->size - 1);
    } else if (val > obj->heap[0]) {                       // beats the current k-th largest
        obj->heap[0] = val;
        down(obj->heap, obj->size, 0);
    }
    return obj->heap[0];
}   // O(log k) per add · O(k) space
""",
    "take-gifts-from-the-richest-pile": r"""
// Repeatedly take from the biggest pile: sqrt(floor) each time.
static int biggestPile(int *piles, int n) {
    int best = 0;
    for (int i = 1; i < n; i++) if (piles[i] > piles[best]) best = i;
    return best;
}

long long pickGifts(int *gifts, int n, int k) {
    for (int step = 0; step < k; step++) {
        int i = biggestPile(gifts, n);
        gifts[i] = (int) sqrt((double) gifts[i]);          // floor of the square root
    }
    long long total = 0;
    for (int i = 0; i < n; i++) total += gifts[i];
    return total;
}   // O(k * n) time (a heap gives O((n + k) log n)) · O(1) space
""",
    "maximum-product-of-two-elements-in-an-array": r"""
// The answer is (largest - 1) * (second largest - 1).
static int cmpInt(const void *a, const void *b) {
    int x = *(const int *) a, y = *(const int *) b;
    return (x > y) - (x < y);
}

int maxProduct(int *nums, int n) {
    qsort(nums, (size_t) n, sizeof(int), cmpInt);
    return (nums[n - 1] - 1) * (nums[n - 2] - 1);
}   // O(n log n) time · O(1) space
""",
    "the-k-weakest-rows-in-a-matrix": r"""
// Count the soldiers in each row, then sort the row indices by (count, index).
static int rowCount(int *row, int cols) {
    int lo = 0, hi = cols;                                 // rows are sorted: binary search
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (row[mid] == 1) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

static int sortKey[4096];
static int *sortCounts;

static int cmpRow(const void *a, const void *b) {
    int x = *(const int *) a, y = *(const int *) b;
    if (sortCounts[x] != sortCounts[y]) return sortCounts[x] - sortCounts[y];
    return x - y;
}

int *kWeakestRows(int **mat, int rows, int cols, int k, int *returnSize) {
    int *counts = malloc(sizeof(int) * (size_t) rows);
    int *index = malloc(sizeof(int) * (size_t) rows);
    for (int i = 0; i < rows; i++) { counts[i] = rowCount(mat[i], cols); index[i] = i; }
    sortCounts = counts;
    (void) sortKey;
    qsort(index, (size_t) rows, sizeof(int), cmpRow);
    int *out = malloc(sizeof(int) * (size_t) k);
    for (int i = 0; i < k; i++) out[i] = index[i];
    free(counts); free(index);
    *returnSize = k;
    return out;
}   // O(rows log cols + rows log rows) time · O(rows) space
""",
    "implement-queue-using-stacks": r"""
// Two lists: `in` receives pushes, `out` serves pops (filled only when empty).
typedef struct { int in[4096], out[4096]; int inTop, outTop; } MyQueue;

MyQueue *myQueueCreate(void) { return calloc(1, sizeof(MyQueue)); }

void myQueuePush(MyQueue *q, int x) { q->in[q->inTop++] = x; }

int myQueuePop(MyQueue *q) {
    if (!q->outTop)
        while (q->inTop) q->out[q->outTop++] = q->in[--q->inTop];   // reverse once, in bulk
    return q->out[--q->outTop];
}

int myQueuePeek(MyQueue *q) {
    if (!q->outTop)
        while (q->inTop) q->out[q->outTop++] = q->in[--q->inTop];
    return q->out[q->outTop - 1];
}

int myQueueEmpty(MyQueue *q) { return q->inTop == 0 && q->outTop == 0; }
// amortised O(1) per operation · O(n) space
""",
    "kth-largest-element-in-an-array": r"""
// Quickselect: partition around a pivot and only recurse into the side that matters.
static void swapInt(int *a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }

static int partition(int *a, int lo, int hi) {
    int pivot = a[hi], store = lo;
    for (int i = lo; i < hi; i++) if (a[i] < pivot) swapInt(a, i, store++);
    swapInt(a, store, hi);
    return store;
}

int findKthLargest(int *nums, int n, int k) {
    int target = n - k, lo = 0, hi = n - 1;               // the k-th largest is at n - k sorted
    while (lo <= hi) {
        int p = partition(nums, lo, hi);
        if (p == target) return nums[p];
        if (p < target) lo = p + 1;
        else hi = p - 1;
    }
    return -1;
}   // O(n) average time · O(1) space
""",
    "k-closest-points-to-origin": r"""
// Sort by squared distance — no square root needed to compare.
static int **gPoints;

static int cmpPoint(const void *a, const void *b) {
    const int *x = gPoints[*(const int *) a], *y = gPoints[*(const int *) b];
    long long dx = (long long) x[0] * x[0] + (long long) x[1] * x[1];
    long long dy = (long long) y[0] * y[0] + (long long) y[1] * y[1];
    return dx < dy ? -1 : dx > dy ? 1 : 0;
}

int **kClosest(int **points, int n, int k, int *returnSize) {
    int *index = malloc(sizeof(int) * (size_t) n);
    for (int i = 0; i < n; i++) index[i] = i;
    gPoints = points;
    qsort(index, (size_t) n, sizeof(int), cmpPoint);
    int **out = malloc(sizeof(int *) * (size_t) k);
    for (int i = 0; i < k; i++) out[i] = points[index[i]];
    free(index);
    *returnSize = k;
    return out;
}   // O(n log n) time · O(n) space
""",
    "reorganize-string": r"""
// Alternate between the two most frequent letters; adjacency is impossible if it works out.
char *reorganizeString(const char *s) {
    int n = (int) strlen(s);
    int count[26] = {0};
    for (int i = 0; i < n; i++) count[s[i] - 'a']++;
    for (int c = 0; c < 26; c++) if (count[c] > (n + 1) / 2) return strdup("");
    char *out = malloc((size_t) n + 1);
    int previous = -1;
    for (int pos = 0; pos < n; pos++) {
        int pick = -1;
        for (int c = 0; c < 26; c++) {
            if (!count[c] || c == previous) continue;
            if (pick < 0 || count[c] > count[pick]) pick = c;
        }
        out[pos] = (char) ('a' + pick);
        count[pick]--;
        previous = pick;
    }
    out[n] = '\0';
    return out;
}   // O(26 * n) time · O(n) space
""",
    "longest-happy-string": r"""
// Always use the letter with the most left, unless it would make three in a row.
char *longestDiverseString(int a, int b, int c) {
    char *out = malloc(4096);
    int n = 0;
    int counts[3] = {a, b, c};
    while (1) {
        int pick = -1;
        for (int i = 0; i < 3; i++) {
            if (!counts[i]) continue;
            int repeats = n >= 2 && out[n - 1] == 'a' + i && out[n - 2] == 'a' + i;
            if (repeats) continue;                         // would be three in a row
            if (pick < 0 || counts[i] > counts[pick]) pick = i;
        }
        if (pick < 0) break;
        out[n++] = (char) ('a' + pick);
        counts[pick]--;
    }
    out[n] = '\0';
    return out;
}   // O(a + b + c) time · O(a + b + c) space
""",
    "furthest-building-you-can-reach": r"""
// Climb while bricks suffice; replace the tallest climb so far with a ladder when needed.
int furthestBuilding(int *heights, int n, int bricks, int ladders) {
    int *ladderClimbs = malloc(sizeof(int) * (size_t) (ladders + 1));   // ascending
    int count = 0;
    for (int i = 1; i < n; i++) {
        int climb = heights[i] - heights[i - 1];
        if (climb <= 0) continue;                          // downhill is free
        int j = count;
        while (j > 0 && ladderClimbs[j - 1] > climb) { ladderClimbs[j] = ladderClimbs[j - 1]; j--; }
        ladderClimbs[j] = climb;
        count++;
        if (count > ladders) {                             // the shortest climb needs bricks
            int shortest = ladderClimbs[0];
            for (int t = 0; t < count - 1; t++) ladderClimbs[t] = ladderClimbs[t + 1];
            count--;
            bricks -= shortest;
            if (bricks < 0) { free(ladderClimbs); return i - 1; }
        }
    }
    free(ladderClimbs);
    return n - 1;
}   // O(n * ladders) time · O(ladders) space
""",
    "design-twitter": r"""
// A single feed table: who posted, when, and what. `follow` is a small bit matrix.
typedef struct {
    int *user, *tweet, time[8192];
    int n, clock;
    char following[512][512];
} Twitter;

Twitter *twitterCreate(void) { return calloc(1, sizeof(Twitter)); }

void twitterPostTweet(Twitter *t, int userId, int tweetId) {
    t->user[t->n] = userId;
    t->tweet[t->n] = tweetId;
    t->time[t->n] = ++t->clock;
    t->n++;
}

void twitterFollow(Twitter *t, int followerId, int followeeId) {
    t->following[followerId % 512][followeeId % 512] = 1;
}

void twitterUnfollow(Twitter *t, int followerId, int followeeId) {
    t->following[followerId % 512][followeeId % 512] = 0;
}

int *twitterGetNewsFeed(Twitter *t, int userId, int *returnSize) {
    int *out = malloc(sizeof(int) * 10);
    int count = 0;
    for (int i = t->n - 1; i >= 0 && count < 10; i--) {   // newest first
        int author = t->user[i];
        if (author == userId || t->following[userId % 512][author % 512]) out[count++] = t->tweet[i];
    }
    *returnSize = count;
    return out;
}   // O(n) per feed request · O(n) space
""",
    "find-k-pairs-with-smallest-sums": r"""
// Pairs from sorted arrays: always advance the side that is currently smaller.
int **kSmallestPairs(int *a, int n, int *b, int m, int k, int *returnSize, int **returnColumnSizes) {
    int **out = malloc(sizeof(int *) * (size_t) (k < n * m ? k : n * m));
    *returnColumnSizes = malloc(sizeof(int) * (size_t) (k < n * m ? k : n * m));
    int count = 0, i = 0, j = 0;
    while (count < k && i < n && j < m) {
        out[count] = malloc(sizeof(int) * 2);
        out[count][0] = a[i];
        out[count][1] = b[j];
        (*returnColumnSizes)[count] = 2;
        count++;
        long long nextI = i + 1 < n ? (long long) a[i + 1] + b[j] : LLONG_MAX;
        long long nextJ = j + 1 < m ? (long long) a[i] + b[j + 1] : LLONG_MAX;
        if (nextI <= nextJ) i++;                           // advance the smaller side
        else j++;
    }
    *returnSize = count;
    return out;
}   // O(k) time · O(k) space
""",
    "kth-smallest-element-in-a-sorted-matrix": r"""
// Binary search the value and count how many entries are <= it.
int kthSmallest(int rows, int cols, int **matrix, int k) {
    int lo = matrix[0][0], hi = matrix[rows - 1][cols - 1];
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2, count = 0;
        for (int r = 0; r < rows; r++) {
            int c = cols - 1;                              // count each row from the right
            while (c >= 0 && matrix[r][c] > mid) c--;
            count += c + 1;
        }
        if (count >= k) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}   // O((rows + cols) log range) time · O(1) space
""",
    "seat-reservation-manager": r"""
// The smallest free seat is the next unused number, because seats are handed out in order.
typedef struct { char *taken; int size, next; } SeatManager;

SeatManager *seatManagerCreate(int n) {
    SeatManager *m = calloc(1, sizeof(SeatManager));
    m->taken = calloc((size_t) n + 2, 1);
    m->size = n;
    m->next = 1;
    return m;
}

int seatManagerReserve(SeatManager *m) {
    while (m->next <= m->size && m->taken[m->next]) m->next++;      // skip unreserved ones
    m->taken[m->next] = 1;
    return m->next;
}

void seatManagerUnreserve(SeatManager *m, int seatNumber) {
    m->taken[seatNumber] = 0;
    if (seatNumber < m->next) m->next = seatNumber;        // this seat is now the smallest
}   // O(1) amortised per call · O(n) space
""",
    "maximum-number-of-events-that-can-be-attended": r"""
// Take the earliest ending event each day; a "next free day" array skips the days already used.
static int cmpEventEnd(const void *a, const void *b) {
    const int *x = *(const int *const *) a, *y = *(const int *const *) b;
    return x[1] - y[1];
}

static int findFreeDay(int *next, int day) {
    while (next[day] != day) { next[day] = next[next[day]]; day = next[day]; }   // path halving
    return day;
}

int maxEvents(int **events, int n) {
    int lastDay = 0;
    for (int i = 0; i < n; i++) if (events[i][1] > lastDay) lastDay = events[i][1];
    int *next = malloc(sizeof(int) * (size_t) (lastDay + 2));
    for (int d = 0; d <= lastDay + 1; d++) next[d] = d;     // lastDay + 1 means "no day left"
    qsort(events, (size_t) n, sizeof(int *), cmpEventEnd);
    int attended = 0;
    for (int i = 0; i < n; i++) {
        int day = findFreeDay(next, events[i][0]);          // earliest free day from the start
        if (day > events[i][1]) continue;                   // the event has already ended
        attended++;
        next[day] = findFreeDay(next, day + 1);             // that day is taken now
    }
    free(next);
    return attended;
}   // O(n log n + n \u03b1(days)) time \u00b7 O(days) space
""",
    "process-tasks-using-servers": r"""
// Two heaps: free servers by (weight, index) and busy servers by (free time, weight, index).
typedef struct { int weight, index; } FreeServer;
typedef struct { long long freeTime; int weight, index; } BusyServer;

static FreeServer freeHeap[100001];
static BusyServer busyHeap[100001];
static int freeSize, busySize;

static void freePush(int weight, int index) {              // sift up
    int i = freeSize++;
    freeHeap[i].weight = weight;
    freeHeap[i].index = index;
    while (i > 0) {
        int parent = (i - 1) / 2;
        FreeServer *a = &freeHeap[parent], *b = &freeHeap[i];
        if (a->weight < b->weight || (a->weight == b->weight && a->index <= b->index)) break;
        FreeServer t = *a; *a = *b; *b = t;
        i = parent;
    }
}

static FreeServer freePop(void) {
    FreeServer top = freeHeap[0];
    freeHeap[0] = freeHeap[--freeSize];
    int i = 0;
    while (1) {
        int l = 2 * i + 1, r = l + 1, best = i;
        if (l < freeSize && (freeHeap[l].weight < freeHeap[best].weight ||
            (freeHeap[l].weight == freeHeap[best].weight && freeHeap[l].index < freeHeap[best].index))) best = l;
        if (r < freeSize && (freeHeap[r].weight < freeHeap[best].weight ||
            (freeHeap[r].weight == freeHeap[best].weight && freeHeap[r].index < freeHeap[best].index))) best = r;
        if (best == i) break;
        FreeServer t = freeHeap[i]; freeHeap[i] = freeHeap[best]; freeHeap[best] = t;
        i = best;
    }
    return top;
}

static int busyLess(const BusyServer *a, const BusyServer *b) {
    if (a->freeTime != b->freeTime) return a->freeTime < b->freeTime;
    if (a->weight != b->weight) return a->weight < b->weight;
    return a->index < b->index;
}

static void busyPush(long long freeTime, int weight, int index) {
    int i = busySize++;
    busyHeap[i].freeTime = freeTime;
    busyHeap[i].weight = weight;
    busyHeap[i].index = index;
    while (i > 0) {
        int parent = (i - 1) / 2;
        if (!busyLess(&busyHeap[i], &busyHeap[parent])) break;
        BusyServer t = busyHeap[i]; busyHeap[i] = busyHeap[parent]; busyHeap[parent] = t;
        i = parent;
    }
}

static BusyServer busyPop(void) {
    BusyServer top = busyHeap[0];
    busyHeap[0] = busyHeap[--busySize];
    int i = 0;
    while (1) {
        int l = 2 * i + 1, r = l + 1, best = i;
        if (l < busySize && busyLess(&busyHeap[l], &busyHeap[best])) best = l;
        if (r < busySize && busyLess(&busyHeap[r], &busyHeap[best])) best = r;
        if (best == i) break;
        BusyServer t = busyHeap[i]; busyHeap[i] = busyHeap[best]; busyHeap[best] = t;
        i = best;
    }
    return top;
}

int *assignTasks(int *servers, int n, int *tasks, int m, int *returnSize) {
    freeSize = busySize = 0;
    int *out = malloc(sizeof(int) * (size_t) m);
    for (int i = 0; i < n; i++) freePush(servers[i], i);
    long long time = 0;
    for (int t = 0; t < m; t++) {
        if (time < t) time = t;                            // tasks arrive one per second
        while (busySize && busyHeap[0].freeTime <= time) {
            BusyServer done = busyPop();
            freePush(done.weight, done.index);
        }
        if (!freeSize) {                                   // everybody busy: skip to the next free
            time = busyHeap[0].freeTime;
            while (busySize && busyHeap[0].freeTime <= time) {
                BusyServer done = busyPop();
                freePush(done.weight, done.index);
            }
        }
        FreeServer chosen = freePop();
        out[t] = chosen.index;                             // lightest qualifying server
        busyPush(time + tasks[t], chosen.weight, chosen.index);
    }
    *returnSize = m;
    return out;
}   // O((n + m) log n) time \u00b7 O(n + m) space
""",
    "time-based-key-value-store": r"""
// Append-only history per (key, timestamp) pair, scanned backwards for the newest fit.
typedef struct {
    char keys[4096][32];
    char values[4096][128];
    int times[4096], n;
} TimeMap;

TimeMap *timeMapCreate(void) { return calloc(1, sizeof(TimeMap)); }

void timeMapSet(TimeMap *t, const char *key, const char *value, int timestamp) {
    snprintf(t->keys[t->n], 32, "%s", key);
    snprintf(t->values[t->n], 128, "%s", value);
    t->times[t->n] = timestamp;
    t->n++;
}

char *timeMapGet(TimeMap *t, const char *key, int timestamp) {
    int best = -1;
    for (int i = 0; i < t->n; i++)                          // newest timestamp <= given one
        if (!strcmp(t->keys[i], key) && t->times[i] <= timestamp && t->times[i] > best) best = t->times[i];
    if (best < 0) return strdup("");                       // the API returns an empty string
    for (int i = 0; i < t->n; i++)
        if (!strcmp(t->keys[i], key) && t->times[i] == best) return strdup(t->values[i]);
    return strdup("");
}   // O(n) per get · O(n) space
""",
    "find-median-from-data-stream": r"""
// Two heaps: a max-heap for the lower half and a min-heap for the upper half.
typedef struct {
    int lower[8192], upper[8192];
    int lowerSize, upperSize;
} MedianFinder;

static void pushLower(MedianFinder *f, int v) {           // max-heap
    int i = f->lowerSize++;
    f->lower[i] = v;
    while (i > 0 && f->lower[(i - 1) / 2] < f->lower[i]) {
        int t = f->lower[i]; f->lower[i] = f->lower[(i - 1) / 2]; f->lower[(i - 1) / 2] = t;
        i = (i - 1) / 2;
    }
}

static int popLower(MedianFinder *f) {
    int top = f->lower[0];
    f->lower[0] = f->lower[--f->lowerSize];
    int i = 0;
    while (1) {
        int l = 2 * i + 1, r = l + 1, big = i;
        if (l < f->lowerSize && f->lower[l] > f->lower[big]) big = l;
        if (r < f->lowerSize && f->lower[r] > f->lower[big]) big = r;
        if (big == i) break;
        int t = f->lower[i]; f->lower[i] = f->lower[big]; f->lower[big] = t;
        i = big;
    }
    return top;
}

static void pushUpper(MedianFinder *f, int v) {           // min-heap
    int i = f->upperSize++;
    f->upper[i] = v;
    while (i > 0 && f->upper[(i - 1) / 2] > f->upper[i]) {
        int t = f->upper[i]; f->upper[i] = f->upper[(i - 1) / 2]; f->upper[(i - 1) / 2] = t;
        i = (i - 1) / 2;
    }
}

static int popUpper(MedianFinder *f) {
    int top = f->upper[0];
    f->upper[0] = f->upper[--f->upperSize];
    int i = 0;
    while (1) {
        int l = 2 * i + 1, r = l + 1, small = i;
        if (l < f->upperSize && f->upper[l] < f->upper[small]) small = l;
        if (r < f->upperSize && f->upper[r] < f->upper[small]) small = r;
        if (small == i) break;
        int t = f->upper[i]; f->upper[i] = f->upper[small]; f->upper[small] = t;
        i = small;
    }
    return top;
}

MedianFinder *medianFinderCreate(void) { return calloc(1, sizeof(MedianFinder)); }

void medianFinderAddNum(MedianFinder *f, int num) {
    pushLower(f, num);
    if (f->lowerSize > f->upperSize + 1) pushUpper(f, popLower(f));   // keep the sizes close
    if (f->upperSize && f->lower[0] > f->upper[0]) {                  // and the halves ordered
        int a = popLower(f), b = popUpper(f);
        pushLower(f, b);
        pushUpper(f, a);
    }
}

double medianFinderFindMedian(MedianFinder *f) {
    if (f->lowerSize > f->upperSize) return f->lower[0];
    return (f->lower[0] + f->upper[0]) / 2.0;
}   // O(log n) per add · O(n) space
""",
    "sliding-window-median": r"""
// Insertion-sorted window: the median is simply the middle slot (or two middle slots).
double *medianSlidingWindow(int *nums, int n, int k, int *returnSize) {
    double *out = malloc(sizeof(double) * (size_t) (n - k + 1));
    int *window = malloc(sizeof(int) * (size_t) (k + 1));
    int count = 0, written = 0;
    for (int i = 0; i < n; i++) {
        int j = count;                                     // keep `window` sorted as we insert
        while (j > 0 && window[j - 1] > nums[i]) { window[j] = window[j - 1]; j--; }
        window[j] = nums[i];
        count++;
        if (i >= k) {                                      // drop the element leaving the window
            for (int t = 0; t < count; t++)
                if (window[t] == nums[i - k]) {
                    for (int m = t; m < count - 1; m++) window[m] = window[m + 1];
                    break;
                }
            count--;
        }
        if (count == k) {
            if (k % 2) out[written++] = window[k / 2];
            else out[written++] = (window[k / 2 - 1] + window[k / 2]) / 2.0;
        }
    }
    free(window);
    *returnSize = written;
    return out;
}   // O(n * k) time \u00b7 O(k) space
""",
    "find-the-kth-smallest-sum-of-a-matrix-with-sorted-rows": r"""
// Binary search the sum; count how many combinations stay under it with a DP over rows.
int kthSmallestSum(int **mat, int rows, int cols, int k) {
    int lo = 0, hi = 0;
    for (int r = 0; r < rows; r++) {
        lo += mat[r][0];
        hi += mat[r][cols - 1];
    }
    int **count = malloc(sizeof(int *) * (size_t) rows);
    for (int r = 0; r < rows; r++) count[r] = calloc((size_t) (hi + 1), sizeof(int));
    for (int c = 0; c < cols; c++) count[0][mat[0][c]] = 1;
    for (int r = 1; r < rows; r++)
        for (int s = 0; s <= hi; s++) {
            if (!count[r - 1][s]) continue;
            for (int c = 0; c < cols; c++)
                if (s + mat[r][c] <= hi) count[r][s + mat[r][c]] = 1;
        }
    while (lo < hi) {                                     // walk up until k sums are covered
        int mid = lo + (hi - lo) / 2, total = 0;
        for (int s = 0; s <= mid; s++) total += count[rows - 1][s];
        if (total >= k) hi = mid;
        else lo = mid + 1;
    }
    for (int r = 0; r < rows; r++) free(count[r]);
    free(count);
    return lo;
}   // O(rows * sum) time · O(rows * sum) space
""",
    "the-skyline-problem": r"""
// Collect every building's left and right wall, then sweep the horizontal line.
typedef struct { int x, height; } Edge;

static Edge gEdges[8192];
static int gEdgeCount;

static int cmpEdge(const void *a, const void *b) {
    const Edge *x = a, *y = b;
    if (x->x != y->x) return x->x - y->x;
    return y->height - x->height;                          // tall starts first, short ends last
}

int **getSkyline(int **buildings, int n, int *returnSize, int **returnColumnSizes) {
    gEdgeCount = 0;
    for (int i = 0; i < n; i++) {
        gEdges[gEdgeCount].x = buildings[i][0];
        gEdges[gEdgeCount].height = -buildings[i][2];      // negative marks a start
        gEdgeCount++;
        gEdges[gEdgeCount].x = buildings[i][1];
        gEdges[gEdgeCount].height = buildings[i][2];       // positive marks an end
        gEdgeCount++;
    }
    qsort(gEdges, (size_t) gEdgeCount, sizeof(Edge), cmpEdge);
    int *heights = calloc((size_t) gEdgeCount, sizeof(int));   // active heights
    int active = 0;
    int **out = malloc(sizeof(int *) * (size_t) (gEdgeCount + 1));
    *returnColumnSizes = malloc(sizeof(int) * (size_t) (gEdgeCount + 1));
    int count = 0, previousMax = 0;
    for (int i = 0; i < gEdgeCount; i++) {
        int h = gEdges[i].height;
        if (h < 0) heights[active++] = -h;                 // a building starts
        else {
            for (int k = 0; k < active; k++) if (heights[k] == h) {
                heights[k] = heights[--active];
                break;
            }
        }
        if (i + 1 < gEdgeCount && gEdges[i + 1].x == gEdges[i].x) continue;   // same x: one point
        int tallest = 0;
        for (int k = 0; k < active; k++) if (heights[k] > tallest) tallest = heights[k];
        if (tallest != previousMax) {
            out[count] = malloc(sizeof(int) * 2);
            out[count][0] = gEdges[i].x;
            out[count][1] = tallest;
            (*returnColumnSizes)[count] = 2;
            count++;
            previousMax = tallest;
        }
    }
    free(heights);
    *returnSize = count;
    return out;
}   // O(n^2) time (a multiset gives O(n log n)) · O(n) space
""",
    "trapping-rain-water-ii": r"""
// Flood inwards from the border: water above a cell is the smallest wall met on the way in.
int trapRainWater(int **heightMap, int rows, int cols) {
    int total = rows * cols;
    int *seen = calloc((size_t) total, sizeof(int));
    int *queue = malloc(sizeof(int) * (size_t) total);
    int *water = malloc(sizeof(int) * (size_t) total);
    int head = 0, tail = 0, answer = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) {
            if (r && r != rows - 1 && c && c != cols - 1) continue;   // the border is the wall
            seen[r * cols + c] = 1;
            water[r * cols + c] = heightMap[r][c];
            queue[tail++] = r * cols + c;
        }
    while (head < tail) {                                  // always take the lowest cell so far
        int best = head;
        for (int k = head; k < tail; k++)
            if (water[queue[k]] < water[queue[best]]) best = k;
        int cell = queue[best];
        queue[best] = queue[head++];
        int r = cell / cols, c = cell % cols;
        int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
        for (int k = 0; k < 4; k++) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
            int next = nr * cols + nc;
            if (seen[next]) continue;
            seen[next] = 1;
            int level = water[cell] > heightMap[nr][nc] ? water[cell] : heightMap[nr][nc];
            water[next] = level;
            answer += level - heightMap[nr][nc];           // the water sitting on this cell
            queue[tail++] = next;
        }
    }
    free(seen); free(queue); free(water);
    return answer;
}   // O((rows * cols)^2) with this scan (a heap gives O(n log n)) · O(rows * cols) space
""",
    "max-value-of-equation": r"""
// A deque of candidates in decreasing (value - x): the front is always the best partner.
int findMaxValueOfEquation(int **points, int n, int k) {
    int *deque = malloc(sizeof(int) * (size_t) (n + 1));
    int head = 0, tail = 0, best = INT_MIN;
    for (int i = 0; i < n; i++) {
        while (head < tail && points[i][0] - points[deque[head]][0] > k) head++;  // too far left
        if (head < tail) {
            int j = deque[head];
            int value = points[j][1] - points[j][0] + points[i][1] + points[i][0];
            if (value > best) best = value;
        }
        while (head < tail && points[deque[tail - 1]][1] - points[deque[tail - 1]][0]
                                <= points[i][1] - points[i][0]) tail--;           // weaker: drop
        deque[tail++] = i;
    }
    free(deque);
    return best;
}   // O(n) time \u00b7 O(n) space
""",
    "construct-target-array-with-multiple-sums": r"""
// Reverse: the biggest element must have been the sum of the rest, so replace it.
int isPossible(int *target, int n) {
    if (n == 1) return target[0] == 1;
    long long sum = 0;
    for (int i = 0; i < n; i++) sum += target[i];
    while (1) {
        int biggest = 0;
        for (int i = 1; i < n; i++) if (target[i] > target[biggest]) biggest = i;
        if (target[biggest] == 1) return 1;
        long long rest = sum - target[biggest];
        if (rest < 1 || target[biggest] <= rest) return 0;
        long long replacement = target[biggest] % rest;     // undo as many steps as possible
        if (replacement == 0) replacement = rest;           // keep the sum valid
        sum = rest + replacement;
        target[biggest] = (int) replacement;
    }
}   // O(n * log max) time · O(1) space
""",
    "minimum-difference-in-sums-after-removal-of-elements": r"""
// prefix[i] = best sum of n elements from the first part, suffix[i] = best from the last.
static long long *maxSumsLeft(const int *a, int n, int keep) {
    long long *best = malloc(sizeof(long long) * (size_t) (n + 1));
    long long sum = 0;
    int *heap = malloc(sizeof(int) * (size_t) (keep + 1));   // max-heap of the kept elements
    int size = 0;
    for (int i = 0; i < n; i++) {
        int j = size++;
        heap[j] = a[i];
        while (j > 0 && heap[(j - 1) / 2] < heap[j]) {
            int t = heap[j]; heap[j] = heap[(j - 1) / 2]; heap[(j - 1) / 2] = t;
            j = (j - 1) / 2;
        }
        sum += a[i];
        if (size > keep) {                                  // drop the largest: keep the n smallest
            sum -= heap[0];
            heap[0] = heap[--size];
            int i2 = 0;
            while (1) {
                int l = 2 * i2 + 1, r = l + 1, big = i2;
                if (l < size && heap[l] > heap[big]) big = l;
                if (r < size && heap[r] > heap[big]) big = r;
                if (big == i2) break;
                int t = heap[i2]; heap[i2] = heap[big]; heap[big] = t;
                i2 = big;
            }
        }
        best[i + 1] = sum;
    }
    free(heap);
    return best;
}

long long minimumDifference(int *nums, int n) {
    int third = n / 3;
    long long *leftBest = maxSumsLeft(nums, n, third);
    int *reversed = malloc(sizeof(int) * (size_t) n);
    for (int i = 0; i < n; i++) reversed[i] = -nums[n - 1 - i];   // negate to reuse the helper
    long long *rightBest = maxSumsLeft(reversed, n, third);
    long long answer = LLONG_MAX;
    for (int i = third; i <= 2 * third; i++) {
        long long difference = leftBest[i] - rightBest[n - i];    // rightBest holds negated values
        if (difference < answer) answer = difference;
    }
    free(leftBest); free(rightBest); free(reversed);
    return answer;
}   // O(n log n) time · O(n) space
""",
    "insert-delete-getrandom-o1-duplicates-allowed": r"""
// Values in one array for O(1) random access; per-value index buckets point at positions.
#define RC_BUCKETS 4096
#define RC_SLOTS 128

typedef struct {
    int *values, size;
    int bucket[RC_BUCKETS][RC_SLOTS];                       // positions holding this value
    int bucketCount[RC_BUCKETS];
    int bucketOf[200000], slotOf[200000];                   // where each position lives
} RandomizedCollection;

static int rcHash(int value) {
    int key = value % RC_BUCKETS;
    return key < 0 ? key + RC_BUCKETS : key;
}

RandomizedCollection *randomizedCollectionCreate(void) {
    RandomizedCollection *c = calloc(1, sizeof(RandomizedCollection));
    c->values = malloc(sizeof(int) * 200000);
    return c;
}

int randomizedCollectionInsert(RandomizedCollection *c, int value) {
    int key = rcHash(value);
    int fresh = c->bucketCount[key] == 0 ? 1 : 0;
    int position = c->size++;
    c->values[position] = value;
    c->bucketOf[position] = key;
    c->slotOf[position] = c->bucketCount[key];
    c->bucket[key][c->bucketCount[key]++] = position;
    return fresh;
}

int randomizedCollectionRemove(RandomizedCollection *c, int value) {
    int key = rcHash(value);
    int found = -1;
    for (int s = 0; s < c->bucketCount[key]; s++)            // a bucket may hold several values
        if (c->values[c->bucket[key][s]] == value) { found = s; break; }
    if (found < 0) return 0;
    int position = c->bucket[key][found];
    int last = c->size - 1;
    if (position != last) {                                  // move the array's last value here
        int movedKey = c->bucketOf[last], movedSlot = c->slotOf[last];
        c->values[position] = c->values[last];
        c->bucketOf[position] = movedKey;
        c->slotOf[position] = movedSlot;
        c->bucket[movedKey][movedSlot] = position;           // its index bucket follows it
    }
    c->size--;
    int lastSlot = --c->bucketCount[key];                    // drop the removed position
    if (found != lastSlot) {
        int swapped = c->bucket[key][lastSlot];
        c->bucket[key][found] = swapped;
        c->slotOf[swapped] = found;
    }
    return 1;
}

int randomizedCollectionGetRandom(RandomizedCollection *c) {
    return c->values[rand() % c->size];
}   // O(1) average per operation \u00b7 O(n + buckets) space
""",
    "minimum-cost-to-reach-destination-in-time": r"""
// DP over (time, city): the cheapest way to be there with that much time spent.
int minCost(int maxTime, int **edges, int n, int *passingFees, int feeCount) {
    const int INF = INT_MAX / 4;
    (void) feeCount;
    int rows = n + 1;
    int *dp = malloc(sizeof(int) * (size_t) rows * (size_t) (maxTime + 1));
    for (int i = 0; i < rows * (maxTime + 1); i++) dp[i] = INF;
    dp[0 * (maxTime + 1) + 0] = passingFees[0];
    for (int t = 0; t <= maxTime; t++) {
        for (int v = 0; v < n; v++) {
            int here = dp[v * (maxTime + 1) + t];
            if (here >= INF) continue;
            for (int e = 0; e < n; e++) {                  // edges are given as plain triples
                int a = edges[e][0], b = edges[e][1], w = edges[e][2];
                int next = -1;
                if (a == v) next = b;
                else if (b == v) next = a;
                if (next < 0 || t + w > maxTime) continue;
                int cost = here + passingFees[next];
                if (cost < dp[next * (maxTime + 1) + t + w]) dp[next * (maxTime + 1) + t + w] = cost;
            }
        }
    }
    int best = INF;
    for (int t = 0; t <= maxTime; t++) {
        int cost = dp[(n - 1) * (maxTime + 1) + t];
        if (cost < best) best = cost;
    }
    free(dp);
    return best >= INF ? -1 : best;
}   // O(maxTime * n * E) time · O(n * maxTime) space
""",
    "minimize-deviation-in-array": r"""
// Halve the largest odd multiples: keep the maximum as low as possible while raising the minimum.
int minimumDeviation(int *nums, int n) {
    long long *values = malloc(sizeof(long long) * (size_t) n);
    long long lowest = LLONG_MAX;
    for (int i = 0; i < n; i++) {
        long long v = nums[i];
        if (v % 2) v *= 2;                                 // odds can only be doubled once
        values[i] = v;
        if (v < lowest) lowest = v;
    }
    long long best = LLONG_MAX;
    while (1) {
        int biggest = 0;
        for (int i = 1; i < n; i++) if (values[i] > values[biggest]) biggest = i;
        long long span = values[biggest] - lowest;
        if (span < best) best = span;
        if (values[biggest] % 2) break;                    // it cannot be halved any further
        values[biggest] /= 2;
        if (values[biggest] < lowest) lowest = values[biggest];
    }
    free(values);
    return (int) best;
}   // O(n log max) time · O(n) space
""",
    "maximum-number-of-robots-within-budget": r"""
// Sliding window: a heap keeps the largest charge cost inside the current window.
int maximumRobots(int *chargeTimes, int n, int *runningCosts, int m, long long budget) {
    int *deque = malloc(sizeof(int) * (size_t) (n + 1));   // indices of decreasing charge times
    int head = 0, tail = 0, left = 0, best = 0;
    long long cost = 0;
    for (int right = 0; right < n; right++) {
        cost += runningCosts[right];
        while (tail > head && chargeTimes[deque[tail - 1]] <= chargeTimes[right]) tail--;  // monotone
        deque[tail++] = right;
        while (head < tail && (long long) chargeTimes[deque[head]] + (long long) (right - left + 1) * cost > budget) {
            cost -= runningCosts[left];                    // shrink from the left
            if (deque[head] == left) head++;
            left++;
        }
        if (right - left + 1 > best) best = right - left + 1;
    }
    free(deque);
    return best;
}   // O(n) time · O(n) space
""",
}
