def get_pow(n):
    num = n
    pow_2 = 0
    while num > 0:
        num = num /2
        pow_2 += 1
    return pow_2

def int_to_bytea(n):
    out = []
    final = ''
    num = n
    num_bytes = get_pow(n)
    for i in xrange(num_bytes):
        out.append(0)
    
    while num > 0:
        pows = get_pow(num)
        num -= 2 ** (pows - 1)
        out[-pows] = 1
    for i in out:
        final += str(i)
    return final

def int_to_byte(n):
    s = bin(n).lstrip('-0')[1:]
    return s

def bin_to_int(l, start = 0):
    out = 0
    for i, j in zip(reversed(l), range(len(l))):
        if int(i):
            out += 2 ** (j + start)
    return out
    
        
class BigByte(list):    
    
    def __init__(self, string = 0, length = 0):
        if (type(string) != type(1)) and (type(string) != type('seed')):
            print "Invalid Type"
        elif (type(string) == type('seed')) and string.isdigit():
            string = int(string)
        byte = int_to_byte(string)
        if len(byte) < length:
            l = length - len(byte)
            for i in range(l):
                self.append(0)
        for e in byte:
            self.append(int(e))
        if length > 0:
            diff = length - len(self)
            for i in xrange(diff):
                self = [0] + self                

    def __repr__(self):
        return str(self)

    def __str__(self):
        out = ''
        for e in self:
            out += str(e)
        return out

    def __int__(self):
        out = 0
        for e in xrange(len(self)):
            if self[e]:
                out += 2 ** (len(self) - e - 1)
        return out
    
    def bAnd(self, byte2):
        out = int(self) & int(byte2)
        return BigByte(out)

    def __and__(self, byte2):
        return self.bAnd(byte2)

    def __rand__(self, byte2):
        return self.bAnd(byte2)

    def bOr(self, byte2):
        out = int(self) | int(byte2)
        return BigByte(out)

    def __or__(self, byte2):
        return self.bOr(byte2)

    def __ror__(self, byte2):
        return self.bOr(byte2)

    def bXor(self, byte2):
        out = int(self) ^ int(byte2)
        return BigByte(out)

    def __xor__(self, byte2):
        return self.bXor(byte2)

    def __rxor__(self, byte2):
        return self.bXor(byte2)

    def bLshift(self, n):
        num = int(self)
        return BigByte(num << n)

    def __lshift__(self, n):
        return self.bLshift(n)

    def bRshift(self, n):
        num = int(self)
        return BigByte(num >> n)

    def __rshift__(self, n):
        return self.bRshift(n)

    def bNot(self):
        out = ''
        for i in range(len(self)):
            if self[i]:
                out += '0'
            else:
                out += '1'
        out = bin_to_int(out)
        return BigByte(out, len(self))
                

    def __invert__(self):
        return self.bNot()

    def cross(self, byte2, index):
        self[index:], byte2[index:] = byte2[index:], self[index:]
            
