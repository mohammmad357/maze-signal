"""Rebuild demo fixtures from Python, verify cost/path/expansions against C."""
from pathlib import Path
import json
import os
import random
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'python'))
from solver import parse, solve

def main():
    binary = ROOT / 'build' / ('solver.exe' if os.name == 'nt' else 'solver')
    texts = ['3 5\nS999G\n.###.\n.....\n', '1 3\nS#G\n', '1 2\nSG\n', '4 1\nS\n9\n.\nG\n', '2 2\r\nS.\r\n.G\r\n']
    rng = random.Random(357)
    for _ in range(500):
        h, w = rng.randrange(2, 8), rng.randrange(2, 8)
        cells = rng.choices('#..123789', k=h*w)
        s, g = rng.sample(range(h*w), 2)
        cells[s], cells[g] = 'S', 'G'
        texts.append(f'{h} {w}\n' + '\n'.join(''.join(cells[j:j+w]) for j in range(0, len(cells), w)) + '\n')
    fixtures = []
    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory) / 'map.txt'
        for i, text in enumerate(texts):
            rows, s, g = parse(text)
            temp.write_text(text, encoding='ascii', newline='')
            expected = {}
            for algorithm in ('dijkstra', 'astar'):
                py = solve(rows, s, g, algorithm)
                native = json.loads(subprocess.check_output([str(binary), str(temp), algorithm], text=True))
                for key in ('cost', 'path', 'expanded'):
                    if py[key] != native[key]:
                        raise RuntimeError(f'Native mismatch: map {i}, {algorithm}, {key}')
                expected[algorithm] = py
            fixtures.append({'name': f'fixed-{i}' if i < 5 else f'seed357-{i-5}', 'text': text, 'expected': expected})
    (ROOT / 'docs/fixtures.json').write_text(json.dumps(fixtures, separators=(',', ':')), encoding='utf-8')
    print('505 fixtures generated; 1010 Python/C comparisons passed.')

if __name__ == '__main__':
    main()
