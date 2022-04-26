from munkres import Munkres, print_matrix, DISALLOWED, make_cost_matrix
import numpy as np

class TaskAssignment:

    def __init__(self, task_matrix, mode, wait):
        self.task_matrix = task_matrix
        self.mode = mode
        self.wait = wait
        self.maxsize = 99999999
        if mode == 'Hungary_min':
            self.min_cost, self.best_min_solution = self.Hungary_min(task_matrix)
        if mode == 'Hungary_max':
            self.max_cost, self.best_max_solution = self.Hungary_max(task_matrix)
    
    def Hungary_min(self, task_matrix):  

        m = Munkres()
        indexes = m.compute(task_matrix)
        print_matrix(task_matrix, msg='Lowest cost through this matrix:')
        total = 0
        best_count = []
        for row, column in indexes:
            value = task_matrix[row][column]
            total += value
            print(f'({row}, {column}) -> {value}')
            best_count.append(value)
            
        print(f'total cost: {total}')

        min_cost = total
        best_min_solution = best_count

        if self.wait == 'soon': 
            print("soon")

            task_matrix[row].pop(column) 
            task_matrix[row].insert(column, DISALLOWED)
            
            m = Munkres()
            indexes = m.compute(task_matrix)
            print_matrix(task_matrix, msg='Lowest cost through this matrix:')
            total = 0
            best_count = []
            value = 0
            for row, column in indexes:
                value = task_matrix[row][column]
                total += value
                print(f'({row}, {column}) -> {value}')
                best_count.append(value)
            print(f'total cost: {total}')

            min_cost = total
            best_min_solution = best_count    

        return min_cost, best_min_solution

    def Hungary_max(self, task_matrix):
        
        cost_matrix = make_cost_matrix(task_matrix, lambda cost: (float(self.maxsize) - cost) if
                                      (cost != DISALLOWED) else DISALLOWED)
        m = Munkres()

        indexes = m.compute(cost_matrix)
        print_matrix(task_matrix, msg='Highest profit through this matrix:')
        total = 0
        best_count = []
        for row, column in indexes:
            value = task_matrix[row][column]
            total += value
            print(f'({row}, {column}) -> {value}')
            best_count.append(value)
        print(f'total profit={total}')
        max_cost = total
        best_max_solution = best_count

        if self.wait == 'not soon': 
            print("not soon")

            task_matrix[row].pop(column) 
            task_matrix[row].insert(column, DISALLOWED)

            cost_matrix = make_cost_matrix(task_matrix, lambda cost: (float(self.maxsize) - cost) if
                                      (cost != DISALLOWED) else DISALLOWED)
            m = Munkres()

            indexes = m.compute(cost_matrix)
            print_matrix(task_matrix, msg='Highest profit through this matrix:')
            total = 0
            best_count = []
            for row, column in indexes:
                value = task_matrix[row][column]
                total += value
                print(f'({row}, {column}) -> {value}')
                best_count.append(value)
            print(f'total profit={total}')
            max_cost = total
            best_max_solution = best_count
        return max_cost, best_max_solution