# echo-client.py

import socket
import ipaddress
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
ip = ""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello, world")
    data = s.recv(1024)
    stringip = str(data)[2:-1]
    print(data)
    print(stringip)
    ip = ipaddress.ip_address(stringip)

print(f"Received {data!r}")