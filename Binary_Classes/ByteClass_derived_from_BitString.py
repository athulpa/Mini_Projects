from BinaryStringClass import BitString

Eight = int( 8 )

class Byte(BitString):
    def __init__(self, I=None):
        # super().__init__(self)
        # print(hasattr(self, 'vals'))    
        if(I is None):
            super().__init__([False]*Eight)
        elif(type(I) is Byte):
            self.vals = I.vals[:]
            self.numDigs = I.numDigs
        elif(I==0):
            super().__init__([False]*Eight)
        elif(I==1):
            super().__init__([True]*Eight)
        else:
            super().__init__(I)
        self.lengthCheck()
        
    def lengthCheck(self):
        if(self.numDigs > Eight):
            print("Length of Byte can't be ", self.numDigs, ". SET_TO_ZERO")
            self.__init__([False]*Eight)
        elif(self.numDigs < Eight):
            self.vals = ([False] * (Eight-self.numDigs))+ self.vals
            self.numDigs = Eight
    
    def disp(self, Format='hex'):
        if(Format=='hex'):
            return Byte.numToHex(int(self))
        elif(Format=='dec'):
            return str(int(self))
        else:
            return super().disp(Format)
            
    def numToHex(N):
        a = N//16
        b = N%16
        ret = ''.join([ (chr(55+a) if (a>=10) else chr(48+a)),     (chr(55+b) if (b>=10) else chr(48+b)) ])
        return ret
    
    def twosComp(self):
        pass        
    
    def __eq__(self, other):
        assert hasattr(self, 'vals')
        assert hasattr(other, 'vals')
        return (self.vals == other.vals)
        
    def __int__(self):
        n=0
        for v in self.vals:
            n *= 2
            n += (1 if v else 0)
        return n
    
    def __float__(self):
        return self.__int__()
    
    
# A funciton to add two bytes.
# Implements rollover of bytes if range gets exceeded.
# Returns Carry and Overflow if required (ask for these vals with retCarry and retOverflow inputs)    
    def adder(A, B, retCarry=False, retOverFlow=False):
        assert type(A) is Byte
        assert type(B) is Byte
        s = int(A)
        o = int(B)
        R = Byte((s+o)%256)
        C = (s+o)>256
        OF = ( A.vals[0] and B.vals[0] and not R.vals[0] )  or  (not A.vals[0] and not B.vals[0] and R.vals[0])
        if(not retCarry and not retOverFlow):
            return R
        ret = (R,)
        if(retCarry):
            ret += (C,)
        if(retOverFlow):
            ret += (OF,)
        return ret
    
        
    def __add__(self, other):
        return self.adder(other,False,False)
        
    def multiplier(self, other, retCarry, retOverFlow):
        pass
        
    def __addi__(self, other):
        r = self.adder(other,False,False)
        self.__init__(r)
    
    def __bool__(self):
        return (True in self.vals)
    
    def __mul__(self, other):
        return NotImplemented
    
    def __imul__(self, other):
        return NotImplemented
    
    __rmul__ = __mul__
    
    def __and__(self, other):
        if (len(other.vals)!=Eight):
            return NotImplemented('Both operands need to be bytes of length 8.')
        return Byte([(i and j) for i,j in zip(self.vals, other.vals)])
    
    def __or__(self, other):
        if (len(other.vals)!=Eight):
            return NotImplemented('Both operands need to be bytes of length 8.')
        return Byte([(i or j) for i,j in zip(self.vals, other.vals)])
    
    def __xor__(self, other):
        if (len(other.vals)!=Eight):
            return NotImplemented('Both operands need to be bytes of length 8.')
        return Byte(   ((i or j) and not (i and j))    for i,j in zip(self.vals, other.vals))
    
    def __inverse__(self):
        self.vals = [not v for v in self.vals]
    
    # Defines how to interpret someSeq[self].
    # Returns the integer representation of the Byte.
    # Enbales usage of hex(self), bin(self) and oct(self). They all use this Magic method.
    def __index__(self):
        return self.__int__()
    
    def __getitem__(self, key):
        try:
            return self.vals[key]
        except IndexError:
            raise IndexError('Byte object has indices 1-7 only') from None
    
    def __setitem__(self, pos, val):
        raise NotImplementedError('Cannot change individual bits in a Byte object')
    
    def __str__(self):
        return self.disp(Format='hex')
    
    def __repr__(self):
        return 'Byte('+self.disp(Format='hex')+')'