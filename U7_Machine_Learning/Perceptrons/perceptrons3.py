import sys
from itertools import product


def truth_table(bits, n):
    pair, temp, num = list(product((1, 0), repeat=bits)), [], None
    if n == 0:
        num = [0]
    else:
        while n:
            temp.append(int(n % 2))
            n //= 2
        num = temp[::-1]
    over = len(pair) - len(num)
    for add in range(0, over):
        num.insert(0, 0)
    table = zip(pair, num)
    return tuple(table)


def a(x):
    if x > 0:
        return 1
    else:
        return 0


def perceptron(A, w, b, x):
    return A(sum([x[1] * x[0] for x in zip(w, x)]) + b)


def simulation(in12):
    # XOR HAPPENS HERE
    w13 = 1
    w23 = 1
    b3 = -.5

    w14 = -1
    w24 = -1
    b4 = 1.5

    w15 = 1
    w25 = 1
    b5 = -1

    perceptron_3 = perceptron(a, (w13, w23), b3, in12)
    perceptron_4 = perceptron(a, (w14, w24), b4, in12)
    perceptron_5 = perceptron(a, (w15, w25), b5, (perceptron_3, perceptron_4))
    return perceptron_5


def inputt():
    import ast
    input_vect = ast.literal_eval(sys.argv[1])
    print(simulation(input_vect))


def fix_values():
    print(xor((1, 1)), ':', '0')
    print(xor((1, 0)), ':', '1')
    print(xor((0, 1)), ':', '1')
    print(xor((0, 0)), ':', '0')


inputt()
