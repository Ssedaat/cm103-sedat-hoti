from socket import *
import sys 

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('127.0.0.1', 6789))
serverSocket.listen(1)

while True:
    print('Ready to serve...')

    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024).decode()

        filename = message.split()[1]
        f = open(filename[1:])

        outputdata = f.readlines()
        f.close()

        connectionSocket.sendall(
            "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n".encode()
        )

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())

        connectionSocket.close()

    except IOError:
        
        connectionSocket.sendall(
            "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n".encode()
        )
        connectionSocket.sendall(
            "<html><body><h1>404 Not Found</h1></body></html>".encode()
        )
        
        connectionSocket.close()
        

serverSocket.close()
sys.exit()
