import argparse  # User terminal input
import sys
import threading  # multisocketing, will solve server issue not allowing terminal usage
import keyboard
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
prompt_displayed = False


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
                print("Enter a command: ", end ='', flush=True)
            threading.Thread(target=handle_client, args=(connectionSocket, addr)).start()
        except OSError:
            break


def handle_client(conn, addr):
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            if message:
                print(f"\nMessage from: {addr[0]} | {addr[1]}: {message}")
                # print_cmd_prompt()
            else:
                break
        except OSError:
            break


def handle_server(clientSocket, addr):
    while True:
        try:
            message = clientSocket.recv(1024).decode('utf-8')
            if message:
                print(f"\nMessage from: {addr[0]} | {addr[1]}: {message}")
                # print_cmd_prompt()
            else:
                break
        except OSError:
            break


# def prompt_on_keypress():
#     global prompt_displayed
#     while is_running:
#         keyboard.read_key()
#         if not prompt_displayed:
#             print("\nEnter a command: ", end ='', flush=True)
#             prompt_displayed = True
#         time.sleep(0.2)
#
#
# def print_cmd_prompt():
#     global prompt_displayed
#     if not prompt_displayed:
#         print("\nEnter a command: ", end ='', flush=True)
#         prompt_displayed = True


def client():
    global prompt_displayed
    time.sleep(1)  # Gives time for threads,so client() and server() commands don't overlap weirdly i.e. print statements
    print("For command information type: help")

    # threading.Thread(target=prompt_on_keypress, daemon=True).start()

    while True:
        # if not prompt_displayed:  # Check if prompt has already been displayed
        #     print("\nEnter a command: ", end='', flush=True)
        #     prompt_displayed = True
        userInput = input("Enter a command: ")
        # prompt_displayed = False

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
        else:
            print("Invalid command. Type 'help' for a list of commands")


def help():
    print("""
    myip: Displays ipv4 address of the process
    myport: Displays the port that the server socket is listening on
    connect (ip, port #): Given two inputs, will attempt to that given computer and socket. Failure/Success will give corresponding message to client and server peer
    list: Displays connection_id, IP, and port # of all connections to and from other peers")
    terminate (connection_id): Terminates connection between peers. errors for no valid connections should be displayed, and disconnections initiated by other peers should also
    send (connection_id): Sends message based on list of connections, sender should get info of message, receiver should get sender info and message
    exit: Close all connections made on this process.
    """)


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
    input = input.replace("terminate", "").strip()

    if not clients:
        print("No clients connected")

    if not input.isdigit():
        print("Usage: terminate <connection_id>")
        return

    id = int(input)

    index = id - 1

    if 0 <= index < len(clients) and clients[index][0] == id:
        socket = clients[index][3]
        try:
            socket.close()
            print(f"Client {id} disconnected")
        except OSError as e:
            print(f"Error disconnecting client ID {id}: {e}")
        clients.pop(index)
    else:
        print(f"No client found with connection ID {id}. Use 'list' to list all connections")


def send(input):
    input = input.replace("send", "").strip()

    if not clients:
        print("No clients connected")

    parts = input.split(maxsplit=1)
    if len(input) < 2 or not parts[0].isdigit():
        print("Usage: send <connection_id> <message>")
        return

    index = int(parts[0])
    message = parts[1]

    for client in clients:
        if index == client[0]:
            socket = client[3]
            try:
                socket.send(message.encode('utf-8'))
                print(f"Message sent to client:", {index})
            except OSError as e:
                print(f"Error sending message to connection ID {index}: {e}")
            return
        print(f"No client found with connection ID {index}. Use 'list' to list all connections")


def exit():
    global is_running
    is_running = False
    print("Terminating all connections and exiting...")

    for client in clients:
        print(f"Closing connection to client ID {client[0]} at {client[1]}:{client[2]}")
        client[3].close()
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
