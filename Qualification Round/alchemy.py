# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Qualification Round - Problem B. Alchemy
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/B
#
# Time:  O(N)
# Space: O(1)
#

from collections import Counter

def alchemy():
    N = input()
    count = Counter(raw_input().strip())
    return "NY"[int(abs(count['A']-count['B']) == 1)]

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, alchemy())
