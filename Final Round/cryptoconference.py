# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Final Round - Problem A. Cryptoconference
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/final-round/problems/A
#
# Time:  O(NlogN)
# Space: O(N)
#

from random import randint, seed

# Template modified from:
# https://github.com/kamyu104/FacebookHackerCup-2020/blob/master/Round%203/mail_security.py
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

def count(it):
    a = it.val[0]+1
    it = it.nexts[0]
    b, c = it.val[0], it.val[1]-1
    v1, v2 = c-b, c-a
    return (v2+v1)*(v2-v1+1)//2

def insert(ordered_set, a, b):
    it = ordered_set.lower_bound((a, -1))
    if a <= it.val[0] <= it.val[1] <= b:
        return 0
    if it.val[0] > a:
        it = it.prevs[0]
    delta = 0
    while it.val[1] >= b:
        jt, it = it, it.prevs[0]
        delta -= count(jt) + count(it)
        ordered_set.remove(jt)
        delta += count(it)
    delta -= count(it)
    jt = ordered_set.add((a, b))[0]
    delta += count(it) + count(jt)
    return delta

def cryptoconference():
    N, K = map(int, raw_input().strip().split())

    ordered_set = SkipList()
    ordered_set.add((-1, -1))
    ordered_set.add((K, K+1))
    result, curr = 1, count(ordered_set.begin())
    for _ in xrange(N):
        S, D = map(int, raw_input().strip().split())
        curr += insert(ordered_set, S, S+D)
        result = result*(curr%MOD)%MOD
    return result

MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, cryptoconference())
