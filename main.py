import sys
import validators
import socket
import threading
from datetime import datetime

from server import createServerSocket, forwardClientRequest, responseWithCachedStatus

def extractPortUrl(arguments):
    port_number = None
    url = None

    for i, argument in enumerate(arguments):
        if argument.startswith("--help"):
            print("Usage: main.py --port <number> --origin <url>")
            exit()
        if argument.startswith("--port"):
            port_number = int(sys.argv[i+1])
        elif argument.startswith("--origin"):
            url = sys.argv[i+1]
    
    checkPortUrlValues(port_number, url)
    
    return port_number, url

def checkPortUrlValues(port_number: int, url: str):
    if port_number == None:
        raise Exception("The Port_number was not set. For help, use the --help flag!")
    if port_number < 0 and port_number > 65535:
        raise Exception("Invalid Port Number!")
    
    if url == None:
        raise Exception("The Origin was not set. For help, use the --help flag!")
    
    if not validators.url(url):
        raise Exception("Invalid URL!")

def clear_cache_input(cached_responses: dict):
    while True:
        try:
            user_input = input("Available Commands: --clear-cache\n")
            if user_input.strip() == "--clear-cache":
                cached_responses.clear()
                print("Cache cleared successfully!\n")
        except EOFError:
            break

def cached_response_expired(cached_responses: dict, client_request: str, cache_expiration_time: int) -> bool:
    timestamp_response = cached_responses[client_request]["timestamp"]

    current_time = datetime.now()

    difference_in_seconds = (current_time - timestamp_response).total_seconds()

    if difference_in_seconds > cache_expiration_time:
        return True
    
    return False

def main():
    port_number, url = extractPortUrl(sys.argv)
    cached_responses = {}

    server_socket = createServerSocket(port_number)
    server_socket.settimeout(1)

    # Start the thread that listens for the 'clear-cache' command 
    input_thread = threading.Thread(target=clear_cache_input, args=(cached_responses,), daemon=True)
    input_thread.start()

    cache_expiration_time_seconds = 10

    with server_socket:
        while True:
            try:
                server_socket.listen(1)
                client_conn, _ = server_socket.accept()
                with client_conn:
                    client_request = client_conn.recv(8192)
                    
                    if client_request in cached_responses and not cached_response_expired(cached_responses, client_request, cache_expiration_time_seconds):
                        response = cached_responses[client_request]["response"]
                        modified_response = responseWithCachedStatus(response, True)
                    else:                  
                        response = forwardClientRequest(client_request, url)
                        timed_response = {
                            "response": response,
                            "timestamp": datetime.now()
                        }

                        cached_responses[client_request] = timed_response

                        modified_response = responseWithCachedStatus(response, False)

                    client_conn.sendall(modified_response)
            except socket.timeout:
                pass
            except KeyboardInterrupt:
                print("Shutting down the server.")
                break

if __name__ == "__main__":
    main()