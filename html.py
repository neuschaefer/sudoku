#!/usr/bin/python3
# SPDX-License-Identifier: 0BSD
# Shoutouts to OpenStark on Stackoverflow:
# https://stackoverflow.com/questions/23497444/how-to-make-a-sudoku-grid-using-html-and-css#23497700

from sudoku import *
import datetime

s = Sudoku()
s.add_sudoku_constraints()
pat = s.make_unique(Pattern())
print("""
<html>
<head><title>Sudoku</title></head>
<body>
<style>
    body { margin-top: 5em; }
    table { border-collapse: collapse; font-family: sans-serif; margin: auto; font-size: 200%%; }
    colgroup, tbody { border: solid; }
    td { border: solid thin; height: 1.4em; width: 1.4em; text-align: center; padding: 0; }
</style>
<table>
    <caption>Sudoku (%s)</caption>
    <colgroup><col><col><col>
    <colgroup><col><col><col>
    <colgroup><col><col><col>
""" % datetime.date.today().strftime('%F'))
for y in DIG:
    if y in [1,4,7]:
        print('    <tbody>')
    l = '    <tr> '
    for x in DIG:
        l += '<td>'
        if pat.v[x,y]:
            l += str(pat.v[x,y])
    print(l)
print("""
</table>
</body>
</html>
""")
