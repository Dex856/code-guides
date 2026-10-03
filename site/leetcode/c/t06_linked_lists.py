# Topic 6 · Linked Lists — C17 solutions
#
# In C a list node is a struct you own:
#     struct ListNode { int val; struct ListNode *next; };
# The judge supplies that definition, so the solutions below only write the functions.

CODE = {
    "reverse-linked-list": r"""
// Three pointers: prev, cur, next — rewire each node as you pass it.
struct ListNode *reverseList(struct ListNode *head) {
    struct ListNode *prev = NULL;
    while (head) {
        struct ListNode *next = head->next;
        head->next = prev;                                // flip the arrow
        prev = head;
        head = next;
    }
    return prev;
}   // O(n) time · O(1) space
""",
    "merge-two-sorted-lists": r"""
// A dummy head removes the "which list starts the result" special case.
struct ListNode *mergeTwoLists(struct ListNode *a, struct ListNode *b) {
    struct ListNode dummy = {0, NULL}, *tail = &dummy;
    while (a && b) {
        if (a->val <= b->val) { tail->next = a; a = a->next; }
        else { tail->next = b; b = b->next; }
        tail = tail->next;
    }
    tail->next = a ? a : b;                               // whatever is left is already sorted
    return dummy.next;
}   // O(n + m) time · O(1) space
""",
    "remove-duplicates-from-sorted-list": r"""
// Sorted, so equal values are neighbours: skip the duplicates.
struct ListNode *deleteDuplicates(struct ListNode *head) {
    struct ListNode *cur = head;
    while (cur && cur->next) {
        if (cur->val == cur->next->val) cur->next = cur->next->next;   // drop the twin
        else cur = cur->next;
    }
    return head;
}   // O(n) time · O(1) space
""",
    "middle-of-the-linked-list": r"""
// Slow and fast pointers: when fast reaches the end, slow is at the middle.
struct ListNode *middleNode(struct ListNode *head) {
    struct ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow;
}   // O(n) time · O(1) space
""",
    "linked-list-cycle": r"""
// Floyd's tortoise and hare: if there is a cycle, the two pointers must meet.
int hasCycle(struct ListNode *head) {
    struct ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return 1;                       // true
    }
    return 0;                                             // false
}   // O(n) time · O(1) space
""",
    "palindrome-linked-list": r"""
// Find the middle, reverse the second half, then compare the two halves.
struct ListNode *reverseAll(struct ListNode *head) {
    struct ListNode *prev = NULL;
    while (head) { struct ListNode *next = head->next; head->next = prev; prev = head; head = next; }
    return prev;
}

int isPalindrome(struct ListNode *head) {
    struct ListNode *slow = head, *fast = head;
    while (fast && fast->next) { slow = slow->next; fast = fast->next->next; }
    struct ListNode *right = reverseAll(slow);
    struct ListNode *left = head;
    while (right) {                                       // compare up to the middle
        if (left->val != right->val) return 0;
        left = left->next;
        right = right->next;
    }
    return 1;
}   // O(n) time · O(1) space
""",
    "remove-nth-node-from-end-of-list": r"""
// A gap of n between two pointers puts the second exactly before the node to drop.
struct ListNode *removeNthFromEnd(struct ListNode *head, int n) {
    struct ListNode dummy = {0, head}, *first = &dummy, *second = &dummy;
    for (int i = 0; i <= n; i++) first = first->next;     // n + 1 steps ahead
    while (first) { first = first->next; second = second->next; }
    second->next = second->next->next;
    return dummy.next;
}   // O(n) time · O(1) space
""",
    "intersection-of-two-linked-lists": r"""
// Walk both lists; when one ends, continue on the other. They meet at the crossing.
struct ListNode *getIntersectionNode(struct ListNode *a, struct ListNode *b) {
    struct ListNode *pa = a, *pb = b;
    while (pa != pb) {
        pa = pa ? pa->next : b;                           // switch lists on reaching the end
        pb = pb ? pb->next : a;
    }
    return pa;                                            // NULL when there is no crossing
}   // O(n + m) time · O(1) space
""",
    "add-two-numbers": r"""
// Walk both numbers least-significant digit first, carrying as you go.
struct ListNode *addTwoNumbers(struct ListNode *a, struct ListNode *b) {
    struct ListNode dummy = {0, NULL}, *tail = &dummy;
    int carry = 0;
    while (a || b || carry) {
        int sum = carry + (a ? a->val : 0) + (b ? b->val : 0);
        carry = sum / 10;
        struct ListNode *node = malloc(sizeof(struct ListNode));
        node->val = sum % 10;
        node->next = NULL;
        tail->next = node;
        tail = node;
        if (a) a = a->next;
        if (b) b = b->next;
    }
    return dummy.next;
}   // O(max(n, m)) time · O(1) extra space
""",
    "odd-even-linked-list": r"""
// Two chains — odd positions and even positions — joined at the end.
struct ListNode *oddEvenList(struct ListNode *head) {
    if (!head || !head->next) return head;
    struct ListNode *odd = head, *even = head->next, *evenHead = even;
    while (even && even->next) {
        odd->next = even->next;                           // skip over the even node
        odd = odd->next;
        even->next = odd->next;
        even = even->next;
    }
    odd->next = evenHead;                                 // the even chain goes last
    return head;
}   // O(n) time · O(1) space
""",
    "reorder-list": r"""
// Three steps: find the middle, reverse the second half, then interleave.
struct ListNode *revList(struct ListNode *head) {
    struct ListNode *prev = NULL;
    while (head) { struct ListNode *next = head->next; head->next = prev; prev = head; head = next; }
    return prev;
}

void reorderList(struct ListNode *head) {
    if (!head || !head->next) return;
    struct ListNode *slow = head, *fast = head;
    while (fast->next && fast->next->next) { slow = slow->next; fast = fast->next->next; }
    struct ListNode *second = revList(slow->next);
    slow->next = NULL;
    struct ListNode *first = head;
    while (second) {                                      // interleave first and second
        struct ListNode *n1 = first->next, *n2 = second->next;
        first->next = second;
        second->next = n1;
        first = n1;
        second = n2;
    }
}   // O(n) time · O(1) space
""",
    "rotate-list": r"""
// Close the list into a ring, then cut it k steps before the end.
struct ListNode *rotateRight(struct ListNode *head, int k) {
    if (!head || !head->next) return head;
    int n = 1;
    struct ListNode *tail = head;
    while (tail->next) { tail = tail->next; n++; }
    k %= n;
    if (k == 0) return head;
    tail->next = head;                                    // make it a ring
    struct ListNode *newTail = head;
    for (int i = 0; i < n - k - 1; i++) newTail = newTail->next;
    struct ListNode *newHead = newTail->next;
    newTail->next = NULL;                                 // break the ring at the right place
    return newHead;
}   // O(n) time · O(1) space
""",
    "swap-nodes-in-pairs": r"""
// A dummy head plus three pointers: swap each pair, then advance by two.
struct ListNode *swapPairs(struct ListNode *head) {
    struct ListNode dummy = {0, head}, *prev = &dummy;
    while (prev->next && prev->next->next) {
        struct ListNode *first = prev->next, *second = first->next;
        first->next = second->next;
        second->next = first;
        prev->next = second;
        prev = first;                                     // the pair's tail
    }
    return dummy.next;
}   // O(n) time · O(1) space
""",
    "partition-list": r"""
// Two chains: values below x and values at least x, joined at the end.
struct ListNode *partition(struct ListNode *head, int x) {
    struct ListNode less = {0, NULL}, ge = {0, NULL};
    struct ListNode *lessTail = &less, *geTail = &ge;
    for (; head; head = head->next) {
        if (head->val < x) { lessTail->next = head; lessTail = head; }
        else { geTail->next = head; geTail = head; }
    }
    geTail->next = NULL;                                  // terminate the second chain
    lessTail->next = ge.next;
    return less.next;
}   // O(n) time · O(1) space
""",
    "copy-list-with-random-pointer": r"""
// A random pointer makes a deep copy: the copy is kept beside each original, then split.
struct Node { int val; struct Node *next, *random; };

struct Node *copyRandomList(struct Node *head) {
    if (!head) return NULL;
    for (struct Node *cur = head; cur; cur = cur->next->next) {      // interleave the copies
        struct Node *copy = malloc(sizeof(struct Node));
        copy->val = cur->val;
        copy->next = cur->next;
        copy->random = NULL;
        cur->next = copy;
    }
    for (struct Node *cur = head; cur; cur = cur->next->next)        // fix the random pointers
        if (cur->random) cur->next->random = cur->random->next;
    struct Node *copyHead = head->next;
    for (struct Node *cur = head; cur; ) {                           // split the two lists
        struct Node *copy = cur->next;
        cur->next = copy->next;
        copy->next = copy->next ? copy->next->next : NULL;
        cur = cur->next;
    }
    return copyHead;
}   // O(n) time · O(1) extra space
""",
    "flatten-multilevel-doubly-linked-list": r"""
// Depth-first with an explicit stack of the nodes to resume after a child list.
struct Node { int val; struct Node *prev, *next, *child; };

struct Node *flatten(struct Node *head) {
    if (!head) return NULL;
    struct Node *stack[4096];
    int top = 0, first = 1;
    for (struct Node *cur = head; cur; cur = cur->next) {
        if (cur->child) {
            if (cur->next) stack[top++] = cur->next;      // come back to the rest later
            cur->next = cur->child;
            cur->child->prev = cur;
            cur->child = NULL;
        }
        if (!cur->next && top) {                          // splice the saved tail back in
            cur->next = stack[--top];
            cur->next->prev = cur;
        }
        (void) first;
    }
    return head;
}   // O(n) time · O(d) space
""",
    "linked-list-cycle-ii": r"""
// After the pointers meet, a walker from the head meets the cycle start.
struct ListNode *detectCycle(struct ListNode *head) {
    struct ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            struct ListNode *fromHead = head;
            while (fromHead != slow) { fromHead = fromHead->next; slow = slow->next; }
            return slow;                                  // the first node of the cycle
        }
    }
    return NULL;
}   // O(n) time · O(1) space
""",
    "split-linked-list-in-parts": r"""
// Walk once to count, then cut parts of size n / k (plus one for the first remainder).
struct ListNode **splitListToParts(struct ListNode *head, int k, int *returnSize) {
    int n = 0;
    for (struct ListNode *cur = head; cur; cur = cur->next) n++;
    int width = n / k, extra = n % k;
    struct ListNode **parts = malloc(sizeof(struct ListNode *) * (size_t) k);
    struct ListNode *cur = head;
    for (int i = 0; i < k; i++) {
        parts[i] = cur;
        int take = width + (i < extra ? 1 : 0);           // the first `extra` parts are longer
        for (int j = 0; j < take - 1 && cur; j++) cur = cur->next;
        if (cur) { struct ListNode *next = cur->next; cur->next = NULL; cur = next; }
    }
    *returnSize = k;
    return parts;
}   // O(n) time · O(k) space
""",
    "merge-k-sorted-lists": r"""
// Take the smallest head with a simple scan — a heap makes it O(n log k).
struct ListNode *mergeKLists(struct ListNode **lists, int k) {
    struct ListNode dummy = {0, NULL}, *tail = &dummy;
    while (1) {
        int best = -1;
        for (int i = 0; i < k; i++)
            if (lists[i] && (best < 0 || lists[i]->val < lists[best]->val)) best = i;
        if (best < 0) break;                              // every list is empty
        tail->next = lists[best];
        tail = lists[best];
        lists[best] = lists[best]->next;
    }
    tail->next = NULL;
    return dummy.next;
}   // O(N * k) time · O(1) space
""",
    "reverse-nodes-in-k-group": r"""
// Check that k nodes remain, reverse that group, then continue after it.
struct ListNode *reverseKGroup(struct ListNode *head, int k) {
    struct ListNode dummy = {0, head}, *groupPrev = &dummy;
    while (1) {
        struct ListNode *kth = groupPrev;
        for (int i = 0; i < k && kth; i++) kth = kth->next;
        if (!kth) break;                                  // fewer than k nodes left
        struct ListNode *groupNext = kth->next, *prev = groupNext, *cur = groupPrev->next;
        while (cur != groupNext) {                        // reverse the group in place
            struct ListNode *next = cur->next;
            cur->next = prev;
            prev = cur;
            cur = next;
        }
        struct ListNode *newTail = groupPrev->next;
        groupPrev->next = kth;                            // the group's new head
        groupPrev = newTail;                              // and its tail for the next round
    }
    return dummy.next;
}   // O(n) time · O(1) space
""",
    "lru-cache": r"""
// A hash-free LRU for clarity: an array of keys in recency order.
typedef struct {
    int capacity, size;
    int *keys, *values;
} LRUCache;

LRUCache *lRUCacheCreate(int capacity) {
    LRUCache *c = calloc(1, sizeof(LRUCache));
    c->capacity = capacity;
    c->keys = calloc((size_t) capacity, sizeof(int));
    c->values = calloc((size_t) capacity, sizeof(int));
    return c;
}

static int lruFind(LRUCache *c, int key) {
    for (int i = 0; i < c->size; i++) if (c->keys[i] == key) return i;
    return -1;
}

static void lruTouch(LRUCache *c, int idx) {              // move to the front (most recent)
    int key = c->keys[idx], value = c->values[idx];
    for (int i = idx; i > 0; i--) { c->keys[i] = c->keys[i - 1]; c->values[i] = c->values[i - 1]; }
    c->keys[0] = key;
    c->values[0] = value;
}

int lRUCacheGet(LRUCache *c, int key) {
    int idx = lruFind(c, key);
    if (idx < 0) return -1;
    int value = c->values[idx];
    lruTouch(c, idx);
    return value;
}

void lRUCachePut(LRUCache *c, int key, int value) {
    int idx = lruFind(c, key);
    if (idx >= 0) { c->values[idx] = value; lruTouch(c, idx); return; }
    if (c->size == c->capacity) c->size--;                // evict the least recent entry
    for (int i = c->size; i > 0; i--) { c->keys[i] = c->keys[i - 1]; c->values[i] = c->values[i - 1]; }
    c->keys[0] = key;
    c->values[0] = value;
    c->size++;
}   // O(capacity) per operation here · O(capacity) space (a hash map + list give O(1))
""",
    "lfu-cache": r"""
// Count the uses of each key and evict the least used, oldest first on ties.
typedef struct {
    int capacity, size;
    int *keys, *values, *freq, *age;
    int clock;
} LFUCache;

LFUCache *lFUCacheCreate(int capacity) {
    LFUCache *c = calloc(1, sizeof(LFUCache));
    c->capacity = capacity;
    c->keys = calloc((size_t) capacity, sizeof(int));
    c->values = calloc((size_t) capacity, sizeof(int));
    c->freq = calloc((size_t) capacity, sizeof(int));
    c->age = calloc((size_t) capacity, sizeof(int));
    return c;
}

static int lfuFind(LFUCache *c, int key) {
    for (int i = 0; i < c->size; i++) if (c->keys[i] == key) return i;
    return -1;
}

int lFUCacheGet(LFUCache *c, int key) {
    int idx = lfuFind(c, key);
    if (idx < 0) return -1;
    c->freq[idx]++;
    c->age[idx] = ++c->clock;
    return c->values[idx];
}

void lFUCachePut(LFUCache *c, int key, int value) {
    int idx = lfuFind(c, key);
    if (idx >= 0) { c->values[idx] = value; c->freq[idx]++; c->age[idx] = ++c->clock; return; }
    if (c->capacity == 0) return;
    if (c->size == c->capacity) {                         // find the least used, oldest
        int victim = 0;
        for (int i = 1; i < c->size; i++)
            if (c->freq[i] < c->freq[victim] ||
                (c->freq[i] == c->freq[victim] && c->age[i] < c->age[victim])) victim = i;
        c->keys[victim] = key;
        c->values[victim] = value;
        c->freq[victim] = 1;
        c->age[victim] = ++c->clock;
        return;
    }
    c->keys[c->size] = key;
    c->values[c->size] = value;
    c->freq[c->size] = 1;
    c->age[c->size] = ++c->clock;
    c->size++;
}   // O(capacity) per operation here · O(capacity) space
""",
    "sort-list": r"""
// Bottom-up merge sort: merge runs of length 1, 2, 4, … so no recursion is needed.
static struct ListNode *mergeRuns(struct ListNode *a, struct ListNode *b) {
    struct ListNode dummy = {0, NULL}, *tail = &dummy;
    while (a && b) {
        if (a->val <= b->val) { tail->next = a; a = a->next; }
        else { tail->next = b; b = b->next; }
        tail = tail->next;
    }
    tail->next = a ? a : b;
    return dummy.next;
}

struct ListNode *sortList(struct ListNode *head) {
    int n = 0;
    for (struct ListNode *c = head; c; c = c->next) n++;
    struct ListNode dummy = {0, head};
    for (int width = 1; width < n; width *= 2) {
        struct ListNode *cur = dummy.next, *tail = &dummy;
        while (cur) {
            struct ListNode *left = cur, *right = cur;
            for (int i = 0; i < width && right; i++) right = right->next;   // split the run
            int lc = 0, rc = 0;
            for (struct ListNode *p = left; p != right && lc < width; p = p->next) lc++;
            for (struct ListNode *p = right; p && rc < width; p = p->next) rc++;
            struct ListNode *rest = right;
            for (int i = 0; i < rc && rest; i++) rest = rest->next;
            struct ListNode *next = rest;
            struct ListNode *leftTail = left;
            for (int i = 0; i < lc - 1 && leftTail; i++) leftTail = leftTail->next;
            if (leftTail) leftTail->next = NULL;          // terminate the left run
            struct ListNode *rightTail = right;
            for (int i = 0; i < rc - 1 && rightTail; i++) rightTail = rightTail->next;
            if (rightTail) rightTail->next = NULL;        // terminate the right run
            tail->next = mergeRuns(left, right);
            while (tail->next) tail = tail->next;
            cur = next;
        }
    }
    return dummy.next;
}   // O(n log n) time · O(1) space
""",
    "design-skiplist": r"""
// A probabilistic skiplist: each new node is promoted with probability 1/2.
#define SKIP_MAX 32
typedef struct SkipNode {
    int val;
    struct SkipNode *forward[SKIP_MAX];
} SkipNode;

typedef struct {
    SkipNode *head;
    int level;
} Skiplist;

static SkipNode *skipNew(int val, int level) {
    SkipNode *n = calloc(1, sizeof(SkipNode));
    n->val = val;
    (void) level;
    return n;
}

Skiplist *skiplistCreate(void) {
    Skiplist *s = calloc(1, sizeof(Skiplist));
    s->head = skipNew(-1, SKIP_MAX);
    s->level = 1;
    return s;
}

int skiplistSearch(Skiplist *s, int target) {
    SkipNode *cur = s->head;
    for (int i = s->level - 1; i >= 0; i--)
        while (cur->forward[i] && cur->forward[i]->val < target) cur = cur->forward[i];
    cur = cur->forward[0];
    return cur && cur->val == target;
}

void skiplistAdd(Skiplist *s, int num) {
    SkipNode *update[SKIP_MAX];
    SkipNode *cur = s->head;
    for (int i = s->level - 1; i >= 0; i--) {
        while (cur->forward[i] && cur->forward[i]->val < num) cur = cur->forward[i];
        update[i] = cur;
    }
    int level = 1;
    while (level < SKIP_MAX && (rand() & 1)) level++;     // coin flips decide the height
    if (level > s->level) {
        for (int i = s->level; i < level; i++) update[i] = s->head;
        s->level = level;
    }
    SkipNode *node = skipNew(num, level);
    for (int i = 0; i < level; i++) {
        node->forward[i] = update[i]->forward[i];         // splice it into every level
        update[i]->forward[i] = node;
    }
}

int skiplistErase(Skiplist *s, int num) {
    SkipNode *update[SKIP_MAX];
    SkipNode *cur = s->head;
    for (int i = s->level - 1; i >= 0; i--) {
        while (cur->forward[i] && cur->forward[i]->val < num) cur = cur->forward[i];
        update[i] = cur;
    }
    cur = cur->forward[0];
    if (!cur || cur->val != num) return 0;
    for (int i = 0; i < s->level; i++) {
        if (update[i]->forward[i] != cur) break;          // not linked at this level
        update[i]->forward[i] = cur->forward[i];
    }
    free(cur);
    while (s->level > 1 && !s->head->forward[s->level - 1]) s->level--;
    return 1;
}   // O(log n) expected time per operation · O(n) space
""",
    "reverse-nodes-in-even-length-groups": r"""
// Count each group, reverse the ones of even length, leave the rest alone.
struct ListNode *reverseEvenLengthGroups(struct ListNode *head) {
    struct ListNode dummy = {0, head}, *groupPrev = &dummy;
    int group = 1;
    while (groupPrev->next) {
        struct ListNode *kth = groupPrev, *cur = groupPrev->next;
        int count = 0;
        while (count < group && kth->next) { kth = kth->next; count++; }
        if (count % 2 == 0) {                             // even group: reverse it
            struct ListNode *groupNext = kth->next, *prev = groupNext;
            while (cur != groupNext) {
                struct ListNode *next = cur->next;
                cur->next = prev;
                prev = cur;
                cur = next;
            }
            struct ListNode *newTail = groupPrev->next;
            groupPrev->next = kth;
            groupPrev = newTail;
        } else {
            groupPrev = kth;                              // odd group: leave the nodes in place
        }
        group++;
    }
    return dummy.next;
}   // O(n) time · O(1) space
""",
    "design-a-text-editor": r"""
// A gap buffer: the text before the cursor plus the text after it.
typedef struct {
    char before[4096], after[4096];
    int nBefore, nAfter;
} TextEditor;

TextEditor *textEditorCreate(void) { return calloc(1, sizeof(TextEditor)); }

void textEditorAddText(TextEditor *e, const char *text) {
    for (int i = 0; text[i]; i++) e->before[e->nBefore++] = text[i];
}

int textEditorDeleteText(TextEditor *e, int k) {
    int removed = k < e->nBefore ? k : e->nBefore;        // never delete past the start
    e->nBefore -= removed;
    return removed;
}

char *textEditorCursorLeft(TextEditor *e, int k) {
    int moved = k < e->nBefore ? k : e->nBefore;
    for (int i = 0; i < moved; i++) e->after[e->nAfter++] = e->before[--e->nBefore];
    return e->before;                                     // the text left of the cursor
}

char *textEditorCursorRight(TextEditor *e, int k) {
    int moved = k < e->nAfter ? k : e->nAfter;
    for (int i = 0; i < moved; i++) e->before[e->nBefore++] = e->after[--e->nAfter];
    return e->before;
}   // each operation is O(k) · O(n) space
""",
    "flatten-multilevel-linked-list-o1": r"""
// Same flattening, but using the child pointer itself as the stack.
struct Node { int val; struct Node *prev, *next, *child; };

struct Node *flattenO1(struct Node *head) {
    for (struct Node *cur = head; cur; cur = cur->next) {
        if (!cur->child) continue;
        struct Node *child = cur->child, *childTail = child;
        while (childTail->next) childTail = childTail->next;
        childTail->next = cur->next;                      // splice the rest onto the child's tail
        if (cur->next) cur->next->prev = childTail;
        cur->next = child;
        child->prev = cur;
        cur->child = NULL;
    }
    return head;
}   // O(n) time · O(1) space
""",
    "copy-list-with-random-pointer-o1": r"""
// Interleave copies with the originals, then split — no hash map needed.
struct Node { int val; struct Node *next, *random; };

struct Node *copyRandomO1(struct Node *head) {
    if (!head) return NULL;
    for (struct Node *cur = head; cur; cur = cur->next->next) {
        struct Node *copy = malloc(sizeof(struct Node));
        copy->val = cur->val;
        copy->next = cur->next;
        cur->next = copy;
    }
    for (struct Node *cur = head; cur; cur = cur->next->next)
        cur->next->random = cur->random ? cur->random->next : NULL;
    struct Node *copyHead = head->next;
    for (struct Node *cur = head; cur; ) {
        struct Node *copy = cur->next;
        cur->next = copy->next;
        copy->next = copy->next ? copy->next->next : NULL;
        cur = cur->next;
    }
    return copyHead;
}   // O(n) time · O(1) extra space
""",
    "reverse-linked-list-ii": r"""
// Move to position left, then reverse the section by inserting each node at its head.
struct ListNode *reverseBetween(struct ListNode *head, int left, int right) {
    struct ListNode dummy = {0, head}, *prev = &dummy;
    for (int i = 1; i < left; i++) prev = prev->next;     // node just before the section
    struct ListNode *cur = prev->next;
    for (int i = 0; i < right - left; i++) {
        struct ListNode *next = cur->next;
        cur->next = next->next;                           // cut `next` out
        next->next = prev->next;                          // and put it at the section's front
        prev->next = next;
    }
    return dummy.next;
}   // O(n) time · O(1) space
""",
    "next-greater-node-in-linked-list": r"""
// Copy the values into an array, then the usual monotonic stack runs over it.
int *nextLargerNodes(struct ListNode *head, int *returnSize) {
    int n = 0;
    for (struct ListNode *c = head; c; c = c->next) n++;
    int *values = malloc(sizeof(int) * (size_t) n);
    int i = 0;
    for (struct ListNode *c = head; c; c = c->next) values[i++] = c->val;
    int *res = calloc((size_t) n, sizeof(int));
    int *stack = malloc(sizeof(int) * (size_t) n);
    int top = 0;
    for (int k = 0; k < n; k++) {
        while (top && values[k] > values[stack[top - 1]]) res[stack[--top]] = values[k];
        stack[top++] = k;
    }
    free(values); free(stack);
    *returnSize = n;
    return res;
}   // O(n) time · O(n) space
""",
}
