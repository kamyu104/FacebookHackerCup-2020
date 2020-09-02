# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Round 2 - Problem B. Elimination
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-2/problems/B
#
# Time:  O(N^2)
# Space: O(N^2)
#

def pair_count(x):
    return x*(x-1)//2

def expected_count(dp, b, w, is_swapped):
    ev = 1.0
    if b:
        ev += (dp[b-1][w] if not is_swapped else dp[w][b-1]) * pair_count(b) / pair_count(b+1+w)
    if w:
        ev += (dp[b][w-1] if not is_swapped else dp[w-1][b]) * ((b+1)*w+pair_count(w)) / pair_count(b+1+w)
    return ev

def elimination():
    N, P = raw_input().strip().split()
    N = int(N)
    P = float(P)

    dp = [[0.0]*N for _ in xrange(N)]
    for b in xrange(N):
        for w in xrange(N-b):
            if (b, w) == (0, 0):
                continue
            dp[b][w] = expected_count(dp, b, w, False)*P + expected_count(dp, w, b, True)*(1-P)
    return "\n" + "\n".join("%.8f" % (dp[N-1-i][i]) for i in xrange(N))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, elimination())
