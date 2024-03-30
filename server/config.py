CERTIFICATE_PATH = ''
USE_TLS          = False
PORT             = 80

DATABASE_CONF    = {
    "host": "192.168.56.101",
    "user": "postgres",
    "password": "a"
}

DATABASE_NAME    = "db_flower"
DATABASE_SCHEMA  = "flower_f1"

WEB_DIST         = "../web/dist"
DATASET_PATH     = "../dataset"
NEW_DATASET_PATH = "../dataset/new" # For new image only

THRESHOLD        = 0.2

from utils.utils import logger
from utils.utils import make_dir_if_not_exists

LOG_LEVEL       = logger.INFO
LOG_FILE        = None

import os
make_dir_if_not_exists(os.path.join(os.getcwd(), NEW_DATASET_PATH))
