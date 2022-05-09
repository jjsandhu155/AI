import math
import sys


class Node:
    def __init__(self, data):
        self.children = []
        self.leaf = True
        self.data = data

    def add_child(self, key):
        temp_list = self.children
        temp_list.append(Node(key))
        self.children = temp_list

    def update_leaf_status(self):
        if self.children:
            self.leaf = False
        else:
            self.leaf = True


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


def loop(current_table, current_tree, depth, filename):
    heading = current_table[0]
    feature = choose_greatest_info(current_table)
    vals = find_possible_vals(current_table, feature)
    new_tables = [(split_table(current_table, feature, val), val) for val in vals]

    current_tree[heading[feature]] = dict()
    print(depth * '  ', str(heading[feature]) + '?', file=filename)
    depth += 1

    for new_table, value in new_tables:
        if calculate_starting_entropy(new_table) == 0:
            current_tree[heading[feature]][value] = new_table[1][len(heading) - 1]
            depth += 1
            print(depth * '  ' + value, '-->', new_table[1][len(heading) - 1], file=filename)
            depth -= 1
        else:
            depth += 1
            print(depth * '  ', value, file=filename)
            temp_recur = loop(new_table, dict(), depth + 1, filename)
            current_tree[heading[feature]][value] = temp_recur

    return current_tree


file_out = open("treeout.txt", 'w')
tab, height, width = store_table(sys.argv[1])
tree = loop(tab, dict(), 0, file_out)
