import numpy as np
import pandas as pd
import sys

class sudoku():
    def __init__(self):
        self.sudoku_array = [[1, 2, 3, 4, 5, 6, 7, 8, 9]]
        self.bkup_stack = list()
        self.verbose = 0
        self.index_value_stack = list()
        self.filled_cnt_val = 0
        self.exit_flag = 0
        self.row_excl = [[0],[0],[0],[0],[0],[0],[0],[0],[0]]
        self.col_excl = [[0],[0],[0],[0],[0],[0],[0],[0],[0]]
        self.box_excl = [[0],[0],[0],[0],[0],[0],[0],[0],[0]]

        for i in range(80):
            self.sudoku_array.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
    
    def print_sudoku(self):
        sudoku_pd = pd.DataFrame(columns = ('a','b','c','d','e','f','g','h','i')) 
        for i in range(9):
            sudoku_pd = sudoku_pd.append({"a":self.sudoku_array[(i*9)+0],
                                          "b":self.sudoku_array[(i*9)+1],
                                          "c":self.sudoku_array[(i*9)+2],
                                          "d":self.sudoku_array[(i*9)+3],
                                          "e":self.sudoku_array[(i*9)+4],
                                          "f":self.sudoku_array[(i*9)+5],
                                          "g":self.sudoku_array[(i*9)+6],
                                          "h":self.sudoku_array[(i*9)+7],
                                          "i":self.sudoku_array[(i*9)+8]},ignore_index=True)
        print(sudoku_pd)
    
    def row_excl_update(self):
        self.row_excl = [[0],[0],[0],[0],[0],[0],[0],[0],[0]]
        for i in range(0,80,9):
            k = i//9
            for j in range(i, i+9):
                if len(self.sudoku_array[j]) == 1:
                    self.row_excl[k] = self.row_excl[k] + self.sudoku_array[j]
        
    def col_excl_update(self):
        self.col_excl = [[0],[0],[0],[0],[0],[0],[0],[0],[0]]
        for i in range(9):
            k = i
            for j in range(i, 80, 9):
                if len(self.sudoku_array[j]) == 1:
                    self.col_excl[k] = self.col_excl[k] + self.sudoku_array[j]
    
    def box_excl_update(self):
        self.box_excl = [[0],[0],[0],[0],[0],[0],[0],[0],[0]]
        for i in range(81):
            k = ((i//3)//9)*3 + ((i//3)%3)
            if len(self.sudoku_array[i]) == 1:
                self.box_excl[k] = self.box_excl[k] + self.sudoku_array[i]
    
    def filled_cnt(self):
        self.filled_cnt_val = 0
        for i in range(81):
            if len(self.sudoku_array[i]) == 1:
                self.filled_cnt_val+=1
        return(self.filled_cnt_val)

    def soft_assignment(self):
        print("soft assignment starting...") if self.verbose == 1 else None
        self.bkup_stack.append(self.sudoku_array[:])
        print("copied dataset to bkup_stack") if self.verbose == 1 else None
        
        index_value = next(self.sudoku_array.index(x) for x in self.sudoku_array if len(x) > 1)
        self.sudoku_array[index_value] = [self.sudoku_array[index_value][0]]
        self.index_value_stack.append(index_value)
        
        print("element #",index_value," of the sudoku array is being assigned value:", self.sudoku_array[index_value]) if self.verbose == 1 else None
        print("updating row, col and box exclusion rules") if self.verbose == 1 else None
        self.row_excl_update()
        self.col_excl_update()
        self.box_excl_update()
        print("---soft assignment complete---") if self.verbose == 1 else None

    def cancel_assignment(self):
        if len(self.index_value_stack) > 0:
            print("issue encountered. running cancellation...") if self.verbose == 1 else None
            print("cancelling assignment at index ", self.index_value_stack[len(self.index_value_stack)-1]) if self.verbose == 1 else None
            self.sudoku_array.clear()
            self.sudoku_array = self.bkup_stack[len(self.bkup_stack)-1][:]
            self.sudoku_array[self.index_value_stack[len(self.index_value_stack)-1]] = self.sudoku_array[self.index_value_stack[len(self.index_value_stack)-1]][1:]
            self.bkup_stack.pop()
            self.index_value_stack.pop()
            print("---cancelling assignment complete---") if self.verbose == 1 else None
            
            print("updating row, col and box exclusion rules") if self.verbose == 1 else None
            self.row_excl_update()
            self.col_excl_update()
            self.box_excl_update()
            self.update_array()
        else:
            self.exit_flag = 1
            print("no assignment to cancel") if self.verbose == 1 else None

    def update_array(self):
        error_flag_duplicate_list = 0
        error_flag_zero_list = 0

        def issue_check():
            nonlocal error_flag_duplicate_list
            nonlocal error_flag_zero_list
            for i in range(9):
                if len([x for x in self.box_excl[i] if self.box_excl[i].count(x) > 1]) > 0: error_flag_duplicate_list+=1
                if len([x for x in self.box_excl[i] if self.row_excl[i].count(x) > 1]) > 0: error_flag_duplicate_list+=1
                if len([x for x in self.box_excl[i] if self.col_excl[i].count(x) > 1]) > 0: error_flag_duplicate_list+=1
                
            for i in range(81):
                if len(self.sudoku_array[i]) < 1: error_flag_zero_list+=1
    
            if error_flag_duplicate_list > 0:
                print("duplicate list error") if self.verbose == 1 else None
                
            if error_flag_zero_list > 0:
                print("zero list error") if self.verbose == 1 else None

        print("updating array based on latest assignments...") if self.verbose == 1 else None
        fc_s = 0
        fc_e = 1
        while (fc_s < fc_e):
            fc_s = self.filled_cnt()
            print("filled cells at start: ",self.filled_cnt()) if self.verbose == 1 else None
            for i in range(81):
                if len(self.sudoku_array[i]) > 1:
                    self.sudoku_array[i] = [x for x in self.sudoku_array[i] if x not in self.row_excl[i//9]] # row condition
                if len(self.sudoku_array[i]) > 1:
                    self.sudoku_array[i] = [x for x in self.sudoku_array[i] if x not in self.col_excl[i%9]] # col condition
                if len(self.sudoku_array[i]) > 1:
                    self.sudoku_array[i] = [x for x in self.sudoku_array[i] if x not in self.box_excl[((i//3)//9)*3 + ((i//3)%3)]]  # box condition
            print("filled cells at end: ",self.filled_cnt()) if self.verbose == 1 else None
            self.row_excl_update()
            self.col_excl_update()
            self.box_excl_update()
            issue_check()
            fc_e = self.filled_cnt()
            if (error_flag_duplicate_list + error_flag_zero_list) > 0:
                self.cancel_assignment()
                break
        self.print_sudoku() if self.verbose == 1 else None
        print("---array update complete---") if self.verbose == 1 else None
    
    def solve(self):
        self.soft_assignment()
        self.update_array()
        if self.filled_cnt_val == 81:
            self.print_sudoku()
        elif self.exit_flag == 1:
            print("unable to solve. check if initial values are right")
            sys.exit(0)
        else:
            self.solve()
