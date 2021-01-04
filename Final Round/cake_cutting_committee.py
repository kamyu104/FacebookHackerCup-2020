# Copyright (c) 2021 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Final Round - Problem F. Cake-Cutting Committee
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/final-round/problems/F
#
# Time:  O(N^2 * logN), pass in PyPy2 but Python2
# Space: O(N)
#

from itertools import izip

class SegmentTree(object):  # 0-based index
    def __init__(self, N,
                 build_fn=lambda x, y: [y]*(2*x),
                 query_fn=lambda x, y: y if x is None else max(x, y),
                 update_fn=lambda x, y: y if x is None else x+y,
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

    def update(self, L, R, h):  # Time: O(logN), Space: O(N)
        def pull(x):
            while x > 1:
                x //= 2
                assert(x*2 < len(self.tree))
                self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2+1])
                if self.lazy[x] is not None:
                    self.tree[x] = self.update_fn(self.tree[x], self.lazy[x])

        if L > R:
            return
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
    
    def __str__(self):
        showList = []
        for i in xrange(self.N):
            showList.append(self.query(i, i))
        return ",".join(map(str, showList))

def is_between(S, a, b, p):
    if b < a:
        b += 4*S
    if p < a:
        p += 4*S
    return a <= p <= b

def get_pos_after(S, a, p):
    if p < a:
        p += 4*S
    return p-a

def get_max_combined_c(S, N, C, P, h):
    base = 0
    ys, E = [], []
    for i in xrange(N):
        # full intersection?
        if (is_between(S, P[i][0], P[i][2], h[0]) or is_between(S, P[i][3], P[i][1], h[0])) and \
           (is_between(S, P[i][0], P[i][2], h[1]) or is_between(S, P[i][3], P[i][1], h[1])):
            base += C[i]
            continue
        # look for orientation of line segments such that at least one spans crosses from the 1st to the 2nd half
        for s in xrange(2):
            p = P[i][:]
            if s:
                p.reverse()
            # check which points are on their required halves
            bx, by = [0]*2, [0]*2
            for j in xrange(2):
                bx[j] = is_between(S, h[0], h[1], p[j*2])
                by[j] = is_between(S, h[1], h[0], p[j*2+1])
            # neither line segment is entirely valid?
            if (not bx[0] or not by[0]) and (not bx[1] or not by[1]):
                continue
            assert(bx[0]+by[0]+bx[1]+by[1] >= 3)  # other one must be at least half-valid
            # map points to positions on their halves
            x, y = [0]*2, [0]*2
            for j in xrange(2):
                x[j] = get_pos_after(S, h[0], p[j*2]) if bx[j] else (get_pos_after(S, h[0], h[1]) if j else 0)
                y[j] = -get_pos_after(S, h[1], p[j*2+1]) if by[j] else (0 if j else -get_pos_after(S, h[1], h[0]))
            assert(x[0] <= x[1] and y[0] <= y[1])
            E.append((x[0], y[0], y[1], C[i], 1))
            E.append((x[1], y[0], y[1], C[i], 0))
            ys.append(y[0]), ys.append(y[1])
            break
    # compress Y-coordinates
    lookup = {y:i for i, y in enumerate(sorted(set(ys)))}
    # line sweep
    st = SegmentTree(len(lookup))
    E.sort(key=lambda x: (x[0], not x[-1]))
    for _, y1, y2, c, s in E:
        y1, y2 = lookup[y1], lookup[y2]
        if s:  # left edge of a rectangle?
            st.update(y1, len(lookup)-1, c)
            continue
        # right edge of a rectangle
        st.update(y2, y2, st.query(y2, len(lookup)-1)-st.query(y2, y2))  # update y2 to max combined c in [y2, len(sorted_unique_ys)-1]
        st.update(y2+1, len(lookup)-1, -c)
    return base + st.query(0, len(lookup)-1)

def cake_cutting_committee():
    S, N = map(int, raw_input().strip().split())
    C = [0]*N
    P = [[0]*4 for _ in xrange(N)]
    for i in xrange(N):
        tmp = map(int, raw_input().strip().split())
        C[i] = tmp[0]
        for j, (x, y) in enumerate(izip(tmp[1::2], tmp[2::2])):  # number the positions in clockewise order around the edge of the square
            if not x:
                P[i][j] = y
            elif y == S:
                P[i][j] = S+x
            elif x == S:
                P[i][j] = 3*S-y
            else:  # y == 0
                P[i][j] = 4*S-x
        # normalize lines
        if is_between(S, P[i][1], P[i][0], P[i][2]):
            P[i][0], P[i][1] = P[i][1], P[i][0]
        if is_between(S, P[i][2], P[i][3], P[i][0]):
            P[i][2], P[i][3] = P[i][3], P[i][2]
    # consider all possible dividing lines
    result = 0
    for i in xrange(N):
        for j in xrange(2):
            result = max(result, get_max_combined_c(S, N, C, P, [P[i][j*2], P[i][j*2+1]]))
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, cake_cutting_committee())
