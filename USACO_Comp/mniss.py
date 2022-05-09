import math

import numpy as np

mock_run = True
weights = []
biass = []
network_size = [784, 300, 100, 10]

base = -1


def sig_base(num):
    return 1 / (1 + math.e ** (base * num))


sig_vec = np.vectorize(sig_base)


def sig_d(num):
    return (math.e ** (base * num)) / ((1 + math.e ** (base * num)) ** 2)


sig_d_vec = np.vectorize(sig_d)


def get_data(file_name):
    data_set = []
    with open(file_name) as file:
        for line in file:
            row = line.strip().split(',')
            x_new = [float(a) / 255.0 for a in row[1:]]
            array = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            array[int(row[0])] = 1
            array = array.reshape(1, -1)
            data_set.append((np.asarray(x_new), array))
    return data_set


def backprop():
    data = get_data("mnist_train.csv")

    num_epoch = 0
    if mock_run:
        num_epoch = 3
    else:
        num_epoch = 100

    learning = 0.1
    weights = [None, np.random.rand(network_size[0], network_size[1]) * 2 - 1, np.random.rand(network_size[1], network_size[2]) * 2 - 1,
               np.random.rand(network_size[2], network_size[3]) * 2 - 1]
    biass = [None, np.random.rand(1, network_size[1]) * 2 - 1, np.random.rand(1, network_size[2]) * 2 - 1,
            np.random.rand(1, network_size[3]) * 2 - 1]

    for epoch in range(num_epoch):
        for x, y in data:
            dot_backprops = [0 for i in range(5)]
            a_backprops = [np.array([x]) for i in range(5)]
            delta_backprops = [np.zeros((1, 784)) for k in range(5)]

            for i in range(1, 4):
                dot_backprops[i] = (a_backprops[i - 1] @ weights[i]) + biass[i]
                a_backprops[i] = sig_vec(dot_backprops[i])

            for i in range(3, 4):
                delta_backprops[i] = sig_d_vec(dot_backprops[i]) * (y - a_backprops[i])

            for a in range(2, -1, -1):
                delta_backprops[a] = sig_d_vec(dot_backprops[a]) * (delta_backprops[a + 1] @ weights[a + 1].transpose())

            for h in range(3, 0, -1):
                biass[h] = biass[h] + learning * delta_backprops[h]
                weights[h] = weights[h] + learning * (a_backprops[h - 1].transpose() @ delta_backprops[h])
        print("Epoch: " + str(epoch))
    return weights, biass
jjj

def p_net(dataset, weights, biases):
    print("Network:", network_size)
    weights, biases = weights[1:], biases[1:]
    amt_wrong = 0
    for x, y in dataset:
        x = sig_vec(x @ weights[0] + biases[0])
        x = sig_vec(x @ weights[1] + biases[1])
        x = sig_vec(x @ weights[2] + biases[2])
        if x.argmax() != y.argmax():
            amt_wrong += 1
    return amt_wrong, float(amt_wrong) / len(dataset)


test_set = get_data("mnist_test.csv")
weight, bias = backprop()
wrong, accuracy = p_net(test_set, weight, bias)
print(wrong, 'Wrong')
print('Accuracy:', accuracy)