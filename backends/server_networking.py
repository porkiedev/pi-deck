# Notes
# For added security, consider allowing the server to only accept connections from specific ip(s)
# Incorporate a timeout for a client connection, so they can't hang the server indefinitely


# Imports
import os
import socket
import sys
import threading
import event_handler
import time


# Variables
file_name = "[" + os.path.basename(sys.argv[0]) + "] "
server_ip, server_port = "0.0.0.0", 3325


# Functions
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((server_ip, server_port))
    except socket.error:
        print(file_name + "Error: Server port is already in use, retrying in 5 seconds.")
        time.sleep(5)
        return main()
    server_socket.listen(1)

    while True:
        client, (client_ip, client_port) = server_socket.accept()
        client.settimeout(5)
        client_formatted = "[Client: " + client_ip + ":" + str(client_port) + "] "
        print(file_name + client_formatted + "Connection has been opened.")

        try:
            received_message = client.recv(1024).decode().split()
            if received_message[0] == "exit":
                print(file_name + client_formatted + "Client asked server to stop running. "
                                                     "This is for internal use only and likely comes from the server.")
                client.close()
                print(file_name + client_formatted + "Connection has been closed.")
                break
            elif event_handler.run_module_function(received_message[0], received_message[1]):
                client.send(bytes("success", "utf-8"))
            else:
                client.send(bytes("failure", "utf-8"))
            print(file_name + client_formatted + "Client request has been handled.")
        except IndexError:
            print(file_name + client_formatted + "Error: An error occurred while handling client request. "
                                                 "Are you sure it wasn't a malformed request?")
        except socket.timeout:
            print(file_name + client_formatted + "Warning: Client timeout of 5 seconds has been hit. "
                                                 "Disconnecting from client so the server doesn't lock up.")
        client.close()
        print(file_name + client_formatted + "Connection has been closed.")


def start():
    print(file_name + "Starting server in separate thread.")
    thread = threading.Thread(target=main)
    thread.start()


def stop():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", server_port))
        s.send(bytes("exit", "utf-8"))
        s.close()


if __name__ == "__main__":
    print(file_name + "Server was run directly, now entering development mode.")
    start()
    try:
        user_input = input("Press enter to exit\n")
        stop()
    except KeyboardInterrupt:
        stop()
