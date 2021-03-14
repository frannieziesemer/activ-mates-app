from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
)
from flask_login import login_user, current_user, logout_user, login_required
from activmatesApp import bcrypt, db
from activmatesApp.models import Activity, Profile, User
from activmatesApp.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RequestPasswordResetForm,
    ResetPasswordForm,
)
from activmatesApp.users.utils import save_picture, send_reset_email


# instance of blueprint
users = Blueprint("users", __name__)

# add routes specific for users


@users.route("/signup", methods=["GET", "POST"])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        # alert message
        flash(
            f"Account created for {form.username.data} you are now able to login!",
            "success",
        )
        return redirect(url_for("users.login"))
    return render_template("sign-up.html", title="Sign Up", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash(f"You have been logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            error = "Login Unsuccessful. Please check username and password"
    return render_template("login.html", title="Login", form=form, error=error)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/update-account", methods=["GET", "POST"])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f"account updated!", "success")
        return redirect(
            url_for("profiles.account_profile")
        )  # - can i render a button here? on no redirect at all?
    elif request.method == "GET":  # populates form field with current data
        form.username.data = current_user.username
        form.email.data = current_user.email
    # remove image? i think this should only be in profile
    image_file = url_for(
        "static", filename="images/profile-pics/" + current_user.image_file
    )
    return render_template("update-account.html", form=form, image_file=image_file)


@users.route("/user/<string:username>")
@login_required
def user_activities(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    profile = Profile.query.filter_by(user=user).first_or_404()
    activities = (
        Activity.query.filter_by(profile=profile)
        .order_by(Activity.date_posted.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template(
        "user-activities.html",
        title="Search",
        user=user,
        profiles=profile,
        activities=activities,
        map_key=current_app.config["GOOGLE_MAPS_API_KEY"],
    )


@users.route("/reset-password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("email has been sent with instructions to reset your password", "info")
        return redirect(url_for("users.login"))
    return render_template(
        "reset-password-request.html", title="Reset Password", form=form
    )


@users.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        # alert message
        flash(f"Password changed, you are now able to login!", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
