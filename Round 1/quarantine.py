# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Round 1 - Problem C. Quarantine
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-1/problems/C
#
# Time:  O(N)
# Space: O(N)
#

from collections import defaultdict
from functools import partial

class PreorderTree(object):
    def __init__(self, root, N, adj):
        self.__at = []
        self.__children = adj
        self.__left = [-1]*N
        self.__right = [-1]*N
        self.__dfs(root)

    def __dfs(self, i):  # Time: O(N)
        def divide(i):
            stk.append(partial(conquer, i))
            for j in reversed(xrange(len(children[i]))):
                c = children[i][j]
                stk.append(partial(divide, c))
            stk.append(partial(init, i))

        def init(i):
            left[i] = len(at)
            at.append(i)

        def conquer(i):
            right[i] = len(at)

        stk, children, at, left, right = [], self.__children, self.__at, self.__left, self.__right
        stk.append(partial(divide, i))
        while stk:
            stk.pop()()

    def at(self, i):
        return self.__at[i]

    def left(self, i):
        return self.__left[i]

    def right(self, i):
        return self.__right[i]

def get_count(S, adj, i):
    cnt = 0
    stk = [i]
    while stk:
        node = stk.pop()
        if S[node] == '#':
            continue
        cnt += 1
        for child in reversed(adj[node]):
            stk.append(child)
    return cnt

def set_count(S, adj, i, cnt, C):
    stk = [i]
    while stk:
        node = stk.pop()
        if S[node] == '#':
            continue
        C[node] = cnt
        for child in reversed(adj[node]):
            stk.append(child)

def max_count(x, y):
    if x[0] != y[0]:
        return max(x, y)
    return (x[0], x[1]+y[1])

def quarantine():
    N, K = map(int, raw_input().strip().split())
    S = raw_input().strip()
    E = [0]+map(int, raw_input().strip().split())
    A, B, C = map(int, raw_input().strip().split())
    for i in xrange(K+1, N):
        E.append((A*E[-2] + B*E[-1] + C) % i + 1)
    adj = defaultdict(list)
    for i in xrange(len(E)):
        E[i] -= 1
        adj[E[i]].append(i)
    
    preorder_tree = PreorderTree(0, N, adj)
    C, region_count, base = [0]*N, 0, 0
    for i in xrange(N):  # flood fill in preorder traversal
        node = preorder_tree.at(i)
        if S[node] == '#' or C[node]:
            continue
        node_count = get_count(S, adj, node)
        set_count(S, adj, node, node_count, C)
        base += node_count*(node_count-1)//2
        region_count += 1
    subtree_pair = [(0, 0)]*N
    for i in reversed(xrange(N)):  # count subtree max_count in reversed preorder traversal
        node = preorder_tree.at(i)
        subtree_pair[node] = (C[node], 1)
        for child in adj[node]:
            subtree_pair[node] = max_count(subtree_pair[node], subtree_pair[child])
    prefix_pair = [(0, 0)]*(N+1)
    for i in xrange(N):  # count prefix max_count in preorder traversal
        node = preorder_tree.at(i)
        prefix_pair[i+1] = max_count(prefix_pair[i], (C[node], 1))
    suffix_pair = [(0, 0)]*(N+1)
    for i in reversed(xrange(N)):  # count suffix max_count in reversed preorder traversal
        node = preorder_tree.at(i)
        suffix_pair[i] = max_count(suffix_pair[i+1], (C[node], 1))
    result = (0, 0)
    if region_count != 1:
        for i in xrange(1, N):  # count each edge
            if S[i] == '*' and S[E[i]] == '*':
                continue
            # a edge could be only inserted between safe nodes of inside and outside
            inside = subtree_pair[i]
            outside = max_count(prefix_pair[preorder_tree.left(i)], suffix_pair[preorder_tree.right(i)])
            result = max_count(result, (base + inside[0]*outside[0], inside[1]*outside[1]))
    else:
        for i in xrange(1, N):  # count each edge
            if S[i] == '*' and S[E[i]] == '*':  # a edge could be only inserted between safe nodes of inside and safe nodes of outside
                inside = subtree_pair[i]
                outside = max_count(prefix_pair[preorder_tree.left(i)], suffix_pair[preorder_tree.right(i)])
            else:  # any edge could be inserted between inside and outside
                inside = (0, preorder_tree.right(i)-preorder_tree.left(i))
                outside = (0, N-inside[1])
            curr = (base, inside[1]*outside[1])  # max number of pairs won't be changed if region_count is 1
            result = max_count(result, curr)
    return "%s %s" % result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, quarantine())
