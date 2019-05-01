import pickle
from collections import defaultdict

def suffix_array(str): 
    def sort_bucket(str, bucket, order): 
        d = defaultdict(list) 
        for i in bucket: 
            key = str[i:i+order] 
            d[key].append(i) 
        result = [] 
        for _,v in sorted(d.items()): 
            if len(v) > 1: 
                result += sort_bucket(str, v, order*2) 
            else: 
                result.append(v[0]) 
        return result 
    return sort_bucket(str, (i for i in range(len(str))), 1)

def bwt(t, sa=None):
    bw = []
    if sa is None:
        sa = suffix_array(t)
    for si in sa:
        if si == 0:
            bw.append('$')
        else:
            bw.append(t[si-1])
    return ''.join(bw)

class FmIndex():    
    @staticmethod
    def __downsample_suffix_array(sa, n=32):
        ssa = {}
        for i, suf in enumerate(sa):
            if suf % n == 0:
                ssa[i] = suf
        return ssa
    
    def __init__(self, t, loadFromFile = False, sa = None, cpIval=128, ssaIval=32):
        if loadFromFile == True:
            self.__load(t)
            self.slen = len(self.bwt)
        else:
            if t[-1] != '$':
                t += '$'
            if sa == None:
                sa = suffix_array(t)
            self.bwt = bwt(t, sa)
            self.ssa = self.__downsample_suffix_array(sa, ssaIval)
            self.slen = len(self.bwt)

            self.__create_checkpoints(cpIval)

            tots = dict()
            for c in self.bwt:
                tots[c] = tots.get(c, 0) + 1

            self.first = {}
            totc = 0
            for c, count in sorted(tots.items()):
                self.first[c] = totc
                totc += count

    def __create_checkpoints(self, cpIval=128):
        self.cps = {}        
        self.cpIval = cpIval 
        tally = {}           
        
        for c in self.bwt:
            if c not in tally:
                tally[c] = 0
                self.cps[c] = []
                
        for i, c in enumerate(self.bwt):
            tally[c] += 1
            if i % cpIval == 0:
                for c in tally.keys():
                    self.cps[c].append(tally[c])
    
    def __load(self, filePath):
        with open(filePath, "rb") as f:
            x = pickle.load(f)
        self.bwt = x["bwt"]
        self.ssa = x["ssa"]
        self.cpIval = x["cpIval"]
        self.first = x["first"]
        self.cps = x["cps"]
    
    def __rank(self, bw, c, row):
        if row < 0 or c not in self.cps:
            return 0
        i, nocc = row, 0
        
        while (i % self.cpIval) != 0:
            if bw[i] == c:
                nocc += 1
            i -= 1
        return self.cps[c][i // self.cpIval] + nocc
    
    def __range(self, p):
        l, r = 0, self.slen - 1
        for i in range(len(p)-1, -1, -1):
            l = self.__rank(self.bwt, p[i], l-1) + self.__count(p[i])
            r = self.__rank(self.bwt, p[i], r)   + self.__count(p[i]) - 1
            if r < l:
                break
        return l, r+1
    
    def __resolve(self, row):
        def step_left(row):
            c = self.bwt[row]
            return self.__rank(self.bwt, c, row-1) + self.__count(c)
        nsteps = 0
        while row not in self.ssa:
            row = step_left(row)
            nsteps += 1
        return self.ssa[row] + nsteps
    
    def __count(self, c):
        if c not in self.first:
            for cc in sorted(self.first.keys()):
                if c < cc: return self.first[cc]
            return self.first[cc]
        else:
            return self.first[c]
    
    def has_substring(self, p):
        ''' Return true if p is substring of t '''
        l, r = self.__range(p)
        return r > l
    
    def has_suffix(self, p):
        ''' Return true if p is suffix of t '''
        l, r = self.__range(p)
        if(l >= self.slen):
            return False
        off = self.__resolve(l)
        return r > l and off + len(p) == self.slen-1
    
    def search(self, p):
        ''' Return all occurrences of p in t '''
        l, r = self.__range(p)
        return [ self.__resolve(x) for x in range(l, r) ]

    def save(self, filePath):
        ''' Save FM Index '''
        x = {"bwt": self.bwt,
        "ssa": self.ssa,
        "cps": self.cps,
        "cpIval": self.cpIval,
        "first": self.first}
        with open(filePath, "wb") as f:
            pickle.dump(x, f)