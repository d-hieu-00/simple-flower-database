import sys, pathlib
import threading
import torch
import clip
from PIL import Image

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from utils.utils import logger

def _load_handler():
    logger.info(f"[{__name__}] Loading handler")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    return device, model, preprocess

class ModelHandlerV1:
    __device, __model, __preprocess = _load_handler()
    __lock    = threading.Lock()

    @staticmethod
    def img_to_features(img_path):
        features  = None
        with ModelHandlerV1.__lock:
            image    = ModelHandlerV1.__preprocess(Image.open(img_path)).unsqueeze(0).to(ModelHandlerV1.__device)
            features = ModelHandlerV1.__model.encode_image(image).cpu().detach().numpy().tolist()
        logger.debug(f"[{__name__}] Extract image features result", features)
        if len(features) >= 1:
            return features[0]
        return features

    @staticmethod
    def txt_to_features(in_text):
        features  = None
        with ModelHandlerV1.__lock:
            pre_input = clip.tokenize([in_text]).to(ModelHandlerV1.__device)
            with torch.no_grad():
                features = ModelHandlerV1.__model.encode_text(pre_input).squeeze().cpu().detach().numpy().tolist()
        logger.debug(f"[{__name__}] Extract text features result", features)
        return features
