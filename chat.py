from socket import *
import argparse  # User terminal input
import threading  # multisocketing, will solve server issue not allowing terminal usage

clients = []  # 2d array that will hold all connection information between peers
serverSocket = socket(AF_INET, SOCK_STREAM)  # Initialized outside of server() for port number fetching
server_running = True


def server(serverPort):
    serverSocket.bind(("", serverPort))
    serverSocket.listen(5)
    print("The server is ready to receive")
    while server_running:
        try:
            conn, addr = serverSocket.accept()
            clients.append((conn, addr))
            threading.Thread(target=handle_client, args=(conn, addr)).start()
        except OSError:
            break


def handle_client(conn, addr):
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            if message:
                print(f"Message From: {addr[0]}: {message}")
            else:
                break
        except OSError:
            break


def connect(server_ip, server_port):
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((server_ip, server_port))
        clients.append((clientSocket, (server_ip, server_port)))
        print("The client is connected to {server_ip}:{server_port}")
    except Exception as e:
        print(f"Failed to connect: {e}")


def send_message(connection_id, message):
    if 0 < connection_id <= len(clients):
        conn, addr = clients[connection_id - 1]
        try:
            conn.send(message.encode())
            print(f"Message sent to {addr}")
        except Exception as e:
            print("Invalid connection ID.")


def remove_client(addr):
    global clients
    clients = [client for client in clients if client[1] != addr]


def client():
    while True:
        userInput = input("Enter a command: ").split()

        if userInput[0] == "connect" and len(userInput) == 3:
            try:
                server_ip = userInput[1]
                server_port = int(userInput[2])
                connect(server_ip, server_port)
            except ValueError:
                print("Error: port must be a number.")
        elif userInput[0].lower() == "send" and len(userInput) >= 3:
            try:
                connection_id = int(userInput[1])
                message = ' '.join(userInput[2:])
                send_message(connection_id, message)
            except ValueError:
                print("Error: Connection ID must be a number.")
        elif userInput[0].lower() == "help":
            help()
        elif userInput[0].lower() == "myport":
            myport()
        elif userInput[0].lower() == "myip":
            print(f"My IP: {get_ip_address()}")
        else:
            print("Invalid command.")


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


def get_ip_address():
    s = socket(AF_INET, SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # Connect to Google's DNS (no data sent)
        ip_address = s.getsockname()[0]  # Get the IP used for this connection
    except Exception:
        ip_address = "Unable to fetch IP"  # If something goes wrong, return an error message
    finally:
        s.close()
    return ip_address


def myport():
    portNum = serverSocket.getsockname()[1]  # Index 1 gives port #, Index 0 gives IP default "0.0.0.0"
    print("Your server is running on port", portNum)


def list():
    print("id: IP Addresses     Port No.")
    id = 1
    for client in clients:
        for index in client:
            print(id, " ", index, end=" ")
        id += 1
    print()


#def terminate()

#def exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TCP server/client Initialization")
    parser.add_argument('port', type=int, help='The port that the server socket is listening on.')
    args = parser.parse_args()

    serverThread = threading.Thread(target=server, args=(args.port,))
    clientThread = threading.Thread(target=client, args=())

    serverThread.start()
    clientThread.start()

    serverThread.join()
    clientThread.join()
