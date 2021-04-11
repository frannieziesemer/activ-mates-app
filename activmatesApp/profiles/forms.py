from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ProfileForm(FlaskForm):
    first_name = StringField(
        "First Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired(), Length(min=2, max=20)]
    )
    picture = FileField(
        "Add/ update Profile Picture", validators=[FileAllowed(["jpg", "png", "jpeg"])]
    )
    ## direct the info from google maps to the address field
    phone_number = IntegerField("Phone Number", validators=[DataRequired()])
    twitter = StringField("Twitter", validators=[DataRequired(), Length(min=2, max=20)])
    facebook = StringField(
        "Facebook", validators=[DataRequired(), Length(min=2, max=20)]
    )
    submit = SubmitField("Save")
