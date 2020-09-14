# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Round 3 - Problem B. Railroad Renovations
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-3/problems/B
#
# Time:  O(N^3)
# Space: O(N * K)
#

from bisect import bisect_left

def railroad_renovations():
    N, K = map(int, raw_input().strip().split())
    observations = []
    for i in xrange(N):
        Pi, Ri = map(int, raw_input().strip().split())
        observations.append((Pi, i, Ri))
    observations.sort()
    dp = [[float("inf")]*(K+1) for _ in xrange(N+1)]  # dp[i][j]: min renovations after first i observations with j rearrangements
    dp[0][0] = 0
    for i in xrange(N):
        if i-1 >= 0 and observations[i][0] == observations[i-1][0]:
            continue
        count = [0]*2
        ordered_set = []
        for j in xrange(i, N):
            ordered_set.insert(bisect_left(ordered_set, observations[j][1:]), observations[j][1:])
            count[observations[j][2]] += 1
            if j+1 < N and observations[j][0] == observations[j+1][0]:
                continue
            min_cost = min(count)  # find min cost to make all 0s before all 1s
            curr_count = [0]*2
            for _, r in ordered_set:
                curr_count[r] += 1
                min_cost = min(min_cost, curr_count[1]+(count[0]-curr_count[0]))
            for k in xrange(min_cost, K+1):
                dp[j+1][k] = min(dp[j+1][k], dp[i][k-min_cost]+int(count[1] > 0))
    result = min(dp[N])
    return result if result != float("inf") else -1

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, railroad_renovations())
