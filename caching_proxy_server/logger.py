import logging
from logging.handlers import RotatingFileHandler

def setup_logging(fname: str, maxBytes: int = 4096, backupCount: int = 5):
    logger = logging.getLogger('ProxyServer')
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)


    file_handler = RotatingFileHandler(fname, maxBytes=maxBytes, backupCount=backupCount) 
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
