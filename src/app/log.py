import logging
import os

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, "app.log")

logging.root.handlers.clear()

logger = logging.getLogger("medigenie")

log_level = os.getenv("LOG_LEVEL", "ERROR").upper()
logger.setLevel(getattr(logging, log_level, logging.ERROR))

log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")

file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

