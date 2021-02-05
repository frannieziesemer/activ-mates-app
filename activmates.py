from flask import Flask, render_template, url_for, flash, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, CreateProfileForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '36678eaa6a847166122011a8472d4f21'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    profile = db.relationship('Profile', backref='account_holder', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.type}')"


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    street_address = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    postcode = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    twitter = db.Column(db.String(20), nullable=False)
    facebook = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.image_file}', '{self.street_address}', , '{self.city}', '{self.postcode}', '{self.phone_number}', '{self.twitter}', , '{self.facebook}')"


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey(
        'profile.id'), nullable=False)
    activity_type = db.relationship(
        'ActivityType', backref='activity_type', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.image_file}', '{self.description}')"


class ActivityType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey(
        'activity.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.number}', '{self.naem}')"


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


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login')


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    registrationForm = RegistrationForm()
    if registrationForm.validate_on_submit():
        # alert message
        flash(
            f'Account created for {registrationForm.username.data}!', 'success')
        # redirect on submit and validation # !!!!!here i want new profile section to show
        # return redirect(url_for('home'))
    createProfileForm = CreateProfileForm()
    return render_template('sign-up.html',
                           title='Sign Up',
                           registrationForm=registrationForm,
                           createProfileForm=createProfileForm
                           )


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


if __name__ == '__main__':
    app.run(debug=True)
