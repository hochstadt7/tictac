Web application in a server / client structure, for the Nim game. The server plays against several clients. It maintains a waiting list of non-gaming customers, sorted by their login order.
The waiting list is completed in turn, which means that as soon as an active player leaves the game, the first player on the waiting list will start playing against the server.
The waiting list is limited, therefore any client can either play against the server, be on the waiting list or be rejected by the server.

To establish a connection from the server side, the following command should be ran: python3 tictac-server.py _num_players_ _wait_list_size_ [port_num]
where: _num_players_ is the maximum number of clients/players whcih may play against the (same) server simultaneously, _wait_list_size_ is the maximum size of the list containing waiting-to-play
clients, [port_num] is an optional parameter representing the port number to use for connection/communication with the clients.
Then, to connect to the server as a client, the following command should be run:
python3 tictac.py [hostName] [portNum]
where: [hostName] is the host name used for the connection with the server and [portNum] is the port number used for the connection.

Imagine a standart 3x3 board game, numbered from 1 to 9: [[1, 2, 3], [4, 5, 6], [7, 8, 9]].
The initial (empty) board is printed.
The current client makes the first move. He is requested to give as input a number between 1-9, representing the square in which he want to put circle (O).
Then comes the server's response, and so on. After each move, the new board after applying the requesed change is printed.
Following each move, it is being checked whether the game is over, and if so, the winner is declared and the connection is paused, which allows the next client in the waiting list to become an active player.
If the client gives a wrong input, its turn is skipped, and the server makes another move.
A client may quit the game in the middle, if he inserts "Q" as an input, causing the termination of the game and a disconnection from the server.
