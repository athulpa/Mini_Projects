
from sudoku4 import Sudoku4

sud = Sudoku4()


def valid(sud):
    for i in range(4):
        for num in range(1, 5):
            if((sud[i, :]==num).sum()>1):
                return False
            if((sud[:, i]==num).sum()>1):
                return False
    for i in range(4):
        for num in range(1, 5):
            if((sud[(i//2)*2:(i//2)*2+2, (i%2)*2:(i%2)*2+2]==num).sum()>1):
                return False
#    print(True)
    return True
    
def solve(pos):
    if(pos==16):
        print('Complete')
        return True
    
    i = pos//4
    j = pos%4
    
    for num in range(1, 5):
        sud.values[i, j] = num
        if(valid(sud.values) == True):
#            print(pos+1)
#            sud.disp()
            retval = solve(pos+1)
            if(retval==False):
                continue
            else:
                return True
#        else:
#            print(num, 'is invalid')
    sud.values[i, j]=0
#    print('latest was zeroed')
#    sud.disp()
    return False
        
