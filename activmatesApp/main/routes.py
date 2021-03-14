from flask import Blueprint, render_template, request, current_app
from activmatesApp.models import Activity, Profile
from flask_login import login_required


# instance of blueprint
main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
@login_required
def home():
    profiles = Profile.query.all()
    page = request.args.get("page", 1, type=int)
    activities = Activity.query.order_by(Activity.date_posted.desc()).paginate(
        page=page, per_page=5
    )
    return render_template(
        "home.html",
        title="Search",
        profiles=profiles,
        activities=activities,
        map_key=current_app.config["GOOGLE_MAPS_API_KEY"],
    )


@main.route("/home/list-activities")
@login_required
def home_list_view():
    profiles = Profile.query.all()
    page = request.args.get("page", 1, type=int)
    activities = Activity.query.order_by(Activity.date_posted.desc()).paginate(
        page=page, per_page=5
    )
    return render_template(
        "home-list-view.html",
        title="Search",
        profiles=profiles,
        activities=activities,
        map_key=current_app.config["GOOGLE_MAPS_API_KEY"],
    )
