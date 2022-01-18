#!/usr/bin/python3
# SPDX-License-Identifier: 0BSD
from sudoku import *
import sys

s = Sudoku()
s.add_sudoku_constraints()
pat = Pattern(sys.stdin.read())
s.set_pattern(pat)
if s.sat():
    if s.unique():
        print('Puzzle is unique')
    else:
        print('Puzzle is NOT unique')
    s.print_all_solutions()
else:
    print('Puzzle is NOT solvable')
