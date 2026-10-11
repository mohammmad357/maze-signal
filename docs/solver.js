(function (root) {
  'use strict';
  function parse(text) {
    const lines = text.trimEnd().split(/\r?\n/);
    const dims = (lines.shift() || '').trim().split(/\s+/);
    if (dims.length !== 2 || dims.some(x => !/^\d+$/.test(x))) throw new Error('Expected height width.');
    const [height, width] = dims.map(Number);
    if (height < 1 || width < 1 || height > 40 || width > 40) throw new Error('Demo grids must be 1–40 rows and columns.');
    if (lines.length !== height || lines.some(r => r.length !== width)) throw new Error('Map dimensions do not match.');
    const cells = lines.join('').split('');
    if (cells.some(c => !'#.SG123456789'.includes(c))) throw new Error('Allowed cells: # . S G and 1–9.');
    if (cells.filter(c => c === 'S').length !== 1 || cells.filter(c => c === 'G').length !== 1) throw new Error('Place one distinct start and goal.');
    return {height, width, cells, start: cells.indexOf('S'), goal: cells.indexOf('G')};
  }
  class Heap {
    constructor() { this.items = []; }
    before(a, b) { return a[0] < b[0] || (a[0] === b[0] && (a[1] < b[1] || (a[1] === b[1] && a[2] < b[2]))); }
    push(x) {
      const a = this.items; a.push(x); let i = a.length - 1;
      while (i) {const p = (i - 1) >> 1; if (!this.before(a[i], a[p])) break; [a[i], a[p]] = [a[p], a[i]]; i = p;}
    }
    pop() {
      const a = this.items, top = a[0], end = a.pop();
      if (a.length) {a[0] = end; let i = 0;
        for (;;) {let j = i, l = 2 * i + 1, r = l + 1; if (l < a.length && this.before(a[l], a[j])) j = l; if (r < a.length && this.before(a[r], a[j])) j = r; if (j === i) break; [a[i], a[j]] = [a[j], a[i]]; i = j;}
      }
      return top;
    }
  }
  function solve(map, algorithm) {
    if (!['astar', 'dijkstra'].includes(algorithm)) throw new Error('Unknown algorithm.');
    const {height, width, cells, start, goal} = map;
    if (start === goal || cells[start] !== 'S' || cells[goal] !== 'G') throw new Error('Start and goal must be distinct.');
    const dist = Array(cells.length).fill(Infinity), parent = Array(cells.length).fill(-1), closed = new Set(), visited = [], heap = new Heap();
    const h = n => algorithm === 'astar' ? Math.abs(Math.floor(n / width) - Math.floor(goal / width)) + Math.abs(n % width - goal % width) : 0;
    dist[start] = 0; heap.push([h(start), 0, start]);
    while (heap.items.length) {
      const [, neg, u] = heap.pop(), cost = -neg;
      if (closed.has(u) || cost !== dist[u]) continue;
      closed.add(u); visited.push(u);
      if (u === goal) {
        const path = [goal]; while (path[path.length - 1] !== start) path.push(parent[path[path.length - 1]]);
        return {cost, expanded: visited.length, path: path.reverse(), visited};
      }
      const row = Math.floor(u / width), col = u % width;
      for (const [dr, dc] of [[-1, 0], [0, -1], [0, 1], [1, 0]]) {
        const nr = row + dr, nc = col + dc;
        if (nr < 0 || nr >= height || nc < 0 || nc >= width) continue;
        const v = nr * width + nc, cell = cells[v]; if (cell === '#') continue;
        const candidate = cost + (/^[1-9]$/.test(cell) ? Number(cell) : 1);
        if (candidate < dist[v]) {dist[v] = candidate; parent[v] = u; heap.push([candidate + h(v), -candidate, v]);}
      }
    }
    return {cost: null, expanded: visited.length, path: [], visited};
  }
  const api = {parse, solve};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.MazeSearch = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
