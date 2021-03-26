#!/bin/python3
import socketserver
from http.server import SimpleHTTPRequestHandler as Handler

# settings
PORT = 8080

# start server at localhost
with socketserver.TCPServer(("",PORT), Handler) as httpd:
    print(
        "HTTP local server is serving for test at port",PORT,
        "\nbeware of using sweetheart for production purposes"
        "\npress Ctrl-C to quit..."
        )
    try: httpd.serve_forever()
    except: print("\nHTTP server stopped")
