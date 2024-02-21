# Filip Maletic (250866829)
# CS 3357A Assignment 2: UDP Simple Chat Room - UDP Client Code Implementation
# October 19, 2023

# **Libraries and Imports**: 
import socket
import threading
import sys
import random

# **Global Variables**:
PORT = 9301
SERVER_IP = "127.0.0.1"
ADDR = (SERVER_IP, PORT)
username = input("Please enter your username: ")

# **Function Definitions**:

# This fucntion recieves messages from the UDP server and prints them for the client to see.
def receive_message():
    while True:
        try:
            message, _ = client_socket.recvfrom(1024)
            decoded_message = message.decode()
            # Ignores displaying the Choose_Username message on the client side.
            if not decoded_message.startswith("Choose_Username:"):
                print(decoded_message)
        except:
            pass

# **Main Code**:  
if __name__ == "__main__":
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    # Binds clients to different ports using random numbers between 7000 and 9000.
    client_socket.bind((SERVER_IP, random.randint(7000, 9000)))
    # Creates and starts thread for recieved messages.
    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()
    # Sends username of the client to the server.
    client_socket.sendto(f"Choose_Username:{username}".encode(), (ADDR))

    while True:
        try:
            # Takes user input for any message.
            message = input(" ")
            # If user types exit, the connection is closed.
            if message.upper() == "EXIT":
                client_socket.sendto('EXIT'.encode(), ADDR)
                client_socket.close()
                sys.exit(0)
            else:
                client_socket.sendto(f"{username}: {message}".encode(), (ADDR))
        except KeyboardInterrupt:
            client_socket.close()
            sys.exit(0)
   
