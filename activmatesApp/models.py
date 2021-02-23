import enum
from datetime import datetime
from activmatesApp import db, login_manager
from flask_login import UserMixin
#from geoalchemy2 import Geometry

@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))

class UserTypes(enum.Enum):
   Admin = 1
   Regular = 2

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.Enum(UserTypes), nullable=False, default=UserTypes.Regular)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    profile = db.relationship('Profile', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    phone_number = db.Column(db.Integer, nullable=False)
    twitter = db.Column(db.String(20), nullable=False)
    facebook = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity = db.relationship('Activity', backref='profile', lazy=True)

    def __repr__(self):
        return f"Profile('{self.user_id}', '{self.first_name}', '{self.last_name}', '{self.image_file}', '{self.phone_number}', '{self.twitter}', '{self.facebook}')"

#TODO create a form for Admin use to input new activities into the db activity_types table

class ActivityType(db.Model):
    __tablename__ = 'activity_types'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    activity = db.relationship('Activity', backref='activity_type', lazy=True)
    

    def __repr__(self):
        return f"activitytype('{self.number}', '{self.name}')"


class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    # image_file = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(150), nullable=False)
    lat = db.Column(db.Integer, nullable=False)
    lng = db.Column(db.Integer, nullable=False)
    #location = db.Column(Geometry('POINT'))
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity_types.id'), nullable=False)
    # activity_type = db.relationship('ActivityType', backref='activity', lazy=True)

    def __repr__(self):
        return f"Activity('{self.title}', '{self.date_posted}', '{self.location}', '{self.lat}', '{self.lng}', '{self.description}')"


