###### Part 1

1. we can see that the client side works fine but the connection with the server fails to be done so there is no 	answer coming back from the server side and an error is being shown.
2. The server needs to bind to a port because it needs to have a specified port from which it is going to expect the 	incoming "message", on the other hand the clients UDP know where it will send the "message" so it doesn't 	need to bind to any port
3. The server registers the address and port number of the clients the moment the clients message is sent to the 	server and then the server send the reply in the same address it got the message from.

###### Part 2

1. In TCP there is not connection being made also, therefore because TCP uses a three ways handshake it first needs 	to secure the connection to the server then to send and receive the message, but because our server wasn't 	started yet, there is immediately an error appearing.

2\. Because it is a TCP connection, the three-way handshake has to be done so this connection is complete and that's         	why the server creates a new socket for each accepted connection so that server Socket can continue 	listening for new clients while connection Socket handles communication with the connected client.

3\. This is because in TCP the clients message already knows its path from the process of connection and directly 	send the message without the need to specify where it should be send just like in UDP

###### Part 3

*Run the client three times. Write down the port numbers.*



*a)Is the client's port the same every time? Who chose it?*

*b)Does the port the server prints match the port the client prints?*



1)Client socket address: ('0.0.0.0', 63757)

2)Client socket address: ('0.0.0.0', 61052)

3)Client socket address: ('0.0.0.0', 50493)

a)The clients port is not the same, it is chosen automatically during the connection process.

b)Yes it matches, because we are using UDP they have to match otherwise the message would have been sent and received 

Run	Client socket (IP, port)	Connection socket (IP, port)	Connection socket peer

1	('127.0.0.1', 53438)		('127.0.0.1', 12000)		('127.0.0.1', 53438)	

2	('127.0.0.1', 54816)		('127.0.0.1', 12000)		('127.0.0.1', 54816)





1. Even that every connection uses port 1200 each of them has a different source port (just like in the above example). Thats what also differs them appart.
2. The ports are identical. The client's socket address is the same as the peer address reported by the server's connection socket because both refer to the client's endpoint.
3. The welcoming socket uses 0.0.0.0 because it listens on all available local IPv4 network interfaces. The connection socket shows 127.0.0.1 because the client connects through localhost

