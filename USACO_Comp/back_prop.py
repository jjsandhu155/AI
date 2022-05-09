import math
import random
import sys

import numpy as nummy

file_name = "10000_pairs.txt"

base = -1


def sig_base(num):
    return 1 / (1 + math.e ** (base * num))


def sig_d(num):
    return (math.e ** (base * num)) / ((1 + math.e ** (base * num)) ** 2)


def in_out(point):
    return math.sqrt(point[0] ** 2 + point[1] ** 2) <= 1


def initialize():
    l_c = 0.4
    w1 = nummy.array([[1, -1], [-1, -1], [1, 1], [-1, 1]]).T
    w2 = nummy.array([[1, 2, 3, 4]]).T
    w = [None, w1, w2]
    b1 = nummy.array([[1], [1], [1], [1]]).T
    b2 = nummy.array([[-6]]).T
    b = [None, b1, b2]
    ina = [None] * 4
    ina[0] = (nummy.array([[0, 0]]), nummy.array([[0, 0]]))
    ina[1] = (nummy.array([[0, 1]]), nummy.array([[0, 1]]))
    ina[2] = (nummy.array([[1, 0]]), nummy.array([[0, 1]]))
    ina[3] = (nummy.array([[1, 1]]), nummy.array([[1, 0]]))

    return l_c, w, b, ina


def s_in():
    lr = random.uniform(math.pow(8, -2), math.pow(8, 1))
    w1 = nummy.array([[random.uniform(-1, 1), random.uniform(-1, 1)], [random.uniform(-1, 1), random.uniform(-1, 1)]])
    wss = [None, w1, w1]
    b1 = nummy.array([[random.uniform(-1, 1), random.uniform(-1, 1)]])
    bss = [None, b1, b1]

    dop = [nummy.array([[0, 0]])] * 10
    aop = dop.copy()
    dep = dop.copy()

    return lr, wss, bss, dop, aop, dep


def pt1(res):
    for x in range(200):
        learn, w_l, b_l, backd, backa, backdel = s_in()

        for x in range(100):
            for i_1, o_1 in ins:
                backa[0] = i_1
                backd[1] = (backa[0] @ w_l[1]) + (b_l[1])
                backa[1] = vec_sig(backd[1])
                backd[2] = (backa[1] @ w_l[2]) + (b_l[2])
                backa[2] = vec_sig(backd[2])

                backdel[2] = (vec_sig_d(backd[2])) * (o_1 * 1 - backa[2])

                backdel[1] = vec_sig_d(backd[1]) * (backdel[2] @ w_l[2].T)
                backdel[0] = vec_sig_d(backd[0]) * (backdel[1] @ w_l[1].T)

                b_l[2] = b_l[2] + learn * backdel[2]
                w_l[2] = w_l[2] + learn * (backa[1].T @ backdel[2])

                b_l[1] = b_l[1] + learn * backdel[1]
                w_l[1] = w_l[1] + learn * (backa[0].T @ backdel[1])

            s_weights_orig = w_l
            s_bias_orig = b_l

            mi = 0
            for i_1 in ins:
                temp = i_1
                i_1 = vec_sig((i_1 @ w_l[1:][0]) + b_l[1:][0])
                i_1 = vec_sig((i_1 @ w_l[1:][1]) + b_l[1:][1])
                mi = mi + (nummy.linalg.norm(i_1 - temp) ** 2) / 2.0
                res[mi] = ([learn, s_weights_orig, s_bias_orig])
    return res[min(res.keys())]


def challenge_2_out(total):
    for ind in range(len(ins)):
        inp = ins[ind]
        print(inp[0])
        w, b = total[1][1:][0], total[2][1:][0]
        inp = vec_sig((inp @ w) + b)
        w, b = total[1][1:][1], total[2][1:][1]
        inp = vec_sig((inp @ w) + b)
        print(inp[0])


def real_points(file_name):
    f = open(file_name)
    master_list = []
    for line in f.readlines():
        line = line.strip()
        x_coord, y_coord = line.split()
        x_coord, y_coord = float(x_coord), float(y_coord)
        punto = (x_coord, y_coord)
        if not in_out(punto):
            inside = 0
        else:
            inside = 1
        point = nummy.array([punto])
        master_list.append([point, inside])
    return master_list


def challenge_3_out(master_list):
    dbp, a_ar, tri = [0, 0, 0], [0, 0, 0], [nummy.array([[0, 0]]), nummy.array([[0, 0]]), nummy.array([[0, 0]])]
    ep = 0
    while ep < 100:
        for x in range(len(master_list)):
            point_array = master_list[x]
            point_array = point_array[0]
            in_circle = master_list[x]
            in_circle = in_circle[1]
            a_ar[0] = point_array

            dbp[1] = (a_ar[0] @ ws[1]) + bs[1]
            a_ar[1] = vec_sig(dbp[1])

            dbp[2] = (a_ar[1] @ ws[2]) + bs[2]
            a_ar[2] = vec_sig(dbp[2])

            tri[2] = (vec_sig_d(dbp[2])) * (in_circle * 1 - a_ar[2])

            tri[1] = vec_sig_d(dbp[1]) * (tri[2] @ ws[2].T)
            tri[0] = vec_sig_d(dbp[0]) * (tri[1] @ ws[1].T)

            bs[2] = bs[2] + lamb * tri[2]
            ws[2] = ws[2] + lamb * (a_ar[1].T @ tri[2])

            bs[1] = bs[1] + lamb * tri[1]
            ws[1] = ws[1] + lamb * (a_ar[0].T @ tri[1])

        cumulat_wv, cumulat_b = ws[1:], bs[1:]
        misclassified_points_amt = 0
        for x in range(len(master_list)):
            point_array = master_list[x]
            point_array = point_array[0]
            in_circle = master_list[x]
            in_circle = in_circle[1]
            point_array = vec_sig((point_array @ cumulat_wv[0]) + cumulat_b[0])
            point_array = vec_sig((point_array @ cumulat_wv[1]) + cumulat_b[1])
            if round(point_array[0][0]) != in_circle:
                misclassified_points_amt = misclassified_points_amt + 1
        print('Epoch:', ep)
        print('# Misclassified:', misclassified_points_amt)
        ep += 1


lamb, ws, bs, ins = initialize()
vec_sig = nummy.vectorize(sig_base)
vec_sig_d = nummy.vectorize(sig_d)

if sys.argv[1] == 'S':
    print('SUM')
    challenge_2_out(pt1(dict()))
    print()

if sys.argv[1] == 'C':
    print('CIRCLE')
    challenge_3_out(real_points('10000_pairs.txt'))
    print()
