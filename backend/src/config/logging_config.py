from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler


def set_logger(name, log_file):

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    Path(log_file).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(processName)s | %(levelname)s | %(name)s | %(message)s"
    )

    # File handler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
    )
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    return logger


# def setup_logger():

#     Path("logs").mkdir(exist_ok=True)

#     logging.basicConfig(
#         level=logging.INFO,
#         format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
#         handlers=[
#             logging.StreamHandler(),
#             logging.FileHandler("logs/enterprise_rag.log", encoding="utf-8")
#         ]
#     )

#     logging.getLogger("httpx").setLevel(logging.WARNING)
#     logging.getLogger("httpcore").setLevel(logging.WARNING)
#     logging.getLogger("urllib3").setLevel(logging.WARNING)