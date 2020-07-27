# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Qualification Round - Problem A. Travel Restrictions
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/A
#
# Time:  O(N^2)
# Space: O(N^2)
#

def travel_restrictions():
    N = input()
    I, O = [raw_input().strip() for _ in xrange(2)]
    adj = [[0]*N for _ in xrange(N)]
    for i in xrange(N):
        for j in xrange(i, N):
            adj[i][j] = 1
            if j+1 == N or O[j] == 'N' or I[j+1] == 'N':
                break
    for i in xrange(N):
        for j in reversed(xrange(i+1)):
            adj[i][j] = 1
            if j-1 == -1 or O[j] == 'N' or I[j-1] == 'N':
                break
    return "\n" + "\n".join("".join(map(lambda x: "NY"[x], row)) for row in adj)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, travel_restrictions())
