# Tic Tac Toe
import sys


def score_board(board, current_player):  # determines if the current_player won, drew, or lost the game
    resultant = game_is_over(board)[1]
    if resultant == 'Draw':
        return 0
    if resultant == current_player:
        return 1
    if resultant == switch_player(current_player):
        return -1


def switch_player(current_player):  # Simple helper for negamax that changes the current_player
    if current_player == 'X':
        return 'O'
    if current_player == 'O':
        return 'X'


def negamax(board, current_player):  # negamax function returning expected outcome
    if game_is_over(board)[0]:
        return score_board(board, current_player)
    results = []
    for next_board in next_possible_boards(board, current_player):
        temp = -negamax(next_board, switch_player(current_player))
        results.append(temp)
    return max(results)


def negamax_move(board, current_player):  # negamax function returning best move
    if game_is_over(board)[0]:
        return score_board(board, current_player)
    results = []
    for next_board in next_possible_boards(board, current_player):
        temp = -1 * negamax(next_board, switch_player(current_player))
        results.append((temp, next_board))
    return sorted(results)[len(results) - 1][1]


def next_possible_boards(board, current_player):  # generates possible tic-tac-toe moves
    posses = []
    for i in range(9):
        if board[i] == '.':
            posses.append(board[:i] + current_player + board[i + 1:])
    if posses:
        return posses
    else:
        return None


def display_board(board):  # prints formatted tic-tac-toe board
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


def game_is_over(board):  # checks if game is over: if the game is over it will return the result of the game (X wins, O wins, draw)
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

    return False, 'RandomBS'


def player_turn(board, character_symb):  # handles user input for a player move
    print('Current board:')
    display_board(board)
    empty = []
    for i in range(len(board)):
        if board[i] == '.':
            empty.append(i)
    print('You can move to any of these spaces:', empty)
    move = int(input('Your Choice?'))
    return board[0:move] + character_symb + board[move + 1:]


def computer_turn(board, character_symb):  # handles ai move selection + output
    pos = None
    sample = None
    possible_moves = next_possible_boards(board, character_symb)
    outcomes = []
    print('Current Board:')
    display_board(board)
    for move in possible_moves:
        for i in range(len(board)):
            if board[i] != move[i]:
                pos = str(i)
        result = negamax(move, switch_player(character_symb))
        if result == -1:
            sample = 'win'
            outcomes.append((-1, pos, move))
        if result == 0:
            sample = 'tie'
            outcomes.append((0, pos, move))
        if result == 1:
            sample = 'loss'
            outcomes.append((1, pos, move))
        print('Moving at %s results in a %s' % (pos, sample))
        sample = None
    outcomes = sorted(outcomes)
    print()
    print('I choose space %s' % outcomes[0][1])
    print()
    return outcomes[0][2]


def game():  # deals with output formatting + puts the tic-tac-toe game together
    first, computer_is, player_is = None, None, None
    board = sys.argv[1]
    if board.count('.') == 9:
        computer_is = str(input("Should I(Computer) be X or O? "))
        print()
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


game()
