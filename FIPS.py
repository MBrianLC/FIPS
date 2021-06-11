import numpy as np
import collections
from scipy import stats

# Executes the Monobit test: it counts ones in the sequence
def monobit(u,n):
    f = collections.Counter(u)
    ones = f['1']
    return (ones,stats.binom_test(ones, n))
	
# Divides the sequence into blocks and executes the Monobit test on each one
def monobit_blocks(u,n,m):
    a = n//m
    l = []
    for i in range(a):
        f = collections.Counter(u[i*m:(i+1)*m])
        ones = f['1']
        l.append(ones)
    return stats.chisquare(l,a*[m/2])
	
# Executes the Poker test: it counts the number of occurrences of each possible 4-bit subsequence
def poker(u,n):
    b = n//4
    r = 4*b
    mat = [int(u[start:start+4],2) for start in range(0, r, 4)]
    oc_mat = sep(2,2,mat)
    return chisquare(np.array(oc_mat))
	
# Returns a vector with the number of runs (consecutive 0s or 1s) of size 1, 2, 3, 4, 5, +6 and + long
from itertools import groupby

def runs_seq(u,n,long):
    r = [(k, sum(1 for i in g)) for k,g in groupby(u)]
    f = collections.Counter(r)
    runs = [0 for i in range(13)]
    cont = 0
    l = len(r)
    for i in range(1,6):
        r1,r2 = f[('0',i)],f[('1',i)]
        runs[2*i-2] = r1
        runs[2*i-1] = r2
        cont += r1 + r2
    for i in range(6,long):
        r1,r2 = f[('0',i)],f[('1',i)]
        runs[10] += r1
        runs[11] += r2
        cont += r1 + r2
    j = long
    while(cont < l):
        r1,r2 = f[('0',j)],f[('1',j)]
        r3 = r1 + r2
        runs[10] += r1
        runs[11] += r2
        runs[12] += r3
        cont += r3
        j += 1
    return runs
	
# Executes the Runs test: it counts the number of occurrences of runs (of 0s or 1s) of size k, with k = 1, 2, 3, 4, 5, +6 (6 and more)
long = 8
runs_freq = [1/4,1/4,1/8,1/8,1/16,1/16,1/32,1/32,1/64,1/64,1/64,1/64]

def runs(u,n,long):
    runs = runs_seq(u,n,long)
    s = sum(runs) - runs[12]
    rf = [s*i for i in runs_freq]
    return stats.chisquare(runs[:12],rf,1)
	
# Executes the Long Run test (modified): it counts the number of runs of size long or more
def long_run(u,n,long):
    runs = runs_seq(u,n,long)
    rl = runs[12]
    s = sum(runs) - rl
    return (rl,stats.binom_test(rl,s,1/(2**(long-1))))
	
# Divides the sequence into blocks and executes the Long Run test on each one
def long_run_blocks(u,n,m,long):
    a = n//m
    l = []
    for i in range(a):
        l.append(runs_seq(u[i*m:(i+1)*m],m,long)[12])
    return stats.chisquare(l,a*[m/(2**long)])

# Executes the Long Run test (modified): it counts how many times two subsequences of size bits are equal
def cont_run(u,n,bits):
    b = n//bits
    r = bits*b
    v = [u[start:start+bits] for start in range(0, r, bits)]
    cont = 0
    act = v[0]
    for i in range(1,b):
        if (v[i] == act):
            cont += 1
        v[i] = act
    return (cont,stats.binom_test(cont, b-1, 1/(2**bits)))
	
# Divides the sequence into blocks and executes the Continuous test on each one
def cont_run_blocks(u,n,m,bits):
    a = n//m
    l = []
    for i in range(a):
        b = m//bits
        r = bits*b
        v = [u[start:start+bits] for start in range(i, i+r, bits)]
        cont = 0
        act = v[0]
        for i in range(1,b):
            if (v[i] == act):
                cont += 1
            v[i] = act
        l.append(cont)
    return stats.chisquare(l,a*[(b-1)/(2**bits)])
	
# Executes FIPS 140-2 battery tests in a sequence (faster than executing each test separately)
def fips(u,n,long):
    runs_freq = [1/4,1/4,1/8,1/8,1/16,1/16,1/32,1/32,1/64,1/64,1/64,1/64]
    aux = 1/(2**(long-1))
    l = len(u)
    b = n//4
    r = 4*b
    sp = [[] for i in range(l)]
    for i in range(l):
        # Monobit
        f = collections.Counter(u[i])
        ones = f['1']
        sp[i].append((ones,stats.binom_test(ones, n)))
        # Poker
        mat = [int(u[i][start:start+4],2) for start in range(0, r, 4)]
        oc_mat = sep(2,2,mat)
        sp[i].append(stats.chisquare(np.array(oc_mat)))
        # Runs
        runs = runs_seq(u[i],n,long)
        rl = runs[12]
        s = sum(runs) - rl
        rf = [s*i for i in runs_freq]
        sp[i].append(stats.chisquare(runs[:12],rf,1))
        # Long Run
        sp[i].append((rl,stats.binom_test(rl,s,aux)))
        # Continuous Run
		if bits != 4:
			mat = [int(u[i][start:start+bits],2) for start in range(0, r, bits)]
        cont = 0
        act = mat[0]
        for j in range(1,b):
            if (mat[j] == act):
                cont += 1
            mat[j] = act
        sp[i].append((cont,stats.binom_test(cont, b-1, 1/16)))
    return sp

# Executes FIPS 140-2 battery tests in a set of sequences
def FIPS(u,n,long):
    l = len(u)
    f = fips(u,n,8)
    s = [[] for i in range(l)]
    p = [[] for i in range(l)]
    for i in range(l):
        (s[i], p[i]) = zip(*f[i])
    return (s,p)