# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Round 2 - Problem B. Elimination
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-2/problems/B
#
# Time:  O((N * M + E) * log(N * M)) = O((N * M + E) * (logN + logM)), pass in PyPy2 but Python2
# Space: O(N * M)
#

from itertools import izip
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

    def __init__(self, end=float("-inf"), can_duplicated=True):
        seed(0)
        self.__head = SkipNode()
        self.__len = 0
        self.__can_duplicated = can_duplicated
        self.add(end)

    def begin(self):
        return self.__head.nexts[0]

    def lower_bound(self, target):
        return self.__lower_bound(target, self.__find_prev_nodes(target))

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

    def __find_prev_nodes(self, val):
        prevs = [None]*len(self.__head.nexts)
        curr = self.__head
        for i in reversed(xrange(len(self.__head.nexts))):
            while curr.nexts[i] and curr.nexts[i].val > val:
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

def read(K, N, M):
    X = map(int, raw_input().strip().split())
    A, B, C = map(int, raw_input().strip().split())
    for _ in xrange(K, N):
        X.append((A*X[-2] + B*X[-1] + C) % M)
    return X

def max_weight(circle_weights, i):
    return circle_weights[i].begin().val

def max_delta_weight(circle_weights, half_circle_weights, i):
    return half_circle_weights[i][0].begin().val+half_circle_weights[i][1].begin().val-circle_weights[i].begin().val

def group(X, Y, i, j):
    return 0 if X[i] <= j < Y[i] else 1

def update(s, v1, v2):
    s.remove(v1)
    s.add(v2)

def update_circle_edge(X, Y, circle_weights, half_circle_weights, circle_delta_weights, i, j, w1, w2):
    r1, d1 = max_weight(circle_weights, i), max_delta_weight(circle_weights, half_circle_weights, i)
    update(circle_weights[i], w1, w2), update(half_circle_weights[i][group(X, Y, i, j)], w1, w2)
    r2, d2 = max_weight(circle_weights, i), max_delta_weight(circle_weights, half_circle_weights, i)
    update(circle_delta_weights, d1, d2)
    return r2-r1

def circular_circles():
    N, M, E, K = map(int, raw_input().strip().split())
    X = read(K, N, M)
    Y = read(K, N, M)
    I = read(K, E, N*M + N)
    W = read(K, E, 10**9)

    weights = [1]*(M*N + N)
    circle_weights = [SkipList() for _ in xrange(N)]
    half_circle_weights = [[SkipList() for _ in xrange(2)] for _ in xrange(N)]
    circle_delta_weights, inter_circle_weights = SkipList(), SkipList()
    for i in xrange(N):
        if X[i] > Y[i]:
            X[i], Y[i] = Y[i], X[i]
        for j in xrange(len(half_circle_weights[i])):
            half_circle_weights[i][j].add(0)
        for j in xrange(M):
            circle_weights[i].add(1)
            half_circle_weights[i][group(X, Y, i, j)].add(1)
        circle_delta_weights.add(max_delta_weight(circle_weights, half_circle_weights, i))
        inter_circle_weights.add(1)

    result, total, top1_sum = 1, N*M+N, N
    for j, w2 in izip(I, W):
        w1, weights[j]  = weights[j], w2
        total += w2-w1
        if j < N*M:
            top1_sum += update_circle_edge(X, Y, circle_weights, half_circle_weights, circle_delta_weights, j//M, j%M, w1, w2)
        else:
            update(inter_circle_weights, w1, w2)
        curr = (total-top1_sum-max(circle_delta_weights.begin().val, inter_circle_weights.begin().val)) % MOD
        result = result*curr % MOD
    return result

MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, circular_circles())
