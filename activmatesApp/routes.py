import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from activmatesApp import app, db, bcrypt
from activmatesApp.forms import RegistrationForm, ProfileForm, LoginForm, UpdateAccountForm
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




@app.route('/account-profile')
@login_required
def account_profile():
    current_user_id = current_user.id
    profile_data = Profile.query.filter_by(user_id=current_user_id).all()
    for item in profile_data:
        profile_image = item.image_file
    image_file = url_for('static', filename='images/profile-pics/' + profile_image)
    return render_template('account-profile.html',
                            title='Account and Profile',
                            image_file=image_file,
                            current_user_id=current_user_id,
                            profile_data=profile_data
                            )

def save_picture(form_picture):
        random_hex = secrets.token_hex(8) #- creates secret hex to save file
        _, f_ext = os.path.splitext(form_picture.filename)   # - returns  file extension
        picture_filename = random_hex + f_ext    #- changes filename to a hex
        picture_path = os.path.join(app.root_path, 'static/images/profile-pics', picture_filename) #- creates path to where we want to save the file
        
        #resize image
        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
        
        return picture_filename


@app.route('/create-profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    profileForm = ProfileForm()
    address_data = profileForm.street_address.data
    image_file = url_for('static', filename='images/profile-pics/' + current_user.image_file)
    if profileForm.validate_on_submit():
        profile = Profile(first_name=profileForm.first_name.data,
                        last_name=profileForm.last_name.data,
                        street_address=profileForm.street_address.data,
                        phone_number=profileForm.phone_number.data,
                        twitter=profileForm.twitter.data,
                        facebook=profileForm.facebook.data,
                        lat=profileForm.lat.data,
                        lng=profileForm.lng.data,
                        user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
        flash(f'Profile created!', 'success')
        return redirect(url_for('account_profile'))
    return render_template('create-profile.html',
                            profileForm=profileForm,
                            map_key=app.config['GOOGLE_MAPS_API_KEY'],
                            address_data=address_data
                            )


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    profileForm = ProfileForm()
    current_user_id = current_user.id
    profile_data = Profile.query.filter_by(user_id=current_user_id).all()
    #update database info
    if profileForm.validate_on_submit():
        if profileForm.picture.data:
            picture_file = save_picture(profileForm.picture.data)
            for item in profile_data:
                item.image_file=picture_file
        for item in profile_data:
            item.first_name = profileForm.first_name.data
            item.last_name=profileForm.last_name.data
            item.phone_number=profileForm.phone_number.data
            item.twitter=profileForm.twitter.data
            item.facebook=profileForm.facebook.data
            item.street_address=profileForm.street_address.data
            item.lat=profileForm.lat.data
            item.lng=profileForm.lng.data
        db.session.commit()
        flash(
            f'profile updated!', 'success')
        return redirect(url_for('account_profile'))
    # display info inside form
    elif request.method == 'GET':
        for item in profile_data:
            profileForm.first_name.data = item.first_name
            profileForm.first_name.data = item.first_name
            profileForm.last_name.data =  item.last_name
            profileForm.phone_number.data = item.phone_number
            profileForm.twitter.data = item.twitter
            profileForm.facebook.data = item.facebook
            profileForm.street_address.data = item.street_address
            profile_picture = item.image_file
    image_file = url_for('static', filename='images/profile-pics/' + profile_picture)
    return render_template('edit-profile.html',
                            profileForm=profileForm,
                            image_file=image_file,
                            title='Update profile',
                            map_key=app.config['GOOGLE_MAPS_API_KEY']
                            )


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
        return redirect(url_for('account_profile')) #- can i render a button here? on no redirect at all?
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


@app.route('/view-activity')
@login_required
def view_activity():
    return render_template('view-activity.html', title='View Activity')
