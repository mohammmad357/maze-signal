/* UI state is separate from pure search. All map edits cancel prior animation. */
'use strict';
const $ = id => document.getElementById(id);
const examples = {
  trap: '3 5\nS999G\n.###.\n.....\n',
  open: '10 14\nS.............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n..............\n.............G\n',
  blocked: '3 5\nS.#.G\n..#..\n..#..\n'
};
let map, results = null, shown = {dijkstra: 0, astar: 0}, running = false, paused = false, timer = null, generation = 0, paint = null;
const algorithms = ['dijkstra', 'astar'];
const focused = {dijkstra: 0, astar: 0};
function rememberFocus(algorithm, i) {
  const grid = $('grid-' + algorithm);
  focused[algorithm] = i;
  Array.from(grid.children).forEach((b, index) => {b.tabIndex = index === i ? 0 : -1;});
}
function updateTool() {
  const weighted = $('tool').value === 'weight';
  $('weight').disabled = !weighted;
  $('tool-help').textContent = weighted ? 'Terrain weight: select 1–9, then paint a non-endpoint cell.' : 'Weight applies only to Terrain weight. Select Start or Goal to move endpoints.';
}
function stop() {generation++; clearTimeout(timer); timer = null; running = false; paused = false; $('pause').disabled = true; $('pause').textContent = 'Pause';}
function invalidate(message) {stop(); results = null; shown = {dijkstra: 0, astar: 0}; render(); $('status').textContent = message;}
function labelCell(i, algorithm) {
  const c = map.cells[i], state = c === 'S' ? 'start' : c === 'G' ? 'goal' : c === '#' ? 'wall' : `entry cost ${c === '.' ? 1 : c}`;
  const r = results && results[algorithm], done = r && shown[algorithm] >= r.visited.length;
  const route = done && r.path.includes(i), explored = r && r.visited.slice(0, shown[algorithm]).includes(i);
  return `Row ${Math.floor(i / map.width) + 1}, column ${i % map.width + 1}, ${state}${route ? ', final route' : explored ? ', explored' : ''}`;
}
function renderGrid(algorithm, rebuild) {
  const grid = $('grid-' + algorithm); grid.style.gridTemplateColumns = `repeat(${map.width}, minmax(0, 1fr))`;
  if (rebuild || grid.children.length !== map.cells.length) {
    grid.replaceChildren();
    for (let i = 0; i < map.cells.length; i++) {const b = document.createElement('button'); b.type = 'button'; b.dataset.index = String(i); b.className = 'cell'; grid.append(b);}
  }
  const result = results && results[algorithm], visited = new Set(result ? result.visited.slice(0, shown[algorithm]) : []), complete = result && shown[algorithm] >= result.visited.length, path = new Set(complete ? result.path : []);
  for (let i = 0; i < map.cells.length; i++) {
    const b = grid.children[i], c = map.cells[i];
    b.className = 'cell' + (c === '#' ? ' wall' : /^[1-9]$/.test(c) ? ' terrain' : '') + (visited.has(i) ? ' visited' : '') + (path.has(i) ? ' path' : '') + (c === 'S' ? ' start' : c === 'G' ? ' goal' : '');
    b.textContent = c !== '.' ? c : path.has(i) ? '•' : visited.has(i) ? '·' : '';
    b.setAttribute('aria-label', labelCell(i, algorithm)); b.tabIndex = i === focused[algorithm] ? 0 : -1;
  }
  const values = complete ? [result.cost === null ? 'No route' : result.cost, result.cost === null ? '—' : result.path.length - 1, result.expanded] : ['—', '—', '—'];
  $('metrics-' + algorithm).querySelectorAll('b').forEach((b, i) => {b.textContent = String(values[i]);});
}
function render(rebuild = false) {
  algorithms.forEach(a => renderGrid(a, rebuild));
  const rows = [];
  for (let r = 0; r < map.height; r++) rows.push(map.cells.slice(r * map.width, (r + 1) * map.width).join(''));
  $('map-text').value = `${map.height} ${map.width}\n${rows.join('\n')}\n`;
}
function loadExample() {stop(); focused.dijkstra = focused.astar = 0; map = MazeSearch.parse(examples[$('example').value]); results = null; shown = {dijkstra: 0, astar: 0}; render(true); $('status').textContent = 'Ready. Paint a cell or run the comparison.';}
function edit(i, mode = $('tool').value) {
  if (!Number.isInteger(i) || i < 0 || i >= map.cells.length) return;
  if ((mode === 'start' && i === map.goal) || (mode === 'goal' && i === map.start)) { $('status').textContent = 'Start and goal must be on different cells.'; return; }
  if (mode === 'start' || mode === 'goal') {const old = mode === 'start' ? map.start : map.goal; map.cells[old] = '.'; map.cells[i] = mode === 'start' ? 'S' : 'G'; map[mode] = i;}
  else {
    if (i === map.start || i === map.goal) {$('status').textContent = 'Endpoints stay traversable. Use Start or Goal to move them.'; return;}
    map.cells[i] = mode === 'wall' ? '#' : mode === 'erase' ? '.' : $('weight').value;
  }
  invalidate('Map changed. Previous results cleared; run again to compare.');
}
function finishText() {
  const d = results.dijkstra, a = results.astar;
  $('status').textContent = d.cost === null ? 'No route. Both algorithms exhausted the reachable area.' : `Same optimal cost: ${d.cost}. Dijkstra expanded ${d.expanded} cells; A* expanded ${a.expanded}.`;
}
function tick(token) {
  if (token !== generation || !running || paused) return;
  const speed = Number($('speed').value), batch = speed === 0 ? map.cells.length : speed <= 5 ? 4 : 1;
  algorithms.forEach(a => {shown[a] = Math.min(results[a].visited.length, shown[a] + batch);}); render();
  if (algorithms.every(a => shown[a] >= results[a].visited.length)) {running = false; $('pause').disabled = true; $('pause').textContent = 'Pause'; finishText();}
  else timer = setTimeout(() => tick(token), speed);
}
$('run').addEventListener('click', () => {stop(); results = {dijkstra: MazeSearch.solve(map, 'dijkstra'), astar: MazeSearch.solve(map, 'astar')}; shown = {dijkstra: 0, astar: 0}; running = true; $('pause').disabled = false; $('status').textContent = 'Exploring the same map. Animation speed does not measure search performance.'; tick(generation);});
$('pause').addEventListener('click', () => {if (!running) return; paused = !paused; $('pause').textContent = paused ? 'Resume' : 'Pause'; $('status').textContent = paused ? 'Paused. Resume or edit the map to cancel.' : 'Exploring…'; if (paused) clearTimeout(timer); else tick(generation);});
$('reset').addEventListener('click', loadExample);
$('example').addEventListener('change', loadExample);
$('clear').addEventListener('click', () => {map.cells = map.cells.map(c => c === 'S' || c === 'G' ? c : '.'); invalidate('Walls and terrain cleared. Endpoints kept.');});
algorithms.forEach(a => {
  const grid = $('grid-' + a);
  grid.addEventListener('focusin', e => {const b = e.target.closest('button.cell'); if (b) rememberFocus(a, Number(b.dataset.index));});
  grid.addEventListener('click', e => {const cell = e.target.closest('button.cell'); if (cell) edit(Number(cell.dataset.index));});
  grid.addEventListener('pointerdown', e => {const b = e.target.closest('button.cell'); if (b && ['wall', 'erase', 'weight'].includes($('tool').value)) {paint = {id: e.pointerId, mode: $('tool').value, last: Number(b.dataset.index), moved: false};}});
  grid.addEventListener('pointermove', e => {if (!paint || paint.id !== e.pointerId || !e.buttons) return; const b = document.elementFromPoint(e.clientX, e.clientY)?.closest('button.cell'); if (b && b.closest('.grid') === grid) {const i = Number(b.dataset.index); if (i !== paint.last) {if (!paint.moved) edit(paint.last, paint.mode); paint.moved = true; paint.last = i; edit(i, paint.mode);}}});
  grid.addEventListener('keydown', e => {const b = e.target.closest('button.cell'); if (!b) return; const i = Number(b.dataset.index), r = Math.floor(i / map.width), c = i % map.width; let n = i; if (e.key === 'ArrowLeft' && c) n--; else if (e.key === 'ArrowRight' && c < map.width - 1) n++; else if (e.key === 'ArrowUp' && r) n -= map.width; else if (e.key === 'ArrowDown' && r < map.height - 1) n += map.width; else if (!e.key.startsWith('Arrow')) return; e.preventDefault(); grid.children[n].focus();});
});
window.addEventListener('pointerup', () => {paint = null;});
window.addEventListener('pointercancel', () => {paint = null;});
$('tool').addEventListener('change', updateTool);
// Respect the OS preference only on first load; the user can still choose a speed.
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) $('speed').value = '0';
updateTool();
loadExample();
