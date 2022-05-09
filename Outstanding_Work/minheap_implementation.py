import sys
import time
import heapq


# ^ for timing comparison purposes

def heappop(heap):  # Pops off the smallest value in the heap, while retaining the structure
    if heap:
        pop = heap[0]
        heap[0] = heap.pop()
        ind = 0
        while True:
            first_child = 1 + (2 * ind)
            if first_child >= len(heap):
                return pop
            second_child = first_child + 1
            if second_child < len(heap) and heap[second_child] < heap[first_child]:
                child = second_child
            else:
                child = first_child
            if heap[ind] <= heap[child]:
                return pop
            heap[child], heap[ind], ind = heap[ind], heap[child], child
            pass
        pass
    return heap.pop()


def heappush(heap, value):  # Pushes a new value onto the heap, while retaining the structure
    heap.append(value)
    current_position = len(heap) - 1
    newitem = heap[current_position]
    while current_position > 0:  # Follow the path to the root, moving parents down until finding a place newitem fits.
        parent_position = (current_position - 1) >> 1
        parent = heap[parent_position]
        if newitem < parent:
            heap[current_position] = parent
            current_position = parent_position
            continue
        break
    heap[current_position] = newitem  # puts new item into the position derived above


def heapify(x):  # Transfers a list to a heap in place
    n = len(x)
    for i in reversed(range(n // 2)):  # transforms from the bottom upwards
        shift_upwards(x, i)


def shift_upwards(heap, ind):
    initial_position = ind
    value = heap[ind]
    leftmost_child_position = 2 * ind + 1
    while leftmost_child_position < len(heap):  # bubble up to smaller child until leaf is hit
        rightward_position = leftmost_child_position + 1  # set index to smaller child
        if not heap[leftmost_child_position] < heap[rightward_position] and rightward_position < len(heap):
            leftmost_child_position = rightward_position
        # Move the smaller child up.
        heap[ind] = heap[leftmost_child_position]
        ind = leftmost_child_position
        leftmost_child_position = 2 * ind + 1

    while ind > initial_position:  # put the newitem in at the empty leaf position by shifting its parents down
        parentpos = (ind - 1) >> 1
        parent = heap[parentpos]
        if value < parent:
            heap[ind] = parent
            ind = parentpos
            continue
        break
    heap[ind] = value


def output():  # code for specification
    list1 = []
    index = 1
    for arg in sys.argv[1:]:
        if arg not in ('A', 'R'):
            list1.append(int(arg))
            index += 1
        else:
            break
    # newlist = [int(i) for i in list1]
    print('Initial list:', list1)

    heapify(list1)
    print('Heapified list:', list1)

    for i in range(index, len(sys.argv)):
        if sys.argv[i] == 'A':
            heappush(list1, int(sys.argv[i + 1]))
            print('Added', str(sys.argv[i + 1]), 'to heap:', list1)
        if sys.argv[i] == 'R':
            removed = heappop(list1)
            print('Popped', str(removed), 'from heap:', list1)


def time_comparison():  # just a time test, ignore this
    print("Custom Heap Implementation:")
    start1 = time.perf_counter()
    list1 = []
    index = 1
    for arg in sys.argv[1:]:
        if arg not in ('A', 'R'):
            list1.append(int(arg))
            index += 1
        else:
            break
    print('Initial list:', list1)
    heapify(list1)
    print('Heapified list:', list1)
    for i in range(index, len(sys.argv)):
        if sys.argv[i] == 'A':
            heappush(list1, int(sys.argv[i + 1]))
            print('Added', str(sys.argv[i + 1]), 'to heap:', list1)
        if sys.argv[i] == 'R':
            removed = heappop(list1)
            print('Popped', str(removed), 'from heap:', list1)
    end1 = time.perf_counter()
    print()

    print("Python's C Implementation:")
    start2 = time.perf_counter()
    list2 = []
    index = 1
    for arg in sys.argv[1:]:v
        if arg not in ('A', 'R'):
            list2.append(int(arg))
            index += 1
        else:
            break
    print('Initial list:', list2)

    heapq.heapify(list1)
    print('Heapified list:', list2)

    for i in range(index, len(sys.argv)):
        if sys.argv[i] == 'A':
            heapq.heappush(list1, int(sys.argv[i + 1]))
            print('Added', str(sys.argv[i + 1]), 'to heap:', list2)
        if sys.argv[i] == 'R':
            removed = heapq.heappop(list2)
            print('Popped', str(removed), 'from heap:', list2)
    end2 = time.perf_counter()
    print()

    print('Custom Time:', str(end1 - start1))
    print('C Implementation Time:', str(end2 - start2))


output()

# time_comparison()
"""
(venv) (base) JJs-MacBook-Pro:Outstanding_Work_2 jjsmac$ python minheap_implementation.py 3 -1 5 17 8 -4 19 3 6 A 7 A -8 A 5 R R R R A 2
Initial list: [3, -1, 5, 17, 8, -4, 19, 3, 6]
Heapified list: [-4, -1, 3, 3, 8, 5, 19, 17, 6]
Added 7 to heap: [-4, -1, 3, 3, 7, 5, 19, 17, 6, 8]
Added -8 to heap: [-8, -4, 3, 3, -1, 5, 19, 17, 6, 8, 7]
Added 5 to heap: [-8, -4, 3, 3, -1, 5, 19, 17, 6, 8, 7, 5]
Popped -8 from heap: [-4, -1, 3, 3, 5, 5, 19, 17, 6, 8, 7]
Popped -4 from heap: [-1, 3, 3, 6, 5, 5, 19, 17, 7, 8]
Popped -1 from heap: [3, 3, 5, 6, 5, 8, 19, 17, 7]
Popped 3 from heap: [3, 5, 5, 6, 7, 8, 19, 17]
Added 2 to heap: [2, 3, 5, 5, 7, 8, 19, 17, 6]

Initial list: [3, -1, 5, 17, 8, -4, 19, 3, 6]
Heapified list: [-4, -1, 3, 3, 8, 5, 19, 17, 6]
Added 7 to heap: [-4, -1, 3, 3, 7, 5, 19, 17, 6, 8]
Added -8 to heap: [-8, -4, 3, 3, -1, 5, 19, 17, 6, 8, 7]
Added 5 to heap: [-8, -4, 3, 3, -1, 5, 19, 17, 6, 8, 7, 5]
Popped -8 from heap: [-4, -1, 3, 3, 5, 5, 19, 17, 6, 8, 7]
Popped -4 from heap: [-1, 3, 3, 6, 5, 5, 19, 17, 7, 8]
Popped -1 from heap: [3, 3, 5, 6, 5, 8, 19, 17, 7]
Popped 3 from heap: [3, 5, 5, 6, 7, 8, 19, 17]
Added 2 to heap: [2, 3, 5, 5, 7, 8, 19, 17, 6]
"""
