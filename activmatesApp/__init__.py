from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.sql import select, func
from sqlalchemy.event import listen
from sqlalchemy.pool import Pool
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from activmatesApp.config import Config


db = SQLAlchemy()


# @event.listens_for(db.engine, "connect")
def load_spatialite(dbapi_conn, connection_record):
    # From https://geoalchemy-2.readthedocs.io/en/latest/spatialite_tutorial.html
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension("/usr/lib/x86_64-linux-gnu/mod_spatialite.so")
    dbapi_conn.execute("SELECT InitSpatialMetaData()")


bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message = "info"

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    listen(Pool, "connect", load_spatialite)

    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from activmatesApp.users.routes import users
    from activmatesApp.posts.routes import posts
    from activmatesApp.profiles.routes import profiles
    from activmatesApp.main.routes import main
    from activmatesApp.apis.routes import apis

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(profiles)
    app.register_blueprint(main)
    app.register_blueprint(apis)

    return app
