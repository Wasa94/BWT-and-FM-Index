def suffix_array(s):
    """ Given T return suffix array SA(T).  We use Python's sorted
        function here for simplicity, but we can do better. """
    satups = sorted([(s[i:], i) for i in range(len(s))])
    # Extract and return just the offsets
    # print(satups)
    return list(map(lambda x: x[1], satups))

def bwt(t):
    """ Given T, returns BWT(T) by way of the suffix array. """
    bw = []
    for si in suffix_array(t):
        if si == 0: bw.append('$')
        else: bw.append(t[si-1])
    return ''.join(bw) # return string-ized version of list bw

class FmIndex():
    def __init__(self, t, step = 32):
        if t[-1] != '$':
            t += '$'
        self.bwt = bwt(t)
        self.offset = {}
        self.step = step
        
        A = {}
        for _, c in enumerate(self.bwt):
            if A.get(c):
                A[c] += 1
            else:
                A[c] = 1

        letters = sorted(A.keys())
        occ = {}
        
        idx = 0
        for c in letters:
            occ[c] = idx
            idx += A[c]
        
        self.first = occ

        self.__create_checkpoints()
 
    def __create_checkpoints(self):
        A = {}
        cps = []
        for i, c in enumerate(self.bwt):
            if i % self.step == 0:
                cps.append(A.copy())
            if A.get(c):
                A[c] += 1
            else:
                A[c] = 1
        self.cps = cps
    
    def __count(self, idx, qc):
        def count_letter_with_checkpoints(cps, step, s, idx, letter):
            check = int((idx + (step / 2)) / step)
            if check >= len(cps):
                check = len(cps) - 1
            pos = check * step
            
            count = cps[check].get(letter)
            if count == None:
                count = 0
                
            if pos < idx:
                r = range(pos, idx)
            else:
                r = range(idx, pos)
                
            k = 0        
            for i in r:
                if letter == s[i]:
                    k += 1
                    
            if pos < idx:
                count += k
            else:
                count -= k
            
            return count
            
        count = count_letter_with_checkpoints(self.cps, self.step, self.bwt, idx, qc)
        return count
    
    def __rank(self, idx, qc):
        c = self.first.get(qc)
        if c == None:
            o = 0
        else:
            o = c
        c = self.__count(idx, qc)
        return o + c
    
    def __resolve(self, idx):
        r = 0
        i = idx 
        while self.bwt[i] != '$':
            if self.offset.get(i):
                r += self.offset[i]
                break
            r += 1
            i = self.__rank(i, self.bwt[i])
        
        if not self.offset.get(idx):
            self.offset[i] = r
        return r
    
    def __range(self, p):
        l = 0
        r = len(self.bwt)
        for _, i in enumerate(p[::-1]):
            l = self.__rank(l, i)
            r = self.__rank(r, i)
            if l == r: return (-1,-1)
        return (l,r)
    
    def search(self, p):
        ''' Return all occurrences of p in t '''
        l, r = self.__range(p)
        matches = []
        
        for i in range(l, r):
            pos = self.__resolve(i)
            matches.append(pos)
            
        return matches
    
    def has_substring(self, p):
        ''' Return true if p is substring of t '''
        l, r = self.__range(p)
        return r > l

    def has_suffix(self, p):
        ''' Return true if p is suffix of t '''
        l, r = self.__range(p)
        if(l >= len(self.bwt)):
            return False
        off = self.__resolve(l)
        return r > l and off + len(p) == len(self.bwt)-1