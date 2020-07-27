# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Qualification Round - Problem C. Timber
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/C
#
# Time:  O(NlogN)
# Space: O(N)
#

from collections import defaultdict

def timber():
    N = input()
    P = [map(int, raw_input().strip().split()) for _ in xrange(N)]
    P.sort()
    lookup = defaultdict(lambda:defaultdict(int))
    result = 0
    for d, direction in ((1, lambda x:x), (-1, reversed)):
        for p, l in direction(P):
            lookup[d][p+d*l] = max(lookup[d][p+d*l], lookup[d][p]+l)
        for p, l in lookup[d].iteritems():
            result = max(result, lookup[-d][p]+l)
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, timber())
