import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
root_folder = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(root_folder, 'logs.log')
file_handler = logging.FileHandler(file, "w")


def get_logger(log_module=True):
    if log_module:
        formatter = logging.Formatter('[%(asctime)s]: %(levelname)s: %(module)s: %(message)s', '%Y-%m-%d %H:%M:%S')
    else:
        formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
