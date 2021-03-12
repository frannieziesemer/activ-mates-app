import secrets
import os
from PIL import Image
from flask import url_for
from activmatesApp import app, mail
from flask_mail import Message


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)  # - creates secret hex to save file
    _, f_ext = os.path.splitext(form_picture.filename)  # - returns  file extension
    picture_filename = random_hex + f_ext  # - changes filename to a hex
    picture_path = os.path.join(
        app.root_path, "static/images/profile-pics", picture_filename
    )  # - creates path to where we want to save the file

    # resize image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request",
        sender="noreply@activmates.com",
        recipients=[user.email],
    )
    msg.body = f"""To reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, then simply ignore this email and no changes will be made.
"""
    mail.send(msg)