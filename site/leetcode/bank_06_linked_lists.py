# Topic 6 · Linked Lists
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.

TOPIC = {
    "name": "Linked Lists",
    "tagline": "Pointer surgery: dummy heads, fast/slow runners, in-place reversal — the three moves that solve almost every list question.",
    "focus": "Handling pointers without losing nodes: a dummy head removes every 'is this the first node?' special case, a slow/fast pair finds middles "
             "and cycles, and local reversal is the building block for reordering, palindromes and k-group problems. The hard end adds design "
             "questions (LRU/LFU/text editor) where a hash map and a doubly linked list must be kept in sync.",
    "ordering": "easy 1–6 are reversal, merging, duplicate removal and the two-pointer basics; medium 1–4 are dummy-head surgery, 5–8 are "
                "reordering by combining reversal with splitting, 9–12 are copies, cycles and multi-list splitting; hard 1–4 are k-way merging "
                "and k-group reversal, 5–8 are cache/editor designs, 9–12 are the O(1)-space variants of the medium problems.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "reverse-linked-list",
        "title": "Reverse a Linked List",
        "difficulty": "Easy",
        "pattern": "three pointers, walked forward",
        "statement": "Reverse a singly linked list and return the new head.",
        "examples": [("head = 1 -> 2 -> 3 -> 4 -> 5", "5 -> 4 -> 3 -> 2 -> 1"), ("head = []", "[]")],
        "constraints": ["0 <= number of nodes <= 5000", "-5000 <= node values <= 5000", "the reversal must be in place"],
        "approach": "Walk the list carrying `prev` behind the current node and `next` ahead of it. Save the next node *before* overwriting the "
                     "link, then flip the pointer, then advance both. Saving `next` first is the whole trick — without it the rest of the list "
                     "is lost.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// prev, cur, next: save next before flipping the link
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
ListNode* reverseList(ListNode* head) {
    ListNode* prev = nullptr;
    while (head) {
        ListNode* nxt = head->next;              // save before overwriting
        head->next = prev;                       // flip the link
        prev = head;
        head = nxt;
    }
    return prev;                                 // new head
}   // O(n) time · O(1) space""",
            "java": r"""// prev, cur, next: save next before flipping the link
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode reverseList(ListNode head) {
    ListNode prev = null;
    while (head != null) {
        ListNode nxt = head.next;                // save before overwriting
        head.next = prev;                        // flip the link
        prev = head;
        head = nxt;
    }
    return prev;                                 // new head
}   // O(n) time · O(1) space""",
            "python": r"""def reverse_list(head):
    prev = None
    while head:
        nxt = head.next      # save before overwriting
        head.next = prev     # flip the link
        prev = head
        head = nxt
    return prev              # new head""",
        },
    },
    {
        "slug": "merge-two-sorted-lists",
        "title": "Merge Two Sorted Lists",
        "difficulty": "Easy",
        "pattern": "dummy head + tail",
        "statement": "Merge two sorted linked lists into one sorted list by splicing the existing nodes, and return its head.",
        "examples": [("l1 = 1 -> 2 -> 4, l2 = 1 -> 3 -> 4", "1 -> 1 -> 2 -> 3 -> 4 -> 4"), ("l1 = [], l2 = []", "[]")],
        "constraints": ["0 <= nodes per list <= 50", "-100 <= node values <= 100", "both inputs are sorted ascending"],
        "approach": "A dummy head plus a moving tail removes the 'what if the result is still empty?' branch entirely: always append to "
                     "tail.next and advance the tail. When one list runs out, splice the remainder in one step instead of copying node by node.",
        "complexity": ("O(n + m)", "O(1)"),
        "code": {
            "cpp": r"""// Dummy head: no special case for the first node
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
ListNode* mergeTwoLists(ListNode* a, ListNode* b) {
    ListNode dummy(0), *tail = &dummy;           // tail always points at the last node
    while (a && b) {
        if (a->val <= b->val) { tail->next = a; a = a->next; }
        else { tail->next = b; b = b->next; }
        tail = tail->next;
    }
    tail->next = a ? a : b;                      // splice the leftover run
    return dummy.next;
}   // O(n + m) time · O(1) space""",
            "java": r"""// Dummy head: no special case for the first node
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode mergeTwoLists(ListNode a, ListNode b) {
    ListNode dummy = new ListNode(0), tail = dummy;   // tail = last node
    while (a != null && b != null) {
        if (a.val <= b.val) { tail.next = a; a = a.next; }
        else { tail.next = b; b = b.next; }
        tail = tail.next;
    }
    tail.next = (a != null) ? a : b;             // splice the leftover run
    return dummy.next;
}   // O(n + m) time · O(1) space""",
            "python": r"""def merge_two_lists(a, b):
    dummy = tail = ListNode(0)     # dummy removes all first-node cases
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b             # splice the leftover run in one step
    return dummy.next""",
        },
    },
    {
        "slug": "remove-duplicates-from-sorted-list",
        "title": "Remove Duplicates From a Sorted List",
        "difficulty": "Easy",
        "pattern": "skip equal neighbours",
        "statement": "Delete the duplicates so each value appears once, keeping the sorted order, and return the head.",
        "examples": [("head = 1 -> 1 -> 2", "1 -> 2"), ("head = 1 -> 1 -> 2 -> 3 -> 3", "1 -> 2 -> 3")],
        "constraints": ["0 <= number of nodes <= 300", "-100 <= node values <= 100", "the list is sorted ascending"],
        "approach": "Because the list is sorted, duplicates are always adjacent. Compare the current node with its successor and, on equality, "
                     "unlink the successor; otherwise advance. Only one pointer is needed and no node is ever revisited.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Sorted input: duplicates are adjacent, so skip them in place
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
ListNode* deleteDuplicates(ListNode* head) {
    for (ListNode* cur = head; cur && cur->next; ) {
        if (cur->val == cur->next->val) cur->next = cur->next->next;   // unlink
        else cur = cur->next;
    }
    return head;
}   // O(n) time · O(1) space""",
            "java": r"""// Sorted input: duplicates are adjacent, so skip them in place
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode deleteDuplicates(ListNode head) {
    ListNode cur = head;
    while (cur != null && cur.next != null) {
        if (cur.val == cur.next.val) cur.next = cur.next.next;   // unlink
        else cur = cur.next;
    }
    return head;
}   // O(n) time · O(1) space""",
            "python": r"""def delete_duplicates(head):
    cur = head
    while cur and cur.next:
        if cur.val == cur.next.val:
            cur.next = cur.next.next     # unlink the duplicate
        else:
            cur = cur.next
    return head""",
        },
    },
    {
        "slug": "middle-of-the-linked-list",
        "title": "Middle of the Linked List",
        "difficulty": "Easy",
        "pattern": "slow and fast pointers",
        "statement": "Return the middle node; if there are two middles, return the second one.",
        "examples": [("head = 1 -> 2 -> 3 -> 4 -> 5", "3 (the node itself)"), ("head = 1 -> 2 -> 3 -> 4", "3")],
        "constraints": ["1 <= number of nodes <= 100", "the list is singly linked", "the returned node must be the actual middle node"],
        "approach": "Advance one pointer by one node and another by two. When the fast pointer falls off the end, the slow one is exactly at the "
                     "middle — no length pass, no array. Starting both at the head is what makes the *second* middle win for even lengths, which "
                     "is the version reorder-list and palindrome checks need.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Fast moves twice as far, so slow lands on the middle
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
ListNode* middleNode(ListNode* head) {
    ListNode* slow = head; ListNode* fast = head;
    while (fast && fast->next) {                 // second middle wins for even n
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow;
}   // O(n) time · O(1) space""",
            "java": r"""// Fast moves twice as far, so slow lands on the middle
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode middleNode(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {  // second middle wins for even n
        slow = slow.next;
        fast = fast.next.next;
    }
    return slow;
}   // O(n) time · O(1) space""",
            "python": r"""def middle_node(head):
    slow = fast = head
    while fast and fast.next:      # fast runs out first
        slow = slow.next
        fast = fast.next.next
    return slow                    # for even n this is the second middle""",
        },
    },
    {
        "slug": "linked-list-cycle",
        "title": "Linked List Cycle",
        "difficulty": "Easy",
        "pattern": "Floyd's tortoise and hare",
        "statement": "Return true if the list contains a cycle, following the next pointers only, using O(1) extra memory.",
        "examples": [("3 -> 2 -> 0 -> -4 with the last node pointing back to node 2", "true"), ("1 -> 2 with no cycle", "false")],
        "constraints": ["0 <= number of nodes <= 10^4", "the list may be empty or have a cycle", "extra memory must be O(1)"],
        "approach": "If two runners start together and one moves twice as fast, inside a loop the faster one gains on the slower by one node each "
                     "step, so they must eventually meet — the distance shrinks and cannot jump over zero. No set of visited nodes is needed, "
                     "which is the entire point of the trick.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Tortoise and hare: inside a cycle the faster runner is always catching up
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
bool hasCycle(ListNode* head) {
    ListNode* slow = head; ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;           // met inside the loop
    }
    return false;
}   // O(n) time · O(1) space""",
            "java": r"""// Tortoise and hare: inside a cycle the faster runner is always catching up
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;
        fast = fast.next.next;
        if (slow == fast) return true;           // met inside the loop
    }
    return false;
}   // O(n) time · O(1) space""",
            "python": r"""def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:           # identity, not value equality
            return True
    return False""",
        },
    },
    {
        "slug": "palindrome-linked-list",
        "title": "Palindrome Linked List",
        "difficulty": "Easy",
        "pattern": "middle + in-place reversal",
        "statement": "Return true if the list reads the same forwards and backwards, using O(1) extra memory.",
        "examples": [("head = 1 -> 2 -> 2 -> 1", "true"), ("head = 1 -> 2", "false")],
        "constraints": ["1 <= number of nodes <= 10^5", "extra memory must be O(1)", "values fit in a 32-bit integer"],
        "approach": "Split at the middle with the fast/slow pair, reverse the second half in place, then walk the two halves together comparing "
                     "values. Reversing the second half is safe because the comparison destroys nothing — this 'reverse half and walk inward' idea "
                     "is also the basis of reordering and twin-sum problems.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Find the middle, reverse the second half, compare outwards
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
bool isPalindrome(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) { slow = slow->next; fast = fast->next->next; }
    ListNode* prev = nullptr;
    while (slow) { ListNode* nxt = slow->next; slow->next = prev; prev = slow; slow = nxt; }
    for (ListNode *a = head, *b = prev; b; a = a->next, b = b->next)
        if (a->val != b->val) return false;
    return true;
}   // O(n) time · O(1) space""",
            "java": r"""// Find the middle, reverse the second half, compare outwards
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
boolean isPalindrome(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
    ListNode prev = null;
    while (slow != null) { ListNode nxt = slow.next; slow.next = prev; prev = slow; slow = nxt; }
    for (ListNode a = head, b = prev; b != null; a = a.next, b = b.next)
        if (a.val != b.val) return false;
    return true;
}   // O(n) time · O(1) space""",
            "python": r"""def is_palindrome(head):
    slow = fast = head
    while fast and fast.next:          # split at the middle
        slow = slow.next
        fast = fast.next.next
    prev = None
    while slow:                        # reverse the second half in place
        slow.next, prev, slow = prev, slow, slow.next
    a, b = head, prev
    while b:                           # walk the halves together
        if a.val != b.val:
            return False
        a, b = a.next, b.next
    return True""",
        },
    },
    # ---------------------------------------------------------------- MEDIUM
    {
        "slug": "remove-nth-node-from-end-of-list",
        "title": "Remove the N-th Node From the End",
        "difficulty": "Medium",
        "pattern": "fixed-gap two pointers",
        "statement": "Remove the n-th node counted from the end of the list in one pass, and return the head.",
        "examples": [("head = 1 -> 2 -> 3 -> 4 -> 5, n = 2", "1 -> 2 -> 3 -> 5"), ("head = 1, n = 1", "[]")],
        "constraints": ["1 <= number of nodes <= 30", "1 <= n <= number of nodes", "one pass is expected"],
        "approach": "Give the fast pointer an n-node head start, then move both until fast reaches the end: slow is now just before the node to "
                     "delete. A dummy head in front is essential, because removing the first node has no distinct 'previous' without it — the "
                     "classic off-by-one here is a lost node, not a wrong index.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Fast gets an n-node head start; dummy handles n == length
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
ListNode* removeNthFromEnd(ListNode* head, int n) {
    ListNode dummy(0); dummy.next = head;
    ListNode *slow = &dummy, *fast = &dummy;
    for (int i = 0; i < n; i++) fast = fast->next;   // head start of n
    while (fast->next) { slow = slow->next; fast = fast->next; }
    slow->next = slow->next->next;                   // unlink the target
    return dummy.next;
}   // O(n) time · O(1) space""",
            "java": r"""// Fast gets an n-node head start; dummy handles n == length
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode removeNthFromEnd(ListNode head, int n) {
    ListNode dummy = new ListNode(0); dummy.next = head;
    ListNode slow = dummy, fast = dummy;
    for (int i = 0; i < n; i++) fast = fast.next;    // head start of n
    while (fast.next != null) { slow = slow.next; fast = fast.next; }
    slow.next = slow.next.next;                      // unlink the target
    return dummy.next;
}   // O(n) time · O(1) space""",
            "python": r"""def remove_nth_from_end(head, n):
    dummy = ListNode(0)
    dummy.next = head
    slow = fast = dummy
    for _ in range(n):
        fast = fast.next            # head start of n nodes
    while fast.next:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next      # unlink the target
    return dummy.next""",
        },
    },
    {
        "slug": "intersection-of-two-linked-lists",
        "title": "Intersection of Two Linked Lists",
        "difficulty": "Medium",
        "pattern": "align by length difference",
        "statement": "Two lists merge at some node (or not at all). Return the first shared node, comparing by identity, in O(1) extra memory.",
        "examples": [("a = 4 -> 1 -> 8 -> 4 -> 5, b = 5 -> 6 -> 1 -> 8 -> 4 -> 5", "the node with value 8"),
                     ("no shared node", "null")],
        "constraints": ["0 <= nodes per list <= 3 * 10^4", "the lists must not be modified", "extra memory must be O(1)"],
        "approach": "The longer list has extra nodes at the front that cannot be part of the intersection, so skip the length difference first and "
                     "the two pointers then advance in lockstep until they meet. Alternatively switch pointers at the ends — both encode the same "
                     "idea of equalising distance.",
        "complexity": ("O(n + m)", "O(1)"),
        "code": {
            "cpp": r"""// Skip the length difference, then walk in lockstep
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
int len(ListNode* h) { int n = 0; for (; h; h = h->next) n++; return n; }
ListNode* getIntersectionNode(ListNode* a, ListNode* b) {
    int la = len(a), lb = len(b);
    while (la > lb) { a = a->next; la--; }       // drop the extra prefix
    while (lb > la) { b = b->next; lb--; }
    while (a != b) { a = a->next; b = b->next; } // same remaining length
    return a;                                    // nullptr if none
}   // O(n + m) time · O(1) space""",
            "java": r"""// Skip the length difference, then walk in lockstep
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
int len(ListNode h) { int n = 0; for (; h != null; h = h.next) n++; return n; }
ListNode getIntersectionNode(ListNode a, ListNode b) {
    int la = len(a), lb = len(b);
    while (la > lb) { a = a.next; la--; }        // drop the extra prefix
    while (lb > la) { b = b.next; lb--; }
    while (a != b) { a = a.next; b = b.next; }   // same remaining length
    return a;                                    // null if none
}   // O(n + m) time · O(1) space""",
            "python": r"""def get_intersection_node(a, b):
    def length(h):
        n = 0
        while h:
            n += 1
            h = h.next
        return n

    la, lb = length(a), length(b)
    for _ in range(la - lb):
        a = a.next                    # drop the extra prefix
    for _ in range(lb - la):
        b = b.next
    while a is not b:                 # identity comparison
        a, b = a.next, b.next
    return a""",
        },
    },
    {
        "slug": "add-two-numbers",
        "title": "Add Two Numbers",
        "difficulty": "Medium",
        "pattern": "digit-by-digit with carry",
        "statement": "Each list holds a non-negative integer in reverse digit order. Return their sum in the same form.",
        "examples": [("l1 = 2 -> 4 -> 3, l2 = 5 -> 6 -> 4", "7 -> 0 -> 8  (342 + 465 = 807)"),
                     ("l1 = 9 -> 9 -> 9, l2 = 1", "0 -> 0 -> 0 -> 1")],
        "constraints": ["1 <= nodes per list <= 100", "0 <= digit <= 9", "no number has leading zeros except 0 itself"],
        "approach": "Reverse order is a gift: the least significant digits come first, so the addition proceeds with a single carry variable and "
                     "no reversal. Keep looping while either list has digits *or* a carry remains — forgetting the final carry is the standard "
                     "bug (999 + 1 needs a fourth node).",
        "complexity": ("O(max(n, m))", "O(1) output space"),
        "code": {
            "cpp": r"""// Digits arrive least-significant first: one carry, one dummy tail
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
ListNode* addTwoNumbers(ListNode* a, ListNode* b) {
    ListNode dummy(0), *tail = &dummy;
    int carry = 0;
    while (a || b || carry) {                    // carry can add one more node
        int sum = carry;
        if (a) { sum += a->val; a = a->next; }
        if (b) { sum += b->val; b = b->next; }
        carry = sum / 10;
        tail->next = new ListNode(sum % 10);
        tail = tail->next;
    }
    return dummy.next;
}   // O(max(n, m)) time · O(1) space beyond the answer""",
            "java": r"""// Digits arrive least-significant first: one carry, one dummy tail
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode addTwoNumbers(ListNode a, ListNode b) {
    ListNode dummy = new ListNode(0), tail = dummy;
    int carry = 0;
    while (a != null || b != null || carry != 0) {   // carry can add a node
        int sum = carry;
        if (a != null) { sum += a.val; a = a.next; }
        if (b != null) { sum += b.val; b = b.next; }
        carry = sum / 10;
        tail.next = new ListNode(sum % 10);
        tail = tail.next;
    }
    return dummy.next;
}   // O(max(n, m)) time · O(1) space beyond the answer""",
            "python": r"""def add_two_numbers(a, b):
    dummy = tail = ListNode(0)
    carry = 0
    while a or b or carry:          # the carry may need one more node
        total = carry
        if a:
            total += a.val
            a = a.next
        if b:
            total += b.val
            b = b.next
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
    return dummy.next""",
        },
    },
    {
        "slug": "odd-even-linked-list",
        "title": "Odd Even Linked List",
        "difficulty": "Medium",
        "pattern": "two chains woven apart",
        "statement": "Group all nodes at odd indices together followed by all nodes at even indices, preserving the relative order inside each group, "
                     "in O(1) extra space.",
        "examples": [("head = 1 -> 2 -> 3 -> 4 -> 5", "1 -> 3 -> 5 -> 2 -> 4"), ("head = 2 -> 1 -> 3 -> 5 -> 6 -> 4 -> 7", "2 -> 3 -> 6 -> 7 -> 1 -> 5 -> 4")],
        "constraints": ["0 <= number of nodes <= 10^4", "-10^6 <= node values <= 10^6", "extra space must be O(1)"],
        "approach": "Build two chains simultaneously: an odd chain and an even chain, each with its own tail. Because both tails walk forward in "
                     "the same loop, the original order inside each parity survives, and a single link from the odd tail to the even head finishes "
                     "the job.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Two chains built in one pass, then stitched
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
ListNode* oddEvenList(ListNode* head) {
    if (!head) return nullptr;
    ListNode *odd = head, *even = head->next, *evenHead = even;
    while (even && even->next) {
        odd->next = even->next; odd = odd->next;   // odd chain grows
        even->next = odd->next; even = even->next; // even chain grows
    }
    odd->next = evenHead;                          // stitch the two chains
    return head;
}   // O(n) time · O(1) space""",
            "java": r"""// Two chains built in one pass, then stitched
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode oddEvenList(ListNode head) {
    if (head == null) return null;
    ListNode odd = head, even = head.next, evenHead = even;
    while (even != null && even.next != null) {
        odd.next = even.next; odd = odd.next;      // odd chain grows
        even.next = odd.next; even = even.next;    // even chain grows
    }
    odd.next = evenHead;                           // stitch the two chains
    return head;
}   // O(n) time · O(1) space""",
            "python": r"""def odd_even_list(head):
    if not head:
        return None
    odd, even = head, head.next
    even_head = even
    while even and even.next:
        odd.next = even.next          # odd chain grows
        odd = odd.next
        even.next = odd.next          # even chain grows
        even = even.next
    odd.next = even_head              # stitch the two chains
    return head""",
        },
    },
    {
        "slug": "reorder-list",
        "title": "Reorder List",
        "difficulty": "Medium",
        "pattern": "split, reverse, interleave",
        "statement": "Reorder the list as first, last, second, second-last, ... in place and with O(1) extra space.",
        "examples": [("head = 1 -> 2 -> 3 -> 4", "1 -> 4 -> 2 -> 3"), ("head = 1 -> 2 -> 3 -> 4 -> 5", "1 -> 5 -> 2 -> 4 -> 3")],
        "constraints": ["1 <= number of nodes <= 5 * 10^4", "the list must not be modified structurally except as described", "O(1) extra space is required"],
        "approach": "Three familiar moves chained together: find the middle, reverse the second half, then interleave the two halves one node at a "
                     "time. Each move was an easy problem on its own — this is what 'compose the patterns you already know' looks like in practice.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Middle, reverse the second half, then interleave
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
void reorderList(ListNode* head) {
    if (!head || !head->next) return;
    ListNode *slow = head, *fast = head;
    while (fast->next && fast->next->next) { slow = slow->next; fast = fast->next->next; }
    ListNode *prev = nullptr, *cur = slow->next;   // 1. reverse the second half
    slow->next = nullptr;                          // split the two halves
    while (cur) { ListNode* nxt = cur->next; cur->next = prev; prev = cur; cur = nxt; }
    for (ListNode *a = head, *b = prev; b; ) {     // 2. interleave
        ListNode *an = a->next, *bn = b->next;
        a->next = b; b->next = an;
        a = an; b = bn;
    }
}   // O(n) time · O(1) space""",
            "java": r"""// Middle, reverse the second half, then interleave
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
void reorderList(ListNode head) {
    if (head == null || head.next == null) return;
    ListNode slow = head, fast = head;
    while (fast.next != null && fast.next.next != null) { slow = slow.next; fast = fast.next.next; }
    ListNode prev = null, cur = slow.next;         // 1. reverse the second half
    slow.next = null;                              // split the two halves
    while (cur != null) { ListNode nxt = cur.next; cur.next = prev; prev = cur; cur = nxt; }
    for (ListNode a = head, b = prev; b != null; ) {   // 2. interleave
        ListNode an = a.next, bn = b.next;
        a.next = b; b.next = an;
        a = an; b = bn;
    }
}   // O(n) time · O(1) space""",
            "python": r"""def reorder_list(head):
    if not head or not head.next:
        return
    slow, fast = head, head              # 1. split at the middle
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    prev, cur = None, slow.next
    slow.next = None                     # the two halves are now separate
    while cur:                           # 2. reverse the second half
        cur.next, prev, cur = prev, cur, cur.next
    a, b = head, prev
    while b:                             # 3. interleave first-half / reversed
        a.next, a = b, a.next
        b.next, b = a, b.next""",
        },
    },
    {
        "slug": "rotate-list",
        "title": "Rotate List",
        "difficulty": "Medium",
        "pattern": "close the ring, cut it",
        "statement": "Rotate the list to the right by k places and return the new head.",
        "examples": [("head = 1 -> 2 -> 3 -> 4 -> 5, k = 2", "4 -> 5 -> 1 -> 2 -> 3"), ("head = 0 -> 1 -> 2, k = 4", "2 -> 0 -> 1")],
        "constraints": ["0 <= number of nodes <= 500", "-100 <= node values <= 100", "0 <= k <= 2 * 10^9 (so k may exceed the length)"],
        "approach": "A rotation is a cut and a re-join. Measure the length, reduce k modulo it (k can be enormous), then close the list into a "
                     "ring and sever it at the right place — one pass, no reversal, and no need to know the length twice.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Measure, close the ring, cut at n - (k % n)
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
ListNode* rotateRight(ListNode* head, int k) {
    if (!head || !head->next) return head;
    int n = 1; ListNode* tail = head;
    while (tail->next) { tail = tail->next; n++; }
    k %= n;                                      // k may exceed the length
    if (k == 0) return head;
    tail->next = head;                           // close the ring
    ListNode* newTail = head;
    for (int i = 0; i < n - k - 1; i++) newTail = newTail->next;
    ListNode* newHead = newTail->next;
    newTail->next = nullptr;                     // cut the ring
    return newHead;
}   // O(n) time · O(1) space""",
            "java": r"""// Measure, close the ring, cut at n - (k % n)
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode rotateRight(ListNode head, int k) {
    if (head == null || head.next == null) return head;
    int n = 1; ListNode tail = head;
    while (tail.next != null) { tail = tail.next; n++; }
    k %= n;                                      // k may exceed the length
    if (k == 0) return head;
    tail.next = head;                            // close the ring
    ListNode newTail = head;
    for (int i = 0; i < n - k - 1; i++) newTail = newTail.next;
    ListNode newHead = newTail.next;
    newTail.next = null;                         // cut the ring
    return newHead;
}   // O(n) time · O(1) space""",
            "python": r"""def rotate_right(head, k):
    if not head or not head.next:
        return head
    n, tail = 1, head
    while tail.next:
        tail, n = tail.next, n + 1
    k %= n                      # k can be billions
    if k == 0:
        return head
    tail.next = head            # close the ring
    new_tail = head
    for _ in range(n - k - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None        # cut the ring
    return new_head""",
        },
    },
    {
        "slug": "swap-nodes-in-pairs",
        "title": "Swap Nodes in Pairs",
        "difficulty": "Medium",
        "pattern": "local rewiring with a predecessor",
        "statement": "Swap every two adjacent nodes and return the head, changing the links rather than the values.",
        "examples": [("head = 1 -> 2 -> 3 -> 4", "2 -> 1 -> 4 -> 3"), ("head = 1", "1")],
        "constraints": ["0 <= number of nodes <= 100", "values must not be copied between nodes", "only the links may change"],
        "approach": "Keep a pointer to the node *before* the pair. Swapping the pair means three re-links, after which the predecessor must become "
                     "the old first node of the pair — the position the next pair will start from. A dummy head makes the first pair look like "
                     "every other pair.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// prev -> (a, b) becomes prev -> (b, a), then prev advances to a
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
ListNode* swapPairs(ListNode* head) {
    ListNode dummy(0); dummy.next = head;
    ListNode* prev = &dummy;
    while (prev->next && prev->next->next) {
        ListNode *a = prev->next, *b = a->next;
        a->next = b->next;                       // a now points past b
        b->next = a;                             // b points at a
        prev->next = b;                          // predecessor points at b
        prev = a;                                // a is in front of the next pair
    }
    return dummy.next;
}   // O(n) time · O(1) space""",
            "java": r"""// prev -> (a, b) becomes prev -> (b, a), then prev advances to a
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode swapPairs(ListNode head) {
    ListNode dummy = new ListNode(0); dummy.next = head;
    ListNode prev = dummy;
    while (prev.next != null && prev.next.next != null) {
        ListNode a = prev.next, b = a.next;
        a.next = b.next;                         // a now points past b
        b.next = a;                              // b points at a
        prev.next = b;                           // predecessor points at b
        prev = a;                                // a sits before the next pair
    }
    return dummy.next;
}   // O(n) time · O(1) space""",
            "python": r"""def swap_pairs(head):
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    while prev.next and prev.next.next:
        a, b = prev.next, prev.next.next
        a.next = b.next        # a now points past b
        b.next = a             # b points at a
        prev.next = b          # predecessor points at b
        prev = a               # a sits in front of the next pair
    return dummy.next""",
        },
    },
    {
        "slug": "partition-list",
        "title": "Partition List",
        "difficulty": "Medium",
        "pattern": "two dummy chains",
        "statement": "Rearrange the nodes so that all values less than x come before all values greater than or equal to x, preserving the original "
                     "relative order inside each group.",
        "examples": [("head = 1 -> 4 -> 3 -> 2 -> 5 -> 2, x = 3", "1 -> 2 -> 2 -> 4 -> 3 -> 5"),
                     ("head = 2 -> 1, x = 2", "1 -> 2")],
        "constraints": ["0 <= number of nodes <= 200", "-100 <= node values <= 100", "relative order must be preserved"],
        "approach": "Two dummy heads, one collecting the small values and one collecting the rest; walk the input once and append each node to its "
                     "chain. Joining the two chains at the end is the only link you have to build yourself — remember to terminate the second "
                     "chain or it will still point into the old structure.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Two chains: smaller-than-x and everything else
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
ListNode* partition(ListNode* head, int x) {
    ListNode smallDummy(0), bigDummy(0);
    ListNode *small = &smallDummy, *big = &bigDummy;
    for (; head; head = head->next) {
        if (head->val < x) { small->next = head; small = head; }   // append
        else { big->next = head; big = head; }
    }
    big->next = nullptr;                          // terminate the big chain!
    small->next = bigDummy.next;                  // join them
    return smallDummy.next;
}   // O(n) time · O(1) space""",
            "java": r"""// Two chains: smaller-than-x and everything else
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode partition(ListNode head, int x) {
    ListNode smallDummy = new ListNode(0), bigDummy = new ListNode(0);
    ListNode small = smallDummy, big = bigDummy;
    for (; head != null; head = head.next) {
        if (head.val < x) { small.next = head; small = head; }    // append
        else { big.next = head; big = head; }
    }
    big.next = null;                              // terminate the big chain!
    small.next = bigDummy.next;                   // join them
    return smallDummy.next;
}   // O(n) time · O(1) space""",
            "python": r"""def partition(head, x):
    small_dummy = ListNode(0)
    big_dummy = ListNode(0)
    small, big = small_dummy, big_dummy
    while head:
        if head.val < x:
            small.next = head         # append to the small chain
            small = head
        else:
            big.next = head           # append to the big chain
            big = head
        head = head.next
    big.next = None                   # terminate the big chain!
    small.next = big_dummy.next       # join them
    return small_dummy.next""",
        },
    },
    {
        "slug": "copy-list-with-random-pointer",
        "title": "Copy a List With Random Pointers",
        "difficulty": "Medium",
        "pattern": "hash map old -> new",
        "statement": "Each node has a next pointer and a random pointer that may point anywhere in the list (or to null). Return a deep copy.",
        "examples": [("[[7,null],[13,0],[11,4],[10,2],[1,0]]", "an identical but fully independent list"),
                     ("[]", "[]")],
        "constraints": ["0 <= number of nodes <= 1000", "random pointers may point backwards or forwards", "the copy must share no nodes with the original"],
        "approach": "Two passes over a map from original node to its copy: the first pass creates every copy (so every target exists), the second "
                     "wires next and random using the map. Creating all the nodes first is what makes a forward random pointer possible.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Pass 1 creates every copy, pass 2 wires next and random
struct Node { int val; Node *next, *random; Node(int v) : val(v), next(nullptr), random(nullptr) {} };
Node* copyRandomList(Node* head) {
    unordered_map<Node*, Node*> copy;             // original -> duplicate
    for (Node* p = head; p; p = p->next) copy[p] = new Node(p->val);
    for (Node* p = head; p; p = p->next) {
        if (p->next) copy[p]->next = copy[p->next];       // target already exists
        if (p->random) copy[p]->random = copy[p->random];
    }
    return head ? copy[head] : nullptr;
}   // O(n) time · O(n) space""",
            "java": r"""// Pass 1 creates every copy, pass 2 wires next and random
class Node { int val; Node next, random; Node(int v) { val = v; } }
Node copyRandomList(Node head) {
    Map<Node, Node> copy = new HashMap<>();       // original -> duplicate
    for (Node p = head; p != null; p = p.next) copy.put(p, new Node(p.val));
    for (Node p = head; p != null; p = p.next) {
        Node c = copy.get(p);
        if (p.next != null) c.next = copy.get(p.next);       // target exists
        if (p.random != null) c.random = copy.get(p.random);
    }
    return head == null ? null : copy.get(head);
}   // O(n) time · O(n) space""",
            "python": r"""def copy_random_list(head):
    copy = {}                        # original node -> its duplicate
    p = head
    while p:                         # pass 1: create every duplicate
        copy[p] = Node(p.val)
        p = p.next
    p = head
    while p:                         # pass 2: wire the pointers through the map
        if p.next:
            copy[p].next = copy[p.next]
        if p.random:
            copy[p].random = copy[p.random]
        p = p.next
    return copy[head] if head else None""",
        },
    },
    {
        "slug": "flatten-multilevel-doubly-linked-list",
        "title": "Flatten a Multilevel Doubly Linked List",
        "difficulty": "Medium",
        "pattern": "stack of pending next nodes",
        "statement": "Nodes have next, prev and child pointers. Flatten the list so that a child list is spliced in immediately after its parent, "
                     "keeping the doubly linked order, and return the head.",
        "examples": [("1 - 2 - 3 with 3 child 7 - 8 and 8 child 11", "1 - 2 - 3 - 7 - 8 - 11"),
                     ("empty list", "empty list")],
        "constraints": ["0 <= number of nodes <= 1000", "the structure is a valid doubly linked list", "no node may appear twice in the result"],
        "approach": "Walk the top level and keep a stack of 'next' pointers you had to postpone. When you reach a node with a child, push the old "
                     "next, then dive into the child. Popping the stack when you run out restores the postponed tail — this is depth-first "
                     "traversal written without recursion.",
        "complexity": ("O(n)", "O(n) worst case for the stack"),
        "code": {
            "cpp": r"""// Push the postponed 'next' and dive into the child; pop to resume
struct Node { int val; Node *prev, *next, *child; Node(int v) : val(v), prev(nullptr), next(nullptr), child(nullptr) {} };
Node* flatten(Node* head) {
    vector<Node*> st;                            // postponed next pointers
    for (Node* cur = head; cur; cur = cur->next) {
        if (cur->child) {
            if (cur->next) st.push_back(cur->next);       // remember the remainder
            cur->next = cur->child; cur->child->prev = cur;
            cur->child = nullptr;                         // the child is consumed
        } else if (!cur->next && !st.empty()) {           // end of a level
            Node* nxt = st.back(); st.pop_back();
            cur->next = nxt; nxt->prev = cur;
        }
    }
    return head;
}   // O(n) time · O(n) space""",
            "java": r"""// Push the postponed 'next' and dive into the child; pop to resume
class Node { int val; Node prev, next, child; Node(int v) { val = v; } }
Node flatten(Node head) {
    Deque<Node> st = new ArrayDeque<>();         // postponed next pointers
    for (Node cur = head; cur != null; cur = cur.next) {
        if (cur.child != null) {
            if (cur.next != null) st.push(cur.next);       // remember the rest
            cur.next = cur.child; cur.child.prev = cur;
            cur.child = null;                              // the child is consumed
        } else if (cur.next == null && !st.isEmpty()) {    // end of a level
            Node nxt = st.pop();
            cur.next = nxt; nxt.prev = cur;
        }
    }
    return head;
}   // O(n) time · O(n) space""",
            "python": r"""def flatten(head):
    st = []                          # postponed 'next' pointers
    cur = head
    while cur:
        if cur.child:
            if cur.next:
                st.append(cur.next)  # remember the remainder
            cur.next = cur.child
            cur.child.prev = cur
            cur.child = None         # the child is consumed
        elif not cur.next and st:    # end of a level: resume the postponed tail
            nxt = st.pop()
            cur.next = nxt
            nxt.prev = cur
        cur = cur.next
    return head""",
        },
    },
    {
        "slug": "linked-list-cycle-ii",
        "title": "Linked List Cycle II",
        "difficulty": "Medium",
        "pattern": "meet, then walk from the head",
        "statement": "If the list has a cycle, return the node where the cycle begins; otherwise return null — with O(1) extra memory.",
        "examples": [("3 -> 2 -> 0 -> -4 with -4 pointing back to the node holding 2", "the node holding 2"),
                     ("1 -> 2 with no cycle", "null")],
        "constraints": ["0 <= number of nodes <= 10^4", "extra memory must be O(1)", "do not modify the list"],
        "approach": "Once the two runners meet, the distance from the head to the cycle entry equals the distance from the meeting point to the "
                     "entry *measured along the cycle*. So restart one pointer at the head and advance both one step at a time; they collide "
                     "exactly at the entry. Beautiful, non-obvious, and worth being able to derive rather than memorise.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// After the meeting, head-to-entry equals meeting-to-entry along the cycle
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
ListNode* detectCycle(ListNode* head) {
    ListNode *slow = head, *fast = head;
    while (fast && fast->next) {
        slow = slow->next; fast = fast->next->next;
        if (slow == fast) {                      // met inside the cycle
            for (ListNode* p = head; p != slow; p = p->next, slow = slow->next) { }
            return slow;                         // entry point
        }
    }
    return nullptr;
}   // O(n) time · O(1) space""",
            "java": r"""// After the meeting, head-to-entry equals meeting-to-entry along the cycle
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode detectCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next; fast = fast.next.next;
        if (slow == fast) {                      // met inside the cycle
            ListNode p = head;
            while (p != slow) { p = p.next; slow = slow.next; }
            return slow;                         // entry point
        }
    }
    return null;
}   // O(n) time · O(1) space""",
            "python": r"""def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:               # met inside the cycle
            p = head
            while p is not slow:       # equal distances to the entry
                p, slow = p.next, slow.next
            return slow                # the entry node
    return None""",
        },
    },
    {
        "slug": "split-linked-list-in-parts",
        "title": "Split Linked List in Parts",
        "difficulty": "Medium",
        "pattern": "quotient and remainder",
        "statement": "Split the list into k consecutive parts where no two part sizes differ by more than one and the earlier parts are never "
                     "smaller; return the k pieces (some may be empty).",
        "examples": [("head = 1 -> 2 -> 3, k = 5", "[[1],[2],[3],[],[]]"), ("head = 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 10, k = 3", "[[1,2,3,4],[5,6,7],[8,9,10]]")],
        "constraints": ["0 <= number of nodes <= 1000", "1 <= k <= 50", "empty parts must be represented as an empty list, not skipped"],
        "approach": "Size the parts before cutting: every part gets n/k nodes and the first n%k parts get one extra. Then walk once, taking the "
                     "computed number of nodes per part and severing the link at each boundary — computing the sizes first is what makes the "
                     "'earlier parts are never smaller' rule automatic.",
        "complexity": ("O(n + k)", "O(k) for the output"),
        "code": {
            "cpp": r"""// Sizes first: n/k each, plus one extra for the first n%k parts
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
vector<ListNode*> splitListToParts(ListNode* head, int k) {
    int n = 0; for (ListNode* p = head; p; p = p->next) n++;
    int base = n / k, extra = n % k;
    vector<ListNode*> parts;
    ListNode* cur = head;
    for (int i = 0; i < k; i++) {
        parts.push_back(cur);
        int take = base + (i < extra ? 1 : 0);
        for (int j = 0; j < take - 1 && cur; j++) cur = cur->next;   // walk to the end
        if (cur) { ListNode* nxt = cur->next; cur->next = nullptr; cur = nxt; }   // cut
    }
    return parts;
}   // O(n + k) time · O(k) space""",
            "java": r"""// Sizes first: n/k each, plus one extra for the first n%k parts
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode[] splitListToParts(ListNode head, int k) {
    int n = 0; for (ListNode p = head; p != null; p = p.next) n++;
    int base = n / k, extra = n % k;
    ListNode[] parts = new ListNode[k];
    ListNode cur = head;
    for (int i = 0; i < k; i++) {
        parts[i] = cur;
        int take = base + (i < extra ? 1 : 0);
        for (int j = 0; j < take - 1 && cur != null; j++) cur = cur.next;   // walk
        if (cur != null) { ListNode nxt = cur.next; cur.next = null; cur = nxt; }   // cut
    }
    return parts;
}   // O(n + k) time · O(k) space""",
            "python": r"""def split_list_to_parts(head, k):
    n = 0
    p = head
    while p:
        n += 1
        p = p.next
    base, extra = divmod(n, k)          # first 'extra' parts get one more node
    parts, cur = [], head
    for i in range(k):
        parts.append(cur)
        take = base + (1 if i < extra else 0)
        for _ in range(take - 1):       # walk to the end of this part
            if cur:
                cur = cur.next
        if cur:                         # cut the link to the next part
            cur.next, cur = None, cur.next
    return parts""",
        },
    },
    # ------------------------------------------------------------------ HARD
    {
        "slug": "merge-k-sorted-lists",
        "title": "Merge K Sorted Lists",
        "difficulty": "Hard",
        "pattern": "k-way merge (heap or divide and conquer)",
        "statement": "Given k sorted linked lists, merge them into one sorted list and return its head.",
        "examples": [("lists = [[1,4,5],[1,3,4],[2,6]]", "1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 5 -> 6"), ("lists = []", "[]")],
        "constraints": ["0 <= k <= 10^4", "0 <= total nodes <= 10^4", "-10^4 <= node values <= 10^4", "the naive k-way scan is too slow"],
        "approach": "A min-heap of the k current heads always hands back the smallest remaining value; each pop pushes that list's next node, so "
                     "the cost is O(total · log k). The divide-and-conquer alternative — merge lists in pairs, log k rounds — reaches the same "
                     "bound with no heap and is often faster in practice. Know both; interviewers ask for the second after you write the first.",
        "complexity": ("O(N log k)", "O(k)"),
        "code": {
            "cpp": r"""// Min-heap over the k current heads
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
struct Cmp { bool operator()(ListNode* a, ListNode* b) const { return a->val > b->val; } };
ListNode* mergeKLists(vector<ListNode*>& lists) {
    priority_queue<ListNode*, vector<ListNode*>, Cmp> pq;
    for (ListNode* h : lists) if (h) pq.push(h);          // seed with every head
    ListNode dummy(0), *tail = &dummy;
    while (!pq.empty()) {
        ListNode* node = pq.top(); pq.pop();              // smallest remaining
        tail->next = node; tail = node;                   // append it
        if (node->next) pq.push(node->next);              // advance that list
    }
    tail->next = nullptr;
    return dummy.next;
}   // O(N log k) time · O(k) space""",
            "java": r"""// Min-heap over the k current heads
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode mergeKLists(ListNode[] lists) {
    PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> a.val - b.val);
    for (ListNode h : lists) if (h != null) pq.add(h);    // seed with every head
    ListNode dummy = new ListNode(0), tail = dummy;
    while (!pq.isEmpty()) {
        ListNode node = pq.poll();                         // smallest remaining
        tail.next = node; tail = node;                     // append it
        if (node.next != null) pq.add(node.next);          // advance that list
    }
    tail.next = null;
    return dummy.next;
}   // O(N log k) time · O(k) space""",
            "python": r"""import heapq

def merge_k_lists(lists):
    pq = [(h.val, i, h) for i, h in enumerate(lists) if h]
    heapq.heapify(pq)               # tuple carries i so nodes never compare
    dummy = tail = ListNode(0)
    while pq:
        _, i, node = heapq.heappop(pq)      # smallest remaining head
        tail.next, tail = node, node        # append it
        if node.next:
            heapq.heappush(pq, (node.next.val, i, node.next))
    tail.next = None
    return dummy.next""",
        },
    },
    {
        "slug": "reverse-nodes-in-k-group",
        "title": "Reverse Nodes in k-Group",
        "difficulty": "Hard",
        "pattern": "count first, then reverse the group",
        "statement": "Reverse the nodes of the list k at a time; if the final group has fewer than k nodes, leave it unchanged. Only the links may "
                     "change.",
        "examples": [("head = 1 -> 2 -> 3 -> 4 -> 5, k = 2", "2 -> 1 -> 4 -> 3 -> 5"),
                     ("head = 1 -> 2 -> 3 -> 4 -> 5, k = 3", "3 -> 2 -> 1 -> 4 -> 5")],
        "constraints": ["1 <= number of nodes <= 5000", "1 <= k <= number of nodes", "node values may not be swapped"],
        "approach": "Two rules make this manageable: check that k nodes remain *before* touching anything (so the short tail stays intact), and "
                     "reverse inside the group by inserting each node right after the group's predecessor — a head-insertion loop that never "
                     "needs a second pass over the group.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// If k nodes remain, head-insert each of them after 'prev'
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
ListNode* reverseKGroup(ListNode* head, int k) {
    ListNode dummy(0); dummy.next = head;
    ListNode* prev = &dummy;
    while (true) {
        ListNode* probe = prev;
        for (int i = 0; i < k && probe; i++) probe = probe->next;
        if (!probe) break;                            // fewer than k left: stop
        ListNode* cur = prev->next;
        for (int i = 1; i < k; i++) {                 // head-insert k-1 nodes
            ListNode* nxt = cur->next;
            cur->next = nxt->next;
            nxt->next = prev->next;
            prev->next = nxt;
        }
        for (int i = 0; i < k; i++) prev = prev->next;   // prev = group's new tail
    }
    return dummy.next;
}   // O(n) time · O(1) space""",
            "java": r"""// If k nodes remain, head-insert each of them after 'prev'
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode reverseKGroup(ListNode head, int k) {
    ListNode dummy = new ListNode(0); dummy.next = head;
    ListNode prev = dummy;
    while (true) {
        ListNode probe = prev;
        for (int i = 0; i < k && probe != null; i++) probe = probe.next;
        if (probe == null) break;                     // fewer than k left: stop
        ListNode cur = prev.next;
        for (int i = 1; i < k; i++) {                 // head-insert k-1 nodes
            ListNode nxt = cur.next;
            cur.next = nxt.next;
            nxt.next = prev.next;
            prev.next = nxt;
        }
        for (int i = 0; i < k; i++) prev = prev.next; // prev = group's new tail
    }
    return dummy.next;
}   // O(n) time · O(1) space""",
            "python": r"""def reverse_k_group(head, k):
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    while True:
        probe = prev                      # check k nodes remain
        for _ in range(k):
            probe = probe.next
            if not probe:
                return dummy.next
        cur = prev.next
        for _ in range(k - 1):            # head-insert k-1 nodes
            nxt = cur.next
            cur.next = nxt.next
            nxt.next = prev.next
            prev.next = nxt
        for _ in range(k):                # prev becomes the group's new tail
            prev = prev.next
    return dummy.next""",
        },
    },
    {
        "slug": "lru-cache",
        "title": "LRU Cache",
        "difficulty": "Hard",
        "pattern": "hash map + doubly linked list",
        "statement": "Design a cache with capacity c supporting get(key) and put(key, value) in O(1). When full, evict the least recently used key; "
                     "both get and put count as uses.",
        "examples": [("capacity 2: put(1,1), put(2,2), get(1), put(3,3)", "get(1) = 1, then key 2 is evicted"),
                     ("after that, get(2)", "-1 (it was evicted)")],
        "constraints": ["1 <= capacity <= 3000", "up to 2 * 10^5 calls", "0 <= key, value <= 10^4"],
        "approach": "Two structures with one job each: a hash map from key to node gives O(1) lookup, and a doubly linked list gives O(1) "
                     "reordering. A *hit* means unlinking the node and pushing it to the front; a *put* that overflows means deleting the tail. "
                     "The map must be updated in step with the list — every list operation has a matching map operation, and forgetting one is the "
                     "usual bug.",
        "complexity": ("O(1) per operation", "O(capacity)"),
        "code": {
            "cpp": r"""// map: key -> node; list: most recent at the front
struct DNode {
    int key, val; DNode *prev, *next;
    DNode(int k, int v) : key(k), val(v), prev(nullptr), next(nullptr) {}
};
class LRUCache {
    int cap;
    unordered_map<int, DNode*> mp;
    DNode *head, *tail;                          // sentinels: no null checks
    void unlink(DNode* n) { n->prev->next = n->next; n->next->prev = n->prev; }
    void pushFront(DNode* n) {
        n->next = head->next; n->prev = head;
        head->next->prev = n; head->next = n;
    }
public:
    LRUCache(int capacity) : cap(capacity) {
        head = new DNode(0, 0); tail = new DNode(0, 0);
        head->next = tail; tail->prev = head;
    }
    int get(int key) {
        auto it = mp.find(key);
        if (it == mp.end()) return -1;
        unlink(it->second); pushFront(it->second);   // mark as most recent
        return it->second->val;
    }
    void put(int key, int value) {
        if (mp.count(key)) { DNode* n = mp[key]; n->val = value; unlink(n); pushFront(n); return; }
        if ((int)mp.size() == cap) {                 // evict the least recent
            DNode* lru = tail->prev;
            unlink(lru); mp.erase(lru->key); delete lru;
        }
        DNode* n = new DNode(key, value);
        mp[key] = n; pushFront(n);
    }
};   // O(1) per operation · O(capacity) space""",
            "java": r"""// map: key -> node; list: most recent at the front
class LRUCache {
    class DNode { int key, val; DNode prev, next; DNode(int k, int v) { key = k; val = v; } }
    private final int cap;
    private final Map<Integer, DNode> map = new HashMap<>();
    private final DNode head = new DNode(0, 0), tail = new DNode(0, 0);   // sentinels

    public LRUCache(int capacity) { cap = capacity; head.next = tail; tail.prev = head; }
    private void unlink(DNode n) { n.prev.next = n.next; n.next.prev = n.prev; }
    private void pushFront(DNode n) {
        n.next = head.next; n.prev = head;
        head.next.prev = n; head.next = n;
    }
    public int get(int key) {
        DNode n = map.get(key);
        if (n == null) return -1;
        unlink(n); pushFront(n);                 // mark as most recent
        return n.val;
    }
    public void put(int key, int value) {
        DNode n = map.get(key);
        if (n != null) { n.val = value; unlink(n); pushFront(n); return; }
        if (map.size() == cap) {                 // evict the least recent
            DNode lru = tail.prev;
            unlink(lru); map.remove(lru.key);
        }
        DNode fresh = new DNode(key, value);
        map.put(key, fresh); pushFront(fresh);
    }
}   // O(1) per operation · O(capacity) space""",
            "python": r"""class DNode:
    __slots__ = ('key', 'val', 'prev', 'next')

    def __init__(self, key=0, val=0):
        self.key, self.val = key, val
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}                    # key -> node
        self.head, self.tail = DNode(), DNode()   # sentinels: no null checks
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, n):
        n.prev.next = n.next
        n.next.prev = n.prev

    def _push_front(self, n):
        n.prev, n.next = self.head, self.head.next
        self.head.next.prev = n
        self.head.next = n

    def get(self, key):
        n = self.map.get(key)
        if n is None:
            return -1
        self._unlink(n)
        self._push_front(n)              # mark as most recent
        return n.val

    def put(self, key, value):
        n = self.map.get(key)
        if n is not None:
            n.val = value
            self._unlink(n)
            self._push_front(n)
            return
        if len(self.map) == self.cap:    # evict the least recently used
            lru = self.tail.prev
            self._unlink(lru)
            del self.map[lru.key]
        n = DNode(key, value)
        self.map[key] = n
        self._push_front(n)""",
        },
    },
    {
        "slug": "lfu-cache",
        "title": "LFU Cache",
        "difficulty": "Hard",
        "pattern": "frequencies + recency buckets",
        "statement": "Design a cache with capacity c supporting get and put in O(1). When full, evict the key with the smallest use frequency; ties "
                     "are broken by least recent use, with a fresh put starting at frequency 1.",
        "examples": [("capacity 2: put(1,1), put(2,2), get(1), put(3,3)", "key 2 is evicted (frequency 1, and older)"),
                     ("then get(2), get(3)", "-1, then 3")],
        "constraints": ["1 <= capacity <= 10^4", "up to 2 * 10^5 calls", "0 <= key, value <= 10^5"],
        "approach": "Extend the LRU design with one more map: frequency -> ordered set of keys with that frequency. Eviction always comes from "
                     "the smallest non-empty frequency, and each access moves the key up exactly one bucket. Tracking the minimum frequency "
                     "explicitly (rather than searching for it) is what keeps every operation constant time.",
        "complexity": ("O(1) per operation", "O(capacity)"),
        "code": {
            "cpp": r"""// freq -> ordered keys; evict from the smallest non-empty bucket
class LFUCache {
    int cap, minFreq = 0;
    unordered_map<int, pair<int, int>> kv;                 // key -> (value, freq)
    unordered_map<int, list<int>> byFreq;                  // freq -> keys, oldest first
    unordered_map<int, list<int>::iterator> pos;           // key -> its list position
    void touch(int key) {
        auto& [val, f] = kv[key];
        byFreq[f].erase(pos[key]);
        if (byFreq[f].empty()) {
            byFreq.erase(f);
            if (minFreq == f) minFreq++;                   // only bucket was f
        }
        byFreq[++f].push_back(key);                        // move up one bucket
        pos[key] = prev(byFreq[f].end());
    }
public:
    LFUCache(int capacity) : cap(capacity) {}
    int get(int key) {
        auto it = kv.find(key);
        if (it == kv.end()) return -1;
        touch(key);
        return it->second.first;
    }
    void put(int key, int value) {
        if (cap == 0) return;
        if (kv.count(key)) { kv[key].first = value; touch(key); return; }
        if ((int)kv.size() == cap) {                       // evict the LFU key
            int victim = byFreq[minFreq].front();
            byFreq[minFreq].pop_front();
            if (byFreq[minFreq].empty()) byFreq.erase(minFreq);
            kv.erase(victim); pos.erase(victim);
        }
        kv[key] = {value, 1};
        byFreq[1].push_back(key);
        pos[key] = prev(byFreq[1].end());
        minFreq = 1;                                       // a new key is freq 1
    }
};   // O(1) per operation · O(capacity) space""",
            "java": r"""// freq -> ordered keys; evict from the smallest non-empty bucket
class LFUCache {
    private final int cap;
    private int minFreq = 0;
    private final Map<Integer, int[]> kv = new HashMap<>();              // key -> {val, freq}
    private final Map<Integer, LinkedHashSet<Integer>> byFreq = new HashMap<>();   // oldest first
    private final Map<Integer, Integer> freqOf = new HashMap<>();

    public LFUCache(int capacity) { cap = capacity; }
    private void touch(int key) {
        int f = freqOf.get(key);
        LinkedHashSet<Integer> bucket = byFreq.get(f);
        bucket.remove(key);
        if (bucket.isEmpty()) {
            byFreq.remove(f);
            if (minFreq == f) minFreq++;                    // only bucket was f
        }
        freqOf.put(key, f + 1);                              // move up one bucket
        byFreq.computeIfAbsent(f + 1, k -> new LinkedHashSet<>()).add(key);
        kv.get(key)[1] = f + 1;
    }
    public int get(int key) {
        if (!kv.containsKey(key)) return -1;
        int val = kv.get(key)[0];
        touch(key);
        return val;
    }
    public void put(int key, int value) {
        if (cap == 0) return;
        if (kv.containsKey(key)) { kv.get(key)[0] = value; touch(key); return; }
        if (kv.size() == cap) {                              // evict the LFU key
            LinkedHashSet<Integer> bucket = byFreq.get(minFreq);
            int victim = bucket.iterator().next();
            bucket.remove(victim);
            if (bucket.isEmpty()) byFreq.remove(minFreq);
            kv.remove(victim); freqOf.remove(victim);
        }
        kv.put(key, new int[]{value, 1});
        freqOf.put(key, 1);
        byFreq.computeIfAbsent(1, k -> new LinkedHashSet<>()).add(key);
        minFreq = 1;                                         // a new key is freq 1
    }
}   // O(1) per operation · O(capacity) space""",
            "python": r"""from collections import OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.val = {}                    # key -> value
        self.freq = {}                   # key -> frequency
        self.by_freq = {}                # frequency -> OrderedDict of keys
        self.min_freq = 0

    def _touch(self, key):
        f = self.freq[key]
        bucket = self.by_freq[f]
        del bucket[key]
        if not bucket:
            del self.by_freq[f]
            if self.min_freq == f:       # that was the only bucket at this level
                self.min_freq += 1
        self.freq[key] = f + 1           # move up one bucket
        self.by_freq.setdefault(f + 1, OrderedDict())[key] = None

    def get(self, key):
        if key not in self.val:
            return -1
        self._touch(key)
        return self.val[key]

    def put(self, key, value):
        if self.cap == 0:
            return
        if key in self.val:
            self.val[key] = value
            self._touch(key)
            return
        if len(self.val) == self.cap:                # evict the least frequent
            bucket = self.by_freq[self.min_freq]
            victim, _ = bucket.popitem(last=False)   # oldest key in that bucket
            del self.val[victim]
            del self.freq[victim]
            if not bucket:
                del self.by_freq[self.min_freq]
        self.val[key] = value
        self.freq[key] = 1
        self.by_freq.setdefault(1, OrderedDict())[key] = None
        self.min_freq = 1                            # a fresh key is frequency 1""",
        },
    },
    {
        "slug": "sort-list",
        "title": "Sort a Linked List",
        "difficulty": "Hard",
        "pattern": "bottom-up merge sort",
        "statement": "Sort a linked list in O(n log n) time with O(1) extra space.",
        "examples": [("head = 4 -> 2 -> 1 -> 3", "1 -> 2 -> 3 -> 4"), ("head = -1 -> 5 -> 3 -> 4 -> 0", "-1 -> 0 -> 3 -> 4 -> 5")],
        "constraints": ["0 <= number of nodes <= 5 * 10^4", "-10^5 <= node values <= 10^5", "extra space must be O(1), so recursion is out"],
        "approach": "Merge sort, but built upwards instead of recursively: start with runs of length 1, merge neighbouring runs, then double "
                     "the run length and repeat. Each pass costs O(n) and there are log n passes, and the only state kept between passes is a "
                     "few pointers — the reason it satisfies the O(1) space rule.",
        "complexity": ("O(n log n)", "O(1)"),
        "code": {
            "cpp": r"""// Merge runs of size 1, 2, 4, ... — no recursion, no extra memory
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
ListNode* cut(ListNode* head, int size) {        // cut after 'size' nodes
    for (int i = 0; head && i < size - 1; i++) head = head->next;
    if (!head) return nullptr;
    ListNode* rest = head->next;
    head->next = nullptr;
    return rest;
}
ListNode* mergeInto(ListNode* tail, ListNode* a, ListNode* b) {
    while (a && b) {
        if (a->val <= b->val) { tail->next = a; a = a->next; }
        else { tail->next = b; b = b->next; }
        tail = tail->next;
    }
    tail->next = a ? a : b;
    while (tail->next) tail = tail->next;        // tail must end at the last node
    return tail;
}
ListNode* sortList(ListNode* head) {
    int n = 0; for (ListNode* p = head; p; p = p->next) n++;
    ListNode dummy(0); dummy.next = head;
    for (int size = 1; size < n; size *= 2) {    // log n passes
        ListNode* tail = &dummy;
        ListNode* cur = dummy.next;
        while (cur) {                            // merge this pass, run by run
            ListNode* left = cur;
            ListNode* right = cut(left, size);
            cur = cut(right, size);
            tail = mergeInto(tail, left, right);
        }
    }
    return dummy.next;
}   // O(n log n) time · O(1) space""",
            "java": r"""// Merge runs of size 1, 2, 4, ... — no recursion, no extra memory
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode cut(ListNode head, int size) {          // cut after 'size' nodes
    for (int i = 0; head != null && i < size - 1; i++) head = head.next;
    if (head == null) return null;
    ListNode rest = head.next;
    head.next = null;
    return rest;
}
ListNode mergeInto(ListNode tail, ListNode a, ListNode b) {
    while (a != null && b != null) {
        if (a.val <= b.val) { tail.next = a; a = a.next; }
        else { tail.next = b; b = b.next; }
        tail = tail.next;
    }
    tail.next = (a != null) ? a : b;
    while (tail.next != null) tail = tail.next;  // tail ends at the last node
    return tail;
}
ListNode sortList(ListNode head) {
    int n = 0; for (ListNode p = head; p != null; p = p.next) n++;
    ListNode dummy = new ListNode(0); dummy.next = head;
    for (int size = 1; size < n; size *= 2) {    // log n passes
        ListNode tail = dummy, cur = dummy.next;
        while (cur != null) {                    // merge this pass, run by run
            ListNode left = cur;
            ListNode right = cut(left, size);
            cur = cut(right, size);
            tail = mergeInto(tail, left, right);
        }
    }
    return dummy.next;
}   // O(n log n) time · O(1) space""",
            "python": r"""def sort_list(head):
    n = 0
    p = head
    while p:
        n += 1
        p = p.next

    def cut(node, size):             # cut after 'size' nodes, return the rest
        for _ in range(size - 1):
            if node:
                node = node.next
        if not node:
            return None
        rest, node.next = node.next, None
        return rest

    dummy = ListNode(0)
    dummy.next = head
    size = 1
    while size < n:                  # log n passes over the list
        tail, cur = dummy, dummy.next
        while cur:
            left = cur
            right = cut(left, size)
            cur = cut(right, size)
            while left and right:    # merge one pair of runs
                if left.val <= right.val:
                    tail.next, left = left, left.next
                else:
                    tail.next, right = right, right.next
                tail = tail.next
            tail.next = left or right
            while tail.next:         # tail must end at the last node
                tail = tail.next
        size *= 2
    return dummy.next""",
        },
    },
    {
        "slug": "design-skiplist",
        "title": "Design Skiplist",
        "difficulty": "Hard",
        "pattern": "probabilistic layered lists",
        "statement": "Implement a skiplist with search(target), add(num) and erase(num), each in O(log n) expected time, and with no duplicates.",
        "examples": [("add 1, add 2, add 3, search(0), add 4, search(1)", "false, then true"),
                     ("erase(0), erase(1), search(1)", "false, true, false")],
        "constraints": ["0 <= num <= 10^4", "up to 5 * 10^4 calls", "the judge's values are distinct", "level 1 must always be a complete sorted list"],
        "approach": "Every node carries a tower of forward pointers, and each extra level is added with probability 1/2 when the node is created. "
                     "Searching drops down whenever the next node would overshoot, so the expected path length is logarithmic without any "
                     "rebalancing. Erase unlinks the node from every level of its own tower — keeping track of the predecessor at each level "
                     "during the search is what makes that possible.",
        "complexity": ("O(log n) expected per op", "O(n) expected"),
        "code": {
            "cpp": r"""// Towers of forward pointers; each extra level appears with probability 1/2
const int MAXLEVEL = 16;
struct SNode {
    int val; vector<SNode*> next;
    SNode(int v, int lvl) : val(v), next(lvl, nullptr) {}
};
class Skiplist {
    SNode* head = new SNode(-1, MAXLEVEL);
    int level = 1;
    int randomLevel() {
        int lvl = 1;
        while (lvl < MAXLEVEL && rand() % 2) lvl++;      // coin flips
        return lvl;
    }
public:
    bool search(int target) {
        SNode* cur = head;
        for (int i = level - 1; i >= 0; i--) {
            while (cur->next[i] && cur->next[i]->val < target) cur = cur->next[i];
        }
        cur = cur->next[0];
        return cur && cur->val == target;
    }
    void add(int num) {
        vector<SNode*> update(MAXLEVEL, head);           // predecessor per level
        SNode* cur = head;
        for (int i = level - 1; i >= 0; i--) {
            while (cur->next[i] && cur->next[i]->val < num) cur = cur->next[i];
            update[i] = cur;
        }
        int lvl = randomLevel();
        level = max(level, lvl);                         // grow if the tower is tall
        SNode* node = new SNode(num, lvl);
        for (int i = 0; i < lvl; i++) {
            node->next[i] = update[i]->next[i];
            update[i]->next[i] = node;
        }
    }
    bool erase(int num) {
        vector<SNode*> update(MAXLEVEL, head);
        SNode* cur = head;
        for (int i = level - 1; i >= 0; i--) {
            while (cur->next[i] && cur->next[i]->val < num) cur = cur->next[i];
            update[i] = cur;
        }
        SNode* target = cur->next[0];
        if (!target || target->val != num) return false;
        for (int i = 0; i < (int)target->next.size(); i++)
            if (update[i]->next[i] == target) update[i]->next[i] = target->next[i];
        while (level > 1 && !head->next[level - 1]) level--;   // shrink empty top
        return true;
    }
};   // O(log n) expected per op · O(n) expected space""",
            "java": r"""// Towers of forward pointers; each extra level appears with probability 1/2
class Skiplist {
    private static final int MAXLEVEL = 16;      // constant: legal in an inner class
    class SNode {
        int val; SNode[] next;
        SNode(int v, int lvl) { val = v; next = new SNode[lvl]; }
    }
    private final SNode head = new SNode(-1, MAXLEVEL);
    private int level = 1;
    private final Random rnd = new Random();
    private int randomLevel() {
        int lvl = 1;
        while (lvl < MAXLEVEL && rnd.nextBoolean()) lvl++;   // coin flips
        return lvl;
    }
    public boolean search(int target) {
        SNode cur = head;
        for (int i = level - 1; i >= 0; i--)
            while (cur.next[i] != null && cur.next[i].val < target) cur = cur.next[i];
        cur = cur.next[0];
        return cur != null && cur.val == target;
    }
    public void add(int num) {
        SNode[] update = new SNode[MAXLEVEL];                // predecessor per level
        SNode cur = head;
        for (int i = level - 1; i >= 0; i--) {
            while (cur.next[i] != null && cur.next[i].val < num) cur = cur.next[i];
            update[i] = cur;
        }
        int lvl = randomLevel();
        level = Math.max(level, lvl);                        // grow if taller
        SNode node = new SNode(num, lvl);
        for (int i = 0; i < lvl; i++) {
            node.next[i] = update[i].next[i];
            update[i].next[i] = node;
        }
    }
    public boolean erase(int num) {
        SNode[] update = new SNode[MAXLEVEL];
        SNode cur = head;
        for (int i = level - 1; i >= 0; i--) {
            while (cur.next[i] != null && cur.next[i].val < num) cur = cur.next[i];
            update[i] = cur;
        }
        SNode target = cur.next[0];
        if (target == null || target.val != num) return false;
        for (int i = 0; i < target.next.length; i++)
            if (update[i].next[i] == target) update[i].next[i] = target.next[i];
        while (level > 1 && head.next[level - 1] == null) level--;   // shrink
        return true;
    }
}   // O(log n) expected per op · O(n) expected space""",
            "python": r"""import random

MAXLEVEL = 16

class SNode:
    __slots__ = ('val', 'nxt')

    def __init__(self, val, lvl):
        self.val = val
        self.nxt = [None] * lvl          # one forward pointer per level

class Skiplist:
    def __init__(self):
        self.head = SNode(-1, MAXLEVEL)
        self.level = 1

    def _random_level(self):
        lvl = 1
        while lvl < MAXLEVEL and random.random() < 0.5:
            lvl += 1                     # each extra level is a coin flip
        return lvl

    def search(self, target):
        cur = self.head
        for i in range(self.level - 1, -1, -1):
            while cur.nxt[i] and cur.nxt[i].val < target:
                cur = cur.nxt[i]         # drop down when the next node overshoots
        cur = cur.nxt[0]
        return bool(cur) and cur.val == target

    def add(self, num):
        update = [self.head] * MAXLEVEL  # predecessor at each level
        cur = self.head
        for i in range(self.level - 1, -1, -1):
            while cur.nxt[i] and cur.nxt[i].val < num:
                cur = cur.nxt[i]
            update[i] = cur
        lvl = self._random_level()
        self.level = max(self.level, lvl)
        node = SNode(num, lvl)
        for i in range(lvl):
            node.nxt[i] = update[i].nxt[i]
            update[i].nxt[i] = node

    def erase(self, num):
        update = [self.head] * MAXLEVEL
        cur = self.head
        for i in range(self.level - 1, -1, -1):
            while cur.nxt[i] and cur.nxt[i].val < num:
                cur = cur.nxt[i]
            update[i] = cur
        target = cur.nxt[0]
        if not target or target.val != num:
            return False
        for i in range(len(target.nxt)):
            if update[i].nxt[i] is target:
                update[i].nxt[i] = target.nxt[i]
        while self.level > 1 and not self.head.nxt[self.level - 1]:
            self.level -= 1              # shrink an empty top level
        return True""",
        },
    },
    {
        "slug": "reverse-nodes-in-even-length-groups",
        "title": "Reverse Nodes in Even Length Groups",
        "difficulty": "Hard",
        "pattern": "growing group sizes",
        "statement": "Group the nodes into sizes 1, 2, 3, 4, ... (the last group may be shorter) and reverse each group whose size is even. Return "
                     "the head.",
        "examples": [("head = 5 -> 2 -> 6 -> 3 -> 9 -> 1 -> 7 -> 3 -> 8 -> 4", "5 -> 6 -> 2 -> 3 -> 9 -> 1 -> 4 -> 8 -> 3 -> 7"),
                     ("head = 1 -> 1 -> 0 -> 6", "1 -> 0 -> 1 -> 6")],
        "constraints": ["1 <= number of nodes <= 10^5", "0 <= node values <= 10^9", "only the links may change"],
        "approach": "Walk group by group with a group index, count how many nodes the group actually contains (the last one may be short), and "
                     "reverse in place only when that count is even. Reusing the head-insertion reversal from the k-group problem keeps this "
                     "short — the new difficulty is that the group size is discovered rather than given.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Groups of size 1,2,3,...; reverse only the ones whose real size is even
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
ListNode* reverseEvenLengthGroups(ListNode* head) {
    ListNode dummy(0); dummy.next = head;
    ListNode* prev = &dummy;
    int size = 1;
    while (prev->next) {
        ListNode* groupStart = prev->next;
        int count = 0; ListNode* probe = groupStart;
        while (probe && count < size) { probe = probe->next; count++; }   // real size
        if (count % 2 == 0) {                            // even: reverse in place
            ListNode* cur = groupStart;
            for (int i = 1; i < count; i++) {            // head-insert each node
                ListNode* nxt = cur->next;
                cur->next = nxt->next;
                nxt->next = prev->next;
                prev->next = nxt;
            }
        }
        for (int i = 0; i < count; i++) prev = prev->next;   // skip the group
        size++;
    }
    return dummy.next;
}   // O(n) time · O(1) space""",
            "java": r"""// Groups of size 1,2,3,...; reverse only the ones whose real size is even
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode reverseEvenLengthGroups(ListNode head) {
    ListNode dummy = new ListNode(0); dummy.next = head;
    ListNode prev = dummy;
    int size = 1;
    while (prev.next != null) {
        ListNode groupStart = prev.next;
        int count = 0; ListNode probe = groupStart;
        while (probe != null && count < size) { probe = probe.next; count++; }   // real size
        if (count % 2 == 0) {                            // even: reverse in place
            ListNode cur = groupStart;
            for (int i = 1; i < count; i++) {            // head-insert each node
                ListNode nxt = cur.next;
                cur.next = nxt.next;
                nxt.next = prev.next;
                prev.next = nxt;
            }
        }
        for (int i = 0; i < count; i++) prev = prev.next;   // skip the group
        size++;
    }
    return dummy.next;
}   // O(n) time · O(1) space""",
            "python": r"""def reverse_even_length_groups(head):
    dummy = ListNode(0)
    dummy.next = head
    prev, size = dummy, 1
    while prev.next:
        start = prev.next
        count, probe = 0, start
        while probe and count < size:      # discover the group's real size
            probe, count = probe.next, count + 1
        if count % 2 == 0:                 # even groups are reversed
            cur = start
            for _ in range(count - 1):     # head-insert each node
                nxt = cur.next
                cur.next = nxt.next
                nxt.next = prev.next
                prev.next = nxt
        for _ in range(count):             # step past this group
            prev = prev.next
        size += 1
    return dummy.next""",
        },
    },
    {
        "slug": "design-a-text-editor",
        "title": "Design a Text Editor",
        "difficulty": "Hard",
        "pattern": "two stacks around a cursor",
        "statement": "Support addText(text), deleteText(k) (returns how many characters were deleted), cursorLeft(k), cursorRight(k) and getText() "
                     "(up to the last 10 characters before the cursor). All operations must be fast.",
        "examples": [("addText(\"leetcode\"), deleteText(4), addText(\"practice\"), cursorRight(3)", "4, then \"etpractice\""),
                     ("cursorLeft(8), deleteText(10), cursorLeft(2), cursorRight(6)", "\"leet\", 4, \"\", \"practi\""),],
        "constraints": ["up to 10^4 calls", "text contains lowercase letters", "at most 2 * 10^5 characters are ever added"],
        "approach": "Represent the document as two stacks: characters before the cursor and characters after it. Every operation then touches only "
                     "the tops — adding pushes onto the left stack, deleting pops from it, and moving the cursor shifts characters between the "
                     "two. getText is the only partial read, and it is capped at ten characters.",
        "complexity": ("O(1) per character touched", "O(total text)"),
        "code": {
            "cpp": r"""// Two stacks meeting at the cursor: left = before, right = after
class TextEditor {
    deque<char> left, right;                     // top of each stack is at the cursor
public:
    void addText(string text) {
        for (char c : text) left.push_back(c);
    }
    int deleteText(int k) {
        int deleted = 0;
        while (k-- > 0 && !left.empty()) { left.pop_back(); deleted++; }
        return deleted;
    }
    string cursorLeft(int k) {
        while (k-- > 0 && !left.empty()) { right.push_back(left.back()); left.pop_back(); }
        return tail();
    }
    string cursorRight(int k) {
        while (k-- > 0 && !right.empty()) { left.push_back(right.back()); right.pop_back(); }
        return tail();
    }
    string getText() { return tail(); }
private:
    string tail() {                              // last <= 10 characters before cursor
        string s;
        int take = min<size_t>(10, left.size());
        for (size_t i = left.size() - take; i < left.size(); i++) s += left[i];
        return s;
    }
};   // O(k) per cursor move · O(total text) space""",
            "java": r"""// Two deques meeting at the cursor: left = before, right = after
class TextEditor {
    private final Deque<Character> left = new ArrayDeque<>(), right = new ArrayDeque<>();

    public void addText(String text) {
        for (char c : text.toCharArray()) left.addLast(c);
    }
    public int deleteText(int k) {
        int deleted = 0;
        while (k-- > 0 && !left.isEmpty()) { left.pollLast(); deleted++; }
        return deleted;
    }
    public String cursorLeft(int k) {
        while (k-- > 0 && !left.isEmpty()) right.addLast(left.pollLast());
        return tail();
    }
    public String cursorRight(int k) {
        while (k-- > 0 && !right.isEmpty()) left.addLast(right.pollLast());
        return tail();
    }
    public String getText() { return tail(); }
    private String tail() {                      // last <= 10 before the cursor
        StringBuilder sb = new StringBuilder();
        int take = Math.min(10, left.size());
        Iterator<Character> it = left.descendingIterator();   // back to front
        for (int i = 0; i < take; i++) sb.append(it.next());
        return sb.reverse().toString();
    }
}   // O(k) per cursor move · O(total text) space""",
            "python": r"""class TextEditor:
    def __init__(self):
        self.left = []           # characters before the cursor, end = at cursor
        self.right = []          # characters after the cursor, end = at cursor

    def add_text(self, text):
        self.left.extend(text)   # every operation touches only a stack top

    def delete_text(self, k):
        deleted = 0
        while k > 0 and self.left:
            self.left.pop()
            deleted += 1
            k -= 1
        return deleted

    def cursor_left(self, k):
        while k > 0 and self.left:
            self.right.append(self.left.pop())
            k -= 1
        return self._tail()

    def cursor_right(self, k):
        while k > 0 and self.right:
            self.left.append(self.right.pop())
            k -= 1
        return self._tail()

    def get_text(self):
        return self._tail()

    def _tail(self):
        return ''.join(self.left[-10:])   # at most ten characters""",
        },
    },
    {
        "slug": "flatten-multilevel-linked-list-o1",
        "title": "Flatten a Multilevel List in O(1) Space",
        "difficulty": "Hard",
        "pattern": "in-place splicing without a stack",
        "statement": "Flatten a multilevel doubly linked list using O(1) additional memory — no stack and no recursion.",
        "examples": [("1 - 2 - 3 with child 7 - 8 on 3", "1 - 2 - 3 - 7 - 8"),
                     ("nested children three levels deep", "all nodes in depth-first order")],
        "constraints": ["0 <= number of nodes <= 1000", "extra space must be O(1)", "the doubly linked pointers must stay consistent"],
        "approach": "For each node with a child, walk to the child's last node and sew it onto the parent's next pointer, then splice the child "
                     "chain in. Nothing is stored — but the tail walk is repeated for every child encountered, which is exactly the trade-off "
                     "against the stack version: constant space, and time that degrades for deeply nested chains.",
        "complexity": ("O(n) typical, O(n²) worst case", "O(1)"),
        "code": {
            "cpp": r"""// Splice each child in by walking to its tail: no stack, no recursion
struct Node { int val; Node *prev, *next, *child; Node(int v) : val(v), prev(nullptr), next(nullptr), child(nullptr) {} };
Node* flatten(Node* head) {
    for (Node* cur = head; cur; cur = cur->next) {
        if (!cur->child) continue;
        Node* child = cur->child;
        while (child->next) child = child->next;     // child chain's tail
        Node* nxt = cur->next;
        child->next = nxt;                           // sew child tail to the rest
        if (nxt) nxt->prev = child;
        cur->next = cur->child;                      // splice the child in
        cur->child->prev = cur;
        cur->child = nullptr;                        // the child pointer is consumed
    }
    return head;
}   // O(n) typical, O(n²) worst time · O(1) space""",
            "java": r"""// Splice each child in by walking to its tail: no stack, no recursion
class Node { int val; Node prev, next, child; Node(int v) { val = v; } }
Node flatten(Node head) {
    for (Node cur = head; cur != null; cur = cur.next) {
        if (cur.child == null) continue;
        Node child = cur.child;
        while (child.next != null) child = child.next;   // child chain's tail
        Node nxt = cur.next;
        child.next = nxt;                                // sew tail to the rest
        if (nxt != null) nxt.prev = child;
        cur.next = cur.child;                            // splice the child in
        cur.child.prev = cur;
        cur.child = null;                                // consumed
    }
    return head;
}   // O(n) typical, O(n²) worst time · O(1) space""",
            "python": r"""def flatten_o1(head):
    cur = head
    while cur:
        if cur.child:
            child = cur.child
            while child.next:            # walk to the child chain's tail
                child = child.next
            nxt = cur.next
            child.next = nxt             # sew the tail onto the rest of the list
            if nxt:
                nxt.prev = child
            cur.next = cur.child         # splice the child chain in
            cur.child.prev = cur
            cur.child = None             # the child pointer is consumed
        cur = cur.next
    return head""",
        },
    },
    {
        "slug": "copy-list-with-random-pointer-o1",
        "title": "Copy a Random-Pointer List in O(1) Space",
        "difficulty": "Hard",
        "pattern": "interleave copies with originals",
        "statement": "Deep-copy a list whose nodes have next and random pointers, using O(1) extra memory.",
        "examples": [("[[7,null],[13,0],[11,4],[10,2],[1,0]]", "an identical independent list"),
                     ("[[1,1],[2,1]]", "an identical independent list")],
        "constraints": ["0 <= number of nodes <= 1000", "extra space must be O(1)", "the original list must stay usable"],
        "approach": "Weave the copies into the original list as A -> A' -> B -> B', so every copy sits right after its original and `random` becomes "
                     "`original->random->next`. Then unweave the two interleaved lists. The doubled list *is* the lookup table — that is the whole "
                     "trick, and it is why no hash map is needed.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Weave A->A'->B->B', point randoms, then unweave
struct Node { int val; Node *next, *random; Node(int v) : val(v), next(nullptr), random(nullptr) {} };
Node* copyRandomList(Node* head) {
    for (Node* p = head; p; p = p->next->next) {      // 1. weave in the copies
        Node* c = new Node(p->val);
        c->next = p->next;
        p->next = c;
    }
    for (Node* p = head; p; p = p->next->next)        // 2. fix random pointers
        if (p->random) p->next->random = p->random->next;
    Node dummy(0), *tail = &dummy;
    for (Node* p = head; p; ) {                       // 3. unweave
        Node* c = p->next;
        p->next = c->next;                            // restore the original
        tail->next = c; tail = c;
        p = p->next;
    }
    tail->next = nullptr;
    return dummy.next;
}   // O(n) time · O(1) space""",
            "java": r"""// Weave A->A'->B->B', point randoms, then unweave
class Node { int val; Node next, random; Node(int v) { val = v; } }
Node copyRandomList(Node head) {
    for (Node p = head; p != null; p = p.next.next) {   // 1. weave in the copies
        Node c = new Node(p.val);
        c.next = p.next;
        p.next = c;
    }
    for (Node p = head; p != null; p = p.next.next)     // 2. fix random pointers
        if (p.random != null) p.next.random = p.random.next;
    Node dummy = new Node(0), tail = dummy;
    for (Node p = head; p != null; ) {                  // 3. unweave
        Node c = p.next;
        p.next = c.next;                                // restore the original
        tail.next = c; tail = c;
        p = p.next;
    }
    tail.next = null;
    return dummy.next;
}   // O(n) time · O(1) space""",
            "python": r"""def copy_random_list_o1(head):
    p = head
    while p:                          # 1. weave: A -> A' -> B -> B'
        c = Node(p.val)
        c.next = p.next
        p.next = c
        p = c.next
    p = head
    while p:                          # 2. randoms: original.random.next is the copy
        if p.random:
            p.next.random = p.random.next
        p = p.next.next
    dummy = tail = Node(0)
    p = head
    while p:                          # 3. unweave the two lists
        c = p.next
        p.next = c.next               # restore the original list
        tail.next = c
        tail = c
        p = p.next
    tail.next = None
    return dummy.next""",
        },
    },
    {
        "slug": "reverse-linked-list-ii",
        "title": "Reverse a Section of a List",
        "difficulty": "Hard",
        "pattern": "one-pass head insertion",
        "statement": "Reverse the nodes between positions left and right (1-indexed) in a single pass with O(1) extra space, and return the head.",
        "examples": [("head = 1 -> 2 -> 3 -> 4 -> 5, left = 2, right = 4", "1 -> 4 -> 3 -> 2 -> 5"), ("head = 5, left = 1, right = 1", "5")],
        "constraints": ["1 <= number of nodes <= 500", "1 <= left <= right <= number of nodes", "only the links may change"],
        "approach": "Walk to the node before `left` and then repeatedly lift the node after it to the front of the section: after right-left "
                     "liftings the section is reversed, and the node before `left` never moves — which is why the loop needs no position "
                     "bookkeeping and works for left = 1 with a dummy head.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Lift the node after 'prev' to the front of the section, right-left times
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
ListNode* reverseBetween(ListNode* head, int left, int right) {
    ListNode dummy(0); dummy.next = head;
    ListNode* prev = &dummy;
    for (int i = 1; i < left; i++) prev = prev->next;      // node before the section
    ListNode* cur = prev->next;                            // stays the section's tail
    for (int i = 0; i < right - left; i++) {
        ListNode* nxt = cur->next;
        cur->next = nxt->next;                             // detach nxt
        nxt->next = prev->next;                            // lift it to the front
        prev->next = nxt;
    }
    return dummy.next;
}   // O(n) time · O(1) space""",
            "java": r"""// Lift the node after 'prev' to the front of the section, right-left times
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
ListNode reverseBetween(ListNode head, int left, int right) {
    ListNode dummy = new ListNode(0); dummy.next = head;
    ListNode prev = dummy;
    for (int i = 1; i < left; i++) prev = prev.next;       // node before the section
    ListNode cur = prev.next;                              // stays the section's tail
    for (int i = 0; i < right - left; i++) {
        ListNode nxt = cur.next;
        cur.next = nxt.next;                               // detach nxt
        nxt.next = prev.next;                               // lift it to the front
        prev.next = nxt;
    }
    return dummy.next;
}   // O(n) time · O(1) space""",
            "python": r"""def reverse_between(head, left, right):
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    for _ in range(left - 1):        # node just before the section
        prev = prev.next
    cur = prev.next                  # cur stays the section's tail
    for _ in range(right - left):
        nxt = cur.next
        cur.next = nxt.next          # detach nxt
        nxt.next = prev.next         # lift it to the front of the section
        prev.next = nxt
    return dummy.next""",
        },
    },
    {
        "slug": "next-greater-node-in-linked-list",
        "title": "Next Greater Node in a Linked List",
        "difficulty": "Hard",
        "pattern": "monotonic stack over list indices",
        "statement": "Return an array where the i-th value is the value of the first node after node i that has a strictly greater value, or 0 if "
                     "there is none.",
        "examples": [("head = 2 -> 1 -> 5", "[5,5,0]"), ("head = 2 -> 7 -> 4 -> 3 -> 5", "[7,0,5,5,0]")],
        "constraints": ["1 <= number of nodes <= 10^4", "1 <= node values <= 10^9", "the array is indexed by node position from the head"],
        "approach": "The list has no random access, so copy the values into an array (or keep a monotonic stack of node pointers) and apply the "
                     "next-greater-element pass from the stack topic: keep a decreasing stack of indices, and every new value resolves all "
                     "smaller values waiting on top. Each node is pushed and popped once, so the pass is linear.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// Same decreasing stack as in arrays, over a list's indices
struct ListNode { int val; ListNode* next; ListNode(int v = 0) : val(v), next(nullptr) {} };
vector<int> nextLargerNodes(ListNode* head) {
    vector<int> vals;
    for (ListNode* p = head; p; p = p->next) vals.push_back(p->val);
    vector<int> ans(vals.size(), 0), st;          // decreasing stack of indices
    for (int i = 0; i < (int)vals.size(); i++) {
        while (!st.empty() && vals[st.back()] < vals[i]) {
            ans[st.back()] = vals[i];             // first greater value to the right
            st.pop_back();
        }
        st.push_back(i);
    }
    return ans;
}   // O(n) time · O(n) space""",
            "java": r"""// Same decreasing stack as in arrays, over a list's indices
class ListNode { int val; ListNode next; ListNode(int v) { val = v; } }
int[] nextLargerNodes(ListNode head) {
    List<Integer> vals = new ArrayList<>();
    for (ListNode p = head; p != null; p = p.next) vals.add(p.val);
    int[] ans = new int[vals.size()];
    Deque<Integer> st = new ArrayDeque<>();       // decreasing stack of indices
    for (int i = 0; i < vals.size(); i++) {
        while (!st.isEmpty() && vals.get(st.peek()) < vals.get(i)) {
            ans[st.pop()] = vals.get(i);          // first greater value to the right
        }
        st.push(i);
    }
    return ans;
}   // O(n) time · O(n) space""",
            "python": r"""def next_larger_nodes(head):
    vals = []
    p = head
    while p:
        vals.append(p.val)
        p = p.next
    ans = [0] * len(vals)
    st = []                            # decreasing stack of indices
    for i, v in enumerate(vals):
        while st and vals[st[-1]] < v:
            ans[st.pop()] = v          # first greater value to the right
        st.append(i)
    return ans""",
        },
    },
]
