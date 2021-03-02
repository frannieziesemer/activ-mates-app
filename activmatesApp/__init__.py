import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.sql import select, func
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('activmatesApp.default_settings')
app.config.from_envvar('YOURAPPLICATIONSETTNGS')
app.config['SQLALCHEMY_ECHO'] = False


db = SQLAlchemy(app)


@event.listens_for(db.engine, "connect")
def load_spatialite(dbapi_conn, connection_record):
  # From https://geoalchemy-2.readthedocs.io/en/latest/spatialite_tutorial.html
  dbapi_conn.enable_load_extension(True)
  dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')
  dbapi_conn.execute('SELECT InitSpatialMetaData()')


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'info'


from activmatesApp import routes
