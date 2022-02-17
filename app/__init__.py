from dotenv import load_dotenv
from flask import Flask

from .database import db

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)

    register_extenstions(app)
    register_blueprint(app)

    return app


def register_extenstions(app):
    db.init_app(app)


def register_blueprint(app):
    from .auth.views import auth
    from .error.views import error
    from .user.views import user_module
    from .admin.views import admin

    app.register_blueprint(auth)
    app.register_blueprint(error)
    app.register_blueprint(user_module)
    app.register_blueprint(admin)
