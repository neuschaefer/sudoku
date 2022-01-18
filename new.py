#!/usr/bin/python3
# SPDX-License-Identifier: 0BSD
from sudoku import *

s = Sudoku()
s.add_sudoku_constraints()
pat = s.make_unique(Pattern())
print("Puzzle:")
print(pat.str_pretty())
s.set_pattern(pat)
print("Solution:")
s.solution().show()
