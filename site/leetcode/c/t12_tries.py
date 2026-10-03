# Topic 12 · Tries & String Algorithms — C17 solutions
#
# A trie in C is just a node with 26 children (or 128 for general ASCII) allocated on
# demand. String problems that are not tries are almost always counting, sliding windows
# or KMP — the three string idioms worth memorising.

CODE = {
    "length-of-last-word": r"""
// Walk backwards: skip the trailing spaces, then count the letters.
int lengthOfLastWord(const char *s) {
    int i = (int) strlen(s) - 1;
    while (i >= 0 && s[i] == ' ') i--;
    int length = 0;
    while (i >= 0 && s[i] != ' ') { length++; i--; }
    return length;
}   // O(n) time · O(1) space
""",
    "reverse-words-in-a-string-iii": r"""
// Reverse each run of non-space characters, leaving the spaces where they are.
char *reverseWords(char *s) {
    int n = (int) strlen(s), start = 0;
    for (int i = 0; i <= n; i++) {
        if (i < n && s[i] != ' ') continue;
        for (int left = start, right = i - 1; left < right; left++, right--) {
            char t = s[left]; s[left] = s[right]; s[right] = t;   // reverse this word
        }
        start = i + 1;
    }
    return s;
}   // O(n) time · O(1) space
""",
    "sorting-the-sentence": r"""
// Every token ends in a digit: that digit gives its slot in the answer.
char *sortSentence(const char *s) {
    char *tokens[10] = {0};
    int n = (int) strlen(s), i = 0;
    while (i < n) {
        int start = i;
        while (i < n && s[i] != ' ') i++;
        int slot = s[i - 1] - '1';                         // the trailing digit
        int length = i - start - 1;
        tokens[slot] = malloc((size_t) length + 1);
        memcpy(tokens[slot], s + start, (size_t) length);
        tokens[slot][length] = '\0';
        i++;
    }
    char *out = malloc((size_t) n + 1);
    out[0] = '\0';
    for (int slot = 0; slot < 10; slot++) {
        if (!tokens[slot]) continue;
        if (out[0]) strcat(out, " ");
        strcat(out, tokens[slot]);
        free(tokens[slot]);
    }
    return out;
}   // O(n) time · O(n) space
""",
    "uncommon-words-from-two-sentences": r"""
// Split both sentences, then keep the words that appear exactly once overall.
static int countWord(char words[][32], int n, const char *target) {
    int count = 0;
    for (int i = 0; i < n; i++)
        if (!strcmp(words[i], target)) count++;
    return count;
}

char **uncommonFromSentences(const char *s1, const char *s2, int *returnSize) {
    char words[512][32];
    int n = 0;
    for (int part = 0; part < 2; part++) {
        const char *text = part ? s2 : s1;
        for (int i = 0, start = 0; ; i++) {
            if (text[i] && text[i] != ' ') continue;
            if (i > start) {
                int length = i - start < 31 ? i - start : 31;
                memcpy(words[n], text + start, (size_t) length);
                words[n][length] = '\0';
                n++;
            }
            start = i + 1;
            if (!text[i]) break;
        }
    }
    char **out = malloc(sizeof(char *) * (size_t) n);
    int count = 0;
    for (int i = 0; i < n; i++) {
        if (countWord(words, n, words[i]) != 1) continue;   // appears once in total
        out[count] = malloc(strlen(words[i]) + 1);
        strcpy(out[count], words[i]);
        count++;
    }
    *returnSize = count;
    return out;
}   // O(n^2) time · O(n) space
""",
    "find-words-that-can-be-formed-by-characters": r"""
// An array of 26 counters answers "can these letters spell this word?".
int countCharacters(char **words, int wordCount, const char *chars) {
    int available[26] = {0};
    for (int i = 0; chars[i]; i++) available[chars[i] - 'a']++;
    int total = 0;
    for (int i = 0; i < wordCount; i++) {
        int need[26] = {0}, ok = 1;
        for (int j = 0; words[i][j] && ok; j++) {
            int c = words[i][j] - 'a';
            if (++need[c] > available[c]) ok = 0;
        }
        if (ok) total += (int) strlen(words[i]);
    }
    return total;
}   // O(total letters) time · O(1) space
""",
    "rotate-string": r"""
// A rotation of s is a substring of s + s, provided the lengths match.
int rotateString(const char *s, const char *goal) {
    int n = (int) strlen(s);
    if (n != (int) strlen(goal)) return 0;
    char *doubled = malloc((size_t) 2 * n + 1);
    strcpy(doubled, s);
    strcat(doubled, s);
    int found = strstr(doubled, goal) != NULL;              // substring search
    free(doubled);
    return found;
}   // O(n) time · O(n) space
""",
    "implement-trie-prefix-tree": r"""
// Each node has 26 slots plus an end-of-word flag; children appear on demand.
typedef struct TrieNode {
    struct TrieNode *children[26];
    int isWord;
} Trie;

Trie *trieCreate(void) { return calloc(1, sizeof(Trie)); }

void trieInsert(Trie *t, const char *word) {
    Trie *node = t;
    for (int i = 0; word[i]; i++) {
        int c = word[i] - 'a';
        if (!node->children[c]) node->children[c] = calloc(1, sizeof(Trie));
        node = node->children[c];
    }
    node->isWord = 1;
}

static Trie *walk(Trie *t, const char *word) {
    Trie *node = t;
    for (int i = 0; word[i] && node; i++) node = node->children[word[i] - 'a'];
    return node;
}

int trieSearch(Trie *t, const char *word) {
    Trie *node = walk(t, word);
    return node && node->isWord;
}

int trieStartsWith(Trie *t, const char *prefix) { return walk(t, prefix) != NULL; }
// O(length) per operation · O(total letters * 26) space
""",
    "map-sum-pairs": r"""
// A trie whose nodes also carry a value: sum the values on the prefix path.
typedef struct MapNode {
    struct MapNode *children[26];
    int value;
} MapSum;

MapSum *mapSumCreate(void) { return calloc(1, sizeof(MapSum)); }

void mapSumInsert(MapSum *m, const char *key, int val) {
    MapSum *node = m;
    for (int i = 0; key[i]; i++) {
        int c = key[i] - 'a';
        if (!node->children[c]) node->children[c] = calloc(1, sizeof(MapSum));
        node = node->children[c];
    }
    node->value = val;                                     // overwrite when the key exists again
}

static void collect(MapSum *node, int *total) {
    if (!node) return;
    *total += node->value;
    for (int c = 0; c < 26; c++) collect(node->children[c], total);
}

int mapSumSum(MapSum *m, const char *prefix) {
    MapSum *node = m;
    for (int i = 0; prefix[i] && node; i++) node = node->children[prefix[i] - 'a'];
    int total = 0;
    collect(node, &total);
    return total;
}   // O(prefix + subtree) per query · O(total letters * 26) space
""",
    "replace-words": r"""
// Walk each word through the trie of roots and stop at the first root found.
typedef struct Node { struct Node *children[26]; int isRoot; } Node;

char *replaceWords(char **dictionary, int dictCount, const char *sentence) {
    Node *root = calloc(1, sizeof(Node));
    for (int i = 0; i < dictCount; i++) {
        Node *node = root;
        for (int j = 0; dictionary[i][j]; j++) {
            int c = dictionary[i][j] - 'a';
            if (!node->children[c]) node->children[c] = calloc(1, sizeof(Node));
            node = node->children[c];
        }
        node->isRoot = 1;                                  // a complete root word ends here
    }
    char *out = calloc(8192, 1);
    int n = (int) strlen(sentence), written = 0;
    for (int i = 0, start = 0; ; i++) {
        if (i < n && sentence[i] != ' ') continue;
        int length = i - start;
        Node *node = root;
        int matched = 0;
        for (int j = 0; j < length && node; j++) {          // shortest root that is a prefix
            node = node->children[sentence[start + j] - 'a'];
            if (node && node->isRoot) { matched = j + 1; break; }
        }
        if (written) out[written++] = ' ';
        if (matched) {
            memcpy(out + written, sentence + start, (size_t) matched);
            written += matched;
        } else {
            memcpy(out + written, sentence + start, (size_t) length);
            written += length;
        }
        start = i + 1;
        if (i >= n) break;
    }
    out[written] = '\0';
    return out;
}   // O(n * word length) time · O(dictionary) space
""",
    "longest-word-in-dictionary": r"""
// Sort the words; a word is buildable when every prefix of it is in the list.
static int cmpStr(const void *a, const void *b) {
    const char *x = *(char *const *) a, *y = *(char *const *) b;
    return strcmp(x, y);                                   // short words first, then alphabetical
}

static int hasWord(char **words, int n, const char *target, int length) {
    for (int i = 0; i < n; i++) if ((int) strlen(words[i]) == length && !strncmp(words[i], target, (size_t) length)) return 1;
    return 0;
}

char *longestWord(char **words, int n) {
    qsort(words, (size_t) n, sizeof(char *), cmpStr);
    char *best = strdup("");
    for (int i = 0; i < n; i++) {
        int length = (int) strlen(words[i]), buildable = 1;
        for (int prefix = 1; prefix <= length && buildable; prefix++)
            if (!hasWord(words, n, words[i], prefix)) buildable = 0;
        if (buildable) {
            if (length > (int) strlen(best) ||
                (length == (int) strlen(best) && strcmp(words[i], best) < 0)) {
                free(best);
                best = strdup(words[i]);
            }
        }
    }
    return best;
}   // O(n^2 * length) with this scan · O(n) space
""",
    "search-suggestions-system": r"""
// Insert every product into a trie, then collect up to three sentences per prefix.
typedef struct Sug { struct Sug *children[26]; int last; } Sug;

static void collectWords(Sug *node, char *path, int depth, char ***out, int *count, int limit) {
    if (!node || *count >= limit) return;
    if (node->last) {
        path[depth] = '\0';
        (*out)[*count] = strdup(path);
        (*count)++;
    }
    for (int c = 0; c < 26 && *count < limit; c++) {
        if (!node->children[c]) continue;
        path[depth] = (char) ('a' + c);                    // depth-first gives alphabetical order
        collectWords(node->children[c], path, depth + 1, out, count, limit);
    }
}

char ***suggestedProducts(char **products, int n, const char *searchWord, int *returnSize, int **returnColumnSizes) {
    Sug *root = calloc(1, sizeof(Sug));
    for (int i = 0; i < n; i++) {
        Sug *node = root;
        for (int j = 0; products[i][j]; j++) {
            int c = products[i][j] - 'a';
            if (!node->children[c]) node->children[c] = calloc(1, sizeof(Sug));
            node = node->children[c];
        }
        node->last = 1;
    }
    int length = (int) strlen(searchWord);
    char ***out = malloc(sizeof(char **) * (size_t) length);
    *returnColumnSizes = malloc(sizeof(int) * (size_t) length);
    Sug *node = root;
    char path[512];
    for (int i = 0; i < length; i++) {
        if (node) node = node->children[searchWord[i] - 'a'];
        out[i] = malloc(sizeof(char *) * 3);
        int count = 0;
        if (node) {
            memcpy(path, searchWord, (size_t) i + 1);
            collectWords(node, path, i + 1, &out[i], &count, 3);
        }
        (*returnColumnSizes)[i] = count;
    }
    *returnSize = length;
    return out;
}   // O(total letters + n * 3) time · O(total letters * 26) space
""",
    "design-add-and-search-words-data-structure": r"""
// '.' means "any letter", so a query is a small depth-first search over the trie.
typedef struct WordNode { struct WordNode *children[26]; int isWord; } WordDictionary;

WordDictionary *wordDictionaryCreate(void) { return calloc(1, sizeof(WordDictionary)); }

void wordDictionaryAddWord(WordDictionary *d, const char *word) {
    WordDictionary *node = d;
    for (int i = 0; word[i]; i++) {
        int c = word[i] - 'a';
        if (!node->children[c]) node->children[c] = calloc(1, sizeof(WordDictionary));
        node = node->children[c];
    }
    node->isWord = 1;
}

static int searchFrom(WordDictionary *node, const char *word) {
    if (!node) return 0;
    if (!*word) return node->isWord;
    if (*word == '.') {
        for (int c = 0; c < 26; c++)                       // try every branch
            if (searchFrom(node->children[c], word + 1)) return 1;
        return 0;
    }
    return searchFrom(node->children[*word - 'a'], word + 1);
}

int wordDictionarySearch(WordDictionary *d, const char *word) { return searchFrom(d, word); }
// O(26^dots * length) worst case · O(total letters * 26) space
""",
    "subdomain-visit-count": r"""
// Split "count domain", add the count to the domain and to every parent suffix.
typedef struct { char name[128]; int visits; } Entry;

static Entry *findEntry(Entry *table, int *n, const char *name) {
    for (int i = 0; i < *n; i++) if (!strcmp(table[i].name, name)) return &table[i];
    snprintf(table[*n].name, 128, "%s", name);
    table[*n].visits = 0;
    return &table[(*n)++];
}

char **subdomainVisits(char **cpdomains, int n, int *returnSize) {
    Entry *table = calloc(512, sizeof(Entry));
    int count = 0;
    for (int i = 0; i < n; i++) {
        int visits = atoi(cpdomains[i]);
        char *space = strchr(cpdomains[i], ' ');
        char *domain = space + 1;
        findEntry(table, &count, domain)->visits += visits;
        for (char *dot = strchr(domain, '.'); dot; dot = strchr(dot + 1, '.'))
            findEntry(table, &count, dot + 1)->visits += visits;   // every parent suffix
    }
    char **out = malloc(sizeof(char *) * (size_t) count);
    for (int i = 0; i < count; i++) {
        out[i] = malloc(160);
        snprintf(out[i], 160, "%d %s", table[i].visits, table[i].name);
    }
    free(table);
    *returnSize = count;
    return out;
}   // O(n * domain length * table size) time · O(table) space
""",
    "string-to-integer-atoi": r"""
// Read the signs, then the digits, clamping at the 32-bit limits.
int myAtoi(const char *s) {
    int i = 0;
    while (s[i] == ' ') i++;
    int sign = 1;
    if (s[i] == '+' || s[i] == '-') { if (s[i] == '-') sign = -1; i++; }
    long long value = 0;
    while (s[i] >= '0' && s[i] <= '9') {
        value = value * 10 + (s[i] - '0');
        if (value > 2147483648LL) value = 2147483648LL;     // stop early: it clamps anyway
        i++;
    }
    value *= sign;
    if (value > INT_MAX) return INT_MAX;
    if (value < INT_MIN) return INT_MIN;
    return (int) value;
}   // O(n) time · O(1) space
""",
    "find-all-anagrams-in-a-string": r"""
// Slide a window of p's length and compare the two 26-letter counters.
int *findAnagrams(const char *s, const char *p, int *returnSize) {
    int n = (int) strlen(s), m = (int) strlen(p);
    int *out = malloc(sizeof(int) * (size_t) (n + 1));
    int count = 0;
    if (m > n) { *returnSize = 0; return out; }
    int need[26] = {0}, have[26] = {0};
    for (int i = 0; i < m; i++) need[p[i] - 'a']++;
    for (int i = 0; i < n; i++) {
        have[s[i] - 'a']++;
        if (i >= m) have[s[i - m] - 'a']--;                // drop the letter leaving the window
        if (i >= m - 1 && !memcmp(need, have, sizeof need)) out[count++] = i - m + 1;
    }
    *returnSize = count;
    return out;
}   // O(n) time · O(1) space
""",
    "making-file-names-unique": r"""
// Keep every name already used; a clash becomes name(1), name(2), \u2026
char **getFolderNames(char **names, int n, int *returnSize) {
    char **out = malloc(sizeof(char *) * (size_t) n);
    char **used = malloc(sizeof(char *) * (size_t) (n * 2));
    int usedCount = 0;
    for (int i = 0; i < n; i++) {
        char base[64];
        snprintf(base, sizeof base, "%s", names[i]);
        char *open = strchr(base, '(');
        if (open) {                                        // "name(k)" keeps only "name"
            char *close = strchr(open, ')');
            if (close && close[1] == '\0') *open = '\0';
        }
        char candidate[80];
        snprintf(candidate, sizeof candidate, "%s", base);
        int counter = 0;
        while (1) {
            int taken = 0;
            for (int u = 0; u < usedCount && !taken; u++)
                if (!strcmp(used[u], candidate)) taken = 1;
            if (!taken) break;                             // this name is free
            counter++;
            snprintf(candidate, sizeof candidate, "%s(%d)", base, counter);
        }
        out[i] = strdup(candidate);
        used[usedCount++] = out[i];
        if (counter) {                                     // the "name(k)" form is now used too
            char numbered[80];
            snprintf(numbered, sizeof numbered, "%s", names[i]);
            used[usedCount++] = strdup(numbered);
        }
    }
    free(used);
    *returnSize = n;
    return out;
}   // O(n^2 * length) time \u00b7 O(n) space
""",
    "lexicographical-numbers": r"""
// Walking the tree of prefixes: 1, 10, 100, … then back up like a pre-order traversal.
int *lexicalOrder(int n, int *returnSize) {
    int *out = malloc(sizeof(int) * (size_t) n);
    int count = 0;
    long long current = 1;
    while (count < n) {
        out[count++] = (int) current;
        if (current * 10 <= n) current *= 10;               // go deeper
        else {
            while (current % 10 == 9 || current + 1 > n) current /= 10;   // no sibling: up
            current++;                                      // next sibling
        }
    }
    *returnSize = count;
    return out;
}   // O(n) time · O(1) space
""",
    "number-of-matching-subsequences": r"""
// Two pointers per word: walk the source once and advance every waiting word.
int numMatchingSubseq(const char *s, char **words, int n) {
    int matched = 0;
    for (int i = 0; i < n; i++) {
        int j = 0;
        for (int k = 0; s[k] && words[i][j]; k++)
            if (s[k] == words[i][j]) j++;                   // consume the next needed letter
        if (!words[i][j]) matched++;
    }
    return matched;
}   // O(n * length) time · O(1) space
""",
    "stream-of-characters": r"""
// Only the last maxLength letters can matter, so keep them and test every suffix.
typedef struct {
    char **words;
    int size, maxLength, length;
    char buffer[8192];
} StreamChecker;

StreamChecker *streamCheckerCreate(char **words, int wordCount, int maxLength) {
    StreamChecker *c = calloc(1, sizeof(StreamChecker));
    c->words = malloc(sizeof(char *) * (size_t) wordCount);
    for (int i = 0; i < wordCount; i++) c->words[i] = words[i];
    c->size = wordCount;
    c->maxLength = maxLength;
    return c;
}

int streamCheckerQuery(StreamChecker *c, char letter) {
    if (c->length == c->maxLength) {                       // drop the oldest letter
        memmove(c->buffer, c->buffer + 1, (size_t) (c->length - 1));
        c->length--;
    }
    c->buffer[c->length++] = letter;
    for (int i = 0; i < c->size; i++) {
        int w = (int) strlen(c->words[i]);
        if (w <= c->length && !strncmp(c->buffer + c->length - w, c->words[i], (size_t) w)) return 1;
    }
    return 0;
}   // O(maxLength * words) per query \u00b7 O(maxLength + words) space
""",
    "prefix-and-suffix-search": r"""
// Store every "suffix#prefix" combination in a hash-like table and remember its index.
typedef struct { char key[512]; int index; } Combo;

typedef struct { Combo *table; int count; } WordFilter;

WordFilter *wordFilterCreate(char **words, int n) {
    WordFilter *f = calloc(1, sizeof(WordFilter));
    int capacity = n * 64;
    f->table = calloc((size_t) capacity, sizeof(Combo));
    for (int i = 0; i < n; i++) {
        int length = (int) strlen(words[i]);
        for (int suffix = 0; suffix < length; suffix++) {
            char key[512];
            snprintf(key, sizeof key, "%s#%s", words[i] + suffix, words[i]);
            for (int prefix = 1; prefix <= length; prefix++) {
                char full[512];
                snprintf(full, sizeof full, "%s|%.*s", key, prefix, words[i]);
                int slot = 0;                              // simple hash of the combination
                for (int c = 0; full[c]; c++) slot = (slot * 31 + full[c]) % capacity;
                while (f->table[slot].index && strcmp(f->table[slot].key, full)) slot = (slot + 1) % capacity;
                snprintf(f->table[slot].key, 512, "%s", full);
                f->table[slot].index = i + 1;              // later words win: keep overwriting
            }
        }
    }
    f->count = capacity;
    return f;
}

int wordFilterF(WordFilter *f, const char *prefix, const char *suffix) {
    char full[512];
    snprintf(full, sizeof full, "%s#%s|%s", suffix, prefix, prefix);
    int slot = 0;
    for (int c = 0; full[c]; c++) slot = (slot * 31 + full[c]) % f->count;
    while (f->table[slot].index && strcmp(f->table[slot].key, full)) slot = (slot + 1) % f->count;
    return f->table[slot].index ? f->table[slot].index - 1 : -1;
}   // O(n * length^2) build · O(n * length^2) space
""",
    "word-search-ii": r"""
// Depth-first search on the board, pruned by the trie of the words.
typedef struct WNode { struct WNode *children[26]; char *word; } WNode;

static void explore(char **board, int rows, int cols, int r, int c, WNode *node,
                    char **out, int *count) {
    if (r < 0 || r >= rows || c < 0 || c >= cols) return;
    char letter = board[r][c];
    if (letter == '#') return;                             // already used on this path
    WNode *next = node->children[letter - 'a'];
    if (!next) return;
    if (next->word) {                                      // a complete word ends here
        out[*count] = strdup(next->word);
        (*count)++;
        next->word = NULL;                                 // report each word once
    }
    board[r][c] = '#';
    explore(board, rows, cols, r + 1, c, next, out, count);
    explore(board, rows, cols, r - 1, c, next, out, count);
    explore(board, rows, cols, r, c + 1, next, out, count);
    explore(board, rows, cols, r, c - 1, next, out, count);
    board[r][c] = letter;
}

char **findWords(char **board, int rows, char **words, int n, int *returnSize) {
    int cols = (!rows) ? 0 : (int) strlen(board[0]);
    WNode *root = calloc(1, sizeof(WNode));
    for (int i = 0; i < n; i++) {
        WNode *node = root;
        for (int j = 0; words[i][j]; j++) {
            int ch = words[i][j] - 'a';
            if (!node->children[ch]) node->children[ch] = calloc(1, sizeof(WNode));
            node = node->children[ch];
        }
        node->word = words[i];
    }
    char **out = malloc(sizeof(char *) * (size_t) n);
    int count = 0;
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++) explore(board, rows, cols, r, c, root, out, &count);
    *returnSize = count;
    return out;
}   // O(rows * cols * word length) time · O(total letters * 26) space
""",
    "concatenated-words": r"""
// A word is made of others when every suffix keeps splitting into dictionary words.
static int isBuildable(const char *word, char **words, int n, int depth) {
    if (depth > 0) {
        for (int i = 0; i < n; i++) if (!strcmp(words[i], word)) return 1;   // ends on a word
    }
    for (int split = 1; word[split]; split++) {
        int matches = 0;
        for (int i = 0; i < n && !matches; i++)
            if ((int) strlen(words[i]) == split && !strncmp(words[i], word, (size_t) split)) matches = 1;
        if (matches && isBuildable(word + split, words, n, depth + 1)) return 1;
    }
    return 0;
}

char **findAllConcatenatedWordsInADict(char **words, int n, int *returnSize) {
    char **out = malloc(sizeof(char *) * (size_t) n);
    int count = 0;
    for (int i = 0; i < n; i++) {
        if (isBuildable(words[i], words, n, 0)) {
            out[count] = malloc(strlen(words[i]) + 1);
            strcpy(out[count], words[i]);
            count++;
        }
    }
    *returnSize = count;
    return out;
}   // O(n^2 * length^2) time · O(length) recursion
""",
    "longest-chunked-palindrome-decomposition": r"""
// Take the shortest possible chunk each time: greedily comparing the two ends.
int longestDecomposition(const char *text) {
    int n = (int) strlen(text), count = 0;
    int left = 0, right = n - 1;
    while (left <= right) {
        int length = 1, found = 0;
        while (left + length - 1 < right - length + 1) {    // try chunk sizes from 1 upwards
            if (!strncmp(text + left, text + right - length + 1, (size_t) length)) { found = 1; break; }
            length++;
        }
        if (found) {                                       // a matching pair of chunks
            count += 2;
            left += length;
            right -= length;
        } else {
            count++;                                       // the middle is one chunk
            break;
        }
    }
    return count;
}   // O(n^2) time · O(1) space
""",
    "longest-happy-prefix": r"""
// KMP on the string itself: the last value of the prefix function is the answer.
char *longestPrefix(const char *s) {
    int n = (int) strlen(s);
    int *fail = malloc(sizeof(int) * (size_t) (n + 1));
    fail[0] = 0;
    for (int i = 1; i < n; i++) {
        int length = fail[i - 1];
        while (length && s[i] != s[length]) length = fail[length - 1];
        if (s[i] == s[length]) length++;
        fail[i] = length;
    }
    int best = n ? fail[n - 1] : 0;                        // proper prefix: strictly shorter
    char *out = malloc((size_t) best + 1);
    memcpy(out, s, (size_t) best);
    out[best] = '\0';
    free(fail);
    return out;
}   // O(n) time · O(n) space
""",
    "shortest-palindrome": r"""
// The longest palindromic prefix is found with KMP on s + '#' + reversed(s).
char *shortestPalindrome(const char *s) {
    int n = (int) strlen(s);
    char *combined = malloc((size_t) 2 * n + 2);
    snprintf(combined, (size_t) 2 * n + 2, "%s#", s);
    for (int i = 0; i < n; i++) combined[n + 1 + i] = s[n - 1 - i];
    combined[2 * n + 1] = '\0';
    int size = 2 * n + 1;
    int *fail = malloc(sizeof(int) * (size_t) (size + 1));
    fail[0] = 0;
    for (int i = 1; i < size; i++) {
        int length = fail[i - 1];
        while (length && combined[i] != combined[length]) length = fail[length - 1];
        if (combined[i] == combined[length]) length++;
        fail[i] = length;
    }
    int palindromicPrefix = fail[size - 1];                // how much of s is already a palindrome
    int extra = n - palindromicPrefix;
    char *out = malloc((size_t) n + (size_t) extra + 1);
    for (int i = 0; i < extra; i++) out[i] = s[n - 1 - i];
    memcpy(out + extra, s, (size_t) n);
    out[extra + n] = '\0';
    free(combined); free(fail);
    return out;
}   // O(n) time · O(n) space
""",
    "count-unique-characters-of-all-substrings-of-a-given-string": r"""
// Each character helps only the substrings that start after its previous occurrence
// and end before its next one.
int uniqueLetterString(const char *s) {
    int n = (int) strlen(s);
    long long total = 0;
    for (int i = 0; i < n; i++) {
        int previous = -1, next = n;
        for (int j = i - 1; j >= 0; j--) if (s[j] == s[i]) { previous = j; break; }
        for (int j = i + 1; j < n; j++) if (s[j] == s[i]) { next = j; break; }
        total += (long long) (i - previous) * (next - i);
    }
    return (int) total;
}   // O(n^2) time · O(1) space
""",
    "distinct-echo-substrings": r"""
// Compare every pair of equal-length halves and keep the distinct ones in a set.
int distinctEchoSubstrings(const char *text) {
    int n = (int) strlen(text);
    char **seen = malloc(sizeof(char *) * (size_t) (n * n + 1));
    int *seenLength = malloc(sizeof(int) * (size_t) (n * n + 1));
    int seenCount = 0, total = 0;
    for (int length = 1; length * 2 <= n; length++)
        for (int start = 0; start + 2 * length <= n; start++) {
            if (strncmp(text + start, text + start + length, (size_t) length)) continue;
            int duplicate = 0;
            for (int i = 0; i < seenCount && !duplicate; i++)
                if (seenLength[i] == length && !strncmp(seen[i], text + start, (size_t) length)) duplicate = 1;
            if (duplicate) continue;                       // this echo was counted already
            seen[seenCount] = malloc((size_t) length + 1);
            memcpy(seen[seenCount], text + start, (size_t) length);
            seen[seenCount][length] = '\0';
            seenLength[seenCount] = length;
            seenCount++;
            total++;
        }
    for (int i = 0; i < seenCount; i++) free(seen[i]);
    free(seen); free(seenLength);
    return total;
}   // O(n^3) time \u00b7 O(n^2) space
""",
    "word-break-ii": r"""
// Depth-first search that rebuilds every sentence, memoising failed suffixes.
static void build(const char *s, char **dict, int dictCount, char *current, int length,
                  char **out, int *count) {
    if (!*s) {
        out[*count] = strdup(current);                     // a complete sentence
        (*count)++;
        return;
    }
    for (int w = 0; w < dictCount; w++) {
        int len = (int) strlen(dict[w]);
        if (strncmp(s, dict[w], (size_t) len)) continue;
        int before = length;
        if (length) current[length++] = ' ';
        memcpy(current + length, dict[w], (size_t) len);
        length += len;
        current[length] = '\0';
        build(s + len, dict, dictCount, current, length, out, count);
        length = before;                                   // backtrack
        current[length] = '\0';
    }
}

char **wordBreakII(const char *s, char **wordDict, int dictCount, int *returnSize) {
    char **out = malloc(sizeof(char *) * 8192);
    char current[8192] = "";
    int count = 0;
    build(s, wordDict, dictCount, current, 0, out, &count);
    *returnSize = count;
    return out;
}   // O(2^n) worst case · O(n) recursion
""",
    "count-different-palindromic-subsequences": r"""
// dp[i][j] = number of distinct palindromic subsequences in s[i..j].
int countPalindromicSubsequences(const char *s) {
    const long long MOD = 1000000007;
    int n = (int) strlen(s);
    long long **dp = malloc(sizeof(long long *) * (size_t) (n + 1));
    for (int i = 0; i <= n; i++) dp[i] = calloc((size_t) n + 1, sizeof(long long));
    for (int i = 0; i < n; i++) dp[i][i] = 1;
    for (int width = 2; width <= n; width++)
        for (int i = 0; i + width - 1 < n; i++) {
            int j = i + width - 1;
            if (s[i] == s[j]) {
                int low = i + 1, high = j - 1;
                while (low <= high && s[low] != s[i]) low++;      // next same letter inside
                while (low <= high && s[high] != s[i]) high--;    // previous same letter inside
                if (low > high) dp[i][j] = (dp[i + 1][j - 1] * 2 + 2) % MOD;   // no repeats
                else if (low == high) dp[i][j] = (dp[i + 1][j - 1] * 2 + 1) % MOD;
                else dp[i][j] = (dp[i + 1][j - 1] * 2 - dp[low + 1][high - 1] % MOD + MOD) % MOD;
            } else {
                dp[i][j] = (dp[i + 1][j] + dp[i][j - 1] - dp[i + 1][j - 1] + MOD) % MOD;
            }
        }
    long long answer = dp[0][n - 1];
    for (int i = 0; i <= n; i++) free(dp[i]);
    free(dp);
    return (int) answer;
}   // O(n^2) time · O(n^2) space
""",
    "find-all-good-strings": r"""
// Digit DP over the two bounds with a KMP automaton for the forbidden pattern:
// answer = (strings <= s2) - (strings <= s1) + (s1 itself is good).
static int failure[64];

static void buildFailure(const char *evil) {
    int length = (int) strlen(evil);
    failure[0] = 0;
    for (int i = 1; i < length; i++) {
        int state = failure[i - 1];
        while (state && evil[i] != evil[state]) state = failure[state - 1];
        if (evil[i] == evil[state]) state++;
        failure[i] = state;
    }
}

// Move the automaton by one character; a result equal to the pattern length means a hit.
static int goState(int state, char letter, const char *evil, int length) {
    while (state && evil[state] != letter) state = failure[state - 1];
    if (evil[state] == letter) state++;
    return state;
}

static int avoids(const char *text, const char *evil) {     // does text contain evil?
    int length = (int) strlen(evil), state = 0;
    for (int i = 0; text[i]; i++) {
        state = goState(state, text[i], evil, length);
        if (state == length) return 0;
    }
    return 1;
}

static long long countUpTo(int n, int k, const char *limit, const char *evil) {
    const long long MOD = 1000000007;
    int length = (int) strlen(evil);
    long long *stateCount = calloc((size_t) length, sizeof(long long));   // already smaller
    stateCount[0] = 1;
    long long tightCount = 1;                              // equal to the limit so far
    int tightState = 0;
    for (int pos = 0; pos < n; pos++) {
        long long *next = calloc((size_t) length, sizeof(long long));
        for (int state = 0; state < length; state++) {
            if (!stateCount[state]) continue;
            for (int c = 0; c < k; c++) {
                int moved = goState(state, (char) ('a' + c), evil, length);
                if (moved < length) next[moved] = (next[moved] + stateCount[state]) % MOD;
            }
        }
        if (tightCount) {
            int highest = limit[pos] - 'a';
            for (int c = 0; c < highest && c < k; c++) {   // choosing less frees the rest
                int moved = goState(tightState, (char) ('a' + c), evil, length);
                if (moved < length) next[moved] = (next[moved] + 1) % MOD;
            }
            if (highest < k) {                             // still equal: carry the tight path
                int moved = goState(tightState, (char) ('a' + highest), evil, length);
                if (moved < length) tightState = moved;
                else tightCount = 0;
            } else tightCount = 0;
        }
        free(stateCount);
        stateCount = next;
    }
    long long total = tightCount;                          // the limit itself, if it stayed good
    for (int state = 0; state < length; state++) total = (total + stateCount[state]) % MOD;
    free(stateCount);
    return total;
}

int findGoodStrings(int n, const char *s1, const char *s2, const char *evil) {
    const long long MOD = 1000000007;
    buildFailure(evil);
    long long upToSecond = countUpTo(n, 26, s2, evil);
    long long upToFirst = countUpTo(n, 26, s1, evil);
    long long answer = (upToSecond - upToFirst + (avoids(s1, evil) ? 1 : 0)) % MOD;
    if (answer < 0) answer += MOD;
    return (int) answer;
}   // O(n * 26 * pattern) time \u00b7 O(pattern) space
""",
}
