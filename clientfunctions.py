#!/usr/bin/env python3

def game_seq_progress(message_type, o1, o2, o3, o4, o5, o6, o7, o8,
                      o9):  # Returns True if game continues and False if game is over.
    indicator = True
    if message_type == 0:  # INITIAL SERVER MESSAGE
        print("Now you are playing against the server!")
        print_board(o1, o2, o3, o4, o5, o6, o7, o8, o9)
        print("Your turn:")
    elif message_type == 1:  # LEGAL MOVE
        print("Move accepted")
        print_board(o1, o2, o3, o4, o5, o6, o7, o8, o9)
        print("Your turn:")
    elif message_type == 2:  # ILLEGAL MOVE
        print("Illegal move")
        print_board(o1, o2, o3, o4, o5, o6, o7, o8, o9)
        print("Your turn:")
    elif message_type == 3:  # WIN
        print("Move accepted")
        print_board(o1, o2, o3, o4, o5, o6, o7, o8, o9)
        print("You win!")
        indicator = False
    elif message_type == 4:  # LOSE
        print("Move accepted")
        print_board(o1, o2, o3, o4, o5, o6, o7, o8, o9)
        print("Server win!")
        indicator = False
    elif message_type == 5:  # ILLEGAL AND GAMEOVER SIMULTANEOUSLY
        print("Illegal move")
        print_board(o1, o2, o3, o4, o5, o6, o7, o8, o9)
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
        return False
    else:
        try:
            num = int(input_segments[0])
            if not (1 <= num <= 9):
                return False

        except ValueError:
            print('please insert an integer')
            return False

        return True


def print_board(o1, o2, o3, o4, o5, o6, o7, o8, o9):
    print(f'{o1} {o2} {o3}\n')
    print(f'{o4} {o5} {o6}\n')
    print(f'{o7} {o8} {o9}\n')
