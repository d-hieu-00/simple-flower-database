import sys, pathlib

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from database.db_main import DBMain

class DBHanlder:
    dbMain = DBMain()
