import os
import sys
import logging

FORMAT = '%(asctime)s|%(levelname)s|%(filename)s|  %(message)s'
LOG_FILE = f"/tmp/container_logs/{os.environ.get('CI_PROJECT_NAME')}.log"
LEVEL = logging.INFO

if bool(int(os.environ.get('DEBUG', 0))):
    LEVEL = logging.DEBUG

def _get_file_handler():
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(FORMAT))
    return file_handler

def _get_stream_handler():
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(FORMAT))
    return stream_handler

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LEVEL)
    # logger.addHandler(_get_file_handler())
    logger.addHandler(_get_stream_handler())
    return logger