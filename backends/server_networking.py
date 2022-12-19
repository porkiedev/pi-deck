# Notes
# For added security, consider allowing the server to only accept connections from specific ip(s)
# Incorporate a timeout for a client connection, so they can't hang the server indefinitely


# Imports
import socket
import threading
import event_handler
import time
import json


# Variables
script_name = "[ServerNetworkHandler] "
server_ip, server_port = "0.0.0.0", 3325


# Functions
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((server_ip, server_port))
        server_socket.listen(1)
        while True:
            client, (client_ip, client_port) = server_socket.accept()
            data = client.recv(1024)
            if not data:
                continue
            received_message = json.loads(data.decode())
            if received_message["module_name"] == "server" and received_message["function_name"] == "exit":
                break
            elif event_handler.run_module_function(received_message):
                args = json.dumps({"status": "success"})
                client.send(bytes(args, "utf-8"))
            else:
                args = json.dumps({"status": "failure"})
                client.send(bytes(args, "utf-8"))
            client.close()
    except socket.error:
        print(script_name + "Error: Server port is already in use, retrying in 5 seconds.")
        time.sleep(5)
        return main()


def start():
    print(script_name + "Starting server in separate thread.")
    thread = threading.Thread(target=main)
    thread.start()


def stop():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", server_port))
        args = {
            "module_name": "server",
            "function_name": "exit"
        }
        args = json.dumps(args)
        s.send(bytes(args, "utf-8"))
        s.close()


if __name__ == "__main__":
    print(script_name + "Server was run directly, now entering development mode.")
    start()
    try:
        user_input = input("Press enter to exit\n")
        stop()
    except KeyboardInterrupt:
        stop()
