
class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

#######################
#    MAGIC METHODS
#######################

    def __abs__(self):
        return ( (self.x**2)+(self.y**2) )**(0.5)
    
    def __add__(self, other):
        return Vector2D(self.x+other.x, self.y+other.y)
    
    def __mul__(self, N):
        try:
            return Vector2D(self.x*N, self.y*N)
        except TypeError:
            raise NotImplementedError('Multiplication of '+self.__class__.__name__+\
                                      ' with '+N.__class__.__name__+' is not supported.')
    __rmul__ = __mul__
       
    # "a**b" is the syntax for Dot Operation on vectors
    def __pow__(self, other):
        return (self.x*other.x + self.y*other.y)
    
    def __bool__(self):
        return bool(self.x or self.y)

    # Uncomment this method to enable '~v1' syntax to calculate |v1|
    def __invert__(self):
        return self.__abs__()
    
    def __repr__(self):
        return 'Vector2D(' + str(self.x) + ',' + str(self.y) + ')'
    
    
    