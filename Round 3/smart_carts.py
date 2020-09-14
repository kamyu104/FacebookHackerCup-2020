# Copyright (c) 2020 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2020 Round 3 - Problem D. Smart Carts
# https://www.facebook.com/codingcompetitions/hacker-cup/2020/round-3/problems/D
#
# Time:  O(N^3), pass in PyPy2 but Python2
# Space: O(N)
#

def query0(line_count, parent, target_line_cap, initial_max_count):  # Time: O(1)
    for i in xrange(2):
        if line_count[A][i] > target_line_cap[i]:
            return -1
    return initial_max_count

def precompute_for_query1(N, parent, pos, seq, line_count, c):  # Time: O(N^2)
    def is_free(i, has_non_free_but_accessible):
        j, p = pos[A][i]
        return p > line_count[A][j]-free_count[j]-has_non_free_but_accessible

    free_count = [min(c-line_count[A][1-i], line_count[A][i]) for i in xrange(2)]
    possible_max_count = sum(parent[A][i] == parent[B][i] or (is_free(i, 0) and is_free(parent[B][i], 1)) for i in xrange(N))
    fixed_line_count, possible_sum_of_free_chain_length_set = [0]*2, 1
    for i in xrange(2):
        seq_B_i = seq[B][i]
        curr_free_chain_length, fixed_line = 0, -1
        for j in xrange(len(seq_B_i)):
            if not is_free(seq_B_i[j], 0):
                continue
            curr_free_chain_length += 1
            if curr_free_chain_length == 1 and j and is_free(seq_B_i[j-1], 1):
                fixed_line = pos[A][seq_B_i[j-1]][0]
            if j+1 == len(seq_B_i) or not is_free(seq_B_i[j+1], 0):
                if fixed_line < 0:
                    possible_sum_of_free_chain_length_set |= (possible_sum_of_free_chain_length_set << curr_free_chain_length)  # O(N^2) time in total
                else:
                    fixed_line_count[fixed_line] += curr_free_chain_length
                curr_free_chain_length, fixed_line = 0, -1
    possible_sum_of_free_chain_length, i = [], 0
    while possible_sum_of_free_chain_length_set:
        possible_sum_of_free_chain_length_set, has = divmod(possible_sum_of_free_chain_length_set, 2)
        if has:
            possible_sum_of_free_chain_length.append(i)
        i += 1
    return [possible_max_count, free_count, fixed_line_count, possible_sum_of_free_chain_length, 0]

def query1(line_count, target_line_cap, args):  # amortized time: O(1)
    possible_max_count, free_count, fixed_line_count, possible_sum_of_free_chain_length, idx = args
    space = [target_line_cap[i] - (line_count[A][i]-free_count[i]) - fixed_line_count[i] for i in xrange(2)]
    if min(space[0], space[1]) < 0:
        return possible_max_count-1  # not enough space, a chain should be splitted and one cart is not satisfied
    while idx+1 < len(possible_sum_of_free_chain_length) and possible_sum_of_free_chain_length[idx+1] <= space[0]:
        idx += 1  # O(N) time in total during O(N^2) (x, y) pair loops 
    args[-1] = idx  # save the state of idx
    if possible_sum_of_free_chain_length[-1] - possible_sum_of_free_chain_length[idx] > space[1]:
        return possible_max_count-1  # not enough space, a chain should be splitted and one cart is not satisfied
    return possible_max_count  # all free cart chains could be packed into the lines

def query2(N, line_count, target_line_cap):  # Time: O(1)
    for i in xrange(2):
        if line_count[B][i] > target_line_cap[i]:
            return N-1  # not enough space, a chain should be splitted and one cart is not satisfied
    return N  # all free cart chains could be packed into the lines

def query(N, parent, line_count, initial_max_count, d, c, x, y, args):  # amortized time: O(1)
    target_line_cap = [min(c, x), min(c, y)]
    for i in xrange(2):
        if line_count[A][i] > c:
            return -1
    if target_line_cap[0] + target_line_cap[1] < N:
        return -1
    if d == 0:
        return query0(line_count, parent, target_line_cap, initial_max_count)
    if d == 1:
        return query1(line_count, target_line_cap, args)
    return query2(N, line_count, target_line_cap)

def smart_carts():
    N = input()
    parent, child = [[-1]*N for _ in xrange(2)], [[-1]*(N+2) for _ in xrange(2)]
    for i in xrange(N):
        parent[A][i], parent[B][i] = map(int, raw_input().strip().split())
        for config in [A, B]:
            parent[config][i] -= 1
            child[config][parent[config][i]] = i
    line_count = [[0]*2 for _ in xrange(2)]
    pos = [[None for _ in xrange(N+2)] for _ in xrange(2)]
    seq = [[[] for _ in xrange(2)] for _ in xrange(2)]
    for config in [A, B]:
        for i in xrange(2):
            j = N+i
            while j >= 0:
                pos[config][j] = (i, len(seq[config][i]))
                seq[config][i].append(j)
                j = child[config][j]
            line_count[config][i] = len(seq[config][i])-1
    initial_max_count = sum(parent[A][i] == parent[B][i] for i in xrange(N))
    G, args = [0]*(N+2), []
    for d in xrange(min(N+1, 3)):
        for c in xrange(N+1):
            if d == 1:
                args = precompute_for_query1(N, parent, pos, seq, line_count, c)  # Time: O(N^2)
            for x in xrange(N+1):  # Time: O(N^2) loops and each query costs amortized O(1)
                for y in xrange(N+1):
                    # given (c, x, y), for any d >= 2, the result v of query is the same, thus increase count by N-1
                    G[query(N, parent, line_count, initial_max_count, d, c, x, y, args)+1] += N-1 if d == 2 else 1
    return " ".join(map(str, G))

A, B = range(2)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, smart_carts())
