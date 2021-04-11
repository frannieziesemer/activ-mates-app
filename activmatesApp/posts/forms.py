from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

# from activmatesApp.models import User, Profile
# from flask_login import current_user


class CreateActivityForm(FlaskForm):
    title = StringField(u"Title", validators=[DataRequired()])
    lat = HiddenField("lat", )
    lng = HiddenField("lng", )
    address = HiddenField(
        "address", validators=[DataRequired(), Length(min=2, max=200)]
    )
    activity_type = SelectField(
        u"Type of activity", choices=[], validators=[DataRequired()]
    )
    description = TextAreaField(
        u"Let us know what you do, your skill level, your availability",
        validators=[DataRequired()],
    )
    submit = SubmitField("Post")
