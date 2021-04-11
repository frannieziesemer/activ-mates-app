import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from activmatesApp import db
from activmatesApp.profiles.forms import ProfileForm
from activmatesApp.models import Profile
from activmatesApp.profiles.utils import save_picture
from flask_login import current_user, login_required


# instance of blueprint
profiles = Blueprint("profiles", __name__)


@profiles.route("/account-profile")
@login_required
def account_profile():
    profile_data = current_user.profile
    if profile_data:
        for item in profile_data:
            profile_image = item.image_file
    else:
        profile_image = "default.jpg"
    image_file = url_for("static", filename="images/profile-pics/" + profile_image)
    return render_template(
        "account-profile.html",
        title="Account and Profile",
        image_file=image_file,
        profile_data=profile_data,
    )


@profiles.route("/create-profile", methods=["GET", "POST"])
@login_required
def create_profile():
    form = ProfileForm()
    image_file = url_for(
        "static", filename="images/profile-pics/" + current_user.image_file
    )
    if form.validate_on_submit():
        profile = Profile(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone_number=form.phone_number.data,
            twitter=form.twitter.data,
            facebook=form.facebook.data,
            user=current_user,
        )
        db.session.add(profile)
        db.session.commit()
        flash(f"Profile created!", "success")
        return redirect(url_for("profiles.account_profile"))
    return render_template(
        "create-profile.html",
        form=form,
        legend="Create a Profile"
    )


@profiles.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = ProfileForm()
    profile_data = current_user.profile
    for item in profile_data:
        display_profile_picture = item.image_file
    # update database info
    if form.validate_on_submit():
        # check if new picture
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            for item in profile_data:
                item.image_file = picture_file
        for item in profile_data:
            item.first_name = form.first_name.data
            item.last_name = form.last_name.data
            item.phone_number = form.phone_number.data
            item.twitter = form.twitter.data
            item.facebook = form.facebook.data

        db.session.commit()
        flash(f"profile updated!", "success")
        return redirect(url_for("profiles.account_profile"))
    # display info inside form
    elif request.method == "GET":
        for item in profile_data:
            form.first_name.data = item.first_name
            form.first_name.data = item.first_name
            form.last_name.data = item.last_name
            form.phone_number.data = item.phone_number
            form.twitter.data = item.twitter
            form.facebook.data = item.facebook
    image_file = url_for(
        "static", filename="images/profile-pics/" + display_profile_picture
    )
    return render_template(
        "create-profile.html",
        form=form,
        image_file=image_file,
        title="Update profile",
        map_key=os.environ.get(""),
        legend="Update profile"
    )
