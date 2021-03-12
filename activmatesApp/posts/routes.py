from flask import abort, flash, redirect, render_template, request, url_for, Blueprint
from activmatesApp import app, db
from activmatesApp.posts.forms import CreateActivityForm
from activmatesApp.models import Activity, ActivityType
from flask_login import current_user, login_required

# instance of blueprint
posts = Blueprint("posts", __name__)


@posts.route("/activity/new", methods=["GET", "POST"])
@login_required
def new_activity():
    profile = current_user.profile
    for item in profile:
        profile_id = item.id
    form = CreateActivityForm()
    form.activity_type.choices = [
        (item.id, item.name) for item in ActivityType.query.all()
    ]
    if form.validate_on_submit():
        activity = Activity(
            title=form.title.data,
            description=form.description.data,
            address=form.address.data,
            location=Activity.point_representation(form.lat.data, form.lng.data),
            activity_type_id=form.activity_type.data,
            profile_id=profile_id,
        )
        db.session.add(activity)
        db.session.commit()
        flash(f"new activity posted!", "success")
        return redirect(url_for("main.home"))
    return render_template(
        "new-activity.html",
        title="New Activity",
        form=form,
        profile=profile,
        map_key=app.config["GOOGLE_MAPS_API_KEY"],
        legend="New Activity",
    )


@posts.route("/activity/<int:activity_id>")
@login_required
def view_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    return render_template(
        "view-activity.html", title=activity.title, activity=activity
    )


@posts.route("/activity/<int:activity_id>/update", methods=["GET", "POST"])
@login_required
def update_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    # checks that only the owner of post can update this
    if activity.profile.id != current_user.profile[0].id:
        abort(403)
    form = CreateActivityForm()
    if form.validate_on_submit():
        activity.title = form.title.data
        activity.description = form.description.data
        activity.street_address = form.street_address.data
        activity.location = (
            Activity.point_representation(form.lat.data, form.lng.data),
        )
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("posts.view_activity", activity_id=activity.id))
    elif request.method == "GET":
        form.title.data = activity.title
        form.description.data = activity.description
        form.street_address.data = activity.street_address
    return render_template(
        "new-activity.html",
        title="Update Activity",
        form=form,
        legend="Update Post",
        activity=activity,
    )


@posts.route("/activity/<int:activity_id>/delete", methods=["POST"])
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.profile.id != current_user.profile[0].id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.home"))
