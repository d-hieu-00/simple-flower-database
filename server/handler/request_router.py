import os
import re
import sys, pathlib
import mimetypes

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from utils.utils import logger
import config

class Router:
    def __init__(self):
        self.__routes = {}

    def register(self, method: str, path: str, handler):
        if method not in self.__routes:
            self.__routes[method] = {}
        if path in self.__routes[method]:
            raise Exception(f"Already register handler for '{method}' -- '{path}'")
        self.__routes[method][path] = handler

    def route(self, method: str, path: str):
        handler = None
        if method in self.__routes:
            for r_path in self.__routes[method]:
                if re.match(r_path, path) != None:
                    handler = self.__routes[method][r_path]
        return handler

class RequestRouter(BaseHTTPRequestHandler):
    __web_dir    = os.path.join(os.getcwd(), config.WEB_DIST)
    __data_dir   = os.path.join(os.getcwd(), config.DATASET_PATH)
    __req_router = Router()

    @classmethod
    def register_handler(cls, method, path, handler):
        cls.__req_router.register(method, path, handler)

    @property
    def __class_name(self): return self.__class__.__name__

    def log_message(self, format, *args):
        logger.info(self.__class_name, __msg = (format % args))

    def log_error(self, format, *args):
        logger.error(self.__class_name, __msg = (format % args))

    def log_request(self, code='-', size='-'):
        if isinstance(code, HTTPStatus): code = code.value
        if "dataset" in self.requestline and code == 200:
            logger.debug(self.__class_name, self.address_string(), self.requestline, str(code), size)
        else:
            logger.info(self.__class_name, self.address_string(), self.requestline, str(code), size)

    def do_METHOD(self, method):
        if method not in ('GET', 'POST', 'PUT', 'DELETE'):
            self.send_error(403)

    def do_PUT(self):       self.route_request('PUT')
    def do_POST(self):      self.route_request('POST')
    def do_DELETE(self):    self.route_request('DELETE')

    def do_GET(self):
        if self.path.startswith('/api/'):
            self.route_request('GET')
        elif self.path.startswith("/dataset/"):
            self.handle_data_request()
        else:
            self.handle_ui_request()

    def route_request(self, method):
        in_path = urlparse(self.path).path
        handler = self.__req_router.route(method, in_path)
        if handler:
            handler().handle(self)
        elif in_path.startswith("/api/"):
            self.handle_ui_request(403)
        else:
            self.handle_ui_request()

    def handle_data_request(self):
        # Serve UI files
        req_file  = urlparse(self.path).path.replace("/dataset/", "")
        filename  = os.path.join(self.__data_dir, req_file)
        if os.path.isfile(filename) == False:
            self.send_response(404)
            self.end_headers()
            return
        self.send_file(filename, 200)

    def handle_ui_request(self, resp_code = 200):
        # Serve UI files
        req_file  = urlparse(self.path).path.lstrip('/')
        filename  = os.path.join(self.__web_dir, req_file)
        if os.path.isfile(filename) == False:
            resp_code = 404
            filename = os.path.join(self.__web_dir, 'index.html')
        self.send_file(filename, resp_code)

    def send_file(self, filepath, resp_code):
        with open(filepath, 'rb') as f:
            mimetype = mimetypes.guess_type(filepath)
            self.send_response(resp_code)
            if mimetype[0] is not None:
                self.send_header('Content-type', mimetype[0])
            else:
                self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read())

sys.path.append(str(pathlib.Path(__file__).parent))
import request_handler.register_request_handler as register
register.register_handler()
