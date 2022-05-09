# Othello Part 1
import sys

# Adjacency Borders to Assist Adjacent Square Calculations
top_borders = [x for x in range(8)]
left_borders = [x for x in range(0, 57, 8)]
right_borders = [x for x in range(7, 64, 8)]
bottom_borders = [x for x in range(56, 64)]


def is_bounded(ind, state, tok, opposite_tok):
    if ind not in top_borders and state[ind - 8] == opposite_tok:  # up bound
        top_temp = ind - 8
        while top_temp not in top_borders:
            top_temp -= 8
            if state[top_temp] == '.':
                break
            if state[top_temp] == tok:
                return True

    if ind not in bottom_borders and state[ind + 8] == opposite_tok:  # down bound
        bot_temp = ind + 8
        while bot_temp not in bottom_borders:
            bot_temp += 8
            if state[bot_temp] == '.':
                break
            if state[bot_temp] == tok:
                return True

    if ind not in left_borders and state[ind - 1] == opposite_tok:  # left bound
        left_temp = ind - 1
        while left_temp not in left_borders:
            left_temp -= 1
            if state[left_temp] == '.':
                break
            if state[left_temp] == tok:
                return True

    if ind not in right_borders and state[ind + 1] == opposite_tok:  # right bound
        right_temp = ind + 1
        while right_temp not in right_borders:
            right_temp += 1
            if state[right_temp] == '.':
                break
            if state[right_temp] == tok:
                return True

    if ind not in top_borders and ind not in left_borders and state[ind - 9] == opposite_tok:  # up left diagonal
        up_left = ind - 9
        while up_left not in top_borders + left_borders:
            up_left -= 9
            if state[up_left] == '.':
                break
            if state[up_left] == tok:
                return True

    if ind not in top_borders and ind not in right_borders and state[ind - 7] == opposite_tok:  # up right diagonal
        up_right = ind - 7
        while up_right not in right_borders + top_borders:
            up_right -= 7
            if state[up_right] == '.':
                break
            if state[up_right] == tok:
                return True

    if ind not in bottom_borders and ind not in left_borders and state[ind + 7] == opposite_tok:  # down left diagonal
        down_left = ind + 7
        while down_left not in bottom_borders + left_borders + right_borders:
            down_left += 7
            if state[down_left] == '.':
                break
            if state[down_left] == tok:
                return True

    if ind not in bottom_borders and ind not in right_borders and state[ind + 9] == opposite_tok:  # down right diagonal
        down_right = ind + 9
        while down_right not in bottom_borders + right_borders:
            down_right += 9
            if state[down_right] == '.':
                break
            if state[down_right] == tok:
                return True

    return False


def display_board(board):
    index = 0
    for i in range(8):
        for j in range(8):
            print(board[index], end=' ')
            index += 1
        print('')


def possible_moves(board, token):
    valid_moves = set()
    if token == 'x':
        opposite_token = 'o'
    else:
        opposite_token = 'x'
    for i in range(64):
        if board[i] == opposite_token:
            if i in top_borders and i in left_borders:
                bot_ind = i + 8
                right_ind = i + 1
                down_right_diag = i + 9
                adjacents = {bot_ind, right_ind, down_right_diag}
                adjacents = {z for z in adjacents if board[z] == '.'}
            elif i in top_borders and i in right_borders:
                bot_ind = i + 8
                left_ind = i - 1
                down_left_diag = i + 7
                adjacents = {bot_ind, left_ind, down_left_diag}
                adjacents = {z for z in adjacents if board[z] == '.'}
            elif i in bottom_borders and i in left_borders:
                top_ind = i - 8
                right_ind = i + 1
                up_right_diag = i - 7
                adjacents = {top_ind, right_ind, up_right_diag}
                adjacents = {z for z in adjacents if board[z] == '.'}
            elif i in bottom_borders and i in right_borders:
                top_ind = i - 8
                left_ind = i - 1
                up_left_diag = i - 9
                adjacents = {top_ind, left_ind, up_left_diag}
                adjacents = {z for z in adjacents if board[z] == '.'}
            elif i in top_borders:
                bot_ind = i + 8
                left_ind = i - 1
                right_ind = i + 1
                down_left_diag = i + 7
                down_right_diag = i + 9
                adjacents = {bot_ind, left_ind, right_ind,
                             down_left_diag, down_right_diag}
                adjacents = {z for z in adjacents if board[z] == '.'}
            elif i in bottom_borders:
                top_ind = i - 8
                left_ind = i - 1
                right_ind = i + 1
                up_left_diag = i - 9
                up_right_diag = i - 7
                adjacents = {top_ind, left_ind, right_ind,
                             up_left_diag, up_right_diag}
                adjacents = {z for z in adjacents if board[z] == '.'}
            elif i in left_borders:
                top_ind = i - 8
                bot_ind = i + 8
                right_ind = i + 1
                up_right_diag = i - 7
                down_right_diag = i + 9
                adjacents = {top_ind, bot_ind, right_ind,
                             up_right_diag, down_right_diag}
                adjacents = {z for z in adjacents if board[z] == '.'}
            elif i in right_borders:
                top_ind = i - 8
                bot_ind = i + 8
                left_ind = i - 1
                up_left_diag = i - 9
                down_left_diag = i + 7
                adjacents = {top_ind, bot_ind, left_ind,
                             up_left_diag, down_left_diag}
                adjacents = {z for z in adjacents if board[z] == '.'}
            else:
                top_ind = i - 8
                bot_ind = i + 8
                left_ind = i - 1
                right_ind = i + 1
                up_left_diag = i - 9
                up_right_diag = i - 7
                down_left_diag = i + 7
                down_right_diag = i + 9
                adjacents = {top_ind, bot_ind, left_ind, right_ind,
                             up_left_diag, up_right_diag, down_left_diag, down_right_diag}
                adjacents = {z for z in adjacents if board[z] == '.'}
            for index in adjacents:
                if is_bounded(index, board, token, opposite_token):
                    valid_moves.add(index)
    return sorted(valid_moves)


def is_bounded_direction(ind, state, tok, opposite_tok):
    bound_directions = set()
    if ind not in top_borders and state[ind - 8] == opposite_tok:  # up bound
        top_temp = ind - 8
        while top_temp not in top_borders:
            top_temp -= 8
            if state[top_temp] == '.':
                break
            if state[top_temp] == tok:
                bound_directions.add(('u', top_temp))
                break

    if ind not in bottom_borders and state[ind + 8] == opposite_tok:  # down bound
        bot_temp = ind + 8
        while bot_temp not in bottom_borders:
            bot_temp += 8
            if state[bot_temp] == '.':
                break
            if state[bot_temp] == tok:
                bound_directions.add(('d', bot_temp))
                break
    if ind not in left_borders and state[ind - 1] == opposite_tok:  # left bound
        left_temp = ind - 1
        while left_temp not in left_borders:
            left_temp -= 1
            if state[left_temp] == '.':
                break
            if state[left_temp] == tok:
                bound_directions.add(('l', left_temp))
                break
    if ind not in right_borders and state[ind + 1] == opposite_tok:  # right bound
        right_temp = ind + 1
        while right_temp not in right_borders:
            right_temp += 1
            if state[right_temp] == '.':
                break
            if state[right_temp] == tok:
                bound_directions.add(('r', right_temp))
                break
    if ind not in top_borders and ind not in left_borders and state[ind - 9] == opposite_tok:  # up-left diagonal bound
        up_left = ind - 9
        while up_left not in top_borders + left_borders:
            up_left -= 9
            if state[up_left] == '.':
                break
            if state[up_left] == tok:
                bound_directions.add(('ul', up_left))
                break
    if ind not in top_borders and ind not in right_borders and state[ind - 7] == opposite_tok:  # up-right diagonal bound
        up_right = ind - 7
        while up_right not in right_borders + top_borders:
            up_right -= 7
            if state[up_right] == '.':
                break
            if state[up_right] == tok:
                bound_directions.add(('ur', up_right))
                break
    if ind not in bottom_borders and ind not in left_borders and state[ind + 7] == opposite_tok:  # down-left diagonal bound
        down_left = ind + 7
        while down_left not in bottom_borders + left_borders + right_borders:
            down_left += 7
            if state[down_left] == '.':
                break
            if state[down_left] == tok:
                bound_directions.add(('dl', down_left))
                break
    if ind not in bottom_borders and ind not in right_borders and state[ind + 9] == opposite_tok:  # down-right diagonal bound
        down_right = ind + 9
        while down_right not in bottom_borders + right_borders:
            down_right += 9
            if state[down_right] == '.':
                break
            if state[down_right] == tok:
                bound_directions.add(('dr', down_right))
                break

    return bound_directions


def move(board, token, position):
    if token == 'x':
        opposite_token = 'o'
    else:
        opposite_token = 'x'
    list_of_bounds = is_bounded_direction(
        position, board, token, opposite_token)
    changed_board = board
    if list_of_bounds:
        for bound_dir, bounded_index in list_of_bounds:
            if bound_dir == 'u':
                temp = position
                changed_board = changed_board[0:temp] + \
                                token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp -= 8
                    changed_board = changed_board[0:temp] + \
                                    token + changed_board[temp + 1:]

            if bound_dir == 'd':
                temp = position
                changed_board = changed_board[0:temp] + \
                                token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp += 8
                    changed_board = changed_board[0:temp] + \
                                    token + changed_board[temp + 1:]
            if bound_dir == 'l':
                temp = position
                changed_board = changed_board[0:temp] + \
                                token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp -= 1
                    changed_board = changed_board[0:temp] + \
                                    token + changed_board[temp + 1:]
            if bound_dir == 'r':
                temp = position
                changed_board = changed_board[0:temp] + \
                                token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp += 1
                    changed_board = changed_board[0:temp] + \
                                    token + changed_board[temp + 1:]
            if bound_dir == 'ul':
                temp = position
                changed_board = changed_board[0:temp] + \
                                token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp -= 9
                    changed_board = changed_board[0:temp] + \
                                    token + changed_board[temp + 1:]
            if bound_dir == 'ur':
                temp = position
                changed_board = changed_board[0:temp] + \
                                token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp -= 7
                    changed_board = changed_board[0:temp] + \
                                    token + changed_board[temp + 1:]
            if bound_dir == 'dl':
                temp = position
                changed_board = changed_board[0:temp] + \
                                token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp += 7
                    changed_board = changed_board[0:temp] + \
                                    token + changed_board[temp + 1:]
            if bound_dir == 'dr':
                temp = position
                changed_board = changed_board[0:temp] + \
                                token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp += 9
                    changed_board = changed_board[0:temp] + \
                                    token + changed_board[temp + 1:]
        return changed_board
    else:
        return board


def in_and_out():
    puzzle, player = sys.argv[1:3]
    moves = possible_moves(puzzle, player)
    print(moves)
    for switch in moves:
        print(move(puzzle, player, switch))


in_and_out()
