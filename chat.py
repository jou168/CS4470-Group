import argparse  # User terminal input
import sys
import threading  # multisocketing, will solve server issue not allowing terminal usage
import time
from socket import *

clients = []
# id 0
# ip 1
# port 2
# socket 3
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
            if not any(addr[0] == client[1] and addr[1] == client[2] for client in clients):
                clients.append([len(clients) + 1, addr[0], addr[1], connectionSocket])
                print("\nA user has connected from,", addr[0])
            threading.Thread(target=handle_client, args=(connectionSocket, addr)).start()
        except OSError:
            break


def handle_client(conn, addr):
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            if message:
                print(f"\nMessage received From: {addr[0]} \nSender's Port: {addr[1]} \n{message}")
            else:
                break
        except OSError:
            break


def handle_server(clientSocket, addr):
    while True:
        try:
            message = clientSocket.recv(1024).decode('utf-8')
            if message:
                print(f"\nMessage received From: {addr[0]}:\nSender's Port: {addr[1]} \n{message}")
            else:
                break
        except OSError:
            break


def client():
    time.sleep(1)  # Gives time for threads,so client() and server() commands don't overlap weirdly i.e. print statements
    print("For command information type: help")
    while True:
        time.sleep(1)  # Helps with communication between clients to not overlap terminal output
        userInput = input("Enter a command: ")
        if userInput.lower() == 'help':
            help()
        elif userInput.lower() == "myip":
            myip()
        elif userInput.lower() == "myport":
            myport()
        elif userInput.lower().startswith("connect"):
            connect(userInput)
        elif userInput.lower() == "list":
            list()
        elif userInput.lower().startswith("terminate"):
            terminate(userInput)
        elif userInput.lower().startswith("send"):
            send(userInput)
        elif userInput.lower() == "exit":
            exit()


def help():
    print("myip: Displays ipv4 address of the process")
    print("myport: Displays the port that the server socket is listening on")
    print(
        "connect (ip, port #): Given two inputs, will attempt to that given computer and socket. Failure/Success will give corresponding message to client and server peer")
    print("list: Displays connection_id, IP, and port # of all connections to and from other peers")
    print(
        "terminate (connection_id): Terminates connection between peers. errors for no valid connections should be displayed, and disconnections initiated by other peers should also")
    print(
        "send (connection_id): Sends message based on list of connections, sender should get info of message, reciever should get sender info and message")
    print("exit: Close all connections made on this process.")


def myip():
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # Connect to Google DNS
        print(s.getsockname()[0])  # Get IP
    except Exception:
        print("Unable to fetch IP")  # Exception catch/error message
    finally:
        s.close()


def myport():
    portNum = serverSocket.getsockname()[1]  # Index 1 gives port #, Index 0 gives IP default "0.0.0.0"
    print(f"Your server is running on port", portNum)


def connect(input):
    connectInput = input.split()
    if len(connectInput) == 3:
        command, serverIP, portString = connectInput  # the split will be divided up between these three variables
        serverPort = int(portString)
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverIP, serverPort))
        clients.append([len(clients) + 1, serverIP, serverPort, clientSocket])
        print("You have connected to", serverIP, "on socket", serverPort)
        threading.Thread(target=handle_server, args=(clientSocket, serverIP)).start()


def list():
    print("id: IP Addresses   Port No.")
    for client in clients:
        print(client[0], client[1], client[2])


def terminate(input):
    command, id = input.split()
    id = int(id)
    for client in clients:
        if id == client[0]:
            index = id - 1
            socket = clients[index][3]
            socket.close()
            del clients[index]


def send(input):
    input = input.replace("send", "").strip()

    if not clients:
        print("No clients connected")

    if len(input) < 2 or input[0] != ' ':
        print("Usage: send <connection_id> <message>")
        return

    try:
        index = int(input[1])
        message = input[3:]
        for client in clients:
            if index == client[0]:
                socket = client[3]
                # socket.connect((client[1], client[2]))
                socket.send(message.encode('utf-8'))
                print("Message sent to:", index)
                return
        print(f"No client found with connection ID {index}. Use 'list' to list all connections")

    except ValueError:
        print("Invalid connection ID")


def exit():
    global is_running
    is_running = False
    print("Terminating all connections and exiting...")
    for client in clients:
        print(f"Closing connection to {client[0]}:{client[1]}")
    clients.clear()
    serverSocket.close()
    sys.exit(0)


if __name__ == '__main__':
    terminalInput = argparse.ArgumentParser(description="TCP server/client Initialization")
    terminalInput.add_argument('port', type=int, help='Listening Port')

    args = terminalInput.parse_args()
    serverThread = threading.Thread(target=server, args=(args.port,))
    clientThread = threading.Thread(target=client, args=())

    serverThread.start()
    clientThread.start()

    serverThread.join()
    clientThread.join()
