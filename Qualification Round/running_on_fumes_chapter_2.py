# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Qualification Round - Problem D2. Running on Fumes - Chapter 2
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/qualification-round/problems/D2
#
# Time:  O(NlogN)
# Space: O(N)
#

# Template: https://github.com/kamyu104/FacebookHackerCup-2018/blob/master/Round%202/fossil_fuels.py
# Range Minimum Query
class SegmentTree(object):  # 0-based index
    def __init__(self, N,
                 build_fn=lambda x, y: [y]*(2*x),
                 query_fn=lambda x, y: y if x is None else min(x, y),
                 update_fn=lambda x, y: y if x is None else min(x, y),
                 default_val=float("inf")):
        self.N = N
        self.H = (N-1).bit_length()
        self.query_fn = query_fn
        self.update_fn = update_fn
        self.default_val = default_val
        self.tree = build_fn(N, default_val)
        self.lazy = [None]*N

    def __apply(self, x, val):
        self.tree[x] = self.update_fn(self.tree[x], val)
        if x < self.N:
            self.lazy[x] = self.update_fn(self.lazy[x], val)

    def update(self, L, R, h):  # Time: O(logN), Space: O(N)
        def pull(x):
            while x > 1:
                x //= 2
                self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2+1])
                if self.lazy[x] is not None:
                    self.tree[x] = self.update_fn(self.tree[x], self.lazy[x])

        L += self.N
        R += self.N
        L0, R0 = L, R
        while L <= R:
            if L & 1:  # is right child
                self.__apply(L, h)
                L += 1
            if R & 1 == 0:  # is left child
                self.__apply(R, h)
                R -= 1
            L //= 2
            R //= 2
        pull(L0)
        pull(R0)

    def query(self, L, R):  # Time: O(logN), Space: O(N)
        def push(x):
            n = 2**self.H
            while n != 1:
                y = x // n
                if self.lazy[y] is not None:
                    self.__apply(y*2, self.lazy[y])
                    self.__apply(y*2 + 1, self.lazy[y])
                    self.lazy[y] = None
                n //= 2

        result = self.default_val
        if L > R:
            return result

        L += self.N
        R += self.N
        push(L)
        push(R)
        while L <= R:
            if L & 1:  # is right child
                result = self.query_fn(result, self.tree[L])
                L += 1
            if R & 1 == 0:  # is left child
                result = self.query_fn(result, self.tree[R])
                R -= 1
            L //= 2
            R //= 2
        return result

def dfs(adj, root):
    parents = [-2]*len(adj)
    parents[root] = -1
    stk = [root]
    while stk:
        node = stk.pop()
        for child in adj[node]:
            if parents[child] >= -1:
                continue
            parents[child] = node
            stk.append(child)
    return parents

def bfs(adj, C, parents, root, prev, max_d):
    min_C = []
    q = [root]
    while q and len(min_C) <= max_d:
        new_q = []
        min_C.append(INF)
        for node in q:
            if C[node]:
                 min_C[-1] =  min(min_C[-1], C[node])
            for child in adj[node]:
                if parents[child] == node and child != prev:
                    new_q.append(child)
        q = new_q
    return min_C

def running_on_fumes_chapter_2():
    N, M, A, B = map(int, raw_input().strip().split())
    A -= 1
    B -= 1
    C = [0]*N
    adj = [[] for _ in xrange(N)]
    for i in xrange(N):
        parent, C[i] =  map(int, raw_input().strip().split())
        parent -= 1
        if parent == -1:
            continue
        adj[i].append(parent)
        adj[parent].append(i)
    parents = dfs(adj, B)
    node, K = A, 0
    while node != B:
        node = parents[node]
        K += 1
    segment_tree = SegmentTree(K, default_val=INF)
    segment_tree.update(0, 0, 0)
    node, prev = A, -1
    for k in xrange(K):
        min_C = bfs(adj, C, parents, node, prev, min(k, M))
        for d, min_c in enumerate(min_C):
            if min_c == INF:
                continue
            min_cs = segment_tree.query(max(k-(M-d), 0), max(k-1, 0))
            if min_cs < INF-min_c:
                segment_tree.update(k-d, k-d, min_cs+min_c)
        node, prev = parents[node], node
    result = segment_tree.query(max(K-M, 0), K-1)
    return result if result != INF else -1

MAX_N = 10**6
MAX_C = 10**9
INF = (MAX_N-2)*MAX_C+1
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, running_on_fumes_chapter_2())
