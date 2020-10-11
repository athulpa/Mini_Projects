
import numpy as np

# Initializes 'pos' and 'fixed' based on the values in 'sud'.
# (pos is False'd for every fixed value)
def start(sud):
    pos = np.zeros((9,9,9), dtype=np.bool)
    pos[:]=True
    fixed = (sud.values!=0)
    for i in range(9):
        for j in range(9):
            if(fixed[i, j] == True):
                pos[i, j, :]=False
                pos[i, j, sud.values[i, j]-1]=True
    return pos, fixed

# Wherever a value is fixed, that value is removed from the pos of that row, column and box.
def upd_pos(sud, pos, fixed):
    for i in range(9):
        for j in range(9):
            if(fixed[i, j]==True):
                pos[i, :, sud.values[i, j]-1]=False
                pos[:, j, sud.values[i, j]-1]=False
                pos[(i//3)*3:(i//3)*3+3, (j//3)*3:(j//3)*3+3, sud.values[i, j]-1]=False
                pos[i, j, sud.values[i, j]-1]=True

# If pos is only once True at any place, then that place's value is fixed.
def upd_fixed(sud, pos, fixed):
    count = 0
    for i in range(9):
        for j in range(9):
            if(np.count_nonzero(pos[i, j])==0):
                print("ERROR FOR ", i, 'th row, ', j, 'th column', sep='')
            elif(fixed[i, j]==False):
#                print(np.count_nonzero(pos[i, j]))
                if(np.count_nonzero(pos[i, j])==1):
                    sud.values[i, j] = np.argmax(pos[i, j])+1
                    fixed[i, j]=True
                    count+=1
                    print(i+1, 'th row, ', j+1, 'th column has been fixed', sep='')
    print('fixed', count, 'values')
                
# Tests if a number is possible in only one location or not in a row/column/box.
# If so, that number is placed there and 'fixed' and sud.values is updated.
# Searches for every number in every row, column, box.
def find_val(sud, pos, fixed):
    for i in range(9):
        for num in range(9):
            if(num+1 not in sud.values[i, :]):
                if(np.count_nonzero(pos[i, :, num])==1):
                    print('\n',pos[i, :, num])
                    print(i+1, 'th row: number ', num+1, ' at ', sep='', end='')
                    fixed[i, np.argmax(pos[i,:,num])] = True
                    sud.values[i, np.argmax(pos[i,:,num])] = num+1
                    print(np.argmax(pos[i,:,num])+1, 'th position', sep='')
            
            if(num+1 not in sud.values[:, i]):
                if(np.count_nonzero(pos[:, i, num])==1):
                    print()
                    print(sud.values[:, i])
                    print(pos[:, i, num])
                    print(i+1, 'th column: number ', num+1, ' at ', sep='', end='')
                    fixed[np.argmax(pos[:,i,num]), i] = True
                    sud.values[np.argmax(pos[:,i,num]), i] = num+1
                    print(np.argmax(pos[:,i,num])+1, 'th position', sep='')
                    
            if(num+1 not in sud.values[(i//3)*3:(i//3)*3+3, (i%3)*3:(i%3)*3+3]):
                if(np.count_nonzero(pos[(i//3)*3:(i//3)*3+3, (i%3)*3:(i%3)*3+3, num])==1):
                    print('\n', pos[(i//3)*3:(i//3)*3+3, (i%3)*3:(i%3)*3+3, num])
                    print(i+1, 'th box: number ', num+1, ' at ', sep='', end='')
                    idx = np.argmax(pos[(i//3)*3:(i//3)*3+3, (i%3)*3:(i%3)*3+3, num])
                    print(idx+1, 'th position', sep='')
                    idx0 = idx//3
                    idx1 = idx % 3
                    fixed[(i//3)*3 + idx0, (i%3)*3 + idx1] = True
                    sud.values[(i//3)*3 + idx0, (i%3)*3 + idx1] = num+1
def fixed2(sud, pos, fixed):
    pass