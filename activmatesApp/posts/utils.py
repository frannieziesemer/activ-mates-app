import secrets
import os
from PIL import Image
from flask import current_app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)  # - creates secret hex to save file
    _, f_ext = os.path.splitext(form_picture.filename)  # - returns  file extension
    picture_filename = random_hex + f_ext  # - changes filename to a hex
    picture_path = os.path.join(
        current_app.root_path, "static/images/activity-pics", picture_filename
    )  # - creates path to where we want to save the file

    # resize image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename
