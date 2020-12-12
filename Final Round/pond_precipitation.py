# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Final Round - Problem C. Pond Precipitation
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/final-round/problems/C
#
# Time:  O(N^5)
# Space: O(N^2)
#

def inv(n):  # Time: O(logN)
    return pow(n, MOD-2, MOD)

def addmod(a, b):
    return (a+b)%MOD

def mulmod(a, b):
    return (a*b)%MOD

def nCr(fact, inv_fact, n, r):
    return ((fact[n]*inv_fact[r])%MOD)*inv_fact[n-r]%MOD

def pond_precipitation():
    N = input()
    D = map(int, raw_input().strip().split())

    max_capacity = [0]*N
    prev, capacity = 0, 0
    for i in xrange(N+1):  # Time: O(N), Space: O(N)
        if i == N or D[i] < D[prev]:
            for j in xrange(prev+1, i):
                capacity += D[j]-D[prev]
            for j in xrange(prev+1 if prev else 0, i+1 if i < N else i):
                max_capacity[j] = capacity
            prev = i
    fact, inv_fact = [0]*(capacity+1), [0]*(capacity+1)
    fact[0] = 1
    for i in xrange(1, capacity+1):  # Time: O(N^2), Space: O(N^2)
        fact[i] = mulmod(fact[i-1], i)
    inv_fact[capacity] = inv(fact[capacity])
    for i in reversed(xrange(capacity)):
        inv_fact[i] = mulmod(inv_fact[i+1], (i+1))
    dp = [1]
    for i in xrange(N):  # Time: O(N * N^2 * N^2), Space: O(N^2)
        new_dp = [0]*(max_capacity[i]+1)
        for j in xrange(max_capacity[i-1]+1 if i else 1):
            for k in xrange(max_capacity[i]-j+1):
                new_dp[j+k] = addmod(new_dp[j+k], mulmod(dp[j], nCr(fact, inv_fact, j+k, j)))
        dp = new_dp
    result = 0
    inv_N, inv_N_pow_i = inv(N), 1
    for i in xrange(capacity+1):  # Time: O(N^2), Space: O(N^2)
        result = addmod(result, mulmod(dp[i], inv_N_pow_i))
        inv_N_pow_i = mulmod(inv_N_pow_i, inv_N)
    return result

MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, pond_precipitation())
