# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Qualification Round - Problem D1. Running on Fumes - Chapter 1
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/D1
#
# Time:  O(N)
# Space: O(M)
#

from collections import deque

def running_on_fumes_chapter_1():
    N, M = map(int, raw_input().strip().split())
    C = [input() for _ in xrange(N)]
    dq = deque([(0, 0)])
    for i in xrange(1, len(C)):
        count = 0
        if dq and i-dq[0][0] > M:
            count += 1
            dq.popleft()
        if not dq:
            return -1
        if not C[i]:
            continue
        d = dq[0][1]+C[i]
        while dq and dq[-1][1] >= d:
            dq.pop()
        dq.append((i, d))   
    return dq[0][1]

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, running_on_fumes_chapter_1())
