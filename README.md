# Caching Proxy Server

This project is a command-line interface (CLI) tool that starts a caching proxy server. The proxy server forwards client requests to an origin server, caches the responses, and returns cached responses when repeated requests are made. This caching mechanism improves efficiency by reducing redundant requests to the origin server.

This project is based on backend challenge called "Caching Proxy" from [roadmap.sh](https://roadmap.sh/), intended to deepen understanding of caching and request forwarding in network programming.

## Features
- **Request Forwarding**: Forwards client requests to the specified origin server.
- **Response Caching**: Caches responses to avoid redundant requests to the origin server.
- **Cache Expiration**: Supports cache expiration to maintain up-to-date content.
- **Cache Status Header**: Adds an `X-Cache` header to responses, indicating if the response is from the cache (`HIT`) or the origin server (`MISS`).
- **Clear Cache Command**: Supports clearing the cache while the server is running.

## Usage

### Starting the Caching Proxy Server

To start the caching proxy server, use the following command:

```bash
python main.py --port <number> --origin <url>
```

--port: The port on which the caching proxy server will run.
--origin: The URL of the origin server to which the requests will be forwarded.

Example:

```bash
python main.py --port 8080 --origin "http://dummyjson.com"
```

### Clearing the Cache

While the server is running, you can manually clear the cache by entering the --clear-cache command: