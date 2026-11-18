# Lab: Socket Programming with Python (UDP and TCP)

CM-103 Network and Internet Technologies · Nov 12, 2026 · @Mahi

## Overview

In this lab you build a simple client-server application twice: first over UDP, then over TCP. The client sends a sentence in lowercase, and the server sends it back in uppercase. Both programs run on your own computer and talk through the loopback address `localhost` (127.0.0.1). The code follows Kurose & Ross, *Computer Networking: A Top-Down Approach*, Section 2.7.

**After this lab you can:**

- create UDP and TCP sockets in Python and explain each socket call
- explain why UDP needs no connection and TCP does
- tell the difference between the TCP welcoming socket and the connection socket
- run a server and a client in two terminals on one machine

**Note on running the client and server processes on the same machine**

In real networks, the client process and the server process usually run on separate machines, for example your browser on your laptop and a web server in a daugh Wi-Fi or Ethernet. The operating system loops it straight back to a process on the same computer. The data still passes through the full network stack (sockets, UDP or TCP, IP), so the programs behave exactly as they would between two machines. The operating system uses the assigned **port number** to deliver each message to the right process.

Because the server and the client are two separate processes that must run at the same time, you open two terminals: **Terminal 1** runs the server, and **Terminal 2** runs the client. To run them on two different computers later, you only change `serverName` in the client from `'localhost'` to the server's IP address.

## Part 1: UDP

UDP sends independent datagrams. There is no connection setup, so every message must carry the destination address.

### Step 1: Write the client

Save this as `UDPClient.py`:

```python
from socket import *

serverName = 'localhost'      # the server runs on this same computer
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input('Input lowercase sentence: ')
clientSocket.sendto(message.encode(), (serverName, serverPort))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
```

### Step 2: Write the server

Save this as `UDPServer.py`:

```python
from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)    # IPv4, UDP
serverSocket.bind(('', serverPort))           # all local interfaces, port 12000
print('The server is ready to receive')

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
```

### What the code does

| Line | Meaning |
| --- | --- |
| `socket(AF_INET, SOCK_DGRAM)` | Create an IPv4 socket that uses UDP |
| `bind(('', serverPort))` | Server only: attach the socket to port 12000 so clients can find it |
| `sendto(data, (host, port))` | Send one datagram to the given address |
| `recvfrom(2048)` | Wait for one datagram (up to 2048 bytes); also returns the sender's address |
| `.encode()` / `.decode()` | Convert between a string and bytes; sockets only send bytes |

### Step 3: Run it in two terminals

1. Open **Terminal 1**. Go to your lab folder with `cd socket-lab`. Check the files are there with `dir *.py` (Windows) or `ls *.py` (macOS/Linux).
2. Start the server: `python UDPServer.py` (macOS/Linux: `python3 UDPServer.py`). You should see `The server is ready to receive`. Leave this terminal open.
3. Open **Terminal 2** and go to the same folder.
4. Start the client: `python UDPClient.py`.
5. Type a sentence in lowercase, for example `hello networks`, and press Enter. The client prints `HELLO NETWORKS` and ends.
6. Run the client again a few times. The server keeps running and answers each time.
7. Stop the server in Terminal 1 (see Troubleshooting for Windows).

In VS Code, you can use **Terminal → Split Terminal** to see both terminals side by side.

### Questions

1. Start the client **without** the server running and send a sentence. What happens?&#32;
2. Why does the server call `bind()` but the client does not?
3. How does the server know where to send its reply?

## Part 2: TCP

TCP is connection-oriented. The client and server first set up a connection (the three-way handshake), and only then exchange data. The server uses two kinds of socket: a **welcoming socket** that waits for new clients, and a new **connection socket** for each client.

### Step 1: Write the client

Save this as `TCPClient.py`:

```python
from socket import *

serverName = 'localhost'      # the server runs on this same computer
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))   # three-way handshake

sentence = input('Input lowercase sentence: ')
clientSocket.send(sentence.encode())             # no address needed

modifiedSentence = clientSocket.recv(1024)
print('From Server:', modifiedSentence.decode())
clientSocket.close()
```

### Step 2: Write the server

Save this as `TCPServer.py`:

```python
from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)   # IPv4, TCP
serverSocket.bind(('', serverPort))
serverSocket.listen(1)                        # welcoming socket waits for clients
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()   # new socket for this client
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()                         # welcoming socket stays open
```

### What is new compared with UDP

| Line | Meaning |
| --- | --- |
| `socket(AF_INET, SOCK_STREAM)` | Create an IPv4 socket that uses TCP |
| `listen(1)` | Server: turn `serverSocket` into a welcoming socket that waits for connection requests |
| `accept()` | Server: wait for a client, complete the handshake and return a **new** `connectionSocket` plus the client's address |
| `connect((host, port))` | Client: set up the TCP connection before sending anything |
| `send()` / `recv()` | Send and receive over the connection; no address is needed because the connection already knows it |
| `connectionSocket.close()` | Close only this client's connection; `serverSocket` keeps waiting for the next client |

### Step 3: Run it in two terminals

1. Make sure the UDP server from Part 1 is stopped (it can run at the same time, but it keeps things simpler).
2. In **Terminal 1**, start the server: `python TCPServer.py`. Leave it running.
3. In **Terminal 2**, start the client: `python TCPClient.py`.
4. Type a sentence in lowercase and press Enter. The client prints the uppercase version and ends.
5. Run the client several more times. Each run is a new TCP connection.
6. Stop the server in Terminal 1.

### Questions

1. Start the TCP client without the server. What error do you get, and why is this different from UDP?
2. Why does the server create a new socket in `accept()` instead of using `serverSocket` to talk to the client?
3. Why does the TCP client use `send()` while the UDP client uses `sendto()`?

## Part 3: Looking inside the sockets

In this part you add `print()` lines to see which IP address and port number each socket uses. This shows how the operating system tells sockets apart.

Two socket methods help:

| Method | Returns |
| --- | --- |
| `getsockname()` | This socket's own address: `(IP, port)` |
| `getpeername()` | The address of the other end (TCP only, after connecting) |

### Step 1: The client's port number

In `UDPClient.py`, add this line right after `sendto(...)`:

```python
print('Client socket address:', clientSocket.getsockname())
```

In `UDPServer.py`, add this line right after `recvfrom(...)`:

```python
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print('Message from:', clientAddress)        # new line: indented inside the loop
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
```

The new line must be indented by 4 spaces, like the other lines in the loop. If it is not indented, or is added at the end of the file, it is outside the `while True:` loop and never runs. After saving the change, stop the server and start it again: a server that is already running still uses the old code.

Run the client three times. Write down the port numbers.

- Is the client's port the same every time? Who chose it?
- Does the port the server prints match the port the client prints?

### Step 2: Welcoming socket vs. connection socket (TCP)

In `TCPServer.py`, add one line before the `while` loop and one line right after `accept()`:

```python
print('Welcoming socket:', serverSocket.getsockname())
```

```python
print('Connection socket:', connectionSocket.getsockname(),
      'peer', connectionSocket.getpeername())
```

In `TCPClient.py`, add this line right after `connect(...)`:

```python
print('Client socket:', clientSocket.getsockname(), 'peer', clientSocket.getpeername())
```

Run the client twice and fill in the table:

| Run | Client socket (IP, port) | Connection socket (IP, port) | Connection socket peer |
| --- | --- | --- | --- |
| 1 |  |  |  |
| 2 |  |  |  |

### Questions

1. The welcoming socket and every connection socket use port 12000. How can the server have several sockets on the same port? What extra information tells them apart?
2. Compare the client's port with the connection socket's peer port. What do you notice?
3. Why is the welcoming socket's IP shown as `0.0.0.0`, while the connection socket shows `127.0.0.1`?

## What to submit

Upload one PDF and your code to the course submission repository:

- [ ] Your four python files: `UDPServer.py`, `UDPClient.py`, `TCPServer.py`, `TCPClient.py`, including the `print()` lines from Part 3
- [ ] One file with short answers to the questions in Parts 1, 2 and 3 and your filled-in table from Part 3, Step 2

Source: J. F. Kurose and K. W. Ross, *Computer Networking: A Top-Down Approach*, Section 2.7, Socket Programming: Creating Network Applications.
