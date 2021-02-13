from flask import render_template, url_for, flash, redirect, request
from activmatesApp import app, db, bcrypt
from activmatesApp.forms import RegistrationForm, EditProfileForm, LoginForm, UpdateAccountForm
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
@login_required
def edit_profile():
    editProfileForm = EditProfileForm()
    if editProfileForm.validate_on_submit():
        profile = Profile(  first_name=editProfileForm.first_name.data, 
                            last_name=editProfileForm.last_name.data, 
                            street_address=editProfileForm.street_address.data,
                            city=editProfileForm.city.data,
                            postcode=editProfileForm.postcode.data,
                            phone_number=editProfileForm.phone_number.data,
                            twitter=editProfileForm.twitter.data,
                            facebook=editProfileForm.facebook.data, user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
        flash(
            f'Profile created!', 'success')
        return redirect(url_for('edit_profile')) #- can i render a button here?
    # GET: Serve Sign-up page
    image_file = url_for('static', filename='images/profile-pics/' + current_user.image_file)
    return render_template('edit-profile.html', editProfileForm=editProfileForm, image_file=image_file)

@app.route('/update-account', methods=['GET', 'POST'])
@login_required
def update_account():
    updateAccountForm = UpdateAccountForm()
    if updateAccountForm.validate_on_submit():
        current_user.username = updateAccountForm.username.data
        current_user.email = updateAccountForm.email.data
        db.session.commit()
        flash(
            f'account updated!', 'success')
        return redirect(url_for('update_account')) #- can i render a button here? on no redirect at all?
    elif request.method == 'GET': # populates form field with current data
        updateAccountForm.username.data = current_user.username
        updateAccountForm.email.data = current_user.email
    #remove image? i think this should only be in profile
    image_file = url_for('static', filename='images/profile-pics/' + current_user.image_file)
    return render_template('update-account.html', updateAccountForm=updateAccountForm, image_file=image_file)

@app.route('/main-search')
@login_required
def main_search():
    return render_template('main-search.html', title='Search', activities=activities)


@app.route('/new-activity')
@login_required
def new_activity():
    return render_template('new-activity.html', title='New Activity')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile')


@app.route('/view-activity')
@login_required
def view_activity():
    return render_template('view-activity.html', title='View Activity')
