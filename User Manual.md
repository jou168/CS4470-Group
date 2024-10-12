--------------User Guide for chat program--------------

To start the program use open the terminal and navigate to the directory holding the process file
Type chat.py <port number> to start the chat application

User Command Guide:

**help**: Lists all available commands for any end user, as well as the functionalities and how to invoke the commands
**myip**: Displays the personal computer's ipv4 address
**myport**: Displays the port on which the server is listening to, which is designated on process startup
**connect <destination> <port number>:** establishes a connection to another user when inputting the command with the other user's ipv4 address and port number of their server 
**list:** Displays a numbered list of all user connections, with corresponding information, initiated or accepted by the process.
**terminate <connection id>**: Upon using list, ids assigned to each connection are to be used with the terminate command if the user wants to attempt disconnecting from any other client.
**send <connection id> <message>**: Users may send messages to other users given they are connected prior to the message being sent. id's can be obtained from the list function and messages must be less than 100 characters.
**exit**: Closes the program and any existing connections to other users.
