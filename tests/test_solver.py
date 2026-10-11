"""Differential checks against independent Bellman-Ford, plus CLI validation."""
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import parse, solve


def reference(rows, start, goal):
    cells = "".join(rows)
    width = len(rows[0])
    dist = [float("inf")] * len(cells)
    dist[start] = 0
    for _ in range(len(cells) - 1):
        changed = False
        for u, cell in enumerate(cells):
            if cell == "#":
                continue
            for v in range(len(cells)):
                if cells[v] == "#" or abs(u // width - v // width) + abs(u % width - v % width) != 1:
                    continue
                candidate = dist[u] + (int(cells[v]) if cells[v].isdigit() else 1)
                if candidate < dist[v]:
                    dist[v] = candidate
                    changed = True
        if not changed:
            break
    return None if dist[goal] == float("inf") else dist[goal]


class SearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.binary = Path(os.environ.get("SOLVER_C", str(ROOT / "build" / ("solver.exe" if os.name == "nt" else "solver"))))
        if not cls.binary.exists():
            raise RuntimeError("Compile c/solver.c into build/solver first")

    def check_map(self, text):
        rows, start, goal = parse(text)
        expected = reference(rows, start, goal)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "map.txt"
            path.write_text(text, encoding="ascii", newline="")
            for algorithm in ("dijkstra", "astar"):
                result = solve(rows, start, goal, algorithm)
                native = json.loads(subprocess.check_output([str(self.binary), str(path), algorithm], text=True))
                self.assertEqual(result["cost"], expected)
                for key in ("cost", "path", "expanded"):
                    self.assertEqual(result[key], native[key])
                route = result["path"]
                if expected is not None:
                    self.assertEqual((route[0], route[-1]), (start, goal))
                    total = 0
                    for u, v in zip(route, route[1:]):
                        self.assertEqual(abs(u // len(rows[0]) - v // len(rows[0])) + abs(u % len(rows[0]) - v % len(rows[0])), 1)
                        cell = rows[v // len(rows[0])][v % len(rows[0])]
                        self.assertNotEqual(cell, "#")
                        total += int(cell) if cell.isdigit() else 1
                    self.assertEqual(total, expected)

    def test_weighted_detour(self):
        self.check_map("3 5\nS999G\n.###.\n.....\n")

    def test_unreachable(self):
        self.check_map("1 3\nS#G\n")

    def test_adjacent(self):
        self.check_map("1 2\nSG\n")

    def test_single_column(self):
        self.check_map("4 1\nS\n9\n.\nG\n")

    def test_crlf(self):
        self.check_map("2 2\r\nS.\r\n.G\r\n")

    def test_seeded_random_maps(self):
        rng = random.Random(357)
        for case in range(500):
            h, w = rng.randrange(2, 8), rng.randrange(2, 8)
            cells = rng.choices("#..123789", k=h * w)
            start, goal = rng.sample(range(h * w), 2)
            cells[start], cells[goal] = "S", "G"
            text = f"{h} {w}\n" + "\n".join("".join(cells[i:i+w]) for i in range(0, len(cells), w)) + "\n"
            with self.subTest(case=case):
                self.check_map(text)

    def test_invalid_maps(self):
        texts = ["", "0 1\n", "1+2\nSG\n", "1 2\nSS\n", "1 3\nS0G\n", "2 2\nSG\n", "1 2\nSGx\n", "1 2\nSG\nextra\n", "99999999999999 2\nSG\n"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.txt"
            for text in texts:
                with self.subTest(text=text):
                    with self.assertRaises(ValueError):
                        parse(text)
                    path.write_text(text, encoding="ascii")
                    process = subprocess.run([str(self.binary), str(path), "astar"], capture_output=True)
                    self.assertNotEqual(process.returncode, 0)


if __name__ == "__main__":
    unittest.main()
