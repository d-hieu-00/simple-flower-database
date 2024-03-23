CERTIFICATE_PATH = ''
USE_TLS          = False
PORT             = 80
DB_PATH          = "../database/flower.db.sqlite"
SAVED_MODEL      = "../model/saved"
WEB_DIST         = "../web/dist"
DATASET_PATH     = "../dataset"
NEW_DATASET_PATH = "../dataset/new" # For new image only

from utils.utils import logger
from utils.utils import make_dir_if_not_exists

LOG_LEVEL       = logger.INFO
LOG_FILE        = None

import os
make_dir_if_not_exists(os.path.join(os.getcwd(), NEW_DATASET_PATH))
