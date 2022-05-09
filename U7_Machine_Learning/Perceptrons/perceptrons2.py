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


def train_perceptron(bits, n):
    truth, weight, bias, old_w, old_b = truth_table(bits, n), tuple([0] * bits), 0, tuple([0] * bits), 0
    for epoch in range(0, 100):
        for input_vector, real_output in truth:
            function_output = perceptron(a, weight, bias, input_vector)
            bias += (real_output - function_output) * 1
            weight = tuple((weight + (1 * (real_output - function_output) * input_vector)) for (weight, input_vector) in zip(weight, input_vector))
        if (weight, bias) != (old_w, old_b):
            old_w, old_b = weight, bias
        else:
            break
    acc = check(n, weight, bias)
    return acc, weight, bias


def inputt():
    user_input = sys.argv[1:3]
    bits = int(user_input[0])
    canonical_integer = int(user_input[1])
    accuracy, w, b = train_perceptron(bits, canonical_integer)
    print('Final Weight Vector:', w)
    print('Final Bias Value:', b)
    print('Perceptron Accuracy:', accuracy)


inputt()
