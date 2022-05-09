# Tic Tac Toe
import sys


def display_board(board):
    index = 0
    start = 0
    for i in range(3):
        for j in range(3):
            print(board[index], end=' ')
            index += 1
        print('', end='   ')
        for x in range(start, start + 3):
            print(x, end=' ')
        start += 3
        print('')
    print()


def current_player_is(board):
    if board.count('X') == board.count('O'):
        return 'X'
    else:
        return 'O'


def next_possible_boards(board):
    current_player = current_player_is(board)
    posses = []
    for i in range(9):
        if board[i] == '.':
            posses.append(board[:i] + current_player + board[i + 1:])
    if posses:
        return posses
    else:
        return None


def game_is_over(board):
    if board[2] == board[4] == board[6] == 'X':  # Backwards Diagonal
        return True, 'X'

    if board[2] == board[4] == board[6] == 'O':  # Backwards Diagonal
        return True, 'O'

    if board[0] == board[4] == board[8] == 'X':  # Forwards Diagonal
        return True, 'X'

    if board[0] == board[4] == board[8] == 'O':  # Forwards Diagonal
        return True, "O"

    for i in range(3):  # Columns
        if board[i] == board[i + 3] == board[i + 6] == 'X':
            return True, "X"

        if board[i] == board[i + 3] == board[i + 6] == 'O':
            return True, 'O'

    for i in range(0, 9, 3):  # Rows
        if board[i] == board[i + 1] == board[i + 2] == 'X':
            return True, 'X'

        if board[i] == board[i + 1] == board[i + 2] == 'O':
            return True, 'O'

    if '.' not in board:
        return True, 'Draw'

    return False, next_possible_boards(board)


def min_step(board):
    if game_is_over(board)[0]:
        return score_board(board)
    results = []
    for next_board in next_possible_boards(board):
        results.append(max_step(next_board))
    return min(results)


def max_step(board):
    if game_is_over(board)[0]:
        return score_board(board)
    results = []
    for next_board in next_possible_boards(board):
        results.append(min_step(next_board))
    return max(results)


def min_move(board):
    if game_is_over(board)[0]:
        return score_board(board)
    results = []
    for next_board in next_possible_boards(board):
        results.append(max_step(next_board))
    return sorted(results)[0][1]


def max_move(board):
    if game_is_over(board):
        return score_board(board)
    results = []
    for next_board in next_possible_boards(board):
        results.append((min_step(next_board), next_board))
    return sorted(results)[len(results) - 1][1]


def player_turn(board, character_symb):
    print('Current board:')
    display_board(board)
    empty = []
    for i in range(len(board)):
        if board[i] == '.':
            empty.append(i)
    print('You can move to any of these spaces:', empty)
    move = int(input('Your Choice?'))
    return board[0:move] + character_symb + board[move + 1:]


def computer_turn(board, character_symb):
    pos = None
    sample = None
    possible_moves = next_possible_boards(board)
    outcomes = []
    for move in possible_moves:
        for i in range(len(board)):
            if board[i] != move[i]:
                pos = str(i)
        if character_symb == 'X':
            result = min_step(move)
            if result == 1:
                sample = 'win'
                outcomes.append((1, pos, move))
            if result == 0:
                sample = 'tie'
                outcomes.append((0, pos, move))
            if result == -1:
                sample = 'loss'
                outcomes.append((-1, pos, move))
            print('Moving at %s results in a %s' % (pos, sample))

        else:
            result = max_step(move)
            if result == 1:
                sample = 'loss'
                outcomes.append((1, pos, move))
            if result == 0:
                sample = 'tie'
                outcomes.append((0, pos, move))
            if result == -1:
                sample = 'win'
                outcomes.append((-1, pos, move))
            print('Moving at %s results in a %s' % (pos, sample))
    outcomes = sorted(outcomes)
    if character_symb == 'X':
        print()
        print('I choose space %s' % outcomes[len(outcomes) - 1][1])
        print()
        return outcomes[len(outcomes) - 1][2]
    else:
        print()
        print('I choose space %s' % outcomes[0][1])
        print()
        return outcomes[0][2]


def score_board(board):
    resultant = game_is_over(board)
    if resultant[1] == 'X':
        return 1
    if resultant[1] == 'O':
        return -1
    if resultant[1] == 'Draw':
        return 0


def print_directions():
    print('Hello, Welcome to a Game of Tic Tac Toe!')
    print('Simply Follow the Prompts to Play a Game Against an Artificial Intelligence Based Tic Tac Toe Bot!')
    print('Just Make Moves When Prompted, And the Bot Will Play Against You, Showing its Thought Process Too!')


def ai():
    print_directions()
    first, computer_is, player_is = None, None, None
    board = "........."
    if board.count('.') == 9:
        computer_is = str(input("Should I(Computer) be X or O? "))
        print('Current Board:')
        display_board(board)
        if computer_is == 'X':
            player_is = 'O'
            first = 'c'

        if computer_is == 'O':
            player_is = 'X'
            first = 'p'
    else:
        first = 'c'
        if board.count('X') == board.count('O'):
            computer_is = 'X'
            player_is = 'O'
        else:
            computer_is = 'O'
            player_is = 'X'
    if first == 'c':
        if game_is_over(board)[0]:
            if computer_is == game_is_over(board)[1]:
                print('Current board:')
                display_board(board)
                print()
                print('I win!')
                sys.exit(0)
            elif player_is == game_is_over(board)[1]:
                print('Current board:')
                display_board(board)
                print()
                print('You win!')
                sys.exit(0)
            else:
                print('Current board:')
                display_board(board)
                print()
                print('We Tied!')
                sys.exit(0)

        while not game_is_over(board)[0]:
            board = computer_turn(board, computer_is)
            if game_is_over(board)[0]:
                if computer_is == game_is_over(board)[1]:
                    print('Current board:')
                    display_board(board)
                    print()
                    print('I win!')
                    sys.exit(0)
                elif player_is == game_is_over(board)[1]:
                    print('Current board:')
                    display_board(board)
                    print()
                    print('You win!')
                    sys.exit(0)
                else:
                    print('Current board:')
                    display_board(board)
                    print()
                    print('We Tied!')
                    sys.exit(0)
            board = player_turn(board, player_is)

    elif first == 'p':
        if game_is_over(board)[0]:
            if computer_is == game_is_over(board)[1]:
                print('Current board:')
                display_board(board)
                print()
                print('I win!')
                sys.exit(0)
            elif player_is == game_is_over(board)[1]:
                print('Current board:')
                display_board(board)
                print()
                print('You win!')
                sys.exit(0)
            else:
                print('Current board:')
                display_board(board)
                print()
                print('We Tied!')
                sys.exit(0)
        while not game_is_over(board)[0]:
            board = player_turn(board, player_is)
            if game_is_over(board)[0]:
                if computer_is == game_is_over(board)[1]:
                    print('Current board:')
                    display_board(board)
                    print()
                    print('I win!')
                    sys.exit(0)
                elif player_is == game_is_over(board)[1]:
                    print('Current board:')
                    display_board(board)
                    print()
                    print('You win!')
                    sys.exit(0)
                else:
                    print('Current board:')
                    display_board(board)
                    print()
                    print('We Tied!')
                    sys.exit(0)
            board = computer_turn(board, computer_is)


ai()
