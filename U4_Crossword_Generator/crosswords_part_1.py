# Began 2/9/2020 in Class - Video, Read Spec, Downloaded Files
from sys import argv


def intake_format():
    """
    Takes Sys Arguments, Translates to Tangible Information

    :return:
    height (int) : height/number of rows of crossword puzzle
    width (int) : width/number of columns of crossword puzzle
    number_of_blocking_squares (int) : the number of desired blocking squared for the crossword
    word_list (String) : the filename of the desired dictionary
    seed_strings_formatted (Tuple) : Contains H or V for Orientation Direction, Row # Vertical, Column # Horizontal, Word Placed
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    height, width = (int(x) for x in argv[1].split('x'))
    number_of_blocking_squares = int(argv[2])
    word_list = argv[3]
    seed_strings_raw = argv[4:]
    seed_strings_formatted = []
    for seed_string in seed_strings_raw:
        orientation, interest = seed_string[0], seed_string[1:]
        x_index, beginning_of_word = interest.index('x'), 100
        for index in range(len(interest)):
            if index != x_index and interest[index].lower() in alphabet:
                beginning_of_word = index
                break
        row, column = (int(x) for x in interest[:beginning_of_word].split('x'))
        word = interest[beginning_of_word:]
        seed_strings_formatted.append((orientation, row, column, word.upper()))
    return height, width, number_of_blocking_squares, word_list, seed_strings_formatted


def check_intake(height, width, number_of_blocking_squares, word_list, seed_strings_formatted):
    """
    Simple Print Check to Ensure Proper Input Processing

    :param: Takes Intake Format
    """
    print('Height:', height)
    print('Width:', width)
    print('# Blocking Squares:', number_of_blocking_squares)
    print('Dictionary:', word_list)
    for s in seed_strings_formatted:
        print(s)


def place_seed_strings(seed_strings, height, width):
    """
    Places Seed Strings to Compose Initial Board

    :param seed_strings: List of Seeds or (H/V, Row, Column, Word)
    :param height: Puzzle Height/Number of Rows
    :param width: Puzzle Width/Number of Columns

    :return: Initialized Board With Seed Strings Placed
    """

    board = []
    for i in range(height):
        row = []
        for z in range(width):
            row.append('-')
        board.append(row)
    for seed in seed_strings:
        orientation, row, column, word = seed
        if orientation == 'H':
            for i in range(len(word)):
                board[row][column + i] = word[i]
        if orientation == 'V':
            for i in range(len(word)):
                board[row + i][column] = word[i]
    return board


def display_board(board):
    for row in board:
        for space in row:
            print(space, end=' ')
        print('')


def is_rotationally_symmetrical(board):
    """
    Tests Whether or Not a Board Follows Crossword Convention of Being 180 Degrees Rotationally Symmetric
    :param board: Crossword Puzzle State
    :return: True or False Indicating Symmetry
    """

    return stringified_board == stringified_board[::-1]


def is_section_disconnected(board):
    """

    :param board:
    :return:
    """


def stringified_board(board):
    stringed_board = ''
    for row in board:
        for column in board:
            stringed_board += str(board[row][column])


def is_palindrome(word):
    return word == word[::-1]


print(is_palindrome('-----##-----------##------------#----------#----#------#----#-------#---#-----###---#---###-----#---#-------#----#------#----#----------#------------##-----------##-----'))
