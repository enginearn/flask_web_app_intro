from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config

from flask_login import LoginManager

db = SQLAlchemy() # type: SQLAlchemy
csrf = CSRFProtect() # type: CSRFProtect
login_manager = LoginManager() # type: LoginManager
login_manager.login_view = 'auth.signup' # type: str
login_manager.login_message = '' # type: str

def create_app(config_key) -> Flask:
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{Path(Path(__file__).parent)}/db.sqlite3',
        # SQLALCHEMY_DATABASE_URI='sqlite:////C:/Users/nagar/DevelopmentPython/flask/flask_web_app_intro/crud_login_app/apps/db.sqlite3',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRET_KEY='dev'
    )

    csrf.init_app(app)

    db.init_app(app)
    Migrate(app, db)

    login_manager.init_app(app)

    from apps.auth import views as auth_views

    app.register_blueprint(auth_views.auth, url_prefix='/auth')

    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix='/crud')

    return app
