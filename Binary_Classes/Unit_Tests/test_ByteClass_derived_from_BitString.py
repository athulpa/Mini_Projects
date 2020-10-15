
# Unit Tests for Byte Class

from ByteClass_derived_from_BitString import Byte

# Test the call to int(b) - should return the corresponsing integer [0 - 255]
def testInteger():
    for n in range(0, 256):
        b = Byte(n)
        ret = int(b)
        # print('n:', n, '\t ret:', ret)
        assert (ret==n)
    

def testIncrement():
    for i in range(0, 255):
        b = Byte(i)
        b_plus = b.inc()
        i_plus = int(b_plus)
        # print('i:', i, '\t ret:', i_plus)
        assert i_plus==(i+1)
        
    # Verify the roll-around case
    assert int(Byte(255).inc())==0
    
def testTwosComplement():
    for n in range(1, 255):
        b = Byte(n)
        b_twos = b.twosComp()
        n_twos = int(b_twos)
        # print('n:', n, '\t ret:', n_twos)
        assert (n + n_twos == 256)
    
    # Verify two's compliment of zero
    assert (int( Byte(0).twosComp() ) == 0)
        