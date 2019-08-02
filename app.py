import re
from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy		# database ORM import
from sqlalchemy.sql import func
from sqlalchemy import desc
from flask_migrate import Migrate			# used by SQLAlchemy to actually create db/tables
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'I drink and I know things'
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///j_mikes_bar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# User Database
# Id
# Admin flag
# First Name
# Last Name
# Username
# Email 
# Password
# Over 21?
# Events Interested In
	# not implemented yet, still developing desired function
	# possibly disregard "signing up" for events?
# Date Created
# Date Updated
class User(db.Model):	
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(255))
	last_name = db.Column(db.String(255))
	username = db.Column(db.String(255))
	email = db.Column(db.String(255))
	password = db.Column(db.String(255))
	legal_drinker_flag = db.Column(db.Boolean, default=False)
	date_created = db.Column(db.DateTime, server_default=func.now())
	date_updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())


class Admin(db.Model):
	__tablename__ = "admins"
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	date_created = db.Column(db.DateTime, server_default=func.now())

# Events Database
# id
# name
# date
# time
# coordinator
# Type (foreign key 1 to many relationship)
# Created by
# Date created
# Date updated
# Attendees (foreign key 1 to many relationship)
	# possibly disregard "signing up" for events?
# class Event(db.Model):	
# 	__tablename__ = "events"
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(255))
# 	time = db.Column(db.DateTime)
# 	coordinator = db.Column(db.String(255))
# 	event_type = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)
# 	created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #might need to change to admin table
# 	date_created = db.Column(db.DateTime, server_default=func.now())
# 	date_updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

# Events Type Database
# id
# Name
# Short description
# Events of type (backref)
# class Type(db.Model):
# 	__tablename__ = "types"
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(255))
# 	description = db.Column(db.Text)
# 	events_of_type = db.relationship('Event', backref='events_type_info')
# 	is_active = db.Column(db.Boolean, server_default=True)
# 	date_created = db.Column(db.DateTime, server_default=func.now())
# 	date_updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

# Food Menu
# Id
# Name
# Price
# Description
# Created by
# Date Created
# Date Updated
class Food(db.Model):
	__tablename__ = "foods"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	price = db.Column(db.Numeric(5,2))
	description = db.Column(db.Text)
	category = db.Column(db.Integer) # 1 = app, 2 = entree
	created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #might need to change to admin table
	is_active = db.Column(db.Boolean, default=True)
	date_created = db.Column(db.DateTime, server_default=func.now())
	date_updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

# Beer Taps
# Id
# Brewery Name
# Beer Name
# Beer type
# ABV
# IBU
# Gas type
	# changed to 'nitro_flag'
class Beer(db.Model):
	__tablename__ = "beers"
	id = db.Column(db.Integer, primary_key=True)
	brewery_name = db.Column(db.String(255))
	beer_name = db.Column(db.String(255))
	beer_type = db.Column(db.String(255))
	price = db.Column(db.Numeric(5,2))
	description = db.Column(db.Text)
	abv = db.Column(db.Numeric(2,1))
	ibu = db.Column(db.Integer)
	nitro_flag = db.Column(db.Boolean, default=False)
	created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #might need to change to admin table
	is_active = db.Column(db.Boolean, default=True)
	date_created = db.Column(db.DateTime, server_default=func.now())
	date_updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

# Liquor
# Id
# Name
# Type
# ABV
class Liquor(db.Model):
	__tablename__ = "liquors"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	brand = db.Column(db.String(255))
	price = db.Column(db.Numeric(5,2))
	liquor_type = db.Column(db.Text)
	abv = db.Column(db.Numeric(2,1))
	created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #might need to change to admin table
	is_active = db.Column(db.Boolean, default=True)
	date_created = db.Column(db.DateTime, server_default=func.now())
	date_updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())




################
## ROOT ROUTE ##
################
@app.route("/")
def index():
	return render_template("index.html")


##########################################
## VALIDATE FORM DATA and REGISTER USER ##
##########################################
@app.route('/submit/signup', methods=['POST'])
def user_signup():
	is_valid = True
	EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
	NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
	USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9_-]+$')
	# Password regex - uppercase, lowercase, and number required
	PW_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$')

	# Validate name fields
	if len(request.form['fname']) < 2 or len(request.form['lname']) < 2:
		flash("Both your first and last name must be at least 2 characters long.", 'reg_error')
		is_valid = False
	else:
		if NAME_REGEX.match(request.form['fname']) is None or NAME_REGEX.match(request.form['lname']) is None:
			flash("Your name can only contain letters.", 'reg_error')
			is_valid = False

	# Validate username
	if len(request.form['uname']) < 3:
		flash("Your username must be at least 3 characters long.", 'reg_error')
		is_valid = False
	else:
		if USERNAME_REGEX.match(request.form['uname']) is None:
			flash("Your username can only contain letters and numbers.", 'reg_error')
			is_valid = False
		else:
			checkUsername = User.query.filter_by(username=request.form['uname']).first()
			if checkUsername:
				flash("Account already exists with this username.", 'reg_error')
				is_valid = False

	if EMAIL_REGEX.match(request.form['email']):
		checkEmail = User.query.filter_by(email=request.form['email']).first()
		if checkEmail:
			flash("Account already exists with this Email.", 'reg_error')
			is_valid = False
	else:
		flash("Email address not valid.", 'reg_error')
		is_valid = False

	# Validate Password
	if len(request.form['password']) < 5:
		flash("Password must be a minimum of 5 characters.", 'reg_error')
		is_valid = False
	elif PW_REGEX.match(request.form['password']) is None:
		flash("Password requires at least one uppercase, one lowercase letter, and a number.", 'reg_error')
		is_valid = False
	else:
		if request.form['confirm_password'] != request.form['password']:
			flash("Passwords did not match.", 'reg_error')
			is_valid = False

	# Record data and flash success
	if is_valid:
		new_instance_of_user = User(admin_flag=request.form['admin_flag'], first_name=request.form['fname'], last_name=request.form['lname'], username=request.form['uname'], email=request.form['email'], password=bcrypt.generate_password_hash(request.form['password']), legal_drinker_flag=request.form['legal_age'])
		db.session.add(new_instance_of_user)
		db.session.commit()
		session['userid'] = new_instance_of_user.id
		session['name'] = request.form['uname']

		return redirect('/')

	return redirect('/signup')


######################
## USER SIGNUP FORM ##
######################
@app.route('/signup')
def signup_form():
	if 'userid' in session:
		return redirect('/')

	return render_template('signup.html')


#########################
## VALIDATE USER LOGIN ##
#########################
@app.route('/user/validate/login', methods=['POST'])
def validate_login():
	loginUser = User.query.filter_by(email=request.form['email']).first()

	if loginUser:
		pw = bcrypt.check_password_hash(loginUser.password, request.form['password'])

		if pw:
			session['userid'] = loginUser.id
			session['name'] = loginUser.username
			return redirect('/')
		else:
			flash("Password incorrect! Please try again.", 'login_error')
	else:
		flash("Email not recognized", 'login_error')

	return redirect('/login')


#####################
## USER LOGIN FORM ##
#####################
@app.route('/login')
def login_form():
	if 'userid' in session:
		return redirect('/')

	return render_template('index.html?login_form=1')


#####################
## USER LOGIN FORM ##
#####################
@app.route('/contactus')
def contactus_page():
	return render_template('contactus.html')


#####################
## USER LOGIN FORM ##
#####################
@app.route('/calendar')
def calendar_page():
	return render_template('calendar.html')


#####################
## USER LOGIN FORM ##
#####################
@app.route('/admin')
def admin_page():
	return render_template('admin.html')


#####################
## USER LOGIN FORM ##
#####################
@app.route('/thanks')
def thanks_page():
	return render_template('thanks.html')



############
## LOGOUT ##
############
@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')


#########################################################################################
## 								ADMIN ONLY ACCESS 									   ##
#########################################################################################
######################
## UPDATE FOOD MENU ##
######################
@app.route('/update/food', methods=['POST'])
def update_food_menu():
	# perform check for Admin access BEFORE updating

	# ADD
	# UPDATE
	# MAKE INACTIVE
	# DELETE
	pass


######################
## UPDATE BEER MENU ##
######################
@app.route('/update/beer', methods=['POST'])
def update_beer_menu():
	# perform check for Admin access BEFORE updating

	# ADD
	# UPDATE
	# MAKE INACTIVE
	# DELETE
	pass


########################
## UPDATE LIQUOR MENU ##
########################
@app.route('/update/liquor', methods=['POST'])
def update_liquor_menu():
	# perform check for Admin access BEFORE updating

	# ADD
	# UPDATE
	# MAKE INACTIVE
	# DELETE
	pass


###################
## UPDATE EVENTS ##
###################
@app.route('/update/event', methods=['POST'])
def update_event():
	# perform check for Admin access BEFORE updating

	# ADD
	# UPDATE
	# DELETE
	pass


########################
## UPDATE EVENT TYPES ##
########################
@app.route('/update/event/type', methods=['POST'])
def update_event_type():
	# perform check for Admin access BEFORE updating

	# ADD
	# UPDATE
	# MAKE INACTIVE
	# DELETE
	pass




if __name__=="__main__":
	app.run(debug=True)

    