"""
MedBlock Configuration Settings

This module contains the configuration settings for the MedBlock application.
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Basic application configuration
APP_NAME = "MedBlock"
APP_VERSION = "0.1.0"
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "5000"))
API_URL_PREFIX = os.getenv("API_URL_PREFIX", "/api")

# Frontend Configuration
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = os.getenv("LOG_FILE", "medblock.log")

# Set up logging
numeric_level = getattr(logging, LOG_LEVEL.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError(f"Invalid log level: {LOG_LEVEL}")

logging.basicConfig(
    level=numeric_level,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# ML Model Configuration
MODELS_DIR = os.getenv("MODELS_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), "models"))
os.makedirs(MODELS_DIR, exist_ok=True)

# Blockchain Configuration
BLOCKCHAIN_PROVIDER = os.getenv("BLOCKCHAIN_PROVIDER", "http://localhost:8545")
BLOCKCHAIN_CONTRACT_ADDRESS = os.getenv("BLOCKCHAIN_CONTRACT_ADDRESS", None)
BLOCKCHAIN_KEY_FILE = os.getenv("BLOCKCHAIN_KEY_FILE", "encryption_key.key")

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-in-production")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-key-change-in-production")
JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600"))  # 1 hour by default

# Database Configuration
DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "medblock")
DB_USER = os.getenv("DB_USER", "medblock")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# SQLite specific configuration
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "medblock.db"))

# Get database URL based on configuration
if DB_TYPE == "sqlite":
    DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"
elif DB_TYPE == "postgresql":
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    raise ValueError(f"Unsupported database type: {DB_TYPE}")

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", FRONTEND_URL).split(",")

# File upload configuration
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads"))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "16777216"))  # 16MB by default 