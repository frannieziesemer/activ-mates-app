from flask import render_template, url_for, flash, redirect, request
from activmatesApp import app, db, bcrypt
from activmatesApp.forms import RegistrationForm, CreateProfileForm, LoginForm
from activmatesApp.models import User, Profile, Activity, ActivityType
from flask_login import login_user, current_user, logout_user, login_required

# this would be called from the database
activities = [
    {
        'author': 'Frannie Ziesemer',
        'type': 'Running',
        'description': '....',
        'date_posted': 'February 1, 2021'
    },
    {
        'author': 'Jonas Bischof',
        'type': 'Tennis',
        'description': '....',
        'date_posted': 'February 1, 2021'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/landing-page')
def landing_page():
    return render_template('landing-page.html')

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    registrationForm = RegistrationForm()
    if registrationForm.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registrationForm.password.data).decode('utf-8')
        user = User(username=registrationForm.username.data, email=registrationForm.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # alert message
        flash(
            f'Account created for {registrationForm.username.data} you are now able to login!', 'success')
        return redirect(url_for('login'))
    return render_template('sign-up.html',
                            title='Sign Up',
                            registrationForm=registrationForm
                           )
                           
@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    error = None
    if loginForm.validate_on_submit():
        user = User.query.filter_by(email=loginForm.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginForm.password.data):
            login_user(user, remember=loginForm.remember.data)
            next_page = request.args.get('next')
            flash(f'You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main_search'))
        else: 
            error = 'Login Unsuccessful. Please check username and password'
    return render_template('login.html', 
                            title='Login',
                            loginForm=loginForm, 
                            error=error
                            )

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))
    
@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    """User sign up page"""
    editProfileForm = editProfileForm()
    image_file = url_for('static', filename='images/profilepics/' + current_user.image_file)
    #POST: sign user in 
    if createProfileForm.validate_on_submit():
        flash(
            f'Profile created!', 'success')
        return redirect(url_for('main_search'))
    # GET: Serve Sign-up page
    return render_template('edit-profile.html', editProfileForm=editProfileForm, image_file=image_file)
    
@app.route('/main-search')
def main_search():
    return render_template('main-search.html', title='Search', activities=activities)


@app.route('/new-activity')
def new_activity():
    return render_template('new-activity.html', title='New Activity')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile')


@app.route('/view-activity')
def view_activity():
    return render_template('view-activity.html', title='View Activity')
