# Filip Maletic (250866829)
# CS 3357A Assignment 2: TCP Simple Chat Room - TCP Client Code Implementation
# October 19, 2023

# **Libraries and Imports**: 
import socket
import threading
import sys

# **Global Variables**:
PORT = 9301
SERVER_IP = "127.0.0.1"
ADDR = (SERVER_IP, PORT)
username = input("Please enter your username: ")

# **Function Definitions**:

# This function recieves messages from the server and helps set up the user with the server. A thread will handle all the recieved messages.
def receive_message():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            # If the user keyword is received, the username of the client is sent to the server.
            if message == 'USER':
                client_socket.send(username.encode())
            else:
                print(message)
        except Exception as error:
            print(f"The following error occured: {error}")
            client_socket.close()
            break

# This function handles the client writing and sending messages to the server (chatroom). A separate thread will handle all sent messages.
def write_message():
    while True:
        # Is constantly accepting input for messages
        message = f'{username}: {input("")}'
        # If client types exit, the connection to the server is closed and other clients are notified.
        if message.split(':')[-1].strip().upper() == "EXIT":
            client_socket.send('EXIT'.encode())
            client_socket.close()
            sys.exit(0)
        # Regular message is sent to server.
        else:
            client_socket.send(message.encode())

# **Main Code**:  
if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
    client_socket.connect((ADDR))
    # Creates and starts thread for recieved messages.
    recieve_message_thread = threading.Thread(target=receive_message)
    recieve_message_thread.start()
    # Creates and starts thread for sent messages.
    write_message_thread = threading.Thread(target=write_message)
    write_message_thread.start()

    
 
