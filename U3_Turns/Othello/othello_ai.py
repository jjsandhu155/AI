import math


def find_next_move(board, player, depth):
    # Based on whether player is x or o, start an appropriate version of minimax
    # that is depth-limited to "depth".  Return the best available move.
    if player == 'x':
        return max_move(board, depth, -math.inf, math.inf, player)
    if player == 'o':
        return min_move(board, depth, -math.inf, math.inf, player)


top_borders = [x for x in range(8)]
left_borders = [x for x in range(0, 57, 8)]
right_borders = [x for x in range(7, 64, 8)]
bottom_borders = [x for x in range(56, 64)]

WEIGHTS = [20, -3, 2, 2, 2, 2, -3, 20,
           -3, -5, -1, -1, -1, -1, -5, -3,
           2, -1, 1, 0, 0, 1, -1, 2,
           2, -1, 0, 1, 1, 0, -1, 2,
           2, -1, 0, 1, 1, 0, -1, 2,
           2, -1, 1, 0, 0, 1, -1, 2,
           -3, -5, -1, -1, -1, -1, -5, -3,
           20, -3, 2, 2, 2, 2, -3, 20]


def score_board(board, player):
    def filled(board):
        return (board.count('x') + board.count('o'))

    def mobility_differential(board, weight):
        x_moves = len(next_possible_boards(board, 'x'))
        o_moves = len(next_possible_boards(board, 'o'))
        return (x_moves - o_moves) * weight * 1.0

    def board_coverage(board, weight):
        return (board.count('x') - board.count('o')) * weight

    def victory_account(board):
        if game_is_over(board):
            if board.count('x') > board.count('o'):
                return 10000000000000000000
            elif board.count('x') < board.count('o'):
                return -10000000000000000
        return 0

    def weighted(board, locations):
        score = 0
        if locations:
            for p in locations:
                if board[p] == 'x':
                    score += WEIGHTS[p]
                elif board[p] == 'o':
                    score -= WEIGHTS[p]
        return score

    def get_used_positions(board):
        posses = []
        for b in range(len(board)):
            if board[b] != '.':
                posses.append(b)

    if filled(board) <= 16:  # CHANGES: Here, the heuristic calculates how much of the board is currently filled in order to gauge the stage of the game.
        # Early game mobility is prioritized while mid games smarter moves (corners, edges, etc...) are prioritized
        # and in the end board coverage is also quite important.
        # Throughout the game victory is the highest weight by a large margin.
        return mobility_differential(board, 1) + victory_account(board)
    elif filled(board) <= 35:
        return mobility_differential(board, 1) + weighted(board, get_used_positions(board)) + victory_account(board)
    else:
        return mobility_differential(board, 1) + board_coverage(board, 1) + victory_account(board)


def switch_player(player):
    if player == 'x':
        return 'o'
    if player == 'o':
        return 'x'


def max_step(board, depth, alpha, beta, player):
    if game_is_over(board) or depth == 0:
        return score_board(board, player)
    results = []
    moves = next_possible_boards(board, player)
    if not moves:
        return min_step(board, depth - 1, alpha, beta, switch_player(player))
    for next_board in moves:
        val = min_step(next_board, depth - 1, alpha, beta, switch_player(player))
        results.append(val)
        if val > alpha:  # PRUNING
            alpha = val
        if alpha >= beta:
            break
    return max(results)


def min_step(board, depth, alpha, beta, player):
    if game_is_over(board) or depth == 0:
        return score_board(board, player)
    results = []
    moves = next_possible_boards(board, player)
    if not moves:
        return max_step(board, depth - 1, alpha, beta, switch_player(player))
    for next_board in moves:
        val = max_step(next_board, depth - 1, alpha, beta, switch_player(player))
        results.append(val)
        if val > alpha:  # PRUNING
            alpha = val
        if alpha >= beta:
            break
    return min(results)


def max_move(board, depth, alpha, beta, player):
    if game_is_over(board) or depth == 0:
        return score_board(board, player)
    results = []
    moves = possible_moves(board, player)
    if not moves:
        return board
    else:
        for space in moves:
            next_board = move(board, player, space)
            val = min_step(next_board, depth - 1, alpha, beta, switch_player(player))
            results.append((val, space))
            if val > alpha:  # PRUNING
                alpha = val
            if alpha >= beta:
                break
        return sorted(results)[len(results) - 1][1]


def min_move(board, depth, alpha, beta, player):
    if game_is_over(board) or depth == 0:
        return score_board(board, player)
    results = []
    moves = possible_moves(board, player)
    if not moves:
        return board
    else:
        for space in moves:
            next_board = move(board, player, space)
            val = max_step(next_board, depth - 1, alpha, beta, switch_player(player))
            results.append((val, space))
            if val > alpha:  # PRUNING
                alpha = val
            if alpha >= beta:
                break
        return sorted(results)[0][1]


def game_is_over(board):
    if not possible_moves(board, 'x') and not possible_moves(board, 'o'):
        return True
    if board.count('.') == 0:
        return True
    return False


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
                changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp -= 8
                    changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]

            if bound_dir == 'd':
                temp = position
                changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp += 8
                    changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]
            if bound_dir == 'l':
                temp = position
                changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp -= 1
                    changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]
            if bound_dir == 'r':
                temp = position
                changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp += 1
                    changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]
            if bound_dir == 'ul':
                temp = position
                changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp -= 9
                    changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]
            if bound_dir == 'ur':
                temp = position
                changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp -= 7
                    changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]
            if bound_dir == 'dl':
                temp = position
                changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp += 7
                    changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]
            if bound_dir == 'dr':
                temp = position
                changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]
                while not temp == bounded_index:
                    temp += 9
                    changed_board = changed_board[0:temp] + token + changed_board[temp + 1:]
        return changed_board
    else:
        return board


def next_possible_boards(board, player):
    switches = possible_moves(board, player)
    possible_boards = [move(board, player, switch) for switch in switches]
    return possible_boards


class Strategy:
    def best_strategy(self, board, player, best_move, still_running):
        depth = 1
        while True:
            best_move.value = find_next_move(board, player, depth)
            depth += 1

# board = sys.argv[1]
# player = sys.argv[2]
# depth = 1
# for count in range(15):  # 15 is arbitrary; a depth that your code won't reach, but infinite loops crash the grader
#     print(find_next_move(board, player, depth))
#     depth += 1
