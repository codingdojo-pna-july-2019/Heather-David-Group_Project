import re
from flask import flash
from sqlalchemy.sql import func
from datetime import datetime
from config import db, bcrypt

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

	# Class Methods
	@classmethod
	def validate_user_signup(cls, user_data):
		is_valid = cls.validate_user_first_name(user_data["fname"])
		if is_valid:
			is_valid = cls.validate_user_last_name(user_data["lname"])
		if is_valid:
			is_valid = cls.validate_user_name(user_data["uname"])
		if is_valid:
			is_valid = cls.validate_user_email(user_data["email"])
		if is_valid:
			is_valid = cls.validate_user_password(user_data["password"], user_data["confirm_password"])
		return is_valid

	@classmethod
	def validate_user_first_name(cls, fname):
		is_valid = True
		NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
		if len(fname) < 2:
			flash("Both your first and last name must be at least 2 characters long.", 'err_fname')
			is_valid = False
		else:
			if NAME_REGEX.match(fname) is None:
				flash("Your name can only contain letters.", 'err_fname')
				is_valid = False

		return is_valid

	@classmethod
	def validate_user_last_name(cls, lname):
		is_valid = True
		NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

		if len(lname) < 2:
			flash("Both your first and last name must be at least 2 characters long.", 'err_lname')
			is_valid = False
		else:
			if NAME_REGEX.match(user_data['lname']) is None:
				flash("Your name can only contain letters.", 'err_lname')
				is_valid = False

		return is_valid

	@classmethod
	def validate_user_name(cls, uname):
		is_valid = True
		USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9_-]+$')
		if len(uname) < 3:
			flash("Your username must be at least 3 characters long.", 'err_uname')
			is_valid = False
		else:
			if USERNAME_REGEX.match(uname) is None:
				flash("Your username can only contain letters and numbers.", 'err_uname')
				is_valid = False
			else:
				checkUsername = cls.query.filter_by(username=uname).first()
				if checkUsername:
					flash("Account already exists with this username.", 'err_uname')
					is_valid = False

		return is_valid

	@classmethod
	def validate_user_email(cls, email):
		is_valid = True
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		if EMAIL_REGEX.match(email):
			checkEmail = cls.query.filter_by(email=email).first()
			if checkEmail:
				flash("Account already exists with this Email.", 'err_email')
				is_valid = False
		else:
			flash("Email address not valid.", 'err_email')
			is_valid = False

		return is_valid

	@classmethod
	def validate_user_password(cls, password, confirm_password):
		is_valid = True
		# Password regex - uppercase, lowercase, and number required
		PW_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$')
		if len(password) < 5:
			flash("Password must be a minimum of 5 characters.", 'err_pw')
			is_valid = False
		elif PW_REGEX.match(password) is None:
			flash("Password requires at least one uppercase, one lowercase letter, and a number.", 'err_pw')
			is_valid = False
		else:
			if not cls.validate_user_password_sameness(password, confirm_password):
				flash("Passwords did not match.", 'err_pw')
				is_valid = False

		return is_valid

	@classmethod
	def validate_user_password_sameness(cls, password, confirm_password):
		if confirm_password != password:
			return False
		else:
			return True

	@classmethod
	def add_new_user(cls, user_data):
		new_instance_of_user = cls(first_name=user_data['fname'], last_name=user_data['lname'], username=user_data['uname'], email=user_data['email'], password=bcrypt.generate_password_hash(user_data['password']), legal_drinker_flag=user_data['legal_age'])
		db.session.add(new_instance_of_user)
		db.session.commit()
		return new_instance_of_user


class Admin(db.Model):
	__tablename__ = "admins"
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	date_created = db.Column(db.DateTime, server_default=func.now())

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