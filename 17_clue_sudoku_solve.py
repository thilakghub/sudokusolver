#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 15:31:13 2020

@author: z001t72
"""

import multiprocessing
import time
import sys
from solver import sudoku

sys.setrecursionlimit(100000)

f = open('/Users/z001t72/Documents/Training/Sudoku/all_17_clue_sudokus.txt', 'r')
content = f.readlines()
f.close()

def sev_clue(x):
    arr = sudoku()

    for j in range(len(x)-1):
        if int(x[j]) != 0: arr.sudoku_array[j] = [int(x[j])]
    
    arr.verbose = 0
    arr.row_excl_update()
    arr.col_excl_update()
    arr.box_excl_update()
    arr.solve()

start_time= time.time()
pool = multiprocessing.Pool()
outputs_1 = pool.map_async(sev_clue, content[0:10])
outputs_1.get()
print(round((time.time() - start_time),2),"seconds")
print(outputs_1.get())