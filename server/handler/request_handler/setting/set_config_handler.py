import sys, pathlib
import json

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.parent))
from utils.utils import is_json
from handler.db_handler import DBHanlder
from handler.request_router import RequestRouter
from handler.request_handler.base_request_handler import BaseRequestHandler

class SetConfigHandler(BaseRequestHandler):
    def method():   return "PUT"
    def path():     return "/api/config"

    def _handle(self, req: RequestRouter):
        body = self._read_body(req).decode('utf-8')
        # Check config format
        if body is None or is_json(body) == False:
            self._set_resp(400, "Invalid body")
            return
        # Save to DB
        db_resp = DBHanlder.dbMain.save_conf(body)
        if db_resp is None:
            self._set_resp(500, f"Failed to update config '{body}'")
            return
        # Response OK
        self._set_resp(200, json.dumps({ "resp": "Save config successfully" }))
