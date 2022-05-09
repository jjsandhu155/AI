# JJ Sandhu - Pd. 2
# Python Exercises 1 (Started: 9/7 -- Finished: 9/8)

import sys

input_letter = sys.argv[1]


def fiber(n):  # Fibonnaci Calculator O(2^N) -- can be done in O(logn) time and O(1) space with more effort
    n = int(n)
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fiber(n - 1) + fiber(n - 2)


if input_letter == 'A':  # Sum of three numbers
    print('Sum: ' + str(int(sys.argv[2]) +
                        int(sys.argv[3]) + int(sys.argv[4])))

if input_letter == 'B':  # Sum of all given integers
    total = 0
    for num in sys.argv[2:]:
        total += int(num)
    print('Sum: ' + str(total))

if input_letter == 'C':  # Output given multiples of three
    divis = []
    for num in sys.argv[2:]:
        if int(num) % 3 == 0:
            divis.append(num)
    print('Multiples of 3: ', end='')
    print(divis)

if input_letter == 'D':  # Output first (given number) fibbonaci numbers
    numbers = int(sys.argv[2]) + 1
    lis = []
    for i in range(1, numbers):
        lis.append(fiber(i))
    print('First ' + str(numbers) + ' Fibonacci Numbers: ', end='')
    print(lis)

# Output (k^2-3k+2) for all numbers from input1 to input 2 inclusive
if input_letter == 'E':
    lis = []
    for i in range(int(sys.argv[2]), int(sys.argv[3])+1):
        lis.append((i ** 2) + (-3 * i) + 2)
    print('Function Values:', end=' ')
    print(lis)

if input_letter == 'F':  # Calculate and output area of triangle given its three sides
    a = float(sys.argv[2])
    b = float(sys.argv[3])
    c = float(sys.argv[4])

    if (a + b <= c) or (a + c <= b) or (b + c <= a):
        print('Not a Valid Triangle')
    else:
        s = (a + b + c) / 2
        area = (s * (s - a) * (s - b) * (s - c)) ** (1/2)
        print('Area of Triangle: ' + str(area))

if input_letter == 'G':  # count and output number of each vowel given from a string
    # vowel counts for a, e, i, o, u respectively
    vowel_count = [0, 0, 0, 0, 0]
    for ch in sys.argv[2]:
        le = ch.lower()
        if le == 'a':
            vowel_count[0] += 1
        if le == 'e':
            vowel_count[1] += 1
        if le == 'i':
            vowel_count[2] += 1
        if le == 'o':
            vowel_count[3] += 1
        if le == 'u':
            vowel_count[4] += 1
    print('# a\'s: ' + str(vowel_count[0]) + ', # e\'s: ' + str(vowel_count[1]) + ', # i\'s: ' + str(
        vowel_count[2]) + '. # o\'s: ' + str(vowel_count[3]) + ', # u\'s: ' + str(vowel_count[4]))
