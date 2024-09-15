from socket import *
import argparse #User terminal input
import threading #multisocketing, will solve server issue not allowing terminal usage
import time


clients= [] #2d array that will hold all connection information between peers
serverSocket = socket(AF_INET, SOCK_STREAM) #Initialized outside of server() for port number fetching


def server(serverPort):
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
   time.sleep(1) #Gives time for threads,so client() and server() commands don't overlap weirdly i.e. print statements
   print("For command information type: help")
   #sentence = input("Input lowercase sentence:")
   #clientSocket.send(sentence.encode('utf-8'))
   #modifiedSentence = clientSocket.recv(1024).decode('utf-8')
   #print('From Server:', modifiedSentence)
   while 1:
       serverIP = ""
       serverPort = 0
       userInput = input("Enter a command: ")
       if userInput.lower() == 'help':
           help()
       #elif userInput.lower() == "myip":
       elif userInput.lower() == "myport":
           myport()
       elif userInput.lower() == ('connect'+ serverIP + str(serverPort)):
           clientSocket = socket(AF_INET, SOCK_STREAM)
           clientSocket.connect((serverIP, serverPort))
           clients.append([serverIP, serverPort])
           print("You have connected to", serverIP, "on socket", serverPort)
       elif userInput.lower() == "list":
           list()
       #elif userInput.lower() == "terminate":
       #elif userInput.lower() == "send":
       #elif userInput.lower() == "exit":


def help():
   print("myip: Displays ipv4 address of the process")
   print("myport: Displays the port that the server socket is listening on")
   print("connect (ip, port #): Given two inputs, will attempt to that given computer and socket. Failure/Success will give corresponding message to client and server peer")
   print("list: Displays connection_id, IP, and port # of all connections to and from other peers")
   print("terminate (connection_id): Terminates connection between peers. errors for no valid connections should be displayed, and disconnections initiated by other peers should also")
   print("send (connection_id): Sends message based on list of connections, sender should get info of message, reciever should get sender info and message")
   print("exit: Close all connections made on this process.")


#def myip():
def myport():
   portNum = serverSocket.getsockname()[1] #Index 1 gives port #, Index 0 gives IP default "0.0.0.0"
   print("Your server is running on port", portNum)
#def connect()
def list():
   print("id: IP Addresses     Port No.")
   id = 1
   for client in clients:
       for index in client:
           print(id, " ", index, end=" ")
       id += 1
   print()
#def terminate()
#def send()
#def exit()




if __name__ == '__main__':
   terminalInput = argparse.ArgumentParser(description="TCP server/client Initialization")
   terminalInput.add_argument('port', type=int, help='Listening Port')
   #terminalInput.add_argument('--ip', type=str, default="localhost", help="computer ip address to connect to")
   # -- for ip adds optionality, so not mandatory input, but terminal requires --ip when inputting address
   args = terminalInput.parse_args()
   serverThread = threading.Thread(target=server, args=(args.port,))
   clientThread = threading.Thread(target=client, args=())


   serverThread.start()
   clientThread.start()


   serverThread.join()
   clientThread.join()
   #if args.ip == "localhost":
       #server(args.port)
   #elif args.ip != "localhost":
      # client(args.ip, args.port)

