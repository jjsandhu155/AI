import math
import sys
from random import random

import numpy as np


def old_a(x):
    return int(0 < x)


def sigmoid_function(num):
    return 1 / (1 + math.e ** (-1.2 * num))


def p_net(A, ws, bs, x):
    A = np.vectorize(A)
    for w, b in zip(ws, bs):
        x = A((x @ w) + b)
    return x


def xor(in_1):
    # XOR HAPPENS HERE
    w0 = np.matrix([[1, -1], [1, -1]])
    b1 = np.matrix([[-.5, 1.5]])

    w1 = np.matrix([[1], [1]])
    b2 = np.matrix([[-1]])

    return p_net(old_a, [w0, w1], [b1, b2], in_1)[0, 0]


def diamond_testing():
    setss = set()
    x, y = None, None
    while len(setss) < 1000:
        x = random()
        y = random()
        if abs(x) + abs(y) > 1:
            print(diamond((x, y)))


def test_xor():
    print(xor((1, 1)), ':', '0')
    print(xor((1, 0)), ':', '1')
    print(xor((0, 1)), ':', '1')
    print(xor((0, 0)), ':', '0')


def diamond(xy):
    ws = [None] * 2
    bs = ws[:]
    ws[0] = np.array([[1, -1, 1, -1], [1, 1, -1, -1]])
    bs[0] = np.array([[1, 1, 1, 1]])
    ws[1] = np.array([[1], [1], [1], [1]])
    bs[1] = np.array([[-3]])
    return p_net(old_a, ws, bs, xy)[0, 0]


def circle(A, x):
    ws = [None] * 2
    bs = ws[:]
    ws[0] = np.array([[1, -1, 1, -1], [1, 1, -1, -1]])
    bs[0] = np.array([[-1.35, -1.35, -1.35, -1.35]])
    ws[1] = np.array([[1], [1], [1], [1]])
    bs[1] = np.array([[-.89]])

    resultant = p_net(A, ws, bs, np.array([[x[0], x[1]]]))
    resultant = int(round(resultant[0][0]))
    if resultant == 0:
        return 1
    else:
        return 0


def in_out(point):
    return math.sqrt(point[0] ** 2 + point[1] ** 2)


def circle_tester():
    misclassifications, proper = [], 0
    for pt in range(500):
        x = (random(), random())
        if circle(sigmoid_function, x) == 1 and in_out(x) <= 1:
            proper = proper + 1
        elif circle(sigmoid_function, x) == 0 and in_out(x) > 1:
            proper = proper + 1
        else:
            misclassifications.append(x)
    accuracy = proper / 500
    print('Misclassified Points:', misclassifications)
    print('Accuracy:', accuracy)


def inputt():
    user_input = sys.argv
    if len(user_input) == 2:
        import ast
        input_vect = ast.literal_eval(user_input[1])
        print(xor(input_vect))
    elif len(user_input) == 3:
        x, y = float(user_input[1]), float(user_input[2])
        resultant = diamond((x, y))
        if resultant == 0:
            print('outside')
        if resultant == 1:
            print('inside')
    elif len(user_input) == 1:
        circle_tester()


inputt()
