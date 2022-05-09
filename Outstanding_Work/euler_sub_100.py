# JJ Sandhu -- Project Euler Outstanding Work #1
# 10/5 - 10/5
# Slow Implementations Due to Time Constraint (Didn't Have Much Time to Improve Efficiency, Do Later)
"""
✅ Problem 12
✅ Problem 14
✅ Problem 17
✅ Problem 21
✅ Problem 24
✅ Problem 30
"""

import sys
# 12 -- Divisible Triangular Number


def factor_len(x):
    len = 0
    for i in range(1, (int(x**(1/2))+1)):
        if x % i == 0:
            len = len + 2
    return len


x = 1
for y in range(2, 100000):
    x = x + y
    if factor_len(x) > 490:
        break

print('Problem 12:', x)


# 14 -- Collatz Sequence


def col_length(x):
    count = 0
    while x != 1:
        if x % 2 == 0:
            x = x / 2
        else:
            x = 3 * x + 1
        count = count + 1
    return count


max_val = 8
max = 13
for i in range(13, 1000000):
    temp = col_length(i)
    if temp > max_val:
        max_val = temp
        max = i
print('Problem 14:', max)
# 17 -- Number Letter Counts


def translate(x):
    sin = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven',
           12: 'twelve', 13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen', 19: 'nineteen'}
    two = {2: 'twenty', 3: 'thirty', 4: 'forty', 5: 'fifty',
           6: 'sixty', 7: 'seventy', 8: 'eighty', 9: 'ninety'}

    trans = ''
    if x >= 1000:
        trans = trans + sin[x // 1000]
        if x % 1000 == 0:
            trans = trans + " thousand"
        else:
            trans = trans + " thousand "
        x = x % 1000
    if x >= 100:
        trans += sin[x // 100]
        if x % 100 == 0:
            trans = trans + " hundred"
        else:
            trans = trans + " hundred and "
        x = x % 100
    if x >= 20:
        trans = trans + two[x // 10]
        x = x % 10
        if x % 10 in sin:
            trans = trans + '-'
    if x in sin:
        trans = trans + sin[x]
    return trans


print('Problem 17:', sum(len((translate(i).replace(' ', '')).replace('-', ''))
                         for i in range(1, 1001)))

# 21 -- Amicable Numbers


def factor_sum(x):
    return sum(i for i in range(1, x // 2 + 1) if not (x % i))


print('Problem 21:', sum([i for i in range(1, 10000) if i == factor_sum(
    factor_sum(i)) and factor_sum(i) != factor_sum(factor_sum(i))]))


# Problem 24 -- Lexicographic Permutations
count = 0
for cero in range(0, 10):
    for uno in [x for x in range(0, 10) if x not in {cero}]:
        for dos in [x for x in range(0, 10) if x not in {cero, uno}]:
            for tres in [x for x in range(0, 10) if x not in {cero, uno, dos}]:
                for quatro in [x for x in range(0, 10) if x not in {cero, uno, dos, tres}]:
                    for cinco in [x for x in range(0, 10) if x not in {cero, uno, dos, tres, quatro}]:
                        for seis in [x for x in range(0, 10) if x not in {cero, uno, dos, tres, quatro, cinco}]:
                            for siete in [x for x in range(0, 10) if x not in {cero, uno, dos, tres, quatro, cinco, seis}]:
                                for ocho in [x for x in range(0, 10) if x not in {cero, uno, dos, tres, quatro, cinco, seis, siete}]:
                                    for nueve in [x for x in range(0, 10) if x not in {cero, uno, dos, tres, quatro, cinco, seis, siete, ocho}]:
                                        count = count + 1
                                        if count == 1000000:
                                            num = str(cero) + str(uno) + str(dos) + str(tres) + str(quatro) + str(
                                                cinco) + str(seis) + str(siete) + str(ocho) + str(nueve)
                                            break
print('Problem 24:', num)

# Problem 30 -- Digit Fifth Powers
print('Problem 30:', sum([num for num in range(
    10, 355000) if num == sum([int(a) ** 5 for a in str(num)])]))
