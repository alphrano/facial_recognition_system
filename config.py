from dotenv import load_dotenv
import os
import logging

load_dotenv()  # Load environment variables

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("DB_PASSWORD", ""),  # Load from .env
    "database": "facial_recognition"
}

COOKOUT_DB = {
    "host": "localhost",
    "user": "root",
    "password": os.getenv("DB_PASSWORD", ""),
    "database": "cookout_db"
}

# SQLAlchemy Database URI (for Flask apps)
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"

COOKOUT_DATABASE_URI = f"mysql+pymysql://{COOKOUT_DB['user']}:{COOKOUT_DB['password']}@{COOKOUT_DB['host']}/{COOKOUT_DB['database']}"

# Flask Configuration
SECRET_KEY = os.getenv("SECRET_KEY")

# Email Configuration (securely loaded from .env)
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ADMIN_EMAIL = "admin@cookout.com"

# Logging Configuration
LOG_FILE_PATH = "app.log"
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Facial Recognition Settings
DETECTOR_BACKEND = "opencv"  # Options: "opencv", "ssd", "mtcnn", "retinaface"
ENFORCE_DETECTION = False
