import math
import random
import sys

import matplotlib.pyplot


def test():
    hor = [random.randint(0, 100) for i in range(100)]
    ver = [random.randint(0, 100) for z in range(100)]
    matplotlib.pyplot.scatter(hor, ver, s=15, alpha=.5)
    matplotlib.pyplot.title('ZIFP')
    matplotlib.pyplot.xlabel('Word Rank')
    matplotlib.pyplot.ylabel('Words Frequency')
    matplotlib.pyplot.show()


def store_table(file_name):
    my_table = []
    heightt = -1
    widthh = 0
    with open(file_name) as csv_file:
        for line in csv_file.readlines():
            formatted = line.strip().split(',')
            my_table.append(formatted)
            heightt += 1
            widthh = len(formatted)

    return my_table, heightt, widthh


def calculate_entropy(column, tabl):
    heit = len(tabl) - 1
    wid = len(tabl[0])
    unique_feature_counts = dict()
    for row_ind in range(1, len(tabl)):
        row = tabl[row_ind]
        feat = row[column]
        outcome = tabl[row_ind][wid - 1]
        if feat in unique_feature_counts:
            counter = unique_feature_counts[feat][0] + 1
            lister = unique_feature_counts[feat][1]
            lister.append(outcome)
            unique_feature_counts[feat] = (counter, lister)
        else:
            unique_feature_counts[feat] = (1, [outcome])
    probabilities = [(unique_feature_counts[x][0] / heit, unique_feature_counts[x][1]) for x in unique_feature_counts]
    entropy = 0
    for probability, outcomes in probabilities:
        temp_dict = dict()
        entropy_1 = 0
        for i in outcomes:
            if i in temp_dict:
                temp_dict[i] = temp_dict[i] + 1
            else:
                temp_dict[i] = 1
        second_probs = [temp_dict[x] / len(outcomes) for x in temp_dict]
        for second_prob in second_probs:
            entropy_1 += (second_prob * math.log(second_prob, 2))
        entropy += probability * entropy_1
    return -entropy


def calculate_starting_entropy(tabl):
    wid = len(tabl[0])
    heit = len(tabl) - 1
    starting_entrop = 0
    decisions = dict()
    for row in tabl[1:]:
        outcome = row[wid - 1]
        if outcome in decisions:
            decisions[outcome] = decisions[outcome] + 1
        else:
            decisions[outcome] = 1

    probabilities = [decisions[x] / heit for x in decisions]
    for prob in probabilities:
        starting_entrop += (prob * math.log(prob, 2))
    return -starting_entrop


def calculate_information_gain(tabl, split):
    og_entropy = calculate_starting_entropy(tabl)
    return og_entropy - calculate_entropy(split, tabl)


def split_table(tabll, feature, value):
    indices = []
    new_table = []
    new_table.append(tabll[0])
    for row_ind in range(1, len(tabll)):
        if tabll[row_ind][feature] == value:
            indices.append(row_ind)
    for index in indices:
        new_table.append(tabll[index])
    return new_table


def find_possible_vals(table, feature):
    vals = set()
    for row_ind in range(1, len(table)):
        current_val = table[row_ind][feature]
        vals.add(current_val)
    return vals


def choose_greatest_info(table):
    max_info = -99999999
    max_info_feat = None
    width = len(table[0])
    for i in range(width - 1):
        info_gain = calculate_information_gain(table, i)
        if info_gain > max_info:
            max_info = info_gain
            max_info_feat = i
    return max_info_feat


def loop(current_table, current_tree, depth, things):
    heading = current_table[0]
    feature = choose_greatest_info(current_table)
    vals = find_possible_vals(current_table, feature)
    new_tables = [(split_table(current_table, feature, val), val) for val in vals]
    current_tree[heading[feature]] = dict()
    # print(depth * '  ', str(heading[feature]) + '?')
    depth += 1

    for new_table, value in new_tables:
        if calculate_starting_entropy(new_table) == 0:
            current_tree[heading[feature]][value] = new_table[1][len(heading) - 1]
            depth += 1
            things.add(new_table[1][len(heading) - 1])
            # print(depth * '  ' + value, '-->', new_table[1][len(heading) - 1])
            depth -= 1
        else:
            depth += 1
            # print(depth * '  ', value)
            temp_recur = loop(new_table, dict(), depth + 1, things)
            current_tree[heading[feature]][value] = temp_recur

    return current_tree, things


def classify(feature_vector, tree, outcome, headings):
    temp = None
    if isinstance(tree, str) and tree in outcome:
        # print('Classification:', tree)
        return tree
    for question, temp in tree.items():
        # print('Vector:', question)
        # print('Answer:', feature_vector[headings.index(question)])
        temp2 = feature_vector[headings.index(question)]
        try:
            temp = temp[temp2]
        except KeyError:
            temp = random.choice(tuple(temp.values()))
        if isinstance(temp, str) and temp in outcome:
            # print('Classification:', temp)
            return temp

        if isinstance(temp, tuple):
            temp = temp[0]
            if isinstance(temp, str) and temp in outcome:
                # print('Classification:', temp)
                return temp
    return classify(feature_vector, temp, outcome, headings)


def training_test(file_name):
    def check_same_classification(classifications):
        return len(set(classifications)) == 1

    table, height, width = store_table(file_name)

    width = width - 1
    NONMISSING = list()
    for row_index in range(1, height):
        if '?' not in table[row_index]:
            NONMISSING.append(table[row_index][1:])
    headers = table[0][1:]
    NONMISSING, test_set = NONMISSING[:-50], NONMISSING[-50:]
    horizontal, vertical = [], []
    for SIZE in range(5, 183):
        TRAIN = []
        for i in range(SIZE):
            TRAIN.append(random.choice(NONMISSING))
        while check_same_classification([row[width - 1] for row in TRAIN]):
            TRAIN = []
            for i in range(SIZE):
                TRAIN.append(random.choice(NONMISSING))
        TRAIN.insert(0, headers)

        generated_tree, resultants = loop(TRAIN, dict(), 0, set())
        correct_count = 0.0
        for feature_vector in test_set:
            real_outcome = feature_vector[width - 1]
            tested_outcome = classify(feature_vector, generated_tree, resultants, headers)
            if real_outcome == tested_outcome:
                correct_count += 1
        accuracy = correct_count / len(test_set)
        horizontal.append(SIZE)
        vertical.append(accuracy)
    matplotlib.pyplot.scatter(horizontal, vertical, s=15, alpha=.5)
    matplotlib.pyplot.title('House Votes Test')
    matplotlib.pyplot.xlabel('SIZE')
    matplotlib.pyplot.ylabel('ACCURACY')
    matplotlib.pyplot.show()


def eckel_input():
    file_name, test_set_size, min_training_size, max_training_size, step = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])

    def check_same_classification(classifications):
        return len(set(classifications)) == 1

    table, height, width = store_table(file_name)
    headers, table = table[0], table[1:]

    width = width - 1
    horizontal, vertical = [], []
    table, test_set = table[:-test_set_size], table[-test_set_size:]

    for SIZE in range(min_training_size, max_training_size, step):
        TRAIN = []
        for i in range(SIZE):
            TRAIN.append(random.choice(table))
        while check_same_classification([row[width] for row in TRAIN]):
            TRAIN = []
            for i in range(SIZE):
                TRAIN.append(random.choice(table))
        TRAIN.insert(0, headers)
        generated_tree, resultants = loop(TRAIN, dict(), 0, set())
        correct_count = 0.0
        for feature_vector in test_set:
            real_outcome = feature_vector[width]
            tested_outcome = classify(feature_vector, generated_tree, resultants, headers)
            if real_outcome == tested_outcome:
                correct_count += 1
        accuracy = correct_count / len(test_set)
        horizontal.append(SIZE)
        vertical.append(accuracy)
    matplotlib.pyplot.scatter(horizontal, vertical, s=15, alpha=.5)
    matplotlib.pyplot.title('SIZE VS ACCURACY')
    matplotlib.pyplot.xlabel('SIZE')
    matplotlib.pyplot.ylabel('ACCURACY')
    matplotlib.pyplot.show()


training_test("house-votes-84.csv")