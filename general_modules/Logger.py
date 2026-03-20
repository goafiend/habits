import logging
import os
from logging.handlers import RotatingFileHandler

class LogColors:
    RESET = "\033[0m"
    DEBUG = "\033[90m"      # bright black / gray
    INFO = "\033[92m"       # green
    WARNING = "\033[93m"    # yellow
    ERROR = "\033[91m"      # red
    CRITICAL = "\033[95m"   # magenta

class ColorFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: LogColors.DEBUG,
        logging.INFO: LogColors.INFO,
        logging.WARNING: LogColors.WARNING,
        logging.ERROR: LogColors.ERROR,
        logging.CRITICAL: LogColors.CRITICAL,
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self.LEVEL_COLORS.get(record.levelno, LogColors.RESET)
        message = super().format(record)
        return f"{color}{message}{LogColors.RESET}"


def create_logger(name, subfolder=None):
    # Create a named logger
    logger = logging.getLogger(f"{name}")
    # Prevent duplicate handlers if module reloads / multiple imports
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # 1) Console handler (default: INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(
        ColorFormatter("%(levelname)s %(name)s [%(funcName)s:%(lineno)d] %(message)s")
    )
    logger.addHandler(ch)
    # 2) File handler (DEBUG, rotating)
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    if subfolder is not None:
        if type(subfolder) == str:
            log_dir = os.path.join(log_dir, subfolder)
    os.makedirs(log_dir, exist_ok=True)
    filepath = os.path.join(log_dir, f"{name}.log")
    if os.path.exists(filepath):
        os.remove(filepath)
    fh = RotatingFileHandler(
        os.path.join(log_dir, f"{name}.log"),
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
        mode = "w",
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s [%(funcName)s:%(lineno)d] %(message)s"
    ))
    logger.addHandler(fh)

    logger.propagate = False
    return logger
