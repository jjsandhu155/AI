# Final Sliding Puzzles 3

import sys
import time
from heapq import heappush, heappop

size = 4
goal = 'ABCDEFGHIJKLMNO.'


def submission_test():
    with open(sys.argv[1]) as f:
        puzzles = [line.strip() for line in f]
    total = 0.0000
    for i in range(len(puzzles)):
        solv_start = time.perf_counter()
        solvable = is_solvable(puzzles[i])
        solv_end = time.perf_counter()
        parity_time = str(solv_end - solv_start)
        if solvable:
            start = time.perf_counter()
            a_depth = a_star(puzzles[i])
            end = time.perf_counter()
            a_dfs_time = str(end - start)
            total += float(a_dfs_time)
            print('Line %d: %s, A* - %d moves in %s seconds' %
                  (i, puzzles[i], a_depth, a_dfs_time))
        else:
            total += float(parity_time)
            print('Line %d: %s, A* - no solution in %s seconds' % (i, puzzles[i], parity_time))
        print()
    print('Total Time %s' % total)


def test_linear_conflicts():
    with open('long.txt') as f:
        puzzles = [line.strip() for line in f]
    for p in puzzles:
        print(p, str(linear_conflicts(p)))


def comparison_test():
    with open('long.txt') as f:
        puzzles = [line.strip() for line in f]
    total = 0.0000
    for i in range(len(puzzles)):
        solv_start = time.perf_counter()
        solvable = is_solvable(puzzles[i])
        solv_end = time.perf_counter()
        parity_time = str(solv_end - solv_start)
        if solvable:
            start = time.perf_counter()
            a_depth = a_star(puzzles[i])
            end = time.perf_counter()
            a_dfs_time = str(end - start)
            total += float(a_dfs_time)
            print('Line %d: %s, A* - %d moves in %s seconds' %
                  (i, puzzles[i], a_depth, a_dfs_time))
        else:
            total += parity_time
            print('Line %d: %s, A* - no solution in %s seconds' % (i, puzzles[i], parity_time))
        print()
    print('Total Time %s' % total)


def get_size(board):
    return int(len(board) ** (1 / 2))


def find_goal(str_b):
    return ''.join(sorted(str_b[0:str_b.index('.')] + str_b[str_b.index('.') + 1:])) + '.'


def goal_test(board):
    return True if board == find_goal(board) else False


def get_children(og_state):
    if og_state:
        index = og_state.index('.')
        wid = get_size(og_state)
        length = len(og_state)
        if index in {0, wid - 1, length - wid, length - 1}:
            if index == 0:
                return [(og_state[1] + og_state[0] + og_state[2:]), (og_state[wid] + og_state[1:wid] + og_state[0] + og_state[wid + 1:])]
            if index == wid - 1:
                return [(og_state[0:wid - 2] + og_state[wid - 1] + og_state[wid - 2] + og_state[wid:]), (og_state[0:wid - 1] + og_state[(2 * wid) - 1] + og_state[wid:(2 * wid) - 1] + og_state[wid - 1] + og_state[(2 * wid):])]
            if index == length - wid:
                return [(og_state[0:length-wid-wid] + og_state[length - wid] + og_state[length-wid-wid+1:length - wid] + og_state[length-wid-wid] + og_state[length - wid+ 1:]), (og_state[0:length - wid] + og_state[length - wid + 1] + og_state[length - wid] + og_state[length - wid + 2:])]
            if index == length - 1:
                return [(og_state[0:length - 2] + og_state[length - 1] + og_state[length - 2]), (og_state[0:length - 1 - wid] + og_state[length - 1] + og_state[length - wid: length - 1] + og_state[length - wid - 1])]
        top, bottom, left, right = ([a for a in range(1, wid - 1)], [a for a in range(length - wid, length - 1)], [i for i in range(length) if i %
                                                                                                                   wid == 0 and i not in {0, length - wid}], [i for i in range(length) if i % wid == wid - 1 and i not in {wid - 1, length - 1}])
        edges = top + bottom + left + right
        if index in edges:
            if index in top:
                return [(og_state[0:index] + og_state[index + 1] + og_state[index] + og_state[index + 2:]), (og_state[0:index - 1] + og_state[index] + og_state[index - 1] + og_state[index + 1:]), (og_state[0:index] + og_state[index + wid] + og_state[index + 1:index + wid] + og_state[index] + og_state[index + wid + 1:])]
            # left, right, bottom
            if index in bottom:
                return [(og_state[0:index] + og_state[index + 1] + og_state[index] + og_state[index + 2:]), (og_state[0:index - 1] + og_state[index] + og_state[index - 1] + og_state[index + 1:]), (og_state[0:index - wid] + og_state[index] + og_state[index - wid + 1:index] + og_state[index - wid] + og_state[index + 1:])]  # left, right, top
            if index in left:
                # up, down, right
                return [(og_state[0:index - wid] + og_state[index] + og_state[index - wid + 1:index] + og_state[index - wid] + og_state[index + 1:]), (og_state[0:index] + og_state[index + wid] + og_state[index + 1:index + wid] + og_state[index] + og_state[index + wid + 1:]), (og_state[0:index] + og_state[index + 1] + og_state[index] + og_state[index + 2:])]
            if index in right:
                return [(og_state[0:index - wid] + og_state[index] + og_state[index - wid + 1:index] + og_state[index - wid] + og_state[index + 1:]), (og_state[0:index] + og_state[index + wid] + og_state[index + 1:index + wid] + og_state[index] + og_state[index + wid + 1:]), (og_state[0:index - 1] + og_state[index] + og_state[index - 1] + og_state[index + 1:])]  # up, down, left
        else:
            return [(og_state[0:index] + og_state[index + 1] + og_state[index] + og_state[index + 2:]), (og_state[0:index - 1] + og_state[index] + og_state[index - 1] + og_state[index + 1:]), (og_state[0:index] + og_state[index + wid] + og_state[index + 1:index + wid] + og_state[index] + og_state[index + wid + 1:]), (og_state[0:index - wid] + og_state[index] + og_state[index - wid + 1:index] + og_state[index - wid] + og_state[index + 1:])]


def is_solvable(board):
    unordered = num_unordered(board)
    row = int(board.index('.') / size) + 2
    if size % 2 != 0:
        if unordered % 2 == 0:
            return True
        else:
            return False
    else:
        if row % 2 == 0:
            if unordered % 2 != 0:
                return True
            else:
                return False
        else:
            if unordered % 2 == 0:
                return True
            else:
                return False


def num_unordered(board):
    count = 0
    board = board.replace('.', '')
    for i in range(len(board)):
        for i2 in range(i + 1, len(board)):
            if board[i] > board[i2]:
                count += 1
    return count


def a_star(start_state):
    """
    When you generate children, add in code that runs linear_conflicts on the parent (again, I know) and the child.  (This will obviously slow things down a little bit.)
    Then, compare the two.  The difference between the heuristic value for parent and child should be precisely 1 or -1.
    If any other number is found, print the parent state, the child state, and the difference.
    :param start_state:
    :return:
    """
    closed = set()
    start_node = (linear_conflicts(start_state), 0, start_state)
    fringe = []
    heappush(fringe, start_node)
    while fringe:
        v = heappop(fringe)
        v_f, v_depth, v_state = v
        if v_state == goal:
            return v_depth
        if v_state not in closed:
            closed.add(v_state)
            for c in get_children(v_state):
                # if (linear_conflicts(v_state) - linear_conflicts(c)) not in {-1,1}:
                #     print('Error!', 'Parent:', v_state, 'Child:', c, 'Difference:', linear_conflicts(v_state) - linear_conflicts(c))
                if c not in closed:
                    temp = (v_depth + 1 + 1.001 * linear_conflicts(c), v_depth + 1, c)
                    heappush(fringe, temp)
    return None


def taxicab(board):
    res = 0
    for i in range(16):
        if board[i] != '.' and board[i] != goal[i]:
            ci = goal.index(board[i])
            y = (i // size) - (ci // size)
            x = (i % size) - (ci % size)
            res += abs(y) + abs(x)
    return res


def linear_conflicts(board):
    def line_conflict(line, solved_line, size, cost=0):
        conflict_additions = [0 for x in range(size)]
        for i, l1 in enumerate(line):
            if l1 in solved_line and l1 != '.':
                for j, l2 in enumerate(line):
                    if l2 in solved_line and l2 != '.':
                        if l1 != l2:
                            if (solved_line.index(l1) > solved_line.index(l2)) and i < j:
                                conflict_additions[i] += 1
                            if (solved_line.index(l1) < solved_line.index(l2)) and i > j:
                                conflict_additions[i] += 1
        if max(conflict_additions) == 0:
            return cost * 2
        else:
            i = conflict_additions.index(max(conflict_additions))
            line[i] = -1
            cost += 1
            return line_conflict(line, solved_line, size, cost)

    res = taxicab(board)
    rows = [[] for y in range(size)]
    columns = [[] for x in range(size)]
    solved_rows = [[] for y in range(size)]
    solved_columns = [[] for x in range(size)]
    for y in range(size):
        for x in range(size):
            idx = (y * size) + x
            rows[y].append(board[idx])
            columns[x].append(board[idx])
            solved_rows[y].append(goal[idx])
            solved_columns[x].append(goal[idx])
    for i in range(size):
        res += line_conflict(rows[i], solved_rows[i], size)
    for i in range(size):
        res += line_conflict(columns[i], solved_columns[i], size)
    return res


# submission_test()
comparison_test()
