#!/usr/bin/python3
# SPDX-License-Identifier: 0BSD
from sudoku import *
import sys

pat = Pattern(sys.stdin.read())
print(pat.str_secuso())
