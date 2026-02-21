import logging
import os
from config import APP_NAME

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "engine.log")

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)