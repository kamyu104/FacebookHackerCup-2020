# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Round 3 - Problem A. Chain Explosions
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-3/problems/A
#
# Time:  O(K^(1/2))
# Space: O(1)
#

def chain_explosions():
    K = input()
    N, edges = 2, [(1, 2)]
    while K:
        hub, D = N, 1
        while (D+1)*D <= K:
            N += 1
            edges.append((hub, N))
            D += 1
        K -= D*(D-1)
    return "%s %s\n" % (N, len(edges)) + "\n".join("%s %s" % (a, b) for a, b in edges)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, chain_explosions())
