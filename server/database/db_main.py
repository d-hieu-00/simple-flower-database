import sys, pathlib
import threading
import json

# Internal
sys.path.append(str(pathlib.Path(__file__).parent.parent))
import config
from utils.utils import logger
from utils.utils import safe_execute
from utils.utils import process_img_label
from utils.utils import process_sel_tokens
from database.db_connector import DBConnector

class DBMain:
    __predict_threshold = 0.1

    @property
    def class_name(self): return self.__class__.__name__

    def __init__(self, db_config = { "path": config.DB_PATH }):
        self.__connector = DBConnector(DBConnector.SQLite3, db_config)
        self.__rconn = self.__connector.new_connection()
        self.__wconn = self.__connector.new_connection()
        self.__wlock = threading.Lock()
        self.__create_tables()
        logger.info(f"[{self.class_name}] Started database", db_config)

    def __del__(self):
        self.__wconn.close()
        self.__rconn.close()

    def __write(self, query: str, *args):
        logger.debug(f"[{self.class_name}] Excute write query", query, *args)
        with self.__wlock:
            cursor = self.__wconn.cursor()
            cursor.execute(query, [*args])
            self.__wconn.commit()
            return cursor

    def __read(self, query: str, *args):
        logger.debug(f"[{self.class_name}] Excute read query", query, *args)
        cursor = self.__rconn.cursor()
        cursor.execute(query, [*args])
        return cursor

    def __create_tables(self):
        logger.debug(f"[{self.class_name}] Create tables")
        queries = [
            """CREATE TABLE IF NOT EXISTS flowers_img(pid INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT)
            """,
            """CREATE VIRTUAL TABLE IF NOT EXISTS flowers_vector USING fts5(pid, tokens, score)
            """,
            """ CREATE TABLE IF NOT EXISTS config (
                key  TEXT NOT NULL PRIMARY KEY,
                data TEXT DEFAULT '{}'
            ) WITHOUT ROWID;
            """,
            """ INSERT OR IGNORE INTO config(key, data) VALUES ('base', '{}')
            """
        ]
        for query in queries:
            safe_execute(None, self.__write, query)

    ### IMAGE HANDLER ####
    def save_img(self, filename, predicts):
        err_msg = ""
        cursor  = None
        try:
            cursor = self.__write("INSERT INTO flowers_img(filename) VALUES (?)", filename)
            for predict in predicts:
                if predict["score"] < self.__predict_threshold:
                    continue
                self.__write("INSERT INTO flowers_vector(pid, tokens, score) VALUES (?, ?, ?)", cursor.lastrowid, process_img_label(predict["label"]), predict["score"])
        except Exception as e:
            err_msg = f"Failed to save. Error occur: {str(e)}"
        except:
            err_msg = "Failed to save. Unknow Error"
        if err_msg != "":
            logger.error(f"[{self.class_name}] Err: {err_msg}")
            return err_msg
        return cursor.lastrowid

    def delete_img(self, pid):
        err_msg = ""
        try:
            # Ignore no row deleted in table flowers_vector. Must delete this table first
            self.__write("DELETE FROM flowers_vector WHERE pid = ?", pid)
            # Delete and check it
            if self.__write("DELETE FROM flowers_img WHERE pid = ?", pid).rowcount < 1:
                raise Exception("item not found")
        except Exception as e:
            err_msg = f"Failed to delete. Error: {str(e)}"
        except:
            err_msg = "Failed to delete. Unknow Error"
        if err_msg != "":
            logger.error(err_msg)
            return err_msg
        return True

    def query_img_by_id(self, id: int):
        query = "SELECT * FROM flowers_img WHERE pid = ?"
        return self.__read(query, id).fetchall()

    def query_img(self, tokens: str, first: int, size: int):
        base_query  = "SELECT fv.pid %s FROM flowers_vector fv JOIN flowers_img fi ON fv.pid = fi.pid WHERE tokens MATCH ? GROUP BY fv.pid"

        count_query = f"SELECT COUNT(1) FROM ({ base_query % "" })"
        sel_query   = f"{ base_query % ", GROUP_CONCAT(tokens, ', '), fi.filename " } ORDER BY tokens LIKE ? DESC LIMIT { size if size is not None else 10 }"
        # sel_query   = f"{base_query} ORDER BY score DESC, rank DESC LIMIT { size if size is not None else 10 }"

        if first is not None:
            sel_query += f" OFFSET {first}"

        data    = None
        count   = None
        err_msg = ""
        try:
            q_tokens = process_sel_tokens(tokens)
            cursor   = self.__read(count_query, q_tokens)
            count    = cursor.fetchall()[0][0]

            cursor   = self.__read(sel_query, q_tokens, q_tokens)
            data     = cursor.fetchall()
        except Exception as e:
            err_msg = f"Failed to select. Error: {str(e)}"
        except:
            err_msg = "Failed to select. Unknow Error"

        if err_msg != "":
            logger.error(err_msg)
            return err_msg

        out_data = []
        for it in data:
            out_it = {
                "id":       it[0],
                "label":    it[1],
                "path":     it[2],
            }
            out_data.append(out_it)

        return count, out_data

    ### END OF [IMAGE HANDLER] ####

    ### BASE CONFIG ####
    def save_conf(self, data):
        query = "UPDATE config SET data = ? WHERE key = ?"
        return safe_execute(None, self.__write, query, data, 'base')

    def query_conf(self):
        query = "SELECT data FROM config where key = ?"
        cursor = self.__rconn.cursor()
        cursor.execute(query, ['base'])
        _rows = cursor.fetchall()

        if len(_rows) == 0:
            return '{}'
        return _rows[0][0]
    ### END OF [BASE CONFIG] ####
