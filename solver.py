import numpy as np
import pandas as pd

sudoku_array = [[1, 2, 3, 4, 5, 6, 7, 8, 9]]
for i in range(80):
    sudoku_array.append([1, 2, 3, 4, 5, 6, 7, 8, 9])

bkup_stack = list()
index_value_stack = list()

# functions for updating the sudoku array
def row_excl_update():
    global row_excl
    row_excl = [[0],[0],[0],[0],[0],[0],[0],[0],[0]]
    for i in range(0,80,9):
        k = i//9
        for j in range(i, i+9):
            if len(sudoku_array[j]) == 1:
                row_excl[k] = row_excl[k] + sudoku_array[j]
    return(row_excl)

def row_condn(i):
    sudoku_array[i] = [x for x in sudoku_array[i] if x not in row_excl[i//9]]

def col_excl_update():
    global col_excl
    col_excl = [[0],[0],[0],[0],[0],[0],[0],[0],[0]]
    for i in range(9):
        k = i
        for j in range(i, 80, 9):
            if len(sudoku_array[j]) == 1:
                col_excl[k] = col_excl[k] + sudoku_array[j]
    return(col_excl)

def col_condn(i):
    sudoku_array[i] = [x for x in sudoku_array[i] if x not in col_excl[i%9]]

def box_excl_update():
    global box_excl
    box_excl = [[0],[0],[0],[0],[0],[0],[0],[0],[0]]
    for i in range(81):
        k = ((i//3)//9)*3 + ((i//3)%3)
        if len(sudoku_array[i]) == 1:
            box_excl[k] = box_excl[k] + sudoku_array[i]
    return(box_excl)

def box_condn(i):
    sudoku_array[i] = [x for x in sudoku_array[i] if x not in box_excl[((i//3)//9)*3 + ((i//3)%3)]]

def issue_check():
    global error_flag_duplicate_list
    global error_flag_zero_list
    error_flag_duplicate_list = 0
    error_flag_zero_list = 0
    
    for i in range(9):
        if len([x for x in box_excl[i] if box_excl[i].count(x) > 1]) > 0: error_flag_duplicate_list+=1
        if len([x for x in box_excl[i] if row_excl[i].count(x) > 1]) > 0: error_flag_duplicate_list+=1
        if len([x for x in box_excl[i] if col_excl[i].count(x) > 1]) > 0: error_flag_duplicate_list+=1
    
    for i in range(81):
        if len(sudoku_array[i]) < 1: error_flag_zero_list+=1
    
    if error_flag_duplicate_list > 0:
        print("duplicate list error")

    if error_flag_zero_list > 0:
        print("zero list error")

def filled_cnt():
    global filled_cnt_val
    filled_cnt_val = 0
    for i in range(81):
        if len(sudoku_array[i]) == 1:
            filled_cnt_val+=1
    return(filled_cnt_val)

def print_sudoku():
    sudoku_pd = pd.DataFrame(columns = ('a','b','c','d','e','f','g','h','i')) 
    
    for i in range(9):
        sudoku_pd = sudoku_pd.append({"a":sudoku_array[(i*9)+0],
                                      "b":sudoku_array[(i*9)+1],
                                      "c":sudoku_array[(i*9)+2],
                                      "d":sudoku_array[(i*9)+3],
                                      "e":sudoku_array[(i*9)+4],
                                      "f":sudoku_array[(i*9)+5],
                                      "g":sudoku_array[(i*9)+6],
                                      "h":sudoku_array[(i*9)+7],
                                      "i":sudoku_array[(i*9)+8]},ignore_index=True)
    
    return(sudoku_pd)

def re_evaluation():
    print("filled cells at start: ",filled_cnt())
    for i in range(81):
        if len(sudoku_array[i]) > 1: row_condn(i)
        if len(sudoku_array[i]) > 1: col_condn(i)
        if len(sudoku_array[i]) > 1: box_condn(i)
    print("filled cells at end: ",filled_cnt())
    row_excl_update()
    col_excl_update()
    box_excl_update()
    issue_check()

def soft_assignment():
    print("soft assignment starting...")
    bkup_stack.append(sudoku_array[:])
    print("copied dataset to bkup_stack")
    
    global index_value
    index_value = next(sudoku_array.index(x) for x in sudoku_array if len(x) > 1)
    sudoku_array[index_value] = [sudoku_array[index_value][0]]
    index_value_stack.append(index_value)
    
    print("element #",index_value," of the sudoku array is being assigned value:", sudoku_array[index_value])
    print("updating row, col and box exclusion rules")
    row_excl_update()
    col_excl_update()
    box_excl_update()
    print("---soft assignment complete---")

def update_array():
    print("updating array based on latest assignments...")
    fc_s = 0
    fc_e = 1
    while (fc_s < fc_e):
        fc_s = filled_cnt()
        re_evaluation()
        fc_e = filled_cnt()
        if (error_flag_duplicate_list + error_flag_zero_list) > 0:
            cancel_assignment()
            break
    print(print_sudoku())
    print("---array update complete---")

def cancel_assignment():
    global sudoku_array
    print("issue encountered. running cancellation...")
    print("cancelling assignment at index ", index_value_stack[len(index_value_stack)-1])
    sudoku_array.clear()
    sudoku_array = bkup_stack[len(bkup_stack)-1][:]
    sudoku_array[index_value_stack[len(index_value_stack)-1]] = sudoku_array[index_value_stack[len(index_value_stack)-1]][1:]
    bkup_stack.pop()
    index_value_stack.pop()
    print("---cancelling assignment complete---")
    
    print("updating row, col and box exclusion rules")
    row_excl_update()
    col_excl_update()
    box_excl_update()
    update_array()

def recursive_eval():
    soft_assignment()
    
    update_array()
    
    if filled_cnt_val == 81:
        return(print(print_sudoku()))
    
    else:
        recursive_eval()

# PROBLEM STATEMENT
# difficulty level: Hard
sudoku_array[4] = [9]
sudoku_array[6] = [3]
sudoku_array[10] = [4]
sudoku_array[11] = [9]
sudoku_array[15] = [7]
sudoku_array[19] = [5]
sudoku_array[20] = [6]
sudoku_array[30] = [6]
sudoku_array[32] = [8]
sudoku_array[40] = [3]
sudoku_array[41] = [2]
sudoku_array[46] = [8]
sudoku_array[48] = [9]
sudoku_array[49] = [1]
sudoku_array[51] = [2]
sudoku_array[53] = [4]
sudoku_array[55] = [9]
sudoku_array[59] = [4]
sudoku_array[60] = [1]
sudoku_array[62] = [2]
sudoku_array[65] = [4]
sudoku_array[69] = [5]
sudoku_array[71] = [8]
sudoku_array[76] = [6]
sudoku_array[80] = [9]

# SOLUTION
update_array()
recursive_eval()