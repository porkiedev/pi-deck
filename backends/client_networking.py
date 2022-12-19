import sys
import socket
import os
import json


sender_server_ip, sender_server_port, = "10.13.1.89", 3325
script_name = "[ClientNetworkHandler] "


def send_message(args):
    try:
        json_args = json.dumps(args)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((sender_server_ip, sender_server_port))
        client_socket.settimeout(5)
        client_socket.send(bytes(json_args, "utf-8"))
        response = json.loads(client_socket.recv(1024).decode())
        print(script_name + "Response from server: " + str(response))
        client_socket.close()
    except socket.error:
        print(script_name + "Error: Either received no response from server in time or connection could not be made.")


if __name__ == "__main__":
    temp_args = json.dumps({
        "module_name": "media_controls",
        "function_name": "media_play_pause"
    })
    while True:
        user_input = input()
        if user_input.lower() == "exit":
            break
        else:
            send_message(temp_args)
