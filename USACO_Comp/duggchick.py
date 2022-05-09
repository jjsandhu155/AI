import math
import random
import sys

import numpy as np

c_learn = 0.4
c_weights = [None, np.array([[1, -1], [-1, -1], [1, 1], [-1, 1]]).transpose(), np.array([[1, 2, 3, 4]]).transpose()]
c_bias = [None, np.array([[1], [1], [1], [1]]).T, np.array([[-6.05]]).transpose()]


s_input = [
    (np.array([[0, 0]]), np.array([[0, 0]])),
    (np.array([[0, 1]]), np.array([[0, 1]])),
    (np.array([[1, 0]]), np.array([[0, 1]])),
    (np.array([[1, 1]]), np.array([[1, 0]])),
]


def get_matrices():
    return [None, np.array(
        [[random.uniform(-1, 1) for i in range(2)], [random.uniform(-1, 1) for i in range(2)]]), np.array(
        [[random.uniform(-1, 1) for i in range(2)], [random.uniform(-1, 1) for i in range(2)]])], [None, np.array([[random.uniform(-1, 1) for i in range(2)]]),
                                                                                                   np.array([[random.uniform(-1, 1) for i in range(2)]])]


def sigmoid_step(num): return (1.0 / (1.0 + math.exp(-1.0 * num)))


def sigmoid_derivative(num): return float((1.0 / (1.0 + math.exp(-1.0 * num))) * (1.0 - (1.0 / (1.0 + math.exp(-1.0 * num)))))


def s_error(y, a): return 0.5 * math.pow(np.linalg.norm(y - a), 2)

"""
fsdfs
dsfsdfs

fsdf
sd
fsd
f
s
sd
f
sd
"""

def s_values():
    combos = dict()
    for train_amount in range(200):
        sigmoid_vectorized = np.vectorize(sigmoid_step)
        sigmoid_derivative_vectorized = np.vectorize(sigmoid_derivative)
        lr = random.uniform(math.pow(8, -2), math.pow(8, 1))

        s_weights, s_bias = get_matrices()

        dot_backprops = [np.array([[0, 0]])] * 10
        a_backprops = [np.array([[0, 0]])] * 10
        delta_backprops = [np.array([[0, 0]])] * 10

        for epoch in range(100):
            for input, output in s_input:
                a_backprops[0] = input
                for i in range(1, 3):
                    dot_backprops[i] = (a_backprops[i - 1] @ s_weights[i]) + (s_bias[i])
                    a_backprops[i] = sigmoid_vectorized(dot_backprops[i])

                for i in range(2, 3):
                    delta_backprops[i] = (sigmoid_derivative_vectorized(dot_backprops[i])) * (output * 1 - a_backprops[i])

                for i in range(1, -1, -1):
                    delta_backprops[i] = sigmoid_derivative_vectorized(dot_backprops[i]) * (delta_backprops[i + 1] @ s_weights[i + 1].transpose())

                for i in range(2, 0, -1):
                    s_bias[i] = s_bias[i] + lr * delta_backprops[i]
                    s_weights[i] = s_weights[i] + lr * (
                            a_backprops[i - 1].transpose() @ delta_backprops[i])

            s_weights_orig = s_weights
            s_bias_orig = s_bias

            err = 0
            for input in s_input:
                saved = input
                for i in range(0, 2):
                    input = sigmoid_vectorized((input @ s_weights[1:][i]) + s_bias[1:][i])
                err += s_error(input, saved)
                combos[err] = ([lr, s_weights_orig, s_bias_orig])
    most_accurate = combos[min(combos.keys())]
    return most_accurate


def main():
    sigmoid_vectorized = np.vectorize(sigmoid_step)
    sigmoid_derivative_vectorized = np.vectorize(sigmoid_derivative)
    if 'S' == "S":
        sum_values = s_values()
        for input in s_input:
            print(str(input[0]))
            for i in range(0, 2):
                final_weight = sum_values[1][1:][i]
                final_bias = sum_values[2][1:][i]
                input = sigmoid_vectorized((input @ final_weight) + final_bias)
            print(str(input[0]))

    elif sys.argv[1] == "C":
        dot_backprops = [0, 0, 0]
        a_backprops = [0, 0, 0]
        delta_backprops = [np.array([[0, 0]]) for n in range(3)]

        all_points = []
        with open("10000_pairs.txt") as file:
            for line in file:
                line = line.strip().rstrip()
                x_coord = float(line.split()[0])
                y_coord = float(line.split()[1])
                in_circle = None
                if math.sqrt(math.pow(x_coord, 2) + math.pow(y_coord, 2)) <= 1:
                    in_circle = 1
                else:
                    in_circle = 0
                all_points.append((np.array([[x_coord, y_coord]]), in_circle))

        for epoch in range(100):
            for i in range(len(all_points)):
                point_array = all_points[i][0]
                in_circle = all_points[i][1]
                a_backprops[0] = point_array

                for i in range(1, 3):

                    dot_backprops[i] = (a_backprops[i - 1] @ c_weights[i]) + c_bias[i]
                    a_backprops[i] = sigmoid_vectorized(dot_backprops[i])

                for i in range(2, 3):
                    delta_backprops[i] = (sigmoid_derivative_vectorized(dot_backprops[i])) * (in_circle * 1 - a_backprops[i])

                for i in range(1, -1, -1):
                    delta_backprops[i] = sigmoid_derivative_vectorized(dot_backprops[i]) * (delta_backprops[i + 1] @ c_weights[i + 1].transpose())

                for i in range(2, 0, -1):
                    c_bias[i] = c_bias[i] + c_learn * delta_backprops[i]
                    c_weights[i] = c_weights[i] + c_learn * (
                            a_backprops[i - 1].transpose() @ delta_backprops[i])

            final_weights, final_biases = c_weights[1:], c_bias[1:]
            misclassified_points_amt = 0
            for i in range(len(all_points)):
                point_array = all_points[i][0]
                in_circle = all_points[i][1]
                for temp in range(0, 2):
                    point_array = sigmoid_vectorized((point_array @ final_weights[temp]) + final_biases[temp])

                if round(point_array[0][0]) != in_circle:
                    misclassified_points_amt += 1
            print("Epoch #" + str(epoch))
            print("Misclassified points: " + str(misclassified_points_amt))


main()
