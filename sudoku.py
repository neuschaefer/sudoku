#!/usr/bin/python3
# SPDX-License-Identifier: 0BSD

from z3 import Int, Solver, Or, And, Not, CheckSatResult
import random, os

random.seed(os.urandom(16))

# digits
DIG = range(1, 10)

def shuffled(l):
    l = list(l)
    random.shuffle(l)
    return l

def all_idx():
    for y in DIG:
        for x in DIG:
            yield x,y

def box_offsets():
    for y in range(3):
        for x in range(3):
            yield x,y

class Pattern:
    def __init__(self, text=''):
        self.v = {}
        for x,y in all_idx(): self.v[x,y] = None

        if isinstance(text, Pattern):
            for x,y in all_idx(): self.v[x,y] = text.v[x,y]
            return

        y = 1
        for line in text.splitlines():
            line = line.strip()
            if line == '' or '-' in line:
                continue
            x = 1
            for v in line:
                if v == '.' or v in [str(i) for i in DIG]:
                    if v == '.':
                        self.v[x,y] = None
                    else:
                        self.v[x,y] = int(v)
                    x += 1
            y += 1

    def set(self, x,y,v):
        self.v[x,y] = v

    def clear(self, x,y):
        self.v[x,y] = None

    def str_raw(self):
        ll = []
        for y in DIG:
            if y in [4, 7]:
                ll.append('')
            l = '  '
            for x in DIG:
                if x in [4, 7]:
                    l += ' '
                l += ' ' + (str(self.v[x,y]) if self.v[x,y] else '.')
            ll.append(l)
        return '\n'.join(ll)

    def __str__(self):
        return self.str_raw()

    def show(self):
        print(self)

    def str_pretty(self):
        LINE = ".-------.-------.-------."
        ll = []
        for y in range(1, 10):
            if y in [1, 4, 7]:
                ll.append(LINE)
            l = '|'
            for x in DIG:
                if x in [4, 7]:
                    l += ' |'
                l += ' ' + (str(self.v[x,y]) if self.v[x,y] else '.')
            l += ' |'
            ll.append(l)
        ll.append(LINE)
        return '\n'.join(ll)

    def str_secuso(self):
        digits = ''
        for x,y in all_idx():
            v = self.v[x,y]
            digits += str(v) if v else '0'
        return 'https://sudoku.secuso.org/' + digits

    def __eq__(self, other):
        return all([self.v[x,y] == other.v[x,y] for x,y in all_idx()])

    def diff(self, other):
        p1 = Pattern()
        p2 = Pattern()
        for x,y in all_idx():
            if self.v[x,y] != other.v[x,y]:
                p1.set(x,y, self.v[x,y])
                p2.set(x,y, other.v[x,y])
        return p1, p2

class Solution(Pattern):
    def from_model(model, sudoku):
        sol = Solution()
        for x,y in all_idx():
            sol.v[x,y] = model.eval(sudoku.v[x,y]).as_long()
        return sol

    def __str__(self):
        return self.str_pretty()

class Sudoku:
    def __init__(self, name='s'):
        self.name = name
        self.v = {} # values
        self.s = Solver()

        for x,y in all_idx():
            self.v[x,y] = Int(f'{name}{x}{y}')

    def add_different(self, idx):
        vv = [self.v[x,y] for x,y in idx]
        for i in range(len(vv)):
            for j in range(i + 1, len(vv)):
                self.s.add(vv[i] != vv[j])

    def add_sudoku_constraints(self):
        for x,y in all_idx():
            self.s.add(Or([self.v[x,y] == i for i in DIG]))

        # row and column constraints
        for y in DIG: self.add_different([(x,y) for x in DIG])
        for x in DIG: self.add_different([(x,y) for y in DIG])

        # box constraints
        for y0 in range(1,10,3):
            for x0 in range(1,10,3):
                self.add_different([(x0+x, y0+y) for x,y in box_offsets()])

    def set(self, x, y, value):
        self.s.add(self.v[x,y] == value)

    def set_pattern(self, pattern):
        if isinstance(pattern, str):
            pattern = Pattern(pattern)
        for x,y in all_idx():
            if pattern.v[x,y]:
                self.set(x,y, pattern.v[x,y])

    def solution(self):
        assert self.sat()
        return Solution.from_model(self.s.model(), self)

    def print_all_solutions(self):
        self.s.push()
        while self.sat():
            sol = self.solution()
            print("Solution:")
            sol.show()
            self.deny_solution(sol)
        self.s.pop()

    def all_solutions(self):
        sols = []
        self.s.push()
        while s.sat():
            sol = s.solution()
            sols.append(sol)
            s.deny_solution(sol)
        self.s.pop()
        return sols

    def two_solutions(self):
        assert self.sat()
        one = self.solution()
        self.s.push()
        self.deny_solution(one)
        assert self.sat()
        two = self.solution()
        self.s.pop()
        return one, two

    def unique(self):
        if not self.sat():
            return False
        m = self.solution()
        self.s.push()
        self.deny_solution(m)
        second = self.sat()
        self.s.pop()
        return not second

    def sat(self):
        return repr(self.s.check()) == 'sat'

    def deny_solution(self, sol):
        constraints = [self.v[x,y] == sol.v[x,y] for x,y in all_idx()]
        self.s.add(Not(And(constraints)))

    # Add constraints to disambiguate the pattern
    def make_unique(self, pat):
        assert self.sat()
        self.s.push()
        self.set_pattern(pat)
        pat = Pattern(pat)
        while not self.unique():
            # Take the difference between the first two solutions, and try to
            # learn something from it
            s1, s2 = self.two_solutions()
            p = random.choice(s1.diff(s2))
            for x,y in shuffled(all_idx()):
                v = p.v[x,y]
                if v:
                    self.set(x,y,v)
                    pat.set(x,y,v)
                    break
        self.s.pop()
        return pat
