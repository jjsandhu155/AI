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


def pretty_print_tt(table):
    for ins, out in table:
        output = ""
        for in_1 in ins:
            output = output + str(in_1) + ' '
        print(output + '| ' + str(out))


def a(x):
    if x > 0:
        return 1
    else:
        return 0


def perceptron(A, w, b, x):
    return A(sum([x[1] * x[0] for x in zip(w, x)]) + b)


def check(n, w, b):
    truth = truth_table(len(w), n)
    return sum([1 for ins, out in truth_table(len(w), n) if perceptron(a, w, b, ins) == out]) / len(truth)


def inputt():
    import ast
    user_in = sys.argv[1:4]
    n = int(user_in[0])
    w = ast.literal_eval(user_in[1])
    b = float(user_in[2])
    print(check(n, w, b))


inputt()
