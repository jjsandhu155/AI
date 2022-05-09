import sys
import tkinter as tk

from heapq import heappush, heappop
from math import pi, acos, sin, cos, tan, log
root = tk.Tk()
height = root.winfo_screenheight()
width = root.winfo_screenwidth()


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


def gen_structure() -> object:
    structure = dict()
    longitude_latitudes = dict()
    edge_dict = dict()
    cities = dict()
    junctions = set()
    with open("rrNodeCity.txt") as city_file:
        for line in city_file:
            city_junction = line.split()
            city_name = " ".join(city_junction[1:])
            cities[city_name] = city_junction[0]

    with open("rrNodes.txt") as node_file:
        for line in node_file:
            args = line.split()
            structure[args[0]] = set()
            longitude_latitudes[args[0]] = (float(args[1]), float(args[2]))

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
            structure[key].add((c, distance(longitude_latitudes[key], longitude_latitudes[c])))
    return longitude_latitudes, cities, structure


def djkstra(start_state, end_state, structure, liner, coord, canvas,root):
    count = 0
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
                if (c_state, v_state) in liner:
                    canvas.itemconfig(liner[(v_state, c_state)], fill='red')
                else:
                    liner[(v_state, c_state)] = canvas.create_line([*conversion(*coord[c_state]), *conversion(*coord[v_state])], tag='graph_line', fill='red')
                count += 1
                if count == 800:
                    root.update()
                    count = 0
                if c_state not in closed:
                    temp = (v_depth + c_length, c_state)
                    heappush(fringe, temp)
    return None


def djkstra(start_state, end_state, structure, liner, coord, canvas,root):
    count = 0
    closed = set()
    start_node = (0, start_state, [start_state])
    fringe = []
    heappush(fringe, start_node)
    while fringe:
        v = heappop(fringe)
        v_depth, v_state, v_path = v
        if v_state == end_state:
            for i in range(len(v_path)-1):
                if (v_path[i], v_path[i+1]) in liner:
                    canvas.itemconfig(liner[(v_path[i], v_path[i+1])], fill='cadet blue')
                else:
                    liner[(v_path[i], v_path[i+1])] = canvas.create_line([*conversion(*coord[v_path[i]]), *conversion(*coord[v_path[i+1]])], tag='graph_line', fill='cadet blue')

            return v_depth
        if v_state not in closed:
            closed.add(v_state)
            for c in structure[v_state]:
                c_state, c_length = c
                if (c_state, v_state) in liner:
                    canvas.itemconfig(liner[(v_state, c_state)], fill='red')
                else:
                    liner[(v_state, c_state)] = canvas.create_line([*conversion(*coord[c_state]), *conversion(*coord[v_state])], tag='graph_line', fill='red')
                count += 1
                if count == 800:
                    root.update()
                    count = 0
                if c_state not in closed:
                    temp = (v_depth + c_length, c_state,v_path + [c_state] )
                    heappush(fringe, temp)
    return None


def heuristic(current, end_state):
    return distance(current, end_state)


def quits(self):
    self.destroy()
    exit()


def a_star(start_state, end_state, structure, liner, coord, canvas, root):
    count = 0
    closed = set()
    longlat = coord[end_state]
    start_node = (heuristic(coord[start_state], longlat), 0, start_state, [start_state])
    fringe = []
    heappush(fringe, start_node)
    while fringe:
        v = heappop(fringe)
        v_f, v_depth, v_state, v_path = v
        if v_state == end_state:
            for i in range(len(v_path)-1):
                if (v_path[i], v_path[i+1]) in liner:
                    canvas.itemconfig(liner[(v_path[i], v_path[i+1])], fill='black')
                else:
                    liner[(v_path[i], v_path[i+1])] = canvas.create_line([*conversion(*coord[v_path[i]]), *conversion(*coord[v_path[i+1]])], tag='graph_line', fill='black')
            return v_depth
        if v_state not in closed:
            closed.add(v_state)
            for c in structure[v_state]:
                c_state, c_length = c
                if (c_state, v_state) in liner:
                    canvas.itemconfig(liner[(v_state, c_state)], fill='light sea green')
                else:
                    liner[(v_state, c_state)] = canvas.create_line([*conversion2(*coord[c_state]), *conversion2(*coord[v_state])], tag='graph_line', fill='light sea green')
                count += 1
                if count == 100:
                    root.update()
                    count = 0
                if c_state not in closed:
                    temp = (v_depth + 1 + c_length + heuristic(coord[c_state], longlat), v_depth + c_length, c_state, v_path + [c_state])
                    heappush(fringe, temp)

    return None


def input_output_2():
    root.geometry(str(root.winfo_screenwidth()) + 'x' + str(root.winfo_screenheight()))
    canvas = tk.Canvas(root, height=root.winfo_screenheight(), width=root.winfo_screenwidth())
    liner = dict()
    coord, cities, structure = gen_structure()
    for key, values in structure.items():
        x1, y1 = conversion(*coord[key])
        for val, garbage in values:
            x2, y2 = conversion(*coord[val])
            liner[(key, val)] = canvas.create_line([(x1, y1), (x2, y2)], tag='graph_line', fill='brown')
    liner2 = dict()
    for key, values in structure.items():
        x1, y1 = conversion2(*coord[key])
        for val, garbage in values:
            x2, y2 = conversion2(*coord[val])
            liner2[(key, val)] = canvas.create_line([(x1, y1), (x2, y2)], tag='graph_line', fill='red')

    c1, c2 = sys.argv[1:3]
    canvas.create_text((180,200),text='--A* Algorithm--')
    canvas.create_text((580,200),text='--Dijkstra\'s Algorithm--')
    canvas.create_text((420,125),text='Note: Animation Speeds Are Not Perfectly Reflective of Algorithm Speeds As They Have Been Adjusted for Convenience/Visibility')
    canvas.create_text((400,150),text="Also Note: Dijkstra Goes First (Right)")
    canvas.pack(expand=True)
    djkstra(cities[c1], cities[c2], structure, liner, coord, canvas,root)
    a_star(cities[c1], cities[c2], structure, liner2, coord, canvas, root)
    root.mainloop()


def conversion(lat, longi):
    x = (width * (180 + longi) / 360) % width + (width / 2)
    radians = lat * pi / 180
    inter = log(tan((pi / 4) + (radians / 2)))
    y = (height / 2) - (width * inter / (2 * pi))
    return x-1000, y+100

def conversion2(lat, longi):
    x = (width * (180 + longi) / 360) % width + (width / 2)
    radians = lat * pi / 180
    inter = log(tan((pi / 4) + (radians / 2)))
    y = (height / 2) - (width * inter / (2 * pi))
    return x-1600, y+100

input_output_2()
