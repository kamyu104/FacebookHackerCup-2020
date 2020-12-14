# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Final Round - Problem D. Spider Spring
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/final-round/problems/D
#
# Time:  O((N + M) * logN), pass in PyPy2 but Python2
# Space: O(N)
#

from random import randint, seed

class SegmentTree(object):
    def __init__(self, N,
                 build_fn=lambda x, y: [y]*(2*x),
                 query_fn=lambda x, y: y if x is None else x+y,
                 update_fn=lambda x, y: y,  # lambda x, y: y if x is None else x+y
                 default_val=0):
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

    def __push_one(self, x):
        if x < self.N and self.lazy[x] is not None:
            self.__apply(x*2, self.lazy[x])
            self.__apply(x*2 + 1, self.lazy[x])
            self.lazy[x] = None

    def __push(self, x):
        n = 2**self.H
        while n != 1:
            y = x // n
            self.__push_one(y)
            n //= 2

    def update(self, L, R, h):  # Time: O(logN), Space: O(N)
        def pull(x):
            while x > 1:
                x //= 2
                self.__push_one(x*2)
                self.__push_one(x*2+1)
                self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2+1])
        
        L += self.N
        R += self.N
        self.__push(L)
        self.__push(R)
        L0, R0 = L, R
        while L <= R:
            if L & 1:  # is right child
                self.__apply(L, h)
                self.__push_one(L)
                L += 1
            if R & 1 == 0:  # is left child
                self.__apply(R, h)
                self.__push_one(R)
                R -= 1
            L //= 2
            R //= 2
        pull(L0)
        pull(R0)

    def query(self, L, R):  # Time: O(logN), Space: O(N)
        result = self.default_val
        if L > R:
            return result

        L += self.N
        R += self.N
        self.__push(L)
        self.__push(R)
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
    
    def __str__(self):
        showList = []
        for i in xrange(self.N):
            showList.append(self.query(i, i))
        return ",".join(map(str, showList))
    
# Template modified from:
# https://github.com/kamyu104/FacebookHackerCup-2020/blob/master/Final%20Round/cryptoconference.py
class SkipNode(object):
    def __init__(self, level=0, val=None):
        self.val = val
        self.nexts = [None]*level
        self.prevs = [None]*level

class SkipList(object):
    P_NUMERATOR, P_DENOMINATOR = 1, 2  # P = 1/4 in redis implementation
    MAX_LEVEL = 32  # enough for 2^32 elements

    def __init__(self, end=(float("inf"), float("inf")), can_duplicated=False):
        seed(0)
        self.__head = SkipNode()
        self.__len = 0
        self.__can_duplicated = can_duplicated
        self.add(end)
        self.__end = self.find(end)

    def begin(self):
        return self.__head.nexts[0]
    
    def end(self):
        return self.__end

    def lower_bound(self, target, cmp=lambda x, y: x < y):
        return self.__lower_bound(target, self.__find_prev_nodes(target, cmp))

    def find(self, target):
        return self.__find(target, self.__find_prev_nodes(target))
        
    def add(self, val):
        if not self.__can_duplicated and self.find(val):
            return self.find(val), False
        node = SkipNode(self.__random_level(), val)
        if len(self.__head.nexts) < len(node.nexts): 
            self.__head.nexts.extend([None]*(len(node.nexts)-len(self.__head.nexts)))
        prevs = self.__find_prev_nodes(val)
        for i in xrange(len(node.nexts)):
            node.nexts[i] = prevs[i].nexts[i]
            if prevs[i].nexts[i]:
                prevs[i].nexts[i].prevs[i] = node
            prevs[i].nexts[i] = node
            node.prevs[i] = prevs[i]
        self.__len += 1
        return node if self.__can_duplicated else (node, True)

    def remove(self, it):
        prevs = it.prevs
        curr = self.__find(it.val, prevs)
        if not curr:
            return self.__end
        self.__len -= 1   
        for i in reversed(xrange(len(curr.nexts))):
            prevs[i].nexts[i] = curr.nexts[i]
            if curr.nexts[i]:
                curr.nexts[i].prevs[i] = prevs[i]
            if not self.__head.nexts[i]:
                self.__head.nexts.pop()
        return curr.nexts[0]
    
    def __lower_bound(self, val, prevs):
        if prevs:
            candidate = prevs[0].nexts[0]
            if candidate:
                return candidate
        return None

    def __find(self, val, prevs):
        candidate = self.__lower_bound(val, prevs)
        if candidate and candidate.val == val:
            return candidate
        return None

    def __find_prev_nodes(self, val, cmp=lambda x, y: x < y):
        prevs = [None]*len(self.__head.nexts)
        curr = self.__head
        for i in reversed(xrange(len(self.__head.nexts))):
            while curr.nexts[i] and cmp(curr.nexts[i].val, val):
                curr = curr.nexts[i]
            prevs[i] = curr
        return prevs

    def __random_level(self):
        level = 1
        while randint(1, SkipList.P_DENOMINATOR) <= SkipList.P_NUMERATOR and \
              level < SkipList.MAX_LEVEL:
            level += 1
        return level
    
    def __iter__(self):
        it = self.begin()
        while it != self.end():
            yield it.val
            it = it.nexts[0]

    def __len__(self):
        return self.__len-1  # excluding end node

    def __str__(self):
        result = []
        for i in reversed(xrange(len(self.__head.nexts))):
            result.append([])
            curr = self.__head.nexts[i]
            while curr:
                result[-1].append(str(curr.val))
                curr = curr.nexts[i]
        return "\n".join(map(lambda x: "->".join(x), result))

def read(N, K):
    X = map(int, raw_input().strip().split())
    A, B, C, D = map(int, raw_input().strip().split())
    for _ in xrange(K, N):
        X.append((A*X[-2] + B*X[-1] + C) % D + 1)
    return X    

def query_heights(heights, i):
    return heights.query(i, i)

def update_heights(heights, i, j, h):
    heights.update(i, j, h)

def update_segment_trees(heights, segment_trees, N, i, d):
    if i < 0 or i+1 >= N:
        return
    a, b = query_heights(heights, i), query_heights(heights, i+1)
    if a > b:
        a, b = b, a
    w = (i+1) * (N-i-1)
    segment_trees[0].update(a, a, w*d % MOD)
    segment_trees[1].update(a, a, a*w*d % MOD)
    segment_trees[2].update(b, b, w*d % MOD)
    segment_trees[3].update(b, b, b*w*d % MOD)

def spider_spring():
    N, M, K = map(int, raw_input().strip().split())
    H = read(N, K)
    X, Y, Z, W = [read(M, K) for _ in xrange(4)]
    size = max(max(H), max(Z), max(W))
    heights = SegmentTree(N)
    segment_trees = [SegmentTree(size+1, update_fn=lambda x, y: y if x is None else x+y) for _ in xrange(4)]
    line_segments = SkipList(end=float("inf"))
    horiz = 0
    for i in xrange(N):
        update_heights(heights, i, i, H[i])
        update_segment_trees(heights, segment_trees, N, i-1, 1)
        line_segments.add(i-1)
        horiz = (horiz + i*(N-i)) % MOD
    result = 1
    for i in xrange(M):
        x, y, z, w = X[i]-1,  min(X[i]+Y[i]-1, N)-1, Z[i], W[i]
        it = line_segments.lower_bound(x-1)
        while it != line_segments.end() and it.val <= y:
            update_segment_trees(heights, segment_trees, N, it.val, -1)
            it = line_segments.remove(it)
        update_heights(heights, x, y, z)
        update_segment_trees(heights, segment_trees, N, x-1, 1)
        line_segments.add(x-1)
        update_segment_trees(heights, segment_trees, N, y, 1)
        line_segments.add(y)
        d1 = segment_trees[3].query(w+1, size)-segment_trees[1].query(w+1, size)
        d2 = segment_trees[2].query(w+1, size)-segment_trees[0].query(w+1, size)
        vert = (d1 - d2*w) % MOD
        result = result * (horiz+vert) * 2 % MOD
    return result

MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, spider_spring())
