import sys, pathlib
import json
import mimetypes
import os, tempfile
import time
from urllib.parse import parse_qs, urlparse

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.parent))
from utils.utils import logger
from utils.utils import save_to_file
from handler.db_handler import DBHanlder
from handler.model_handler_v1 import ModelHandlerV1
from handler.request_router import RequestRouter
from handler.request_handler.base_request_handler import BaseRequestHandler

class GetImgByImgHandler(BaseRequestHandler):
    def method():   return "POST"
    def path():     return "/api/image/query"

    def __init__(self) -> None:
        super().__init__()
        self.__tmpFile = None

    def __del__(self):
        if self.__tmpFile is not None:
            self.__tmpFile.close()
            os.unlink(self.__tmpFile.name) # Remove temp file

    def initTmpFile(self, file_extension):
        self.__tmpFile = tempfile.NamedTemporaryFile(suffix=file_extension, delete=False)

    def verify_params(self, in_req_path: str):
        in_params = parse_qs(urlparse(in_req_path).query)
        out_first = None
        out_size  = None
        # Try parse params
        try:
            if "size" in in_params:
                out_size = int(in_params["size"][0])
            if "first" in in_params:
                out_first = int(in_params["first"][0])
        except Exception as e:
            self._set_resp(400, f"Invalid data to query '{in_req_path}' -- {str(e)}")
            return None
        # Try verify params
        try:
            if (out_size is not None and out_size < 1) \
                    or (out_first is not None and out_first < 1):
                self._set_resp(400, f"Invalid data to query")
                return None
        except Exception as e:
            self._set_resp(400, f"Invalid data to query '{in_req_path}' -- {str(e)}")
            return None
        # Out params
        return (out_first, out_size)

    def _handle(self, req: RequestRouter):
        # Parse and verify params
        params = self.verify_params(req.path)
        if params is None:
            return
        # Check request
        if "content-type" not in req.headers:
            self._set_resp(400, "Invalid request -- data is not an image")
            return
        # Determine file extension based on Content-Type
        content_type = req.headers["content-type"]
        file_extension = mimetypes.guess_extension(content_type, strict=True)
        # Ensure that the file extension corresponds to an image type
        if not file_extension or not file_extension.startswith('.'):
            self._set_resp(400, "Invalid image type")
            return
        # Read data & Allow to read file with 20MB size
        data = self._read_body(req, 20 * 1024 * 1024)
        if data is None :
            self._set_resp(400, "Invalid or missing request data")
            return
        # Save to file
        self.initTmpFile(file_extension)
        save_to_file(data, self.__tmpFile.name)
        # Try extract token
        start_ts = int(time.time() * 1000)
        features = ModelHandlerV1.img_to_features(self.__tmpFile.name)
        if features is None:
            self._set_resp(400, f"Failed to process the image. It doesn't seem like a flower.")
            return
        end_ts = int(time.time() * 1000)
        process_time = end_ts - start_ts
        # Query from DB
        start_ts = int(time.time() * 1000)
        db_resp = DBHanlder.dbMain.query_img(features, params[0], params[1])
        if db_resp is None or len(db_resp) != 2:
            logger.error("Failed to query image. Unknow error", db_resp)
            self._set_resp(500, db_resp if db_resp is not None else f"Failed to query image. Unknow error.")
            return
        end_ts = int(time.time() * 1000)
        # Response OK
        self._set_resp(200, json.dumps({
            "count": db_resp[0],
            "resp": db_resp[1],
            "db_time": end_ts - start_ts,
            "ext_time": process_time
        }))
