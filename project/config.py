import os

class BaseConfig:
    "This class is for base configuration"

    APP_KEY = os.getenv('DROPBOX_APP_KEY', 'your app key')
    APP_SECRET = os.getenv('DROPBOX_APP_SECRET', 'your app secret')
    REDIRECT_URI = os.getenv('DROPBOX_REDIRECT_URI', 'http://localhost:5000/auth/callback')
    SECRET_KEY = os.getenv('SECRET_KEY', 'secretkey')


class DevelopmentConfig(BaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY", "secretkey")

class ProductionConfig(BaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY", "secretkey")

class TestConfig(BaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY", "secretkey")


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestConfig,
}