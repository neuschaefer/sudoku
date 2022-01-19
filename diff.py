#!/usr/bin/python3
# SPDX-License-Identifier: 0BSD
from sudoku import *
import sys, os

if len(sys.argv) != 3:
    print("Usage diff.py a.txt b.txt")
    sys.exit(1)

a = Pattern(open(sys.argv[1], 'r').read())
b = Pattern(open(sys.argv[2], 'r').read())

print("Differences (in first, not in second):")
print(a.diff(b)[0].str_pretty())
print("Differences (in second, not in first):")
print(a.diff(b)[1].str_pretty())
