import logging
import os
from logging.handlers import RotatingFileHandler
from config import LOG_FILE_PATH

# Ensure logs directory exists
log_dir = os.path.dirname(LOG_FILE_PATH)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logger
logger = logging.getLogger("FacialRecognitionSystem")
logger.setLevel(logging.INFO)

# Rotating File Handler (5MB per file, keep 3 backups)
file_handler = RotatingFileHandler(
    filename=LOG_FILE_PATH,
    maxBytes=5*1024*1024,  # 5MB
    backupCount=3,
    encoding="utf-8"
)

# Console Handler (prints logs to terminal)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Custom Logging Functions
def log_auth_success(username: str):
    logger.info(f"AUTH_SUCCESS - User: {username}")

def log_auth_failure(reason: str):
    logger.warning(f"AUTH_FAILURE - Reason: {reason}")  # ✅ No facial data logged

def log_system_event(event: str):
    logger.info(f"SYSTEM_EVENT - {event}")

def log_error(error: str, context: str = None):
    message = f"ERROR - {error}"
    if context:
        message += f" | Context: {context}"
    logger.critical(message)  # ✅ Use CRITICAL for major errors
