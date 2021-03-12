import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.sql import select, func
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("activmatesApp.default_settings")
app.config.from_envvar("APPLICATIONSETTNGS")
app.config["SQLALCHEMY_ECHO"] = False


db = SQLAlchemy(app)


@event.listens_for(db.engine, "connect")
def load_spatialite(dbapi_conn, connection_record):
    # From https://geoalchemy-2.readthedocs.io/en/latest/spatialite_tutorial.html
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension("/usr/lib/x86_64-linux-gnu/mod_spatialite.so")
    dbapi_conn.execute("SELECT InitSpatialMetaData()")


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "users.login"
login_manager.login_message = "info"

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

email_user = app.config["EMAIL_USER"]
print(email_user)
email_password = app.config["EMAIL_PASSWORD"]
print(email_password)

app.config["MAIL_USERNAME"] = email_user
app.config["MAIL_PASSWORD"] = email_password
mail = Mail(app)


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
