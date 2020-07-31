# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Qualification Round - Problem A. Travel Restrictions
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/A
#
# Time:  O(N^2)
# Space: O(1), excluding the space of output
#

def travel_restrictions():
    N = input()
    I, O = [raw_input().strip() for _ in xrange(2)]
    result = []
    for start in xrange(N):
        left = right = start
        while left-1 >= 0 and O[left] == I[left-1] == 'Y':
            left -= 1
        while right+1 < N and O[right] == I[right+1] == 'Y':
            right += 1
        result.append('N'*left + 'Y'*(right-left+1) + 'N'*(N-1-right))
    return "\n" + "\n".join(result)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, travel_restrictions())
