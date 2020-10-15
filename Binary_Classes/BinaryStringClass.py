

class BitString:        
    def __init__(self, inp=None):
        if(inp is None):
            self.vals = [False]
        elif(type(inp) is int):
            self.vals = BitString.valsFromInt(inp)
        elif(type(inp) is BitString):
            self.vals = BitString.parseAsBinary(inp.vals)
        elif(hasattr(inp, 'vals')):
            self.vals = BitString.parseAsBinary(inp.vals)
        elif(type(inp) is str):
            for char in inp:
                if(char!='1' and char !='0'):
                    print("Invalid String argument:", inp)
                    assert False
            self.vals = BitString.parseAsBinary([int(i) for i in inp])
        elif(hasattr(inp, '__iter__')):
            self.vals = BitString.parseAsBinary(inp)
        elif(inp==0):
            self.vals = [False]
        elif(inp==1):
            self.vals = [True]
        else:
            self.vals = [False]   # Create a BitString '0' for all edge-case inputs to con'r call.
        self.numDigs = len(self.vals)

# Evaluate the bitstring [to a number]        
# Use 'width=n' keyword argument to specify a width for evaluating 'int' datatypes.
#      Example: [[to evaluate a 16-bit integer]] b.eval('int', width=16) 
    def eval(self, dtype='uint', **kwargs):
        if(dtype=='uint'):
            n=0
            for i in self.vals:
                n *= 2
                n += (1 if i else 0)
            return n
        elif(dtype=='int'):
            if(self.numDigs > kwargs['width']):
                return 0
            posVal=0
            negVal=0
            if(self.numDigs == kwargs['width']):
                if(self.vals[0]):
                    negVal = -2**(self.numDigs-1)
            for i in self.vals[1:]:
                posVal *= 2
                posVal += (1 if i else 0)
            return (posVal + negVal)
        else:       # Edge-Case for argument 'dtype'
            return 0
        
    def any(self):
        return True in self.vals
    
    def all(self):
        return not (False in self.vals)
    
# Displays the object in various formats (specified by Format argument).
    def disp(self, Format='string'):
        ret = ''   # The final string
        if(Format=='string'):
            ret = ''.join([ '1' if i else '0' for i in self.vals ])
        elif(Format=='debug'):
            for idx in range(len(self.vals)):
                ret += str(idx) + ': ' + ('True' if self.vals[idx] else 'False') + ', '
            if(ret[-2:]==', '):      # Removing trailing space added in the for loop.
                ret = ret[:len(ret)-2]
        else:       # Edge-case for the argument 'Format'
            ret = 'Invalid Format specified in call to disp()'
        return ret
    
    def valsFromInt(N):
        if(N<=0):
            return [False]
        ret = list()
        while(N):
            ret = [(True if (N%2) else False)] + ret
            N = N//2
        return ret
    
    # Divides a bitstring into bytes.
    # Returns a list of BitStrings, each of length 8 representing each byte of the input.
    # Input length has to be a multiple of 8, or 0.
    def bytes(self):
        if(self.numDigs%8):
            raise TypeError('Unsupported length of BitString: '+str(self.numDigs)+\
                            '. Length must be a multiple of 8 or 0.')
        else:
            L = list()
            for end in range(8, self.numDigs+1, 8):
                L.append(self.vals[end-8:end])
            return [BitString(b) for b in L]
                


##################
#  MAGIC METHODS  
##################      

# Enables the function call: len(obj)
# The private attribute self.numDigs is returned.
    def __len__(self):
        return self.numDigs
    
# hash(b) combines b's uInt value and length into a tuple 't' and returns hash(t).
    def __hash(self):
        return hash((eval(self, 'unit'), self.numDigs))
    
    def __bool__(self):
        return (self.numDigs > 0)
        
    def __str__(self):
        return self.disp(Format='string')
    
    def __repr__(self):
        return 'BitString(' + self.disp(Format='debug') + ')'
    
    def __eq__(self, b):
        if(not hasattr(b, 'vals') or not hasattr(b.vals, '__iter__')):
            return NotImplemented     # == works for any right object with an iterable 'vals' attribute.
        return (self.vals==b.vals)
    
    def __int__(self):
        return self.eval(dtype='uint')
    
    def __float__(self):
        return float(self.__int__())
    
    def __add__(self, b):
        assert hasattr(b, 'vals')
        assert hasattr(b.vals, '__iter__')
        newVals = self.vals + list(b.vals)
        return BitString(newVals)
    __radd__ = __add__
    
    def __iadd__(self, b):
        assert hasattr(b, 'vals')
        assert hasattr(b.vals, '__iter__')
        extraVals = BitString.parseAsBinary(b.vals)
        self.vals = self.vals + extraVals
        self.numDigs = len(self.vals)
        return self
    
    def __mul__(self, n):
        assert (type(n) is int)
        return BitString(self.vals*n)

    def __rmul__(self, n):
        return NotImplemented
    
    def __and__(self, b):
        if not (hasattr(b, 'vals') and hasattr(b.vals, '__iter__')):
            return NotImplemented
        if(len(self.vals) != len(b.vals)):
            return NotImplemented
        return BitString([(i and j) for i,j in zip(self.vals, b.vals)])

    def __or__(self, b):
        if not (hasattr(b, 'vals') and hasattr(b.vals, '__iter__')):
            return NotImplemented
        if(len(self.vals) != len(b.vals)):
            return NotImplemented
        return BitString([(i or j) for (i,j) in zip(self.vals, b.vals)])
    
    def __xor__(self, b):
        if not (hasattr(b, 'vals') and hasattr(b.vals, '__iter__')):
            return NotImplemented
        if(len(self.vals) != len(b.vals)):
            return NotImplemented
        return BitString(   ((i or j) and not (i and j))    for i,j in zip(self.vals, b.vals))
    
    def __invert__(self):
        assert hasattr(self, 'vals')
        return BitString([not v for v in self.vals])

######################
#  ITERATOR METHODS  
######################

    # def __iter__(self):
    #     return iter(self.vals)     # Return an iterator for b.vals
    
    def __getitem__(self, key):
        try:
            return BitString(self.vals[key])
        except IndexError:
            raise IndexError('BitString index out of range')
    
    def __setitem__(self, pos, val):
        try:
            self.vals[pos] = (True if val else False)
        except IndexError:
            raise IndexError('BitString assignment index out of range')
    
# Parses a given iterable and evaluates each element as True or False by evaluating an 'if' condition.
# Returns a new list containing only True and False objects corresponding to the original iterable.    
    def parseAsBinary(ls):
        newLs = [True if i else False for i in ls]    # A neat use of list comprehension.
        return newLs
    
    def flip(self, pos):
        self.vals[pos] = (not self.vals[pos])
        

        