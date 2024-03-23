import sys, pathlib

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.parent))
from handler.db_handler import DBHanlder
from handler.request_router import RequestRouter
from handler.request_handler.base_request_handler import BaseRequestHandler

class GetConfigHandler(BaseRequestHandler):
    def method():   return "GET"
    def path():     return "/api/config"

    def _handle(self, _: RequestRouter):
        response = DBHanlder.dbMain.query_conf()
        if response is None:
            self._set_resp(500, "Failed to query config")
        else:
            self._set_resp(200, response)
