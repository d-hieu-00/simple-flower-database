import sys, pathlib
import json
import mimetypes
import os, tempfile

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.parent))
from utils.utils import save_to_file
from handler.db_handler import DBHanlder
from handler.model_handler_v1 import ModelHandlerV1
from handler.request_router import RequestRouter
from handler.request_handler.base_request_handler import BaseRequestHandler

import config

class AddImageHandler(BaseRequestHandler):
    def method():   return "POST"
    def path():     return "/api/image"

    def __init__(self) -> None:
        super().__init__()
        self.__tmpFile = None

    def __del__(self):
        if self.__tmpFile is not None:
            self.__tmpFile.close()
            os.unlink(self.__tmpFile.name) # Remove temp file

    def initTmpFile(self, file_extension):
        self.__tmpFile = tempfile.NamedTemporaryFile(suffix=file_extension, delete=False)

    def _handle(self, req: RequestRouter):
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

        # Try extract features
        features = ModelHandlerV1.img_to_features(self.__tmpFile.name)

        if features is None:
            self._set_resp(400, f"Failed to process the image. It doesn't seem like a flower.")
            return

        # Try save to dataset & DB
        _filename  = self.__tmpFile.name.split("\\")[-1]
        _save_path = os.path.join(os.getcwd(), config.NEW_DATASET_PATH, _filename)
        save_to_file(data, _save_path)

        _prefix    = "/".join([i for i in config.NEW_DATASET_PATH.split("/") if i not in config.DATASET_PATH.split("/")])
        _filename  = "/".join([_prefix, self.__tmpFile.name.split("\\")[-1]])
        img_id = DBHanlder.dbMain.save_img(_filename, features)
        if type(img_id) != int or img_id < 1:
            self._set_resp(500, f"Failed to save the image. Something went wrong.")
            return

        # Response OK
        self._set_resp(200, json.dumps({ "resp": DBHanlder.dbMain.query_img_by_id(img_id)[0] }))
