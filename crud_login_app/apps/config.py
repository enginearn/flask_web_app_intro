from pathlib import Path

basedir = Path(__file__).parent.parent # Python\flask\flask_web_app_intro\crud_login_app\apps

class BaseConfig:
    SECRET_KEY = 'dev'
    WTD_CSRF_SECRET_KEY = 'dev'

class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir}/db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir}/db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    WTD_CSRF_ENABLED = False

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{basedir}/db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    WTD_CSRF_ENABLED = True

config = {
    'local': LocalConfig,
    'test': TestConfig,
    'prod': ProductionConfig
}
