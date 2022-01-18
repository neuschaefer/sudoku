#!/usr/bin/python3
# SPDX-License-Identifier: 0BSD
from sudoku import *

s = Sudoku()
s.add_sudoku_constraints()
# diagonals
s.add_different([(i,i) for i in DIG])
s.add_different([(10-i,i) for i in DIG])
pat = Pattern("""
  . 1 .  3 . 5  . 2 .
  . . .  . 1 .  . . 5
  . 4 .  8 2 7  . 1 .

  4 9 .  7 . 8  . . .
  . 8 .  . 3 2  . . 7
  . . .  . . .  3 8 4

  . 3 .  . . .  . . 6
  . 5 .  . . 3  2 4 8
  . 6 8  . . .  7 3 .
  """)
s.set_pattern(pat)
if s.unique():
    print('Puzzle is unique')
else:
    print('Puzzle is NOT unique')
    pat = s.make_unique(pat)
    pat.show()
    s.set_pattern(pat)
s.print_all_solutions()
