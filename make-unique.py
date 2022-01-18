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
        print('Puzzle is NOT unique. Unique pattern:')
        pat = s.make_unique(pat)
        pat.show()
        s.set_pattern(pat)
    print("Solution:")
    s.solution().show()
else:
    print('Puzzle is NOT solvable')
