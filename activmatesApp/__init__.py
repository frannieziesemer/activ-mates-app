import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('activmatesApp.default_settings')
app.config.from_envvar('YOURAPPLICATIONSETTNGS')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'info'
maps_api_key = os.environ.get('MAPS_API_KEY')


from activmatesApp import routes
