#!/usr/bin/env python3

import socket
import sys
from struct import *
import clientfunctions
from select import select


def create_socket(hostname, port):
    global sock

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
    except OSError as error:
        print("Failed to initialize connection")
        sys.exit(1)


def tictactoc_client(hostname, port):
    global sock
    create_socket(hostname, port)
    inputs = [sock, sys.stdin]
    outputs = []
    recv_dict = {sys.stdin: "",sock: b""}  # message from server
    send_dict = {sock: b""} # message for server
    expect_input = 0

    while True:
        readable, writable, exp = select(inputs, outputs, [])
        for obj in readable:
            if obj is sys.stdin:
                packed = input()
                recv_dict[obj] += packed
                splitter=recv_dict[obj].split()
                if len(splitter) == 1 and splitter[0] == "Q":  # quit
                    sock.close()
                    sys.exit(1)
                if not expect_input: # input not in client turn get dropped
                    recv_dict[obj] = ""
                else:
                    expect_input = 0
                    if clientfunctions.is_valid_input(recv_dict[obj]):
                        num = recv_dict[obj].split()[0]
                        num = int(num)
                        send_dict[sock] = pack(">ii3s", 0, num, "end".encode())
                    else:
                        send_dict[sock] = pack(">ii3s", 2, 0, "end".encode())
                    outputs.append(sock)
                    recv_dict[obj] = ""

            else:
                packed = obj.recv(3)
                if len(packed) == 0: # disconnection
                    print("Disconnected from server")
                    sys.exit(1)
                recv_dict[obj] += packed
                if recv_dict[obj][-3:]== b"end":  # message was fully read
                    data = unpack(">i9s", recv_dict[obj][:-3])
                    recv_dict[obj] = b""
                    message_type, board = data
                    game_continue = clientfunctions.game_seq_progress(message_type, board.decode())

                    if not game_continue:
                        sock.close()
                        sys.exit(1)
                    if not message_type == 6: # no expected input from client in waiting list
                        expect_input = 1

        for obj in writable:
            bytes_sent = obj.send(send_dict[obj][:3])
            send_dict[obj] = send_dict[obj][bytes_sent:]
            if send_dict[obj] == b"": # message was fully sent
                outputs.remove(obj)



# get inputs for connection of client side

if __name__ == '__main__':
    if len(sys.argv) > 3:
        print("Unappropriate arguments")
        sys.exit(1)

    if len(sys.argv) == 3:
        tictactoc_client(sys.argv[1], int(sys.argv[2]))

    elif len(sys.argv) == 2:
        tictactoc_client(sys.argv[1], 6444)

    else:
        tictactoc_client('localhost', 6444)