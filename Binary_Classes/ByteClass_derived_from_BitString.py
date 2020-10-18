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
        elif(type(I) is str and len(I)==2):  # for Hex byte input - such as '4F'
            N = Byte._hexToNum(I)
            super().__init__(N)
        # elif(I==0):
        #     super().__init__([False]*Eight)
        # elif(I==1):
        #     super().__init__([True]*Eight)
        else:
            super().__init__(I)
        self._lengthCheck()
        self._lockObject()
        
# This method sets the Locked property to True. 
# Check the __setattr__ method (also __delattr__) to see how this works.        
# It prevents editing of all class attributes.
    def _lockObject(self):
        self.Locked = True

# TODO: Bug - cannot assign new attributes to an existing byte object.
    def __setattr__(self, nm, vl):
        if(hasattr(self, 'Locked') and self.Locked):
            if(nm in ['Locked', 'numDigs', 'vals', '__setattr__', '__dict__']):
                # Can't change Locked, otherwise yo can change that first and then change anything else.
                # Can't set numDigs or vals
                # Can't change __setattr__, otherwise you could change that first and then change anything else.
                # Can't change __dict__, otherwise you could change the entire set of attributes/vals.
                raise TypeError("Cannot edit read-only attribute '"+nm+"' of Byte object.") from None
            else:
                super().__setattr__(nm, vl)
        else:
            super().__setattr__(nm, vl)
        
    def __getattribute__(self, name):
        # if(name in ['vals'])
        if(name=='vals'):
            ret = super().__getattribute__(name)
            return ret.copy()
        elif(name=='__dict__'):
            # User shouldn't be abl modify __dict__ directly to make his changes to attributes
            # __dict__ is modified before returning: a copy of dict is returned and all mutables in dict.values() are also copied.
            print('WARNING: __dict__ has been accessed')
            mutables = ['vals']
            # immutables = ['numDigs', 'Locked']
            ret = super().__getattribute__(name)
            ret = ret.copy()
            for m in mutables:
                if(m in ret.keys()):
                    ret[m] = ret[m].copy()
            return ret
        else:
            return super().__getattribute__(name)
            
    def __delattr__(self, nm):
        if(hasattr(self, 'Locked') and self.Locked):
            if(nm in ['Locked', 'numDigs', 'vals', '__setattr__']):
                raise TypeError("Cannot delete read-only attribute '"+nm+"' of Byte object.") from None
        else:
            super().__delattr__(nm)
            
    # This doesn't work            
    # def _unlockObject(self):
    #     self.__setattr__ = super().__setattr__
        
    def _lengthCheck(self):
        if(self.numDigs > Eight):
            print("Length of Byte can't be ", self.numDigs, ". SET_TO_ZERO")
            self.__init__([False]*Eight)
        elif(self.numDigs < Eight):
            self.vals = ([False] * (Eight-self.numDigs))+ self.vals
            self.numDigs = Eight
    
    def disp(self, Format='hex'):
        if(Format=='hex'):
            return Byte._numToHex(int(self))
        elif(Format=='dec'):
            return str(int(self))
        else:
            return super().disp(Format)
            
    def _numToHex(N):
        a = N//16
        b = N%16
        ret = ''.join([ (chr(55+a) if (a>=10) else chr(48+a)),     (chr(55+b) if (b>=10) else chr(48+b)) ])
        return ret
    
    # Input 's' is a string of length 2, such as '0F' or '2C'
    def _hexToNum(s):
        possibles = '0 1 2 3 4 5 6 7 8 9 A B C D E F'.split()
        # if(not (s[0] in possibles and s[1] in possibles) ):
        try:
            ret = possibles.index(s[0])
            ret = ret*16 + possibles.index(s[1])
            return ret
        except ValueError:
            raise TypeError('Input '+s+' cannot be interpreted as a hexadecimal value.')
        
        
        
#   Idea behind this algorithm :-
#        To take 2's complement of a bitstring, invert all the bits to the left of the rightmost '1'
    def twosComp(self):
        v = self.vals[:]
        invertFlag=False
        for i in range(-1, -(len(v)+1), -1):
            if(invertFlag):
                v[i] = (not v[i])            
            if(v[i]):
                invertFlag=True

        return Byte(v)
                
            
    def inc(self):
        v = self.vals[:]
        for i in range(-1, -(len(v)+1), -1):
            v[i] = (not v[i])
            if(v[i]):
                break
        return Byte(v)
        
    
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
        return float(self.__int__())
    
    
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
    
    def __invert__(self):
        return Byte([not v for v in self.vals])
    
    # Defines how to interpret someSeq[self] (i.e. Byte object passed as an index)
    # Returns the integer representation of the Byte.
    # Enbales usage of hex(self), bin(self) and oct(self). They all use this Magic method.
    def __index__(self):
        return self.__int__()
    
    def __getitem__(self, key):
        try:
            key = int(key)
        except ValueError:
            raise TypeError("Unsupported type "+str(type(key))+" for indexing into Byte") from None
        if(key not in range(Eight)):
            raise IndexError('Byte object has indices 0-7 only, not '+str(key)+'.') from None
        else:
            return self.vals[Eight-1-key]
    
    def __setitem__(self, pos, val):
        raise TypeError('Cannot change individual bits in a Byte object')
    
    
    def __str__(self):
        return self.disp(Format='hex')
    
    def __repr__(self):
        return 'Byte('+self.disp(Format='hex')+')'