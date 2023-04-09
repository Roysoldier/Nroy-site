import logging
from logging.handlers import RotatingFileHandler
import sys

class MyLogger:
    def __init__(self,path="./logs/messages.log",console=False):
        self.logger = None

        if console:
            self.logger = logging.getLogger('mylogger')
            self.logger.setLevel(logging.DEBUG)
            sh = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
            sh.setFormatter(formatter)
            self.logger.addHandler(sh)
        else:
            self.logger = logging.getLogger('mylogger')
            self.logger.setLevel(logging.DEBUG)
            fh = RotatingFileHandler(path, maxBytes=10000000, backupCount=10, encoding='utf-8')
            formatter = logging.Formatter('%(asctime)s %(levelname)-8s > %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
            
    def log(self,message="",severity="DEBUG"):
        match severity:
            case "DEBUG":
                self.logger.debug(message)
            case "INFO":
                self.logger.info(message)
            case "WARN":
                self.logger.warn(message)
            case "ERROR":
                self.logger.error(message)
            case "CRITICAL":
                self.logger.critical(message)
            case _:
                self.logger.debug(message)
