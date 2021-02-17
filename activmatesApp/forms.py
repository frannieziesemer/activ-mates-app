
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, HiddenField
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
    
class CreateProfileForm(FlaskForm):
    lat = HiddenField('lat')
    lng = HiddenField('lng')
    first_name = StringField('First Name',
                             validators=[DataRequired(), 
                             Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), 
                            Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) 

    # street_address = StringField('Address - street and house number',
    #                             validators=[DataRequired(),
    #                             Length(min=2, max=20)])
    phone_number = IntegerField('Phone Number',
                               validators=[DataRequired(), ])
    twitter = StringField('Address - street and house number',
                                validators=[DataRequired(),
                                Length(min=2, max=20)])
    facebook = StringField('Address - street and house number',
                                validators=[DataRequired(),
                                Length(min=2, max=20)])
    submit = SubmitField('Save')

class EditProfileForm(FlaskForm):
    lat = HiddenField('lat')
    lng = HiddenField('lng')
    first_name = StringField('First Name',
                             validators=[DataRequired(), 
                             Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), 
                            Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) 
    # street_address = StringField('Address - street and house number',
    #                             validators=[DataRequired(),
    #                             Length(min=2, max=20)])
    phone_number = IntegerField('Phone Number',
                               validators=[DataRequired(), ])
    twitter = StringField('Address - street and house number',
                                validators=[DataRequired(),
                                Length(min=2, max=20)])
    facebook = StringField('Address - street and house number',
                                validators=[DataRequired(),
                                Length(min=2, max=20)])
    submit = SubmitField('Update')

    # def validate_username(self, username):
    #         if username.data != current_user.username:
    #             user = User.query.filter_by(username=username.data).first()
    #             if user:
    #                 raise ValidationError('That username is taken, please choose a different one')
    # def validate_email(self, email):
    #     if email.data != current_user.email:
    #         user = User.query.filter_by(email=email.data).first()
    #         if user:
    #             raise ValidationError('That username is taken, please choose a different one')    


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), 
                        Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
