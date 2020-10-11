
from sudoku import Sudoku
from time import time

sud = Sudoku('sudoku2_hard.npy')

# sud is a numpy array (i.e. values only)
# Checks if all numbers 1..9 are present in every row, col and box.
def complete(sud):
    for i in range(9):
        for num in range(1, 10):
            if(num not in sud[i, :]):
#                print(num, 'not in row', i+1)
                return False
            if(num not in sud[:, i]):
#                print(num, 'not in col', i+1)
                return False
            if(num not in sud[(i//3)*3:(i//3)*3+3, (i%3)*3:(i%3)*3+3]):
#                print(num, 'not in box', i+1)
                return False
    return True

# Checks if any number 1..9 is repeating in any row, col or box.
# Returns False if repetitions are found.
def valid(sud):
    for i in range(9):
        for num in range(1, 10):
            if((sud[i, :]==num).sum()>1):
                return False
            if((sud[:, i]==num).sum()>1):
                return False
    for i in range(9):
        for num in range(1, 10):
            if((sud[(i//3)*3:(i//3)*3+3, (i%3)*3:(i%3)*3+3]==num).sum()>1):
                return False
#    print(True)
    return True

# A recursive function that inserts values at pos and calls itself with pos+1.    
def recfn(sud, pos, fixed):
#    print('called', pos+1)
    if(pos==81):
        print('Complete')
        sud.disp()
#        resp = input('Conitnue? ')
#        if(resp.lower() in ['y', 'yes']):
#            return False
#        else:
#            return True
        return True
    
    i = pos//9
    j = pos%9
    
    if(fixed[i, j]==True):
#        print(i, j, 'is fixed.')
        return recfn(sud, pos+1, fixed)    
    for num in range(1, 10):
        sud.values[i, j] = num
        if(valid(sud.values) == True):
#            sud.disp()
            retval = recfn(sud, pos+1, fixed)
            if(retval==False):
                continue
            else:
#                print('returning true')
                return True
    sud.values[i, j]=0
    return False

# Solves the sudoku by initiating the recursion with recfn. Also prints time taken.
def solve(sud):
    fixed = (sud.values!=0)
    start = time()
    recfn(sud, pos=0, fixed=fixed)
    end = time()
    print('Completed:', complete(sud.values))
    print(round(end-start, 2), 'seconds.')

