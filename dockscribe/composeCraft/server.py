import json
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import webbrowser

from .utils import get_app_data_path


def open_browser(url):
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Can't automatically open '{url}'")

class ShutdownHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_params = parse_qs(urlparse(self.path).query)
        token = query_params.get("token", [None])[0]  # Get the token value
        print(token)

        if token :
            # Respond with a simple message
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Connection", "close")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"You are successfully logged in. You can close this page.")
            self.wfile.flush()

            config_path = get_app_data_path()+"/config.json"
            with open(config_path,"w+") as f:
                f.write(json.dumps({"token":token}))
            print(f"config file written to {config_path}")

            # Signal the server to shut down from a separate thread
            threading.Thread(target=self.server.shutdown).start()
        else:
            self.send_response(400)
            self.send_header("Content-type", "text/plain")
            self.send_header("Connection", "close")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"Token is missing.")
            self.wfile.flush()

def run_server(port: int):
    """
    Starts an HTTP server that shuts down after a GET request.
    """
    try:
        server = HTTPServer(('localhost', port), ShutdownHTTPRequestHandler)
        print(f"Wait for login on {os.getenv('CC_URL','https://composecraft.com')}/login/cli ...")
        open_browser(f"{os.getenv('CC_URL','https://composecraft.com')}/login/cli")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nCmd interrupted by user.")
    finally:
        server.server_close()