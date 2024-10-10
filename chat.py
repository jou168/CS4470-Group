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


def server(server_port):
    serverSocket.bind(("", server_port))
    serverSocket.listen(1)
    print("The server is ready to receive")
    while is_running:
        try:
            connection_socket, addr = serverSocket.accept()
            if not any(addr[0] == current_client[1] and addr[1] == current_client[2] for current_client in clients):
                clients.append([len(clients) + 1, addr[0], addr[1], connection_socket])
                print("\nA user has connected from:", addr[0])
            threading.Thread(target=handle_client, args=(connection_socket, addr)).start()
        except OSError:
            break


def handle_client(conn, addr):
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            if message:
                message_parts = message.split()
                counter = 0
                for current_client in clients:
                    if message_parts[0] == current_client[1]:
                        print(f"{message}")
                        del clients[counter]
                    elif counter+1 == len(clients):
                        print(f"\nMessage From: {addr[0]} | Port: {addr[1]} : {message}")
                    counter += 1
            else:
                break
        except OSError:
            break


def handle_server(client_socket, addr):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                message_parts = message.split()
                counter = 0
                for current_client in clients:
                    if message_parts[0] == current_client[1]:
                        print(f"{message}")
                        del clients[counter]
                    elif counter+1 == len(clients):
                        print(f"\nMessage From: {addr[0]} | Port: {addr[1]} : {message}")
                    counter += 1
            else:
                break
        except OSError:
            break


def client():
    time.sleep(1)  # Gives time for threads,so client() and server() commands don't overlap weirdly i.e. print statements
    print("For command information type: help")
    while True:
        time.sleep(1)  # Helps with communication between clients to not overlap terminal output
        user_input = input("Enter a command: ")
        if user_input.lower() == 'help':
            help_menu()
        elif user_input.lower() == "myip":
            my_ip()
        elif user_input.lower() == "myport":
            my_port()
        elif user_input.lower().startswith("connect"):
            connect(user_input)
        elif user_input.lower() == "list":
            connection_list()
        elif user_input.lower().startswith("terminate"):
            terminate(user_input)
        elif user_input.lower().startswith("send"):
            send(user_input)
        elif user_input.lower() == "exit":
            exit_app()
        else:
            print("Invalid command. Type 'help' to see list of available commands")


def help_menu():
    print("""
    myip: Displays ipv4 address of the process
    myport: Displays the port that the server socket is listening on
    connect (ip, port #): Given two inputs, will attempt to that given computer and socket. Failure/Success will give corresponding message to client and server peer
    list: Displays connection_id, IP, and port # of all connections to and from other peers")
    terminate (connection_id): Terminates connection between peers. errors for no valid connections should be displayed, and disconnections initiated by other peers should also
    send (connection_id): Sends message based on list of connections, sender should get info of message, receiver should get sender info and message
    exit: Close all connections made on this process.
    """)


def my_ip():
    sock = socket(AF_INET, SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))  # Connect to Google DNS
        print(sock.getsockname()[0])  # Get IP
    except OSError  as e:
        print(f"Unable to fetch IP address: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")  # Exception catch/error message
    finally:
        sock.close()


def my_port():
    port_num = serverSocket.getsockname()[1]  # Index 1 gives port #, Index 0 gives IP default "0.0.0.0"
    print(f"Your server is running on port:", port_num)


def connect(user_input):
    connect_input = user_input.split()
    if len(connect_input) == 3:
        command, server_ip, port_string = connect_input  # the split will be divided up between these three variables
        server_port = int(port_string)

        try:  # Validates IP
            inet_aton(server_ip)
        except error:
            print(f"Invalid IP address: {server_ip}")
            return  # early function end

        # self-connection prevention
        if server_ip == ipv4 and server_port == serverSocket.getsockname()[1]:
            print("Cannot connect to self.")
            return

        # Duplicate Connections
        if any(server_ip == current_client[1] and server_port == current_client[2] for current_client in clients):
            print("Already connected to this client")
            return

        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect((server_ip, server_port))
            clients.append([len(clients) + 1, server_ip, server_port, client_socket])
            print("You have connected to", server_ip, "on socket", server_port)
            threading.Thread(target=handle_server, args=(client_socket, server_ip)).start()
        except OSError as e:
            print(f"Failed to connect to {server_ip} on port {server_port}. Socket Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")


def connection_list():
    print("id: IP Addresses     Port No.")
    for current_client in clients:
        print(f"{current_client[0]}: {current_client[1]} {current_client[2]:>10}")


def terminate(user_input):
    try:
        command, client_id = user_input.split()
        client_id = int(client_id)

        for current_client in clients:
            if client_id == current_client[0]:
                index = client_id - 1
                message_socket = current_client[3]
                message = f"{ipv4} has terminated the connection"
                message_socket.send(message.encode('utf-8'))
                message_socket.close()
                print(f"Closing connection on id: {current_client[0]}")
                del clients[index]
                return
    except ValueError:
        print("Usage: terminate <connection_id>")
    except IndexError:
        print("Invalid connection ID")
    except Exception as e:
        print(f"Error Occurred: {e}")


def send(user_input):
    try:
        if not clients:
            print("No active connections to send a message.")
            return

        user_input = user_input.replace("send", "", 1).strip()
        parts = user_input.split(" ", 1)  # Split once at the first space

        if len(parts) < 2:
            raise ValueError("Incomplete send command.")

        index = int(parts[0].strip())  # The connection ID
        message = parts[1].strip()  # The message to send

        if not message:
            raise ValueError("No message provided.")

        for current_client in clients:
            if index == current_client[0]:
                send_socket = current_client[3]
                send_socket.send(message.encode('utf-8'))
                print("Message sent to:", index)
                return

        print(f"No connection found with ID: {index}")

    except ValueError as ve:
        print("Usage: send <connection_id> <message>")
        print(f"Error: {ve}")
    except IndexError:
        print("Invalid connection ID.")
    except Exception as e:
        print(f"An error occurred: {e}")


def exit_app():
    global is_running
    is_running = False
    print("Terminating all connections and exiting...")
    for current_client in clients:
        send_socket = current_client[3]
        message = f"\nUser from {ipv4} has terminated the connection"
        send_socket.send(message.encode('utf-8'))
        send_socket.close()
        print(f"Closing connection to {current_client[0]}:{current_client[1]}")

    clients.clear()
    serverSocket.close()
    sys.exit(0)


if __name__ == '__main__':
    terminalInput = argparse.ArgumentParser(description="TCP server/client Initialization")
    terminalInput.add_argument('port', type=int, help='Listening Port')

    # myip function but called in main to globally store ipv4
    sock1 = socket(AF_INET, SOCK_DGRAM)
    try:
        sock1.connect(("8.8.8.8", 80))  # Connect to Google DNS
        ipv4 = sock1.getsockname()[0]
    except OSError as e1:
        print(f"Unable to fetch IP address: {e1}")
    except Exception as e1:
        print(f"Unexpected Error: {e1}")  # Exception catch/error message
    finally:
        sock1.close()

    args = terminalInput.parse_args()
    serverThread = threading.Thread(target=server, args=(args.port,))
    clientThread = threading.Thread(target=client, args=())

    serverThread.start()
    clientThread.start()

    serverThread.join()
    clientThread.join()
