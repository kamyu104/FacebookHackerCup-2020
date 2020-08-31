# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Round 2 - Problem A. Ca-pasta-ty
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-2/problems/A
#
# Time:  O(N)
# Space: O(1)
#

def read(K, N):
    X = map(int, raw_input().strip().split())
    A, B, C, D = map(int, raw_input().strip().split())
    for _ in xrange(K, N):
        X.append((A*X[-2] + B*X[-1] + C) % D)
    return X

def capastaty():
    N, K = map(int, raw_input().strip().split())
    S, X, Y = [read(K, N) for _ in xrange(3)]

    add_left, add_right, remove_left, remove_right = 0, 0, 0, 0
    for i in xrange(N):
        add_left += max(X[i]-S[i], 0)
        add_right += max((X[i]+Y[i])-S[i], 0)
        remove_left += max(S[i]-(X[i]+Y[i]), 0)
        remove_right += max(S[i]-X[i], 0)
    if not (add_left <= remove_right and remove_left <= add_right):
        return -1
    return max(add_left, remove_left)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, capastaty())
