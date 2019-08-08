import re
from flask import flash, session
from sqlalchemy import not_
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
	events_flag_karaoke = db.Column(db.Boolean, default=False)
	events_flag_trivia = db.Column(db.Boolean, default=False)
	events_flag_billiards = db.Column(db.Boolean, default=False)
	events_flag_football = db.Column(db.Boolean, default=False)
	events_flag_potluck = db.Column(db.Boolean, default=False)
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
			if NAME_REGEX.match(lname) is None:
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
			is_valid = cls.validate_user_password_sameness(password, confirm_password)

		return is_valid

	@classmethod
	def validate_user_password_sameness(cls, password, confirm_password):
		if confirm_password != password:
			flash("Passwords did not match.", 'err_pw_confirm')
			return False
		else:
			return True

	@classmethod
	def add_new_user(cls, user_data):
		karaoke_flag = False
		trivia_flag = False
		billiards_flag = False
		sunday_football_flag = False
		potluck_flag = False
		if 'karaoke' in user_data:
			karaoke_flag = True
		if 'trivia' in user_data:
			trivia_flag = True
		if 'billiards' in user_data:
			billiards_flag = True
		if 'sunday_football' in user_data:
			sunday_football_flag = True
		if 'potluck' in user_data:
			potluck_flag = True
		new_instance_of_user = cls(first_name=user_data['fname'], last_name=user_data['lname'], username=user_data['uname'], email=user_data['email'], password=bcrypt.generate_password_hash(user_data['password']), events_flag_karaoke=karaoke_flag, events_flag_trivia=trivia_flag, events_flag_billiards=billiards_flag, events_flag_football=sunday_football_flag, events_flag_potluck=potluck_flag)
		db.session.add(new_instance_of_user)
		db.session.commit()
		return new_instance_of_user


class Admin(db.Model):
	__tablename__ = "admins"
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	date_created = db.Column(db.DateTime, server_default=func.now())

	# Class Methods
	@classmethod
	def add_admin_user(cls, cur_user, user_to_add):
		if cur_user == 1:
			new_admin = User.query.filter_by(email=user_to_add).first()
			if new_admin:
				new_instance_of_admin = cls(userid=new_admin.id, created_by=cur_user)
				db.session.add(new_instance_of_admin)
				db.session.commit()
			else:
				flash("User email not recognized.  Cannot add user as Admin.", 'err_new_admin')
			# return new_instance_of_admin
		else:
			flash("You are not authorized to perform this action", 'err_new_admin')

	@classmethod
	def delete_admin_user(cls, admin_id):
		item = cls.query.get(admin_id)
		db.session.delete(item)
		db.session.commit()

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
	category = db.Column(db.Integer) # 1 = app, 2 = soup/salad, 3 = burgers, 4 = steak, 5 = sandwiches, 6 = specials
	created_by = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
	is_active = db.Column(db.Boolean, default=True)
	date_created = db.Column(db.DateTime, server_default=func.now())
	date_updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

	# Class Methods
	@classmethod
	def validate_food_item(cls, food_data):
		MONEY_REGEX = re.compile(r'^([0-9]{1,5}\.[0-9]{1,2})?$')
		is_valid = True

		if len(food_data["food_name"]) < 2:
			flash("The name of the food item must be at least 2 characters long.", 'err_food')
			is_valid = False
		if len(food_data["food_price"]) > 1:
			if MONEY_REGEX.match(food_data["food_price"]) is None:
				flash("The item's price is not in dollar format.", 'err_food')
				is_valid = False
		else:
			flash("Please enter a price for the menu item.", 'err_food')
			is_valid = False
		if int(food_data["food_category"]) < 1 or int(food_data["food_category"]) > 6:
			flash("Please select a valid menu category.", 'err_food')
			is_valid = False

		return is_valid

	@classmethod
	def add_food_item(cls, food_data):
		# print(food_data)
		new_instance_of_food = cls(name=food_data["food_name"], price=food_data["food_price"], description=food_data["food_description"], category=food_data["food_category"], created_by=session["userid"])
		db.session.add(new_instance_of_food)
		db.session.commit()
		return new_instance_of_food

	@classmethod
	def update_food_status(cls, active_food_list):
		active_list = cls.query.filter(cls.id.in_(active_food_list)).all()
		not_active_list = cls.query.filter(not_(cls.id.in_(active_food_list))).all()

		for item in active_list:
			item.is_active = True

		for item in not_active_list:
			item.is_active = False

		db.session.commit()

	@classmethod
	def update_food_item(cls, food_id):
		pass

	@classmethod
	def delete_food_item(cls, food_id):
		item = cls.query.get(food_id)
		db.session.delete(item)
		db.session.commit()

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
	beer_type = db.Column(db.String(255)) # Ale, Lager, IPA, etc.
	price = db.Column(db.Numeric(5,2))
	description = db.Column(db.Text)
	abv = db.Column(db.Numeric(2,1))
	ibu = db.Column(db.Integer)
	nitro_flag = db.Column(db.Boolean, default=False)
	created_by = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
	is_active = db.Column(db.Boolean, default=True)
	date_created = db.Column(db.DateTime, server_default=func.now())
	date_updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

	# Class Methods
	@classmethod
	def validate_beer_item(cls, beer_data):
		MONEY_REGEX = re.compile(r'^([0-9]{1,5}\.[0-9]{1,2})?$')
		ABV_REGEX = re.compile(r'^([0-9]{1,2}\.[0-9]{1,1})?$')
		is_valid = True

		if len(beer_data["brewery_name"]) < 2:
			flash("Please enter the name of the brewery.", 'err_beer')
			is_valid = False
		if len(beer_data["beer_name"]) < 2:
			flash("Please enter the name of the beer.", 'err_beer')
			is_valid = False
		if len(beer_data["beer_type"]) < 2:
			flash("Please enter the style of beer.", 'err_beer')
			is_valid = False
		if len(beer_data["beer_price"]) > 1:
			if MONEY_REGEX.match(beer_data["beer_price"]) is None:
				flash("The item's price is not in dollar format.", 'err_beer')
				is_valid = False
		else:
			flash("Please enter a price for the beer.", 'err_beer')
			is_valid = False
		if len(beer_data["beer_abv"]) > 1:
			if ABV_REGEX.match(beer_data["beer_abv"]) is None:
				flash("The beer's ABV is not in the proper format.", 'err_beer')
				is_valid = False
		else:
			flash("Please enter the ABV of the beer.", 'err_beer')
			is_valid = False
		if len(beer_data["beer_type"]) < 2:
			flash("Please enter the style of beer.", 'err_beer')
			is_valid = False

		return is_valid

	@classmethod
	def add_beer_item(cls, beer_data):
		if "nitro_beer" not in beer_data:
			nitro_beer = False
		if len(beer_data["beer_ibu"]) < 1:
			beer_data["beer_ibu"] = 0

		new_instance_of_beer = cls(brewery_name=beer_data["brewery_name"], beer_name=beer_data["beer_name"], beer_type=beer_data["beer_type"], price=beer_data["beer_price"], description=beer_data["beer_desc"], abv=beer_data["beer_abv"], ibu=beer_data["beer_ibu"], nitro_flag=nitro_beer, created_by=session["userid"])
		db.session.add(new_instance_of_beer)
		db.session.commit()
		return new_instance_of_beer

	@classmethod
	def update_beer_status(cls, active_beer_list):
		active_list = cls.query.filter(cls.id.in_(active_beer_list)).all()
		not_active_list = cls.query.filter(not_(cls.id.in_(active_beer_list))).all()

		for item in active_list:
			item.is_active = True

		for item in not_active_list:
			item.is_active = False

		db.session.commit()

	@classmethod
	def update_beer_item(cls, food_id):
		pass

	@classmethod
	def delete_beer_item(cls, beer_id):
		item = cls.query.get(beer_id)
		db.session.delete(item)
		db.session.commit()

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
	proof = db.Column(db.Integer)
	created_by = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
	is_active = db.Column(db.Boolean, default=True)
	date_created = db.Column(db.DateTime, server_default=func.now())
	date_updated = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

	# Class Methods
	@classmethod
	def validate_liquor_item(cls, liq_data):
		MONEY_REGEX = re.compile(r'^([0-9]{1,5}\.[0-9]{1,2})?$')
		PROOF_REGEX = re.compile(r'^([0-9]{1,3})?$')
		is_valid = True

		if len(liq_data["liq_name"]) < 2:
			flash("Please enter the name of the liquor.", 'err_liq')
			is_valid = False
		if len(liq_data["liq_brand"]) < 2:
			flash("Please enter the brand of the liquor.", 'err_liq')
			is_valid = False
		if len(liq_data["liq_type"]) < 2:
			flash("Please enter the type of liquor.", 'err_liq')
			is_valid = False
		if len(liq_data["liq_price"]) > 1:
			if MONEY_REGEX.match(liq_data["liq_price"]) is None:
				flash("The item's price is not in dollar format.", 'err_liq')
				is_valid = False
		else:
			flash("Please enter a price for the liquor.", 'err_liq')
			is_valid = False
		if len(liq_data["liq_proof"]) > 1:
			if PROOF_REGEX.match(liq_data["liq_proof"]) is None:
				flash("The liquor's proof is not in the proper format.", 'err_liq')
				is_valid = False
		else:
			flash("Please enter a proof for the liquor (0 to disregard).", 'err_liq')
			is_valid = False

		return is_valid

	@classmethod
	def add_liquor_item(cls, liq_data):
		# set nitro flag in calling function and add to request.form before call
		new_instance_of_liq = cls(name=liq_data["liq_name"], brand=liq_data["liq_brand"], price=liq_data["liq_price"], liquor_type=liq_data["liq_type"], proof=liq_data["liq_proof"], created_by=session["userid"])
		db.session.add(new_instance_of_liq)
		db.session.commit()
		return new_instance_of_liq

	@classmethod
	def update_liquor_status(cls, active_liq_list):
		active_list = cls.query.filter(cls.id.in_(active_liq_list)).all()
		not_active_list = cls.query.filter(not_(cls.id.in_(active_liq_list))).all()

		for item in active_list:
			item.is_active = True

		for item in not_active_list:
			item.is_active = False

		db.session.commit()

	@classmethod
	def update_liquor_item(cls, food_id):
		pass

	@classmethod
	def delete_liquor_item(cls, liq_id):
		item = cls.query.get(liq_id)
		db.session.delete(item)
		db.session.commit()