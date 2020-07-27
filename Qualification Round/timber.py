# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Qualification Round - Problem C. Timber
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/C
#
# Time:  O(NlogN)
# Space: O(N)
#

def expand(P, p_h, max_length, direction):
    for p, h in direction(P): 
        if p in max_length:
            continue
        l = 0
        while True:
            next_p, h = p_h[p]
            if next_p in max_length:
                break
            l += h
            max_length[next_p] = l
            if next_p not in p_h:
                break
            p = next_p

def timber():
    N = input()
    P = [map(int, raw_input().strip().split()) for _ in xrange(N)]
    P.sort()
    left, right = {p:(p-h, h) for p, h in P}, {p:(p+h, h) for p, h in P}
    left_max_length, right_max_length = {}, {}
    expand(P, left, left_max_length, reversed)
    expand(P, right, right_max_length, lambda x:x)
    result = 0
    for p, l in left_max_length.iteritems():
        result = max(result, l)
        if p in right_max_length:
            result = max(result, l+right_max_length[p])
    for p, l in right_max_length.iteritems():
        result = max(result, l)
        if p in left_max_length:
            result = max(result, l+left_max_length[p])
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, timber())
