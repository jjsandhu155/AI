# Modeling Tasks -- Sliding Puzzles -- [9/22-9/30]
import time
from collections import deque
import sys

tf = sys.argv[1]


def get_size(board):
    return int(len(board) ** (1/2))


def print_puzzle(size, str_b):
    for i in range(size):
        print(' '.join(str_b[0:size]))
        str_b = str_b[size:]


def find_goal(str_b):
    return ''.join(sorted(str_b[0:str_b.index('.')] + str_b[str_b.index('.')+1:])) + '.'


def goal_test(board):
    return True if board == find_goal(board) else False


def get_children(og_state):
    if og_state:
        index = og_state.index('.')
        wid = get_size(og_state)
        length = len(og_state)
        if index in {0, wid - 1, length - wid, length - 1}:
            if index == 0:
                return [(og_state[1] + og_state[0] + og_state[2:]), (og_state[wid] + og_state[1:wid] + og_state[0] + og_state[wid+1:])]
            if index == wid - 1:
                return [(og_state[0:wid-2] + og_state[wid-1] + og_state[wid-2] + og_state[wid:]), (og_state[0:wid-1] + og_state[(2*wid)-1] + og_state[wid:(2*wid)-1] + og_state[wid-1] + og_state[(2*wid):])]
            if index == length - wid:
                return [(og_state[0:wid] + og_state[length-wid] + og_state[wid+1:length-wid] + og_state[wid] + og_state[length-wid+1:]), (og_state[0:length-wid] + og_state[length-wid+1] + og_state[length-wid] + og_state[length-wid+2:])]
            if index == length - 1:
                return [(og_state[0:length-2] + og_state[length-1] + og_state[length-2]), (og_state[0:length-1-wid] + og_state[length-1] + og_state[length - wid: length-1] + og_state[length-wid-1])]
        top, bottom, left, right = ([a for a in range(1, wid-1)], [a for a in range(length-wid, length-1)], [i for i in range(length) if i %
                                                                                                             wid == 0 and i not in {0, length-wid}], [i for i in range(length) if i % wid == wid - 1 and i not in {wid-1, length-1}])
        edges = top + bottom + left + right
        if index in edges:
            if index in top:
                return [(og_state[0:index] + og_state[index + 1] + og_state[index] + og_state[index+2:]), (og_state[0:index-1] + og_state[index] + og_state[index-1] + og_state[index+1:]), (og_state[0:index] + og_state[index+wid] + og_state[index+1:index+wid] + og_state[index] + og_state[index + wid + 1:])]
            # left, right, bottom
            if index in bottom:
                return [(og_state[0:index] + og_state[index + 1] + og_state[index] + og_state[index+2:]), (og_state[0:index-1] + og_state[index] + og_state[index-1] + og_state[index+1:]), (og_state[0:index-wid] + og_state[index] + og_state[index-wid+1:index] + og_state[index-wid] + og_state[index + 1:])]  # left, right, top
            if index in left:
                # up, down, right
                return [(og_state[0:index-wid] + og_state[index] + og_state[index-wid+1:index] + og_state[index-wid] + og_state[index + 1:]), (og_state[0:index] + og_state[index+wid] + og_state[index+1:index+wid] + og_state[index] + og_state[index + wid + 1:]), (og_state[0:index] + og_state[index + 1] + og_state[index] + og_state[index+2:])]
            if index in right:
                return [(og_state[0:index-wid] + og_state[index] + og_state[index-wid+1:index] + og_state[index-wid] + og_state[index + 1:]), (og_state[0:index] + og_state[index+wid] + og_state[index+1:index+wid] + og_state[index] + og_state[index + wid + 1:]), (og_state[0:index-1] + og_state[index] + og_state[index-1] + og_state[index+1:])]  # up, down, left
        else:
            return [(og_state[0:index] + og_state[index + 1] + og_state[index] + og_state[index+2:]), (og_state[0:index-1] + og_state[index] + og_state[index-1] + og_state[index+1:]), (og_state[0:index] + og_state[index+wid] + og_state[index+1:index+wid] + og_state[index] + og_state[index + wid + 1:]), (og_state[0:index-wid] + og_state[index] + og_state[index-wid+1:index] + og_state[index-wid] + og_state[index + 1:])]


def gen_children(start):
    fringe = deque()
    visited = set()
    fringe.append(start)
    visited.add(start)
    while fringe:
        for c in get_children(fringe.pop()):
            if c not in visited:
                fringe.append(str(c))
                visited.add(str(c))
    return len(visited)


def find_path(given):
    fringe = deque()
    visited = set()
    if goal_test(given):
        return ([], 0)
    fringe.append((given, [given]))
    visited.add(given)
    while fringe:
        v, path = fringe.popleft()
        if goal_test(v):
            return (path, len(path) - 1)
        for c in get_children(v):
            if c not in visited:
                fringe.append((c, path + [c]))
                visited.add(c)
    return None


with open(tf) as f:
    count = 1
    for line in f:
        str_b = line.split()[1]
        start = time.perf_counter()
        path, length = find_path(str_b)
        end = time.perf_counter()
        timer = end - start
        print('Line %d: %s, %d moves found in %s seconds' %
              (count, str_b, length, timer))
        count = count + 1


# print(hard8('12345678.'))
# Step 3 Output
# with open(tf) as f:
#     count = 1
#     for line in f:
#         size, str_b = (line.split()[0], line.split()[1])
#         print("Line %d start state:" % (count))
#         print_puzzle(int(size), str_b)
#         print()
#         print("Line %d goal state:" % (count), end=' ')
#         print(find_goal(str_b))
#         print()
#         print("Line %d children:" % (count), get_children(str_b))
#         print()
#         count = count + 1
"""
Psuedo Code
function BFS(start-node):
    fringe = new Queue()
    visited = new Set()
    fringe.add(start-node)
    visited.add(start-node)
    while fringe is not empty do:
        v = fringe.pop()
        if GoalTest(v) then:
            return v
        for every child c of v do:
            if c not in visited then:
            fringe.add(c)
            visited.add(c)
    return None
"""
