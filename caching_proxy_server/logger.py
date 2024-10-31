import logging

class LogColor:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'


class ColorFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: f"{LogColor.BLUE}DEBUG {LogColor.ENDC}- %(message)s",
        logging.INFO: f"{LogColor.GREEN}INFO {LogColor.ENDC}- %(message)s",
        logging.WARNING: f"{LogColor.YELLOW}WARNING {LogColor.ENDC}- %(message)s",
        logging.ERROR: f"{LogColor.RED}ERROR {LogColor.ENDC}- %(message)s",
        logging.CRITICAL: f"{LogColor.RED}{LogColor.HEADER}CRITICAL {LogColor.ENDC}- %(message)s",
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, "%(message)s")
        formatter = logging.Formatter("%(asctime)s - %(name)s" + log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

def setup_logging():
    logger = logging.getLogger('ProxyServer')
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter())

    logger.addHandler(console_handler)

    return logger
