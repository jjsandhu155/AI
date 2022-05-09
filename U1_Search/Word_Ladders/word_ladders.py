# Word Ladders Main Code -- JJ Sandhu
# 10/5

import re
import sys
import time
from collections import deque

word_file, puzzle_file = (sys.argv[1], sys.argv[2])
alphabet = 'abcdefghijklmnopqrstuvwxyz'


def get_children_regular_expressions(word, words):  # attempt at using regular expressions: Turns out to be about 30 times slower
    words = " ".join(words)
    matches = []
    for i in range(len(word)):
        reg = word[:i] + '\w' + word[i + 1:]
        temp = re.findall(reg, words)
        for item in temp:
            if item != word:
                matches.append(item)
    return matches


def get_children(word, words):  # Generate Words 1 Letter Away
    children = set()
    for i in range(len(word)):
        for letter in alphabet:
            if letter != word[i]:
                temp = word[:i] + letter + word[i + 1:]
                if temp in words:
                    children.add(temp)
    return children


# Method to find the shortest path between two words moving 1 letter at a time
def find_path(graph, given, goal):
    fringe = deque()
    visited = {given}
    if given == goal:
        return [], 0
    fringe.append((given, [given]))
    while fringe:
        v, path = fringe.popleft()
        if v == goal:
            return path, len(path)
        for c in graph[v]:
            if c not in visited:
                fringe.append((c, path + [c]))
                visited.add(c)
    return None, None


def generate_structure():
    print()
    start = time.perf_counter()
    with open(word_file) as f:
        words = {line.strip() for line in f}
    graph = dict()
    for word in words:  # Creating an Undirected Adjacency Graph
        pos_childs = get_children(word, words)
        childs = {c for c in pos_childs}
        graph[word] = childs
    end = time.perf_counter()
    timer = str(end - start)
    print('Time to create the data structure was: %s' % timer)
    print('There are %d words in this dict.' % (len(graph)))
    print()
    return graph, timer


def generate_structure_efficiently():
    """
    Loop through each word in the wordlist ONCE (just O(n)) and built an intermediate dictionary where each key is a pattern and each value is all of the words that have matched that pattern (ie "atone*": {"atones", "atoned"})
    Loop through that intermediate dictionary, look at each set with size larger than 1, and add every word in it as a child of all the others
    atones matches *tones, a*ones, at*nes, etc

    :return: graph
    """

    print()
    start = time.perf_counter()
    graph = dict()
    graph2 = dict()
    graph3 = dict()
    word_set = set()
    with open(word_file) as f:
        for line in f:
            word = line.strip()
            word_set.add(word)
            if word in graph:
                pass
            else:
                graph[word] = set()
                for i in range(len(word)):
                    graph[word].add(word[:i] + '.' + word[i + 1:])

        for pattern in graph:
            for item in graph[pattern]:
                graph2[item] = set()

        for pattern in graph:
            for item in graph[pattern]:
                if item in graph2:
                    graph2[item].add(pattern)
    for group in graph2.values():
        if len(group) > 1:
            for item in group:
                graph3[item] = group.copy()
                graph3[item].remove(item)

    for key in graph2:
        if len(graph2[key]) >= 1:
            for item in graph2[key]:
                temp = graph2[key].copy()
                temp.remove(item)
                if item in graph3:
                    graph3[item] |= temp
                else:
                    graph3[item] = temp

    end = time.perf_counter()
    timer = str(end - start)
    print('Time to create the data structure was: %s' % timer)
    print('There are %d words in this dict.' % (len(graph)))
    print()
    return graph3, timer


def solve_puzzles():
    graph, timer = generate_structure_efficiently()
    with open(puzzle_file) as f:  # read in puzzles
        line_list = [line.strip().split() for line in f]
    solvation = 0.0000
    for i in range(len(line_list)):  # traverse puzzles, solve them. output the solution
        print('Line: %d' % i)
        first = time.perf_counter()
        ladder, length = find_path(graph, line_list[i][0], line_list[i][1])
        last = time.perf_counter()
        solvation += (last - first)
        if (ladder, length) == (None, None):
            print('No Solution!')
        else:
            print('Length is: %d' % length)
            for wod in ladder:
                print(wod)
        print()
    solve_time = str(solvation)
    print('Time to solve all these puzzles was: %s' % solve_time)
    print()
    total_time = str(float(solve_time) + float(timer))
    print('Total Time Was: %s' % total_time)

# ~/AI/U1_Search/Word_Ladders
# python word_ladders.py words_06_longer.txt puzzles_longer.txt

solve_puzzles()

