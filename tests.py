#!/usr/bin/python3
# SPDX-License-Identifier: 0BSD
# run with:
#
#   pytest-3 tests.py
#
from sudoku import *
import unittest

###
###  PATTERN PARSING AND PRINTING
###

PATSTR_EXAMPLE = """\
   3 . 2  . 8 .  . 7 .
   . . .  . . .  4 . 8
   7 . .  4 6 1  2 . .

   4 6 .  . . .  . . .
   . . .  . . .  . . 3
   . . 9  . . 6  8 2 4

   . . 7  . 4 .  . . .
   8 . .  2 1 .  6 . .
   . . 4  . 7 3  . . 5"""
PAT_EXAMPLE = Pattern(PATSTR_EXAMPLE)

PAT_UNSAT = Pattern(PAT_EXAMPLE)
PAT_UNSAT.set(3,3,3)

PAT_UNDERCONSTRAINED = Pattern(PAT_EXAMPLE)
PAT_UNDERCONSTRAINED.clear(3,1)

SOL_EXAMPLE = Solution("""
.-------.-------.-------.
| 3 4 2 | 9 8 5 | 1 7 6 |
| 9 1 6 | 3 2 7 | 4 5 8 |
| 7 5 8 | 4 6 1 | 2 3 9 |
.-------.-------.-------.
| 4 6 3 | 8 5 2 | 7 9 1 |
| 2 8 1 | 7 9 4 | 5 6 3 |
| 5 7 9 | 1 3 6 | 8 2 4 |
.-------.-------.-------.
| 6 9 7 | 5 4 8 | 3 1 2 |
| 8 3 5 | 2 1 9 | 6 4 7 |
| 1 2 4 | 6 7 3 | 9 8 5 |
.-------.-------.-------.
""")

def test_pattern_str_parse():
    p = Pattern(PATSTR_EXAMPLE)
    assert str(p) == PATSTR_EXAMPLE

SOL_BORDERS = """
.-------.-------.-------.
| 3 4 2 | 5 8 9 | 1 7 6 |
| 9 1 6 | 7 3 2 | 4 5 8 |
| 7 8 5 | 4 6 1 | 2 3 9 |
.-------.-------.-------.
| 4 6 8 | 3 5 7 | 9 2 1 |
| 2 7 1 | 8 9 4 | 5 6 3 |
| 5 3 9 | 1 2 6 | 7 8 4 |
.-------.-------.-------.
| 1 5 7 | 6 4 8 | 3 9 2 |
| 8 9 3 | 2 1 5 | 6 4 7 |
| 6 2 4 | 9 7 3 | 8 1 5 |
.-------.-------.-------.
"""
SOL_NORMAL = """
3 4 2   5 8 9   1 7 6
9 1 6   7 3 2   4 5 8
7 8 5   4 6 1   2 3 9

4 6 8   3 5 7   9 2 1
2 7 1   8 9 4   5 6 3
5 3 9   1 2 6   7 8 4

1 5 7   6 4 8   3 9 2
8 9 3   2 1 5   6 4 7
6 2 4   9 7 3   8 1 5
"""
SOL_DENSE = """
342589176
916732458
785461239
468357921
271894563
539126784
157648392
893215647
624973815
"""

def test_parse_pattern_with_borders():
    p1 = Pattern(SOL_NORMAL)
    p2 = Pattern(SOL_BORDERS)
    for x,y in all_idx():
        assert p1.v[x,y] == p2.v[x,y]

def test_parse_dense_pattern():
    p1 = Pattern(SOL_NORMAL)
    p2 = Pattern(SOL_DENSE)
    for x,y in all_idx():
        assert p1.v[x,y] == p2.v[x,y]


###
###  SOLVING
###

def test_solve_unique():
    s = Sudoku()
    s.add_sudoku_constraints()
    s.set_pattern(PAT_EXAMPLE)
    assert s.sat()
    assert s.unique()
    sol = s.solution()
    for x,y in all_idx():
        assert sol.v[x,y] == SOL_EXAMPLE.v[x,y]
    assert s.solution() == Solution(SOL_EXAMPLE)

def test_unsat():
    s = Sudoku()
    s.add_sudoku_constraints()
    s.set_pattern(PAT_UNSAT)
    assert not s.sat()

def test_not_unique():
    s = Sudoku()
    s.add_sudoku_constraints()
    s.set_pattern(PAT_UNDERCONSTRAINED)
    assert s.sat()
    assert not s.unique()
