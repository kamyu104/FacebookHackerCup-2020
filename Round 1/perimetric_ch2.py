# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Round 1 - Problem A. Perimetric - Chapter 2
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-1/problems/A2
#
# Time:  O(NlogN)
# Space: O(N)
#

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

    def __init__(self, end=float("inf"), can_duplicated=False):
        seed(0)
        self.__head = SkipNode()
        self.__len = 0
        self.__can_duplicated = can_duplicated
        self.add(end)
    
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
            while curr.nexts[i] and curr.nexts[i].val < val:
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

def process_rect(left, right, h, intervals, P, accu):
    it = intervals.lower_bound((left, float("-inf"))).prevs[0]
    if it.val[1] < left:
        it = it.nexts[0]
    left = min(left, it.val[0])
    while it.val[0] <= right:
        right = max(right, it.val[1])
        accu -= 2*(it.val[1]-it.val[0]+h)
        it, to_delete = it.nexts[0], it
        intervals.remove(to_delete.val)
    accu += 2*(right-left+h)  # add full perimeter
    P.append(accu)
    intervals.add((left, right))
    return accu

def perimetric_ch1():
    N, K = map(int, raw_input().strip().split())
    L = map(int, raw_input().strip().split())
    A_L, B_L, C_L, D_L = map(int, raw_input().strip().split())
    for _ in xrange(K, N):
        L.append((A_L*L[-2] + B_L*L[-1] + C_L) % D_L + 1)
    W = map(int, raw_input().strip().split())
    A_W, B_W, C_W, D_W = map(int, raw_input().strip().split())
    for _ in xrange(K, N):
        W.append((A_W*W[-2] + B_W*W[-1] + C_W) % D_W + 1)
    H = map(int, raw_input().strip().split())
    A_H, B_H, C_H, D_H = map(int, raw_input().strip().split())
    for _ in xrange(K, N):
        H.append((A_H*H[-2] + B_H*H[-1] + C_H) % D_H + 1)

    P, intervals, accu = [], SkipList(end=(float("inf"), float("inf"))), 0
    intervals.add((float("-inf"), float("-inf")))
    for i in xrange(N):
        accu = process_rect(L[i], L[i]+W[i], H[i], intervals, P, accu)
    return reduce(lambda x, y: (x*y)%MOD, P)

MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, perimetric_ch1())
