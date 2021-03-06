# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Round 3 - Problem C. Mail Security
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-3/problems/C
#
# Time:  O((N + M) * (logN + logM)^2), pass in PyPy2 but Python2
# Space: O(N + M)
#

from functools import partial
from random import randint, seed

# Template modified from:
# https://github.com/kamyu104/LeetCode-Solutions/blob/master/Python/design-skiplist.py
class SkipNode(object):
    def __init__(self, level=0, val=None):
        self.val = val
        self.nexts = [None]*level
        self.prevs = [None]*level

class SkipList(object):
    P_NUMERATOR, P_DENOMINATOR = 1, 2  # P = 1/4 in redis implementation
    MAX_LEVEL = 32  # enough for 2^32 elements

    def __init__(self, end=(float("inf"), float("inf")), can_duplicated=True):
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

def binary_search_right(left, right, check):
    while left <= right:
        mid = left + (right-left)//2
        if not check(mid):
            right = mid-1
        else:
            left = mid+1
    return right

def read(K, N):
    X = map(int, raw_input().strip().split())
    A, B, C, D = map(int, raw_input().strip().split())
    for i in xrange(K, N):
        X.append((A*X[-2] + B*X[-1] + C) % D + 1)
    return X

def check(S, P, X, val):
    objects = []
    for i in reversed(xrange(len(S))):
        if len(objects) < val or S[i] >= X:
            objects.append((S[i], True))
    box_count = len(objects)
    for i in xrange(val):
        objects.append((P[i], False))
    objects.sort(reverse=True)
    ordered_set = SkipList()
    key_count = 0
    for capacity, is_box in objects:
        if is_box:
            key_count += capacity//X
            ordered_set.add((capacity%X, capacity))
            continue
        if not ordered_set:
            return False
        # minimize the lost of key_count, key_count would be lost floor(capacity/X) if box_capacity%X >= capacity%X, otherwise floor(capacity/X)+1
        it = ordered_set.lower_bound((capacity%X, 0))  # yield the min of box_capacity%X s.t. box_capacity%X >= capacity%X to greedily keep more choices of ordered_set
        if it == ordered_set.end():
            it = ordered_set.begin()  # if not exist, yield the smallest box_capacity%X to greedily keep more choices of ordered_set
        box_capacity = it.val[1]
        ordered_set.remove(it)
        key_count += (box_capacity-capacity)//X - box_capacity//X
    return key_count+1 >= box_count

def mail_security():
    N, M, K, X = map(int, raw_input().strip().split())
    S = read(K, N)
    P = read(K, M)
    S.sort()
    P.sort()
    return binary_search_right(0, min(N, M), partial(check, S, P, X))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, mail_security())
