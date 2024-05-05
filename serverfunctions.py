#!/usr/bin/env python3

def choice_validity(board_dict, socket, num_choice):
    board = board_dict[socket]
    if not (1 <= num_choice <= 9 and board[num_choice - 1] == '-'):
        return "ILLEGAL"
    else:
        board_dict[socket] = board[:num_choice - 1] + "O" + board[num_choice:]
        return "LEGAL"


def finish_cond(board):
    for i in range(1, 10, 3):
        # check rows
        if board[i] != '-' and board[i - 1] == board[i] and board[i] == board[i + 1]:
            return True
    for i in range(3, 6):
        # check columns
        if board[i] != '-' and board[i - 3] == board[i] and board[i] == board[i + 3]:
            return True
    if board[0] != '-' and board[0] == board[4] and board[4] == board[8]:
        # check diagonal bottom-left to top-right
        return True
    if board[2] != '-' and board[2] == board[4] and board[4] == board[7]:
        # check diagonal bottom-right to top top-left
        return True
    return False


# ideally the server should play his best move
def server_move(board_dict, socket):
    board = board_dict[socket]
    for i in range(9):
        if board[i] == '-':
            board_dict[socket] = board[:i] + "X" + board[i + 1:]
            break
