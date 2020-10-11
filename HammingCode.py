# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 15:06:34 2020

@author: athul
"""

# 16-bit hamming code.
# Parity is always EVEN.
# 'b' is an object of class 'BIN' (source code below)
# If b is shorter than 16 bits, 'PaddingVal' is repeatedly padded to the ...
#           front of the bitstring
def h(b, PaddingVal='False'):
    N = 16 # Number of bits
    n = 4  # log(N)
    HCode = b.vals
    if(b.numDigs > 11):
        print("Cannot create 16-bit Hamming Code for a bitstream longer than 11 bits.")
        return BIN(b.vals)
    if(b.numDigs < 11):
        HCode = [False] * (11-b.numDigs) + HCode
        
    HCode.insert(0, False)        
    for i in range(n):
        HCode.insert(2**i, False)
    print(HCode)
    
    remVal = 1
    for i in range(n):
        ParityBit = False    # Starts as False. Inverts for every (included-in-selection) bit that is True.
        IsIncluded = False
        for i in range(1,N):
            if(i % remVal==0):
                IsIncluded =  not IsIncluded
            if(IsIncluded and HCode[i]) :
                ParityBit = not ParityBit
        HCode[remVal] = ParityBit
        remVal = remVal*2
    return BIN(HCode)
    
# Returns true if parity is even for the specified selection of bitstring 'b'
# The selection is done by concatenating every alternate group of 'N' consecutive digits, ...
#       ... starting with a skipped group
# Specify 'N' as a power of 2. Also, 0 < N <= (b.numDigs/2)
def calcParity(b, N=1):
    retVal = False
    idx = 0
    while(idx < b.numDigs):
        idx += N
        for i in range(N):
            if(b.vals[idx]):
                retVal = not retVal
            idx += 1
    return (not retVal)         # Need to return True if parity is even.

# Returns the index where error has occurred.
# b is a BIN object and b.numDigs is assumed to be a power of 2.
# Returning '0' from this function is famously ambiguous:-
#           Either there's an error at 0 or there's no error in the bitstring.
#           There's no way to identify error at pos=0 using Hamming code.
def findErrSingle(b):
    retIdx=0
    N=1
    while(N<b.numDigs):
        if(not calcParity(b, N)):
            retIdx += N
        N *= 2
    return retIdx    

class BIN:
    def __init__(self, Input=None):
        if(Input is None):
            self.vals = [False]
        elif(type(Input) is BIN):          # Copy Con'r
            self.vals[:] = Input.vals[:]
        elif(hasattr(Input, 'vals')):
            self.vals[:] = Input.vals[:]
        elif(Input==0):
            self.vals = [False]
        elif(Input==1):
            self.vals = [True]
        # Now 'Input' has to be an iterable
        # The following body catches iterables of string/int/float/boolean
        else:
            self.vals = []
            for i in Input:
                bl = True if int(i) else False
                self.vals.append(bl)
        self.numDigs = len(self.vals)
        
    def disp(self, Type='BitString'):
        if(Type=='BitString'):
            s = ['1' if val else '0' for val in self.vals]
            s = ''.join(s)      # ['1','1','0'] --> '110'
            return s
    
    def eval(self, Order='forward'):
        if(Order=='reversed'):
            N = 0
            L = len(self.vals)
            for i in range(L):
                N = N*2 + (1 if self.vals[L-1-i] else 0)
            return N
        # Any other value of 'Order' is treated as 'forward'.
        else:
            N = 0
            for val in self.vals:
                N = N*2 + (1 if val else 0)
            return N
                
    def flip(b, pos):
        b.vals[pos] = (False if b.vals[pos] else True)
    