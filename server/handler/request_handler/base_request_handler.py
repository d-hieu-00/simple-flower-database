import sys, pathlib
import json
from abc import ABC, abstractmethod, abstractclassmethod
from handler.request_router import RequestRouter

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))
from utils.utils import logger
from utils.utils import is_json

class BaseRequestHandler(ABC):
    @abstractclassmethod
    def method():
        pass

    @abstractclassmethod
    def path():
        pass

    def __init__(self) -> None:
        super().__init__()
        self._resp_code = 400
        self._resp_msg  = "Unhandle"
    
    @abstractmethod
    def _handle(self, req: RequestRouter):
        pass

    def _read_body(self, req: RequestRouter, max_len: int = 10 * 1024 * 1024):
        # Expect request body has less than 10MB data
        # If it is larger. Define your own function to read and parse from stream
        if "content-length" not in req.headers:
            logger.warn("Request have no body to read")
            return None
        body_len = int(req.headers['content-length'])
        if body_len > max_len:
            logger.warn(f"Request body is to larger -- max_len: {max_len}, req_size: {body_len}")
            return None
        return req.rfile.read(body_len)

    def _set_resp(self, code: int, msg: str):
        self._resp_code = code
        self._resp_msg  = msg
        # Print log for error resp
        if code != 200:
            logger.warn(f"{self.__req_line} -- Handle failed [{self._resp_code}]: {self._resp_msg}")

    def _send_resp(self, req: RequestRouter):
        req.send_response(self._resp_code)
        if self._resp_code == 200 and self._resp_msg is not None:
            req.send_header('Content-type', 'application/json' if is_json(self._resp_msg) else 'text/plain')
            req.end_headers()
            req.wfile.write(self._resp_msg.encode())
        elif self._resp_code != 200:
            req.send_header('Content-type', 'application/json')
            req.end_headers()
            req.wfile.write(json.dumps({
                "error": self._resp_msg if self._resp_msg is not None else "Something went wrong"
            }).encode())
        else:
            req.end_headers()

    def handle(self, req: RequestRouter):
        self.__req_line = req.requestline
        try:
            self._handle(req)
        except Exception as e:
            logger.error(f"{self.__req_line} -- Handle failed: {str(e)}")
            self._set_resp(500, str(e))
        except:
            logger.error(f"{self.__req_line} -- Handle failed: Unknow Error")
            self._set_resp(500, "Unknow Error")
        self._send_resp(req)
