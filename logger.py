import os
import logging

# Logging levels: DEBUG, INFO, WARNING, ERROR, CRITICAL


def get_logger(filename=None, on_console=False) -> object:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    if not filename:
        current_filename = os.path.basename(__file__)
        file_handler = logging.FileHandler(f'{current_filename}.log')
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    else:
        file_handler = logging.FileHandler(f'{filename}')
        formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # file_handler.setLevel(logging.ERROR)

    if on_console:  # Add new handler to print on console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
