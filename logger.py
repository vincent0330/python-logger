# -*- coding: utf-8 -*-
"""
  logger
  使用说明：此日志是对logging的封装，目前支持：
  1、写日志到Console和File:
      logger = make_8lab_console_file_logger()
  2、写日志到Console和带时间切割策略的File:
      logger = make_8lab_console_time_logger()
  3、写日志到django框架中配置的日志中（这个要看在django中是如何配置的）:
      logger = make_8lab_django_logger() #default
"""

import logging
import sys


SERVER_ERROR_MSG = '500 Internal Server Error'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FORMAT = '%(asctime)s [%(levelname)s] [%(module)s:%(funcName)s] [%(lineno)d] - %(message)s'
LOG_FILENAME = "/var/log/8lab/8lab_audit_dam_server.log"
LOG_LEVEL = logging.DEBUG
FORMATTER = logging.Formatter(LOG_FORMAT, DATE_FORMAT)


def make_8lab_console_file_logger():
    """
    定义日志对象,实现同时写入Console和文件"/var/log/8lab/app.log"
    :return: logger
    """
    common_logger = logging.getLogger("8lab")
    common_logger.setLevel(LOG_LEVEL)
    common_logger.addHandler(__console_handler())
    common_logger.addHandler(__file_handler())
    return common_logger


def make_8lab_console_time_logger():
    """
    定义日志对象,实现同时写入Console和文件"/var/log/8lab/app.log",并且可以切割
    :return:  logger
    """
    common_logger = logging.getLogger("8lab")
    common_logger.setLevel(LOG_LEVEL)
    common_logger.addHandler(__console_handler())
    common_logger.addHandler(__time_handler())
    return common_logger


def make_8lab_django_logger():
    """
    使用django框架的logger,配置一般在settings.py中
    :return: logger
    """
    return logging.getLogger("app_fuzhou")


def __console_handler():
    """
    写日志到Console
    :return: console_handler
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def __file_handler():
    """
    写日志到文件
    :return: __file_handler
    """
    file_handler = logging.FileHandler(LOG_FILENAME)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def __time_handler():
    """
    切割日志
    :return: __time_handler
    """
    time_handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, 'MIDNIGHT', 1, 0)
    time_handler.setFormatter(FORMATTER)
    # 切割后的日志设置后缀
    time_handler.suffix = '%Y%m%d'
    return time_handler

logger = make_8lab_console_time_logger()
