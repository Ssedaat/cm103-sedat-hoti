from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)   # IPv4, TCP
serverSocket.bind(('', serverPort))
serverSocket.listen(1)                        # welcoming socket waits for clients
print('The server is ready to receive')
print('Welcoming socket:', serverSocket.getsockname())

while True:
    connectionSocket, addr = serverSocket.accept() 
    print('Connection socket:', connectionSocket.getsockname(),
      'peer', connectionSocket.getpeername())# new socket for this client
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close() 