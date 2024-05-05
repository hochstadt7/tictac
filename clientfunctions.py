#!/usr/bin/env python3

def game_seq_progress(message_type, board):  # Returns True if game continues and False if game is over.
    indicator = True
    if message_type == 0:  # INITIAL SERVER MESSAGE
        print("Now you are playing against the server!")
        _print_board(board)
        print("Your turn:")
    elif message_type == 1:  # LEGAL MOVE
        print("Move accepted")
        _print_board(board)
        print("Your turn:")
    elif message_type == 2:  # ILLEGAL MOVE
        print("Illegal move")
        _print_board(board)
        print("Your turn:")
    elif message_type == 3:  # WIN
        print("Move accepted")
        _print_board(board)
        print("You win!")
        indicator = False
    elif message_type == 4:  # LOSE
        print("Move accepted")
        _print_board(board)
        print("Server win!")
        indicator = False
    elif message_type == 5:  # ILLEGAL AND GAMEOVER SIMULTANEOUSLY
        print("Illegal move")
        _print_board(board)
        print("Server win!")  # client can't win in such a case
        indicator = False
    elif message_type == 6:  # WAITING LIST
        print("Waiting to play against the server.")
        indicator = True
    elif message_type == 7:  # REJECTION
        print("You are rejected by the server.")
        indicator = False
    return indicator


def is_valid_input(input_string):
    input_segments = input_string.split()
    if len(input_segments) != 1:
        print("Expected 1-length input string")
        return False
    else:
        try:
            num = int(input_segments[0])
            if not (1 <= num <= 9):
                return False

        except ValueError:
            print('Please insert an integer')
            return False

        return True


def _print_board(board):
    for i in range(3):
        for j in range(3):
            print(board[3 * i + j], end=" ")
        print("")
