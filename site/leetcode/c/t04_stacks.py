# Topic 4 · Stacks, Queues & Monotonic Structures — C17 solutions
CODE = {
    "valid-parentheses": r"""
// A stack of the opening brackets: every closer must match the top.
int isValid(const char *s) {
    char stack[4096];
    int top = 0;
    for (int i = 0; s[i]; i++) {
        char c = s[i];
        if (c == '(' || c == '[' || c == '{') stack[top++] = c;
        else {
            if (top == 0) return 0;                       // a closer with nothing to close
            char open = stack[--top];
            if ((c == ')' && open != '(') || (c == ']' && open != '[') || (c == '}' && open != '{'))
                return 0;                                 // wrong type
        }
    }
    return top == 0;                                      // false when something stayed open
}   // O(n) time · O(n) space
""",
    "min-stack": r"""
// Each slot remembers the minimum of everything below it, so getMin is O(1).
typedef struct {
    int values[4096], mins[4096], top;
} MinStack;

MinStack *minStackCreate(void) { return calloc(1, sizeof(MinStack)); }

void minStackPush(MinStack *s, int val) {
    s->values[s->top] = val;
    s->mins[s->top] = s->top && s->mins[s->top - 1] < val ? s->mins[s->top - 1] : val;
    s->top++;
}

void minStackPop(MinStack *s) { if (s->top) s->top--; }
int minStackTop(MinStack *s) { return s->values[s->top - 1]; }
int minStackGetMin(MinStack *s) { return s->mins[s->top - 1]; }
// every operation is O(1) · O(n) space
""",
    "baseball-game": r"""
// A record list: numbers are scores, the letters replay earlier rounds.
int calPoints(char **ops, int n) {
    int *stack = malloc(sizeof(int) * (size_t) n);
    int top = 0, total = 0;
    for (int i = 0; i < n; i++) {
        if (!strcmp(ops[i], "C")) total -= stack[--top];                  // drop the last score
        else if (!strcmp(ops[i], "D")) { stack[top] = stack[top - 1] * 2; total += stack[top++]; }
        else if (!strcmp(ops[i], "+")) { stack[top] = stack[top - 1] + stack[top - 2]; total += stack[top++]; }
        else { stack[top] = atoi(ops[i]); total += stack[top++]; }
    }
    free(stack);
    return total;
}   // O(n) time · O(n) space
""",
    "queue-using-stacks": r"""
// One stack for input and one for output: the output stack reverses the order.
typedef struct { int in[1024], out[1024], inTop, outTop; } MyQueue;

MyQueue *myQueueCreate(void) { return calloc(1, sizeof(MyQueue)); }

void myQueuePush(MyQueue *q, int x) { q->in[q->inTop++] = x; }

static void queueShift(MyQueue *q) {
    while (q->inTop) q->out[q->outTop++] = q->in[--q->inTop];
}

int myQueuePop(MyQueue *q) {
    if (!q->outTop) queueShift(q);
    return q->out[--q->outTop];
}

int myQueuePeek(MyQueue *q) {
    if (!q->outTop) queueShift(q);
    return q->out[q->outTop - 1];
}

int myQueueEmpty(MyQueue *q) { return q->inTop == 0 && q->outTop == 0; }
// amortised O(1) per operation · O(n) space
""",
    "backspace-string-compare": r"""
// Walk both strings backwards so a '#' deletes the character to its left.
static int nextIndex(const char *s, int i) {
    int skip = 0;
    while (i >= 0) {
        if (s[i] == '#') { skip++; i--; }
        else if (skip) { skip--; i--; }
        else break;
    }
    return i;
}

int backspaceCompare(const char *s, const char *t) {
    int i = (int) strlen(s) - 1, j = (int) strlen(t) - 1;
    while (i >= 0 || j >= 0) {
        i = nextIndex(s, i);
        j = nextIndex(t, j);
        if (i < 0 && j < 0) return 1;                     // both exhausted: equal
        if (i < 0 || j < 0) return 0;
        if (s[i] != t[j]) return 0;
        i--; j--;
    }
    return 1;
}   // O(n + m) time · O(1) space
""",
    "next-greater-element-i": r"""
// The next greater element for every value of nums2, kept in an index map.
int *nextGreaterElement(const int *a, int n, const int *b, int m, int *out, int *outSize) {
    for (int i = 0; i < n; i++) {
        out[i] = -1;
        for (int j = 0; j < m; j++)
            if (b[j] == a[i]) {
                for (int k = j + 1; k < m; k++)
                    if (b[k] > a[i]) { out[i] = b[k]; break; }
                break;
            }
    }
    *outSize = n;
    return out;
}   // O(n * m) time · O(1) extra space (a monotonic stack gives O(n + m))
""",
    "daily-temperatures": r"""
// Monotonic decreasing stack of indices: a warmer day resolves everything below it.
void dailyTemperatures(const int *t, int n, int *out) {
    int *stack = malloc(sizeof(int) * (size_t) n);
    int top = 0;
    for (int i = 0; i < n; i++) {
        while (top && t[i] > t[stack[top - 1]]) {
            int j = stack[--top];
            out[j] = i - j;                               // how many days until it got warmer
        }
        stack[top++] = i;
    }
    while (top) out[stack[--top]] = 0;
    free(stack);
}   // O(n) time · O(n) space
""",
    "evaluate-reverse-polish-notation": r"""
// Push numbers, pop two for every operator.
int evalRPN(char **tokens, int n) {
    int *stack = malloc(sizeof(int) * (size_t) n);
    int top = 0;
    for (int i = 0; i < n; i++) {
        const char *t = tokens[i];
        if (!strcmp(t, "+") || !strcmp(t, "-") || !strcmp(t, "*") || !strcmp(t, "/")) {
            int b = stack[--top], a = stack[--top];
            stack[top++] = t[0] == '+' ? a + b : t[0] == '-' ? a - b : t[0] == '*' ? a * b : a / b;
        } else stack[top++] = atoi(t);
    }
    int result = stack[top - 1];
    free(stack);
    return result;
}   // O(n) time · O(n) space
""",
    "decode-string": r"""
// Two stacks: one for repeat counts, one for the strings built so far.
char *decodeString(const char *s) {
    int counts[256], top = 0;
    char *parts[256];
    parts[0] = calloc(1, 4096);
    size_t cap[256] = {0};
    for (size_t i = 0; i < 256; i++) { parts[i] = calloc(1, 4096); cap[i] = 4096; }
    for (int i = 0; s[i]; ) {
        if (isdigit((unsigned char) s[i])) {
            int k = 0;
            while (isdigit((unsigned char) s[i])) k = k * 10 + (s[i++] - '0');
            counts[top] = k;
        } else if (s[i] == '[') {
            top++;
            strcpy(parts[top], "");
            i++;
        } else if (s[i] == ']') {
            char *inner = strdup(parts[top]);
            int k = counts[top - 1];
            top--;
            for (int r = 0; r < k; r++) strcat(parts[top], inner);
            free(inner);
            i++;
        } else {
            size_t len = strlen(parts[top]);
            parts[top][len] = s[i];
            parts[top][len + 1] = '\0';
            i++;
        }
    }
    return parts[0];
}   // O(n * repeats) time · O(n) space
""",
    "simplify-path": r"""
// Split on '/', keep a stack of directory names, and apply ".." by popping.
char *simplifyPath(const char *path) {
    char *stack[1024];
    int top = 0;
    char *copy = strdup(path);
    for (char *tok = strtok(copy, "/"); tok; tok = strtok(NULL, "/")) {
        if (!strcmp(tok, ".")) continue;
        if (!strcmp(tok, "..")) { if (top) free(stack[--top]); continue; }
        stack[top++] = strdup(tok);
    }
    char *out = calloc(1, strlen(path) + 2);
    out[0] = '\0';
    if (!top) strcpy(out, "/");
    for (int i = 0; i < top; i++) { strcat(out, "/"); strcat(out, stack[i]); free(stack[i]); }
    free(copy);
    return out;
}   // O(n) time · O(n) space
""",
    "next-greater-element-ii": r"""
// Same monotonic stack, but the array is walked twice to handle the wrap-around.
void nextGreaterElements(const int *a, int n, int *out) {
    int *stack = malloc(sizeof(int) * (size_t) (2 * n + 1));
    int top = 0;
    for (int i = 0; i < n; i++) out[i] = -1;
    for (int i = 0; i < 2 * n; i++) {
        int v = a[i % n];
        while (top && a[stack[top - 1]] < v) out[stack[--top]] = v;
        if (i < n) stack[top++] = i;                      // indices only from the first pass
    }
    free(stack);
}   // O(n) time · O(n) space
""",
    "online-stock-span": r"""
// Stack of (price, span): pop every smaller price and add its span.
int *stockSpan(const int *prices, int n, int *out, int *outSize) {
    int *stackPrice = malloc(sizeof(int) * (size_t) n);
    int top = 0;
    for (int i = 0; i < n; i++) {
        int span = 1;
        while (top && stackPrice[top - 1] <= prices[i]) span += out[--top];   // absorb smaller days
        out[i] = span;
        stackPrice[top] = prices[i];
        top++;
    }
    free(stackPrice);
    *outSize = n;
    return out;
}   // O(n) time · O(n) space
""",
    "remove-k-digits": r"""
// Greedy: drop a digit whenever the next one is smaller, at most k times.
char *removeKdigits(const char *num, int k) {
    int n = (int) strlen(num);
    char *stack = malloc((size_t) n + 1);
    int top = 0;
    for (int i = 0; i < n; i++) {
        while (k && top && stack[top - 1] > num[i]) { top--; k--; }        // remove the bigger digit
        stack[top++] = num[i];
    }
    top -= k;                                             // remaining removals come off the end
    if (top < 0) top = 0;
    int start = 0;
    while (start < top && stack[start] == '0') start++;   // no leading zeros
    char *out = malloc((size_t) (top - start) + 1);
    memcpy(out, stack + start, (size_t) (top - start));
    out[top - start] = '\0';
    if (!out[0]) strcpy(out, "0");
    free(stack);
    return out;
}   // O(n) time · O(n) space
""",
    "asteroid-collision": r"""
// Simulate the stack: a left-moving asteroid eats the right-moving ones in front of it.
int *asteroidCollision(const int *a, int n, int *out, int *outSize) {
    int top = 0;
    for (int i = 0; i < n; i++) {
        int v = a[i], alive = 1;
        while (alive && v < 0 && top && out[top - 1] > 0) {
            if (out[top - 1] < -v) top--;                 // the asteroid wins and keeps going
            else if (out[top - 1] == -v) { top--; alive = 0; }   // both explode
            else alive = 0;                               // the one on the stack survives
        }
        if (alive) out[top++] = v;
    }
    *outSize = top;
    return out;
}   // O(n) time · O(n) space
""",
    "design-circular-queue": r"""
// A fixed array plus head, size and capacity.
typedef struct {
    int *buf, cap, head, size;
} MyCircularQueue;

MyCircularQueue *myCircularQueueCreate(int k) {
    MyCircularQueue *q = calloc(1, sizeof(MyCircularQueue));
    q->buf = malloc(sizeof(int) * (size_t) k);
    q->cap = k;
    return q;
}

int myCircularQueueEnQueue(MyCircularQueue *q, int value) {
    if (q->size == q->cap) return 0;                      // full
    q->buf[(q->head + q->size) % q->cap] = value;
    q->size++;
    return 1;
}

int myCircularQueueDeQueue(MyCircularQueue *q) {
    if (!q->size) return 0;                               // empty
    q->head = (q->head + 1) % q->cap;
    q->size--;
    return 1;
}

int myCircularQueueFront(MyCircularQueue *q) { return q->size ? q->buf[q->head] : -1; }
int myCircularQueueRear(MyCircularQueue *q) { return q->size ? q->buf[(q->head + q->size - 1) % q->cap] : -1; }
int myCircularQueueIsEmpty(MyCircularQueue *q) { return q->size == 0; }
int myCircularQueueIsFull(MyCircularQueue *q) { return q->size == q->cap; }
// every operation is O(1) · O(k) space
""",
    "minimum-remove-to-make-valid": r"""
// First mark the unmatched ')' while scanning left to right, then the unmatched '('
// while scanning right to left; what is left is the answer.
char *minRemoveToMakeValid(const char *s) {
    int n = (int) strlen(s);
    char *out = strdup(s);
    int depth = 0, w = 0;
    for (int i = 0; i < n; i++) {
        if (s[i] == '(') depth++;
        else if (s[i] == ')') {
            if (!depth) continue;                         // this ')' has no partner — drop it
            depth--;
        }
        out[w++] = s[i];
    }
    int keep = w;
    depth = 0;
    for (int i = w - 1, k = w - 1; i >= 0; i--) {
        if (out[i] == ')') depth++;
        else if (out[i] == '(') {
            if (!depth) continue;                         // unmatched '(' — drop it
            depth--;
        }
        out[k--] = out[i];
    }
    out[keep] = '\0';
    return out;
}   // O(n) time · O(n) space
""",
    "sum-of-subarray-minimums": r"""
// Monotonic stack: the value at i is the minimum of (i - left) * (right - i) subarrays.
int sumSubarrayMins(const int *a, int n) {
    int *stack = malloc(sizeof(int) * (size_t) (n + 1));
    int *left = malloc(sizeof(int) * (size_t) n);
    int *right = malloc(sizeof(int) * (size_t) n);
    int top = 0;
    for (int i = 0; i < n; i++) {
        while (top && a[stack[top - 1]] >= a[i]) top--;    // >= keeps the earlier equal value
        left[i] = top ? i - stack[top - 1] : i + 1;
        stack[top++] = i;
    }
    top = 0;
    for (int i = n - 1; i >= 0; i--) {
        while (top && a[stack[top - 1]] > a[i]) top--;
        right[i] = top ? stack[top - 1] - i : n - i;
        stack[top++] = i;
    }
    long long total = 0;
    for (int i = 0; i < n; i++)
        total = (total + (long long) a[i] * left[i] % 1000000007 * right[i]) % 1000000007;
    free(stack); free(left); free(right);
    return (int) total;
}   // O(n) time · O(n) space
""",
    "car-fleet": r"""
// Sort by position and compare arrival times from the front of the road backwards.
struct Car { int pos, speed; };
static int cmpCar(const void *x, const void *y) { return ((const struct Car *) y)->pos - ((const struct Car *) x)->pos; }

int carFleet(int target, const int *position, const int *speed, int n) {
    struct Car *cars = malloc(sizeof(struct Car) * (size_t) n);
    for (int i = 0; i < n; i++) { cars[i].pos = position[i]; cars[i].speed = speed[i]; }
    qsort(cars, (size_t) n, sizeof(struct Car), cmpCar);
    int fleets = 0;
    double slowest = 0.0;
    for (int i = 0; i < n; i++) {
        double time = (double) (target - cars[i].pos) / cars[i].speed;
        if (time > slowest) { fleets++; slowest = time; }   // it cannot catch the fleet ahead
    }
    free(cars);
    return fleets;
}   // O(n log n) time · O(n) space
""",
    "largest-rectangle-in-histogram": r"""
// Monotonic increasing stack with a sentinel zero at the end.
long long largestRectangleArea(const int *h, int n) {
    int *stack = malloc(sizeof(int) * (size_t) (n + 2));
    int top = 0;
    long long best = 0;
    for (int i = 0; i <= n; i++) {
        int cur = (i == n) ? 0 : h[i];                    // the sentinel pops everything left
        while (top && h[stack[top - 1]] >= cur) {
            int height = h[stack[--top]];
            int left = top ? stack[top - 1] + 1 : 0;
            long long area = (long long) height * (i - left);
            if (area > best) best = area;
        }
        stack[top++] = i;
    }
    free(stack);
    return best;
}   // O(n) time · O(n) space
""",
    "maximal-rectangle": r"""
// One histogram per row: heights accumulate where the previous row had a '1'.
int maximalRectangle(char **matrix, int rows) {
    if (!rows) return 0;
    int cols = (int) strlen(matrix[0]);
    int *height = calloc((size_t) cols + 1, sizeof(int));
    int *stack = malloc(sizeof(int) * (size_t) (cols + 2));
    int best = 0;
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++)
            height[c] = matrix[r][c] == '1' ? height[c] + 1 : 0;
        int top = 0;
        for (int c = 0; c <= cols; c++) {
            int cur = c == cols ? 0 : height[c];
            while (top && height[stack[top - 1]] >= cur) {
                int hh = height[stack[--top]];
                int left = top ? stack[top - 1] + 1 : 0;
                int area = hh * (c - left);
                if (area > best) best = area;
            }
            stack[top++] = c;
        }
    }
    free(height); free(stack);
    return best;
}   // O(rows * cols) time · O(cols) space
""",
    "longest-valid-parentheses": r"""
// Stack of indices, starting with a base index of -1.
int longestValidParentheses(const char *s) {
    int n = (int) strlen(s);
    int *stack = malloc(sizeof(int) * (size_t) (n + 1));
    int top = 0, best = 0;
    stack[top++] = -1;                                    // base for the first valid run
    for (int i = 0; i < n; i++) {
        if (s[i] == '(') stack[top++] = i;
        else {
            top--;
            if (top == 0) stack[top++] = i;               // this ')' can never be matched
            else if (i - stack[top - 1] > best) best = i - stack[top - 1];
        }
    }
    free(stack);
    return best;
}   // O(n) time · O(n) space
""",
    "trapping-rain-water-stack": r"""
// Stack version: every time a taller bar appears it closes basins above the stack top.
long long trapStack(const int *h, int n) {
    int *stack = malloc(sizeof(int) * (size_t) (n + 1));
    int top = 0;
    long long water = 0;
    for (int i = 0; i < n; i++) {
        while (top && h[stack[top - 1]] < h[i]) {
            int bottom = h[stack[--top]];
            if (!top) break;
            int width = i - stack[top - 1] - 1;
            int height = (h[stack[top - 1]] < h[i] ? h[stack[top - 1]] : h[i]) - bottom;
            water += (long long) width * height;
        }
        stack[top++] = i;
    }
    free(stack);
    return water;
}   // O(n) time · O(n) space
""",
    "basic-calculator": r"""
// Sign, running result and the value inside the current parenthesis pair.
int calculate(const char *s) {
    int stack[1024], top = 0;
    long long result = 0, number = 0;
    int sign = 1;
    for (int i = 0; ; i++) {
        char c = s[i];
        if (isdigit((unsigned char) c)) number = number * 10 + (c - '0');
        else if (c == '+' || c == '-') {
            result += sign * number;
            number = 0;
            sign = c == '+' ? 1 : -1;
        } else if (c == '(') {
            stack[top++] = (int) result;
            stack[top++] = sign;
            result = 0;
            sign = 1;
        } else if (c == ')') {
            result += sign * number;
            number = 0;
            result *= stack[--top];                       // the sign before the bracket
            result += stack[--top];                       // what came before it
        } else if (c == '\0') {
            result += sign * number;
            break;
        }
    }
    return (int) result;
}   // O(n) time · O(n) space
""",
    "parsing-a-boolean-expression": r"""
// Recursive descent over the expression: '!' flips, '&' and '|' fold their operands.
static int evalBool(const char *e, int *i) {
    char c = e[*i];
    if (c == 't') { (*i)++; return 1; }
    if (c == 'f') { (*i)++; return 0; }
    (*i) += 2;                                            // skip "!(", "&(" or "|("
    int first = evalBool(e, i), result = first;
    while (e[*i] == ',') {
        (*i)++;
        int v = evalBool(e, i);
        if (c == '&') result = result && v;
        else if (c == '|') result = result || v;
    }
    (*i)++;                                               // skip ')'
    return c == '!' ? !result : result;
}

int parseBoolExpr(const char *expression) {
    int i = 0;
    return evalBool(expression, &i) ? 1 : 0;              // 1 = true, 0 = false
}   // O(n) time · O(depth) space
""",
    "number-of-atoms": r"""
// Stack of element counts per parenthesised group, then a sorted report.
typedef struct { char name[4]; int count; } Atom;

int countOfAtoms(const char *formula, Atom *out) {
    Atom groups[64][64];
    int sizes[64] = {0};
    int depth = 0;
    for (int i = 0; formula[i]; ) {
        char c = formula[i];
        if (c == '(') { depth++; sizes[depth] = 0; i++; continue; }
        if (c == ')') {
            i++;
            int mult = 0;
            while (isdigit((unsigned char) formula[i])) mult = mult * 10 + (formula[i++] - '0');
            if (!mult) mult = 1;
            for (int k = 0; k < sizes[depth]; k++) {
                Atom a = groups[depth][k];
                a.count *= mult;
                int found = 0;
                for (int m = 0; m < sizes[depth - 1] && !found; m++)
                    if (!strcmp(groups[depth - 1][m].name, a.name)) {
                        groups[depth - 1][m].count += a.count;   // merge into the outer group
                        found = 1;
                    }
                if (!found) groups[depth - 1][sizes[depth - 1]++] = a;
            }
            depth--;
            continue;
        }
        if (isupper((unsigned char) c)) {
            char name[4] = {c, 0, 0, 0};
            i++;
            if (islower((unsigned char) formula[i])) { name[1] = formula[i]; name[2] = 0; i++; }
            int count = 0;
            while (isdigit((unsigned char) formula[i])) count = count * 10 + (formula[i++] - '0');
            if (!count) count = 1;
            int found = 0;
            for (int m = 0; m < sizes[depth] && !found; m++)
                if (!strcmp(groups[depth][m].name, name)) { groups[depth][m].count += count; found = 1; }
            if (!found) {
                strcpy(groups[depth][sizes[depth]].name, name);
                groups[depth][sizes[depth]].count = count;
                sizes[depth]++;
            }
            continue;
        }
        i++;
    }
    for (int k = 0; k < sizes[0]; k++) out[k] = groups[0][k];    // already alphabetical
    return sizes[0];
}   // O(n * elements) time · O(depth * elements) space
""",
    "minimum-increments-to-form-target": r"""
// Every rise over the previous height needs its own increments.
int minNumberOperations(const int *target, int n) {
    long long total = 0;
    int prev = 0;
    for (int i = 0; i < n; i++) {
        if (target[i] > prev) total += target[i] - prev;
        prev = target[i];
    }
    return (int) total;
}   // O(n) time · O(1) space
""",
    "number-of-visible-people-in-a-queue": r"""
// Monotonic decreasing stack from the right: each person sees the taller ones and the
// first shorter-or-equal that ends their view.
int *canSeePersonsCount(const int *h, int n, int *out, int *outSize) {
    int *stack = malloc(sizeof(int) * (size_t) n);
    int top = 0;
    for (int i = n - 1; i >= 0; i--) {
        int seen = 0;
        while (top && h[stack[top - 1]] < h[i]) { top--; seen++; }   // everyone shorter
        if (top) seen++;                                            // plus the first taller one
        out[i] = seen;
        stack[top++] = i;
    }
    free(stack);
    *outSize = n;
    return out;
}   // O(n) time · O(n) space
""",
    "create-maximum-number": r"""
// Two greedy picks merged with a comparison that keeps the lexicographically larger tail.
static int *bestFrom(const int *a, int n, int k, int *outSize) {
    int *stack = malloc(sizeof(int) * (size_t) (k ? k : 1));
    int top = 0;
    for (int i = 0; i < n; i++) {
        while (top && n - i + top > k && stack[top - 1] < a[i]) top--;
        if (top < k) stack[top++] = a[i];
    }
    *outSize = top;
    return stack;
}

static int better(const int *a, int ai, int an, const int *b, int bi, int bn) {
    while (ai < an && bi < bn && a[ai] == b[bi]) { ai++; bi++; }
    return bi == bn || (ai < an && a[ai] > b[bi]);
}

int *maxNumber(const int *a, int n, const int *b, int m, int k, int *outSize) {
    int *best = calloc((size_t) k, sizeof(int));
    for (int take = 0; take <= k; take++) {
        if (take > n || k - take > m) continue;
        int na = 0, nb = 0;
        int *pa = bestFrom(a, n, take, &na);
        int *pb = bestFrom(b, m, k - take, &nb);
        int *merged = malloc(sizeof(int) * (size_t) k);
        int i = 0, j = 0, w = 0;
        while (i < na || j < nb)
            merged[w++] = better(pa, i, na, pb, j, nb) ? pa[i++] : pb[j++];
        int bigger = 0;
        for (int t = 0; t < k && !bigger; t++)           // keep the larger of the two candidates
            if (merged[t] != best[t]) bigger = merged[t] > best[t];
        if (bigger) memcpy(best, merged, sizeof(int) * (size_t) k);
        free(pa); free(pb); free(merged);
    }
    *outSize = k;
    return best;
}   // O(k * n) time · O(k) space
""",
    "shortest-subarray-with-sum-at-least-k": r"""
// Prefix sums plus a monotonic queue of candidate starts.
int shortestSubarray(const int *a, int n, int k) {
    long long *pre = calloc((size_t) n + 1, sizeof(long long));
    for (int i = 0; i < n; i++) pre[i + 1] = pre[i] + a[i];
    int *dq = malloc(sizeof(int) * (size_t) (n + 2));
    int head = 0, tail = 0, best = n + 1;
    for (int i = 0; i <= n; i++) {
        while (tail > head && pre[i] - pre[dq[head]] >= k) {
            int len = i - dq[head++];
            if (len < best) best = len;                    // this start already works
        }
        while (tail > head && pre[dq[tail - 1]] >= pre[i]) tail--;   // keep the queue increasing
        dq[tail++] = i;
    }
    free(pre); free(dq);
    return best <= n ? best : -1;
}   // O(n) time · O(n) space
""",
    "maximum-score-of-a-good-subarray": r"""
// Start at k and expand outwards, always stepping to the larger neighbour.
int maximumScore(const int *a, int n, int k) {
    int lo = k, hi = k, minVal = a[k];
    long long best = a[k];
    while (lo > 0 || hi < n - 1) {
        if (lo == 0) hi++;
        else if (hi == n - 1) lo--;
        else if (a[lo - 1] > a[hi + 1]) lo--;
        else hi++;
        int v = a[lo] < a[hi] ? a[lo] : a[hi];
        if (v < minVal) minVal = v;                       // the window minimum only falls
        long long score = (long long) minVal * (hi - lo + 1);
        if (score > best) best = score;
    }
    return (int) best;
}   // O(n) time · O(1) space
""",
}
