from sys import argv


def is_valid(p_height, p_width, rects):
    area = p_height * p_width
    areas = [one * two for one, two in rects]
    compare = sum(areas)
    return area == compare


def overlap_check(boundary_height, boundary_width, rects, poss):
    for i in range(len(rects)):
        if poss[i] is not None:
            i0, i1 = rects[i]
            i2, i3 = poss[i]
            if i2 < 0 or i3 < 0 or i2 + i0 > boundary_height or i3 + i1 > boundary_width:
                return False
            for z in range(i + 1, len(rects)):
                if poss[z] is not None:
                    i4, i5 = rects[z]
                    i6, i7 = poss[z]
                    if (i2 < i6 + i4) and (i2 + i0 > i6) and (i3 + i1 > i7) and (i3 < i7 + i5):
                        return False
    return True


def get_children(rectangle_index, height, width, rects, positions):
    minrect = min(rects[rectangle_index])
    new_positions = positions.copy()
    new_rectangles = rects.copy()
    h, w = new_rectangles[rectangle_index]
    new_rectangles[rectangle_index] = (w, h)
    for i in range(height):
        for j in range(width - minrect):
            new_positions[rectangle_index] = (i, j)
            if overlap_check(height, width, rects, new_positions):
                yield rects, new_positions
            if overlap_check(height, width, new_rectangles, new_positions):
                yield new_rectangles, new_positions


def backtracking(indexes_left, height, width, rects, positions):
    if len(indexes_left) == 0:
        return rects, positions
    next_var = indexes_left.pop()
    for new_rectangles, new_positions in get_children(next_var, height, width, rects, positions):
        result = backtracking(indexes_left, height, width, new_rectangles, new_positions)
        if result is not None:
            return result
    indexes_left.append(next_var)
    return None



puzzle = argv[1].split()
puzzle_height = int(puzzle[0])  # number rows
puzzle_width = int(puzzle[1])  # number columns
rectangles = [temp.split("x") for temp in puzzle[2:]]  # rectangle dimensions
rectangles = [tuple([int(n) for n in s]) for s in rectangles]
rectangles.sort(key=min, reverse=True)

if not is_valid(puzzle_height, puzzle_width, rectangles):
    print('Containing rectangle incorrectly sized.')
else:
    soln = backtracking(list(range(len(rectangles) - 1, -1, -1)), puzzle_height, puzzle_width, rectangles, [None for i in rectangles])
    if soln is not None:
        sol_rectangles, sol_positions = soln
        for i in range(len(sol_positions)):
            print(*sol_positions[i], *sol_rectangles[i])
    else:
        print('No Solution.')

"""
"4 7 7x4"
"2 3 1x2 2x2"
"18 9 3x11 5x7 4x8 6x10 1x2"
"4 8 4x1 1x6 1x3 3x1 1x3 1x3 6x1 1x4"
"11 12 3x6 2x5 4x10 7x9 1x1"
"9 18 3x8 5x10 4x11 6x7 1x2"
"13 14 4x5 3x8 6x11 7x10 2x1"
"19 19 1x19 1x12 6x9 9x15 15x3 10x6 3x12"

"24 24 4x7 7x4 7x5 11x4 9x3 2x8 22x3 8x4 14x11 8x10 2x12 5x3 9x3"
"56 56 28x14 32x11 32x10 21x18 21x18 21x14 21x14 17x14 28x7 28x6 10x7 14x4"
"""
