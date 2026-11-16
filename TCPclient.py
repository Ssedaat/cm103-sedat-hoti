from socket import *

serverName = 'localhost'      # the server runs on this same computer
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print('Client socket:', clientSocket.getsockname(), 'peer', clientSocket.getpeername())# three-way handshake

sentence = input('Input lowercase sentence: ')
clientSocket.send(sentence.encode())             # no address needed

modifiedSentence = clientSocket.recv(1024)
print('From Server:', modifiedSentence.decode())
clientSocket.close()