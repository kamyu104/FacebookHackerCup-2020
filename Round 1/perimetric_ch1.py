# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Round 1 - Problem A. Perimetric - Chapter 1
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-1/problems/A1
#
# Time:  O(N)
# Space: O(N)
#

from collections import deque

def process_rect(L, W, H, i, P, dq, accu):
    while dq and L[i]-L[dq[0]] > W:
        dq.popleft()
    if not dq:
        accu += 2*(W+H[i])
    else:
        accu += 2*((L[i]-L[dq[-1]])+max(H[i]-H[dq[0]], 0))
    P.append(accu)
    while dq and H[dq[-1]] <= H[i]:
        dq.pop()
    dq.append(i)
    return accu

def perimetric_ch1():
    N, K, W = map(int, raw_input().strip().split())
    L = map(int, raw_input().strip().split())
    A_L, B_L, C_L, D_L = map(int, raw_input().strip().split())
    for _ in xrange(K, N):
        L.append((A_L*L[-2] + B_L*L[-1] + C_L) % D_L + 1)
    H = map(int, raw_input().strip().split())
    A_H, B_H, C_H, D_H = map(int, raw_input().strip().split())
    for _ in xrange(K, N):
        H.append((A_H*H[-2] + B_H*H[-1] + C_H) % D_H + 1)

    P, dq, accu = [], deque(), 0
    for i in xrange(N):
        accu = process_rect(L, W, H, i, P, dq, accu)
    return reduce(lambda x, y: (x*y)%MOD, P)

MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, perimetric_ch1())
