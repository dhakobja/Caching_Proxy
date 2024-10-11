import sys
import validators

def extractPortUrl(arguments):
    port_number = None
    url = None

    for i, argument in enumerate(arguments):
        if argument.startswith("--help"):
            displayCLIHelp()
            exit()
        if argument.startswith("--port"):
            port_number = sys.argv[i+1]
        elif argument.startswith("--origin"):
            url = sys.argv[i+1]
    
    checkPortUrlValues(port_number, url)
    
    return port_number, url

def displayCLIHelp():
    print("Usage: main.py --port <number> --origin <url>")

def checkPortUrlValues(port_number, url):
    if port_number == None:
        raise Exception("The Port_number was not set. For help, use the --help flag!")
    if len(port_number) > 0 and len(port_number) < 65535:
        raise Exception("Invalid Port Number!")
    
    if url == None:
        raise Exception("The Origin was not set. For help, use the --help flag!")
    
    if not validators.url(url):
        raise Exception("Invalid URL!")

def main():
    port_number, url = extractPortUrl(sys.argv)


if __name__ == "__main__":
    main()