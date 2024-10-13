import sys
import validators
import socket

from server import createServerSocket, forwardClientRequest

def extractPortUrl(arguments):
    port_number = None
    url = None

    for i, argument in enumerate(arguments):
        if argument.startswith("--help"):
            displayCLIHelp()
            exit()
        if argument.startswith("--port"):
            port_number = int(sys.argv[i+1])
        elif argument.startswith("--origin"):
            url = sys.argv[i+1]
    
    checkPortUrlValues(port_number, url)
    
    return port_number, url

def displayCLIHelp():
    print("Usage: main.py --port <number> --origin <url>")

def checkPortUrlValues(port_number, url):
    if port_number == None:
        raise Exception("The Port_number was not set. For help, use the --help flag!")
    if port_number < 0 and port_number > 65535:
        raise Exception("Invalid Port Number!")
    
    if url == None:
        raise Exception("The Origin was not set. For help, use the --help flag!")
    
    if not validators.url(url):
        raise Exception("Invalid URL!")

def main():
    port_number, url = extractPortUrl(sys.argv)

    server_socket = createServerSocket(port_number)
    server_socket.settimeout(1)

    with server_socket:
        while True:
            try:
                server_socket.listen(1)
                client_conn, client_addr = server_socket.accept()
                with client_conn:
                    print(f"Connected by {client_addr}")
                    client_request = client_conn.recv(1024)    
                    
                    response = forwardClientRequest(client_request, url)
                    client_conn.sendall(response)
            except socket.timeout:
                pass
            except KeyboardInterrupt:
                print("Shutting down the server.")
                break

if __name__ == "__main__":
    main()