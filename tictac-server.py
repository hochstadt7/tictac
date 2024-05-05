import socket
import sys
from select import select
from serverfunctions import *
from struct import *

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 6444  # Port to listen on (non-privileged ports are > 1023)

num_players = 0
wait_list_size = 0

if len(sys.argv) != 3 and len(sys.argv) != 4:
    print("Unappropriate arguments")
    sys.exit(1)

if len(sys.argv) == 4:
    num_players = int(sys.argv[1])
    wait_list_size = int(sys.argv[2])
    PORT = int(sys.argv[3])

else:
    num_players = int(sys.argv[1])
    wait_list_size = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(wait_list_size)

sockets = [sock]
current_players = []
wait_list = []
outputs = []

recv_dict = {sock: b""}
send_dict = {}
board_dict = {}

while True:
    '''In transmission protocol 0:INITIAL MESSAGE, 1:LEGAL, 2:ILLEGAL, 3:WIN, 4:LOSE, 5:ILLEGAL AND GAMEOVER SIMULTANEOUSLY, 6:WAITING LIST' 7:REJECTION'''
    read, write, err = select(sockets, outputs, [])
    for socket in read:
        if socket == sock:
            try:
                conn, addr = sock.accept()
                if len(current_players) < num_players:  # new player

                    sockets.append(conn)
                    current_players.append(conn)
                    outputs.append(conn)

                    send_dict[conn] = pack(">iccccccccc3s", 0, b'-', b'-', b'-', b'-', b'-', b'-',
                                           b'-', b'-', b'-',
                                           "end".encode())
                    board_dict[conn] = ['-' for i in range(9)]
                    recv_dict[conn] = b""

                else:
                    if len(wait_list) < wait_list_size:  # wait in the waiting list
                        sockets.append(conn)
                        wait_list.append(conn)
                        outputs.append(conn)

                        send_dict[conn] = pack(">iccccccccc3s", 6, b'-', b'-', b'-', b'-', b'-', b'-',
                                               b'-', b'-', b'-',
                                               "end".encode())  # message to send
                        recv_dict[conn] = b""

                    else:  # rejection message
                        send_dict[conn] = pack(">iccccccccc3s", 7, b'-', b'-', b'-', b'-', b'-', b'-',
                                               b'-', b'-', b'-',
                                               "end".encode())
                        sockets.append(conn)
                        outputs.append(conn)


            except OSError as error:
                print("Failed to initialize connection with the client")

        else:
            packed = socket.recv(3)
            if len(packed) == 0:  # disconnection
                refused = 0
                sockets.remove(socket)

                if socket in wait_list:
                    wait_list.remove(socket)
                elif socket in current_players:
                    current_players.remove(socket)
                    board_dict.pop(socket)
                else:
                    refused = 1
                if socket in recv_dict:
                    recv_dict.pop(socket)
                if socket in send_dict:
                    send_dict.pop(socket)
                if socket in outputs:
                    outputs.remove(socket)
                socket.close()

                if len(wait_list) > 0 and not refused:  # waiting player is allowed to play

                    new_player = wait_list[0]
                    current_players.append(new_player)
                    outputs.append(new_player)
                    wait_list.remove(new_player)

                    recv_dict[new_player] = b""
                    send_dict[new_player] = pack(">iccccccccc3s", 0, b'-', b'-', b'-', b'-', b'-', b'-',
                                                 b'-', b'-', b'-',
                                                 "end".encode())
                    board_dict[new_player] = ['-' for i in range(9)]

            else:
                recv_dict[socket] += packed
                if recv_dict[socket][-3:] == b"end":  # message was fully read
                    outputs.append(socket)
                    data = unpack(">ii", recv_dict[socket][:8])
                    recv_dict[socket] = b""
                    message_type, num_taken = data

                    #  illegal input. special case when user input in invalid.
                    if message_type == 2:
                        # the user loses his turn, server plays another turn
                        server_move(board_dict[socket])
                        if finish_cond(board_dict[socket]):  # illegal input and server win
                            send_dict[socket] = pack(">iccccccccc3s", 5, b'-', b'-', b'-', b'-', b'-', b'-',
                                                     b'-', b'-', b'-', "end".encode())
                        else:
                            send_dict[socket] = pack(">iccccccccc3s", 2, board_dict[socket][0].encode(),
                                                     board_dict[socket][1].encode(),
                                                     board_dict[socket][2].encode(),
                                                     board_dict[socket][3].encode(), board_dict[socket][4].encode(),
                                                     board_dict[socket][5].encode(),
                                                     board_dict[socket][6].encode(), board_dict[socket][7].encode(),
                                                     board_dict[socket][8].encode(), "end".encode())

                    else:
                        validity = choice_validity(board_dict[socket], num_taken)

                        if validity == 'LEGAL':
                            # client wins
                            if finish_cond(board_dict[socket]):
                                send_dict[socket] = pack(">iccccccccc3s", 3, b'-', b'-', b'-', b'-', b'-', b'-',
                                                         b'-', b'-', b'-', "end".encode())
                            # regular progression
                            else:
                                server_move(board_dict[socket])
                                if finish_cond(board_dict[socket]):
                                    send_dict[socket] = pack(">iccccccccc3s", 4, board_dict[socket][0].encode(),
                                                             board_dict[socket][1].encode(),
                                                             board_dict[socket][2].encode(),
                                                             board_dict[socket][3].encode(),
                                                             board_dict[socket][4].encode(),
                                                             board_dict[socket][5].encode(),
                                                             board_dict[socket][6].encode(),
                                                             board_dict[socket][7].encode(),
                                                             board_dict[socket][8].encode(), "end".encode())
                                else:
                                    send_dict[socket] = pack(">iccccccccc3s", 1, board_dict[socket][0].encode(),
                                                             board_dict[socket][1].encode(),
                                                             board_dict[socket][2].encode(),
                                                             board_dict[socket][3].encode(),
                                                             board_dict[socket][4].encode(),
                                                             board_dict[socket][5].encode(),
                                                             board_dict[socket][6].encode(),
                                                             board_dict[socket][7].encode(),
                                                             board_dict[socket][8].encode(), "end".encode())
                        elif validity == 'ILLEGAL':
                            server_move(board_dict[socket])
                            if finish_cond(board_dict[socket]):  # illegal turn and server win
                                send_dict[socket] = pack(">iccccccccc3s", 5, b'-', b'-', b'-', b'-', b'-', b'-',
                                                         b'-', b'-', b'-', "end".encode())
                            else:
                                send_dict[socket] = pack(">iccccccccc3s", 2, board_dict[socket][0].encode(),
                                                         board_dict[socket][1].encode(),
                                                         board_dict[socket][2].encode(),
                                                         board_dict[socket][3].encode(), board_dict[socket][4].encode(),
                                                         board_dict[socket][5].encode(),
                                                         board_dict[socket][6].encode(), board_dict[socket][7].encode(),
                                                         board_dict[socket][8].encode(), "end".encode())

    for socket in write:
        bytes_sent = socket.send(send_dict[socket][:3])
        send_dict[socket] = send_dict[socket][bytes_sent:]

        if send_dict[socket] == b"":  # message was fully sent
            outputs.remove(socket)
