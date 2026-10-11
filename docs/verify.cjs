'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {parse, solve} = require('./solver.js');
const fixtures = JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures.json'), 'utf8'));
let comparisons = 0;
for (const f of fixtures) for (const a of ['dijkstra', 'astar']) {
  const result = solve(parse(f.text), a);
  assert.deepEqual(result, f.expected[a], `${f.name}/${a}`); comparisons++;
}
for (const text of ['', '0 2\nSG\n', '1 2\nSS\n', '1 3\nS0G\n', '2 2\nSG\n', '1 2\nSGx\n', '1 2\nSG\nextra\n', '41 1\nSG\n']) assert.throws(() => parse(text));
const adjacent = parse('1 2\nSG\n');
assert.throws(() => solve({...adjacent, goal: adjacent.start}, 'astar'));
assert.throws(() => solve(adjacent, 'unknown'));
const rows = Array.from({length:40}, () => '.'.repeat(40)); rows[0]='S'+'.'.repeat(39); rows[39]='.'.repeat(39)+'G';
assert.equal(solve(parse('40 40\n'+rows.join('\n')), 'astar').cost, 78);
console.log(JSON.stringify({maps:fixtures.length, algorithm_comparisons:comparisons, invalid_inputs:8, overlap_rejected:true, maximum_demo_grid_cost:78, status:'PASS'}));
