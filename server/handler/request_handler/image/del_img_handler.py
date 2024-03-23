import sys, pathlib
import sys, pathlib
import json
from urllib.parse import urlparse

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.parent))
from handler.db_handler import DBHanlder
from handler.request_router import RequestRouter
from handler.request_handler.base_request_handler import BaseRequestHandler

class DeleteImageHandler(BaseRequestHandler):
    def method():   return "DELETE"
    def path():     return "/api/image/([0-9]+)"

    def _handle(self, req: RequestRouter):
        # Get img id to delete
        img_id = urlparse(req.path).path.split('/')[-1]

        # Delete in database
        db_resp = DBHanlder.dbMain.delete_img(img_id)
        if db_resp is None:
            self._set_resp(500, f"Failed to delete image. Id'{img_id}'")
            return

        # Response OK
        self._set_resp(200, json.dumps({ "resp": "Delete image successfully" }))
