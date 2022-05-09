# Rush Hour Modeling Challenge 10/20

# Get Children
from collections import deque
from heapq import heappush, heappop, heapify
import sys
import time
print('Enter Your Board Below Using the Following Formatting:')
print('Represent Blanks as -')
print("Represent the Target Car as X's")
print('Represent any Blocking Car as Other Letters')


def call_input():
    grid = []
    for row_num in range(1, 7):
        row = list(input("Enter Row #%d Here:  " % row_num).replace(' ', ''))
        grid.append(row)
    return grid


def get_children(board):
    children = {}


def print_state(board):
    for r in board:
        for c in r:
            print(c, end=" ")
    print()


def goal_test(given):
    return


def find_path(given):
    fringe = deque()
    visited = {given}
    if goal_test(given):
        return ([], 0)
    fringe.append((given, [given]))
    while fringe:
        v, path = fringe.popleft()
        if goal_test(v):
            return path, len(path) - 1
        for c in get_children(v):  # For Graph Implementartion, graph[v]
            if c not in visited:
                fringe.append((c, path + [c]))
                visited.add(c)
    return None
