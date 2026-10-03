# Topic 8 · Graphs & Union-Find — C17 solutions
#
# Grids are neighbour checks, weighted graphs are arrays of edges and Dijkstra needs a
# small priority queue. Everything is written out rather than hidden in a library.

CODE = {
    "flood-fill": r"""
// Depth-first repaint of the connected region of the start colour.
static void paint(int **image, int rows, int cols, int r, int c, int from, int to) {
    if (r < 0 || r >= rows || c < 0 || c >= cols) return;
    if (image[r][c] != from) return;                       // wrong colour: outside the region
    image[r][c] = to;
    paint(image, rows, cols, r + 1, c, from, to);
    paint(image, rows, cols, r - 1, c, from, to);
    paint(image, rows, cols, r, c + 1, from, to);
    paint(image, rows, cols, r, c - 1, from, to);
}

int **floodFill(int **image, int rows, int cols, int sr, int sc, int color, int **sizes) {
    *sizes = malloc(sizeof(int) * (size_t) rows);
    for (int i = 0; i < rows; i++) (*sizes)[i] = cols;
    if (image[sr][sc] != color) paint(image, rows, cols, sr, sc, image[sr][sc], color);
    return image;
}   // O(rows * cols) time · O(rows * cols) stack space
""",
    "find-if-path-exists-in-graph": r"""
// Union-find: two nodes are connected when they end up in the same set.
static int findRoot(int *parent, int x) {
    while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }   // path halving
    return x;
}

int validPath(int n, int **edges, int edgeCount, int source, int destination) {
    int *parent = malloc(sizeof(int) * (size_t) n);
    for (int i = 0; i < n; i++) parent[i] = i;
    for (int i = 0; i < edgeCount; i++) {
        int a = findRoot(parent, edges[i][0]), b = findRoot(parent, edges[i][1]);
        if (a != b) parent[a] = b;                        // join the two sets
    }
    int result = findRoot(parent, source) == findRoot(parent, destination);
    free(parent);
    return result;
}   // O(n + E) time · O(n) space
""",
    "find-the-town-judge": r"""
// The judge is trusted by everyone and trusts nobody: in-degree n - 1, out-degree 0.
int findJudge(int n, int **trust, int trustCount) {
    int *in = calloc((size_t) n + 1, sizeof(int));
    int *out = calloc((size_t) n + 1, sizeof(int));
    for (int i = 0; i < trustCount; i++) { out[trust[i][0]]++; in[trust[i][1]]++; }
    int judge = -1;
    for (int i = 1; i <= n; i++)
        if (in[i] == n - 1 && out[i] == 0) judge = i;
    free(in); free(out);
    return judge;
}   // O(n + E) time · O(n) space
""",
    "find-center-of-star-graph": r"""
// In a star every edge touches the centre, so the first two edges share it.
int findCenter(int **edges, int edgeCount) {
    (void) edgeCount;
    if (edges[0][0] == edges[1][0] || edges[0][0] == edges[1][1]) return edges[0][0];
    return edges[0][1];
}   // O(1) time · O(1) space
""",
    "island-perimeter": r"""
// Every cell contributes 4 sides minus one for each neighbour it touches.
int islandPerimeter(int rows, int cols, int **grid) {
    int perimeter = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) {
            if (!grid[r][c]) continue;
            perimeter += 4;
            if (r > 0 && grid[r - 1][c]) perimeter--;
            if (r + 1 < rows && grid[r + 1][c]) perimeter--;
            if (c > 0 && grid[r][c - 1]) perimeter--;
            if (c + 1 < cols && grid[r][c + 1]) perimeter--;
        }
    return perimeter;
}   // O(rows * cols) time · O(1) space
""",
    "destination-city": r"""
// The destination is a city you can reach but never leave.
int destinationCity(char ***paths, int n, char *out) {
    for (int i = 0; i < n; i++) {
        int outgoing = 0;
        for (int j = 0; j < n && !outgoing; j++)
            if (!strcmp(paths[i][1], paths[j][0])) outgoing = 1;
        if (!outgoing) { strcpy(out, paths[i][1]); return 1; }
    }
    return 0;
}   // O(n^2) time · O(1) space (a hash set makes it O(n))
""",
    "number-of-islands": r"""
// Sink every island as you find it, so each land cell is visited once.
static void sink(char **grid, int rows, int cols, int r, int c) {
    if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] != '1') return;
    grid[r][c] = '0';                                     // mark as visited
    sink(grid, rows, cols, r + 1, c);
    sink(grid, rows, cols, r - 1, c);
    sink(grid, rows, cols, r, c + 1);
    sink(grid, rows, cols, r, c - 1);
}

int numIslands(char **grid, int rows) {
    int cols = (!rows) ? 0 : (int) strlen(grid[0]), islands = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            if (grid[r][c] == '1') { islands++; sink(grid, rows, cols, r, c); }
    return islands;
}   // O(rows * cols) time · O(rows * cols) stack space
""",
    "clone-graph": r"""
// Depth-first with a map from original node to its copy.
struct Node { int val, count; struct Node **neighbors; };

static struct Node *copyNode(struct Node *node, struct Node **made, int n) {
    for (int i = 0; i < n; i++) if (made[i] == node) return made[i];
    struct Node *clone = calloc(1, sizeof(struct Node));
    clone->val = node->val;
    clone->count = node->count;
    n++;
    made[n - 1] = node;                                   // remember before recursing: cycles
    struct Node *holder = clone;
    clone->neighbors = malloc(sizeof(struct Node *) * (size_t) node->count);
    for (int i = 0; i < node->count; i++)
        clone->neighbors[i] = copyNode(node->neighbors[i], made, n);
    (void) holder;
    for (int i = 0; i < n; i++) if (made[i] == node) made[i] = clone;
    return clone;
}

struct Node *cloneGraph(struct Node *node) {
    if (!node) return NULL;
    struct Node *seen[1024];
    int count = 0;
    return copyNode(node, seen, count);
}   // O(V + E) time · O(V) space
""",
    "course-schedule": r"""
// Kahn's algorithm: if the topological order covers every course, there is no cycle.
int canFinish(int numCourses, int **prerequisites, int n) {
    int *inDegree = calloc((size_t) numCourses, sizeof(int));
    int *queue = malloc(sizeof(int) * (size_t) numCourses);
    int head = 0, tail = 0, done = 0;
    for (int i = 0; i < n; i++) inDegree[prerequisites[i][0]]++;
    for (int c = 0; c < numCourses; c++) if (!inDegree[c]) queue[tail++] = c;
    while (head < tail) {
        int course = queue[head++];
        done++;
        for (int i = 0; i < n; i++)
            if (prerequisites[i][1] == course && --inDegree[prerequisites[i][0]] == 0)
                queue[tail++] = prerequisites[i][0];
    }
    free(inDegree); free(queue);
    return done == numCourses;
}   // O(V * E) with this edge scan (O(V + E) with adjacency lists) · O(V) space
""",
    "course-schedule-ii": r"""
// Same topological sort, keeping the order itself.
int *findOrder(int numCourses, int **prerequisites, int n, int *returnSize) {
    int *inDegree = calloc((size_t) numCourses, sizeof(int));
    int *queue = malloc(sizeof(int) * (size_t) numCourses);
    int *order = malloc(sizeof(int) * (size_t) numCourses);
    int head = 0, tail = 0, count = 0;
    for (int i = 0; i < n; i++) inDegree[prerequisites[i][0]]++;
    for (int c = 0; c < numCourses; c++) if (!inDegree[c]) queue[tail++] = c;
    while (head < tail) {
        int course = queue[head++];
        order[count++] = course;
        for (int i = 0; i < n; i++)
            if (prerequisites[i][1] == course && --inDegree[prerequisites[i][0]] == 0)
                queue[tail++] = prerequisites[i][0];
    }
    free(inDegree); free(queue);
    if (count != numCourses) { *returnSize = 0; return order; }   // a cycle blocks everything
    *returnSize = count;
    return order;
}   // O(V * E) time · O(V) space
""",
    "pacific-atlantic-water-flow": r"""
// Flood upwards from both oceans; cells reached by both are the answer.
static void flow(int **h, int rows, int cols, int r, int c, int **seen, int marker) {
    seen[r][c] |= marker;
    int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
    for (int k = 0; k < 4; k++) {
        int nr = r + dr[k], nc = c + dc[k];
        if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
        if (seen[nr][nc] & marker) continue;
        if (h[nr][nc] < h[r][c]) continue;                 // water would not flow uphill to us
        flow(h, rows, cols, nr, nc, seen, marker);
    }
}

int **pacificAtlantic(int rows, int cols, int **heights, int *returnSize, int **returnColumnSizes) {
    int **seen = malloc(sizeof(int *) * (size_t) rows);
    for (int r = 0; r < rows; r++) seen[r] = calloc((size_t) cols, sizeof(int));
    for (int c = 0; c < cols; c++) flow(heights, rows, cols, 0, c, seen, 1);          // Pacific
    for (int r = 0; r < rows; r++) flow(heights, rows, cols, r, 0, seen, 1);
    for (int c = 0; c < cols; c++) flow(heights, rows, cols, rows - 1, c, seen, 2);   // Atlantic
    for (int r = 0; r < rows; r++) flow(heights, rows, cols, r, cols - 1, seen, 2);
    int **out = malloc(sizeof(int *) * (size_t) (rows * cols));
    *returnColumnSizes = malloc(sizeof(int) * (size_t) (rows * cols));
    int count = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            if (seen[r][c] == 3) {                          // reached from both oceans
                out[count] = malloc(sizeof(int) * 2);
                out[count][0] = r;
                out[count][1] = c;
                (*returnColumnSizes)[count] = 2;
                count++;
            }
    *returnSize = count;
    return out;
}   // O(rows * cols) time · O(rows * cols) space
""",
    "surrounded-regions": r"""
// Mark the 'O's connected to the border, then flip everything else.
static void markBorder(char **board, int rows, int cols, int r, int c) {
    if (r < 0 || r >= rows || c < 0 || c >= cols || board[r][c] != 'O') return;
    board[r][c] = 'K';                                    // K = keeps its O
    markBorder(board, rows, cols, r + 1, c);
    markBorder(board, rows, cols, r - 1, c);
    markBorder(board, rows, cols, r, c + 1);
    markBorder(board, rows, cols, r, c - 1);
}

void solve(char **board, int rows) {
    int cols = (!rows) ? 0 : (int) strlen(board[0]);
    for (int r = 0; r < rows; r++) { markBorder(board, rows, cols, r, 0); markBorder(board, rows, cols, r, cols - 1); }
    for (int c = 0; c < cols; c++) { markBorder(board, rows, cols, 0, c); markBorder(board, rows, cols, rows - 1, c); }
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) {
            if (board[r][c] == 'O') board[r][c] = 'X';     // fully surrounded
            else if (board[r][c] == 'K') board[r][c] = 'O';
        }
}   // O(rows * cols) time · O(rows * cols) stack space
""",
    "rotting-oranges": r"""
// Multi-source BFS: every rotten orange spreads one ring per minute.
int orangesRotting(int rows, int cols, int **grid) {
    int *queue = malloc(sizeof(int) * (size_t) (rows * cols));
    int head = 0, tail = 0, fresh = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) {
            if (grid[r][c] == 2) queue[tail++] = r * cols + c;
            else if (grid[r][c] == 1) fresh++;
        }
    int minutes = 0;
    while (head < tail && fresh) {
        int size = tail - head;                            // one minute = one full ring
        for (int i = 0; i < size; i++) {
            int cell = queue[head++], r = cell / cols, c = cell % cols;
            int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
            for (int k = 0; k < 4; k++) {
                int nr = r + dr[k], nc = c + dc[k];
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || grid[nr][nc] != 1) continue;
                grid[nr][nc] = 2;
                fresh--;
                queue[tail++] = nr * cols + nc;
            }
        }
        minutes++;
    }
    free(queue);
    return fresh ? -1 : minutes;
}   // O(rows * cols) time · O(rows * cols) space
""",
    "walls-and-gates": r"""
// BFS from every gate at once; each room takes the shortest distance.
void wallsAndGates(int rows, int cols, int **rooms) {
    int *queue = malloc(sizeof(int) * (size_t) (rows * cols));
    int head = 0, tail = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) if (rooms[r][c] == 0) queue[tail++] = r * cols + c;
    while (head < tail) {
        int cell = queue[head++], r = cell / cols, c = cell % cols;
        int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
        for (int k = 0; k < 4; k++) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
            if (rooms[nr][nc] != INT_MAX) continue;        // wall or already reached
            rooms[nr][nc] = rooms[r][c] + 1;
            queue[tail++] = nr * cols + nc;
        }
    }
    free(queue);
}   // O(rows * cols) time · O(rows * cols) space
""",
    "number-of-provinces": r"""
// Union-find over the adjacency matrix; each successful union removes one province.
static int findSet(int *parent, int x) {
    while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
    return x;
}

int findCircleNum(int n, int **isConnected) {
    int *parent = malloc(sizeof(int) * (size_t) n);
    for (int i = 0; i < n; i++) parent[i] = i;
    int groups = n;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (isConnected[i][j]) {
                int a = findSet(parent, i), b = findSet(parent, j);
                if (a != b) { parent[a] = b; groups--; }
            }
    free(parent);
    return groups;
}   // O(n^2) time · O(n) space
""",
    "redundant-connection": r"""
// The first edge whose ends are already connected closes the cycle.
static int findSet(int *parent, int x) {
    while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
    return x;
}

int *findRedundantConnection(int **edges, int n, int *returnSize) {
    int *parent = malloc(sizeof(int) * (size_t) (n + 1));
    for (int i = 1; i <= n; i++) parent[i] = i;
    int *result = NULL;
    for (int i = 0; i < n; i++) {
        int a = findSet(parent, edges[i][0]), b = findSet(parent, edges[i][1]);
        if (a == b) result = edges[i];                    // already connected: this one is spare
        else parent[a] = b;
    }
    free(parent);
    *returnSize = 2;
    return result;
}   // O(n α(n)) time · O(n) space
""",
    "accounts-merge": r"""
// Union-find over accounts that share an email, then group by root.
static int cmpStr(const void *a, const void *b) { return strcmp(*(char *const *) a, *(char *const *) b); }

static int findSet(int *parent, int x) {
    while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
    return x;
}

int accountsMerge(char ***accounts, int accountCount, int *sizes,
                  char **outNames, char ***outEmails, int *outSizes) {
    int *parent = malloc(sizeof(int) * (size_t) accountCount);
    for (int i = 0; i < accountCount; i++) parent[i] = i;
    for (int i = 0; i < accountCount; i++)                // merge accounts sharing an email
        for (int j = i + 1; j < accountCount; j++) {
            int shared = 0;
            for (int a = 1; a < sizes[i] && !shared; a++)
                for (int b = 1; b < sizes[j] && !shared; b++)
                    if (!strcmp(accounts[i][a], accounts[j][b])) shared = 1;
            if (shared) parent[findSet(parent, i)] = findSet(parent, j);
        }
    char ***names = calloc((size_t) accountCount, sizeof(char **));
    char ***emails = calloc((size_t) accountCount, sizeof(char **));
    int *counts = calloc((size_t) accountCount, sizeof(int));
    int *capacity = calloc((size_t) accountCount, sizeof(int));
    int groups = 0;
    for (int i = 0; i < accountCount; i++) {
        int root = findSet(parent, i);
        if (!names[root]) { names[root] = &accounts[i][0]; groups++; }
        for (int a = 1; a < sizes[i]; a++) {
            char *email = accounts[i][a];
            int duplicate = 0;
            for (int e = 0; e < counts[root] && !duplicate; e++)
                if (!strcmp(emails[root][e], email)) duplicate = 1;
            if (duplicate) continue;
            if (counts[root] == capacity[root]) {
                capacity[root] = capacity[root] ? capacity[root] * 2 : 8;
                emails[root] = realloc(emails[root], sizeof(char *) * (size_t) capacity[root]);
            }
            emails[root][counts[root]++] = email;
        }
    }
    int w = 0;
    for (int i = 0; i < accountCount; i++) {
        if (!names[i]) continue;
        qsort(emails[i], (size_t) counts[i], sizeof(char *), cmpStr);   // emails are sorted
        outNames[w] = *names[i];                          // the caller's arrays are filled in
        outEmails[w] = emails[i];
        outSizes[w] = counts[i];
        w++;
    }
    free(parent); free(names); free(emails); free(counts); free(capacity);
    return groups;
}   // O(A^2 * E) time with this comparison · O(A + E) space
""",
    "graph-valid-tree": r"""
// A tree has exactly n - 1 edges and no cycle.
static int findSet(int *parent, int x) {
    while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
    return x;
}

int validTree(int n, int **edges, int edgeCount) {
    if (edgeCount != n - 1) return 0;                     // wrong number of edges
    int *parent = malloc(sizeof(int) * (size_t) n);
    for (int i = 0; i < n; i++) parent[i] = i;
    for (int i = 0; i < edgeCount; i++) {
        int a = findSet(parent, edges[i][0]), b = findSet(parent, edges[i][1]);
        if (a == b) { free(parent); return 0; }            // a cycle
        parent[a] = b;
    }
    free(parent);
    return 1;
}   // O(E α(n)) time · O(n) space
""",
    "word-ladder": r"""
// BFS over words, expanding one letter at a time from the current word.
static int oneAway(const char *a, const char *b) {
    int diff = 0;
    for (int i = 0; a[i] && b[i]; i++) if (a[i] != b[i]) diff++;
    return diff == 1;
}

int ladderLength(const char *begin, const char *end, char **words, int n) {
    int *used = calloc((size_t) n, sizeof(int));
    int *queue = malloc(sizeof(int) * (size_t) (n + 1));
    int *depth = malloc(sizeof(int) * (size_t) (n + 1));
    int head = 0, tail = 0;
    queue[tail] = -1;                                      // -1 stands for the begin word
    depth[tail] = 1;
    tail++;
    while (head < tail) {
        int cur = queue[head];
        int d = depth[head];
        head++;
        const char *word = cur < 0 ? begin : words[cur];
        for (int i = 0; i < n; i++) {
            if (used[i] || !oneAway(word, words[i])) continue;
            if (!strcmp(words[i], end)) return d + 1;
            used[i] = 1;
            queue[tail] = i;
            depth[tail] = d + 1;
            tail++;
        }
    }
    free(used); free(queue); free(depth);
    return 0;
}   // O(n^2 * L) time · O(n) space
""",
    "alien-dictionary": r"""
// Build a "letter before letter" graph from the first differing characters, then topo-sort.
char *alienOrder(char **words, int n) {
    int edges[26][26] = {{0}}, inDegree[26] = {0}, present[26] = {0};
    for (int i = 0; i < n; i++) for (int j = 0; words[i][j]; j++) present[words[i][j] - 'a'] = 1;
    for (int i = 0; i + 1 < n; i++) {
        const char *a = words[i], *b = words[i + 1];
        int j = 0;
        while (a[j] && b[j] && a[j] == b[j]) j++;
        if (a[j] && !b[j]) return strdup("");              // prefix rule violated: no order
        if (a[j] && b[j] && !edges[a[j] - 'a'][b[j] - 'a']) {
            edges[a[j] - 'a'][b[j] - 'a'] = 1;
            inDegree[b[j] - 'a']++;
        }
    }
    char *out = malloc(27);
    int w = 0;
    for (int step = 0; step < 26; step++) {                // Kahn's algorithm over 26 letters
        int found = -1;
        for (int c = 0; c < 26; c++) if (present[c] && !inDegree[c]) { found = c; break; }
        if (found < 0) break;
        out[w++] = (char) ('a' + found);
        present[found] = 0;
        for (int c = 0; c < 26; c++) if (edges[found][c]) inDegree[c]--;
    }
    out[w] = '\0';
    for (int c = 0; c < 26; c++) if (present[c]) return strdup("");     // cycle
    return out;
}   // O(n * L + 26^2) time · O(26^2) space
""",
    "network-delay-time": r"""
// Dijkstra with a linear scan for the closest unvisited node (small n keeps it simple).
int networkDelayTime(int **times, int n, int edgeCount, int k) {
    const int INF = INT_MAX / 4;
    int *dist = malloc(sizeof(int) * (size_t) (n + 1));
    int *done = calloc((size_t) n + 1, sizeof(int));
    for (int i = 1; i <= n; i++) dist[i] = INF;
    dist[k] = 0;
    for (int step = 0; step < n; step++) {
        int best = -1;
        for (int v = 1; v <= n; v++)
            if (!done[v] && (best < 0 || dist[v] < dist[best])) best = v;
        if (best < 0 || dist[best] >= INF) break;
        done[best] = 1;
        for (int e = 0; e < edgeCount; e++)                    // relax every outgoing edge
            if (times[e][0] == best && dist[best] + times[e][2] < dist[times[e][1]])
                dist[times[e][1]] = dist[best] + times[e][2];
    }
    int answer = 0;
    for (int v = 1; v <= n; v++) {
        if (dist[v] >= INF) { answer = -1; break; }            // unreachable node
        if (dist[v] > answer) answer = dist[v];
    }
    free(dist); free(done);
    return answer;
}   // O(V^2 + V * E) with this scan · O(V) space
""",
    "cheapest-flights-within-k-stops": r"""
// Bellman-Ford by number of flights: relax every edge once per hop.
int findCheapestPrice(int n, int **flights, int flightCount, int src, int dst, int k) {
    const int INF = INT_MAX / 4;
    int *dist = malloc(sizeof(int) * (size_t) n);
    int *next = malloc(sizeof(int) * (size_t) n);
    for (int i = 0; i < n; i++) dist[i] = INF;
    dist[src] = 0;
    for (int hop = 0; hop <= k; hop++) {
        memcpy(next, dist, sizeof(int) * (size_t) n);      // only one extra flight per round
        for (int e = 0; e < flightCount; e++) {
            int u = flights[e][0], v = flights[e][1], w = flights[e][2];
            if (dist[u] >= INF) continue;
            if (dist[u] + w < next[v]) next[v] = dist[u] + w;
        }
        memcpy(dist, next, sizeof(int) * (size_t) n);
    }
    int result = dist[dst] >= INF ? -1 : dist[dst];
    free(dist); free(next);
    return result;
}   // O(k * E) time · O(n) space
""",
    "min-cost-to-connect-all-points": r"""
// Prim's algorithm: repeatedly attach the cheapest point not yet in the tree.
static int manhattan(int *a, int *b) { return abs(a[0] - b[0]) + abs(a[1] - b[1]); }

int minCostConnectPoints(int **points, int n) {
    const int INF = INT_MAX / 4;
    int *dist = malloc(sizeof(int) * (size_t) n);
    int *inTree = calloc((size_t) n, sizeof(int));
    for (int i = 0; i < n; i++) dist[i] = INF;
    dist[0] = 0;
    int total = 0;
    for (int step = 0; step < n; step++) {
        int best = -1;
        for (int i = 0; i < n; i++) if (!inTree[i] && (best < 0 || dist[i] < dist[best])) best = i;
        inTree[best] = 1;
        total += dist[best];
        for (int i = 0; i < n; i++)
            if (!inTree[i]) {
                int cost = manhattan(points[best], points[i]);
                if (cost < dist[i]) dist[i] = cost;        // cheaper connection found
            }
    }
    free(dist); free(inTree);
    return total;
}   // O(n^2) time · O(n) space
""",
    "swim-in-rising-water": r"""
// Dijkstra on the grid where the cost of a cell is the maximum height on the way.
int swimInWater(int rows, int cols, int **grid) {
    const int INF = INT_MAX / 4;
    int total = rows * cols;
    int *best = malloc(sizeof(int) * (size_t) total);
    int *done = calloc((size_t) total, sizeof(int));
    for (int i = 0; i < total; i++) best[i] = INF;
    best[0] = grid[0][0];
    while (1) {
        int pick = -1;
        for (int i = 0; i < total; i++)
            if (!done[i] && (pick < 0 || best[i] < best[pick])) pick = i;
        if (pick < 0) break;
        if (pick == total - 1) break;                      // reached the bottom-right corner
        done[pick] = 1;
        int r = pick / cols, c = pick % cols;
        int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
        for (int k = 0; k < 4; k++) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
            int cell = nr * cols + nc;
            int cost = best[pick] > grid[nr][nc] ? best[pick] : grid[nr][nc];   // max on the path
            if (cost < best[cell]) best[cell] = cost;
        }
    }
    int answer = best[total - 1];
    free(best); free(done);
    return answer;
}   // O((rows * cols)^2) with this scan · O(rows * cols) space
""",
    "path-with-minimum-effort": r"""
// Binary search the effort: can the grid be crossed keeping every step under a limit?
static int canCross(int rows, int cols, int **h, int limit, int *seen, int *queue) {
    int head = 0, tail = 0;
    memset(seen, 0, sizeof(int) * (size_t) (rows * cols));
    seen[0] = 1;
    queue[tail++] = 0;
    while (head < tail) {
        int cell = queue[head++], r = cell / cols, c = cell % cols;
        if (cell == rows * cols - 1) return 1;
        int dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
        for (int k = 0; k < 4; k++) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
            int next = nr * cols + nc;
            if (seen[next]) continue;
            int diff = abs(h[nr][nc] - h[r][c]);
            if (diff > limit) continue;                    // too steep for this limit
            seen[next] = 1;
            queue[tail++] = next;
        }
    }
    return 0;
}

int minimumEffortPath(int rows, int cols, int **heights) {
    int *seen = malloc(sizeof(int) * (size_t) (rows * cols));
    int *queue = malloc(sizeof(int) * (size_t) (rows * cols));
    int lo = 0, hi = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            for (int k = 0; k < 4; k++) {
                int nr = r + (k == 0) - (k == 1), nc = c + (k == 2) - (k == 3);
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
                int diff = abs(heights[nr][nc] - heights[r][c]);
                if (diff > hi) hi = diff;
            }
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (canCross(rows, cols, heights, mid, seen, queue)) hi = mid;
        else lo = mid + 1;
    }
    free(seen); free(queue);
    return lo;
}   // O(rows * cols * log max) time · O(rows * cols) space
""",
    "critical-connections-in-a-network": r"""
// Tarjan's bridges: an edge is critical when the subtree cannot reach above its parent.
static void dfs(int u, int parent, int **adj, int *degree, int *tin, int *low, int *timer,
                int **bridges, int *count) {
    tin[u] = low[u] = ++(*timer);
    for (int i = 0; i < degree[u]; i++) {
        int v = adj[u][i];
        if (v == parent) continue;
        if (tin[v]) {
            if (tin[v] < low[u]) low[u] = tin[v];          // a back edge: raise the low value
        } else {
            dfs(v, u, adj, degree, tin, low, timer, bridges, count);
            if (low[v] < low[u]) low[u] = low[v];
            if (low[v] > tin[u]) {                         // no way back: it is a bridge
                bridges[*count] = malloc(sizeof(int) * 2);
                bridges[*count][0] = u;
                bridges[*count][1] = v;
                (*count)++;
            }
        }
    }
}

int **criticalConnections(int n, int **connections, int edgeCount, int *returnSize, int **returnColumnSizes) {
    int **adj = malloc(sizeof(int *) * (size_t) n);
    int *degree = calloc((size_t) n, sizeof(int));
    for (int i = 0; i < edgeCount; i++) { degree[connections[i][0]]++; degree[connections[i][1]]++; }
    for (int i = 0; i < n; i++) adj[i] = malloc(sizeof(int) * (size_t) degree[i]);
    int *fill = calloc((size_t) n, sizeof(int));
    for (int i = 0; i < edgeCount; i++) {
        int a = connections[i][0], b = connections[i][1];
        adj[a][fill[a]++] = b;
        adj[b][fill[b]++] = a;
    }
    int *tin = calloc((size_t) n, sizeof(int)), *low = calloc((size_t) n, sizeof(int));
    int timer = 0, count = 0;
    int **bridges = malloc(sizeof(int *) * (size_t) edgeCount);
    for (int v = 0; v < n; v++) if (!tin[v]) dfs(v, -1, adj, degree, tin, low, &timer, bridges, &count);
    *returnColumnSizes = malloc(sizeof(int) * (size_t) edgeCount);
    for (int i = 0; i < count; i++) (*returnColumnSizes)[i] = 2;
    for (int i = 0; i < n; i++) free(adj[i]);
    free(adj); free(degree); free(fill); free(tin); free(low);
    *returnSize = count;
    return bridges;
}   // O(V + E) time · O(V + E) space
""",
    "remove-max-number-of-edges-to-keep-graph-fully-traversable": r"""
// Union-find twice: type-3 edges first (they are worth the most), then the single-type ones.
static int findSet(int *parent, int x) {
    while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
    return x;
}

static int united(int *parent, int *rank, int a, int b) {
    a = findSet(parent, a);
    b = findSet(parent, b);
    if (a == b) return 0;
    if (rank[a] < rank[b]) { int t = a; a = b; b = t; }
    parent[b] = a;
    if (rank[a] == rank[b]) rank[a]++;
    return 1;
}

int maxNumEdgesToRemove(int n, int **edges, int edgeCount) {
    int *parentA = malloc(sizeof(int) * (size_t) (n + 1)), *rankA = calloc((size_t) n + 1, sizeof(int));
    int *parentB = malloc(sizeof(int) * (size_t) (n + 1)), *rankB = calloc((size_t) n + 1, sizeof(int));
    for (int i = 1; i <= n; i++) { parentA[i] = i; parentB[i] = i; }
    int used = 0;
    for (int pass = 3; pass >= 1; pass--) {
        for (int i = 0; i < edgeCount; i++) {
            if (edges[i][0] != pass) continue;
            int a = edges[i][1], b = edges[i][2];
            if (pass == 3) {
                int ua = united(parentA, rankA, a, b);
                int ub = united(parentB, rankB, a, b);
                if (ua || ub) used++;                      // helps at least one of the two
            } else if (pass == 1) {
                if (united(parentA, rankA, a, b)) used++;
            } else {
                if (united(parentB, rankB, a, b)) used++;
            }
        }
    }
    int connected = 1;
    for (int i = 2; i <= n; i++)
        if (findSet(parentA, i) != findSet(parentA, 1) || findSet(parentB, i) != findSet(parentB, 1))
            connected = 0;
    free(parentA); free(rankA); free(parentB); free(rankB);
    return connected ? edgeCount - used : -1;
}   // O(E α(n)) time · O(n) space
""",
    "number-of-ways-to-arrive-at-destination": r"""
// Dijkstra while counting: every relaxation either resets the count or adds to it.
int countPaths(int n, int **roads, int roadCount) {
    const long long INF = LLONG_MAX / 4, MOD = 1000000007;
    long long *dist = malloc(sizeof(long long) * (size_t) n);
    long long *ways = calloc((size_t) n, sizeof(long long));
    int *done = calloc((size_t) n, sizeof(int));
    for (int i = 0; i < n; i++) dist[i] = INF;
    dist[0] = 0;
    ways[0] = 1;
    for (int step = 0; step < n; step++) {
        int best = -1;
        for (int v = 0; v < n; v++) if (!done[v] && (best < 0 || dist[v] < dist[best])) best = v;
        if (best < 0 || dist[best] == INF) break;
        done[best] = 1;
        for (int e = 0; e < roadCount; e++) {
            int u = roads[e][0], v = roads[e][1], w = roads[e][2];
            if (u != best && v != best) continue;
            int other = u == best ? v : u;
            long long cand = dist[best] + w;
            if (cand < dist[other]) { dist[other] = cand; ways[other] = ways[best]; }
            else if (cand == dist[other]) ways[other] = (ways[other] + ways[best]) % MOD;
        }
    }
    int result = (int) ways[n - 1];
    free(dist); free(ways); free(done);
    return result;
}   // O(V^2 + V * E) with this scan · O(n) space
""",
    "find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance": r"""
// Floyd-Warshall over the whole distance matrix, then count reachable cities per row.
int findTheCity(int n, int **edges, int edgeCount, int distanceThreshold) {
    const int INF = INT_MAX / 4;
    int **dist = malloc(sizeof(int *) * (size_t) n);
    for (int i = 0; i < n; i++) {
        dist[i] = malloc(sizeof(int) * (size_t) n);
        for (int j = 0; j < n; j++) dist[i][j] = i == j ? 0 : INF;
    }
    for (int e = 0; e < edgeCount; e++) {
        int a = edges[e][0], b = edges[e][1], w = edges[e][2];
        if (w < dist[a][b]) { dist[a][b] = w; dist[b][a] = w; }   // keep the cheapest parallel edge
    }
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (dist[i][k] + dist[k][j] < dist[i][j]) dist[i][j] = dist[i][k] + dist[k][j];
    int bestCity = -1, bestCount = n + 1;
    for (int i = 0; i < n; i++) {
        int count = 0;
        for (int j = 0; j < n; j++) if (i != j && dist[i][j] <= distanceThreshold) count++;
        if (count <= bestCount) { bestCount = count; bestCity = i; }   // ties take the largest index
        free(dist[i]);
    }
    free(dist);
    return bestCity;
}   // O(n^3) time · O(n^2) space
""",
    "largest-color-value-in-a-directed-graph": r"""
// Topological order plus a running "best value ending here" per node.
int largestPathValue(const char *colors, int **edges, int edgeCount) {
    int n = (int) strlen(colors);
    int *inDegree = calloc((size_t) n, sizeof(int));
    for (int i = 0; i < edgeCount; i++) inDegree[edges[i][1]]++;
    int **best = malloc(sizeof(int *) * (size_t) n);
    for (int i = 0; i < n; i++) best[i] = calloc(26, sizeof(int));
    int *queue = malloc(sizeof(int) * (size_t) n);
    int head = 0, tail = 0, seen = 0, answer = 0;
    for (int v = 0; v < n; v++) if (!inDegree[v]) queue[tail++] = v;
    while (head < tail) {
        int u = queue[head++];
        seen++;
        int colour = colors[u] - 'a';
        best[u][colour]++;
        if (best[u][colour] > answer) answer = best[u][colour];
        for (int e = 0; e < edgeCount; e++) {
            if (edges[e][0] != u) continue;
            int v = edges[e][1];
            for (int c = 0; c < 26; c++)                  // pass the best counts down the edge
                if (best[u][c] > best[v][c]) best[v][c] = best[u][c];
            if (--inDegree[v] == 0) queue[tail++] = v;
        }
    }
    for (int i = 0; i < n; i++) free(best[i]);
    free(best); free(inDegree); free(queue);
    return seen == n ? answer : -1;                       // a cycle means no valid path
}   // O(V * E) with this edge scan · O(V * 26) space
""",
}
