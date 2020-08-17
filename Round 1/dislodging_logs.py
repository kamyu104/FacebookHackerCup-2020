# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Round 1 - Problem B. Dislodging Logs
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-1/problems/B
#
# Time:  O(NlogN + MlogM + (M + N) * log(max(max(Q)-min(P), max(P)-min(Q))))
# Space: O(N + M)
#

def check(P, Q, x):
    left = 0
    for p in P:
        for right in xrange(left, len(Q)):
            if min(abs(Q[left]-p), abs(Q[right]-p)) + Q[right]-Q[left] > x:  # greedy
                left = right
                break
        else:  # fully covered
            return True
    return False

def dislodging_logs():
    N, M, K, S = map(int, raw_input().strip().split())
    assert(S == 0)
    P = map(int, raw_input().strip().split())
    A_P, B_P, C_P, D_P = map(int, raw_input().strip().split())
    for _ in xrange(K, N):
        P.append((A_P*P[-2] + B_P*P[-1] + C_P) % D_P + 1)
    Q = map(int, raw_input().strip().split())
    A_Q, B_Q, C_Q, D_Q = map(int, raw_input().strip().split())
    for _ in xrange(K, M):
        Q.append((A_Q*Q[-2] + B_Q*Q[-1] + C_Q) % D_Q + 1)
    P.sort(), Q.sort()
    left, right = 1, max(max(Q)-min(P), max(P)-min(Q))
    while left <= right:
        mid = left + (right-left)//2
        if check(P, Q, mid):
            right = mid-1
        else:
            left = mid+1
    return left

MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, dislodging_logs())
