#coding:utf-8
#author:wanghan

import logging
import logging.config
from APITest.common.globeObj import *

#
# class LoggingObj():
#     logger = None
#     def __init__(self, filepath="/config/logging.cfg"):
#         logging.config.fileConfig(filepath)
#
#     def getLogger(self, name):
#         try:
#             self.logger = logging.getLogger(name)
#         except Exception as e:
#             print("生成日志器失败！：" + str(e))


logging.config.fileConfig(BASE_DIR+"/config/logging.cfg")

logger=logging.getLogger('test')


def debug(message):

    logging.debug(message)

def warning(message):

    logging.warning(message)

def info(message):

    logging.info(message)