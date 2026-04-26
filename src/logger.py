import logging
import os
from datetime import datetime


def get_logger(name: str) -> logging.Logger:
    """Return a logger that writes to logs/YYYY-MM-DD.log and to the console."""
    os.makedirs("logs", exist_ok=True)
    log_file = os.path.join("logs", f"{datetime.now().strftime('%Y-%m-%d')}.log")

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    return logger
