# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Final Round - Problem E. Tree Training
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/final-round/problems/E
#
# Time:  O(N * (logN)^2), pass in PyPy2 but Python2
# Space: O(N)
#

def ceil_log2_x(x):
    return (x-1).bit_length()

def tree_count(h):  # of nodes in full binary tree with height h
    return POW[h+1]-1

def E(z, s, h):  # E(z, s, h) = max. *s which can fit alongside z 0s (with s *s before the 1st 0) in a tree of height at most h
    if z == 0:
        return tree_count(h)
    left = min(s, h+1-z)  # *s at root and along leftmost branch
    cnt = tree_count(h)
    cnt -= tree_count(h-left)  # subtract subtree of 1st 0
    if cnt >= s:
        cnt += tree_count(h-left-1)  # add back right subtree of 1st 0
    return cnt

def F(p, z, s, LOG):  # F(p, z, s, LOG) = min. tree height for p *s, z 0s, and s *s before 1st 0 (s ignored if z = 0)
    left = (z + int(s > 0) - 1) if z else 0
    right = min(p+z, LOG)-1
    while left <= right:
        mid = left+(right-left)//2
        if E(z, s, mid) >= p:
            right = mid-1
        else:
            left = mid+1
    return left

def tree_training():
    S = raw_input().strip()
    N = len(S)
    LOG = ceil_log2_x(N+1)

    # find 0s
    Z = [-1]
    Z.extend(i for i in xrange(N) if S[i] == '0')
    Z.append(N)
    
    # A) z = 0
    result = cnt = 0
    intervals = [0]*((N+2)+1)
    for i in xrange(1, len(Z)):
        x = Z[i]-Z[i-1]-1  # sequence of x *s before ith 0
        cnt += x
        intervals[2] -= 1  # contribute -1 from [2, x+2)
        intervals[x+2] += 1
    delta = 0
    for i in xrange(1, N+1):
        delta += intervals[i]
        cnt += delta
        result = (result + cnt*F(i, 0, 0, LOG)) % MOD

    # B) 1 <= z <= LOG
    for z in xrange(1, LOG+1):  # z 0s, O(logN) times
        for i in xrange(1, len(Z)-z):  # ith 0 as the leftmost 0, sum(Z[i]-Z[i-1]-1 for i in xrange(1, len(Z)-z)) = O(N) times
            j = i+z-1
            l = Z[i]-Z[i-1]-1  # l *s to the left
            r = Z[j+1]-Z[j]-1  # r *s to the right
            m = Z[j]-Z[i]+1-z  # m *s in between
            for s in xrange(l+1):  # use s *s to the left
                p, max_p = s+m, s+m+r
                h = F(p, z, s, LOG)
                while p <= max_p:  # O(logN) times
                    np = min(max_p, E(z, s, h))
                    result = (result + (np-p+1)*h) % MOD
                    p = np+1
                    h += 1

    # C) z > LOG
    for i in xrange(1, len(Z)-1):  # count contribution of the ith 0, O(N) times
        result = (result + (Z[i]+1)*(N-Z[i])) % MOD  # add # of intervals containing the ith 0
        # subtract # of intervals containing the ith 0, with <= LOG 0s
        for j in xrange(max(i-LOG+1, 1), i+1):  # jth 0 as the leftmost 0, O(logN) times
            k = min(j+LOG, len(Z)-1)  # first disallowed 0
            c = (Z[j]-Z[j-1]) * (Z[k]-Z[i]) % MOD
            result = (result - c) % MOD
        j = i+LOG
        if j < len(Z):  # subtract # of intervals starting with the ith 0, with > LOG 0s
            result = (result - (N-Z[j])) % MOD

    return result

MOD = 10**9+7
MAX_N = 10**6
POW = [1]
for i in xrange(ceil_log2_x(MAX_N+1)+1):
    POW.append(POW[-1]*2)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, tree_training())
