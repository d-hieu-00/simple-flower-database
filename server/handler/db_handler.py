import sys, pathlib

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from database.db_main_v1 import DBMainV1

class DBHanlder:
    dbMain = DBMainV1()
