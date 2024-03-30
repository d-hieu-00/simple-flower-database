import time
import random
import string
import os
import re
import json

""" Logger Functions """
if os.name == 'nt': os.system('color')
class mLogger:
    __COLORS = ["\033[1;97m", "\033[1;92m", "\033[1;93m", "\033[1;91m"]
    __DEBUG = 0; __INFO = 1; __WARNING = 2; __ERROR = 3
    __LOG_LEVEL = __INFO
    __LOG_FILE  = None

    def __del__(self):
        self.debug("Deinit logger, file = %s" % self.log_path)
        if self.__LOG_FILE is not None:
            self.__LOG_FILE.flush()
            self.__LOG_FILE.close()
            self.__LOG_FILE = None

    def __log(self, level, message, *args, **kwargs):
        if level < self.__LOG_LEVEL or level > self.__ERROR: return

        level_s = "[DEBUG  ]"
        if   level == self.__INFO    : level_s = "[INFO   ]"
        elif level == self.__WARNING : level_s = "[WARNING]"
        elif level == self.__ERROR   : level_s = "[ERROR  ]"

        out_message = "%s %s %s" % (time.strftime("%X %x"), level_s, message)
        if args.__len__() != 0:             out_message = "%s, %s" % (out_message, ", ".join("'%s'" % str(arg) for arg in list(args)))
        if kwargs.items().__len__() != 0:   out_message = "%s, %s" % (out_message, kwargs)

        print("%s%s\033[0m" % (self.__COLORS[level], out_message))
        if self.__LOG_FILE is not None:
            self.__LOG_FILE.write("%s\n" % out_message)
            self.__LOG_FILE.flush()

    @property
    def DEBUG(self):    return self.__DEBUG
    @property
    def INFO(self):     return self.__INFO
    @property
    def WARNING(self):  return self.__WARNING
    @property
    def ERROR(self):    return self.__ERROR
    @property
    def log_path(self): return None if self.__LOG_FILE is None else os.path.realpath(self.__LOG_FILE.name)

    def set_level(self, level): self.__LOG_LEVEL = level
    def set_file(self, path):
        self.__LOG_FILE = open(path, 'a')
        self.__LOG_FILE.flush()

    def info(self, message, *args, **kwargs):  self.__log(self.__INFO, message, *args, **kwargs)
    def warn(self, message, *args, **kwargs):  self.__log(self.__WARNING, message, *args, **kwargs)
    def error(self, message, *args, **kwargs): self.__log(self.__ERROR, message, *args, **kwargs)
    def debug(self, message, *args, **kwargs): self.__log(self.__DEBUG, message, *args, **kwargs)
logger = mLogger()

""" Random functions """
def generate_str(len):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(len))

""" Safe execute """
def safe_execute(default, function, *args, **kwargs):
    try:
        return function(*args, **kwargs)
    except Exception as e:
        logger.error("[%s] error occur: '%s'" % (function.__name__, str(e)))
    except:
        logger.error("[%s] unknown error occur" % (function.__name__))
    return default

def is_json(in_text: str):
    try:
        json.loads(in_text)
        return True
    except:
        return False

def save_to_file(in_data, filename):
    with open(filename, 'wb') as f:
        f.write(in_data)

def make_dir_if_not_exists(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)