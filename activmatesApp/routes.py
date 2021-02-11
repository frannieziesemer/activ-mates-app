from flask import render_template, url_for, flash, redirect
from activmatesApp import app, db, bcrypt
from activmatesApp.forms import RegistrationForm, CreateProfileForm, LoginForm
from activmatesApp.models import User, Profile, Activity, ActivityType

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    error = None
    if loginForm.validate_on_submit():
        if loginForm.email.data == 'admin@blog.com' and loginForm.password.data == 'password':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('main_search'))
        else: 
            error = 'Login Unsuccessful. Please check username and password'
    return render_template('login.html', 
                            title='Login',
                            loginForm=loginForm, 
                            error=error
                            )

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    registrationForm = RegistrationForm()
    if registrationForm.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registrationForm.password.data).decode('utf-8')
        user = User(username=registrationForm.username.data, email=registrationForm.password.data, password=hashed_password)
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
    
@app.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    """User sign up page"""
    createProfileForm = CreateProfileForm()
    #POST: sign user in 
    if createProfileForm.validate_on_submit():
        flash(
            f'Profile created!', 'success')
        return redirect(url_for('main_search'))
    # GET: Serve Sign-up page
    return render_template('create-profile.html', createProfileForm=createProfileForm)
    
@app.route('/main-search')
def main_search():
    return render_template('main-search.html', title='Search', activities=activities)


@app.route('/new-activity')
def new_activity():
    return render_template('new-activity.html', title='New Activity')


@app.route('/profile')
def profile():
    return render_template('profile.html', title='Profile')


@app.route('/view-activity')
def view_activity():
    return render_template('view-activity.html', title='View Activity')
