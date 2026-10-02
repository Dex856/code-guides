# Topic 9 · Dynamic Programming
#
# 6 easy · 12 medium · 12 hard, in a constant, gentle slope.

TOPIC = {
    "name": "Dynamic Programming",
    "tagline": "Name the state, write the transition, set the base case — the rest is bookkeeping.",
    "focus": "Every DP problem in this topic is one of six shapes: a one-variable recurrence over a sequence, an unbounded or 0/1 knapsack, a grid "
             "table, a two-string table, an interval table, or a state machine with a few named modes. The hard problems do not use a new shape — they "
             "add a second dimension (two travellers, k transactions, a memo over subsets) or a proof that the greedy order is safe.",
    "ordering": "easy 1–6 are single-sequence recurrences plus one grid table and one win/lose table; medium 1–2 open with the two canonical linear "
                "state machines (best-sum-so-far and take-or-skip), 3–5 are knapsack and grid tables, 6–8 are string DP and the circular case, 9–10 "
                "are subset-sum counting and feasibility, 11–12 are the two-string tables; hard 1–4 are memoised searches and multi-state machines, "
                "5–8 are two-string and partition tables, 9–10 are the interval family, 11–12 add a third dimension.",
}

PROBLEMS = [
    # ------------------------------------------------------------------ EASY
    {
        "slug": "climbing-stairs",
        "title": "Climbing Stairs",
        "difficulty": "Easy",
        "pattern": "one-variable recurrence (Fibonacci shape)",
        "statement": "You climb a staircase of n steps, taking one or two steps at a time. Return the number of distinct ways to reach the top.",
        "examples": [("n = 2", "2"), ("n = 3", "3")],
        "constraints": ["1 <= n <= 45", "the answer fits in a 32-bit integer"],
        "approach": "The number of ways to stand on step i is the sum of the ways to stand on i-1 and i-2, because the last move was either a single "
                     "step or a double one. Only the previous two values are ever needed, so the table collapses into two variables.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// dp[i] = dp[i-1] + dp[i-2]; only two values are ever needed
int climbStairs(int n) {
    int a = 1, b = 1;                            // ways to stand on step 0 and step 1
    for (int i = 2; i <= n; i++) {
        int c = a + b;
        a = b;
        b = c;
    }
    return b;
}   // O(n) time · O(1) space""",
            "java": r"""// dp[i] = dp[i-1] + dp[i-2]; only two values are ever needed
int climbStairs(int n) {
    int a = 1, b = 1;                            // ways to stand on step 0 and step 1
    for (int i = 2; i <= n; i++) {
        int c = a + b;
        a = b;
        b = c;
    }
    return b;
}   // O(n) time · O(1) space""",
            "python": r"""def climb_stairs(n):
    a, b = 1, 1              # ways to stand on step 0 and step 1
    for _ in range(2, n + 1):
        a, b = b, a + b      # dp[i] = dp[i-1] + dp[i-2]
    return b""",
        },
    },
    {
        "slug": "n-th-tribonacci-number",
        "title": "N-th Tribonacci Number",
        "difficulty": "Easy",
        "pattern": "recurrence with a three-value window",
        "statement": "T0 = 0, T1 = 1, T2 = 1 and each later term is the sum of the previous three. Return Tn.",
        "examples": [("n = 4", "4"), ("n = 25", "1389537")],
        "constraints": ["0 <= n <= 37", "the sequence is fixed by T0, T1, T2", "the answer fits in a 32-bit integer"],
        "approach": "The same rolling-window idea as climbing stairs, one term wider. Only the last three values are ever needed, so three variables "
                     "replace the whole table.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// The window is three wide instead of two
int tribonacci(int n) {
    if (n < 2) return n;                         // T0 = 0, T1 = 1
    int a = 0, b = 1, c = 1;                     // T0, T1, T2
    for (int i = 3; i <= n; i++) {
        int d = a + b + c;                       // slide the window by one
        a = b;
        b = c;
        c = d;
    }
    return c;
}   // O(n) time · O(1) space""",
            "java": r"""// The window is three wide instead of two
int tribonacci(int n) {
    if (n < 2) return n;                         // T0 = 0, T1 = 1
    int a = 0, b = 1, c = 1;                     // T0, T1, T2
    for (int i = 3; i <= n; i++) {
        int d = a + b + c;                       // slide the window by one
        a = b;
        b = c;
        c = d;
    }
    return c;
}   // O(n) time · O(1) space""",
            "python": r"""def tribonacci(n):
    if n < 2:
        return n             # T0 = 0, T1 = 1
    a, b, c = 0, 1, 1        # T0, T1, T2
    for _ in range(3, n + 1):
        a, b, c = b, c, a + b + c    # slide the three-value window
    return c""",
        },
    },
    {
        "slug": "min-cost-climbing-stairs",
        "title": "Min Cost Climbing Stairs",
        "difficulty": "Easy",
        "pattern": "recurrence with a cost per step",
        "statement": "Each step of the staircase has a cost. Once you pay it you may climb one or two steps further. Starting from step 0 or step 1, "
                     "return the cheapest way to pass the top of the floor.",
        "examples": [("cost = [10,15,20]", "15"), ("cost = [1,100,1,1,1,100,1,1,100,1]", "6")],
        "constraints": ["2 <= cost.length <= 1000", "0 <= cost[i] <= 999", "may start at index 0 or index 1"],
        "approach": "Same shape as climbing stairs, with the cost folded in: the cheapest way to be *past* step i is the cost of the steps taken plus "
                     "the cheaper of arriving from i-1 or i-2. Two rolling variables keep the answer in O(1) space.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Same recurrence as climbing stairs, with each step's cost added
int minCostClimbingStairs(vector<int>& cost) {
    int a = 0, b = 0;                            // cheapest way past the two previous steps
    for (int i = 2; i <= (int)cost.size(); i++) {
        int c = min(a + cost[i - 2], b + cost[i - 1]);   // arrive from two or one below
        a = b;
        b = c;
    }
    return b;
}   // O(n) time · O(1) space""",
            "java": r"""// Same recurrence as climbing stairs, with each step's cost added
int minCostClimbingStairs(int[] cost) {
    int a = 0, b = 0;                            // cheapest way past the two previous steps
    for (int i = 2; i <= cost.length; i++) {
        int c = Math.min(a + cost[i - 2], b + cost[i - 1]);   // from two or one below
        a = b;
        b = c;
    }
    return b;
}   // O(n) time · O(1) space""",
            "python": r"""def min_cost_climbing_stairs(cost):
    a = b = 0                # cheapest way past the two previous steps
    for i in range(2, len(cost) + 1):
        # arrive from two steps below (paying cost[i-2]) or one (paying cost[i-1])
        a, b = b, min(a + cost[i - 2], b + cost[i - 1])
    return b""",
        },
    },
    {
        "slug": "best-time-to-buy-and-sell-stock",
        "title": "Best Time to Buy and Sell Stock",
        "difficulty": "Easy",
        "pattern": "running minimum (one-transaction state)",
        "statement": "Given daily prices, choose one day to buy and a later day to sell. Return the maximum profit, or 0 if no profit is possible.",
        "examples": [("prices = [7,1,5,3,6,4]", "5"), ("prices = [7,6,4,3,1]", "0")],
        "constraints": ["1 <= prices.length <= 10^5", "0 <= prices[i] <= 10^4", "the selling day must come after the buying day"],
        "approach": "A single pass keeps the cheapest price seen so far; selling today is only worth considering against that minimum. This is the "
                     "one-state version of the multi-state stock problems later in this topic.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Keep the cheapest buy so far; try selling on every later day
int maxProfit(vector<int>& prices) {
    int best = 0, lowest = INT_MAX;
    for (int p : prices) {
        lowest = min(lowest, p);                 // cheapest day to have bought
        best = max(best, p - lowest);            // profit if we sell today
    }
    return best;
}   // O(n) time · O(1) space""",
            "java": r"""// Keep the cheapest buy so far; try selling on every later day
int maxProfit(int[] prices) {
    int best = 0, lowest = Integer.MAX_VALUE;
    for (int p : prices) {
        lowest = Math.min(lowest, p);            // cheapest day to have bought
        best = Math.max(best, p - lowest);       // profit if we sell today
    }
    return best;
}   // O(n) time · O(1) space""",
            "python": r"""def max_stock_profit(prices):
    best, lowest = 0, float('inf')
    for p in prices:
        lowest = min(lowest, p)      # cheapest day to have bought so far
        best = max(best, p - lowest)  # profit if we sell today
    return best""",
        },
    },
    {
        "slug": "pascals-triangle",
        "title": "Pascal's Triangle",
        "difficulty": "Easy",
        "pattern": "grid DP with a boundary condition",
        "statement": "Return the first numRows rows of Pascal's triangle, where every entry is the sum of the two above it.",
        "examples": [("numRows = 5", "[[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]"), ("numRows = 1", "[[1]]")],
        "constraints": ["1 <= numRows <= 30", "each row starts and ends with 1"],
        "approach": "Row i is built from row i-1: the edges stay 1 and the middle entries add their two parents. It is the simplest possible "
                     "two-dimensional table, and the shape returns in the grid problems of the medium section.",
        "complexity": ("O(numRows²)", "O(numRows²) for the output"),
        "code": {
            "cpp": r"""// Each row is the sum of the two entries above it
vector<vector<int>> generate(int numRows) {
    vector<vector<int>> rows;
    for (int i = 0; i < numRows; i++) {
        vector<int> row(i + 1, 1);                // both edges are 1
        for (int j = 1; j < i; j++)
            row[j] = rows[i-1][j-1] + rows[i-1][j];
        rows.push_back(row);
    }
    return rows;
}   // O(numRows²) time · O(numRows²) space""",
            "java": r"""// Each row is the sum of the two entries above it
List<List<Integer>> generate(int numRows) {
    List<List<Integer>> rows = new ArrayList<>();
    for (int i = 0; i < numRows; i++) {
        List<Integer> row = new ArrayList<>();
        for (int j = 0; j <= i; j++) row.add(1);          // both edges are 1
        for (int j = 1; j < i; j++)
            row.set(j, rows.get(i-1).get(j-1) + rows.get(i-1).get(j));
        rows.add(row);
    }
    return rows;
}   // O(numRows²) time · O(numRows²) space""",
            "python": r"""def build_pascals(num_rows):
    rows = []
    for i in range(num_rows):
        row = [1] * (i + 1)                    # edges are 1
        for j in range(1, i):
            row[j] = rows[i-1][j-1] + rows[i-1][j]
        rows.append(row)
    return rows""",
        },
    },
    {
        "slug": "divisor-game",
        "title": "Divisor Game",
        "difficulty": "Easy",
        "pattern": "win/lose DP over positions",
        "statement": "Starting from n, players alternately subtract a divisor of the current number (any divisor smaller than it) from that number. "
                     "Whoever cannot move loses. Alice moves first — does she win with best play?",
        "examples": [("n = 2", "true"), ("n = 3", "false")],
        "constraints": ["1 <= n <= 1000", "a move must subtract a proper divisor", "n = 1 means the player to move has already lost"],
        "approach": "The honest solution is a win/lose table: a position is winning when some legal move hands the opponent a losing position. The "
                     "pattern that falls out — even wins, odd loses — is a bonus, but the table shows *why* without any leap of insight.",
        "complexity": ("O(n²)", "O(n)"),
        "code": {
            "cpp": r"""// win[x]: the player to move wins; hand over a losing position
bool divisorGame(int n) {
    vector<bool> win(n + 1, false);              // x = 1 loses: no legal move
    for (int x = 2; x <= n; x++)
        for (int d = 1; d < x; d++)
            if (x % d == 0 && !win[x - d]) { win[x] = true; break; }
    return win[n];
}   // O(n²) time · O(n) space (the pattern is: even wins, odd loses)""",
            "java": r"""// win[x]: the player to move wins; hand over a losing position
boolean divisorGame(int n) {
    boolean[] win = new boolean[n + 1];          // x = 1 loses: no legal move
    for (int x = 2; x <= n; x++)
        for (int d = 1; d < x; d++)
            if (x % d == 0 && !win[x - d]) { win[x] = true; break; }
    return win[n];
}   // O(n²) time · O(n) space (the pattern is: even wins, odd loses)""",
            "python": r"""def divisor_game(n):
    win = [False] * (n + 1)          # x = 1 loses: there is no legal move
    for x in range(2, n + 1):
        for d in range(1, x):
            if x % d == 0 and not win[x - d]:
                win[x] = True        # hand the opponent a losing position
                break
    return win[n]""",
        },
    },
    # ------------------------------------------------------------------ MEDIUM
    {
        "slug": "maximum-subarray",
        "title": "Maximum Subarray",
        "difficulty": "Medium",
        "pattern": "Kadane (best ending here)",
        "statement": "Return the largest sum of any non-empty contiguous subarray.",
        "examples": [("nums = [-2,1,-3,4,-1,2,1,-5,4]", "6"), ("nums = [1]", "1"), ("nums = [5,4,-1,7,8]", "23")],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4", "the subarray must be non-empty"],
        "approach": "Track the best sum of a subarray *ending at the current index*: either extend the previous one or start fresh here. The running "
                     "maximum of that quantity is the answer, and negatives are handled because restarting is always an option.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Kadane: best sum of a subarray ending at the current position
int maxSubArray(vector<int>& nums) {
    int best = nums[0], cur = nums[0];
    for (int i = 1; i < (int)nums.size(); i++) {
        cur = max(nums[i], cur + nums[i]);       // extend, or restart here
        best = max(best, cur);
    }
    return best;
}   // O(n) time · O(1) space""",
            "java": r"""// Kadane: best sum of a subarray ending at the current position
int maxSubArray(int[] nums) {
    int best = nums[0], cur = nums[0];
    for (int i = 1; i < nums.length; i++) {
        cur = Math.max(nums[i], cur + nums[i]);  // extend, or restart here
        best = Math.max(best, cur);
    }
    return best;
}   // O(n) time · O(1) space""",
            "python": r"""def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)    # extend the run, or restart at x
        best = max(best, cur)
    return best""",
        },
    },
    {
        "slug": "house-robber",
        "title": "House Robber",
        "difficulty": "Medium",
        "pattern": "take-or-skip on a line",
        "statement": "Houses in a row hold the given amounts of money, but two adjacent houses cannot both be robbed. Return the maximum amount that "
                     "can be taken.",
        "examples": [("nums = [1,2,3,1]", "4"), ("nums = [2,7,9,3,1]", "12")],
        "constraints": ["1 <= nums.length <= 100", "0 <= nums[i] <= 400", "no two adjacent houses may be robbed"],
        "approach": "At each house there are exactly two choices: rob it, which forbids the previous house, or skip it. Carrying the best answer for "
                     "the previous two positions is enough, so the classic two-variable walk gives the answer in constant space.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// Two choices per house: take it (skip the previous) or leave it
int rob(vector<int>& nums) {
    int prev2 = 0, prev1 = 0;                    // best up to the two houses back
    for (int x : nums) {
        int take = prev2 + x;                    // rob this one, skip the previous
        prev2 = prev1;
        prev1 = max(prev1, take);
    }
    return prev1;
}   // O(n) time · O(1) space""",
            "java": r"""// Two choices per house: take it (skip the previous) or leave it
int rob(int[] nums) {
    int prev2 = 0, prev1 = 0;                    // best up to the two houses back
    for (int x : nums) {
        int take = prev2 + x;                    // rob this one, skip the previous
        prev2 = prev1;
        prev1 = Math.max(prev1, take);
    }
    return prev1;
}   // O(n) time · O(1) space""",
            "python": r"""def rob_house(nums):
    prev2 = prev1 = 0            # best totals up to the two previous houses
    for x in nums:
        take = prev2 + x         # rob this house, so skip the previous one
        prev2, prev1 = prev1, max(prev1, take)
    return prev1""",
        },
    },
    {
        "slug": "coin-change",
        "title": "Coin Change",
        "difficulty": "Medium",
        "pattern": "unbounded knapsack (fewest coins)",
        "statement": "Given coin denominations and a target amount, return the fewest coins that make the amount exactly, or -1 if it cannot be made. "
                     "Coins may be reused.",
        "examples": [("coins = [1,2,5], amount = 11", "3"), ("coins = [2], amount = 3", "-1"), ("coins = [1], amount = 0", "0")],
        "constraints": ["1 <= coins.length <= 12", "1 <= coins[i] <= 2^31 - 1", "0 <= amount <= 10^4"],
        "approach": "Let dp[a] be the fewest coins summing to a. Trying each coin as the *last* one gives dp[a] = 1 + min over coins of dp[a - coin]. "
                     "Iterating amounts outwards lets a coin be reused any number of times — that is what makes this knapsack unbounded.",
        "complexity": ("O(amount · coins)", "O(amount)"),
        "code": {
            "cpp": r"""// Unbounded knapsack: dp[a] = fewest coins that make amount a
int coinChange(vector<int>& coins, int amount) {
    const int INF = 1e9;
    vector<int> dp(amount + 1, INF);
    dp[0] = 0;                                   // zero coins make zero
    for (int a = 1; a <= amount; a++)
        for (int c : coins)
            if (c <= a && dp[a - c] + 1 < dp[a]) dp[a] = dp[a - c] + 1;
    return dp[amount] == INF ? -1 : dp[amount];
}   // O(amount · coins) time · O(amount) space""",
            "java": r"""// Unbounded knapsack: dp[a] = fewest coins that make amount a
int coinChange(int[] coins, int amount) {
    final int INF = 1_000_000_000;
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, INF);
    dp[0] = 0;                                   // zero coins make zero
    for (int a = 1; a <= amount; a++)
        for (int c : coins)
            if (c <= a && dp[a - c] + 1 < dp[a]) dp[a] = dp[a - c] + 1;
    return dp[amount] == INF ? -1 : dp[amount];
}   // O(amount · coins) time · O(amount) space""",
            "python": r"""def coin_change(coins, amount):
    INF = float('inf')
    dp = [INF] * (amount + 1)
    dp[0] = 0                        # zero coins make zero
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1    # use one more coin of value c
    return -1 if dp[amount] == INF else dp[amount]""",
        },
    },
    {
        "slug": "coin-change-ii",
        "title": "Coin Change II",
        "difficulty": "Medium",
        "pattern": "unbounded knapsack (count the combinations)",
        "statement": "Count the combinations of coins that make the amount exactly. Two combinations are the same if they use the same multiset of "
                     "coins, whatever the order.",
        "examples": [("amount = 5, coins = [1,2,5]", "4"), ("amount = 3, coins = [2]", "0"), ("amount = 10, coins = [10]", "1")],
        "constraints": ["1 <= coins.length <= 300", "1 <= coins[i] <= 5000", "0 <= amount <= 5000", "the answer fits in a 32-bit signed integer"],
        "approach": "The order of the two loops is the whole trick here. Putting the *coins* in the outer loop means each coin is considered once and "
                     "later coins can never be reordered, so 1+2 and 2+1 are counted once. Swapping the loops would count permutations instead.",
        "complexity": ("O(amount · coins)", "O(amount)"),
        "code": {
            "cpp": r"""// Coins in the outer loop: each combination is counted exactly once
int change(int amount, vector<int>& coins) {
    vector<int> dp(amount + 1, 0);
    dp[0] = 1;                                   // one way to make nothing
    for (int c : coins)
        for (int a = c; a <= amount; a++)
            dp[a] += dp[a - c];                  // add combinations that end with c
    return dp[amount];
}   // O(amount · coins) time · O(amount) space""",
            "java": r"""// Coins in the outer loop: each combination is counted exactly once
int change(int amount, int[] coins) {
    int[] dp = new int[amount + 1];
    dp[0] = 1;                                   // one way to make nothing
    for (int c : coins)
        for (int a = c; a <= amount; a++)
            dp[a] += dp[a - c];                  // add combinations that end with c
    return dp[amount];
}   // O(amount · coins) time · O(amount) space""",
            "python": r"""def change_ways(amount, coins):
    dp = [0] * (amount + 1)
    dp[0] = 1                        # one way to make nothing
    for c in coins:                  # coins outside: combinations, not permutations
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]""",
        },
    },
    {
        "slug": "unique-paths",
        "title": "Unique Paths",
        "difficulty": "Medium",
        "pattern": "grid table (count the routes)",
        "statement": "A robot starts at the top-left of an m x n grid and may only move right or down. Count the distinct routes to the bottom-right "
                     "corner.",
        "examples": [("m = 3, n = 7", "28"), ("m = 3, n = 2", "3")],
        "constraints": ["1 <= m, n <= 100", "the answer fits in a 32-bit integer for these limits"],
        "approach": "The number of routes to a cell is the sum of the routes to the cell above and the cell to the left, because any route arrives "
                     "from exactly one of them. One row of the table suffices: updating left to right reuses the value from above in place.",
        "complexity": ("O(m · n)", "O(n)"),
        "code": {
            "cpp": r"""// One row is enough: dp[j] holds the cell above until it is overwritten
int uniquePaths(int m, int n) {
    vector<int> dp(n, 1);                        // top row: one route along it
    for (int i = 1; i < m; i++)
        for (int j = 1; j < n; j++)
            dp[j] += dp[j - 1];                  // from above + from the left
    return dp[n - 1];
}   // O(m · n) time · O(n) space""",
            "java": r"""// One row is enough: dp[j] holds the cell above until it is overwritten
int uniquePaths(int m, int n) {
    int[] dp = new int[n];
    Arrays.fill(dp, 1);                          // top row: one route along it
    for (int i = 1; i < m; i++)
        for (int j = 1; j < n; j++)
            dp[j] += dp[j - 1];                  // from above + from the left
    return dp[n - 1];
}   // O(m · n) time · O(n) space""",
            "python": r"""def unique_paths(m, n):
    dp = [1] * n                 # first row: exactly one route along the top
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]   # from above (old dp[j]) + from the left
    return dp[n - 1]""",
        },
    },
    {
        "slug": "decode-ways",
        "title": "Decode Ways",
        "difficulty": "Medium",
        "pattern": "string DP with two cases per position",
        "statement": "Letters A-Z map to 1-26. Given a digit string, count the ways to decode it, treating 0 as un-decodable on its own.",
        "examples": [("s = \"12\"", "2"), ("s = \"226\"", "3"), ("s = \"06\"", "0")],
        "constraints": ["1 <= s.length <= 100", "s contains digits only", "\"06\" cannot be decoded as 6"],
        "approach": "Walk the string left to right and ask two questions at each position: is the last single digit a valid letter (1-9), and is the "
                     "last pair a valid letter (10-26)? Each valid option inherits the count from one or two positions back. Zero digits are what "
                     "make the bookkeeping interesting.",
        "complexity": ("O(n)", "O(n)"),
        "code": {
            "cpp": r"""// A digit may decode alone (1-9) or as a pair (10-26)
int numDecodings(string s) {
    int n = s.size();
    vector<int> dp(n + 1, 0);
    dp[0] = 1;                                   // the empty prefix: one way
    dp[1] = s[0] == '0' ? 0 : 1;
    for (int i = 2; i <= n; i++) {
        int one = s[i-1] - '0';
        int two = (s[i-2] - '0') * 10 + one;
        if (one >= 1) dp[i] += dp[i-1];                    // take i alone
        if (two >= 10 && two <= 26) dp[i] += dp[i-2];      // take i-1 and i
    }
    return dp[n];
}   // O(n) time · O(n) space""",
            "java": r"""// A digit may decode alone (1-9) or as a pair (10-26)
int numDecodings(String s) {
    int n = s.length();
    int[] dp = new int[n + 1];
    dp[0] = 1;                                   // the empty prefix: one way
    dp[1] = s.charAt(0) == '0' ? 0 : 1;
    for (int i = 2; i <= n; i++) {
        int one = s.charAt(i-1) - '0';
        int two = (s.charAt(i-2) - '0') * 10 + one;
        if (one >= 1) dp[i] += dp[i-1];                    // take i alone
        if (two >= 10 && two <= 26) dp[i] += dp[i-2];      // take i-1 and i
    }
    return dp[n];
}   // O(n) time · O(n) space""",
            "python": r"""def num_decodings(s):
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1                      # the empty prefix: one way
    dp[1] = 0 if s[0] == '0' else 1
    for i in range(2, n + 1):
        one = int(s[i-1])
        two = int(s[i-2:i])
        if one >= 1:
            dp[i] += dp[i-1]       # decode s[i-1] on its own
        if 10 <= two <= 26:
            dp[i] += dp[i-2]       # decode s[i-2:i] as one letter
    return dp[n]""",
        },
    },
    {
        "slug": "word-break",
        "title": "Word Break",
        "difficulty": "Medium",
        "pattern": "string DP over dictionary splits",
        "statement": "Decide whether the string can be split into a sequence of dictionary words, reusing words as often as needed.",
        "examples": [("s = \"leetcode\", wordDict = [\"leet\",\"code\"]", "true"),
                     ("s = \"applepenapple\", wordDict = [\"apple\",\"pen\"]", "true"),
                     ("s = \"catsandog\", wordDict = [\"cats\",\"dog\",\"sand\",\"and\",\"cat\"]", "false")],
        "constraints": ["1 <= s.length <= 300", "1 <= words <= 1000", "1 <= word length <= 20"],
        "approach": "dp[i] means the first i characters can be segmented. It is true when some earlier position j is reachable and the slice between j "
                     "and i is a dictionary word, so the state is a boolean per prefix and the transition scans back over the string.",
        "complexity": ("O(n² · L) with a set lookup", "O(n)"),
        "code": {
            "cpp": r"""// dp[i]: the first i characters can be split into dictionary words
bool wordBreak(string s, vector<string>& wordDict) {
    unordered_set<string> dict(wordDict.begin(), wordDict.end());
    int n = s.size();
    vector<bool> dp(n + 1, false);
    dp[0] = true;                                // empty prefix is reachable
    for (int i = 1; i <= n; i++)
        for (int j = 0; j < i; j++)
            if (dp[j] && dict.count(s.substr(j, i - j))) { dp[i] = true; break; }
    return dp[n];
}   // O(n² · L) time · O(n) space""",
            "java": r"""// dp[i]: the first i characters can be split into dictionary words
boolean wordBreak(String s, List<String> wordDict) {
    Set<String> dict = new HashSet<>(wordDict);
    int n = s.length();
    boolean[] dp = new boolean[n + 1];
    dp[0] = true;                                // empty prefix is reachable
    for (int i = 1; i <= n; i++)
        for (int j = 0; j < i; j++)
            if (dp[j] && dict.contains(s.substring(j, i))) { dp[i] = true; break; }
    return dp[n];
}   // O(n² · L) time · O(n) space""",
            "python": r"""def word_break(s, word_dict):
    words = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True                   # the empty prefix is reachable
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True       # a word ends exactly at i
                break
    return dp[n]""",
        },
    },
    {
        "slug": "house-robber-ii",
        "title": "House Robber II",
        "difficulty": "Medium",
        "pattern": "two passes around a circle",
        "statement": "The houses now form a circle, so the first and last cannot both be robbed. Return the maximum amount that can be taken.",
        "examples": [("nums = [2,3,2]", "3"), ("nums = [1,2,3,1]", "4"), ("nums = [1,2,3]", "3")],
        "constraints": ["1 <= nums.length <= 100", "0 <= nums[i] <= 1000", "the first and last houses are adjacent"],
        "approach": "A circle is just two overlapping lines. Either the last house is not robbed, which leaves the line 0..n-2, or the first is not "
                     "robbed, which leaves 1..n-1. Solving the linear problem twice and taking the better of the two covers every arrangement.",
        "complexity": ("O(n)", "O(1)"),
        "code": {
            "cpp": r"""// A circle is two lines: skip the last house, or skip the first
int robLine(vector<int>& nums, int lo, int hi) {
    int prev2 = 0, prev1 = 0;
    for (int i = lo; i <= hi; i++) {
        int take = prev2 + nums[i];
        prev2 = prev1;
        prev1 = max(prev1, take);
    }
    return prev1;
}
int rob(vector<int>& nums) {
    int n = nums.size();
    if (n == 1) return nums[0];                  // a single house: no wrap-around
    return max(robLine(nums, 0, n - 2), robLine(nums, 1, n - 1));
}   // O(n) time · O(1) space""",
            "java": r"""// A circle is two lines: skip the last house, or skip the first
int robLine(int[] nums, int lo, int hi) {
    int prev2 = 0, prev1 = 0;
    for (int i = lo; i <= hi; i++) {
        int take = prev2 + nums[i];
        prev2 = prev1;
        prev1 = Math.max(prev1, take);
    }
    return prev1;
}
int rob(int[] nums) {
    int n = nums.length;
    if (n == 1) return nums[0];                  // a single house: no wrap-around
    return Math.max(robLine(nums, 0, n - 2), robLine(nums, 1, n - 1));
}   // O(n) time · O(1) space""",
            "python": r"""def rob_circle(nums):
    def rob_line(lo, hi):
        prev2 = prev1 = 0
        for i in range(lo, hi + 1):
            prev2, prev1 = prev1, max(prev1, prev2 + nums[i])
        return prev1

    if len(nums) == 1:
        return nums[0]                # one house: nothing to wrap around
    return max(rob_line(0, len(nums) - 2), rob_line(1, len(nums) - 1))""",
        },
    },
    {
        "slug": "target-sum",
        "title": "Target Sum",
        "difficulty": "Medium",
        "pattern": "subset-sum counting after an algebraic rewrite",
        "statement": "Assign + or - to every number and count the assignments whose total equals the target.",
        "examples": [("nums = [1,1,1,1,1], target = 3", "5"), ("nums = [1], target = 1", "1")],
        "constraints": ["1 <= nums.length <= 20", "0 <= nums[i] <= 1000", "0 <= sum(nums) <= 1000", "-1000 <= target <= 1000"],
        "approach": "Two exponential searches become one polynomial count: if P is the sum of the positive group and N the negative one, then "
                     "P - N = target and P + N = total, so P = (total + target) / 2. Counting subsets that sum to that fixed value is the "
                     "0/1 knapsack counting pass.",
        "complexity": ("O(n · total)", "O(total)"),
        "code": {
            "cpp": r"""// P - N = target and P + N = total  =>  count subsets summing to (total+target)/2
int findTargetSumWays(vector<int>& nums, int target) {
    int total = accumulate(nums.begin(), nums.end(), 0);
    int diff = total - target;                   // sum of the minus signs, doubled
    if (diff < 0 || diff % 2) return 0;          // impossible parity or sign
    int P = diff / 2;
    vector<int> dp(P + 1, 0);
    dp[0] = 1;                                   // the empty subset
    for (int x : nums)
        for (int s = P; s >= x; s--)             // backwards: 0/1, not unbounded
            dp[s] += dp[s - x];
    return dp[P];
}   // O(n · total) time · O(total) space""",
            "java": r"""// P - N = target and P + N = total  =>  count subsets summing to (total+target)/2
int findTargetSumWays(int[] nums, int target) {
    int total = 0;
    for (int x : nums) total += x;
    int diff = total - target;                   // sum of the minus signs, doubled
    if (diff < 0 || diff % 2 != 0) return 0;     // impossible parity or sign
    int P = diff / 2;
    int[] dp = new int[P + 1];
    dp[0] = 1;                                   // the empty subset
    for (int x : nums)
        for (int s = P; s >= x; s--)             // backwards: 0/1, not unbounded
            dp[s] += dp[s - x];
    return dp[P];
}   // O(n · total) time · O(total) space""",
            "python": r"""def find_target_sum_ways(nums, target):
    total = sum(nums)
    diff = total - target          # the minus group counted twice
    if diff < 0 or diff % 2:
        return 0
    P = diff // 2                  # every subset of this sum is one assignment
    dp = [0] * (P + 1)
    dp[0] = 1                      # the empty subset
    for x in nums:
        for s in range(P, x - 1, -1):     # backwards keeps it a 0/1 knapsack
            dp[s] += dp[s - x]
    return dp[P]""",
        },
    },
    {
        "slug": "partition-equal-subset-sum",
        "title": "Partition Equal Subset Sum",
        "difficulty": "Medium",
        "pattern": "subset-sum feasibility (0/1 knapsack)",
        "statement": "Decide whether the array can be split into two parts with equal sums.",
        "examples": [("nums = [1,5,11,5]", "true"), ("nums = [1,2,3,5]", "false")],
        "constraints": ["1 <= nums.length <= 200", "1 <= nums[i] <= 100", "each number is used at most once"],
        "approach": "Equal halves exist exactly when some subset sums to half the total, so this is feasibility rather than counting. Scanning each "
                     "capacity downwards stops a number from being used twice in the same subset — the 0/1 rule.",
        "complexity": ("O(n · total)", "O(total)"),
        "code": {
            "cpp": r"""// Feasibility: can some subset reach exactly half the total?
bool canPartition(vector<int>& nums) {
    int total = accumulate(nums.begin(), nums.end(), 0);
    if (total % 2) return false;                 // an odd total cannot split
    int half = total / 2;
    vector<bool> dp(half + 1, false);
    dp[0] = true;                                // sum 0 is always reachable
    for (int x : nums)
        for (int s = half; s >= x; s--)          // downwards: use x at most once
            dp[s] = dp[s] || dp[s - x];
    return dp[half];
}   // O(n · total) time · O(total) space""",
            "java": r"""// Feasibility: can some subset reach exactly half the total?
boolean canPartition(int[] nums) {
    int total = 0;
    for (int x : nums) total += x;
    if (total % 2 != 0) return false;            // an odd total cannot split
    int half = total / 2;
    boolean[] dp = new boolean[half + 1];
    dp[0] = true;                                // sum 0 is always reachable
    for (int x : nums)
        for (int s = half; s >= x; s--)          // downwards: use x at most once
            dp[s] = dp[s] || dp[s - x];
    return dp[half];
}   // O(n · total) time · O(total) space""",
            "python": r"""def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False             # an odd total can never split evenly
    half = total // 2
    dp = [False] * (half + 1)
    dp[0] = True                 # sum 0 is always reachable
    for x in nums:
        for s in range(half, x - 1, -1):   # downwards: each number used once
            if dp[s - x]:
                dp[s] = True
    return dp[half]""",
        },
    },
    {
        "slug": "longest-common-subsequence",
        "title": "Longest Common Subsequence",
        "difficulty": "Medium",
        "pattern": "two-string table",
        "statement": "Return the length of the longest subsequence appearing in both strings, where a subsequence keeps order but need not be "
                     "contiguous.",
        "examples": [("text1 = \"abcde\", text2 = \"ace\"", "3"), ("text1 = \"abc\", text2 = \"abc\"", "3"),
                     ("text1 = \"abc\", text2 = \"def\"", "0")],
        "constraints": ["1 <= lengths <= 1000", "strings contain lowercase English letters", "subsequences may skip characters"],
        "approach": "dp[i][j] is the answer for the first i characters of one string and the first j of the other. If the current characters match, "
                     "they extend the diagonal cell; otherwise the best is whichever prefix pair is already better. Two rows are enough to run it, "
                     "which matters for the edit-distance family that follows.",
        "complexity": ("O(m · n)", "O(n) with two rows"),
        "code": {
            "cpp": r"""// dp[i][j]: best length using the first i and first j characters
int longestCommonSubsequence(string a, string b) {
    int m = a.size(), n = b.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++)
            dp[i][j] = a[i-1] == b[j-1]
                     ? dp[i-1][j-1] + 1              // extend the diagonal
                     : max(dp[i-1][j], dp[i][j-1]);  // drop a character
    return dp[m][n];
}   // O(m · n) time · O(m · n) space (two rows suffice)""",
            "java": r"""// dp[i][j]: best length using the first i and first j characters
int longestCommonSubsequence(String a, String b) {
    int m = a.length(), n = b.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++)
            dp[i][j] = a.charAt(i-1) == b.charAt(j-1)
                     ? dp[i-1][j-1] + 1              // extend the diagonal
                     : Math.max(dp[i-1][j], dp[i][j-1]);   // drop a character
    return dp[m][n];
}   // O(m · n) time · O(m · n) space (two rows suffice)""",
            "python": r"""def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1        # extend the match
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])   # drop one character
    return dp[m][n]""",
        },
    },
    {
        "slug": "edit-distance",
        "title": "Edit Distance",
        "difficulty": "Medium",
        "pattern": "two-string table with three moves",
        "statement": "Return the minimum number of single-character insertions, deletions or replacements needed to turn one word into another.",
        "examples": [("word1 = \"horse\", word2 = \"ros\"", "3"), ("word1 = \"intention\", word2 = \"execution\"", "5")],
        "constraints": ["0 <= lengths <= 500", "words contain lowercase English letters", "all three operations cost 1"],
        "approach": "Same table as the longest common subsequence, but the transition has three named moves instead of two: deleting a character, "
                     "inserting one, or replacing one. When the characters already match the diagonal carries over untouched.",
        "complexity": ("O(m · n)", "O(m · n)"),
        "code": {
            "cpp": r"""// Three moves per cell: delete, insert, replace
int minDistance(string a, string b) {
    int m = a.size(), n = b.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));
    for (int i = 0; i <= m; i++) dp[i][0] = i;   // delete everything
    for (int j = 0; j <= n; j++) dp[0][j] = j;   // insert everything
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++)
            dp[i][j] = a[i-1] == b[j-1]
                     ? dp[i-1][j-1]                          // free: keep it
                     : 1 + min({dp[i-1][j],                 // delete a[i-1]
                                dp[i][j-1],                 // insert b[j-1]
                                dp[i-1][j-1]});             // replace
    return dp[m][n];
}   // O(m · n) time · O(m · n) space""",
            "java": r"""// Three moves per cell: delete, insert, replace
int minDistance(String a, String b) {
    int m = a.length(), n = b.length();
    int[][] dp = new int[m + 1][n + 1];
    for (int i = 0; i <= m; i++) dp[i][0] = i;   // delete everything
    for (int j = 0; j <= n; j++) dp[0][j] = j;   // insert everything
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++)
            dp[i][j] = a.charAt(i-1) == b.charAt(j-1)
                     ? dp[i-1][j-1]                          // free: keep it
                     : 1 + Math.min(dp[i-1][j],              // delete a[i-1]
                           Math.min(dp[i][j-1],              // insert b[j-1]
                                    dp[i-1][j-1]));          // replace
    return dp[m][n];
}   // O(m · n) time · O(m · n) space""",
            "python": r"""def edit_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i               # delete every character of word1
    for j in range(n + 1):
        dp[0][j] = j               # insert every character of word2
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]              # characters already match
            else:
                dp[i][j] = 1 + min(dp[i-1][j],       # delete from word1
                                   dp[i][j-1],       # insert into word1
                                   dp[i-1][j-1])     # replace one character
    return dp[m][n]""",
        },
    },
    # ------------------------------------------------------------------ HARD
    {
        "slug": "longest-increasing-path-in-a-matrix",
        "title": "Longest Increasing Path in a Matrix",
        "difficulty": "Hard",
        "pattern": "memoised DFS on a DAG",
        "statement": "Return the length of the longest strictly increasing path in a matrix, moving in the four axis directions.",
        "examples": [("matrix = [[9,9,4],[6,6,8],[2,1,1]]", "4"), ("matrix = [[3,4,5],[3,2,6],[2,2,1]]", "4"), ("matrix = [[1]]", "1")],
        "constraints": ["1 <= rows, cols <= 200", "0 <= matrix[i][j] <= 2^31 - 1", "the path may not revisit a cell"],
        "approach": "Strict increase means the moves form a directed acyclic graph, so the answer from any cell is 1 + the best answer among its "
                     "larger neighbours. Memoising that value turns an exponential walk into one visit per cell; no visited set is needed because "
                     "the values themselves prevent cycles.",
        "complexity": ("O(rows · cols)", "O(rows · cols)"),
        "code": {
            "cpp": r"""// Strict increase makes the grid a DAG, so memoise the DFS
int longestIncreasingPath(vector<vector<int>>& m) {
    int R = m.size(), C = m[0].size();
    vector<vector<int>> memo(R, vector<int>(C, 0));
    int dr[4] = {1,-1,0,0}, dc[4] = {0,0,1,-1};
    function<int(int,int)> dfs = [&](int r, int c) {
        if (memo[r][c]) return memo[r][c];       // already solved
        int best = 1;
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= R || nc < 0 || nc >= C) continue;
            if (m[nr][nc] > m[r][c]) best = max(best, 1 + dfs(nr, nc));
        }
        return memo[r][c] = best;
    };
    int best = 0;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) best = max(best, dfs(r, c));
    return best;
}   // O(rows · cols) time · O(rows · cols) space""",
            "java": r"""// Strict increase makes the grid a DAG, so memoise the DFS
int longestIncreasingPath(int[][] m) {
    int R = m.length, C = m[0].length;
    int[][] memo = new int[R][C];
    int best = 0;
    for (int r = 0; r < R; r++)
        for (int c = 0; c < C; c++) best = Math.max(best, dfs(m, memo, r, c));
    return best;
}
int dfs(int[][] m, int[][] memo, int r, int c) {
    if (memo[r][c] != 0) return memo[r][c];      // already solved
    int R = m.length, C = m[0].length;
    int[] dr = {1,-1,0,0}, dc = {0,0,1,-1};
    int best = 1;
    for (int d = 0; d < 4; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr < 0 || nr >= R || nc < 0 || nc >= C) continue;
        if (m[nr][nc] > m[r][c]) best = Math.max(best, 1 + dfs(m, memo, nr, nc));
    }
    return memo[r][c] = best;
}   // O(rows · cols) time · O(rows · cols) space""",
            "python": r"""import sys

def longest_increasing_path(matrix):
    sys.setrecursionlimit(100000)
    R, C = len(matrix), len(matrix[0])
    memo = [[0] * C for _ in range(R)]

    def dfs(r, c):
        if memo[r][c]:
            return memo[r][c]                    # already solved
        length = 1
        for nr, nc in ((r+1,c), (r-1,c), (r,c+1), (r,c-1)):
            if 0 <= nr < R and 0 <= nc < C and matrix[nr][nc] > matrix[r][c]:
                length = max(length, 1 + dfs(nr, nc))
        memo[r][c] = length
        return length

    return max(dfs(r, c) for r in range(R) for c in range(C))""",
        },
    },
    {
        "slug": "number-of-longest-increasing-subsequence",
        "title": "Number of Longest Increasing Subsequences",
        "difficulty": "Hard",
        "pattern": "LIS with a parallel count array",
        "statement": "Count how many longest strictly increasing subsequences the array has.",
        "examples": [("nums = [1,3,5,4,7]", "2"), ("nums = [2,2,2,2,2]", "5")],
        "constraints": ["1 <= nums.length <= 2000", "-10^6 <= nums[i] <= 10^6", "the answer fits in a 32-bit integer"],
        "approach": "Every classic LIS table can carry a second array: how many best subsequences *end* at this position. When a longer chain is "
                     "found the count is replaced; when an equally long chain is found the counts add. The answer is the total over all positions that "
                     "achieve the maximum length.",
        "complexity": ("O(n²)", "O(n)"),
        "code": {
            "cpp": r"""// dp[i] = longest chain ending at i, cnt[i] = how many such chains
int findNumberOfLIS(vector<int>& nums) {
    int n = nums.size(), bestLen = 0, total = 0;
    vector<int> dp(n, 1), cnt(n, 1);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++)
            if (nums[j] < nums[i]) {
                if (dp[j] + 1 > dp[i]) { dp[i] = dp[j] + 1; cnt[i] = cnt[j]; }
                else if (dp[j] + 1 == dp[i]) cnt[i] += cnt[j];   // tie: add
            }
        bestLen = max(bestLen, dp[i]);
    }
    for (int i = 0; i < n; i++) if (dp[i] == bestLen) total += cnt[i];
    return total;
}   // O(n²) time · O(n) space""",
            "java": r"""// dp[i] = longest chain ending at i, cnt[i] = how many such chains
int findNumberOfLIS(int[] nums) {
    int n = nums.length, bestLen = 0, total = 0;
    int[] dp = new int[n], cnt = new int[n];
    Arrays.fill(dp, 1);
    Arrays.fill(cnt, 1);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++)
            if (nums[j] < nums[i]) {
                if (dp[j] + 1 > dp[i]) { dp[i] = dp[j] + 1; cnt[i] = cnt[j]; }
                else if (dp[j] + 1 == dp[i]) cnt[i] += cnt[j];   // tie: add
            }
        bestLen = Math.max(bestLen, dp[i]);
    }
    for (int i = 0; i < n; i++) if (dp[i] == bestLen) total += cnt[i];
    return total;
}   // O(n²) time · O(n) space""",
            "python": r"""def find_number_of_lis(nums):
    n = len(nums)
    dp = [1] * n                 # longest chain ending at i
    cnt = [1] * n                # how many chains of that length end at i
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    cnt[i] = cnt[j]          # a strictly longer chain: replace
                elif dp[j] + 1 == dp[i]:
                    cnt[i] += cnt[j]         # same length: add the routes
    best = max(dp)
    return sum(c for length, c in zip(dp, cnt) if length == best)""",
        },
    },
    {
        "slug": "best-time-to-buy-and-sell-stock-iv",
        "title": "Best Time to Buy and Sell Stock IV",
        "difficulty": "Hard",
        "pattern": "state machine over k transactions",
        "statement": "Given prices and a limit of k transactions (each a buy followed by a later sell), return the maximum profit. Only one share "
                     "may be held at a time.",
        "examples": [("k = 2, prices = [2,4,1]", "2"), ("k = 2, prices = [3,2,6,5,0,3]", "7")],
        "constraints": ["0 <= k <= 100", "0 <= prices.length <= 1000", "0 <= prices[i] <= 50"],
        "approach": "Two arrays per transaction count describe the best position after buying and after selling. Sweeping the transaction index "
                     "downwards inside the price loop keeps the sell used as a starting point one step *older*, which is exactly the ordering that "
                     "prevents buying and selling on the same update. When k is large the limit never binds and summing every upward move is optimal.",
        "complexity": ("O(n · k)", "O(k)"),
        "code": {
            "cpp": r"""// buy[t] / sell[t] = best cash with t transactions after buying / selling
int maxProfit(int k, vector<int>& prices) {
    int n = prices.size();
    if (n == 0 || k == 0) return 0;
    if (k >= n / 2) {                            // the limit never binds
        int total = 0;
        for (int i = 1; i < n; i++) total += max(0, prices[i] - prices[i-1]);
        return total;
    }
    vector<int> buy(k + 1, INT_MIN), sell(k + 1, 0);
    for (int p : prices)
        for (int t = k; t >= 1; t--) {           // descending: keep states consistent
            buy[t]  = max(buy[t],  sell[t-1] - p);   // open transaction t
            sell[t] = max(sell[t], buy[t] + p);      // or close it today
        }
    return sell[k];
}   // O(n · k) time · O(k) space""",
            "java": r"""// buy[t] / sell[t] = best cash with t transactions after buying / selling
int maxProfit(int k, int[] prices) {
    int n = prices.length;
    if (n == 0 || k == 0) return 0;
    if (k >= n / 2) {                            // the limit never binds
        int total = 0;
        for (int i = 1; i < n; i++) total += Math.max(0, prices[i] - prices[i-1]);
        return total;
    }
    int[] buy = new int[k + 1], sell = new int[k + 1];
    Arrays.fill(buy, Integer.MIN_VALUE);
    for (int p : prices)
        for (int t = k; t >= 1; t--) {           // descending: states stay consistent
            buy[t]  = Math.max(buy[t],  sell[t-1] - p);   // open transaction t
            sell[t] = Math.max(sell[t], buy[t] + p);      // or close it today
        }
    return sell[k];
}   // O(n · k) time · O(k) space""",
            "python": r"""def max_profit_k(k, prices):
    n = len(prices)
    if n == 0 or k == 0:
        return 0
    if k >= n // 2:                  # the limit never binds: take every rise
        return sum(max(0, prices[i] - prices[i-1]) for i in range(1, n))
    NEG = float('-inf')
    buy = [NEG] * (k + 1)
    sell = [0] * (k + 1)
    for p in prices:
        for t in range(k, 0, -1):    # descending keeps the states consistent
            buy[t] = max(buy[t], sell[t-1] - p)    # open transaction t
            sell[t] = max(sell[t], buy[t] + p)     # or close it today
    return sell[k]""",
        },
    },
    {
        "slug": "frog-jump",
        "title": "Frog Jump",
        "difficulty": "Hard",
        "pattern": "reachable-state sets (DP over positions and speeds)",
        "statement": "The frog starts on stone 0 and must land on the last stone. From a jump of size k it may next jump k-1, k or k+1, and it may "
                     "only land on a stone. Decide whether the crossing is possible.",
        "examples": [("stones = [0,1,3,5,6,8,12,17]", "true"), ("stones = [0,1,2,3,4,8,9,11]", "false")],
        "constraints": ["2 <= stones.length <= 2000", "0 <= stones[i] <= 2^31 - 1", "the stones are strictly increasing"],
        "approach": "The state is not the stone alone — it is the pair (stone, jump length), because the same stone reached with different speeds "
                     "allows different futures. Keeping a set of speeds per stone and pushing forward through the three possible next jumps visits "
                     "each state once.",
        "complexity": ("O(n²)", "O(n²)"),
        "code": {
            "cpp": r"""// State = (stone, last jump); push the three next jumps forward
bool canCross(vector<int>& stones) {
    unordered_map<int, unordered_set<int>> reach;    // stone -> jump sizes
    reach[stones[0]].insert(0);
    for (int s : stones) {
        for (int jump : reach[s]) {
            for (int next : {jump - 1, jump, jump + 1}) {
                if (next <= 0) continue;                     // k-1 must stay positive
                if (reach.count(s + next)) reach[s + next].insert(next);
            }
        }
    }
    return !reach[stones.back()].empty();            // the last stone is reachable
}   // O(n²) time · O(n²) space""",
            "java": r"""// State = (stone, last jump); push the three next jumps forward
boolean canCross(int[] stones) {
    Map<Integer, Set<Integer>> reach = new HashMap<>();   // stone -> jump sizes
    for (int s : stones) reach.put(s, new HashSet<>());
    reach.get(stones[0]).add(0);
    for (int s : stones) {
        for (int jump : reach.get(s)) {
            for (int next : new int[]{jump - 1, jump, jump + 1}) {
                if (next <= 0) continue;                 // k-1 must stay positive
                Set<Integer> target = reach.get(s + next);
                if (target != null) target.add(next);    // only stones can be hit
            }
        }
    }
    return !reach.get(stones[stones.length - 1]).isEmpty();
}   // O(n²) time · O(n²) space""",
            "python": r"""def can_cross(stones):
    reach = {s: set() for s in stones}      # stone -> jump sizes that reach it
    reach[stones[0]].add(0)
    for s in stones:
        for jump in reach[s]:
            for nxt in (jump - 1, jump, jump + 1):
                if nxt > 0 and s + nxt in reach:
                    reach[s + nxt].add(nxt)  # only stones can be landed on
    return bool(reach[stones[-1]])""",
        },
    },
    {
        "slug": "distinct-subsequences",
        "title": "Distinct Subsequences",
        "difficulty": "Hard",
        "pattern": "two-string counting table",
        "statement": "Count how many distinct subsequences of one string equal a second string, using any set of positions in the first.",
        "examples": [("s = \"rabbbit\", t = \"rabbit\"", "3"), ("s = \"babgbag\", t = \"bag\"", "5")],
        "constraints": ["1 <= lengths <= 1000", "strings contain English letters", "the answer fits in a 32-bit integer"],
        "approach": "dp[j] counts the ways to build the first j characters of the target from the prefix of the source read so far. Scanning j "
                     "downwards means each source character contributes its match exactly once, so a character can never be used twice in the same "
                     "subsequence.",
        "complexity": ("O(m · n)", "O(n)"),
        "code": {
            "cpp": r"""// dp[j] = ways to build the first j characters of t from s read so far
int numDistinct(string s, string t) {
    int n = t.size();
    vector<unsigned long long> dp(n + 1, 0);
    dp[0] = 1;                                   // the empty target is one way
    for (char c : s)
        for (int j = n; j >= 1; j--)             // descending: each copy used once
            if (c == t[j-1]) dp[j] += dp[j-1];
    return (int) dp[n];
}   // O(m · n) time · O(n) space""",
            "java": r"""// dp[j] = ways to build the first j characters of t from s read so far
int numDistinct(String s, String t) {
    int n = t.length();
    long[] dp = new long[n + 1];
    dp[0] = 1;                                   // the empty target is one way
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        for (int j = n; j >= 1; j--)             // descending: each copy used once
            if (c == t.charAt(j-1)) dp[j] += dp[j-1];
    }
    return (int) dp[n];
}   // O(m · n) time · O(n) space""",
            "python": r"""def num_distinct(s, t):
    n = len(t)
    dp = [0] * (n + 1)
    dp[0] = 1                    # the empty target can be built one way
    for c in s:
        for j in range(n, 0, -1):        # descending: each character used once
            if c == t[j-1]:
                dp[j] += dp[j-1]
    return dp[n]""",
        },
    },
    {
        "slug": "regular-expression-matching",
        "title": "Regular Expression Matching",
        "difficulty": "Hard",
        "pattern": "two-string table with a star case",
        "statement": "Match the whole string against a pattern where '.' matches any single character and '*' means zero or more of the preceding "
                     "element.",
        "examples": [("s = \"aa\", p = \"a\"", "false"), ("s = \"aa\", p = \"a*\"", "true"), ("s = \"ab\", p = \".*\"", "true")],
        "constraints": ["1 <= lengths <= 20", "s contains lowercase letters", "p contains lowercase letters, '.' and '*', and '*' never leads"],
        "approach": "The star is the only hard case. \"x*\" either matches nothing — which drops the whole pair and looks two columns back — or it "
                     "consumes one matching character and stays in the same column. Writing those two options as a disjunction, and the plain "
                     "character case as a diagonal step, is the complete recurrence.",
        "complexity": ("O(m · n)", "O(m · n)"),
        "code": {
            "cpp": r"""// dp[i][j]: s[0..i) matches p[0..j)
bool isMatch(string s, string p) {
    int m = s.size(), n = p.size();
    vector<vector<bool>> dp(m + 1, vector<bool>(n + 1, false));
    dp[0][0] = true;                             // empty matches empty
    for (int j = 2; j <= n; j++)
        if (p[j-1] == '*') dp[0][j] = dp[0][j-2];   // "x*" may match nothing
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++) {
            if (p[j-1] == '*') {
                char prev = p[j-2];
                dp[i][j] = dp[i][j-2]                         // zero copies
                        || ((prev == '.' || prev == s[i-1]) && dp[i-1][j]);  // one more
            } else if (p[j-1] == '.' || p[j-1] == s[i-1]) {
                dp[i][j] = dp[i-1][j-1];                      // consume one each
            }
        }
    return dp[m][n];
}   // O(m · n) time · O(m · n) space""",
            "java": r"""// dp[i][j]: s[0..i) matches p[0..j)
boolean isMatch(String s, String p) {
    int m = s.length(), n = p.length();
    boolean[][] dp = new boolean[m + 1][n + 1];
    dp[0][0] = true;                             // empty matches empty
    for (int j = 2; j <= n; j++)
        if (p.charAt(j-1) == '*') dp[0][j] = dp[0][j-2];   // "x*" may match nothing
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++) {
            if (p.charAt(j-1) == '*') {
                char prev = p.charAt(j-2);
                dp[i][j] = dp[i][j-2]                         // zero copies
                        || ((prev == '.' || prev == s.charAt(i-1)) && dp[i-1][j]);
            } else if (p.charAt(j-1) == '.' || p.charAt(j-1) == s.charAt(i-1)) {
                dp[i][j] = dp[i-1][j-1];                      // consume one each
            }
        }
    return dp[m][n];
}   // O(m · n) time · O(m · n) space""",
            "python": r"""def regex_match(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True                      # empty matches empty
    for j in range(2, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]        # "x*" may match the empty string
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                prev = p[j-2]
                dp[i][j] = dp[i][j-2] or (              # zero copies of prev
                    (prev == '.' or prev == s[i-1]) and dp[i-1][j])   # one more
            elif p[j-1] == '.' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]      # consume one character each
    return dp[m][n]""",
        },
    },
    {
        "slug": "wildcard-matching",
        "title": "Wildcard Matching",
        "difficulty": "Hard",
        "pattern": "two-string table with '?' and '*'",
        "statement": "Match the whole string against a pattern where '?' matches any single character and '*' matches any sequence, including an "
                     "empty one.",
        "examples": [("s = \"aa\", p = \"a\"", "false"), ("s = \"aa\", p = \"*\"", "true"),
                     ("s = \"cb\", p = \"?a\"", "false")],
        "constraints": ["0 <= lengths <= 2000", "s contains lowercase letters", "p contains lowercase letters, '?' and '*', with '*' matching anything"],
        "approach": "The same frame as the regular-expression problem, but '*' stands alone instead of modifying the previous element, so there are "
                     "just two options: let the star absorb the current character, or let it match nothing at all.",
        "complexity": ("O(m · n)", "O(m · n)"),
        "code": {
            "cpp": r"""// '*' absorbs one character (same column) or matches nothing (same row)
bool isMatch(string s, string p) {
    int m = s.size(), n = p.size();
    vector<vector<bool>> dp(m + 1, vector<bool>(n + 1, false));
    dp[0][0] = true;
    for (int j = 1; j <= n; j++)
        dp[0][j] = dp[0][j-1] && p[j-1] == '*';      // leading stars match empty
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++) {
            char pc = p[j-1];
            if (pc == '*') dp[i][j] = dp[i-1][j] || dp[i][j-1];
            else if (pc == '?' || pc == s[i-1]) dp[i][j] = dp[i-1][j-1];
        }
    return dp[m][n];
}   // O(m · n) time · O(m · n) space""",
            "java": r"""// '*' absorbs one character (same column) or matches nothing (same row)
boolean isMatch(String s, String p) {
    int m = s.length(), n = p.length();
    boolean[][] dp = new boolean[m + 1][n + 1];
    dp[0][0] = true;
    for (int j = 1; j <= n; j++)
        dp[0][j] = dp[0][j-1] && p.charAt(j-1) == '*';   // leading stars match empty
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++) {
            char pc = p.charAt(j-1);
            if (pc == '*') dp[i][j] = dp[i-1][j] || dp[i][j-1];
            else if (pc == '?' || pc == s.charAt(i-1)) dp[i][j] = dp[i-1][j-1];
        }
    return dp[m][n];
}   // O(m · n) time · O(m · n) space""",
            "python": r"""def wildcard_match(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] and p[j-1] == '*'    # leading stars match empty
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            pc = p[j-1]
            if pc == '*':
                dp[i][j] = dp[i-1][j] or dp[i][j-1]   # absorb one, or none
            elif pc == '?' or pc == s[i-1]:
                dp[i][j] = dp[i-1][j-1]               # exactly one character
    return dp[m][n]""",
        },
    },
    {
        "slug": "palindrome-partitioning-ii",
        "title": "Palindrome Partitioning II",
        "difficulty": "Hard",
        "pattern": "cut DP over a precomputed palindrome table",
        "statement": "Split the string into palindromic pieces using the fewest cuts. Return the number of cuts needed.",
        "examples": [("s = \"aab\"", "1"), ("s = \"a\"", "0"), ("s = \"ab\"", "1")],
        "constraints": ["1 <= s.length <= 2000", "s contains lowercase letters", "\"aab\" cuts as \"aa\" + \"b\""],
        "approach": "Two tables, one inside the other: first decide for every substring whether it is a palindrome, then let dp[i] be the fewest cuts "
                     "for the prefix of length i. Only palindrome suffixes matter, since the last piece must itself be a palindrome.",
        "complexity": ("O(n²)", "O(n²)"),
        "code": {
            "cpp": r"""// pal[l][r] first, then dp over prefixes
int minCut(string s) {
    int n = s.size();
    vector<vector<bool>> pal(n, vector<bool>(n, false));
    for (int l = n - 1; l >= 0; l--)             // shorter substrings first
        for (int r = l; r < n; r++)
            pal[l][r] = s[l] == s[r] && (r - l < 2 || pal[l+1][r-1]);
    vector<int> dp(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        dp[i] = i - 1;                           // worst case: cut every character
        for (int k = 0; k < i; k++)
            if (pal[k][i-1]) dp[i] = min(dp[i], k == 0 ? 0 : dp[k] + 1);
    }
    return dp[n];
}   // O(n²) time · O(n²) space""",
            "java": r"""// pal[l][r] first, then dp over prefixes
int minCut(String s) {
    int n = s.length();
    boolean[][] pal = new boolean[n][n];
    for (int l = n - 1; l >= 0; l--)             // shorter substrings first
        for (int r = l; r < n; r++)
            pal[l][r] = s.charAt(l) == s.charAt(r) && (r - l < 2 || pal[l+1][r-1]);
    int[] dp = new int[n + 1];
    for (int i = 1; i <= n; i++) {
        dp[i] = i - 1;                           // worst case: cut every character
        for (int k = 0; k < i; k++)
            if (pal[k][i-1]) dp[i] = Math.min(dp[i], k == 0 ? 0 : dp[k] + 1);
    }
    return dp[n];
}   // O(n²) time · O(n²) space""",
            "python": r"""def min_cuts(s):
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for l in range(n - 1, -1, -1):        # shorter substrings are solved first
        for r in range(l, n):
            pal[l][r] = s[l] == s[r] and (r - l < 2 or pal[l+1][r-1])
    dp = [0] * (n + 1)                   # dp[i]: cuts for the prefix of length i
    for i in range(1, n + 1):
        dp[i] = i - 1                    # worst case: cut every character
        for k in range(i):
            if pal[k][i-1]:
                dp[i] = min(dp[i], 0 if k == 0 else dp[k] + 1)
    return dp[n]""",
        },
    },
    {
        "slug": "burst-balloons",
        "title": "Burst Balloons",
        "difficulty": "Hard",
        "pattern": "interval DP (choose what bursts last)",
        "statement": "Bursting balloon i earns nums[i-1] * nums[i] * nums[i+1] using the current neighbours, and the balloon then disappears. Return "
                     "the maximum coins obtainable.",
        "examples": [("nums = [3,1,5,8]", "167"), ("nums = [1,5]", "10")],
        "constraints": ["1 <= nums.length <= 300", "0 <= nums[i] <= 100", "out-of-range neighbours count as 1"],
        "approach": "Thinking about which balloon bursts *first* is hopeless, because it changes every later neighbourhood. Thinking about which "
                     "bursts *last* inside a window splits the problem cleanly: the window's last balloon sees the window's two walls, and the two "
                     "inner pieces are independent subproblems.",
        "complexity": ("O(n³)", "O(n²)"),
        "code": {
            "cpp": r"""// dp[l][r]: best coins from the window (l, r); k bursts last inside it
int maxCoins(vector<int>& nums) {
    int n = nums.size();
    vector<int> a(n + 2, 1);                     // pad both walls with 1
    for (int i = 0; i < n; i++) a[i+1] = nums[i];
    vector<vector<int>> dp(n + 2, vector<int>(n + 2, 0));
    for (int len = 1; len <= n; len++)           // window length
        for (int l = 1; l + len - 1 <= n; l++) {
            int r = l + len - 1;
            for (int k = l; k <= r; k++)         // k is the last to burst
                dp[l][r] = max(dp[l][r],
                               dp[l][k-1] + dp[k+1][r] + a[l-1] * a[k] * a[r+1]);
        }
    return dp[1][n];
}   // O(n³) time · O(n²) space""",
            "java": r"""// dp[l][r]: best coins from the window (l, r); k bursts last inside it
int maxCoins(int[] nums) {
    int n = nums.length;
    int[] a = new int[n + 2];                    // pad both walls with 1
    Arrays.fill(a, 1);
    for (int i = 0; i < n; i++) a[i+1] = nums[i];
    int[][] dp = new int[n + 2][n + 2];
    for (int len = 1; len <= n; len++)           // window length
        for (int l = 1; l + len - 1 <= n; l++) {
            int r = l + len - 1;
            for (int k = l; k <= r; k++)         // k is the last to burst
                dp[l][r] = Math.max(dp[l][r],
                        dp[l][k-1] + dp[k+1][r] + a[l-1] * a[k] * a[r+1]);
        }
    return dp[1][n];
}   // O(n³) time · O(n²) space""",
            "python": r"""def max_coins(nums):
    a = [1] + nums + [1]             # pad both walls with 1
    n = len(nums)
    dp = [[0] * (n + 2) for _ in range(n + 2)]
    for length in range(1, n + 1):           # window of that many balloons
        for l in range(1, n - length + 2):
            r = l + length - 1
            for k in range(l, r + 1):        # k is the last balloon to burst
                coins = dp[l][k-1] + dp[k+1][r] + a[l-1] * a[k] * a[r+1]
                if coins > dp[l][r]:
                    dp[l][r] = coins
    return dp[1][n]""",
        },
    },
    {
        "slug": "minimum-cost-to-cut-a-stick",
        "title": "Minimum Cost to Cut a Stick",
        "difficulty": "Hard",
        "pattern": "interval DP over sorted cut positions",
        "statement": "A stick of length n must be cut at every position in cuts. Each cut costs the length of the piece being cut at that moment. "
                     "Return the minimum total cost.",
        "examples": [("n = 7, cuts = [1,3,4,5]", "16"), ("n = 9, cuts = [5,6,1,4,2]", "22")],
        "constraints": ["2 <= n <= 10^6", "1 <= cuts.length <= min(n-1, 100)", "cut positions are distinct"],
        "approach": "The same interval idea as burst balloons: sorting the cut positions (with the two stick ends added) turns them into boundary "
                     "points, and choosing which cut inside a window happens *first* splits the window into two independent sticks. The cost of a "
                     "window is always its full length, whatever the chosen cut inside it was.",
        "complexity": ("O(k³)", "O(k²)"),
        "code": {
            "cpp": r"""// Interval DP over the sorted cut positions plus the two ends
int minCost(int n, vector<int>& cuts) {
    cuts.push_back(0);
    cuts.push_back(n);
    sort(cuts.begin(), cuts.end());
    int m = cuts.size();
    vector<vector<int>> dp(m, vector<int>(m, 0));
    for (int len = 2; len < m; len++)            // window size in cut positions
        for (int i = 0; i + len < m; i++) {
            int j = i + len;
            dp[i][j] = INT_MAX;
            for (int k = i + 1; k < j; k++)      // k is cut first inside the window
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cuts[j] - cuts[i]);
        }
    return dp[0][m - 1];
}   // O(k³) time · O(k²) space""",
            "java": r"""// Interval DP over the sorted cut positions plus the two ends
int minCost(int n, int[] cuts) {
    int m = cuts.length + 2;
    int[] c = new int[m];
    c[0] = 0;
    c[m - 1] = n;
    for (int i = 0; i < cuts.length; i++) c[i + 1] = cuts[i];
    Arrays.sort(c);
    int[][] dp = new int[m][m];
    for (int len = 2; len < m; len++)            // window size in cut positions
        for (int i = 0; i + len < m; i++) {
            int j = i + len;
            dp[i][j] = Integer.MAX_VALUE;
            for (int k = i + 1; k < j; k++)      // k is cut first inside the window
                dp[i][j] = Math.min(dp[i][j], dp[i][k] + dp[k][j] + c[j] - c[i]);
        }
    return dp[0][m - 1];
}   // O(k³) time · O(k²) space""",
            "python": r"""def min_cut_cost(n, cuts):
    c = sorted([0] + cuts + [n])     # the two stick ends join the cut positions
    m = len(c)
    dp = [[0] * m for _ in range(m)]
    for length in range(2, m):               # window of that many boundary points
        for i in range(m - length):
            j = i + length
            best = float('inf')
            for k in range(i + 1, j):        # k is the first cut inside the window
                best = min(best, dp[i][k] + dp[k][j] + c[j] - c[i])
            dp[i][j] = best
    return dp[0][m - 1]""",
        },
    },
    {
        "slug": "cherry-pickup",
        "title": "Cherry Pickup",
        "difficulty": "Hard",
        "pattern": "two travellers on the same diagonal",
        "statement": "Two pickers start at the top-left and walk to the bottom-right, moving only right or down, collecting cherries from the cells they "
                     "pass. A cell's cherries are collected once even if both pass through it. Return the maximum total, or 0 if the route is blocked.",
        "examples": [("grid = [[0,1,-1],[1,0,-1],[1,1,1]]", "5"), ("grid = [[1,1,-1],[1,-1,1],[-1,1,1]]", "0")],
        "constraints": ["1 <= n <= 50", "grid[i][j] is -1, 0 or 1", "both pickers move simultaneously and share the grid"],
        "approach": "Run both pickers together. After the same number of steps they sit on the same anti-diagonal, so the state is just their two row "
                     "indices — the columns follow. When they land on one cell its cherries are counted once, which is exactly the rule the problem "
                     "describes.",
        "complexity": ("O(n³)", "O(n²)"),
        "code": {
            "cpp": r"""// Both pickers advance together: state = (step, row1, row2)
int cherryPickup(vector<vector<int>>& grid) {
    int n = grid.size();
    vector<vector<int>> dp(n, vector<int>(n, -1));
    dp[0][0] = grid[0][0];
    for (int step = 1; step <= 2 * n - 2; step++) {
        vector<vector<int>> nxt(n, vector<int>(n, -1));
        for (int r1 = 0; r1 < n; r1++) {
            int c1 = step - r1;                  // columns follow from the step
            if (c1 < 0 || c1 >= n || grid[r1][c1] == -1) continue;
            for (int r2 = 0; r2 < n; r2++) {
                int c2 = step - r2;
                if (c2 < 0 || c2 >= n || grid[r2][c2] == -1) continue;
                int gained = grid[r1][c1] + (r1 == r2 ? 0 : grid[r2][c2]);
                int best = -1;
                for (int p1 = r1 - 1; p1 <= r1; p1++)      // came from above or left
                    for (int p2 = r2 - 1; p2 <= r2; p2++)
                        if (p1 >= 0 && p2 >= 0) best = max(best, dp[p1][p2]);
                if (best >= 0) nxt[r1][r2] = best + gained;
            }
        }
        dp = move(nxt);
    }
    return max(0, dp[n-1][n-1]);                 // -1 means the route is blocked
}   // O(n³) time · O(n²) space""",
            "java": r"""// Both pickers advance together: state = (step, row1, row2)
int cherryPickup(int[][] grid) {
    int n = grid.length;
    int[][] dp = new int[n][n];
    for (int[] row : dp) Arrays.fill(row, -1);
    dp[0][0] = grid[0][0];
    for (int step = 1; step <= 2 * n - 2; step++) {
        int[][] nxt = new int[n][n];
        for (int[] row : nxt) Arrays.fill(row, -1);
        for (int r1 = 0; r1 < n; r1++) {
            int c1 = step - r1;                  // columns follow from the step
            if (c1 < 0 || c1 >= n || grid[r1][c1] == -1) continue;
            for (int r2 = 0; r2 < n; r2++) {
                int c2 = step - r2;
                if (c2 < 0 || c2 >= n || grid[r2][c2] == -1) continue;
                int gained = grid[r1][c1] + (r1 == r2 ? 0 : grid[r2][c2]);
                int best = -1;
                for (int p1 = r1 - 1; p1 <= r1; p1++)      // from above or left
                    for (int p2 = r2 - 1; p2 <= r2; p2++)
                        if (p1 >= 0 && p2 >= 0) best = Math.max(best, dp[p1][p2]);
                if (best >= 0) nxt[r1][r2] = best + gained;
            }
        }
        dp = nxt;
    }
    return Math.max(0, dp[n-1][n-1]);             // -1: the route is blocked
}   // O(n³) time · O(n²) space""",
            "python": r"""def cherry_pickup(grid):
    n = len(grid)
    dp = [[-1] * n for _ in range(n)]
    dp[0][0] = grid[0][0]
    for step in range(1, 2 * n - 1):
        nxt = [[-1] * n for _ in range(n)]
        for r1 in range(n):
            c1 = step - r1                   # columns follow from the step count
            if not (0 <= c1 < n) or grid[r1][c1] == -1:
                continue
            for r2 in range(n):
                c2 = step - r2
                if not (0 <= c2 < n) or grid[r2][c2] == -1:
                    continue
                gained = grid[r1][c1] + (0 if r1 == r2 else grid[r2][c2])
                best = -1
                for p1 in (r1 - 1, r1):      # each picker came from above or left
                    for p2 in (r2 - 1, r2):
                        if p1 >= 0 and p2 >= 0 and dp[p1][p2] > best:
                            best = dp[p1][p2]
                if best >= 0:
                    nxt[r1][r2] = best + gained
        dp = nxt
    return max(0, dp[n-1][n-1])              # -1 would mean the route is blocked""",
        },
    },
    {
        "slug": "maximum-profit-in-job-scheduling",
        "title": "Maximum Profit in Job Scheduling",
        "difficulty": "Hard",
        "pattern": "sorted DP with binary search for the previous compatible job",
        "statement": "Each job has a start time, an end time and a profit, and chosen jobs may not overlap. Return the maximum total profit.",
        "examples": [("startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]", "120"),
                     ("startTime = [1,2,3,4,6], endTime = [3,5,10,6,9], profit = [20,20,100,70,60]", "150"),
                     ("startTime = [1,1,1], endTime = [2,3,4], profit = [5,6,4]", "6")],
        "constraints": ["1 <= number of jobs <= 5 · 10^4", "startTime[i] < endTime[i]", "times and profits fit in 32-bit integers"],
        "approach": "Sort the jobs by end time and let dp[i] be the best profit using the first i jobs. Taking job i is only possible after the last "
                     "job that finishes at or before its start, which binary search finds in the sorted end times. This is the weighted interval "
                     "scheduling recurrence, and the binary search is what keeps it from becoming quadratic.",
        "complexity": ("O(n log n)", "O(n)"),
        "code": {
            "cpp": r"""// Weighted interval scheduling: sort by end time, binary search the gap
int jobScheduling(vector<int>& startTime, vector<int>& endTime, vector<int>& profit) {
    int n = startTime.size();
    vector<array<int,3>> jobs(n);                 // {end, start, profit}
    for (int i = 0; i < n; i++) jobs[i] = {endTime[i], startTime[i], profit[i]};
    sort(jobs.begin(), jobs.end());              // by end time
    vector<int> ends(n), dp(n + 1, 0);
    for (int i = 0; i < n; i++) ends[i] = jobs[i][0];
    for (int i = 1; i <= n; i++) {
        int start = jobs[i-1][1], gain = jobs[i-1][2];
        // last job (among the first i-1) that ends at or before this start
        int j = upper_bound(ends.begin(), ends.begin() + i - 1, start) - ends.begin();
        dp[i] = max(dp[i-1], dp[j] + gain);      // skip this job, or take it
    }
    return dp[n];
}   // O(n log n) time · O(n) space""",
            "java": r"""// Weighted interval scheduling: sort by end time, binary search the gap
int jobScheduling(int[] startTime, int[] endTime, int[] profit) {
    int n = startTime.length;
    int[][] jobs = new int[n][3];
    for (int i = 0; i < n; i++) jobs[i] = new int[]{endTime[i], startTime[i], profit[i]};
    Arrays.sort(jobs, (a, b) -> a[0] - b[0]);    // by end time
    int[] ends = new int[n], dp = new int[n + 1];
    for (int i = 0; i < n; i++) ends[i] = jobs[i][0];
    for (int i = 1; i <= n; i++) {
        int start = jobs[i-1][1], gain = jobs[i-1][2];
        int j = upperBound(ends, i - 1, start);  // last job ending at or before start
        dp[i] = Math.max(dp[i-1], dp[j] + gain); // skip this job, or take it
    }
    return dp[n];
}
int upperBound(int[] a, int hi, int key) {       // first index >= key, within a[0..hi)
    int lo = 0;
    while (lo < hi) {
        int mid = (lo + hi) >>> 1;
        if (a[mid] <= key) lo = mid + 1; else hi = mid;
    }
    return lo;
}   // O(n log n) time · O(n) space""",
            "python": r"""from bisect import bisect_right

def job_scheduling(start_time, end_time, profit):
    jobs = sorted(zip(end_time, start_time, profit))   # by end time
    ends = [j[0] for j in jobs]
    n = len(jobs)
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        end, start, gain = jobs[i-1]
        # last earlier job that ends at or before this job's start
        j = bisect_right(ends, start, 0, i - 1)
        dp[i] = max(dp[i-1], dp[j] + gain)     # skip this job, or take it
    return dp[n]""",
        },
    },
]
