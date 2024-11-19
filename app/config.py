"""
This module loads environment variables for configuring the QR code API.

It includes settings for directories, colors, server URLs, and authentication.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

QR_DIRECTORY = Path(os.getenv('QR_CODE_DIR', './qr_codes'))

FILL_COLOR = os.getenv('FILL_COLOR', 'red')

BACK_COLOR = os.getenv('BACK_COLOR', 'white')

SERVER_BASE_URL = os.getenv('SERVER_BASE_URL', 'http://localhost:80')

SERVER_DOWNLOAD_FOLDER = os.getenv('SERVER_DOWNLOAD_FOLDER', 'downloads')

SECRET_KEY = os.getenv("SECRET_KEY", "secret-getenvkey")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'secret')
