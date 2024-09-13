from socket import *
def server():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("", serverPort))
    serverSocket.listen(1)
    print("The server is ready to recieve")
    while 1:
        connectionSocket, addr = serverSocket.accept()
        sentence = connectionSocket.recv(1024).decode('utf-8')
        captializedSentence = sentence.upper()
        connectionSocket.send(captializedSentence.encode('utf-8'))
        connectionSocket.close()
def client():
    serverName = 'localhost'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    sentence = input("Input lowercase sentence:")
    clientSocket.send(sentence.encode('utf-8'))
    modifiedSentence = clientSocket.recv(1024)
    print('From Server:', modifiedSentence)
    clientSocket.close()
if __name__ == '__main__':
    server()