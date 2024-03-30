import sys, pathlib
import threading
import json
import os
from urllib.parse import urlparse

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.parent))
from handler.db_handler import DBHanlder
from handler.request_router import RequestRouter
from handler.request_handler.base_request_handler import BaseRequestHandler

import config

class DeleteImageHandler(BaseRequestHandler):
    def method():   return "DELETE"
    def path():     return "/api/image/([0-9]+)"

    lock = threading.Lock()
    def _handle(self, req: RequestRouter):
        # Get img id to delete
        img_id = urlparse(req.path).path.split('/')[-1]

        with DeleteImageHandler.lock: # Prevent multiple requests
            # Query & check img
            imgs = DBHanlder.dbMain.query_img_by_id(img_id)
            if len(imgs) == 0:
                self._set_resp(404, f"Imange not found. Id'{img_id}'")
                return

            # Delete in database
            db_resp = DBHanlder.dbMain.delete_img(img_id)
            if db_resp != True:
                self._set_resp(500, f"Failed to delete image. Id'{img_id}' {db_resp if db_resp is not None else ""}")
                return

            # Response OK
            self._set_resp(200, json.dumps({ "resp": "Delete image successfully" }))

            # Delete in local path
            filename = imgs[0][1]
            os.unlink(os.path.join(os.getcwd(), config.DATASET_PATH, filename))
