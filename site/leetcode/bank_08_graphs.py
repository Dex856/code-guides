# Topic 8 · Graphs & Union-Find
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.

TOPIC = {
    "name": "Graphs & Union-Find",
    "tagline": "Build the adjacency list, pick a traversal, and know the four questions: components, cycles, orderings, and shortest paths.",
    "focus": "The whole topic is a decision tree of four questions. Components and flood fills: any traversal. Cycles and connectivity: union-find or coloured "
             "DFS. Dependencies and orderings: topological sort. Weighted distances: Dijkstra, Bellman-Ford or Floyd-Warshall depending on the shape of the "
             "weights. Hard problems mix two of these ideas or add a proof (bridges, MST, path counting).",
    "ordering": "easy 1–6 are single traversals on grids and small graphs; medium 1–4 are components, clones and cycle detection, 5–8 are multi-source "
                "flood fills on grids, 9–12 are union-find applications; hard 1–4 are BFS over generated states and topological sort, 5–8 are the "
                "shortest-path family (Dijkstra, Bellman-Ford, MST), 9–12 are bridges, path counting and Floyd-Warshall.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "flood-fill",
        "title": "Flood Fill",
        "difficulty": "Easy",
        "pattern": "grid DFS/BFS recolouring",
        "statement": "Starting from a pixel, repaint the starting colour and every pixel of the same colour reachable through up/down/left/right "
                     "neighbours with the new colour.",
        "examples": [("image = [[1,1,1],[1,1,0],[1,0,1]], sr = 1, sc = 1, color = 2", "[[2,2,2],[2,2,0],[2,0,1]]"),
                     ("image = [[0,0,0],[0,0,0]], sr = 0, sc = 0, color = 0", "the image unchanged")],
        "constraints": ["1 <= rows, cols <= 50", "0 <= colour values <= 2^16 - 1", "4-directional adjacency only"],
        "approach": "A traversal that visits four neighbours at a time and repaints as it goes. The only trap is the case where the new colour equals "
                     "the old one: without an early return the frontier never shrinks and the recursion loops forever.",
        "complexity": ("O(rows · cols)", "O(rows · cols)"),
        "code": {
            "cpp": r"""// Visit four neighbours, repaint on the way in
vector<vector<int>> floodFill(vector<vector<int>>& img, int sr, int sc, int color) {
    int old = img[sr][sc];
    if (old == color) return img;                // required: otherwise no termination
    int R = img.size(), C = img[0].size();
    vector<pair<int,int>> st{{sr, sc}};
    img[sr][sc] = color;
    while (!st.empty()) {
        auto [r, c] = st.back(); st.pop_back();
        int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr >= 0 && nr < R && nc >= 0 && nc < C && img[nr][nc] == old) {
                img[nr][nc] = color;
                st.push_back({nr, nc});
            }
        }
    }
    return img;
}   // O(R·C) time · O(R·C) space""",
            "java": r"""// Visit four neighbours, repaint on the way in
int[][] floodFill(int[][] img, int sr, int sc, int color) {
    int old = img[sr][sc];
    if (old == color) return img;                // required: otherwise no termination
    int R = img.length, C = img[0].length;
    Deque<int[]> st = new ArrayDeque<>();
    st.push(new int[]{sr, sc});
    img[sr][sc] = color;
    int[] dr = {1,-1,0,0}, dc = {0,0,1,-1};
    while (!st.isEmpty()) {
        int[] cur = st.pop();
        for (int d = 0; d < 4; d++) {
            int nr = cur[0] + dr[d], nc = cur[1] + dc[d];
            if (nr >= 0 && nr < R && nc >= 0 && nc < C && img[nr][nc] == old) {
                img[nr][nc] = color;
                st.push(new int[]{nr, nc});
            }
        }
    }
    return img;
}   // O(R·C) time · O(R·C) space""",
            "python": r"""def flood_fill(image, sr, sc, color):
    old = image[sr][sc]
    if old == color:
        return image                 # without this the frontier never stops
    R, C = len(image), len(image[0])
    stack = [(sr, sc)]
    image[sr][sc] = color
    while stack:
        r, c = stack.pop()
        for nr, nc in ((r+1,c), (r-1,c), (r,c+1), (r,c-1)):
            if 0 <= nr < R and 0 <= nc < C and image[nr][nc] == old:
                image[nr][nc] = color
                stack.append((nr, nc))
    return image""",
        },
    },
    {
        "slug": "find-if-path-exists-in-graph",
        "title": "Find If a Path Exists",
        "difficulty": "Easy",
        "pattern": "adjacency list + BFS",
        "statement": "Given n nodes and a list of undirected edges, decide whether a path connects source to destination.",
        "examples": [("n = 3, edges = [[0,1],[1,2],[2,0]], source = 0, destination = 2", "true"),
                     ("n = 6, edges = [[0,1],[0,2],[3,5],[5,4],[4,3]], source = 0, destination = 5", "false")],
        "constraints": ["1 <= n <= 2 * 10^5", "0 <= edges <= 2 * 10^5", "no self-loops or repeated edges"],
        "approach": "Build the adjacency list once, then walk from the source starting with only the source in the visited set. Reaching the "
                     "destination ends the walk early — a visited set is what keeps the traversal linear instead of exponential on dense graphs.",
        "complexity": ("O(n + m)", "O(n + m)"),
        "code": {
            "cpp": r"""// Adjacency list, then visit reachable nodes from the source
bool validPath(int n, vector<vector<int>>& edges, int src, int dst) {
    vector<vector<int>> adj(n);
    for (auto& e : edges) {                       // undirected: both directions
        adj[e[0]].push_back(e[1]);
        adj[e[1]].push_back(e[0]);
    }
    vector<bool> seen(n, false);
    vector<int> st{src};
    seen[src] = true;
    while (!st.empty()) {
        int u = st.back(); st.pop_back();
        if (u == dst) return true;                // early exit
        for (int v : adj[u]) if (!seen[v]) { seen[v] = true; st.push_back(v); }
    }
    return false;
}   // O(n + m) time · O(n + m) space""",
            "java": r"""// Adjacency list, then visit reachable nodes from the source
boolean validPath(int n, int[][] edges, int src, int dst) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] e : edges) {                       // undirected: both directions
        adj.get(e[0]).add(e[1]);
        adj.get(e[1]).add(e[0]);
    }
    boolean[] seen = new boolean[n];
    Deque<Integer> st = new ArrayDeque<>();
    st.push(src); seen[src] = true;
    while (!st.isEmpty()) {
        int u = st.pop();
        if (u == dst) return true;                // early exit
        for (int v : adj.get(u)) if (!seen[v]) { seen[v] = true; st.push(v); }
    }
    return false;
}   // O(n + m) time · O(n + m) space""",
            "python": r"""def valid_path(n, edges, src, dst):
    adj = [[] for _ in range(n)]
    for a, b in edges:                # undirected: both directions
        adj[a].append(b)
        adj[b].append(a)
    seen = [False] * n
    stack = [src]
    seen[src] = True
    while stack:
        u = stack.pop()
        if u == dst:
            return True               # early exit
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                stack.append(v)
    return False""",
        },
    },
    {
        "slug": "find-the-town-judge",
        "title": "Find the Town Judge",
        "difficulty": "Easy",
        "pattern": "degree counting",
        "statement": "In a town of n people, trust[i] = [a, b] means a trusts b. The judge trusts nobody and is trusted by everyone else. Return the "
                     "judge's label, or -1.",
        "examples": [("n = 2, trust = [[1,2]]", "2"), ("n = 3, trust = [[1,3],[2,3],[3,1]]", "-1")],
        "constraints": ["1 <= n <= 1000", "0 <= number of trust pairs <= 10^4", "there is at most one judge"],
        "approach": "Two degree arrays, out and in: the judge is the person with out-degree zero and in-degree n-1. One pass over the trust list fills "
                     "both — this is the simplest possible example of turning an edge list into per-vertex facts.",
        "complexity": ("O(n + m)", "O(n)"),
        "code": {
            "cpp": r"""// Judge: trusts nobody (out 0) and is trusted by everyone (in n-1)
int findJudge(int n, vector<vector<int>>& trust) {
    vector<int> in(n + 1, 0), out(n + 1, 0);
    for (auto& t : trust) { out[t[0]]++; in[t[1]]++; }
    for (int p = 1; p <= n; p++)
        if (out[p] == 0 && in[p] == n - 1) return p;
    return -1;
}   // O(n + m) time · O(n) space""",
            "java": r"""// Judge: trusts nobody (out 0) and is trusted by everyone (in n-1)
int findJudge(int n, int[][] trust) {
    int[] in = new int[n + 1], out = new int[n + 1];
    for (int[] t : trust) { out[t[0]]++; in[t[1]]++; }
    for (int p = 1; p <= n; p++)
        if (out[p] == 0 && in[p] == n - 1) return p;
    return -1;
}   // O(n + m) time · O(n) space""",
            "python": r"""def find_judge(n, trust):
    indeg = [0] * (n + 1)
    outdeg = [0] * (n + 1)
    for a, b in trust:
        outdeg[a] += 1
        indeg[b] += 1
    for p in range(1, n + 1):
        if outdeg[p] == 0 and indeg[p] == n - 1:
            return p
    return -1""",
        },
    },
    {
        "slug": "find-center-of-star-graph",
        "title": "Centre of a Star Graph",
        "difficulty": "Easy",
        "pattern": "shared endpoint",
        "statement": "A star graph has one centre connected to every other node. Given its edges, return the centre.",
        "examples": [("edges = [[1,2],[2,3],[4,2]]", "2"), ("edges = [[1,2],[5,1],[1,3],[1,4]]", "1")],
        "constraints": ["3 <= n <= 10^5", "the graph is always a star", "edges are given in any order"],
        "approach": "The centre is the only vertex shared by all edges, so it appears in every edge — two edges are enough to identify it: whichever "
                     "endpoint the first two edges have in common is the centre. Constant time and a nice reminder to look for a stronger guarantee "
                     "before writing a traversal.",
        "complexity": ("O(1)", "O(1)"),
        "code": {
            "cpp": r"""// Two edges are enough: the centre is their shared endpoint
int findCenter(vector<vector<int>>& edges) {
    int a = edges[0][0], b = edges[0][1];
    return (edges[1][0] == a || edges[1][1] == a) ? a : b;
}   // O(1) time · O(1) space""",
            "java": r"""// Two edges are enough: the centre is their shared endpoint
int findCenter(int[][] edges) {
    int a = edges[0][0], b = edges[0][1];
    return (edges[1][0] == a || edges[1][1] == a) ? a : b;
}   // O(1) time · O(1) space""",
            "python": r"""def find_center(edges):
    a, b = edges[0]
    return a if a in edges[1] else b      # the centre appears in every edge""",
        },
    },
    {
        "slug": "island-perimeter",
        "title": "Island Perimeter",
        "difficulty": "Easy",
        "pattern": "count land edges",
        "statement": "A grid contains one island of 1s surrounded by water. Return the length of its perimeter.",
        "examples": [("grid = [[0,1,0,0],[1,1,1,0],[0,1,0,0],[1,1,0,0]]", "16"), ("grid = [[1]]", "4")],
        "constraints": ["1 <= rows, cols <= 100", "cells are 0 or 1", "there is exactly one island and it has no lakes"],
        "approach": "Every land cell starts with four sides; each shared edge between two land cells removes two sides. Counting the shared edges "
                     "right and down only avoids the double count — no traversal needed at all.",
        "complexity": ("O(rows · cols)", "O(1)"),
        "code": {
            "cpp": r"""// 4 sides per land cell, minus 2 for every shared edge
int islandPerimeter(vector<vector<int>>& g) {
    int R = g.size(), C = g[0].size(), perimeter = 0;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) {
            if (!g[r][c]) continue;
            perimeter += 4;                       // start with the full outline
            if (r + 1 < R && g[r+1][c]) perimeter -= 2;   // shared edge below
            if (c + 1 < C && g[r][c+1]) perimeter -= 2;   // shared edge to the right
        }
    return perimeter;
}   // O(R·C) time · O(1) space""",
            "java": r"""// 4 sides per land cell, minus 2 for every shared edge
int islandPerimeter(int[][] g) {
    int R = g.length, C = g[0].length, perimeter = 0;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) {
            if (g[r][c] == 0) continue;
            perimeter += 4;                       // start with the full outline
            if (r + 1 < R && g[r+1][c] == 1) perimeter -= 2;   // shared edge below
            if (c + 1 < C && g[r][c+1] == 1) perimeter -= 2;   // shared edge right
        }
    return perimeter;
}   // O(R·C) time · O(1) space""",
            "python": r"""def island_perimeter(grid):
    R, C, perimeter = len(grid), len(grid[0]), 0
    for r in range(R):
        for c in range(C):
            if grid[r][c]:
                perimeter += 4                        # the full outline
                if r + 1 < R and grid[r+1][c]:
                    perimeter -= 2                    # shared edge below
                if c + 1 < C and grid[r][c+1]:
                    perimeter -= 2                    # shared edge to the right
    return perimeter""",
        },
    },
    {
        "slug": "destination-city",
        "title": "Destination City",
        "difficulty": "Easy",
        "pattern": "hash set of sources (out-degree zero)",
        "statement": "Each pair paths[i] = [from, to] is a direct one-way path between two cities, and together they form a single line with no loops. "
                     "Return the city that has no outgoing path.",
        "examples": [("paths = [[\"London\",\"New York\"],[\"New York\",\"Lima\"],[\"Lima\",\"Sao Paulo\"]]", "\"Sao Paulo\""),
                     ("paths = [[\"B\",\"C\"],[\"D\",\"B\"],[\"C\",\"A\"]]", "\"A\""),
                     ("paths = [[\"A\",\"Z\"]]", "\"Z\"")],
        "constraints": ["1 <= paths.length <= 100", "paths[i].length == 2", "1 <= city name length <= 10",
                        "the paths form a line, so exactly one destination exists"],
        "approach": "Collect every city that starts a path into a hash set; the destination is the only city that never appears in it. That is the "
                     "out-degree-zero condition, and the set turns it into one linear pass instead of a search.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// The destination is the only city that never starts a path
string destCity(vector<vector<string>>& paths) {
    unordered_set<string> outgoing;              // every city that starts a path
    for (auto& p : paths) outgoing.insert(p[0]);
    for (auto& p : paths)
        if (!outgoing.count(p[1])) return p[1];  // never a source: the answer
    return "";
}   // O(n) time · O(n) space""",
            "java": r"""// The destination is the only city that never starts a path
String destCity(List<List<String>> paths) {
    Set<String> outgoing = new HashSet<>();      // every city that starts a path
    for (List<String> p : paths) outgoing.add(p.get(0));
    for (List<String> p : paths)
        if (!outgoing.contains(p.get(1))) return p.get(1);   // never a source
    return "";
}   // O(n) time · O(n) space""",
            "python": r"""def dest_city(paths):
    outgoing = {a for a, b in paths}     # cities that start a path
    for a, b in paths:
        if b not in outgoing:            # never a source: the destination
            return b
    return ''""",
        },
    },
    {
        "slug": "number-of-islands",
        "title": "Number of Islands",
        "difficulty": "Medium",
        "pattern": "component counting on a grid",
        "statement": "A grid of '1' (land) and '0' (water) contains islands of 4-directionally connected land. Return how many islands there are.",
        "examples": [("grid = [[\"1\",\"1\",\"1\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"0\",\"0\"]]", "1"),
                     ("grid = [[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"1\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"1\",\"1\"]]", "3")],
        "constraints": ["1 <= rows, cols <= 300", "cells are the characters '0' and '1'", "islands are counted with 4-directional connectivity"],
        "approach": "Scan every cell; each unvisited land cell starts a new island, and a flood fill (or a union-find pass) marks the whole component. "
                     "Incrementing the counter exactly at the start of each fill is what guarantees one count per island.",
        "complexity": ("O(rows · cols)", "O(rows · cols)"),
        "code": {
            "cpp": r"""// Each flood fill is one island
int numIslands(vector<vector<char>>& g) {
    int R = g.size(), C = g[0].size(), islands = 0;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) {
            if (g[r][c] != '1') continue;
            islands++;                            // a fresh component starts here
            vector<pair<int,int>> st{{r, c}};
            g[r][c] = '0';                        // sink it as we go
            while (!st.empty()) {
                auto [y, x] = st.back(); st.pop_back();
                int dy[4] = {1,-1,0,0}, dx[4] = {0,0,1,-1};
                for (int d = 0; d < 4; d++) {
                    int ny = y + dy[d], nx = x + dx[d];
                    if (ny >= 0 && ny < R && nx >= 0 && nx < C && g[ny][nx] == '1') {
                        g[ny][nx] = '0';
                        st.push_back({ny, nx});
                    }
                }
            }
        }
    return islands;
}   // O(R·C) time · O(R·C) space""",
            "java": r"""// Each flood fill is one island
int numIslands(char[][] g) {
    int R = g.length, C = g[0].length, islands = 0;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) {
            if (g[r][c] != '1') continue;
            islands++;                            // a fresh component starts here
            Deque<int[]> st = new ArrayDeque<>();
            st.push(new int[]{r, c});
            g[r][c] = '0';                        // sink it as we go
            int[] dy = {1,-1,0,0}, dx = {0,0,1,-1};
            while (!st.isEmpty()) {
                int[] cur = st.pop();
                for (int d = 0; d < 4; d++) {
                    int ny = cur[0] + dy[d], nx = cur[1] + dx[d];
                    if (ny >= 0 && ny < R && nx >= 0 && nx < C && g[ny][nx] == '1') {
                        g[ny][nx] = '0';
                        st.push(new int[]{ny, nx});
                    }
                }
            }
        }
    return islands;
}   // O(R·C) time · O(R·C) space""",
            "python": r"""def num_islands(grid):
    R, C = len(grid), len(grid[0])
    islands = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] != '1':
                continue
            islands += 1                  # a fresh component starts here
            stack = [(r, c)]
            grid[r][c] = '0'              # sink the cell as we visit it
            while stack:
                y, x = stack.pop()
                for ny, nx in ((y+1,x), (y-1,x), (y,x+1), (y,x-1)):
                    if 0 <= ny < R and 0 <= nx < C and grid[ny][nx] == '1':
                        grid[ny][nx] = '0'
                        stack.append((ny, nx))
    return islands""",
        },
    },
    {
        "slug": "clone-graph",
        "title": "Clone a Graph",
        "difficulty": "Medium",
        "pattern": "DFS with old-to-new map",
        "statement": "Given a node of a connected undirected graph, return a deep copy of the whole graph.",
        "examples": [("adjList = [[2,4],[1,3],[2,4],[1,3]]", "an identical independent graph"),
                     ("adjList = [[]]", "a single node with no neighbours")],
        "constraints": ["1 <= number of nodes <= 100", "node values are unique", "the graph may contain cycles"],
        "approach": "Create a clone the moment you first meet a node, record it in a map before recursing, and reuse that clone for every later "
                     "reference. Creating the clone early is what stops the cycle from being copied forever — the same pattern as copying a "
                     "linked list with random pointers.",
        "complexity": ("O(V + E)", "O(V)"),
        "code": {
            "cpp": r"""// Create the clone before recursing so cycles terminate
class Node { public: int val; vector<Node*> neighbors; Node(int v = 0) : val(v) {} };
Node* dfs(Node* node, unordered_map<Node*, Node*>& made) {
    if (!node) return nullptr;
    if (made.count(node)) return made[node];     // already copied: reuse it
    Node* copy = new Node(node->val);
    made[node] = copy;                           // register BEFORE recursing
    for (Node* nb : node->neighbors) copy->neighbors.push_back(dfs(nb, made));
    return copy;
}
Node* cloneGraph(Node* node) {
    unordered_map<Node*, Node*> made;
    return dfs(node, made);
}   // O(V + E) time · O(V) space""",
            "java": r"""// Create the clone before recursing so cycles terminate
class Node { public int val; public List<Node> neighbors = new ArrayList<>(); public Node(int v) { val = v; } }
Node dfs(Node node, Map<Node, Node> made) {
    if (node == null) return null;
    if (made.containsKey(node)) return made.get(node);   // reuse the copy
    Node copy = new Node(node.val);
    made.put(node, copy);                        // register BEFORE recursing
    for (Node nb : node.neighbors) copy.neighbors.add(dfs(nb, made));
    return copy;
}
Node cloneGraph(Node node) { return dfs(node, new HashMap<>()); }
// O(V + E) time · O(V) space""",
            "python": r"""def clone_graph(node):
    made = {}                        # original -> copy
    def dfs(n):
        if not n:
            return None
        if n in made:
            return made[n]           # already copied: reuse it
        copy = Node(n.val)
        made[n] = copy               # register BEFORE recursing
        copy.neighbors = [dfs(nb) for nb in n.neighbors]
        return copy

    return dfs(node)""",
        },
    },
    {
        "slug": "course-schedule",
        "title": "Course Schedule",
        "difficulty": "Medium",
        "pattern": "cycle detection in a directed graph",
        "statement": "prerequisites[i] = [a, b] means course b must be taken before course a. Decide whether all courses can be finished.",
        "examples": [("numCourses = 2, prerequisites = [[1,0]]", "true"), ("numCourses = 2, prerequisites = [[1,0],[0,1]]", "false")],
        "constraints": ["1 <= numCourses <= 2000", "0 <= prerequisites <= 5000", "all pairs are distinct"],
        "approach": "This is exactly 'does the dependency graph have a cycle?'. A three-colour DFS answers it: white = untouched, grey = on the current "
                     "stack, black = finished. Meeting a grey node means a cycle, and the colours are essential — a plain visited set cannot tell a "
                     "cycle from a diamond.",
        "complexity": ("O(V + E)", "O(V + E)"),
        "code": {
            "cpp": r"""// Three-colour DFS: grey = on the current path
bool dfs(int u, vector<vector<int>>& adj, vector<int>& state) {
    state[u] = 1;                                // grey: being explored
    for (int v : adj[u]) {
        if (state[v] == 1) return true;          // back edge: a cycle
        if (state[v] == 0 && dfs(v, adj, state)) return true;
    }
    state[u] = 2;                                // black: finished
    return false;
}
bool canFinish(int n, vector<vector<int>>& pre) {
    vector<vector<int>> adj(n);
    for (auto& p : pre) adj[p[1]].push_back(p[0]);   // b -> a
    vector<int> state(n, 0);
    for (int u = 0; u < n; u++)
        if (state[u] == 0 && dfs(u, adj, state)) return false;
    return true;
}   // O(V + E) time · O(V + E) space""",
            "java": r"""// Three-colour DFS: grey = on the current path
boolean dfs(int u, List<List<Integer>> adj, int[] state) {
    state[u] = 1;                                // grey: being explored
    for (int v : adj.get(u)) {
        if (state[v] == 1) return true;          // back edge: a cycle
        if (state[v] == 0 && dfs(v, adj, state)) return true;
    }
    state[u] = 2;                                // black: finished
    return false;
}
boolean canFinish(int n, int[][] pre) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] p : pre) adj.get(p[1]).add(p[0]);      // b -> a
    int[] state = new int[n];
    for (int u = 0; u < n; u++)
        if (state[u] == 0 && dfs(u, adj, state)) return false;
    return true;
}   // O(V + E) time · O(V + E) space""",
            "python": r"""def can_finish(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]
    for a, b in prerequisites:
        adj[b].append(a)              # b must come before a
    state = [0] * num_courses         # 0 white, 1 grey, 2 black

    def has_cycle(u):
        state[u] = 1                  # grey: on the current path
        for v in adj[u]:
            if state[v] == 1:
                return True           # back edge
            if state[v] == 0 and has_cycle(v):
                return True
        state[u] = 2                  # black: finished
        return False

    return not any(state[u] == 0 and has_cycle(u) for u in range(num_courses))""",
        },
    },
    {
        "slug": "course-schedule-ii",
        "title": "Course Schedule II",
        "difficulty": "Medium",
        "pattern": "topological sort (Kahn)",
        "statement": "Return one valid order in which all courses can be taken, or an empty array if that is impossible.",
        "examples": [("numCourses = 2, prerequisites = [[1,0]]", "[0,1]"), ("numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]", "[0,1,2,3] (or similar)")],
        "constraints": ["1 <= numCourses <= 2000", "0 <= prerequisites <= 5000", "any valid order is accepted"],
        "approach": "Kahn's algorithm: start with every course that has no prerequisites, then repeatedly take one out and decrement its dependents' "
                     "counts. If the produced order is shorter than the course count, some cycle blocked the rest — so the same pass detects "
                     "impossibility for free.",
        "complexity": ("O(V + E)", "O(V + E)"),
        "code": {
            "cpp": r"""// Kahn: queue of zero-in-degree nodes, peeling edge by edge
vector<int> findOrder(int n, vector<vector<int>>& pre) {
    vector<vector<int>> adj(n);
    vector<int> indeg(n, 0);
    for (auto& p : pre) { adj[p[1]].push_back(p[0]); indeg[p[0]]++; }
    queue<int> ready;
    for (int u = 0; u < n; u++) if (indeg[u] == 0) ready.push(u);
    vector<int> order;
    while (!ready.empty()) {
        int u = ready.front(); ready.pop();
        order.push_back(u);                      // take this course now
        for (int v : adj[u]) if (--indeg[v] == 0) ready.push(v);
    }
    return (int)order.size() == n ? order : vector<int>{};   // short means cycle
}   // O(V + E) time · O(V + E) space""",
            "java": r"""// Kahn: queue of zero-in-degree nodes, peeling edge by edge
int[] findOrder(int n, int[][] pre) {
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    int[] indeg = new int[n];
    for (int[] p : pre) { adj.get(p[1]).add(p[0]); indeg[p[0]]++; }
    Deque<Integer> ready = new ArrayDeque<>();
    for (int u = 0; u < n; u++) if (indeg[u] == 0) ready.add(u);
    int[] order = new int[n];
    int k = 0;
    while (!ready.isEmpty()) {
        int u = ready.poll();
        order[k++] = u;                          // take this course now
        for (int v : adj.get(u)) if (--indeg[v] == 0) ready.add(v);
    }
    return k == n ? order : new int[0];          // short means cycle
}   // O(V + E) time · O(V + E) space""",
            "python": r"""from collections import deque

def find_order(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1
    ready = deque(u for u in range(num_courses) if indeg[u] == 0)
    order = []
    while ready:
        u = ready.popleft()
        order.append(u)                  # take this course now
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    return order if len(order) == num_courses else []   # short means cycle""",
        },
    },
    {
        "slug": "pacific-atlantic-water-flow",
        "title": "Pacific Atlantic Water Flow",
        "difficulty": "Medium",
        "pattern": "multi-source DFS from the borders",
        "statement": "Water flows from a cell to a neighbour of equal or lower height. Return every cell from which water can reach both the top-left "
                     "and bottom-right oceans.",
        "examples": [("heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]", "[[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]"),
                     ("heights = [[1]]", "[[0,0]]")],
        "constraints": ["1 <= rows, cols <= 200", "0 <= heights <= 10^5", "the two oceans border the top/left and bottom/right edges"],
        "approach": "Searching forward from every cell is expensive; searching *backwards* from each ocean's border finds, for each ocean, all cells "
                     "that drain into it — and uphill reverse traversal is a simple 'neighbour is not lower' test. Intersecting the two sets is the "
                     "answer.",
        "complexity": ("O(rows · cols)", "O(rows · cols)"),
        "code": {
            "cpp": r"""// Reverse DFS from each ocean's border, then intersect
void flow(vector<vector<int>>& h, vector<vector<bool>>& seen, int r, int c) {
    int R = h.size(), C = h[0].size();
    seen[r][c] = true;
    int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    for (int d = 0; d < 4; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= R || nc < 0 || nc >= C || seen[nr][nc]) continue;
        if (h[nr][nc] >= h[r][c]) flow(h, seen, nr, nc);   // can flow back downhill
    }
}
vector<vector<int>> pacificAtlantic(vector<vector<int>>& h) {
    int R = h.size(), C = h[0].size();
    vector<vector<bool>> pac(R, vector<bool>(C, false)), atl(R, vector<bool>(C, false));
    for (int r = 0; r < R; r++) { flow(h, pac, r, 0); flow(h, atl, r, C-1); }
    for (int c = 0; c < C; c++) { flow(h, pac, 0, c); flow(h, atl, R-1, c); }
    vector<vector<int>> out;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            if (pac[r][c] && atl[r][c]) out.push_back({r, c});
    return out;
}   // O(R·C) time · O(R·C) space""",
            "java": r"""// Reverse DFS from each ocean's border, then intersect
void flow(int[][] h, boolean[][] seen, int r, int c) {
    int R = h.length, C = h[0].length;
    seen[r][c] = true;
    int[] dr = {1,-1,0,0}, dc = {0,0,1,-1};
    for (int d = 0; d < 4; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= R || nc < 0 || nc >= C || seen[nr][nc]) continue;
        if (h[nr][nc] >= h[r][c]) flow(h, seen, nr, nc);   // reverse downhill
    }
}
List<List<Integer>> pacificAtlantic(int[][] h) {
    int R = h.length, C = h[0].length;
    boolean[][] pac = new boolean[R][C], atl = new boolean[R][C];
    for (int r = 0; r < R; r++) { flow(h, pac, r, 0); flow(h, atl, r, C-1); }
    for (int c = 0; c < C; c++) { flow(h, pac, 0, c); flow(h, atl, R-1, c); }
    List<List<Integer>> out = new ArrayList<>();
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            if (pac[r][c] && atl[r][c]) out.add(Arrays.asList(r, c));
    return out;
}   // O(R·C) time · O(R·C) space""",
            "python": r"""def pacific_atlantic(heights):
    R, C = len(heights), len(heights[0])

    def flow(seen, r, c):
        seen[r][c] = True
        for nr, nc in ((r+1,c), (r-1,c), (r,c+1), (r,c-1)):
            if 0 <= nr < R and 0 <= nc < C and not seen[nr][nc]:
                if heights[nr][nc] >= heights[r][c]:   # uphill in reverse
                    flow(seen, nr, nc)

    pac = [[False] * C for _ in range(R)]
    atl = [[False] * C for _ in range(R)]
    for r in range(R):
        flow(pac, r, 0); flow(atl, r, C - 1)      # left and right borders
    for c in range(C):
        flow(pac, 0, c); flow(atl, R - 1, c)      # top and bottom borders
    return [[r, c] for r in range(R) for c in range(C) if pac[r][c] and atl[r][c]]""",
        },
    },
    {
        "slug": "surrounded-regions",
        "title": "Surrounded Regions",
        "difficulty": "Medium",
        "pattern": "mark from the border inward",
        "statement": "Flip every region of 'O' fully surrounded by 'X' into 'X'; regions touching the border are never flipped.",
        "examples": [("board = [[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"O\",\"O\",\"X\"],[\"X\",\"X\",\"O\",\"X\"],[\"X\",\"O\",\"X\",\"X\"]]",
                      "[[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"X\",\"X\",\"X\"],[\"X\",\"O\",\"X\",\"X\"]]"),
                     ("board = [[\"X\"]]", "[[\"X\"]]")],
        "constraints": ["1 <= rows, cols <= 200", "cells are the characters 'X' and 'O'", "the board is modified in place"],
        "approach": "Identifying surrounded regions directly is awkward; identifying safe regions is easy. Flood from every border 'O', mark those "
                     "cells as safe, then sweep once: unmarked 'O' becomes 'X' and marked cells return to 'O'. Deciding the complement is a recurring "
                     "trick in grid problems.",
        "complexity": ("O(rows · cols)", "O(rows · cols)"),
        "code": {
            "cpp": r"""// Mark border-connected 'O's safe, then flip the rest
void safe(vector<vector<char>>& b, int r, int c) {
    int R = b.size(), C = b[0].size();
    if (r < 0 || r >= R || c < 0 || c >= C || b[r][c] != 'O') return;
    b[r][c] = 'S';                               // temporarily marked safe
    safe(b, r+1, c); safe(b, r-1, c); safe(b, r, c+1); safe(b, r, c-1);
}
void solve(vector<vector<char>>& b) {
    int R = b.size(), C = b[0].size();
    for (int r = 0; r < R; r++) { safe(b, r, 0); safe(b, r, C-1); }
    for (int c = 0; c < C; c++) { safe(b, 0, c); safe(b, R-1, c); }
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            b[r][c] = (b[r][c] == 'S') ? 'O' : 'X';   // flip the enclosed ones
}   // O(R·C) time · O(R·C) space""",
            "java": r"""// Mark border-connected 'O's safe, then flip the rest
void safe(char[][] b, int r, int c) {
    int R = b.length, C = b[0].length;
    if (r < 0 || r >= R || c < 0 || c >= C || b[r][c] != 'O') return;
    b[r][c] = 'S';                               // temporarily marked safe
    safe(b, r+1, c); safe(b, r-1, c); safe(b, r, c+1); safe(b, r, c-1);
}
void solve(char[][] b) {
    int R = b.length, C = b[0].length;
    for (int r = 0; r < R; r++) { safe(b, r, 0); safe(b, r, C-1); }
    for (int c = 0; c < C; c++) { safe(b, 0, c); safe(b, R-1, c); }
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++)
            b[r][c] = (b[r][c] == 'S') ? 'O' : 'X';   // flip the enclosed ones
}   // O(R·C) time · O(R·C) space""",
            "python": r"""def solve(board):
    R, C = len(board), len(board[0])

    def mark_safe(r, c):
        if not (0 <= r < R and 0 <= c < C) or board[r][c] != 'O':
            return
        board[r][c] = 'S'             # temporarily safe
        mark_safe(r+1, c); mark_safe(r-1, c)
        mark_safe(r, c+1); mark_safe(r, c-1)

    for r in range(R):
        mark_safe(r, 0); mark_safe(r, C - 1)
    for c in range(C):
        mark_safe(0, c); mark_safe(R - 1, c)
    for r in range(R):
        for c in range(C):
            board[r][c] = 'O' if board[r][c] == 'S' else 'X'""",
        },
    },
    {
        "slug": "rotting-oranges",
        "title": "Rotting Oranges",
        "difficulty": "Medium",
        "pattern": "multi-source BFS by layers",
        "statement": "In a grid, 0 is empty, 1 is a fresh orange and 2 is rotten. Every minute each rotten orange rots its 4-neighbours. Return the "
                     "minutes until no fresh orange remains, or -1 if some never rot.",
        "examples": [("grid = [[2,1,1],[1,1,0],[0,1,1]]", "4"), ("grid = [[2,1,1],[0,1,1],[1,0,1]]", "-1"), ("grid = [[0,2]]", "0")],
        "constraints": ["1 <= rows, cols <= 10", "cells are 0, 1 or 2", "all rotten oranges start at minute 0"],
        "approach": "Seed a queue with *every* rotten orange and process it level by level; each level is one minute. Counting fresh oranges up front "
                     "and decrementing on each infection lets a single check at the end decide between the minute count and -1.",
        "complexity": ("O(rows · cols)", "O(rows · cols)"),
        "code": {
            "cpp": r"""// All rotten cells at once; each BFS layer is one minute
int orangesRotting(vector<vector<int>>& g) {
    int R = g.size(), C = g[0].size(), fresh = 0;
    queue<pair<int,int>> q;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) {
            if (g[r][c] == 2) q.push({r, c});     // every source at minute 0
            else if (g[r][c] == 1) fresh++;
        }
    int minutes = 0;
    int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    while (!q.empty() && fresh > 0) {
        int size = q.size();
        minutes++;                                // one layer = one minute
        while (size--) {
            auto [r, c] = q.front(); q.pop();
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nr < R && nc >= 0 && nc < C && g[nr][nc] == 1) {
                    g[nr][nc] = 2; fresh--;
                    q.push({nr, nc});
                }
            }
        }
    }
    return fresh == 0 ? minutes : -1;
}   // O(R·C) time · O(R·C) space""",
            "java": r"""// All rotten cells at once; each BFS layer is one minute
int orangesRotting(int[][] g) {
    int R = g.length, C = g[0].length, fresh = 0;
    Deque<int[]> q = new ArrayDeque<>();
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) {
            if (g[r][c] == 2) q.add(new int[]{r, c});   // every source at minute 0
            else if (g[r][c] == 1) fresh++;
        }
    int minutes = 0;
    int[] dr = {1,-1,0,0}, dc = {0,0,1,-1};
    while (!q.isEmpty() && fresh > 0) {
        int size = q.size();
        minutes++;                                // one layer = one minute
        while (size-- > 0) {
            int[] cur = q.poll();
            for (int d = 0; d < 4; d++) {
                int nr = cur[0] + dr[d], nc = cur[1] + dc[d];
                if (nr >= 0 && nr < R && nc >= 0 && nc < C && g[nr][nc] == 1) {
                    g[nr][nc] = 2; fresh--;
                    q.add(new int[]{nr, nc});
                }
            }
        }
    }
    return fresh == 0 ? minutes : -1;
}   // O(R·C) time · O(R·C) space""",
            "python": r"""from collections import deque

def oranges_rotting(grid):
    R, C = len(grid), len(grid[0])
    q, fresh = deque(), 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 2:
                q.append((r, c))       # every source at minute 0
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while q and fresh:
        minutes += 1                   # one layer is one minute
        for _ in range(len(q)):
            r, c = q.popleft()
            for nr, nc in ((r+1,c), (r-1,c), (r,c+1), (r,c-1)):
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
    return minutes if fresh == 0 else -1""",
        },
    },
    {
        "slug": "walls-and-gates",
        "title": "Walls and Gates",
        "difficulty": "Medium",
        "pattern": "multi-source BFS from all gates",
        "statement": "Fill every empty room with its distance to the nearest gate: 0 is a gate, -1 is a wall, and INF (2^31 - 1) marks an empty "
                     "room. Rooms that cannot reach any gate keep INF.",
        "examples": [("rooms = [[inf,-1,0,inf],[inf,inf,inf,-1],[inf,-1,inf,-1],[0,-1,inf,inf]] with inf = 2147483647",
                      "[[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]]"),
                     ("rooms = [[-1]]", "[[-1]]")],
        "constraints": ["1 <= rows, cols <= 250", "cells are -1 (wall), 0 (gate) or 2^31 - 1 (empty)", "the grid is modified in place"],
        "approach": "A BFS from a single gate would have to be repeated per gate; starting from all gates at once fills every room with the distance "
                     "to the *nearest* gate in one pass. Level order is what makes the distances correct, exactly as in the rotting-oranges problem.",
        "complexity": ("O(rows · cols)", "O(rows · cols)"),
        "code": {
            "cpp": r"""// One BFS with every gate as a source
const int INF = 2147483647;
void wallsAndGates(vector<vector<int>>& rooms) {
    int R = rooms.size(), C = rooms[0].size();
    queue<pair<int,int>> q;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) if (rooms[r][c] == 0) q.push({r, c});
    int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    while (!q.empty()) {
        auto [r, c] = q.front(); q.pop();
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr >= 0 && nr < R && nc >= 0 && nc < C && rooms[nr][nc] == INF) {
                rooms[nr][nc] = rooms[r][c] + 1;   // first visit = nearest gate
                q.push({nr, nc});
            }
        }
    }
}   // O(R·C) time · O(R·C) space""",
            "java": r"""// One BFS with every gate as a source
void wallsAndGates(int[][] rooms) {
    int R = rooms.length, C = rooms[0].length;
    Deque<int[]> q = new ArrayDeque<>();
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) if (rooms[r][c] == 0) q.add(new int[]{r, c});
    int[] dr = {1,-1,0,0}, dc = {0,0,1,-1};
    while (!q.isEmpty()) {
        int[] cur = q.poll();
        for (int d = 0; d < 4; d++) {
            int nr = cur[0] + dr[d], nc = cur[1] + dc[d];
            if (nr >= 0 && nr < R && nc >= 0 && nc < C && rooms[nr][nc] == Integer.MAX_VALUE) {
                rooms[nr][nc] = rooms[cur[0]][cur[1]] + 1;   // nearest gate
                q.add(new int[]{nr, nc});
            }
        }
    }
}   // O(R·C) time · O(R·C) space""",
            "python": r"""from collections import deque

def walls_and_gates(rooms):
    R, C = len(rooms), len(rooms[0])
    INF = 2 ** 31 - 1
    q = deque((r, c) for r in range(R) for c in range(C) if rooms[r][c] == 0)
    while q:                                  # one BFS, every gate a source
        r, c = q.popleft()
        for nr, nc in ((r+1,c), (r-1,c), (r,c+1), (r,c-1)):
            if 0 <= nr < R and 0 <= nc < C and rooms[nr][nc] == INF:
                rooms[nr][nc] = rooms[r][c] + 1   # first visit is the nearest
                q.append((nr, nc))""",
        },
    },
    {
        "slug": "number-of-provinces",
        "title": "Number of Provinces",
        "difficulty": "Medium",
        "pattern": "connected components (matrix input)",
        "statement": "isConnected[i][j] = 1 means city i and city j are directly connected. Return the number of provinces (connected components).",
        "examples": [("isConnected = [[1,1,0],[1,1,0],[0,0,1]]", "2"), ("isConnected = [[1,0,0],[0,1,0],[0,0,1]]", "3")],
        "constraints": ["1 <= n <= 200", "isConnected is symmetric with a 1 on the diagonal", "connections are transitive"],
        "approach": "Count components: scan for an unvisited city, run a traversal from it, and increase the counter. An adjacency matrix is fine at "
                     "this size — the same scan on a 10^6-node problem would need union-find or adjacency lists instead.",
        "complexity": ("O(n²)", "O(n)"),
        "code": {
            "cpp": r"""// Count components with one DFS per unvisited city
int findCircleNum(vector<vector<int>>& conn) {
    int n = conn.size(), provinces = 0;
    vector<bool> seen(n, false);
    for (int start = 0; start < n; start++) {
        if (seen[start]) continue;
        provinces++;                             // a new province begins here
        vector<int> st{start};
        seen[start] = true;
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (int v = 0; v < n; v++)
                if (conn[u][v] && !seen[v]) { seen[v] = true; st.push_back(v); }
        }
    }
    return provinces;
}   // O(n²) time · O(n) space""",
            "java": r"""// Count components with one DFS per unvisited city
int findCircleNum(int[][] conn) {
    int n = conn.length, provinces = 0;
    boolean[] seen = new boolean[n];
    for (int start = 0; start < n; start++) {
        if (seen[start]) continue;
        provinces++;                             // a new province begins here
        Deque<Integer> st = new ArrayDeque<>();
        st.push(start); seen[start] = true;
        while (!st.isEmpty()) {
            int u = st.pop();
            for (int v = 0; v < n; v++)
                if (conn[u][v] == 1 && !seen[v]) { seen[v] = true; st.push(v); }
        }
    }
    return provinces;
}   // O(n²) time · O(n) space""",
            "python": r"""def find_circle_num(is_connected):
    n = len(is_connected)
    seen = [False] * n
    provinces = 0
    for start in range(n):
        if seen[start]:
            continue
        provinces += 1                # a new province begins here
        stack = [start]
        seen[start] = True
        while stack:
            u = stack.pop()
            for v in range(n):
                if is_connected[u][v] and not seen[v]:
                    seen[v] = True
                    stack.append(v)
    return provinces""",
        },
    },
    {
        "slug": "redundant-connection",
        "title": "Redundant Connection",
        "difficulty": "Medium",
        "pattern": "union-find cycle detection",
        "statement": "A tree was turned into a graph by adding one extra edge; return that edge, choosing the last one in the input order if several "
                     "would work.",
        "examples": [("edges = [[1,2],[1,3],[2,3]]", "[2,3]"), ("edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]", "[1,4]")],
        "constraints": ["3 <= n <= 1000", "edges describe a connected graph with exactly one cycle", "the answer is unique in the given order"],
        "approach": "Union-find: add each edge, and the first edge whose two ends are already in the same set is the one that closes the cycle. "
                     "Path compression keeps each operation effectively constant, and processing in input order gives the required 'last valid' choice.",
        "complexity": ("O(n · α(n))", "O(n)"),
        "code": {
            "cpp": r"""// Union-find: the edge that joins two known nodes closes the cycle
struct DSU {
    vector<int> parent, rank_;
    DSU(int n) : parent(n + 1), rank_(n + 1, 0) { iota(parent.begin(), parent.end(), 0); }
    int find(int x) { return parent[x] == x ? x : parent[x] = find(parent[x]); }   // path compression
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;                // already connected
        if (rank_[a] < rank_[b]) swap(a, b);
        parent[b] = a;
        if (rank_[a] == rank_[b]) rank_[a]++;
        return true;
    }
};
vector<int> findRedundantConnection(vector<vector<int>>& edges) {
    DSU dsu(edges.size());
    for (auto& e : edges)
        if (!dsu.unite(e[0], e[1])) return e;    // this edge closes a cycle
    return {};
}   // O(n · α(n)) time · O(n) space""",
            "java": r"""// Union-find: the edge that joins two known nodes closes the cycle
class DSU {
    int[] parent, rank;
    DSU(int n) { parent = new int[n + 1]; rank = new int[n + 1];
                 for (int i = 0; i <= n; i++) parent[i] = i; }
    int find(int x) { return parent[x] == x ? x : (parent[x] = find(parent[x])); }
    boolean unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;                // already connected
        if (rank[a] < rank[b]) { int t = a; a = b; b = t; }
        parent[b] = a;
        if (rank[a] == rank[b]) rank[a]++;
        return true;
    }
}
int[] findRedundantConnection(int[][] edges) {
    DSU dsu = new DSU(edges.length);
    for (int[] e : edges)
        if (!dsu.unite(e[0], e[1])) return e;    // this edge closes a cycle
    return new int[0];
}   // O(n · α(n)) time · O(n) space""",
            "python": r"""def find_redundant_connection(edges):
    parent = list(range(len(edges) + 1))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]    # path compression
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return [a, b]                    # this edge closes the cycle
        parent[ra] = rb
    return []""",
        },
    },
    {
        "slug": "accounts-merge",
        "title": "Accounts Merge",
        "difficulty": "Medium",
        "pattern": "union-find over emails",
        "statement": "Each account is [name, email1, email2, ...]. Accounts sharing any email belong to the same person; merge them and return each "
                     "merged account as [name, sorted emails].",
        "examples": [("accounts = [[\"John\",\"johnsmith@mail.com\",\"john_newyork@mail.com\"],[\"John\",\"johnsmith@mail.com\",\"john00@mail.com\"],[\"Mary\",\"mary@mail.com\"],[\"John\",\"johnnybravo@mail.com\"]]",
                      "[[\"John\",\"john00@mail.com\",\"john_newyork@mail.com\",\"johnsmith@mail.com\"],[\"Mary\",\"mary@mail.com\"],[\"John\",\"johnnybravo@mail.com\"]]")],
        "constraints": ["1 <= number of accounts <= 1000", "1 <= emails per account <= 10", "names are not unique but emails identify a person"],
        "approach": "Emails are the real vertices, so union every email in an account with the account's first email. Then group emails by their "
                     "root, attach the name from any member, and sort — unioning through a representative avoids comparing accounts pairwise.",
        "complexity": ("O(total emails · α)", "O(total emails)"),
        "code": {
            "cpp": r"""// Union the emails inside each account; group by root
struct DSU {
    unordered_map<string, string> parent;        // email -> parent email
    string find(const string& x) {
        if (parent[x] != x) parent[x] = find(parent[x]);   // path compression
        return parent[x];
    }
};
vector<vector<string>> accountsMerge(vector<vector<string>>& accounts) {
    DSU dsu;
    unordered_map<string, string> owner;         // email -> name
    for (auto& acc : accounts)
        for (int i = 1; i < (int)acc.size(); i++) {
            if (!dsu.parent.count(acc[i])) dsu.parent[acc[i]] = acc[i];
            owner[acc[i]] = acc[0];
            dsu.parent[dsu.find(acc[i])] = dsu.find(acc[1]);   // union with the first
        }
    unordered_map<string, vector<string>> groups;   // root -> emails
    for (auto& [email, _] : dsu.parent) groups[dsu.find(email)].push_back(email);
    vector<vector<string>> out;
    for (auto& [root, emails] : groups) {
        sort(emails.begin(), emails.end());
        vector<string> merged{owner[root]};       // the name comes from any member
        merged.insert(merged.end(), emails.begin(), emails.end());
        out.push_back(merged);
    }
    return out;
}   // O(E · α) time · O(E) space""",
            "java": r"""// Union the emails inside each account; group by root
class DSU {
    Map<String, String> parent = new HashMap<>();   // email -> parent email
    String find(String x) {
        if (!parent.get(x).equals(x)) parent.put(x, find(parent.get(x)));
        return parent.get(x);
    }
}
List<List<String>> accountsMerge(List<List<String>> accounts) {
    DSU dsu = new DSU();
    Map<String, String> owner = new HashMap<>();    // email -> name
    for (List<String> acc : accounts)
        for (int i = 1; i < acc.size(); i++) {
            dsu.parent.putIfAbsent(acc.get(i), acc.get(i));
            owner.put(acc.get(i), acc.get(0));
            dsu.parent.put(dsu.find(acc.get(i)), dsu.find(acc.get(1)));   // union
        }
    Map<String, List<String>> groups = new HashMap<>();   // root -> emails
    for (String email : dsu.parent.keySet())
        groups.computeIfAbsent(dsu.find(email), k -> new ArrayList<>()).add(email);
    List<List<String>> out = new ArrayList<>();
    for (var entry : groups.entrySet()) {
        List<String> emails = entry.getValue();
        Collections.sort(emails);
        List<String> merged = new ArrayList<>();
        merged.add(owner.get(entry.getKey()));      // the name comes from a member
        merged.addAll(emails);
        out.add(merged);
    }
    return out;
}   // O(E · α) time · O(E) space""",
            "python": r"""def accounts_merge(accounts):
    parent = {}                       # email -> parent email
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]      # path compression
            x = parent[x]
        return x

    owner = {}                        # email -> name
    for acc in accounts:
        for email in acc[1:]:
            parent.setdefault(email, email)
            owner[email] = acc[0]
            parent[find(email)] = find(acc[1])   # union with the first email

    groups = {}
    for email in parent:
        groups.setdefault(find(email), []).append(email)
    return [[owner[root]] + sorted(emails) for root, emails in groups.items()]""",
        },
    },
    {
        "slug": "graph-valid-tree",
        "title": "Graph Valid Tree",
        "difficulty": "Medium",
        "pattern": "n-1 edges + no cycle",
        "statement": "Given n nodes and a list of undirected edges, decide whether they form a valid tree.",
        "examples": [("n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]", "true"), ("n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]", "false")],
        "constraints": ["1 <= n <= 2000", "0 <= edges <= 5000", "a tree has exactly n-1 edges and no cycle"],
        "approach": "A tree is connected *and* acyclic, which for a graph with n vertices is equivalent to having exactly n-1 edges and no cycle. "
                     "Union-find checks both in one pass: reject an edge that joins two already-connected nodes, and count the edges taken.",
        "complexity": ("O(n · α(n))", "O(n)"),
        "code": {
            "cpp": r"""// Tree ⇔ exactly n-1 edges and never a cycle
struct DSU {
    vector<int> parent;
    DSU(int n) : parent(n) { iota(parent.begin(), parent.end(), 0); }
    int find(int x) { return parent[x] == x ? x : parent[x] = find(parent[x]); }
};
bool validTree(int n, vector<vector<int>>& edges) {
    if ((int)edges.size() != n - 1) return false;   // too few or too many
    DSU dsu(n);
    for (auto& e : edges) {
        int a = dsu.find(e[0]), b = dsu.find(e[1]);
        if (a == b) return false;                   // a cycle
        dsu.parent[a] = b;
    }
    return true;                                    // n-1 edges, no cycle ⇒ tree
}   // O(n · α(n)) time · O(n) space""",
            "java": r"""// Tree ⇔ exactly n-1 edges and never a cycle
class DSU {
    int[] parent;
    DSU(int n) { parent = new int[n]; for (int i = 0; i < n; i++) parent[i] = i; }
    int find(int x) { return parent[x] == x ? x : (parent[x] = find(parent[x])); }
}
boolean validTree(int n, int[][] edges) {
    if (edges.length != n - 1) return false;        // too few or too many
    DSU dsu = new DSU(n);
    for (int[] e : edges) {
        int a = dsu.find(e[0]), b = dsu.find(e[1]);
        if (a == b) return false;                   // a cycle
        dsu.parent[a] = b;
    }
    return true;                                    // n-1 edges, no cycle ⇒ tree
}   // O(n · α(n)) time · O(n) space""",
            "python": r"""def valid_tree(n, edges):
    if len(edges) != n - 1:
        return False                 # too few edges means disconnected
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False             # a cycle
        parent[ra] = rb
    return True                      # n-1 edges and no cycle ⇒ connected tree""",
        },
    },
    # ------------------------------------------------------------------ HARD
    {
        "slug": "word-ladder",
        "title": "Word Ladder",
        "difficulty": "Hard",
        "pattern": "BFS over generated wildcard states",
        "statement": "Change one letter at a time from beginWord to endWord, where every intermediate word must be in the dictionary. Return the "
                     "number of words in the shortest such sequence, or 0 if none exists.",
        "examples": [("beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\",\"cog\"]", "5"),
                     ("beginWord = \"hit\", endWord = \"cog\", wordList = [\"hot\",\"dot\",\"dog\",\"lot\",\"log\"]", "0")],
        "constraints": ["1 <= word length <= 10", "1 <= wordList size <= 5000", "all words have the same length and lowercase letters"],
        "approach": "Comparing every pair of words costs O(n² · L); instead bucket words by their wildcard patterns (h*t, *ot, ...) once, and the "
                     "BFS then moves between words that share a pattern. The bucket index *is* the adjacency list, and building it once is the whole "
                     "optimisation.",
        "complexity": ("O(n · L²)", "O(n · L)"),
        "code": {
            "cpp": r"""// Wildcard buckets act as the adjacency list
int ladderLength(string begin, string end, vector<string>& words) {
    unordered_set<string> dict(words.begin(), words.end());
    if (!dict.count(end)) return 0;
    unordered_map<string, vector<string>> buckets;      // "*ot" -> words
    for (const string& w : words)
        for (int i = 0; i < (int)w.size(); i++) {
            string key = w; key[i] = '*';
            buckets[key].push_back(w);
        }
    unordered_set<string> seen{begin};
    queue<pair<string, int>> q; q.push({begin, 1});
    while (!q.empty()) {
        auto [word, steps] = q.front(); q.pop();
        if (word == end) return steps;
        for (int i = 0; i < (int)word.size(); i++) {
            string key = word; key[i] = '*';
            for (const string& nb : buckets[key])            // one letter away
                if (seen.insert(nb).second) q.push({nb, steps + 1});
        }
    }
    return 0;
}   // O(n · L²) time · O(n · L) space""",
            "java": r"""// Wildcard buckets act as the adjacency list
int ladderLength(String begin, String end, List<String> words) {
    Set<String> dict = new HashSet<>(words);
    if (!dict.contains(end)) return 0;
    Map<String, List<String>> buckets = new HashMap<>();  // "*ot" -> words
    for (String w : words)
        for (int i = 0; i < w.length(); i++) {
            String key = w.substring(0, i) + '*' + w.substring(i + 1);
            buckets.computeIfAbsent(key, k -> new ArrayList<>()).add(w);
        }
    Set<String> seen = new HashSet<>();
    seen.add(begin);
    Deque<Object[]> q = new ArrayDeque<>();               // {word, steps}
    q.add(new Object[]{begin, 1});
    while (!q.isEmpty()) {
        Object[] cur = q.poll();
        String word = (String) cur[0];
        int steps = (Integer) cur[1];
        if (word.equals(end)) return steps;
        for (int i = 0; i < word.length(); i++) {
            String key = word.substring(0, i) + '*' + word.substring(i + 1);
            for (String nb : buckets.getOrDefault(key, List.of()))
                if (seen.add(nb)) q.add(new Object[]{nb, steps + 1});   // one away
        }
    }
    return 0;
}   // O(n · L²) time · O(n · L) space""",
            "python": r"""from collections import deque

def ladder_length(begin, end, words):
    if end not in words:
        return 0
    buckets = {}                     # "*ot" -> words matching that pattern
    for w in words:
        for i in range(len(w)):
            buckets.setdefault(w[:i] + '*' + w[i+1:], []).append(w)
    seen = {begin}
    q = deque([(begin, 1)])
    while q:
        word, steps = q.popleft()
        if word == end:
            return steps
        for i in range(len(word)):
            key = word[:i] + '*' + word[i+1:]
            for nb in buckets.get(key, ()):        # one letter away
                if nb not in seen:
                    seen.add(nb)
                    q.append((nb, steps + 1))
    return 0""",
        },
    },
    {
        "slug": "alien-dictionary",
        "title": "Alien Dictionary",
        "difficulty": "Hard",
        "pattern": "topological sort from adjacent words",
        "statement": "The words are sorted by an unknown alphabet. Derive a valid character order, or return the empty string if none exists.",
        "examples": [("words = [\"wrt\",\"wrf\",\"er\",\"ett\",\"rftt\"]", "\"wertf\""),
                     ("words = [\"z\",\"x\"]", "\"zx\"")],
        "constraints": ["1 <= number of words <= 100", "1 <= word length <= 100", "the order may be impossible, e.g. [\"abc\",\"ab\"]"],
        "approach": "Comparing each pair of adjacent words reveals exactly one ordering constraint — the first position where they differ. Collect those "
                     "edges, topologically sort the resulting character graph, and return \"\" if a cycle appears or a prefix word comes later than its "
                     "extension.",
        "complexity": ("O(total characters)", "O(unique characters)"),
        "code": {
            "cpp": r"""// Adjacent pairs give one order edge; topologically sort them
string alienOrder(vector<string>& words) {
    unordered_map<char, unordered_set<char>> adj;
    unordered_map<char, int> indeg;
    for (const string& w : words) for (char c : w) indeg[c] = indeg[c];   // ensure keys
    for (size_t i = 0; i + 1 < words.size(); i++) {
        const string& a = words[i]; const string& b = words[i + 1];
        size_t j = 0;
        while (j < a.size() && j < b.size() && a[j] == b[j]) j++;
        if (j == b.size() && j < a.size()) return "";   // "abc" before "ab": invalid
        if (j < a.size() && j < b.size() && !adj[a[j]].count(b[j])) {
            adj[a[j]].insert(b[j]);                     // a[j] comes before b[j]
            indeg[b[j]]++;
        }
    }
    queue<char> ready;
    for (auto& [ch, d] : indeg) if (d == 0) ready.push(ch);
    string order;
    while (!ready.empty()) {
        char u = ready.front(); ready.pop();
        order += u;
        for (char v : adj[u]) if (--indeg[v] == 0) ready.push(v);
    }
    return order.size() == indeg.size() ? order : "";   // cycle ⇒ impossible
}   // O(total characters) time · O(1) space (26 letters)""",
            "java": r"""// Adjacent pairs give one order edge; topologically sort them
String alienOrder(String[] words) {
    Map<Character, Set<Character>> adj = new HashMap<>();
    Map<Character, Integer> indeg = new HashMap<>();
    for (String w : words) for (char c : w.toCharArray()) indeg.putIfAbsent(c, 0);
    for (int i = 0; i + 1 < words.length; i++) {
        String a = words[i], b = words[i + 1];
        int j = 0;
        while (j < a.length() && j < b.length() && a.charAt(j) == b.charAt(j)) j++;
        if (j == b.length() && j < a.length()) return "";   // "abc" before "ab"
        if (j < a.length() && j < b.length()) {
            char from = a.charAt(j), to = b.charAt(j);
            if (!adj.getOrDefault(from, Set.of()).contains(to)) {
                adj.computeIfAbsent(from, k -> new HashSet<>()).add(to);   // edge
                indeg.merge(to, 1, Integer::sum);
            }
        }
    }
    Deque<Character> ready = new ArrayDeque<>();
    for (var e : indeg.entrySet()) if (e.getValue() == 0) ready.add(e.getKey());
    StringBuilder order = new StringBuilder();
    while (!ready.isEmpty()) {
        char u = ready.poll();
        order.append(u);
        for (char v : adj.getOrDefault(u, Set.of()))
            if (indeg.merge(v, -1, Integer::sum) == 0) ready.add(v);
    }
    return order.length() == indeg.size() ? order.toString() : "";   // cycle
}   // O(total characters) time · O(1) space (26 letters)""",
            "python": r"""from collections import deque

def alien_order(words):
    adj = {c: set() for w in words for c in w}     # character graph
    indeg = {c: 0 for w in words for c in w}
    for a, b in zip(words, words[1:]):
        j = 0
        while j < len(a) and j < len(b) and a[j] == b[j]:
            j += 1
        if j == len(b) and j < len(a):
            return ''                # e.g. "abc" before "ab": impossible
        if j < len(a) and j < len(b) and b[j] not in adj[a[j]]:
            adj[a[j]].add(b[j])      # a[j] comes before b[j]
            indeg[b[j]] += 1
    ready = deque(c for c, d in indeg.items() if d == 0)
    order = []
    while ready:
        u = ready.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    return ''.join(order) if len(order) == len(indeg) else ''   # cycle ⇒ ''""",
        },
    },
    {
        "slug": "network-delay-time",
        "title": "Network Delay Time",
        "difficulty": "Hard",
        "pattern": "Dijkstra with a priority queue",
        "statement": "Signals travel along directed edges with given travel times. Starting from node k, return the time for all n nodes to receive the "
                     "signal, or -1 if some node never does.",
        "examples": [("times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2", "2"),
                     ("times = [[1,2,1]], n = 2, k = 2", "-1")],
        "constraints": ["1 <= k <= n <= 100", "1 <= number of edges <= 6000", "edge weights are positive, so Dijkstra applies"],
        "approach": "Dijkstra: repeatedly settle the nearest unsettled node with a min-heap, relaxing its outgoing edges. The answer is the largest "
                     "settled distance — if any node is left unsettled, some are unreachable and the answer is -1. The heap is what keeps the "
                     "extract-min step logarithmic.",
        "complexity": ("O(m log n)", "O(n + m)"),
        "code": {
            "cpp": r"""// Dijkstra: settle the nearest node, relax its edges
int networkDelayTime(vector<vector<int>>& times, int n, int k) {
    vector<vector<pair<int,int>>> adj(n + 1);    // u -> (v, weight)
    for (auto& t : times) adj[t[0]].push_back({t[1], t[2]});
    vector<int> dist(n + 1, INT_MAX);
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;   // min-heap
    dist[k] = 0;
    pq.push({0, k});                             // (distance, node)
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;               // stale entry: skip it
        for (auto [v, w] : adj[u])
            if (d + w < dist[v]) {               // relax the edge
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
    }
    int worst = 0;
    for (int u = 1; u <= n; u++) {
        if (dist[u] == INT_MAX) return -1;        // unreachable node
        worst = max(worst, dist[u]);
    }
    return worst;
}   // O(m log n) time · O(n + m) space""",
            "java": r"""// Dijkstra: settle the nearest node, relax its edges
int networkDelayTime(int[][] times, int n, int k) {
    List<List<int[]>> adj = new ArrayList<>();
    for (int i = 0; i <= n; i++) adj.add(new ArrayList<>());
    for (int[] t : times) adj.get(t[0]).add(new int[]{t[1], t[2]});   // u -> (v, w)
    int[] dist = new int[n + 1];
    Arrays.fill(dist, Integer.MAX_VALUE);
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);   // min-heap
    dist[k] = 0;
    pq.add(new int[]{0, k});                     // (distance, node)
    while (!pq.isEmpty()) {
        int[] cur = pq.poll();
        int d = cur[0], u = cur[1];
        if (d > dist[u]) continue;               // stale entry: skip it
        for (int[] e : adj.get(u))
            if (d + e[1] < dist[e[0]]) {         // relax the edge
                dist[e[0]] = d + e[1];
                pq.add(new int[]{dist[e[0]], e[0]});
            }
    }
    int worst = 0;
    for (int u = 1; u <= n; u++) {
        if (dist[u] == Integer.MAX_VALUE) return -1;   // unreachable node
        worst = Math.max(worst, dist[u]);
    }
    return worst;
}   // O(m log n) time · O(n + m) space""",
            "python": r"""import heapq

def network_delay_time(times, n, k):
    adj = [[] for _ in range(n + 1)]        # u -> [(v, weight)]
    for u, v, w in times:
        adj[u].append((v, w))
    dist = [float('inf')] * (n + 1)
    dist[k] = 0
    pq = [(0, k)]                           # (distance, node), a min-heap
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue                        # stale entry
        for v, w in adj[u]:
            if d + w < dist[v]:             # relax the edge
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    worst = max(dist[1:])
    return -1 if worst == float('inf') else worst""",
        },
    },
    {
        "slug": "cheapest-flights-within-k-stops",
        "title": "Cheapest Flights Within K Stops",
        "difficulty": "Hard",
        "pattern": "Bellman-Ford limited to k+1 rounds",
        "statement": "Find the cheapest price from src to dst using at most k stops, or -1 if there is none.",
        "examples": [("n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], src = 0, dst = 3, k = 1", "700"),
                     ("same flights, k = 0", "-1")],
        "constraints": ["1 <= n <= 100", "0 <= flights <= n²", "0 <= price <= 10^4; a node may be revisited with fewer stops"],
        "approach": "Dijkstra alone fails here because a cheaper-but-longer path can violate the stop limit. Bellman-Ford with exactly k+1 rounds "
                     "counts the edges along each path: relaxing from a *snapshot* of the previous round (never from values updated this round) is "
                     "what enforces the limit.",
        "complexity": ("O(k · m)", "O(n)"),
        "code": {
            "cpp": r"""// k+1 relaxation rounds; each round works from a snapshot
int findCheapestPrice(int n, vector<vector<int>>& flights, int src, int dst, int k) {
    const int INF = 1e9;
    vector<int> dist(n, INF);
    dist[src] = 0;
    for (int round = 0; round <= k; round++) {
        vector<int> next = dist;                 // snapshot: at most one extra edge
        for (auto& f : flights) {
            int u = f[0], v = f[1], w = f[2];
            if (dist[u] != INF && dist[u] + w < next[v]) next[v] = dist[u] + w;
        }
        dist = move(next);
    }
    return dist[dst] == INF ? -1 : dist[dst];
}   // O(k · m) time · O(n) space""",
            "java": r"""// k+1 relaxation rounds; each round works from a snapshot
int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
    final int INF = 1_000_000_000;
    int[] dist = new int[n];
    Arrays.fill(dist, INF);
    dist[src] = 0;
    for (int round = 0; round <= k; round++) {
        int[] next = dist.clone();               // snapshot: at most one extra edge
        for (int[] f : flights)
            if (dist[f[0]] != INF && dist[f[0]] + f[2] < next[f[1]])
                next[f[1]] = dist[f[0]] + f[2];
        dist = next;
    }
    return dist[dst] == INF ? -1 : dist[dst];
}   // O(k · m) time · O(n) space""",
            "python": r"""def find_cheapest_price(n, flights, src, dst, k):
    INF = float('inf')
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):                 # at most k+1 edges may be used
        nxt = dist[:]                      # snapshot: only one extra edge per round
        for u, v, w in flights:
            if dist[u] != INF and dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
        dist = nxt
    return -1 if dist[dst] == INF else dist[dst]""",
        },
    },
    {
        "slug": "min-cost-to-connect-all-points",
        "title": "Minimum Cost to Connect All Points",
        "difficulty": "Hard",
        "pattern": "minimum spanning tree (Prim)",
        "statement": "Given points in the plane, connect them all so that the total Manhattan distance of the edges is minimal, and return that cost.",
        "examples": [("points = [[0,0],[2,2],[3,10],[5,2],[7,0]]", "20"), ("points = [[3,12],[-2,5],[-4,1]]", "18")],
        "constraints": ["1 <= n <= 1000", "-10^6 <= coordinates <= 10^6", "the graph is complete, so every pair is an edge"],
        "approach": "Prim's MST: grow a tree from one point, always adding the cheapest edge that leaves the tree. With a complete graph the "
                     "distances can be computed on the fly, so O(n²) time and no edge list is needed — that is why Prim fits this shape better "
                     "than Kruskal.",
        "complexity": ("O(n²)", "O(n)"),
        "code": {
            "cpp": r"""// Prim: repeatedly attach the nearest unvisited point
int minCostConnectPoints(vector<vector<int>>& pts) {
    int n = pts.size();
    vector<int> best(n, INT_MAX);                // cheapest edge into the tree
    vector<bool> inTree(n, false);
    best[0] = 0;
    int total = 0;
    for (int it = 0; it < n; it++) {
        int u = -1;                              // pick the nearest outside point
        for (int i = 0; i < n; i++)
            if (!inTree[i] && (u == -1 || best[i] < best[u])) u = i;
        inTree[u] = true;
        total += best[u];                        // attach it
        for (int v = 0; v < n; v++) {
            if (inTree[v]) continue;
            int d = abs(pts[u][0] - pts[v][0]) + abs(pts[u][1] - pts[v][1]);
            best[v] = min(best[v], d);           // relax the frontier
        }
    }
    return total;
}   // O(n²) time · O(n) space""",
            "java": r"""// Prim: repeatedly attach the nearest unvisited point
int minCostConnectPoints(int[][] pts) {
    int n = pts.length;
    int[] best = new int[n];                     // cheapest edge into the tree
    boolean[] inTree = new boolean[n];
    Arrays.fill(best, Integer.MAX_VALUE);
    best[0] = 0;
    int total = 0;
    for (int it = 0; it < n; it++) {
        int u = -1;                              // pick the nearest outside point
        for (int i = 0; i < n; i++)
            if (!inTree[i] && (u == -1 || best[i] < best[u])) u = i;
        inTree[u] = true;
        total += best[u];                        // attach it
        for (int v = 0; v < n; v++) {
            if (inTree[v]) continue;
            int d = Math.abs(pts[u][0] - pts[v][0]) + Math.abs(pts[u][1] - pts[v][1]);
            best[v] = Math.min(best[v], d);      // relax the frontier
        }
    }
    return total;
}   // O(n²) time · O(n) space""",
            "python": r"""def min_cost_connect_points(points):
    n = len(points)
    best = [float('inf')] * n        # cheapest edge into the growing tree
    in_tree = [False] * n
    best[0] = 0
    total = 0
    for _ in range(n):
        u = min((i for i in range(n) if not in_tree[i]), key=lambda i: best[i])
        in_tree[u] = True
        total += best[u]             # attach u to the tree
        for v in range(n):
            if in_tree[v]:
                continue
            d = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
            if d < best[v]:
                best[v] = d          # relax the frontier
    return total""",
        },
    },
    {
        "slug": "swim-in-rising-water",
        "title": "Swim in Rising Water",
        "difficulty": "Hard",
        "pattern": "Dijkstra on a bottleneck cost",
        "statement": "The grid gives the elevation of each cell; at time t the water level is t and you may swim between cells of height at most t. "
                     "Return the earliest time at which (0,0) and (n-1,n-1) become connected.",
        "examples": [("grid = [[0,2],[1,3]]", "3"), ("grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]", "16")],
        "constraints": ["1 <= n <= 50", "the grid is a permutation of 0..n²-1", "movement is 4-directional"],
        "approach": "The cost of a path is the *largest* cell on it, and the answer is the smallest such largest cell over all paths. Dijkstra works "
                     "with max instead of sum because the cost is monotone: relax a neighbour with max(current, neighbour height), the same "
                     "priority-queue shape with a different combine step.",
        "complexity": ("O(n² log n)", "O(n²)"),
        "code": {
            "cpp": r"""// Dijkstra where the path cost is the maximum cell instead of a sum
int swimInWater(vector<vector<int>>& g) {
    int n = g.size();
    vector<vector<int>> best(n, vector<int>(n, INT_MAX));
    priority_queue<array<int,3>, vector<array<int,3>>, greater<>> pq;   // (cost, r, c)
    best[0][0] = g[0][0];
    pq.push({g[0][0], 0, 0});
    int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    while (!pq.empty()) {
        auto [cost, r, c] = pq.top(); pq.pop();
        if (r == n - 1 && c == n - 1) return cost;
        if (cost > best[r][c]) continue;         // stale entry
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= n || nc < 0 || nc >= n) continue;
            int next = max(cost, g[nr][nc]);     // bottleneck, not sum
            if (next < best[nr][nc]) { best[nr][nc] = next; pq.push({next, nr, nc}); }
        }
    }
    return best[n-1][n-1];
}   // O(n² log n) time · O(n²) space""",
            "java": r"""// Dijkstra where the path cost is the maximum cell instead of a sum
int swimInWater(int[][] g) {
    int n = g.length;
    int[][] best = new int[n][n];
    for (int[] row : best) Arrays.fill(row, Integer.MAX_VALUE);
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
    best[0][0] = g[0][0];
    pq.add(new int[]{g[0][0], 0, 0});            // (cost, r, c)
    int[] dr = {1,-1,0,0}, dc = {0,0,1,-1};
    while (!pq.isEmpty()) {
        int[] cur = pq.poll();
        int cost = cur[0], r = cur[1], c = cur[2];
        if (r == n - 1 && c == n - 1) return cost;
        if (cost > best[r][c]) continue;         // stale entry
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= n || nc < 0 || nc >= n) continue;
            int next = Math.max(cost, g[nr][nc]);   // bottleneck, not sum
            if (next < best[nr][nc]) { best[nr][nc] = next; pq.add(new int[]{next, nr, nc}); }
        }
    }
    return best[n-1][n-1];
}   // O(n² log n) time · O(n²) space""",
            "python": r"""import heapq

def swim_in_water(grid):
    n = len(grid)
    best = [[float('inf')] * n for _ in range(n)]
    best[0][0] = grid[0][0]
    pq = [(grid[0][0], 0, 0)]        # (bottleneck cost, r, c)
    while pq:
        cost, r, c = heapq.heappop(pq)
        if r == n - 1 and c == n - 1:
            return cost
        if cost > best[r][c]:
            continue                 # stale entry
        for nr, nc in ((r+1,c), (r-1,c), (r,c+1), (r,c-1)):
            if 0 <= nr < n and 0 <= nc < n:
                nxt = max(cost, grid[nr][nc])      # bottleneck, not a sum
                if nxt < best[nr][nc]:
                    best[nr][nc] = nxt
                    heapq.heappush(pq, (nxt, nr, nc))
    return best[n-1][n-1]""",
        },
    },
    {
        "slug": "path-with-minimum-effort",
        "title": "Path With Minimum Effort",
        "difficulty": "Hard",
        "pattern": "Dijkstra on absolute differences",
        "statement": "The effort of a path is the largest absolute height difference between consecutive cells. Return the minimum effort over all "
                     "paths from the top-left to the bottom-right.",
        "examples": [("heights = [[1,2,2],[3,8,2],[5,3,5]]", "2"), ("heights = [[1,2,3],[3,8,4],[5,3,5]]", "1")],
        "constraints": ["1 <= rows, cols <= 100", "1 <= heights <= 10^6", "movement is 4-directional"],
        "approach": "Identical to the rising-water problem with a different bottleneck: the edge weight is the absolute difference between neighbouring "
                     "cells, and the path cost is the maximum such weight. Recognising that the two problems share one template is the point of the "
                     "pair.",
        "complexity": ("O(R·C log(R·C))", "O(R·C)"),
        "code": {
            "cpp": r"""// Same bottleneck Dijkstra, with edge weight |difference|
int minimumEffortPath(vector<vector<int>>& h) {
    int R = h.size(), C = h[0].size();
    vector<vector<int>> best(R, vector<int>(C, INT_MAX));
    priority_queue<array<int,3>, vector<array<int,3>>, greater<>> pq;   // (effort, r, c)
    best[0][0] = 0;
    pq.push({0, 0, 0});
    int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    while (!pq.empty()) {
        auto [effort, r, c] = pq.top(); pq.pop();
        if (r == R - 1 && c == C - 1) return effort;
        if (effort > best[r][c]) continue;       // stale entry
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= R || nc < 0 || nc >= C) continue;
            int next = max(effort, abs(h[nr][nc] - h[r][c]));   // bottleneck
            if (next < best[nr][nc]) { best[nr][nc] = next; pq.push({next, nr, nc}); }
        }
    }
    return best[R-1][C-1];
}   // O(R·C log(R·C)) time · O(R·C) space""",
            "java": r"""// Same bottleneck Dijkstra, with edge weight |difference|
int minimumEffortPath(int[][] h) {
    int R = h.length, C = h[0].length;
    int[][] best = new int[R][C];
    for (int[] row : best) Arrays.fill(row, Integer.MAX_VALUE);
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
    best[0][0] = 0;
    pq.add(new int[]{0, 0, 0});                  // (effort, r, c)
    int[] dr = {1,-1,0,0}, dc = {0,0,1,-1};
    while (!pq.isEmpty()) {
        int[] cur = pq.poll();
        int effort = cur[0], r = cur[1], c = cur[2];
        if (r == R - 1 && c == C - 1) return effort;
        if (effort > best[r][c]) continue;       // stale entry
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= R || nc < 0 || nc >= C) continue;
            int next = Math.max(effort, Math.abs(h[nr][nc] - h[r][c]));
            if (next < best[nr][nc]) { best[nr][nc] = next; pq.add(new int[]{next, nr, nc}); }
        }
    }
    return best[R-1][C-1];
}   // O(R·C log(R·C)) time · O(R·C) space""",
            "python": r"""import heapq

def minimum_effort_path(heights):
    R, C = len(heights), len(heights[0])
    best = [[float('inf')] * C for _ in range(R)]
    best[0][0] = 0
    pq = [(0, 0, 0)]                 # (effort, r, c)
    while pq:
        effort, r, c = heapq.heappop(pq)
        if r == R - 1 and c == C - 1:
            return effort
        if effort > best[r][c]:
            continue                 # stale entry
        for nr, nc in ((r+1,c), (r-1,c), (r,c+1), (r,c-1)):
            if 0 <= nr < R and 0 <= nc < C:
                nxt = max(effort, abs(heights[nr][nc] - heights[r][c]))
                if nxt < best[nr][nc]:
                    best[nr][nc] = nxt
                    heapq.heappush(pq, (nxt, nr, nc))
    return best[R-1][C-1]""",
        },
    },
    {
        "slug": "critical-connections-in-a-network",
        "title": "Critical Connections (Bridges)",
        "difficulty": "Hard",
        "pattern": "Tarjan bridges via DFS discovery times",
        "statement": "Return every edge whose removal disconnects the network (a bridge), in any order.",
        "examples": [("n = 4, connections = [[0,1],[1,2],[2,0],[1,3]]", "[[1,3]]"),
                     ("n = 2, connections = [[0,1]]", "[[0,1]]")],
        "constraints": ["2 <= n <= 10^5", "n - 1 <= connections <= 10^5", "the graph is connected with no repeated edges"],
        "approach": "An edge (u, v) is a bridge exactly when the subtree under v has no way back to u or above it. The DFS records a discovery time "
                     "and a low-link value per node; if low[v] > disc[u], nothing below v reaches u, so the edge is critical. The parent edge must be "
                     "skipped by *edge id*, not by node, because parallel edges would otherwise be mistaken for the parent.",
        "complexity": ("O(n + m)", "O(n + m)"),
        "code": {
            "cpp": r"""// Bridges: low[child] > disc[parent] means the edge is critical
class Solver {
public:
    vector<vector<pair<int,int>>> adj;           // (neighbour, edge id)
    vector<int> disc, low;
    vector<vector<int>> bridges;
    int timer = 0;
    void dfs(int u, int parentEdge) {
        disc[u] = low[u] = ++timer;
        for (auto [v, id] : adj[u]) {
            if (id == parentEdge) continue;      // skip the edge we came from
            if (disc[v]) low[u] = min(low[u], disc[v]);       // back edge
            else {
                dfs(v, id);
                low[u] = min(low[u], low[v]);
                if (low[v] > disc[u]) bridges.push_back({u, v});   // bridge
            }
        }
    }
    vector<vector<int>> criticalConnections(int n, vector<vector<int>>& conn) {
        adj.assign(n, {});
        for (int i = 0; i < (int)conn.size(); i++) {          // give every edge an id
            adj[conn[i][0]].push_back({conn[i][1], i});
            adj[conn[i][1]].push_back({conn[i][0], i});
        }
        disc.assign(n, 0); low.assign(n, 0);
        bridges.clear(); timer = 0;
        for (int u = 0; u < n; u++) if (!disc[u]) dfs(u, -1);
        return bridges;
    }
};   // O(n + m) time · O(n + m) space""",
            "java": r"""// Bridges: low[child] > disc[parent] means the edge is critical
class Solver {
    List<List<int[]>> adj;                       // (neighbour, edge id)
    int[] disc, low;
    List<List<Integer>> bridges = new ArrayList<>();
    int timer = 0;
    void dfs(int u, int parentEdge) {
        disc[u] = low[u] = ++timer;
        for (int[] e : adj.get(u)) {
            int v = e[0], id = e[1];
            if (id == parentEdge) continue;      // skip the edge we came from
            if (disc[v] != 0) low[u] = Math.min(low[u], disc[v]);   // back edge
            else {
                dfs(v, id);
                low[u] = Math.min(low[u], low[v]);
                if (low[v] > disc[u]) bridges.add(Arrays.asList(u, v));   // bridge
            }
        }
    }
    List<List<Integer>> criticalConnections(int n, List<List<Integer>> conn) {
        adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int i = 0; i < conn.size(); i++) {      // give every edge an id
            int a = conn.get(i).get(0), b = conn.get(i).get(1);
            adj.get(a).add(new int[]{b, i});
            adj.get(b).add(new int[]{a, i});
        }
        disc = new int[n]; low = new int[n];
        bridges.clear(); timer = 0;
        for (int u = 0; u < n; u++) if (disc[u] == 0) dfs(u, -1);
        return bridges;
    }
}   // O(n + m) time · O(n + m) space""",
            "python": r"""import sys

def critical_connections(n, connections):
    sys.setrecursionlimit(300000)
    adj = [[] for _ in range(n)]      # (neighbour, edge id)
    for i, (a, b) in enumerate(connections):
        adj[a].append((b, i))
        adj[b].append((a, i))
    disc = [0] * n                    # discovery times
    low = [0] * n                     # earliest reachable discovery time
    bridges = []
    timer = 0

    def dfs(u, parent_edge):
        nonlocal timer
        timer += 1
        disc[u] = low[u] = timer
        for v, eid in adj[u]:
            if eid == parent_edge:
                continue              # skip the edge we arrived on
            if disc[v]:
                low[u] = min(low[u], disc[v])      # back edge
            else:
                dfs(v, eid)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append([u, v])         # nothing below reaches u

    for u in range(n):
        if not disc[u]:
            dfs(u, -1)
    return bridges""",
        },
    },
    {
        "slug": "remove-max-number-of-edges-to-keep-graph-fully-traversable",
        "title": "Remove Max Number of Edges to Keep Graph Fully Traversable",
        "difficulty": "Hard",
        "pattern": "one union-find per traveller, shared edges first",
        "statement": "Alice may walk type 1 and type 3 edges, Bob type 2 and type 3, and every edge is undirected. Return the maximum number of edges "
                     "that can be removed so that each of them can still travel between any two nodes, or -1 if that is impossible.",
        "examples": [("n = 4, edges = [[3,1,2],[3,2,3],[1,1,3],[1,2,4],[1,1,2],[2,3,4]]", "2"),
                     ("n = 4, edges = [[3,1,2],[3,2,3],[1,1,4],[2,1,4]]", "0"),
                     ("n = 4, edges = [[3,2,3],[1,1,2],[2,3,4]]", "-1")],
        "constraints": ["1 <= n <= 10^5", "1 <= edges.length <= 10^5", "type 1 belongs to Alice, type 2 to Bob, type 3 to both",
                        "edges[i] = [type, u, v] with 1 <= u, v <= n and u != v"],
        "approach": "Alice and Bob need separate union-find structures, because an edge may be useful to one and pointless to the other. Process the "
                     "type 3 edges first — they are the most valuable, since they can serve both travellers — and count one as removable only when "
                     "*neither* structure needed it. Then do the same for the private type 1 and type 2 edges. Finally both structures must reduce to a "
                     "single component; otherwise one of the two is stuck and the answer is -1.",
        "complexity": ("O(m · α(n))", "O(n)"),
        "code": {
            "cpp": r"""// One DSU per traveller; shared edges first, then private ones
struct DSU {
    vector<int> parent, rank_;
    int components;
    DSU(int n) : parent(n + 1), rank_(n + 1, 0), components(n) {
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int x) { return parent[x] == x ? x : parent[x] = find(parent[x]); }
    bool unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        if (rank_[a] < rank_[b]) swap(a, b);
        parent[b] = a;
        if (rank_[a] == rank_[b]) rank_[a]++;
        components--;                            // one merge, one fewer component
        return true;
    }
};
int maxNumEdgesToRemove(int n, vector<vector<int>>& edges) {
    DSU alice(n), bob(n);
    int removed = 0;
    for (auto& e : edges)                        // shared edges are the most valuable
        if (e[0] == 3) {
            bool a = alice.unite(e[1], e[2]);
            bool b = bob.unite(e[1], e[2]);
            if (!a && !b) removed++;             // useful to neither traveller
        }
    for (auto& e : edges) {
        if (e[0] == 1 && !alice.unite(e[1], e[2])) removed++;
        if (e[0] == 2 && !bob.unite(e[1], e[2])) removed++;
    }
    if (alice.components > 1 || bob.components > 1) return -1;   // someone is stuck
    return removed;
}   // O(m · α(n)) time · O(n) space""",
            "java": r"""// One DSU per traveller; shared edges first, then private ones
class DSU {
    int[] parent, rank;
    int components;
    DSU(int n) {
        parent = new int[n + 1]; rank = new int[n + 1]; components = n;
        for (int i = 0; i <= n; i++) parent[i] = i;
    }
    int find(int x) { return parent[x] == x ? x : (parent[x] = find(parent[x])); }
    boolean unite(int a, int b) {
        a = find(a); b = find(b);
        if (a == b) return false;
        if (rank[a] < rank[b]) { int t = a; a = b; b = t; }
        parent[b] = a;
        if (rank[a] == rank[b]) rank[a]++;
        components--;                            // one merge, one fewer component
        return true;
    }
}
int maxNumEdgesToRemove(int n, int[][] edges) {
    DSU alice = new DSU(n), bob = new DSU(n);
    int removed = 0;
    for (int[] e : edges)                        // shared edges are the most valuable
        if (e[0] == 3) {
            boolean a = alice.unite(e[1], e[2]);
            boolean b = bob.unite(e[1], e[2]);
            if (!a && !b) removed++;             // useful to neither traveller
        }
    for (int[] e : edges) {
        if (e[0] == 1 && !alice.unite(e[1], e[2])) removed++;
        if (e[0] == 2 && !bob.unite(e[1], e[2])) removed++;
    }
    if (alice.components > 1 || bob.components > 1) return -1;   // someone is stuck
    return removed;
}   // O(m · α(n)) time · O(n) space""",
            "python": r"""def max_num_edges_to_remove(n, edges):
    parent_a = list(range(n + 1))     # Alice's forest
    parent_b = list(range(n + 1))     # Bob's forest

    def find(parent, x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def unite(parent, a, b):
        ra, rb = find(parent, a), find(parent, b)
        if ra == rb:
            return False
        parent[ra] = rb
        return True

    removed = 0
    for typ, u, v in edges:              # shared edges are the most valuable
        if typ == 3:
            a = unite(parent_a, u, v)
            b = unite(parent_b, u, v)
            if not a and not b:
                removed += 1             # useful to neither traveller
    for typ, u, v in edges:
        if typ == 1 and not unite(parent_a, u, v):
            removed += 1
        if typ == 2 and not unite(parent_b, u, v):
            removed += 1
    root_a, root_b = find(parent_a, 1), find(parent_b, 1)
    for u in range(2, n + 1):
        if find(parent_a, u) != root_a or find(parent_b, u) != root_b:
            return -1                    # someone cannot reach every node
    return removed""",
        },
    },
    {
        "slug": "number-of-ways-to-arrive-at-destination",
        "title": "Number of Ways to Arrive at Destination",
        "difficulty": "Hard",
        "pattern": "Dijkstra with path counting",
        "statement": "Count the paths from node 0 to node n-1 that have the shortest total travel time, modulo 10^9 + 7.",
        "examples": [("n = 7, roads = [[0,6,7],[0,1,2],[1,2,3],[1,3,3],[6,3,3],[3,5,1],[6,5,1],[2,5,1],[0,4,5],[4,6,2]]", "4"),
                     ("n = 2, roads = [[1,0,10]]", "1")],
        "constraints": ["1 <= n <= 200", "0 <= roads <= n · (n - 1) / 2", "weights are positive; the graph is connected"],
        "approach": "Run Dijkstra, but maintain two arrays: the shortest distance and the number of shortest paths reaching each node. When a "
                     "relaxation finds a strictly shorter route the count is *replaced*; when it finds an equal-length route the count is *added*. "
                     "That distinction is the entire problem.",
        "complexity": ("O(m log n)", "O(n + m)"),
        "code": {
            "cpp": r"""// Dijkstra with a path count: replace on improvement, add on a tie
int countPaths(int n, vector<vector<int>>& roads) {
    const long long MOD = 1000000007;
    vector<vector<pair<int,int>>> adj(n);        // u -> (v, time)
    for (auto& r : roads) {
        adj[r[0]].push_back({r[1], r[2]});
        adj[r[1]].push_back({r[0], r[2]});
    }
    vector<long long> dist(n, LLONG_MAX), ways(n, 0);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    dist[0] = 0; ways[0] = 1;
    pq.push({0, 0});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d > dist[u]) continue;               // stale entry
        for (auto [v, w] : adj[u]) {
            if (d + w < dist[v]) {               // shorter: replace the count
                dist[v] = d + w;
                ways[v] = ways[u];
                pq.push({dist[v], v});
            } else if (d + w == dist[v]) {       // equal: add the count
                ways[v] = (ways[v] + ways[u]) % MOD;
            }
        }
    }
    return (int)ways[n - 1];
}   // O(m log n) time · O(n + m) space""",
            "java": r"""// Dijkstra with a path count: replace on improvement, add on a tie
int countPaths(int n, int[][] roads) {
    final long MOD = 1_000_000_007L;
    List<List<long[]>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    for (int[] r : roads) {                      // u -> (v, time), both ways
        adj.get(r[0]).add(new long[]{r[1], r[2]});
        adj.get(r[1]).add(new long[]{r[0], r[2]});
    }
    long[] dist = new long[n], ways = new long[n];
    Arrays.fill(dist, Long.MAX_VALUE);
    PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
    dist[0] = 0; ways[0] = 1;
    pq.add(new long[]{0, 0});
    while (!pq.isEmpty()) {
        long[] cur = pq.poll();
        long d = cur[0]; int u = (int) cur[1];
        if (d > dist[u]) continue;               // stale entry
        for (long[] e : adj.get(u)) {
            int v = (int) e[0];
            long nd = d + e[1];
            if (nd < dist[v]) {                  // shorter: replace the count
                dist[v] = nd;
                ways[v] = ways[u];
                pq.add(new long[]{nd, v});
            } else if (nd == dist[v]) {          // equal: add the count
                ways[v] = (ways[v] + ways[u]) % MOD;
            }
        }
    }
    return (int) ways[n - 1];
}   // O(m log n) time · O(n + m) space""",
            "python": r"""import heapq

def count_paths(n, roads):
    MOD = 10 ** 9 + 7
    adj = [[] for _ in range(n)]     # u -> [(v, time)]
    for u, v, w in roads:
        adj[u].append((v, w))
        adj[v].append((u, w))
    dist = [float('inf')] * n
    ways = [0] * n
    dist[0], ways[0] = 0, 1
    pq = [(0, 0)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue                 # stale entry
        for v, w in adj[u]:
            if d + w < dist[v]:      # shorter: replace the count
                dist[v] = d + w
                ways[v] = ways[u]
                heapq.heappush(pq, (dist[v], v))
            elif d + w == dist[v]:   # equal: add the count
                ways[v] = (ways[v] + ways[u]) % MOD
    return ways[n - 1]""",
        },
    },
    {
        "slug": "find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance",
        "title": "City With the Fewest Reachable Neighbours",
        "difficulty": "Hard",
        "pattern": "all-pairs shortest paths (Floyd-Warshall)",
        "statement": "Given weighted bidirectional edges and a distance threshold, return the city with the fewest other cities within that distance, "
                     "breaking ties by the largest index.",
        "examples": [("n = 4, edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], distanceThreshold = 4", "3"),
                     ("n = 5, edges = [[0,1,2],[0,4,8],[1,2,3],[1,4,2],[2,3,1],[3,4,1]], distanceThreshold = 2", "0")],
        "constraints": ["2 <= n <= 100", "1 <= edges <= n · (n - 1) / 2", "weights are positive"],
        "approach": "Every pair of cities needs a distance, which is exactly what Floyd-Warshall computes with three nested loops over a matrix: "
                     "try every intermediate node k and relax the pair (i, j). With n <= 100 the O(n³) table is small enough, and the alternative "
                     "of running Dijkstra from every node is more code for no benefit.",
        "complexity": ("O(n³)", "O(n²)"),
        "code": {
            "cpp": r"""// Floyd-Warshall: try every intermediate node k
int findTheCity(int n, vector<vector<int>>& edges, int threshold) {
    const int INF = 1e9;
    vector<vector<int>> d(n, vector<int>(n, INF));
    for (int i = 0; i < n; i++) d[i][i] = 0;
    for (auto& e : edges) { d[e[0]][e[1]] = e[2]; d[e[1]][e[0]] = e[2]; }
    for (int k = 0; k < n; k++)                  // the intermediate node
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
    int bestCity = -1, bestCount = n;
    for (int i = n - 1; i >= 0; i--) {           // descending: largest index wins ties
        int reachable = 0;
        for (int j = 0; j < n; j++) if (i != j && d[i][j] <= threshold) reachable++;
        if (reachable < bestCount) { bestCount = reachable; bestCity = i; }
    }
    return bestCity;
}   // O(n³) time · O(n²) space""",
            "java": r"""// Floyd-Warshall: try every intermediate node k
int findTheCity(int n, int[][] edges, int threshold) {
    final int INF = 1_000_000_000;
    int[][] d = new int[n][n];
    for (int[] row : d) Arrays.fill(row, INF);
    for (int i = 0; i < n; i++) d[i][i] = 0;
    for (int[] e : edges) { d[e[0]][e[1]] = e[2]; d[e[1]][e[0]] = e[2]; }
    for (int k = 0; k < n; k++)                  // the intermediate node
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];
    int bestCity = -1, bestCount = n;
    for (int i = n - 1; i >= 0; i--) {           // descending: largest index wins
        int reachable = 0;
        for (int j = 0; j < n; j++) if (i != j && d[i][j] <= threshold) reachable++;
        if (reachable < bestCount) { bestCount = reachable; bestCity = i; }
    }
    return bestCity;
}   // O(n³) time · O(n²) space""",
            "python": r"""def find_the_city(n, edges, threshold):
    INF = float('inf')
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = d[v][u] = w
    for k in range(n):               # every possible intermediate city
        for i in range(n):
            dik = d[i][k]
            if dik == INF:
                continue
            for j in range(n):
                if dik + d[k][j] < d[i][j]:
                    d[i][j] = dik + d[k][j]
    best_city, best_count = -1, n
    for i in range(n - 1, -1, -1):   # descending so ties keep the larger index
        reachable = sum(1 for j in range(n) if i != j and d[i][j] <= threshold)
        if reachable < best_count:
            best_count, best_city = reachable, i
    return best_city""",
        },
    },
    {
        "slug": "largest-color-value-in-a-directed-graph",
        "title": "Largest Colour Value in a Directed Graph",
        "difficulty": "Hard",
        "pattern": "topological order + per-node colour counts",
        "statement": "Each node has a colour. The colour value of a path is the number of times its most frequent colour appears on it. Return the "
                     "largest colour value over all paths, or -1 if the graph has a cycle.",
        "examples": [("colors = \"abaca\", edges = [[0,1],[0,2],[2,3],[3,4]]", "3"),
                     ("colors = \"a\", edges = [[0,0]]", "-1")],
        "constraints": ["1 <= n <= 10^5", "1 <= edges <= 10^5", "there are at most 26 colours"],
        "approach": "Process nodes in topological order so every predecessor is finished before its successors. Each node stores 26 counters: the best "
                     "count of each colour along any path ending there, computed by copying the best predecessor and adding its own colour. A cycle "
                     "(fewer processed nodes than n) makes the answer -1.",
        "complexity": ("O(26 · (n + m))", "O(26 · n)"),
        "code": {
            "cpp": r"""// Topological order: each node keeps 26 per-colour counts
int largestPathValue(string colors, vector<vector<int>>& edges) {
    int n = colors.size();
    vector<vector<int>> adj(n);
    vector<int> indeg(n, 0);
    for (auto& e : edges) { adj[e[0]].push_back(e[1]); indeg[e[1]]++; }
    vector<array<int, 26>> dp(n);
    for (auto& row : dp) row.fill(0);
    queue<int> ready;
    for (int u = 0; u < n; u++) if (!indeg[u]) ready.push(u);
    int processed = 0, best = 0;
    while (!ready.empty()) {
        int u = ready.front(); ready.pop();
        processed++;
        dp[u][colors[u] - 'a']++;                // count this node's colour
        best = max(best, dp[u][colors[u] - 'a']);
        for (int v : adj[u]) {
            for (int c = 0; c < 26; c++)          // push the better counts forward
                if (dp[u][c] > dp[v][c]) dp[v][c] = dp[u][c];
            if (--indeg[v] == 0) ready.push(v);
        }
    }
    return processed == n ? best : -1;            // fewer than n: a cycle
}   // O(26·(n + m)) time · O(26·n) space""",
            "java": r"""// Topological order: each node keeps 26 per-colour counts
int largestPathValue(String colors, int[][] edges) {
    int n = colors.length();
    List<List<Integer>> adj = new ArrayList<>();
    for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
    int[] indeg = new int[n];
    for (int[] e : edges) { adj.get(e[0]).add(e[1]); indeg[e[1]]++; }
    int[][] dp = new int[n][26];
    Deque<Integer> ready = new ArrayDeque<>();
    for (int u = 0; u < n; u++) if (indeg[u] == 0) ready.add(u);
    int processed = 0, best = 0;
    while (!ready.isEmpty()) {
        int u = ready.poll();
        processed++;
        dp[u][colors.charAt(u) - 'a']++;         // count this node's colour
        best = Math.max(best, dp[u][colors.charAt(u) - 'a']);
        for (int v : adj.get(u)) {
            for (int c = 0; c < 26; c++)          // push the better counts forward
                if (dp[u][c] > dp[v][c]) dp[v][c] = dp[u][c];
            if (--indeg[v] == 0) ready.add(v);
        }
    }
    return processed == n ? best : -1;            // fewer than n: a cycle
}   // O(26·(n + m)) time · O(26·n) space""",
            "python": r"""from collections import deque

def largest_path_value(colors, edges):
    n = len(colors)
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in edges:
        adj[a].append(b)
        indeg[b] += 1
    dp = [[0] * 26 for _ in range(n)]     # per-colour best counts
    ready = deque(u for u in range(n) if indeg[u] == 0)
    processed = best = 0
    while ready:
        u = ready.popleft()
        processed += 1
        c = ord(colors[u]) - 97
        dp[u][c] += 1                     # count this node's colour
        best = max(best, dp[u][c])
        for v in adj[u]:
            dv, du = dp[v], dp[u]
            for k in range(26):           # hand the better counts forward
                if du[k] > dv[k]:
                    dv[k] = du[k]
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
    return best if processed == n else -1   # fewer than n: a cycle""",
        },
    },
]
