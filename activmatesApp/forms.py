
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from activmatesApp.models import User


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
#this function is not working 
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That username is taken, please choose a different one')
 
    


class EditProfileForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(), 
                             Length(min=2, max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), 
                            Length(min=2, max=20)])
    address_line1 = StringField('Address - street and house number',
                                validators=[DataRequired(),
                                Length(min=2, max=20)])
    postcode = IntegerField('Postcode',
                            validators=[DataRequired(),
                            ])
    city = StringField('City',
                       validators=[DataRequired()])
    phone_number = IntegerField('Phone Number',
                               validators=[DataRequired(), ])
    twitter = StringField('Address - street and house number',
                                validators=[DataRequired(),
                                Length(min=2, max=20)])
    facebook = StringField('Address - street and house number',
                                validators=[DataRequired(),
                                Length(min=2, max=20)])
    submit = SubmitField('Save')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose a different one')
#this function is not working 
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That username is taken, please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), 
                        Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
