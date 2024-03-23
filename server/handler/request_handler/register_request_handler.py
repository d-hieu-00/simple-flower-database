from handler.request_router import RequestRouter

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).parent))

from setting.get_config_handler import GetConfigHandler
from setting.set_config_handler import SetConfigHandler

from image.add_img_handler import AddImageHandler
from image.del_img_handler import DeleteImageHandler
from image.get_img_handler import GetImageHandler
from image.get_token_from_img_handler import GetTokensFromImageHandler

def register_handler():
    RequestRouter.register_handler(GetConfigHandler.method(), GetConfigHandler.path(), GetConfigHandler)
    RequestRouter.register_handler(SetConfigHandler.method(), SetConfigHandler.path(), SetConfigHandler)

    RequestRouter.register_handler(AddImageHandler.method(), AddImageHandler.path(), AddImageHandler)
    RequestRouter.register_handler(DeleteImageHandler.method(), DeleteImageHandler.path(), DeleteImageHandler)
    RequestRouter.register_handler(GetImageHandler.method(), GetImageHandler.path(), GetImageHandler)
    RequestRouter.register_handler(GetTokensFromImageHandler.method(), GetTokensFromImageHandler.path(), GetTokensFromImageHandler)
