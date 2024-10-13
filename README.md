# Multi-Threaded TCP Client-Server Chat Application

This project is a multi-threaded TCP client-server chat application that allows multiple clients to connect to a server, communicate with each other, and manage connections through various commands. The server is capable of handling multiple clients simultaneously, thanks to threading. The project is written in Python and leverages the `socket` library for networking.

## Features

- **Multi-threaded Server**: Supports multiple client connections using threading.
- **Client Commands**: Includes commands such as `connect`, `send`, `list`, `terminate`, and `exit`.
- **Ephemeral Ports**: Utilizes ephemeral ports for client-server connections, allowing clients to use random, temporary ports for communication.
- **Interactive Command Line**: Provides a user-friendly CLI for executing commands.
- **Connection Management**: Clients can manage connections, view active connections, and terminate connections by ID.
  
## Requirements

- **Python 3.x**
- Libraries: No additional libraries are needed apart from Python's standard library.

## Setup and Usage

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/CS4470-Group.git
cd CS4470-Group
```
### Step 2: Run the Server and Client

The application consists of both a server and client. To get started, follow these steps:

    Start the Server: The server must be started first. Use the command below to specify the port on which the server should listen.

    bash

    python your_script_name.py <port_number>

    Replace <port_number> with the desired port, such as 5555.

### Commands

Once connected to the server, you can use the following commands:

    help: Display a list of available commands.

    myip: Show the client’s IP address.

    myport: Show the client’s port number.

    connect <IP> <port>: Connect to another client using their IP address and port number.

    list: Display the list of all active connections with their IDs, IP addresses, and ports.

    terminate <connection_id>: Terminate a connection using the connection ID.

    send <connection_id> <message>: Send a message to a specific client using the connection ID.

    exit: Close all active connections and shut down the client.

### Example Usage

To connect to a peer with IP 192.168.1.100 on port 5555:

bash

connect 192.168.1.100 5555

To send a message to a connected client with ID 1:

bash

send 1 Hello, World!

To terminate a connection:

bash

terminate 1

## Implementation Details

- Server and Client Handling: The server listens for incoming connections on a specified port, while clients can initiate connections and communicate with other clients.
- Ephemeral Ports: When clients initiate connections, they use ephemeral ports assigned by the OS. This allows multiple connections from the same client.
- Threading: The server spawns a new thread for each client connection, enabling concurrent message handling.

## Error Handling

The application includes error handling for various scenarios, including invalid IP addresses, connection failures, and incorrect command usage. Each function has been designed to print useful error messages to assist users.
