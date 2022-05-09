# Sliding Puzzles Part 2 -- 10/11
import sys
import time
from heapq import heappush, heappop


def old_code_test():  # Line 19: AIBCFOGD.EKHMJNL, 18 moves found in 27.131812431999997 seconds
    with open(sys.argv[1]) as f:
        count = 1
        for line in f:
            start = time.perf_counter()
            path, length = find_path(line.strip())
            end = time.perf_counter()

            timer = end - start
            print('Line %d: %s, %d moves found in %s seconds' %
                  (count, line.strip(), length, timer))
            count = count + 1


def get_size(board):
    return int(len(board) ** (1 / 2))


def print_puzzle(size, str_b):
    for i in range(size):
        print(' '.join(str_b[0:size]))
        str_b = str_b[size:]


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
                return [(og_state[0:wid] + og_state[length - wid] + og_state[wid + 1:length - wid] + og_state[wid] + og_state[length - wid + 1:]), (og_state[0:length - wid] + og_state[length - wid + 1] + og_state[length - wid] + og_state[length - wid + 2:])]
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


def find_path(given):
    fringe = deque()
    visited = {given}
    if goal_test(given):
        return [], 0
    fringe.append((given, [given]))
    while fringe:
        v, path = fringe.popleft()
        if goal_test(v):
            return path, len(path) - 1
        for c in get_children(v):
            if c not in visited:
                fringe.append((c, path + [c]))
                visited.add(c)
    return None


def is_solvable(board):
    unordered = num_unordered(board)
    size = get_size(board)
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


def k_dfs(start_state, k):
    fringe = []
    an = set()
    an.add(start_state)
    start_node = (start_state, 0, an)
    fringe.append(start_node)
    while fringe:
        v = fringe.pop()
        v_state, v_depth, v_ancestors = v
        if goal_test(v_state):
            return v
        if v_depth < k:
            for c in get_children(v_state):
                if c not in v_ancestors:
                    t_anc = v_ancestors.copy()
                    t_anc.add(c)
                    temp = (c, v_depth + 1, t_anc)
                    fringe.append(temp)
    return None


def id_dfs(start_state):
    max_depth = 0
    result = None
    while result is None:
        result = k_dfs(start_state, max_depth)
        max_depth = max_depth + 1
    return result


def taxicab(board):
    taxi, temp1, temp2, taxi_dist = (0, None, None, 0)
    grid_board = to_grid(board)
    goal_state = find_goal(board)
    grid_solved = to_grid(goal_state)
    for i in range(len(grid_board)):
        if grid_board[i][0] != '.':
            temp1 = grid_board[i][1:]
            temp2 = grid_solved[goal_state.index(grid_board[i][0])][1:]
            taxi += abs(temp1[0] - temp2[0]) + abs(temp1[1] - temp2[1])
    return taxi


def to_grid(board):
    griddy = []
    index = 0
    size = get_size(board)
    for x in range(1, size + 1):
        for y in range(1, size + 1):
            griddy.append((board[index], x, y))
            index += 1
    return griddy


def a_star(start_state):
    closed = set()
    start_node = (taxicab(start_state), 0, start_state)
    fringe = []
    heappush(fringe, start_node)
    while fringe:
        v = heappop(fringe)
        v_f, v_depth, v_state = v
        if goal_test(v_state):
            return v
        if v_state not in closed:
            closed.add(v_state)
            for c in get_children(v_state):
                if c not in closed:
                    temp = (v_depth + 1 + taxicab(c), v_depth + 1, c)
                    heappush(fringe, temp)
    return None


def sliding_2_test():
    with open(sys.argv[1]) as f:
        puzzles = [line.strip().split() for line in f]
    yeeton = time.perf_counter()
    for index in range(len(puzzles)):
        size, board, alg = puzzles[index]
        start = time.perf_counter()
        solvable = is_solvable(board)
        end = time.perf_counter()
        parity_time = str(end - start)
        if solvable:
            if alg == 'B':
                start = time.perf_counter()
                bfs_path, bfs_length = find_path(board)
                end = time.perf_counter()
                bfs_time = str(end - start)
                print('Line %d: %s, BFS - %d moves in %s seconds' %
                      (index, board, bfs_length, bfs_time))
                print()
            if alg == 'I':
                start = time.perf_counter()
                id_state, id_length, id_ancestors = id_dfs(board)
                end = time.perf_counter()
                id_time = str(end - start)
                print('Line %d: %s, ID-DFS - %d moves in %s seconds' %
                      (index, board, id_length, id_time))
                print()
            if alg == 'A':
                start = time.perf_counter()
                a_f, a_depth, a_state = a_star(board)
                end = time.perf_counter()
                a_time = str(end - start)
                print('Line %d: %s, A* - %d moves in %s seconds' %
                      (index, board, a_depth, a_time))
                print()
            if alg == '!':
                start = time.perf_counter()
                bfs_path, bfs_length = find_path(board)
                end = time.perf_counter()
                bfs_time = str(end - start)
                print('Line %d: %s, BFS - %d moves in %s seconds' %
                      (index, board, bfs_length, bfs_time))
                start = time.perf_counter()
                id_state, id_length, id_ancestors = id_dfs(board)
                end = time.perf_counter()
                id_time = str(end - start)
                print('Line %d: %s, ID-DFS - %d moves in %s seconds' %
                      (index, board, id_length, id_time))
                start = time.perf_counter()
                a_f, a_depth, a_state = a_star(board)
                end = time.perf_counter()
                a_time = str(end - start)
                print('Line %d: %s, A* - %d moves in %s seconds' %
                      (index, board, a_depth, a_time))
                print()
        else:
            print('Line %d: %s, no solution determined in %s seconds' %
                  (index, board, parity_time))
            print()
    skeeton = time.perf_counter()
    print(str(skeeton - yeeton))


def sliding_3_test():
    with open(sys.argv[1]) as f:
        puzzles = [line.strip() for line in f]
    total = 0.0000
    for i in range(len(puzzles)):
        start = time.perf_counter()
        a_f, a_depth, a_state = a_star(puzzles[i])
        end = time.perf_counter()
        a_dfs_time = str(end - start)
        total += float(a_dfs_time)
        print('Line %d: %s, A* - %d moves in %s seconds' %
              (i, puzzles[i], a_depth, a_dfs_time))
        print()
    print('Total Time %s' % total)
def comparison_test():
    with open('15_puzzles.txt') as f:
        puzzles = [line.strip() for line in f]
    total = 0.0000
    for i in range(41):
        start = time.perf_counter()
        a_f, a_depth, a_state = a_star(puzzles[i])
        end = time.perf_counter()
        a_dfs_time = str(end - start)
        total += float(a_dfs_time)
        print('Line %d: %s, A* - %d moves in %s seconds' %
              (i, puzzles[i], a_depth, a_dfs_time))
        print()
    print('Total Time %s' % total)

comparison_test()

