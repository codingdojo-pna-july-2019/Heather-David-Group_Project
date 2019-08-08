import re
import tweepy
from flask import render_template, redirect, request, session, url_for, json
from sqlalchemy import desc
from config import db, api, bcrypt
from models import User, Admin, Food, Beer, Liquor

################
## ROOT ROUTE ##
################
def index():
	# if 'userid' in session:
	# 	if session['userid'] == 1:
	# 		temp = Admin.add_admin_user(session['userid'], session['userid'])
	twitter_search_q = '#FortniteWorldCup'
	cur_tweet_ids = []
	for tweet in tweepy.Cursor(api.search, q=twitter_search_q, lang='en').items(10):
		cur_tweet_ids.append(tweet.id)

	return render_template("index.html", cur_tweets=cur_tweet_ids, cur_tweet_q=twitter_search_q, all_food=Food.query.order_by(Food.category, Food.name).all(), all_beers=Beer.query.order_by(Beer.brewery_name, Beer.beer_name).all(), all_liquors=Liquor.query.order_by(Liquor.liquor_type, Liquor.brand, Liquor.name).all())


######################
## USER SIGNUP FORM ##
######################
def signup_form():
	if 'userid' in session:
		return redirect('/')

	return render_template('signup.html')


##########################################
## VALIDATE FORM DATA and REGISTER USER ##
##########################################
def user_signup():
	if 'userid' in session:
		return redirect('/')

	# print(request.form)
	is_valid = User.validate_user_signup(request.form)

	# Record data and flash success
	if is_valid:
		new_user = User.add_new_user(request.form)
		session['userid'] = new_user.id
		session['name'] = request.form['uname']
		return redirect('/')

	return redirect('/signup')


#####################
## USER LOGIN FORM ##
#####################
def login_form():
	if 'userid' in session:
		return redirect('/')

	# return render_template('index.html?login_form=1')
	return render_template('login.html')


#########################
## VALIDATE USER LOGIN ##
#########################
def validate_login():
	if 'userid' in session:
		return redirect('/')

	loginUser = User.query.filter_by(email=request.form['email']).first()

	if loginUser:
		pw = bcrypt.check_password_hash(loginUser.password, request.form['password'])

		if pw:
			session['userid'] = loginUser.id
			session['name'] = loginUser.username
			return redirect('/')
		else:
			flash("Password incorrect! Please try again.", 'login_error_pw')
	else:
		flash("Email not recognized", 'login_error_email')

	return redirect('/login')


#####################
## CONTACT US PAGE ##
#####################
def contactus_page():
	fullName = ""
	userEmail = ""

	if 'userid' in session:
		curUser = User.query.get(session['userid'])
		fullName = curUser.first_name + " " + curUser.last_name
		userEmail = curUser.email

	return render_template('contactus.html', user_name=fullName, user_email=userEmail)


########################
## CALENDAR OF EVENTS ##
########################
def calendar_page():
	return render_template('calendar.html')


####################
## THANK YOU PAGE ##
####################
def thanks_page():
	return render_template('thanks.html')



############
## LOGOUT ##
############
def logout():
	session.clear()
	return redirect('/')


#########################################################################################
## 								    AJAX ROUTES									   	   ##
#########################################################################################
def ajax_validate_user_first_name():
	if not User.validate_user_first_name(request.form["fname"]):
		return render_template('partials/errors/err_fname.html')
	else:
		return ''
def ajax_validate_user_last_name():
	if not User.validate_user_last_name(request.form["lname"]):
		return render_template('partials/errors/err_lname.html')
	else:
		return ''
def ajax_validate_user_name():
	if not User.validate_user_name(request.form["uname"]):
		return render_template('partials/errors/err_uname.html')
	else:
		return ''
def ajax_validate_user_email():
	if not User.validate_user_email(request.form["email"]):
		return render_template('partials/errors/err_email.html')
	else:
		return ''
def ajax_validate_user_password():
	if not User.validate_user_password(request.form["password"], request.form["confirm_password"]):
		return render_template('partials/errors/err_pw.html')
	else:
		return ''
def ajax_validate_user_password_sameness():
	if not User.validate_user_password_sameness(request.form["password"], request.form["confirm_password"]):
		return render_template('partials/errors/err_pw_confirm.html')
	else:
		return ''


#########################################################################################
## 								ADMIN ONLY ACCESS 									   ##
#########################################################################################
################
## ADMIN PAGE ##
################
def admin_page():
	if 'userid' not in session:
		return redirect('/login')

	adminStatus = Admin.query.get(session['userid'])
	if adminStatus:
		return render_template('admin.html')

	return redirect('/')


########################
## ADD NEW ADMIN USER ##
########################
def admin_add_user():
	if 'userid' not in session:
		return redirect('/login')

	adminStatus = Admin.query.get(session['userid'])
	if adminStatus and session['userid'] == 1:
		Admin.add_admin_user(session['userid'], request.form['new_admin_email'])

	return redirect('/admin')


#######################
## REMOVE ADMIN USER ##
#######################
def admin_remove_user():
	if 'userid' not in session:
		return redirect('/login')

	adminStatus = Admin.query.get(session['userid'])
	if adminStatus and session['userid'] == 1:
		Admin.delete_admin_user(request.form)
		
	return redirect('/admin')


####################
## LOAD FOOD MENU ##
####################
def load_food_menu():
	return render_template('partials/admin_food.html', all_food=Food.query.order_by(Food.category, Food.name).all())


####################
## LOAD BEER MENU ##
####################
def load_beer_menu():
	return render_template('partials/admin_beer.html', all_beers=Beer.query.order_by(Beer.brewery_name, Beer.beer_name).all())


######################
## LOAD LIQUOR MENU ##
######################
def load_liquor_menu():
	return render_template('partials/admin_liquor.html', all_liquors=Liquor.query.order_by(Liquor.liquor_type, Liquor.brand, Liquor.name).all())


######################
## UPDATE FOOD MENU ##
######################
def update_food_menu():
	if 'userid' not in session:
		return redirect('/login')

	adminStatus = Admin.query.get(session['userid'])
	if adminStatus:
		# ADD
		if request.form['update_type'] == 'new':
			is_valid = Food.validate_food_item(request.form)
			if is_valid:
				Food.add_food_item(request.form)
		# MAKE ACTIVE/INACTIVE
		elif request.form['update_type'] == 'status':
			Food.update_food_status(request.form.getlist('food_id_cb'))
		# DELETE
		elif request.form['update_type'] == 'delete':
			Food.delete_food_item(request.form['food_id'])
		# UPDATE
		# elif

		return render_template('partials/admin_food.html', all_food=Food.query.order_by(Food.category, Food.name).all())

	return redirect('/')


######################
## UPDATE BEER MENU ##
######################
def update_beer_menu():
	if 'userid' not in session:
		return redirect('/login')

	adminStatus = Admin.query.get(session['userid'])
	if adminStatus:
		# ADD
		if request.form['update_type'] == 'new':
			is_valid = Beer.validate_beer_item(request.form)
			if is_valid:
				Beer.add_beer_item(request.form)
		# MAKE ACTIVE/INACTIVE
		elif request.form['update_type'] == 'status':
			Beer.update_beer_status(request.form.getlist('beer_id_cb'))
		# DELETE
		elif request.form['update_type'] == 'delete':
			Beer.delete_beer_item(request.form['beer_id'])
		# UPDATE
		# elif

		return render_template('partials/admin_beer.html', all_beers=Beer.query.order_by(Beer.brewery_name, Beer.beer_name).all())

	return redirect('/')


########################
## UPDATE LIQUOR MENU ##
########################
def update_liquor_menu():
	if 'userid' not in session:
		return redirect('/login')

	adminStatus = Admin.query.get(session['userid'])
	if adminStatus:
		# ADD
		if request.form['update_type'] == 'new':
			is_valid = Liquor.validate_liquor_item(request.form)
			if is_valid:
				Liquor.add_liquor_item(request.form)
		# MAKE ACTIVE/INACTIVE
		elif request.form['update_type'] == 'status':
			Liquor.update_liquor_status(request.form.getlist("liq_id_cb"))
		# DELETE
		elif request.form['update_type'] == 'delete':
			Liquor.delete_liquor_item(request.form['liq_id'])
		# UPDATE
		# elif

		return render_template('partials/admin_liquor.html', all_liquors=Liquor.query.order_by(Liquor.liquor_type, Liquor.brand, Liquor.name).all())

	return redirect('/')