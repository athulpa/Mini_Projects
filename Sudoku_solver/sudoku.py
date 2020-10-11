# SUGGESTED WORKFLOW
# Initialize s = Sudoku()
# Use s.from_user() to enter Today's sudoku
# Recommended to Save it using s.from_npy ( load using s.from_npy or s = Sudoku(fname='myile') )
# Run sovler_naiveRec (or any other solver module) and then use solve(s) to solve the Sudoku.

import numpy as np

class Sudoku:
    # If a file name is given, the values of the object are loaded from numpy array.
    # If file name is none, then the values of object are all 0's.
    def __init__(self, fname=None):
        if(fname is None):
            self.values = np.zeros((9, 9), dtype=np.int8)
        else:
            self.from_npy(fname, False)
    
    def getbox(self, index, giveOnlyIndices=False):
        idx0 = index[0]//3
        idx1 = index[1]//3
        if(giveOnlyIndices is False):
            return self.values[idx0:idx0+3, idx1:idx1+3]
        else:
            return idx0, idx1

# If 'emptychar' is None, displays the values of the sudoku stylishly with 0 meaning empty.
# If 'emptychar' is given some value, empty values are filled with 'emptychar' and then the sudoku is displayed.
    def disp(self, emptychar=None):
        if(emptychar is None):
            print('| --------------------------- |')
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        print('|', self.values[3*i+j, 3*k:3*k+3], end=' ')
                    print('|')
                print('| --------------------------- |')
        else:
            showarr = np.array(self.values, dtype=np.str)
            showarr[self.values==0] = emptychar
            print('| ------------------------ |')
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        print('|', end=' ')
                        for l in range(3):
                            print(showarr[3*i+j, 3*k+l], end=' ')
                        print(' ', end='')
#                        print('|', self.values[3*i+j, 3*k:3*k+3], end=' ')
                    print('|')
                print('| ------------------------ |')
    
    # Takes input from user and makes a sudoku of it.
    # Input should be given such that it can be passed into eval, i.e. type a list or tuple as you
    # would on the console with () or [].
    def from_user(self):
        print('Enter the Sudoku below as a 9x9 matrix, in row-major form')
        biglist = [ ]
        for i in range(9):
            biglist.append(eval(input()))
            print(biglist[-1], type(biglist[-1]))
            
        print(biglist)
        self.values = np.asarray(biglist)
        print('You have Entered:')
        self.disp()
        
# Saves the sudoku values to 'fname' as a numpy array.
    def from_npy(self, fname, verbose=True):
        self.values = np.load(fname, allow_pickle=False)
        if(verbose is True):
            print('Sudoku has been loaded')
            self.display()
# Loads the numpy array in 'fname' as the values of the sudoku.    
    def to_npy(self, fname):
        np.save(fname, self.values, allow_pickle=False)
        print('Sudoku has been saved')

#################################################################################################
#################################################################################################
