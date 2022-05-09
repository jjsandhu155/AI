def interiors():  # Project Euler Problem 102 - Triangle Containment
    count = 0
    with open('triangle_file.txt') as f:
        for line in f:
            xys = line.strip().split(',')
            xys = [int(i) for i in xys]
            if (xys[0] * xys[3] - xys[1] * xys[2] > 0) == (xys[2] * xys[5] - xys[3] * xys[4] > 0) == (xys[4] * xys[1] - xys[5] * xys[0] > 0):
                count += 1
    print('Number of Random Triangles Containing Origin (Problem 102):', count)


def lowest_proportion_bouncy99():  # Project Euler Problem 112 - Bouncy Numbers
    def is_bouncy(bouncy_number):
        is_increasing = False
        is_decreasing = False
        right = bouncy_number % 10
        bouncy_number = bouncy_number // 10

        while bouncy_number > 0:
            left = bouncy_number % 10
            if left > right:
                is_decreasing = True
            elif left < right:
                is_increasing = True
            right = left
            bouncy_number = bouncy_number // 10
            if is_increasing and is_decreasing:
                return True
        return False

    number_bouncy = 0
    solution = 99
    while number_bouncy < 0.99 * solution:
        solution += 1
        if is_bouncy(solution):
            number_bouncy += 1
    print('Lowest 99% Bouncy Number (Problem 112):', solution)


def kth():  # Project Euler Problem 124 - Ordered Radicals
    j, k = 100000, 10000

    lis = [[1, a] for a in range(j + 1)]
    for x in range(2, j + 1):
        if lis[x][0] == 1:
            for y in range(x, j + 1, x):
                lis[y][0] *= x
    print("Kth Element in Radical List (Problem 124):", sorted(lis)[k][1])


def palindromic_sum():  # Project Euler Problem 125 - Palindromic Sum
    bound, first, sums, answer = 10 ** 8, 1, 5, set()
    while sums < bound:
        last = first + 1
        while sums < bound:
            if str(sums) == str(sums)[::-1]:
                answer.add(sums)
            last = last + 1
            sums = sums + (last ** 2)
        first = first + 1
        sums = first ** 2 + (first + 1) ** 2
    print('Sum of Palindromic Consecutive Squares Under 10^8 (Problem 125):', sum(answer))


interiors()
lowest_proportion_bouncy99()
kth()
palindromic_sum()
