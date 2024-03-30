import sys, pathlib
import json
import time
from urllib.parse import parse_qs, urlparse

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.parent))
from utils.utils import logger
from handler.db_handler import DBHanlder
from handler.model_handler_v1 import ModelHandlerV1
from handler.request_router import RequestRouter
from handler.request_handler.base_request_handler import BaseRequestHandler

class GetImgByTextHandler(BaseRequestHandler):
    def method():   return "GET"
    def path():     return "/api/image"

    def verify_params(self, in_req_path: str):
        in_params = parse_qs(urlparse(in_req_path).query)
        out_first = None
        out_size  = None
        out_query = None
        # Try parse params
        try:
            if "size" in in_params:
                out_size = int(in_params["size"][0])
            if "first" in in_params:
                out_first = int(in_params["first"][0])
            if "query" in in_params:
                out_query = in_params["query"][0]
            else:
                self._set_resp(400, f"Missing required params 'query'")
                return None
        except Exception as e:
            self._set_resp(400, f"Invalid data to query '{in_req_path}' -- {str(e)}")
            return None
        # Try verify params
        try:
            if (out_size is not None and out_size < 1) \
                    or (out_first is not None and out_first < 1) \
                    or out_query == "":
                self._set_resp(400, f"Invalid data to query")
                return None
        except Exception as e:
            self._set_resp(400, f"Invalid data to query '{in_req_path}' -- {str(e)}")
            return None
        # Out params
        return (out_first, out_size, out_query)

    def _handle(self, req: RequestRouter):
        # Parse and verify params
        params = self.verify_params(req.path)
        if params is None:
            return
        # Features
        start_ts = int(time.time() * 1000)
        features = ModelHandlerV1.txt_to_features(params[2])
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
