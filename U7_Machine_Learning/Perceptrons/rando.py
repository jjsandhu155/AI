import sys
from itertools import product

import numpy as np


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


def pretty_print_tt(table):
    for ins, out in table:
        output = ""
        for in_1 in ins:
            output = output + str(in_1) + ' '
        print(output + '| ' + str(out))


def step(x):
    return int(0 < x)


def p_net(A, ws, bs, x):
    A = np.vectorize(A)
    for w, b in zip(ws, bs):
        x = A((x @ w) + b)
    return x


def check(n, w, b):
    truth = truth_table(len(w), n)
    return sum([1 for ins, out in truth_table(len(w), n) if perceptron(step, w, b, ins) == out]) / len(truth)


def train_perceptron(bits, n):
    truth, weight, bias, old_w, old_b = truth_table(bits, n), tuple([0] * bits), 0, tuple([0] * bits), 0
    for epoch in range(0, 100):
        for input_vector, real_output in truth:
            function_output = perceptron(step, weight, bias, input_vector)
            bias += (real_output - function_output) * 1
            weight = tuple((weight + (1 * (real_output - function_output) * input_vector)) for (weight, input_vector) in zip(weight, input_vector))
        if (weight, bias) != (old_w, old_b):
            old_w, old_b = weight, bias
        else:
            break
    acc = check(n, weight, bias)
    return acc, weight, bias


def xor(in_1):
    # XOR HAPPENS HERE
    w0 = np.matrix([[1, -1], [1, -1]])
    b1 = np.matrix([[-.5, 1.5]])

    w1 = np.matrix([[1], [1]])
    b2 = np.matrix([[-1]])

    return p_net(step, [w0, w1], [b1, b2], in_1)[0,0]


def inputt():
    user_input = sys.argv
    if len(user_input) == 2:
        import ast
        input_vect = ast.literal_eval(sys.argv[1])
        print(xor(input_vect))



def fix_values():
    print(xor((1, 1)), ':', '0')
    print(xor((1, 0)), ':', '1')
    print(xor((0, 1)), ':', '1')
    print(xor((0, 0)), ':', '0')


fix_values()