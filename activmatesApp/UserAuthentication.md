###User Authentication 
`pip install flask-bcrypt`
run python in terminal 
    ```>>>from flask_bcrypt import Bcrypt
    >>> bcrypt = Bcrypt()
    >>> bcrypt.generate_password_hash('testing')
    >>> bcrypt.generate_password_hash('testing').decode('utf-8')```
check password hash
    hashed_pw = bcrypt.generate_password_hash('testing').decode('utf-8')
    bcrpyt.check_password_hash(hashed_pw, 'testing') 
should return true 

go back to __init__.py 
    from flask_bcrypt import Bcrypt
underneath the other initialisation lines add 
    bcrypt = Bcrypt(app)

go to routes.oy
check route - registration form 
if form is valid on submit we want to hash the password here we want to 
import db and bcrypt at top of pages 
`from appfolder import , db, bcrypt`
underneath `if validate_on_submit():`
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8)

create a new instance of a user to check it works 
    user = User(username=NameOfForm.username.data, email=NameOfForm.email.data, password=hashed_password)
add to database
    db.session.add(user)
    db.session.commit()    

change message - your account has been created - you are now able to login 
return to login or profile 

check the user is added to db - run app and create user 

start python in terminal 
    >>> from appfolder import db
    >>> from appfolder.models import User
    >>> user = User.query.first()
    >>> user 
    >>> user.password 
should show hashed password 

GO BACK - we need to prevent the user creating profile with same email 
- throws flask error 
- we want to add custom validation on the form 
- WTForms documentions 

in form file inside the class of the form you want to validate,e g. registration form  insert a function to validate 
this is the template for validation conditional-:

    def validate_field(self, field):
        if True:
            raise ValidationError('Validation Message')

now customise 
import user model from models file 
`from appfolder.models import User`
ìmport validation error - add to 
`from wtforms_validators import ,,,, ValidationError`

in the function below - we create a variable which searches through the databas for a match (username=username.data) if a match is returned then the conditional will execute

    def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user :
            raise ValidationError('That username is taken, please choose a different one')

do the same for email etc. 






for LOGIN 
flask-login ext 
`pip install flask-login`
add in init file 
`from flask_login import LoginManager`
below ext list 
`login_manager = LoginManager(app)` - handles all   of the login sessions 
in models file import 
`from appfolder import login_manager`
`from flask_login import UserMixin`
function to load the user taking user id as argument and return user 
ext expects user model to have 4 attributes and methods - import UserMixin class to do this for us
is authenticated
is active 
is anon
get id 
pass UserMixin to db.Model class

	@login_manager.user_loader - this is a decorator
	def load_user(user_id):
		return User.query.get(int(user_id))

modify login route to check db if username and password are valid
routes file 
`from flask_login import login_user`
remove conditionals that i have already and add:
check if user exists and if password verifies
	user = USer.query.filter_by(emial=form.email.data).first()
	if user and bcrypt.check_password_hash(user.password, form.password.data):    - function take in dbpassword and password entered to check if it is correct -
		login_user(user, remember=form.remember.data)
		return redirect(url_for('home'))
	else:
		flash error


update navbar for login state 
routes file 
`from flask_login import current_user`
in register route 
	if current.user.is_authenticated: 
		return redirect(url_for('home'))

CREATE LOGOUT ROUTE
`from flask_login import logout`

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

go back to layout template 
to nav links 
jinja2 conditional 
	{% if current_user.is_authenticated %}
	logout links 
	{% else %}
	login links
	{% endif %}

restricton on route only if logged in 
routes file 
create route for users account to acces when logged in - profile template 
`from flask_loing import login_required` - add decorator 

	@app.route("/account")
	@login_required
	def account():
		return render_template('template name', title= 'title name')

go to init file 
in list of ext - set login route 
`login_manager.login_view = 'login'`
redirects to login page	function name of route 
`login_manager.login_message_category = 'info'`
info is the bootstrap class


redirect to page you wanted to go to before redirected to login page
routes file
`from flask import ,,, request`
go to login route 
under login_user 
	next_page = request.args.get('next')
add to return 
	return redirect(next_page) if next_page else redirect(url_for('home'))
