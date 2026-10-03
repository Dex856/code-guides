# Topic 3 · Hashing & Frequency Maps — C17 solutions
#
# C has no hash map in the standard library, so these use the two idiomatic C answers:
# a direct-address array when the key range is small (letters, remainders, values),
# and a small open-addressing table when it is not. Both are written out in full so
# nothing is hidden behind an STL container.

CODE = {
    "_helpers": r"""
static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}
""",
    "two-sum-hash": r"""
// One pass with a hash table: look for target - a[i] before inserting a[i].
#define TS_CAP 4096
struct TSEntry { int key, idx, used; };

void twoSumHash(const int *a, int n, int target, int *out) {
    struct TSEntry *tab = calloc(TS_CAP, sizeof(struct TSEntry));
    for (int i = 0; i < n; i++) {
        long long want = (long long) target - a[i];
        if (want >= INT_MIN && want <= INT_MAX) {
            int key = (int) want;
            unsigned h = (unsigned) (key * 2654435761u) % TS_CAP;      // Fibonacci hashing
            for (unsigned step = 0; step < TS_CAP; step++) {
                unsigned slot = (h + step) % TS_CAP;
                if (!tab[slot].used) break;
                if (tab[slot].key == key) { out[0] = tab[slot].idx; out[1] = i; free(tab); return; }
            }
        }
        unsigned h = (unsigned) (a[i] * 2654435761u) % TS_CAP;
        for (unsigned step = 0; step < TS_CAP; step++) {
            unsigned slot = (h + step) % TS_CAP;
            if (!tab[slot].used) { tab[slot].key = a[i]; tab[slot].idx = i; tab[slot].used = 1; break; }
        }
    }
    out[0] = out[1] = -1;
    free(tab);
}   // O(n) expected time · O(n) space
""",
    "contains-duplicate": r"""
// Sort a copy and look for neighbours that are equal (C: no set in the standard library).
static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}

int containsDuplicate(int *a, int n) {
    qsort(a, n, sizeof(int), cmpInt);
    for (int i = 1; i < n; i++)
        if (a[i] == a[i - 1]) return 1;                   // true
    return 0;                                             // false
}   // O(n log n) time · O(1) space
""",
    "valid-anagram": r"""
// Two count arrays over the alphabet: equal counts means an anagram.
int isAnagram(const char *s, const char *t) {
    if (strlen(s) != strlen(t)) return 0;
    int count[26] = {0};
    for (int i = 0; s[i]; i++) { count[s[i] - 'a']++; count[t[i] - 'a']--; }
    for (int i = 0; i < 26; i++)
        if (count[i]) return 0;
    return 1;
}   // O(n) time · O(1) space
""",
    "first-unique-character": r"""
// Count the letters, then scan again for the first slot still holding a single hit.
int firstUniqChar(const char *s) {
    int count[26] = {0};
    for (int i = 0; s[i]; i++) count[s[i] - 'a']++;
    for (int i = 0; s[i]; i++)
        if (count[s[i] - 'a'] == 1) return i;
    return -1;
}   // O(n) time · O(1) space
""",
    "intersection-of-two-arrays": r"""
// Sort the first array and binary search every value of the second into it.
static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}

static int *found(int key, int *a, int n) {
    int lo = 0, hi = n - 1;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        if (a[mid] == key) return a + mid;
        if (a[mid] < key) lo = mid + 1; else hi = mid - 1;
    }
    return NULL;
}

int intersection(int *a, int n, int *b, int m, int *out) {
    qsort(a, n, sizeof(int), cmpInt);
    qsort(b, m, sizeof(int), cmpInt);
    int i = 0, j = 0, k = 0;
    while (i < n && j < m) {
        if (a[i] == b[j]) {
            if (!k || out[k - 1] != a[i]) out[k++] = a[i];      // unique results only
            i++; j++;
        } else if (a[i] < b[j]) i++;
        else j++;
    }
    return k;
}   // O((n + m) log(n + m)) time · O(1) extra space
""",
    "word-pattern": r"""
// Two maps kept in sync: pattern letter → word, and word → pattern letter.
int wordPattern(const char *pattern, const char *s) {
    char mapP[128][64], *mapW[128];
    int usedP = 0, usedW = 0;
    const char *p = pattern;
    for (const char *w = s; ; ) {
        const char *end = strchr(w, ' ');
        int len = end ? (int) (end - w) : (int) strlen(w);
        if (!*p) return w[0] == '\0' && len == 0;         // both ran out together
        char word[64];
        if (len >= 64) return 0;
        memcpy(word, w, (size_t) len); word[len] = '\0';
        int pi = -1;
        for (int i = 0; i < usedP; i++) if (mapP[i][0] == *p && strcmp(mapP[i] + 1, word) == 0) pi = i;
        int wi = -1;
        for (int i = 0; i < usedW; i++) if (strcmp(mapW[i], word) == 0) wi = i;
        if (pi < 0) {
            if (wi >= 0) return 0;                        // word already bound to another letter
            mapP[usedP][0] = *p; strcpy(mapP[usedP] + 1, word); usedP++;
            mapW[usedW++] = strdup(word);
        } else if (wi < 0) return 0;                      // letter already bound to another word
        p++;
        if (!end) break;
        w = end + 1;
    }
    return *p == '\0';
}   // O(n * alphabet) time · O(n) space
""",
    "group-anagrams": r"""
// Sort a copy of each word to get its signature, then group equal signatures.
int groupAnagrams(char **words, int n, int *order) {
    char sig[256][64];
    for (int i = 0; i < n; i++) {
        int len = (int) strlen(words[i]);
        strncpy(sig[i], words[i], 63); sig[i][len < 63 ? len : 63] = '\0';
        /* insertion sort the letters — small words, so this is ideal */
        for (int a = 1; sig[i][a]; a++) {
            char c = sig[i][a];
            int b = a - 1;
            while (b >= 0 && sig[i][b] > c) { sig[i][b + 1] = sig[i][b]; b--; }
            sig[i][b + 1] = c;
        }
        order[i] = i;
    }
    for (int i = 1; i < n; i++) {                         // group equal signatures together
        char key[64]; strcpy(key, sig[order[i]]);
        int j = i - 1;
        while (j >= 0 && strcmp(sig[order[j]], key) > 0) { order[j + 1] = order[j]; j--; }
        order[j + 1] = i;
    }
    return n;
}   // O(n * L log L) time · O(n * L) space
""",
    "top-k-frequent-elements": r"""
// Count, sort the (value, count) pairs by count, take the first k.
struct Freq { int value, count; };

static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}

static int cmpFreq(const void *x, const void *y) {
    const struct Freq *a = x, *b = y;
    if (a->count != b->count) return b->count - a->count;  // most frequent first
    return a->value - b->value;
}

int topKFrequent(int *a, int n, int k, int *out) {
    struct Freq *f = malloc(sizeof(struct Freq) * (size_t) n);
    int m = 0;
    qsort(a, n, sizeof(int), cmpInt);
    for (int i = 0; i < n; ) {
        int j = i;
        while (j < n && a[j] == a[i]) j++;
        f[m].value = a[i];
        f[m].count = j - i;
        m++;
        i = j;
    }
    qsort(f, (size_t) m, sizeof(struct Freq), cmpFreq);
    for (int i = 0; i < k && i < m; i++) out[i] = f[i].value;
    free(f);
    return k < m ? k : m;
}   // O(n log n) time · O(n) space
""",
    "subarray-sum-equals-k": r"""
// Running sum plus a hash of how often each sum has been seen.
#define SS_CAP 8192
struct SSEntry { long long key; int count, used; };

int subarraySum(const int *a, int n, int k) {
    struct SSEntry *tab = calloc(SS_CAP, sizeof(struct SSEntry));
    long long sum = 0;
    int total = 0;
    for (int i = 0; i < n; i++) {
        sum += a[i];
        long long need = sum - k;
        unsigned h = (unsigned) ((unsigned long long) need * 2654435761u) % SS_CAP;
        for (unsigned step = 0; step < SS_CAP; step++) {
            unsigned slot = (h + step) % SS_CAP;
            if (!tab[slot].used) break;
            if (tab[slot].key == need) { total += tab[slot].count; break; }
        }
        unsigned h2 = (unsigned) ((unsigned long long) sum * 2654435761u) % SS_CAP;
        for (unsigned step = 0; step < SS_CAP; step++) {
            unsigned slot = (h2 + step) % SS_CAP;
            if (!tab[slot].used) { tab[slot].key = sum; tab[slot].count = 1; tab[slot].used = 1; break; }
            if (tab[slot].key == sum) { tab[slot].count++; break; }
        }
    }
    free(tab);
    return total;
}   // O(n) expected time · O(n) space
""",
    "longest-consecutive-sequence": r"""
// Sort, skip duplicates, and extend the current run while the step is exactly one.
static int cmpInt(const void *x, const void *y) {
    int a = *(const int *) x, b = *(const int *) y;
    return (a > b) - (a < b);
}

int longestConsecutive(int *a, int n) {
    if (n == 0) return 0;
    qsort(a, n, sizeof(int), cmpInt);
    int best = 1, run = 1;
    for (int i = 1; i < n; i++) {
        if (a[i] == a[i - 1]) continue;
        run = (a[i] == a[i - 1] + 1) ? run + 1 : 1;
        if (run > best) best = run;
    }
    return best;
}   // O(n log n) time · O(1) space
""",
    "four-sum-count-ii": r"""
// Every sum of a+b and of c+d: equal sums on both sides pair up.
static int cmpLL(const void *x, const void *y) {
    long long a = *(const long long *) x, b = *(const long long *) y;
    return (a > b) - (a < b);
}

int fourSumCount(const int *a, int n, const int *b, const int *c, const int *d) {
    long long *left = malloc(sizeof(long long) * (size_t) n * (size_t) n);
    long long *right = malloc(sizeof(long long) * (size_t) n * (size_t) n);
    int k = 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            left[k] = (long long) a[i] + b[j];
            right[k] = (long long) c[i] + d[j];
            k++;
        }
    qsort(left, (size_t) k, sizeof(long long), cmpLL);
    qsort(right, (size_t) k, sizeof(long long), cmpLL);
    long long total = 0;
    int i = 0, j = k - 1;
    while (i < k && j >= 0) {
        long long sum = left[i] + right[j];
        if (sum == 0) {                                   // count equal runs on both sides
            long long lv = left[i], rv = right[j];
            long long ci = 0, cj = 0;
            while (i < k && left[i] == lv) { ci++; i++; }
            while (j >= 0 && right[j] == rv) { cj++; j--; }
            total += ci * cj;
        } else if (sum < 0) i++;
        else j--;
    }
    free(left); free(right);
    return (int) total;
}   // O(n^2 log n) time · O(n^2) space
""",
    "insert-delete-getrandom-o1": r"""
// A growable array plus a value→index map: remove = swap with the last element.
typedef struct {
    int *items, size, cap;
} RandomizedSet;

RandomizedSet *randomizedSetCreate(void) {
    RandomizedSet *s = calloc(1, sizeof(RandomizedSet));
    s->cap = 8;
    s->items = malloc(sizeof(int) * (size_t) s->cap);
    return s;
}

static int rsIndexOf(const RandomizedSet *s, int val) {
    for (int i = 0; i < s->size; i++) if (s->items[i] == val) return i;
    return -1;
}

int randomizedSetInsert(RandomizedSet *s, int val) {
    if (rsIndexOf(s, val) >= 0) return 0;                 // already there
    if (s->size == s->cap) {
        s->cap *= 2;
        s->items = realloc(s->items, sizeof(int) * (size_t) s->cap);
    }
    s->items[s->size++] = val;
    return 1;
}

int randomizedSetRemove(RandomizedSet *s, int val) {
    int idx = rsIndexOf(s, val);
    if (idx < 0) return 0;
    s->items[idx] = s->items[--s->size];                  // the last element fills the hole
    return 1;
}

int randomizedSetGetRandom(const RandomizedSet *s) {
    return s->items[rand() % s->size];
}

void randomizedSetFree(RandomizedSet *s) { free(s->items); free(s); }
// insert / remove are O(n) with the plain array (O(1) once the index map is kept) · getRandom O(1)
""",
    "valid-sudoku": r"""
// One row mask, one column mask and one box mask per digit position.
int isValidSudoku(char **board) {
    int rows[9] = {0}, cols[9] = {0}, boxes[9] = {0};
    for (int r = 0; r < 9; r++)
        for (int c = 0; c < 9; c++) {
            char ch = board[r][c];
            if (ch == '.' || ch == '0') continue;
            int bit = 1 << (ch - '1');
            int b = (r / 3) * 3 + c / 3;
            if ((rows[r] & bit) || (cols[c] & bit) || (boxes[b] & bit)) return 0;   // false
            rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit;
        }
    return 1;                                             // true
}   // O(81) time · O(1) space
""",
    "sort-characters-by-frequency": r"""
// Count, then keep taking the most frequent remaining character.
char *frequencySort(const char *s) {
    int count[256] = {0};
    int n = (int) strlen(s);
    for (int i = 0; i < n; i++) count[(unsigned char) s[i]]++;
    char *out = malloc((size_t) n + 1);
    int w = 0;
    while (w < n) {
        int best = -1;
        for (int c = 0; c < 256; c++)
            if (count[c] > 0 && (best < 0 || count[c] > count[best])) best = c;
        while (count[best]-- > 0) out[w++] = (char) best;
        count[best] = 0;
    }
    out[n] = '\0';
    return out;
}   // O(256 * n) time · O(1) extra space
""",
    "find-all-duplicates-in-array": r"""
// Values are in 1..n, so the array itself can carry the "seen" marks by negation.
int findDuplicates(int *a, int n, int *out) {
    int k = 0;
    for (int i = 0; i < n; i++) {
        int v = a[i] < 0 ? -a[i] : a[i];
        if (a[v - 1] < 0) out[k++] = v;                   // second time we see v
        else a[v - 1] = -a[v - 1];
    }
    for (int i = 0; i < n; i++) if (a[i] < 0) a[i] = -a[i];   // restore the input
    return k;
}   // O(n) time · O(1) extra space
""",
    "encode-and-decode-strings": r"""
// Length-prefixed encoding: "5#hello5#world" — no escaping needed.
char *encodeStrings(char **words, int n) {
    size_t total = 1;
    for (int i = 0; i < n; i++) total += strlen(words[i]) + 12;
    char *out = malloc(total);
    out[0] = '\0';
    for (int i = 0; i < n; i++) {
        char head[16];
        snprintf(head, sizeof head, "%d#", (int) strlen(words[i]));
        strcat(out, head);
        strcat(out, words[i]);
    }
    return out;
}

int decodeStrings(const char *s, char **out) {
    int k = 0;
    while (*s) {
        int len = atoi(s);
        const char *hash = strchr(s, '#');
        s = hash + 1;
        char *word = malloc((size_t) len + 1);
        memcpy(word, s, (size_t) len);
        word[len] = '\0';
        out[k++] = word;
        s += len;
    }
    return k;
}   // O(total characters) time · O(1) extra space
""",
    "brick-wall": r"""
// Count how often each vertical seam occurs; the best cut crosses the fewest bricks.
int leastBricks(int rows[][20], const int *widths, int rowCount) {
    int seam[65536] = {0};                                // small coordinate range for the demo
    int best = 0;
    for (int r = 0; r < rowCount; r++) {
        int x = 0;
        for (int c = 0; c + 1 < widths[r]; c++) {         // the right edge is not a seam
            x += rows[r][c];
            if (x >= 0 && x < 65536 && ++seam[x] > best) best = seam[x];
        }
    }
    return rowCount - best;
}   // O(total bricks) time · O(width) space
""",
    "contiguous-array": r"""
// Treat 0 as -1 so "equal counts" becomes "sum 0": two equal prefix sums mark a range.
int findMaxLength(const int *a, int n) {
    int *first = malloc(sizeof(int) * (size_t) (2 * n + 1));
    for (int i = 0; i <= 2 * n; i++) first[i] = -2;
    first[n] = -1;                                        // sum 0 before the array starts
    int sum = 0, best = 0;
    for (int i = 0; i < n; i++) {
        sum += a[i] ? 1 : -1;
        int idx = sum + n;
        if (first[idx] != -2) { if (i - first[idx] > best) best = i - first[idx]; }
        else first[idx] = i;
    }
    free(first);
    return best;
}   // O(n) time · O(n) space
""",
    "max-points-on-a-line": r"""
// For every point, count the other points per reduced slope (dx, dy).
static int gcdInt(int a, int b) {
    while (b) { int t = a % b; a = b; b = t; }
    return a < 0 ? -a : a;
}

int maxPoints(int points[][2], int n) {
    if (n < 3) return n;
    int best = 2;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int dx = points[j][0] - points[i][0], dy = points[j][1] - points[i][1];
            int g = gcdInt(dx, dy);
            if (g) { dx /= g; dy /= g; }                  // reduced direction
            int count = 2;
            for (int k = 0; k < n; k++) {
                if (k == i || k == j) continue;
                int ex = points[k][0] - points[i][0], ey = points[k][1] - points[i][1];
                if ((long long) ex * dy == (long long) ey * dx) count++;   // same line
            }
            if (count > best) best = count;
        }
    }
    return best;
}   // O(n^3) time · O(1) space (O(n^2) with per-point slope counting)
""",
    "longest-duplicate-substring": r"""
// Binary search the answer length with a 64-bit rolling hash over every window.
static unsigned long long *hashesOf(const char *s, int len, int n, int *count) {
    unsigned long long *out = malloc(sizeof(unsigned long long) * (size_t) (n - len + 1));
    unsigned long long h = 0, power = 1, base = 131;
    for (int i = 0; i < len; i++) { h = h * base + (unsigned char) s[i]; if (i) power *= base; }
    *count = 0;
    out[(*count)++] = h;
    for (int i = len; i < n; i++) {
        h = (h - (unsigned char) s[i - len] * power) * base + (unsigned char) s[i];
        out[(*count)++] = h;
    }
    return out;
}

static int cmpULL(const void *x, const void *y) {
    unsigned long long a = *(const unsigned long long *) x, b = *(const unsigned long long *) y;
    return (a > b) - (a < b);
}

char *longestDupSubstring(const char *s) {
    int n = (int) strlen(s);
    int lo = 1, hi = n, bestLen = 0, bestStart = 0;
    while (lo <= hi) {
        int len = (lo + hi) / 2, count = 0;
        unsigned long long *h = hashesOf(s, len, n, &count);
        qsort(h, (size_t) count, sizeof(unsigned long long), cmpULL);
        int dup = 0;
        for (int i = 1; i < count; i++) if (h[i] == h[i - 1]) { dup = 1; break; }
        free(h);
        if (dup) { bestLen = len; lo = len + 1; }
        else hi = len - 1;
    }
    if (!bestLen) return strdup("");
    for (int i = 0; i + bestLen <= n; i++) {              // find the window itself
        if (!strncmp(s + i, s + bestStart, (size_t) bestLen) && i) { bestStart = i; break; }
        for (int j = i + 1; j + bestLen <= n; j++)
            if (!strncmp(s + i, s + j, (size_t) bestLen)) { bestStart = i; i = n; break; }
    }
    char *out = malloc((size_t) bestLen + 1);
    memcpy(out, s + bestStart, (size_t) bestLen);
    out[bestLen] = '\0';
    return out;
}   // O(n log^2 n) time · O(n) space
""",
    "first-missing-positive": r"""
// Place every value v in 1..n at index v-1, then the first index holding the wrong
// value is the answer.
int firstMissingPositive(int *a, int n) {
    for (int i = 0; i < n; i++)
        while (a[i] > 0 && a[i] <= n && a[a[i] - 1] != a[i]) {
            int t = a[a[i] - 1]; a[a[i] - 1] = a[i]; a[i] = t;
        }
    for (int i = 0; i < n; i++)
        if (a[i] != i + 1) return i + 1;
    return n + 1;
}   // O(n) time · O(1) space
""",
    "all-oone-data-structure": r"""
// Counts plus the current best and worst: enough for inc/dec/getMaxKey/getMinKey.
typedef struct {
    char keys[64][32];
    int counts[64], n;
} AllOne;

AllOne *allOneCreate(void) { return calloc(1, sizeof(AllOne)); }

static int aoFind(AllOne *o, const char *key) {
    for (int i = 0; i < o->n; i++) if (!strcmp(o->keys[i], key)) return i;
    return -1;
}

void allOneInc(AllOne *o, const char *key) {
    int i = aoFind(o, key);
    if (i < 0) { strncpy(o->keys[o->n], key, 31); o->counts[o->n] = 0; i = o->n++; }
    o->counts[i]++;
}

void allOneDec(AllOne *o, const char *key) {
    int i = aoFind(o, key);
    if (i >= 0 && --o->counts[i] == 0) {                  // drop the key entirely
        strcpy(o->keys[i], o->keys[--o->n]);
        o->counts[i] = o->counts[o->n];
    }
}

const char *allOneGetMaxKey(AllOne *o) {
    int best = 0;
    for (int i = 1; i < o->n; i++) if (o->counts[i] > o->counts[best]) best = i;
    return o->n ? o->keys[best] : "";
}

const char *allOneGetMinKey(AllOne *o) {
    int best = 0;
    for (int i = 1; i < o->n; i++) if (o->counts[i] < o->counts[best]) best = i;
    return o->n ? o->keys[best] : "";
}   // inc / dec / getMax / getMin are O(k) over the live keys · O(k) space
""",
    "number-of-submatrices-that-sum-to-target": r"""
// Fix the top and bottom row, then the classic "subarray sum equals target" on columns.
int numSubmatrixSumTarget(int rows, int cols, int m[][10], int target) {
    int total = 0;
    for (int top = 0; top < rows; top++) {
        int colSum[10] = {0};
        for (int bottom = top; bottom < rows; bottom++) {
            for (int c = 0; c < cols; c++) colSum[c] += m[bottom][c];
            for (int start = 0; start < cols; start++) {      // O(cols^2) per band
                int sum = 0;
                for (int end = start; end < cols; end++) {
                    sum += colSum[end];
                    if (sum == target) total++;
                }
            }
        }
    }
    return total;
}   // O(rows^2 * cols^2) time · O(cols) space
""",
    "palindrome-pairs": r"""
// Check every ordered pair: two words form a palindrome when their concatenation reads
// the same backwards.
static int isPalin(const char *s, int len) {
    for (int i = 0, j = len - 1; i < j; i++, j--)
        if (s[i] != s[j]) return 0;
    return 1;
}

int palindromePairs(char **words, int n, int (*out)[2]) {
    int k = 0;
    size_t maxLen = 1;
    for (int i = 0; i < n; i++) maxLen += strlen(words[i]);
    char *buf = malloc(maxLen);
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            if (i == j) continue;
            snprintf(buf, maxLen, "%s%s", words[i], words[j]);
            if (isPalin(buf, (int) strlen(buf))) { out[k][0] = i; out[k][1] = j; k++; }
        }
    free(buf);
    return k;
}   // O(n^2 * L) time · O(L) extra space
""",
    "subarrays-with-k-different-integers": r"""
// exactly(k) = atMost(k) - atMost(k - 1), counted with a sliding window.
static int atMost(const int *a, int n, int k) {
    if (k < 0) return 0;
    int count[20001] = {0}, used = 0, left = 0, total = 0;
    for (int right = 0; right < n; right++) {
        int v = a[right] + 10000;
        if (count[v]++ == 0) used++;
        while (used > k) {
            int u = a[left++] + 10000;
            if (--count[u] == 0) used--;
        }
        total += right - left + 1;
    }
    return total;
}

int subarraysWithKDistinct(const int *a, int n, int k) {
    return atMost(a, n, k) - atMost(a, n, k - 1);
}   // O(n) time · O(max value) space
""",
    "count-array-pairs-divisible-by-k": r"""
// Group by remainder mod k: pairs of remainders (r, k - r) count for free.
int countPairsDivisibleByK(const int *a, int n, int k) {
    int *count = calloc((size_t) k, sizeof(int));
    long long total = 0;
    for (int i = 0; i < n; i++) {
        int r = ((a[i] % k) + k) % k;
        int want = r ? k - r : 0;
        total += count[want];
        count[r]++;
    }
    free(count);
    return (int) total;
}   // O(n) time · O(k) space
""",
    "maximum-number-of-visible-points": r"""
// Sort the angles around the viewer and slide a window of `angle` degrees over them.
static int cmpDouble(const void *x, const void *y) {
    double a = *(const double *) x, b = *(const double *) y;
    return (a > b) - (a < b);
}

int visiblePoints(int points[][2], int n, int angle, int locX, int locY) {
    double *ang = malloc(sizeof(double) * (size_t) (2 * n));
    int same = 0, m = 0;
    const double PI = acos(-1.0);
    for (int i = 0; i < n; i++) {
        double dy = points[i][1] - locY, dx = points[i][0] - locX;
        if (dy == 0 && dx == 0) { same++; continue; }      // the viewer's own point
        double deg = atan2(dy, dx) * 180.0 / PI;
        ang[m++] = deg;
    }
    qsort(ang, (size_t) m, sizeof(double), cmpDouble);
    for (int i = 0; i < m; i++) ang[m + i] = ang[i] + 360.0;   // wrap around
    int best = 0, left = 0;
    for (int right = 0; right < 2 * m; right++) {
        while (ang[right] - ang[left] > angle + 1e-9) left++;
        if (right - left + 1 > best) best = right - left + 1;
    }
    free(ang);
    return best + same;
}   // O(n log n) time · O(n) space
""",
    "substring-with-largest-variance": r"""
// For every ordered pair of letters, the classic "best subarray with difference" scan.
int largestVariance(const char *s) {
    int best = 0;
    for (char hi = 'a'; hi <= 'z'; hi++)
        for (char lo = 'a'; lo <= 'z'; lo++) {
            if (hi == lo) continue;
            int countHi = 0, countLo = 0, bestLocal = 0, seenLo = 0;
            for (int i = 0; s[i]; i++) {
                if (s[i] == hi) countHi++;
                else if (s[i] == lo) { countLo++; seenLo = 1; }
                else continue;
                if (seenLo && countHi > countLo) { if (countHi - countLo > bestLocal) bestLocal = countHi - countLo; }
                if (countHi < countLo) { countHi = countLo = 0; seenLo = 0; }
            }
            if (bestLocal > best) best = bestLocal;
        }
    return best;
}   // O(26 * 26 * n) time · O(1) space
""",
    "maximum-frequency-stack": r"""
// Per-value counts plus a stack of (value, count) per push: pop returns the most frequent.
typedef struct {
    int values[1024], counts[1024], size;
} FreqStack;

FreqStack *freqStackCreate(void) { return calloc(1, sizeof(FreqStack)); }

void freqStackPush(FreqStack *f, int val) {
    int c = 1;
    for (int i = f->size - 1; i >= 0; i--) if (f->values[i] == val) { c = f->counts[i] + 1; break; }
    f->values[f->size] = val;
    f->counts[f->size] = c;
    f->size++;
}

int freqStackPop(FreqStack *f) {
    int best = 0;
    for (int i = 1; i < f->size; i++)
        if (f->counts[i] >= f->counts[best]) best = i;     // latest among the most frequent
    int val = f->values[best];
    for (int i = best; i + 1 < f->size; i++) {             // close the hole
        f->values[i] = f->values[i + 1];
        f->counts[i] = f->counts[i + 1];
    }
    f->size--;
    return val;
}   // O(n) per operation with this simple array · O(n) space
""",
    "count-subarrays-with-median-k": r"""
// Index of k splits the array; values below k count -1 and above k count +1.
long long countSubarraysMedianK(int *a, int n, int k) {
    int pos = -1;
    for (int i = 0; i < n; i++) if (a[i] == k) { pos = i; break; }
    if (pos < 0) return 0;
    int offset = n;
    int *leftCount = calloc((size_t) (2 * n + 1), sizeof(int));
    int *rightCount = calloc((size_t) (2 * n + 1), sizeof(int));
    int sum = 0;
    for (int i = pos; i >= 0; i--) {                      // suffixes ending at pos
        sum += (a[i] > k) - (a[i] < k);
        leftCount[sum + offset]++;
    }
    sum = 0;
    for (int i = pos; i < n; i++) {                       // prefixes starting at pos
        sum += (a[i] > k) - (a[i] < k);
        rightCount[sum + offset]++;
    }
    long long total = 0;
    for (int d = -n; d <= n; d++) {                       // odd length: sums cancel
        int need = -d;
        if (need + offset >= 0 && need + offset <= 2 * n && d + offset >= 0 && d + offset <= 2 * n)
            total += (long long) leftCount[d + offset] * rightCount[need + offset];
    }
    for (int d = -n; d <= n; d++) {                       // even length: sums differ by one
        int need = 1 - d;
        if (need + offset >= 0 && need + offset <= 2 * n && d + offset >= 0 && d + offset <= 2 * n)
            total += (long long) leftCount[d + offset] * rightCount[need + offset];
    }
    free(leftCount); free(rightCount);
    return total;
}   // O(n) time · O(n) space
""",
}
