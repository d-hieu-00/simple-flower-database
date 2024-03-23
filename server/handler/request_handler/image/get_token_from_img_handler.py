import sys, pathlib
import json
import mimetypes
import os, tempfile

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.parent))
from utils.utils import save_to_file
from handler.model_handler import ModelHandler
from handler.request_router import RequestRouter
from handler.request_handler.base_request_handler import BaseRequestHandler

class GetTokensFromImageHandler(BaseRequestHandler):
    def method():   return "POST"
    def path():     return "/api/image/token"

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
        data = self._read_body(req, 20480)
        if data is None :
            self._set_resp(400, "Invalid or missing request data")
            return

        # Save to file
        self.initTmpFile(file_extension)
        save_to_file(data, self.__tmpFile.name)

        # Try get token
        token = ModelHandler.img_to_token(self.__tmpFile.name)

        if token is None:
            self._set_resp(400, f"Failed to process the image. It doesn't seem like a flower.")
            return

        # Response OK
        self._set_resp(200, json.dumps({ "resp": token }))
