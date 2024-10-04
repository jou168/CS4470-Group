import sys
from socket import *
import argparse  # User terminal input
import threading  # multisocketing, will solve server issue not allowing terminal usage
import time

clients = {}  # dictionary, key-value pairs, to hold ip/port info
serverSocket = socket(AF_INET, SOCK_STREAM)  # Initialized outside of server() for port number fetching
"""
is_running: Global variable to ensure server is running and when exit() is called this will ensure the 
server shuts down gracefully and is not trying to accept new connections
"""
is_running = True


def server(serverPort):
    serverSocket.bind(("", serverPort))
    serverSocket.listen(1)
    print("The server is ready to receive")
    while is_running:
        try:
            connectionSocket, addr = serverSocket.accept()
            print("A User has connected from,", addr[0])
            clients[addr[0]] = (connectionSocket, addr)
            #sentence = connectionSocket.recv(1024).decode('utf-8')
            #captializedSentence = sentence.upper()
            #connectionSocket.send(captializedSentence.encode('utf-8'))
            connectionSocket.close()
        except OSError:
            break


def client():
    time.sleep(1)  # Gives time for threads,so client() and server() commands don't overlap weirdly i.e. print statements
    print("For command information type: help")
    #sentence = input("Input lowercase sentence:")
    #clientSocket.send(sentence.encode('utf-8'))
    #modifiedSentence = clientSocket.recv(1024).decode('utf-8')
    #print('From Server:', modifiedSentence)
    while is_running:
        # serverIP = ""
        # serverPort = 0
        userInput = input("Enter a command: ")
        if userInput.lower() == 'help':
            help()
        elif userInput.lower() == "myip":
            print(f"My IP: {myip()}")
        elif userInput.lower() == "myport":
            myport()
        elif userInput.lower().startswith("connect"):
            connect(userInput)
        elif userInput.lower() == "list":
            list()
        elif userInput.lower().startswith("terminate"):
            terminate(userInput)
        # elif userInput.lower().startswith("send"):
        #     send(userInput)
        elif userInput.lower() == "exit":
            exit()


def help():
    print("""
    myip: Displays ipv4 address of the process
    myport: Displays the port that the server socket is listening on
    connect (ip, port #): Given two inputs, will attempt to that given computer and socket. Failure/Success will give corresponding message to client and server peer
    list: Displays connection_id, IP, and port # of all connections to and from other peers
    terminate (connection_id): Terminates connection between peers. errors for no valid connections should be displayed, and disconnections initiated by other peers should also
    send (connection_id): Sends message based on list of connections, sender should get info of message, reciever should get sender info and message
    exit: Close all connections made on this process.
    """)


def myip():
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # Connect to Google DNS
        ip_address = s.getsockname()[0]  # Get IP
    except Exception:
        ip_address = "Unable to fetch IP"  # Exception catch/error message
    finally:
        s.close()
    return ip_address


def myport():
    portNum = serverSocket.getsockname()[1]  #Index 1 gives port #, Index 0 gives IP default "0.0.0.0"
    print(f"Your server is running on port: {portNum}")


def connect(input):
    connectInput = input.split()
    if len(connectInput) == 3:
        command, serverIP, portString = connectInput  # the split will be divided up between these three variables
        serverPort = int(portString)
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverIP, serverPort))
        clients[serverIP] = (clientSocket, (serverIP, serverPort))
        print("You have connected to", serverIP, "on socket", serverPort)


def list():
    print("id: IP Addresses     Port No.")
    id = 1
    for ip, (socket, addr) in clients.items():
        print(f"{id}, {id}, {addr[1]}")
        id += 1


def terminate(input):
    command, id = input.split()
    id = int(id) - 1  # accounts for indexing
    for client in clients:
        if id == client:
            for ip, port in client:
                socket = ip, port
                socket.close()
                del clients[ip]


# def sendmessage(connection_id, message):
#     if 0 < connection_id < len(clients):
#         ip = list(clients.keys())[connection_id - 1]
#         client_socket, addr = clients[ip]
#         try:
#             client_socket.send(message.encode())
#             print(f"Message sent to: {addr[0]}:{addr[1]}")
#         except Exception as e:
#             print(f"Error sending message to: {addr[0]}:{addr[1]} - {e}")
#     else:
#         print("Invalid ID")
#
#
# def send(input):
#     parts = input.split(maxsplit=2)
#     if len(parts) < 3:
#         print("Usage: send <connection_id> <ip> <message>")
#         return
#     connection_id = int(parts[0])
#     message = parts[2]
#     sendmessage(connection_id, message)


def exit():
    global is_running
    is_running = False
    print("Terminating all connections and exiting...")
    for ip, (socket, addr) in clients.items():
        print(f"Closing connection to {ip}:{addr[1]}")

    clients.clear()
    serverSocket.close()
    sys.exit(0)


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
