import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base config — shared across all environments"""

    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-change-this")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-change-this")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_DATASET_ROWS = 1000  # Our upload limit



class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DEV_DATABASE_URL",
        "mysql+pymysql://root:password@localhost/mlab_dev"
    )

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # In-memory DB for tests

# This dict lets you select config by name string
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}