# JJ Sandhu - Pd. 2
# Project Euler Challenge (Started: 9/10/20 -- Finished:)

import sys


def is_prime(x):
    if x <= 1:
        return False
    if (x <= 3):
        return True
    if x % 2 == 0 or x % 3 == 0:
        return False
    i = 5
    while i * i <= x:
        if (x % i == 0 or x % (i + 2) == 0):
            return False
        i = i + 6
    return True


# A. -- Problem 7: 10,001st Prime Number
count = 0
num = 0
while count != 10001:
    num += 1
    if is_prime(num):
        count += 1
print('A:', str(num))

# B. -- Problem 1: Sum of Multiples of 3 and 5 Under 1000
print('B:', str(
    sum([i for i in range(1000) if i % 3 == 0 or i % 5 == 0])))

# C. -- Problem 2: Sum of Even Fibonacci Numbers Under 4M


def fib(x):
    return 1 if x in (0, 1) else fib(x-1) + fib(x-2)


total, z = (0, 2)
while fib(z) <= 4000000:
    if fib(z) % 2 == 0:
        total = total + fib(z)
    z = z + 3
print('C:', total)

# D. -- Problem 3: Largest Prime Factor of 600851475143
max_prime = 0
max_prime, g = (0, 600851475143)
while g % 2 == 0:
    max_prime = 2
    g = g / 2
for i in range(3, int(g**(1/2))+1, 2):
    while g % i == 0:
        max_prime = i
        g = g / i
print('D:', max_prime)

# E. -- Problem 4: Largest Palindrome Made from the Product of two 3 Digit Numbers. 9009 = 91 x 99


def is_palindrome(str):
    return True if str == str[::-1] else False


gr8st_palindrome = 0
for num1 in range(100, 999):
    for num2 in range(100, 999):
        if is_palindrome(str(num1 * num2)) and num1 * num2 > gr8st_palindrome:
            gr8st_palindrome = num1 * num2
print('E:', gr8st_palindrome)

# F. -- Problem 8: Find 13 Adjacent Numbers with the Greatest Product, Value of Product
string_num = """
73167176531330624919225119674426574742355349194934
96983520312774506326239578318016984801869478851843
85861560789112949495459501737958331952853208805511
12540698747158523863050715693290963295227443043557
66896648950445244523161731856403098711121722383113
62229893423380308135336276614282806444486645238749
30358907296290491560440772390713810515859307960866
70172427121883998797908792274921901699720888093776
65727333001053367881220235421809751254540594752243
52584907711670556013604839586446706324415722155397
53697817977846174064955149290862569321978468622482
83972241375657056057490261407972968652414535100474
82166370484403199890008895243450658541227588666881
16427171479924442928230863465674813919123162824586
17866458359124566529476545682848912883142607690042
24219022671055626321111109370544217506941658960408
07198403850962455444362981230987879927244284909188
84580156166097919133875499200524063689912560717606
05886116467109405077541002256983155200055935729725
71636269561882670428252483600823257530420752963450
"""
array = [int(dig) for dig in string_num.replace('\n', '')]
gr8_product, local = (0, 1)
for i in range(len(array)-13):
    for num in array[i:i+13]:
        local = local * num
    if local > gr8_product:
        gr8_product = local
    local = 1
print('F:', gr8_product)

# G. -- Problem 9: Pythagorean Triplet for which a + b + c = 1000. Find abc. a < b < c. a2 + b2 = c2
for c in range(2, 1000):
    for a in range(1, c):
        b = 1000 - c - a
        if a**2 + b**2 == c**2 and a*b*c > 0:
            print('G:', str(a*b*c))
            break

#6 (Optional)
print('#6/Optional:', ((sum([i for i in range(101)]))
                       ** 2) - (sum(i*i for i in range(101))))
