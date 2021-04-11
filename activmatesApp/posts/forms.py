from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, HiddenField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length


class CreateActivityForm(FlaskForm):
    title = StringField(u"Title", validators=[DataRequired()])
    lat = HiddenField("lat", )
    lng = HiddenField("lng", )
    address = HiddenField(
        "Address", validators=[DataRequired(), Length(min=2, max=200)]
    )
    activity_type = SelectField(
        u"Type of activity", choices=[], validators=[DataRequired()]
    )
    description = TextAreaField(
        u"Description",
        validators=[DataRequired()],
    )
    picture = FileField(
        "Add Picture", validators=[FileAllowed(["jpg", "png", "jpeg"])]
    )
    submit = SubmitField("Post")
