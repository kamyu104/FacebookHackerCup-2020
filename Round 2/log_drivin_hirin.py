# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Round 2 - Problem D. Log Drivin' Hirin'
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-2/problems/D
#
# Time:  O(N * (logN)^2 + MlogN), pass in PyPy2 but Python2
# Space: O(N)
#

from functools import partial
from random import randint, seed

# Template:
# https://github.com/kamyu104/LeetCode-Solutions/blob/master/Python/design-skiplist.py
class SkipNode(object):
    def __init__(self, level=0, val=None):
        self.val = val
        self.nexts = [None]*level
        self.prevs = [None]*level

class SkipList(object):
    P_NUMERATOR, P_DENOMINATOR = 1, 2  # P = 1/4 in redis implementation
    MAX_LEVEL = 32  # enough for 2^32 elements

    def __init__(self, end=[float("inf"), float("inf"), float("inf")], can_duplicated=False):
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
            return False
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
        return True

    def remove(self, val):
        prevs = self.__find_prev_nodes(val)
        curr = self.__find(val, prevs)
        if not curr:
            return False
        self.__len -= 1   
        for i in reversed(xrange(len(curr.nexts))):
            prevs[i].nexts[i] = curr.nexts[i]
            if curr.nexts[i]:
                curr.nexts[i].prevs[i] = prevs[i]
            if not self.__head.nexts[i]:
                self.__head.nexts.pop()
        return True
    
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

# Template translated from:
# https://github.com/kth-competitive-programming/kactl/blob/master/content/data-structures/LineContainer.h
class LineContainer(object):
    def __init__(self):
        self.__skiplist = SkipList()

    def add(self, k, m):
        self.__skiplist.add([k, m, 0])
        z = self.__skiplist.find([k, m, 0])
        x = y = z
        z = z.nexts[0]
        while self.__intersect(y, z):
            z, to_del = z.nexts[0], z
            self.__skiplist.remove(to_del.val)
        if x != self.__skiplist.begin():
            x = x.prevs[0]
            if self.__intersect(x, y):
                y, to_del = y.nexts[0], y
                self.__skiplist.remove(to_del.val)
                self.__intersect(x, y)
        y = x
        while y != self.__skiplist.begin():
            x = x.prevs[0]
            if x.val[2] < y.val[2]:
                break
            y, to_del = y.nexts[0], y
            self.__skiplist.remove(to_del.val)
            self.__intersect(x, y)
            y = x
    
    def query(self, x):
        it = self.__skiplist.lower_bound(x, cmp=lambda x, y: x[2] < y)
        return it.val[0]* x + it.val[1]

    def gen(self):
        it = self.__skiplist.begin()
        while it != self.__skiplist.end():
            yield it.val
            it = it.nexts[0]

    def __intersect(self, x, y):
        if y == self.__skiplist.end():
            x.val[2] = float("inf")
            return False
        if x.val[0] == y.val[0]:
            x.val[2] = float("inf") if x.val[1] > y.val[1] else float("-inf")
        else:
            x.val[2] = (y.val[1]-x.val[1])//(x.val[0]-y.val[0])
        return x.val[2] >= y.val[2]
    
    def __len__(self):
        return len(self.__skiplist)
    
    def __str__(self):
        return str(self.__skiplist)

def read(K, N, D):
    X = map(int, raw_input().strip().split())
    if D:
        A, B, C = map(int, raw_input().strip().split())
    else:
        A, B, C, D = map(int, raw_input().strip().split())
    for i in xrange(K, N):
        X.append((A*X[-2] + B*X[-1] + C) % (D if D > 0 else i) + 1)
    return X

def iter_tree_traversal(N, children, L, H, Q):
    def query_result(i, d, c):
        return c*d + lines[idx[i]].query(c)

    def init(i):
        idx[i] = at[0]
        at[0] += 1

    def divide(i, d):
        stk.append(partial(conquer, i, d))
        for c in reversed(children[i]):
            stk.append(partial(divide, c, d+L[c]))
        stk.append(partial(init, i))

    def conquer(i, d):
        for j in children[i]:
            if len(lines[idx[i]]) < len(lines[idx[j]]):
                lines[idx[i]], lines[idx[j]] = lines[idx[j]], lines[idx[i]]
            for k, m, _ in lines[idx[j]].gen():  # merged at most O(logN) times, and each at most cost O(NlogN)
                lines[idx[i]].add(k, m)
            lines[idx[j]] = None  # clear
        lines[idx[i]].add(-d, -(-query_result(i, d, H[i]) if children[i] else 0))
        for c in Q[i]:
            result[0] = result[0] * ((-query_result(i, d, c) + 1) % MOD) % MOD

    result, stk, at, idx, lines = [1], [], [0], [-1]*N, [LineContainer() for _ in xrange(N)]
    stk.append(partial(divide, 0, 0))
    while stk:
        stk.pop()()
    return result[0]

def log_drivin_hirin():
    N, M, K = map(int, raw_input().strip().split())
    P = read(K, N, -1)
    L = read(K, N, 0)
    H = read(K, N, 0)
    X = read(K, M, N)
    Y = read(K, M, 0)

    children = [[] for _ in xrange(N)]
    for i in xrange(1, N):
        children[P[i]-1].append(i)
    Q = [[] for _ in xrange(N)]
    for i in xrange(M):
        Q[X[i]-1].append(Y[i])
    return iter_tree_traversal(N, children, L, H, Q)

MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, log_drivin_hirin())
