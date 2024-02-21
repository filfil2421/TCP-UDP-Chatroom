# Filip Maletic (250866829)
# CS 3357A Assignment 2: UDP Simple Chat Room - UDP Server Code Implementation
# October 19, 2023

# **Libraries and Imports**: 
import socket
import threading
import queue
import sys

# **Global Variables**:
PORT = 9301
SERVER_IP = "127.0.0.1"
ADDR = (SERVER_IP, PORT)
messages = queue.Queue() # Messages sent to the server will be stored in a queue so they can be displayed in the order they were recieved.
clients = []

# **Function Definitions**:

# This function recieves and accepts messages, storing them in the queue.
def receive_message():
    while True:
        try:
            message, address = server_socket.recvfrom(1024)
            if message:
                # Handles a client intitiated disconnect from the server and the client is removed from the list.
                if message.decode().upper() == 'EXIT':
                    if address in clients:
                        clients.remove(address)
                        print(f"{address} has left the chat.")
                else:
                    messages.put((message, address))
        except KeyboardInterrupt:
            server_socket.close()
            print("The server has been closed")
            sys.exit(0)

# This function handles displaying messages that have been sent to the server back to all active clients.
def broadcast_message():
    while True:
        try:
            # Gets and dispalys sent messages in order if the queue is not empty.
            while messages.empty() == False:
                message, address = messages.get()
                decoded_message = message.decode()
                # If message is coming from a new client, it adds the client to the list.
                if address not in clients:
                    clients.append(address)
                for client in clients:
                    # If the server receives a message that begins with Choose_Username, it displays to all clients that the specific username has joined the chat.
                    if decoded_message.startswith("Choose_Username:"):
                        username = decoded_message.split(":")[1]
                        server_socket.sendto(f"{username} has joined the chat".encode(), client)
                        print(f"{username} has joined the chat from {address}.")
                else:
                    # Extract the username and message content to show each messages' information in the server console.
                    tempUser = decoded_message.split(':')[0]
                    message_content = decoded_message.split(':')[1]
                    # Displays each messages' contents and who/where it's coming from in the server console.
                    print(f"Message from {tempUser} at {address}: {message_content}")
                    for client in clients:
                        try:
                            server_socket.sendto(message, client)
                        except:
                            clients.remove(client)
        except KeyboardInterrupt:
            server_socket.close()
            print("The server has been closed.")
            sys.exit(0)
        except Exception as error:
            print(f"The following error occurred: {error}")

# **Main Code**:  
if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
    server_socket.bind(ADDR)
    # Creates and starts thread for recieved messages.
    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()
    # Creates and starts thread for broadcasting messages.
    broadcast_thread = threading.Thread(target=broadcast_message)
    broadcast_thread.start()
    print("UDP server has been started and is listening...")
    