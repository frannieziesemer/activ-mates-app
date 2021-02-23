
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, HiddenField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from activmatesApp.models import User, Profile
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), 
                           Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), 
                        Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), 
                                     EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please choose a different one')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), 
                        Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), 
                           Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), 
                        Email()]) 
    submit = SubmitField('Save')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken, please choose a different one')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That username is taken, please choose a different one')
    
class ProfileForm(FlaskForm):
    
    first_name = StringField('First Name',
                             validators=[
                                 DataRequired(), 
                                 Length(min=2, max=20)
                                 ])
    last_name = StringField('Last Name',
                            validators=[
                                DataRequired(), 
                                Length(min=2, max=20)
                                ])
    picture = FileField('Update Profile Picture', 
                            validators=[
                                FileAllowed(['jpg', 'png', 'jpeg'])
                                ]) 
## direct the info from google maps to the address field
    
    phone_number = IntegerField('Phone Number',
                                    validators=[
                                        DataRequired()
                                        ])
    twitter = StringField('Twitter',
                                validators=[
                                    DataRequired(),
                                    Length(min=2, max=20)
                                    ])
    facebook = StringField('Facebook',
                                validators=[DataRequired(),
                                Length(min=2, max=20)])
    submit = SubmitField('Save')

class CreateActivityForm(FlaskForm):
    title = StringField(u'Title',
                            validators=[
                                DataRequired()
                            ])
    lat = HiddenField('lat', validators=[
                                DataRequired()
                                ])
    lng = HiddenField('lng', validators=[
                                DataRequired()
                                ])
    address = HiddenField('address',
                                validators=[
                                DataRequired(),
                                Length(min=2, max=200)
                                ])
    activity_type = SelectField(u'Type of activity', 
                                choices=[],
                                validators=[
                                    DataRequired()
                                    ])
    description = TextAreaField(u'Let us know what you do, your skill level, your availability',
                                    validators=[
                                        DataRequired()
                                        ])
    submit = SubmitField('Post')
