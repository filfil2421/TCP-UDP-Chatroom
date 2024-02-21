# Filip Maletic (250866829)
# CS 3357A Assignment 2: TCP Simple Chat Room - TCP Server Code Implementation
# October 19, 2023

# **Libraries and Imports**: 
import socket
import threading
import sys

# **Global Variables**:
PORT = 9301
SERVER_IP = "127.0.0.1"
ADDR = (SERVER_IP, PORT)
clients = [] #list to add the connected client sockets
usernames = [] #list to add the connected clients' usernames

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating a TCP socket.
server_socket.bind((ADDR))
server_socket.listen(3) # size of the waiting_queue that stores the incoming requests to connect.
    
# **Function Definitions**:

# This function handles each individual client. It is always trying to recieve a message and handles errors and disconnections.
def handling_client(client, address):
    client_index = clients.index(client)
    username = usernames[client_index]
    try:
        while True:
            # Try to recieve a message and if successful display it to all clients.
            try:
                message = client.recv(1024)
                # Client initiated disconnect. The connection to the client is closed and the client is removed from both lists.
                if message.strip().upper() == "EXIT":
                    clients.remove(client)
                    client.close()
                    usernames.remove(username)
                    broadcast_message(f"{username} has left the chat.".encode())
                    print(f"User: {username} left the server.")
                    break
                print(f"Message recieved from {username} at {address}: {message}") # Displays each messages' contents and who/where it's coming from in the server console.
                broadcast_message(message) # Broadcasts message to all clients.
            # If there is an error while recieving a message, the connection to the client is closed and the client is removed from both lists.
            except:
                clients.remove(client)
                client.close()
                usernames.remove(username)
                broadcast_message(f"{username} has left the chat.".encode())
                print(f"User: {username} left the server.")
                break
    except KeyboardInterrupt:
        server_socket.close()
        print("The server has been closed")
        sys.exit(0)

# This function sends and broadcasts a message to all clients currently connected (everyone can see the message).
def broadcast_message(message):
    for client in clients:
        client.send(message)

# This is the main server function
def run(serverSocket, serverPort):
    try:
        while True:
            client, address = serverSocket.accept()
            print(f"Successful connection with: {str(address)}")
            # Asking client for username. If the client recieves the user keyword, the client will send it's username to the server.
            client.send('USER'.encode())
            username = client.recv(1024).decode()
            # Stores the client and the associated username if successful.
            usernames.append(username)
            clients.append(client)
            print(f"Client username: {username}")
            # Shows all current connected clients if someone joins the chat.
            broadcast_message(f"{username} has joined the chat.".encode())
            # Creates a thread for each client so events can be proccessed at the same time.
            thread = threading.Thread(target=handling_client, args=(client, address))
            thread.start()
    except KeyboardInterrupt:
        server_socket.close()
        print("The server has been closed")
        sys.exit(0)
    except Exception as error:
        server_socket.close()
        print(f"The following error occured: {error}")
        sys.exit(0)

# **Main Code**:  
if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating a TCP socket.
    server_socket.bind((ADDR))
    server_socket.listen(3) # size of the waiting_queue that stores the incoming requests to connect.
    print("TCP server has been started and is listening...")
    run(server_socket, PORT)# Calling the function to start the server.
