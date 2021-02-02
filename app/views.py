from flask import Flask, render_template, url_for
from app import app

#this would be called from the database
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
    return render_template('home.html' )

@app.route('/landing-page')
def landing-page():
    return render_template('landing-page.html')

@app.route('/login')
def login():
    return render_template('login.html', title='Login')


@app.route('/signup')
def sign_up():
    return render_template('sign-up.html', title='Sign Up')

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