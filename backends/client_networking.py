import sys
import socket
import os


server_ip, server_port = "10.13.1.89", 3325
file_name = "[" + os.path.basename(sys.argv[0]) + "] "


def send_request(module_name, function_name, num_retries=0, max_retries=3):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_ip, server_port))
        print(file_name + "Connection has been opened.")
        client_socket.send(bytes(module_name + " " + function_name, "utf-8"))
        print(file_name + "Request has been sent to server.")
        client_socket.settimeout(5)
        received_msg = client_socket.recv(1024).decode()
        print(file_name + "Response has been received from server: " + received_msg)
        client_socket.close()
        print(file_name + "Connection has been closed.")
        num_retries = 0
    except ConnectionRefusedError:
        print(file_name + "Error: Connection was refused. Is the server online?")
        if num_retries > max_retries:
            print(file_name + "Max number of retries has been met. Dropping request.")
            num_retries = 0
            return False
        else:
            print(file_name + "Retrying connection to server.")
            num_retries += 1
            return send_request(module_name, function_name, num_retries)
    except TimeoutError:
        print(file_name + "Error: Timeout while connecting to server. Are you using the right server IP?")
    except socket.timeout:
        print(file_name + "Error: Timeout while waiting for server to respond.")


if __name__ == "__main__":
    input_module_name = input("What module are you wanting to use? ")
    input_function_name = input("What function are you wanting to call? ")
    send_request(input_module_name, input_function_name)
