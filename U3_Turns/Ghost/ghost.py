import sys

alphabet = 'abcdefghijklmnopqrstuvwxyz'


def input_output():
    with open(sys.argv[1]) as f:
        word_list = [line.strip().lower() for line in f if len(line.strip()) >= int(sys.argv[2]) and line.strip().isalpha()]
    if len(sys.argv) == 4:
        current_word = sys.argv[3].lower()
    else:
        current_word = ''
    move = [a.upper() for a in min_move(current_word, word_list, '1')]
    if move:
        print('Next player can guarantee victory by playing any of these letters:', move)
    else:
        print('Next player will lose!')


def game_is_over(word, dictionary):
    if word in dictionary:
        return True
    return False


def switch_player(player):
    if player == '1':
        return '2'
    if player == '2':
        return '1'


def score_board(word, player, dictionary):
    if word in dictionary:
        if player == '1':
            return -1
        if player == '2':
            return 1
    return 0


def next_possible_boards(word, dictionary):
    possible_boards = []
    for letter in alphabet:
        temp = word + letter
        for d in dictionary:
            if d.startswith(temp):
                possible_boards.append((temp, letter))
                break
    return possible_boards, {d for d in dictionary if d.startswith(word)}


def min_step(board, dictionary, player):
    if game_is_over(board, dictionary):
        return score_board(board, player, dictionary)
    results = []
    moves, new_dictionary = next_possible_boards(board, dictionary)
    if len(moves) == 0:
        results.append(max_step(board, new_dictionary, switch_player(player)))
    else:
        for next_board in moves:
            results.append(max_step(next_board[0], new_dictionary, switch_player(player)))
    return min(results)


def max_step(board, dictionary, player):
    if game_is_over(board, dictionary):
        return score_board(board, player, dictionary)
    results = []
    moves, new_dictionary = next_possible_boards(board, dictionary)
    if len(moves) == 0:
        results.append(min_step(board, new_dictionary, switch_player(player)))
    else:
        for next_board in moves:
            results.append(min_step(next_board[0], new_dictionary, switch_player(player)))
    return max(results)


def min_move(board, dictionary, player):
    if game_is_over(board, dictionary):
        return score_board(board, player, dictionary)
    results = []
    moves, new_dictionary = next_possible_boards(board, dictionary)
    for next_board in moves:
        results.append((max_step(next_board[0], new_dictionary, switch_player(player)), next_board[1]))
    return [move for value, move in results if value == -1]


def max_move(board, dictionary, player):
    if game_is_over(board, dictionary):
        return score_board(board, player, dictionary)
    results = []
    moves, new_dictionary = next_possible_boards(board, dictionary)
    for next_board in moves:
        results.append((min_step(next_board[0], new_dictionary, switch_player(player)), next_board[1]))
    return [move for value, move in results if value == 1]


input_output()
