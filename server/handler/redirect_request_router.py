import sys, pathlib
from http.server import BaseHTTPRequestHandler

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent))
import config

class RedirectRequestRouter(BaseHTTPRequestHandler):
    def do_METHOD(self, _):
        # Set response status code
        self.send_response(302)  # 302 Found (temporary redirect)
        # Set Location header to redirect to another port
        new_location = f"http://{self.server.server_name}:{config.PORT}{self.path}"
        self.send_header('Location', new_location)
        # End headers
        self.end_headers()
