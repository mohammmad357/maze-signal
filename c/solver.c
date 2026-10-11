/* C11 optimal grid search. Heap order: (f, -g, node), matching Python. */
#include <ctype.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct { int f, g, node; } Entry;
typedef struct { Entry *items; size_t size, capacity; } Heap;
static void fail(const char *message) { fprintf(stderr, "%s\n", message); exit(2); }
static void *allocate(size_t size) { void *p = malloc(size); if (!p) fail("out of memory"); return p; }
static int less(Entry a, Entry b) {
    if (a.f != b.f) return a.f < b.f;
    if (a.g != b.g) return a.g > b.g;
    return a.node < b.node;
}
static void push(Heap *heap, Entry value) {
    if (heap->size == heap->capacity) {
        size_t capacity = heap->capacity ? heap->capacity * 2 : 256;
        Entry *items = realloc(heap->items, capacity * sizeof *items);
        if (!items) fail("out of memory");
        heap->items = items; heap->capacity = capacity;
    }
    size_t i = heap->size++;
    while (i && less(value, heap->items[(i - 1) / 2])) {
        heap->items[i] = heap->items[(i - 1) / 2]; i = (i - 1) / 2;
    }
    heap->items[i] = value;
}
static Entry pop(Heap *heap) {
    Entry result = heap->items[0], value = heap->items[--heap->size];
    size_t i = 0;
    while (2 * i + 1 < heap->size) {
        size_t child = 2 * i + 1;
        if (child + 1 < heap->size && less(heap->items[child + 1], heap->items[child])) ++child;
        if (!less(heap->items[child], value)) break;
        heap->items[i] = heap->items[child]; i = child;
    }
    if (heap->size) heap->items[i] = value;
    return result;
}
static int heuristic(int node, int goal, int width, int astar) {
    return astar ? abs(node / width - goal / width) + abs(node % width - goal % width) : 0;
}
static int search(const char *cells, int height, int width, int start, int goal, int astar,
                  int *parent, int *expanded) {
    int size = height * width;
    int *dist = allocate((size_t)size * sizeof *dist);
    unsigned char *closed = allocate((size_t)size);
    memset(closed, 0, (size_t)size);
    for (int i = 0; i < size; ++i) { dist[i] = INT_MAX; parent[i] = -1; }
    Heap heap = {0}; int answer = -1; *expanded = 0; dist[start] = 0;
    push(&heap, (Entry){heuristic(start, goal, width, astar), 0, start});
    while (heap.size) {
        Entry e = pop(&heap); int u = e.node;
        if (closed[u] || e.g != dist[u]) continue;
        closed[u] = 1; ++*expanded;
        if (u == goal) { answer = e.g; break; }
        const int dr[4] = {-1, 0, 0, 1}, dc[4] = {0, -1, 1, 0};
        for (int k = 0; k < 4; ++k) {
            int r = u / width + dr[k], c = u % width + dc[k];
            if (r < 0 || c < 0 || r >= height || c >= width) continue;
            int v = r * width + c;
            if (cells[v] == '#') continue;
            int cost = cells[v] >= '1' && cells[v] <= '9' ? cells[v] - '0' : 1;
            int candidate = e.g + cost;
            if (candidate < dist[v]) {
                dist[v] = candidate; parent[v] = u;
                push(&heap, (Entry){candidate + heuristic(v, goal, width, astar), candidate, v});
            }
        }
    }
    free(heap.items); free(closed); free(dist); return answer;
}
int main(int argc, char **argv) {
    if (argc < 3 || argc > 4) fail("usage: solver MAP astar|dijkstra [REPEAT]");
    int astar = !strcmp(argv[2], "astar");
    if (!astar && strcmp(argv[2], "dijkstra")) fail("unknown algorithm");
    long repeat = 1;
    if (argc == 4) {
        char *end; repeat = strtol(argv[3], &end, 10);
        if (*end || repeat < 1 || repeat > 10000) fail("repeat must be in 1..10000");
    }
    FILE *file = fopen(argv[1], "rb"); if (!file) fail("cannot open map");
    /* Bounded whole-file read keeps malformed headers away from scanf integer overflow. */
    size_t limit = 2 * 1024 * 1024;
    char *text = allocate(limit + 1);
    size_t length = fread(text, 1, limit, file);
    if (ferror(file) || !feof(file)) fail("map too large or unreadable");
    fclose(file); text[length] = '\0';
    if (strlen(text) != length) fail("NUL bytes are not allowed");
    char *cursor = text, *end;
    long h = strtol(cursor, &end, 10); if (end == cursor || h < 1 || h > 1024) fail("invalid height");
    cursor = end;
    if (*cursor != ' ' && *cursor != '\t') fail("dimensions need a separator");
    long w = strtol(cursor, &end, 10);
    if (end == cursor || w < 1 || w > 1024) fail("invalid width");
    cursor = end;
    while (*cursor == ' ' || *cursor == '\t') ++cursor;
    if (*cursor == '\r') ++cursor;
    if (*cursor++ != '\n') fail("invalid header");
    int height = (int)h, width = (int)w, size = height * width, start = -1, goal = -1;
    char *cells = allocate((size_t)size);
    for (int r = 0; r < height; ++r) {
        for (int c = 0; c < width; ++c) {
            char cell = *cursor; if (!cell || !strchr("#.SG123456789", cell)) fail("invalid cell or row width");
            ++cursor; int i = r * width + c; cells[i] = cell;
            if (cell == 'S') { if (start != -1) fail("duplicate S"); start = i; }
            if (cell == 'G') { if (goal != -1) fail("duplicate G"); goal = i; }
        }
        if (*cursor == '\r') ++cursor;
        if (*cursor == '\n') ++cursor;
        else if (r != height - 1 || *cursor) fail("invalid row width");
    }
    if (*cursor || start == -1 || goal == -1) fail("extra data or missing S/G");
    free(text);
    int *parent = allocate((size_t)size * sizeof *parent), expanded = 0, answer = -1;
    clock_t begin = clock();
    for (long i = 0; i < repeat; ++i) answer = search(cells, height, width, start, goal, astar, parent, &expanded);
    double seconds = (double)(clock() - begin) / CLOCKS_PER_SEC / (double)repeat;
    if (answer < 0) printf("{\"cost\":null,\"expanded\":%d,\"seconds\":%.9f,\"path\":[] }\n", expanded, seconds);
    else {
        int *path = allocate((size_t)size * sizeof *path), count = 0;
        for (int v = goal; v != -1; v = parent[v]) path[count++] = v;
        printf("{\"cost\":%d,\"expanded\":%d,\"seconds\":%.9f,\"path\":[", answer, expanded, seconds);
        for (int i = count - 1; i >= 0; --i) printf("%s%d", i == count - 1 ? "" : ",", path[i]);
        puts("]}"); free(path);
    }
    free(parent); free(cells); return 0;
}
