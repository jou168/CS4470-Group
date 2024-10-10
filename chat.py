import sys
from socket import *
import argparse  # User terminal input
import threading  # multisocketing, will solve server issue not allowing terminal usage
import time

clients = []
# id 0
# ip 1
# port 2
# socket 3
ipv4 = ""
serverSocket = socket(AF_INET, SOCK_STREAM)  # Initialized outside of server() for port number fetching
"""
is_running: Global variable to ensure server is running and when exit() is called this will ensure the
server shuts down gracefully and is not trying to accept new connections
"""
is_running = True


def server(serverPort):
    serverSocket.bind(("", serverPort))
    serverSocket.listen(1)
    print("The server is ready to recieve")
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
                messageParts = message.split()
                counter = 0
                for client in clients:
                    if messageParts[0] == client[1]:
                        print(f"{message}")
                        del clients[counter]
                    elif counter+1 == len(clients):
                        print(f"\nMessage received From: {addr[0]} \nSender's Port: {addr[1]} \n{message}")
                    counter += 1
            else:
                break
        except OSError:
            break


def handle_server(clientSocket, addr):
    while True:
        try:
            message = clientSocket.recv(1024).decode('utf-8')
            if message:
                messageParts = message.split()
                counter = 0
                for client in clients:
                    if messageParts[0] == client[1]:
                        print(f"{message}")
                        del clients[counter]
                    elif counter+1 == len(clients):
                        print(f"\nMessage received From: {addr[0]} \nSender's Port: {addr[1]} \n{message}")
                    counter += 1
            else:
                break
        except OSError:
            break


def client():
    time.sleep(
        1)  # Gives time for threads,so client() and server() commands don't overlap weirdly i.e. print statements
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

        try:  # Validates IP
            inet_aton(serverIP)
        except error:
            print(f"Invalid IP address: {serverIP}")
            return  # early function end

        # self-connection prevention
        if serverIP == ipv4 and serverPort == serverSocket.getsockname()[1]:
            print("Cannot connect to self.")
            return

        # Duplicate Connections
        if any(serverIP == client[1] and serverPort == client[2] for client in clients):
            print("Already connected to this client")
            return

        try:
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverIP, serverPort))
            clients.append([len(clients) + 1, serverIP, serverPort, clientSocket])
            print("You have connected to", serverIP, "on socket", serverPort)
            threading.Thread(target=handle_server, args=(clientSocket, serverIP)).start()
        except Exception:
            print(f"Failed to connect to {serverIP} on port {serverPort}. Error: {Exception}")


def list():
    print("id: IP Addresses     Port No.")
    for client in clients:
        print(f"{client[0]}: {client[1]} {client[2]:>10}")


def terminate(input):
    command, id = input.split()
    id = int(id)
    for client in clients:
        if id == client[0]:
            index = id - 1
            messageSocket = client[3]
            message = f"{ipv4} has terminated the connection"
            messageSocket.send(message.encode('utf-8'))
            messageSocket.close()
            print(f"Closing connection on id: {client[0]}")
            del clients[index]


def send(input):
    input = input.replace("send", "")
    index = int(input[1])
    message = input[3:]

    for client in clients:
        if index == client[0]:
            sendSocket = client[3]
            sendSocket.send(message.encode('utf-8'))
            print("Message sent to:", index)


def exit():
    global is_running
    is_running = False
    print("Terminating all connections and exiting...")
    for client in clients:
        sendSocket = client[3]
        message = f"{ipv4} has terminated the connection"
        sendSocket.send(message.encode('utf-8'))
        sendSocket.close()
        print(f"Closing connection to {client[0]}:{client[1]}")

    clients.clear()
    serverSocket.close()
    sys.exit(0)


if __name__ == '__main__':
    terminalInput = argparse.ArgumentParser(description="TCP server/client Initialization")
    terminalInput.add_argument('port', type=int, help='Listening Port')

    # myip function but called in main to globally store ipv4
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # Connect to Google DNS
        ipv4 = s.getsockname()[0]
    except Exception:
        print("Unable to fetch IP")  # Exception catch/error message
    finally:
        s.close()

    args = terminalInput.parse_args()
    serverThread = threading.Thread(target=server, args=(args.port,))
    clientThread = threading.Thread(target=client, args=())

    serverThread.start()
    clientThread.start()

    serverThread.join()
    clientThread.join()
