import sys, pathlib
import threading
from PIL import Image
from transformers import pipeline, AutoModel

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent))
import config
from utils.utils import logger
from utils.utils import process_img_label

from transformers import pipeline

def _load_pipeline():
    logger.info(f"[{__name__}] Loading model")
    return pipeline("image-classification", model = config.SAVED_MODEL)

class ModelHandler:
    __pipe = _load_pipeline()
    __lock = threading.Lock()

    @staticmethod
    def img_to_token(img_path):
        predicts = None
        with ModelHandler.__lock:
            predicts = ModelHandler.__pipe(Image.open(img_path))
        tokens = []
        for predict in predicts:
            if predict["score"] < 0.5:
                continue
            tokens.append(process_img_label(predict["label"]))
        if len(tokens) == 0:
            return None
        return " ".join(tokens).replace(" ", " OR ")

    @staticmethod
    def predict(img_path):
        with ModelHandler.__lock:
            return ModelHandler.__pipe(Image.open(img_path))
