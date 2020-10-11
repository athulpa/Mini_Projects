

import numpy as np

class Sudoku4:
    # If a file name is given, the values of the object are loaded from numpy array.
    # If file name is none, then the values of object are all 0's.
    def __init__(self, fname=None):
        if(fname is None):
            self.values = np.zeros((4, 4), dtype=np.int8)
        else:
            self.from_npy(fname, False)
    
    def getbox(self, index, giveOnlyIndices=False):
        idx0 = index[0]//2
        idx1 = index[1]//2
        if(giveOnlyIndices is False):
            return self.values[idx0:idx0+2, idx1:idx1+2]
        else:
            return idx0, idx1

# If 'emptychar' is None, displays the values of the sudoku stylishly with 0 meaning empty.
# If 'emptychar' is given some value, empty values are filled with 'emptychar' and then the sudoku is displayed.
    def disp(self, emptychar=None):
        if(emptychar is None):
            print('| ------------- |')
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        print('|', self.values[2*i+j, 2*k:2*k+2], end=' ')
                    print('|')
                print('| ------------- |')
        else:
            showarr = np.array(self.values, dtype=np.str)
            showarr[self.values==0] = emptychar
            print('| ------------------------ |')
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        print('|', end=' ')
                        for l in range(2):
                            print(showarr[2*i+j, 2*k+l], end=' ')
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
        for i in range(4):
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
