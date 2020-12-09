# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Final Round - Problem B. Somebody Else's Problem
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/final-round/problems/B
#
# Time:  O(N)
# Space: O(H), H is the height of the tree
#

from functools import partial

def iter_postorder_traversal(children):  # Time: O(N)
    def divide(i):
        stk.append(partial(conquer, i))
        for j in reversed(xrange(len(children[i]))):
            c = children[i][j]
            stk.append(partial(divide, c))

    def conquer(i):
        for c in children[i]:
            dp1[i] = max(dp1[i], dp1[c]+1)  # dp1[i]: max len from i to leaf

    stk, dp1 = [], [0]*len(children)
    stk.append(partial(divide, 0))
    while stk:
        stk.pop()()
    return dp1

def iter_preorder_traversal(children, dp1):  # Time: O(N)
    def divide(i, d):
        for j in reversed(xrange(len(children[i]))):
            c = children[i][j]
            stk.append(partial(divide, c, d+1))
        stk.append(partial(init, i, d))

    def init(i, d):
        result[0] = result[0]*max(dp1[i]+(1+dp2[i] if i else 0), dp3[i]) % MOD
        m1, m2 = (0, -1), (0, -1)
        for c in children[i]:  # find the top 2 long paths
            p = (dp1[c]+1, c)
            if p > m1:
                m1, m2 = p, m1
            elif p > m2:
                m2 = p
        for c in children[i]:
            m = m2[0] if m1[1] == c else m1[0]                  # if c is included in the top1 long path, use the top2 one
            dp2[c] = max(d+m, dp2[i])                           # dp2[c]: max len from root to leaf outside c's subtree
            dp3[c] = max(dp3[i]+1, 1+m+(1+dp2[i] if i else 0))  # dp3[c]: max len from c to parent i plus from parent i to leaf plus from root to leaf outside parent i's subtree

    result = [1]
    stk, dp2, dp3 = [], [0]*len(children), [0]*len(children)
    stk.append(partial(divide, 0, 0))
    while stk:
        stk.pop()()
    return result[0]

def somebody_elses_problem():
    N = input()

    children = [[] for _ in xrange(N)]
    for i, m in enumerate(map(int, raw_input().strip().split()), 1):
        children[m-1].append(i)
    dp1 = iter_postorder_traversal(children)
    return iter_preorder_traversal(children, dp1)

MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, somebody_elses_problem())
