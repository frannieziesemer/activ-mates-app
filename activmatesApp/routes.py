import secrets
import os
import sqlite3
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from sys import stderr
from activmatesApp import app, db, bcrypt
from activmatesApp.forms import RegistrationForm, ProfileForm, LoginForm, UpdateAccountForm, CreateActivityForm
from activmatesApp.models import User, Profile, Activity, ActivityType
from flask_login import login_user, current_user, logout_user, login_required

#creates a dictionary structure 
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/')
@app.route('/home')
@login_required
def home():
    profiles = Profile.query.all()
    activities = Activity.query.all();
    return render_template('home.html', 
                            title='Search', 
                            profiles=profiles, 
                            activities=activities,
                            map_key=app.config['GOOGLE_MAPS_API_KEY']
                            )

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # alert message
        flash(
            f'Account created for {form.username.data} you are now able to login!', 'success')
        return redirect(url_for('login'))
    return render_template('sign-up.html',
                            title='Sign Up',
                            form=form
                           )

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            error = 'Login Unsuccessful. Please check username and password'
    return render_template('login.html',
                            title='Login',
                            form=form,
                            error=error
                            )

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account-profile')
@login_required
def account_profile():
    profile_data = current_user.profile
    if profile_data:
        for item in profile_data:
            profile_image = item.image_file
    else: 
        profile_image='default.jpg'
    image_file = url_for('static', filename='images/profile-pics/' + profile_image)
    return render_template('account-profile.html',
                            title='Account and Profile',
                            image_file=image_file,
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
    form = ProfileForm()
    image_file = url_for('static', filename='images/profile-pics/' + current_user.image_file)
    if form.validate_on_submit():
        profile = Profile(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        phone_number=form.phone_number.data,
                        twitter=form.twitter.data,
                        facebook=form.facebook.data,
                        user=current_user)
        db.session.add(profile)
        db.session.commit()
        flash(f'Profile created!', 'success')
        return redirect(url_for('account_profile'))
    return render_template('create-profile.html',
                            form=form,
                            )


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    profile_data = current_user.profile
    for item in profile_data:
                display_profile_picture = item.image_file
    #update database info
    if form.validate_on_submit():
        #check if new picture 
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            for item in profile_data:
                item.image_file=picture_file
        for item in profile_data:
            item.first_name = form.first_name.data
            item.last_name=form.last_name.data
            item.phone_number=form.phone_number.data
            item.twitter=form.twitter.data
            item.facebook=form.facebook.data
            
        db.session.commit()
        flash(
            f'profile updated!', 'success')
        return redirect(url_for('account_profile'))
    # display info inside form
    elif request.method == 'GET':
        for item in profile_data:
            form.first_name.data = item.first_name
            form.first_name.data = item.first_name
            form.last_name.data =  item.last_name
            form.phone_number.data = item.phone_number
            form.twitter.data = item.twitter
            form.facebook.data = item.facebook    
    image_file = url_for('static', filename='images/profile-pics/' + display_profile_picture)
    return render_template('edit-profile.html',
                            form=form,
                            image_file=image_file,
                            title='Update profile',
                            map_key=app.config['GOOGLE_MAPS_API_KEY']
                            )


@app.route('/update-account', methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(
            f'account updated!', 'success')
        return redirect(url_for('account_profile')) #- can i render a button here? on no redirect at all?
    elif request.method == 'GET': # populates form field with current data
        form.username.data = current_user.username
        form.email.data = current_user.email
    #remove image? i think this should only be in profile
    image_file = url_for('static', filename='images/profile-pics/' + current_user.image_file)
    return render_template('update-account.html', form=form, image_file=image_file)



@app.route('/activity/new', methods=['GET', 'POST'])
@login_required
def new_activity():
    profile=current_user.profile
    for item in profile:
        profile_id = item.id
    form = CreateActivityForm()
    form.activity_type.choices = [(item.id, item.name) for item in ActivityType.query.all()]
    if form.validate_on_submit():
        activity = Activity(
            title=form.title.data, 
            description=form.description.data,
            address=form.address.data,
            location=Activity.point_representation(form.lat.data, form.lng.data),
            activity_type_id=form.activity_type.data,
            profile_id=profile_id
            )
        db.session.add(activity)
        db.session.commit()
        flash(
            f'new activity posted!', 'success')
        return redirect(url_for('home')) 
    return render_template('new-activity.html', 
                            title='New Activity',
                            form=form,
                            profile=profile,
                            map_key=app.config['GOOGLE_MAPS_API_KEY'],
                            legend='New Activity',
                            )


@app.route('/activity/<int:activity_id>')
@login_required
def view_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    return render_template('view-activity.html', 
                            title=activity.title, 
                            activity=activity)

@app.route('/activity/<int:activity_id>/update', methods=['GET', 'POST'])
@login_required
def update_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    #checks that only the owner of post can update this 
    if activity.profile.id != current_user.profile[0].id:
        abort(403)
    form = CreateActivityForm()
    if form.validate_on_submit():
        activity.title = form.title.data
        activity.description = form.description.data
        activity.street_address=form.street_address.data
        activity.location=Activity.point_representation(form.lat.data, form.lng.data),
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('view_activity', activity_id=activity.id))
    elif request.method == 'GET':
        form.title.data = activity.title
        form.description.data = activity.description
        form.street_address.data = activity.street_address
    return render_template('new-activity.html', 
                            title='Update Activity',
                            form=form,
                            legend='Update Post',
                            activity=activity)

@app.route('/activity/<int:activity_id>/delete', methods=['POST'])
@login_required
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if activity.profile.id != current_user.profile[0].id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))



#JSON API route 
# here i can set a route to create an api url 
# within the function i will create a dictionary using the db data and return this dictionary as json (jsonify) 

@app.route('/api/get_activities')
def api_all():
   # here the lat, lng, and radius is called from the API url created in js file  
    lat = float(request.args.get('lat'))
    lng = float(request.args.get('lng'))
    radius = int(request.args.get('radius'))
 

    activites = Activity.get_activities_within_radius(lat=lat, lng=lng, radius=radius)
    # activites = Activity.query.all()
    output = []
    for item in activites:
        output.append(item.to_dict())
    return jsonify(output)
  