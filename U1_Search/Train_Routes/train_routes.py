# Train_Routes Lab Part 1
import sys
import time
from heapq import heappush, heappop
from math import pi, acos, sin, cos


def distance(node1, node2):
    if node1 == node2:
        return 0
    y1, x1 = node1
    y2, x2 = node2

    R = 3958.76
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0

    return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * R


def gen_structure():
    structure = dict()
    coord_dict = dict()
    edge_dict = dict()
    cities_dict = dict()
    junctions = set()
    with open("rrNodeCity.txt") as city_file:
        for line in city_file:
            city_junction = line.split()
            city_name = " ".join(city_junction[1:])
            cities_dict[city_name] = city_junction[0]

    with open("rrNodes.txt") as node_file:
        for line in node_file:
            args = line.split()
            structure[args[0]] = set()
            coord_dict[args[0]] = (float(args[1]), float(args[2]))
    with open("rrEdges.txt") as edge_file:
        for line in edge_file:
            args = line.split()
            junctions.add((args[0], args[1]))
            edge_dict[args[0]] = set()
            edge_dict[args[1]] = set()
        for tup in junctions:
            i1, i2 = tup
            edge_dict[i1].add(i2)
            edge_dict[i2].add(i1)

    for key, val in structure.items():
        for c in edge_dict[key]:
            structure[key].add((c, distance(coord_dict[key], coord_dict[c])))
    return coord_dict, cities_dict, structure


def djkstra(start_state, end_state, structure):
    closed = set()
    start_node = (0, start_state)
    fringe = []
    heappush(fringe, start_node)
    while fringe:
        v = heappop(fringe)
        v_depth, v_state = v
        if v_state == end_state:
            return v_depth
        if v_state not in closed:
            closed.add(v_state)
            for c in structure[v_state]:
                c_state, c_length = c
                if c_state not in closed:
                    temp = (v_depth + c_length, c_state)
                    heappush(fringe, temp)
    return None


def heuristic(current, end_state):
    return distance(current, end_state)



def a_star(start_state, end_state, structure, coord):
    closed = set()
    longlat = coord[end_state]
    start_node = (heuristic(coord[start_state], longlat), 0, start_state)
    fringe = []
    heappush(fringe, start_node)
    while fringe:
        v = heappop(fringe)
        v_f, v_depth, v_state = v
        if v_state == end_state:
            return v_depth
        if v_state not in closed:
            closed.add(v_state)
            for c in structure[v_state]:
                c_state, c_length = c
                if c_state not in closed:
                    temp = (v_depth + 1 + c_length + heuristic(coord[c_state], longlat), v_depth + c_length, c_state)
                    heappush(fringe, temp)
    return None


def in_out():
    struc_time = time.perf_counter()
    coord, cities, structure = gen_structure()
    struc_time2 = time.perf_counter()
    structural_time = str(struc_time2 - struc_time)
    c1, c2 = sys.argv[1:3]
    dj_start = time.perf_counter()
    length = djkstra(cities[c1], cities[c2], structure)
    dj_end = time.perf_counter()
    dj_time = str(dj_end - dj_start)
    a_start = time.perf_counter()
    dist = a_star(cities[c1], cities[c2], structure, coord)
    a_end = time.perf_counter()
    a_time = str(a_end - a_start)
    print('Time to create data structure:', structural_time)
    print('%s to %s with Dijkstra: %s in %s seconds.' % (c1, c2, str(length), dj_time))
    print('%s to %s with A*: %s in %s seconds.' % (c1, c2, str(dist), a_time))

in_out()

