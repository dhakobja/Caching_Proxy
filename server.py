import socket
from typing import Tuple

def createServerSocket(port_number: int) -> socket.socket:
    addr = ("", port_number)
    server_socket = socket.create_server(addr, family=socket.AF_INET)

    return server_socket    

def forwardClientRequest(client_request:str, url: str) -> str:
    # Strip the protocol from the URL if it exists
    if url.startswith("http://"):
        url = url[len("http://"):]
    elif url.startswith("https://"):
        url = url[len("https://"):]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
        proxy_socket.connect((url, 80)) # Web servers usually provide http services on port 80

        client_request = client_request.replace(b"localhost:8080", url.encode())
        proxy_socket.send(client_request)

        response = proxy_socket.recv(4096)

        return response